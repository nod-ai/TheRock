#!/usr/bin/env python
"""fileset_tool.py

Helper tool for manipulating filesets by listing matching files, copying,
archiving, etc. This is ultimately inspired by the fileset manipulation behavior
of Ant, which uses recursive glob include/exclude patterns rooted on some
base directory to manage artifact moving and packaging.

This is based on a limited form of the pathlib.Path pattern language introduced
in Python 3.13 (https://docs.python.org/3/library/pathlib.html#pattern-language)
with the following changes:

* It does not support character classes.
"""

from typing import Callable, Generator
import argparse
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys


class ComponentDefaults:
    """Defaults for to apply to artifact merging by component name."""

    ALL: dict[str, "ComponentDefaults"] = {}

    def __init__(self, name: str = "", includes=(), excludes=()):
        self.includes = list(includes)
        self.excludes = list(excludes)
        if name:
            if name in ComponentDefaults.ALL:
                raise KeyError(f"ComponentDefaults {name} already defined")
            ComponentDefaults.ALL[name] = self

    @staticmethod
    def get(name: str) -> "ComponentDefaults":
        return ComponentDefaults.ALL.get(name) or ComponentDefaults(name)


# Debug components collect all platform specific dbg file patterns.
ComponentDefaults("dbg", includes=["**/*.dbg"])
# Dev components include all static library based file patterns and
# exclude file name patterns implicitly included for "run" and "lib".
# Descriptors should explicitly include header file any package file
# sub-trees that do not have an explicit "cmake" or "include" path components
# in them.
ComponentDefaults(
    "dev",
    includes=[
        "**/*.a",
        "**/cmake/**",
        "**/include/**",
        "**/share/modulefiles/**",
        "**/pkgconfig/**",
    ],
    excludes=[],
)
# Lib components include shared libraries, dlls and any assets needed for use
# of shared libraries at runtime. Files are included by name pattern and
# descriptors should include/exclude non-standard variations.
ComponentDefaults(
    "lib",
    includes=[
        "**/*.dll",
        "**/*.dylib",
        "**/*.dylib.*",
        "**/*.so",
        "**/*.so.*",
    ],
    excludes=[],
)
# Run components layer on top of 'lib' components and also include executables
# and tools that are not needed by library consumers. Descriptors should
# explicitly include "bin" directory contents as needed.
ComponentDefaults("run")
ComponentDefaults("doc", includes=["**/share/doc/**"])

# To help layering, we make lib/dev/run default patterns exclude patterns
# that the others define. This makes it easier for one of these to do directory
# level includes and have the files sorted into the proper component.
ComponentDefaults.get("dev").excludes.extend(ComponentDefaults.get("lib").includes)
ComponentDefaults.get("dev").excludes.extend(ComponentDefaults.get("run").includes)
ComponentDefaults.get("dev").excludes.extend(ComponentDefaults.get("doc").includes)
ComponentDefaults.get("lib").excludes.extend(ComponentDefaults.get("dev").includes)
ComponentDefaults.get("lib").excludes.extend(ComponentDefaults.get("run").includes)
ComponentDefaults.get("lib").excludes.extend(ComponentDefaults.get("doc").includes)
ComponentDefaults.get("run").excludes.extend(ComponentDefaults.get("dev").includes)
ComponentDefaults.get("run").excludes.extend(ComponentDefaults.get("lib").includes)
ComponentDefaults.get("run").excludes.extend(ComponentDefaults.get("doc").includes)


class RecursiveGlobPattern:
    def __init__(self, glob: str):
        self.glob = glob
        pattern = f"^{re.escape(glob)}$"
        # Intermediate recursive directory match.
        pattern = pattern.replace("/\\*\\*/", "/(.*/)?")
        # First segment recursive directory match.
        pattern = pattern.replace("^\\*\\*/", "^(.*/)?")
        # Last segment recursive directory match.
        pattern = pattern.replace("/\\*\\*$", "(/.*)?$")
        # Intra-segment * match.
        pattern = pattern.replace("\\*", "[^/]*")
        # Intra-segment ? match.
        pattern = pattern.replace("\\?", "[^/]*")
        self.pattern = re.compile(pattern)

    def matches(self, relpath: str, direntry: os.DirEntry[str]) -> bool:
        m = self.pattern.match(relpath)
        return True if m else False


class PatternMatcher:
    def __init__(self, includes: list[str], excludes: list[str]):
        self.includes = [RecursiveGlobPattern(p) for p in includes]
        self.excludes = [RecursiveGlobPattern(p) for p in excludes]
        # Dictionary of relative posix-style path to DirEntry.
        # Last relative path wins.
        self.all: dict[str, os.DirEntry[str]] = {}

    def add_basedir(self, basedir: Path):
        all = self.all
        basedir = basedir.absolute()

        # Using scandir and being judicious about path concatenation/conversion
        # (versus using walk) is on the order of 10-50x faster. This is still
        # about 10x slower than an `ls -R` but gets us down to tens of
        # milliseconds for an LLVM install sized tree, which is acceptable.
        def scan_children(rootpath: str, prefix: str):
            with os.scandir(rootpath) as it:
                for entry in it:
                    if entry.is_dir(follow_symlinks=False):
                        relpath = f"{prefix}{entry.name}"
                        new_rootpath = os.path.join(rootpath, entry.name)
                        all[relpath] = entry
                        scan_children(new_rootpath, f"{relpath}/")
                    else:
                        relpath = f"{prefix}{entry.name}"
                        all[relpath] = entry

        scan_children(basedir, "")

    def matches(self) -> Generator[tuple[str, os.DirEntry[str]], None, None]:
        includes = self.includes
        excludes = self.excludes
        for match_path, direntry in self.all.items():
            if includes:
                for include in includes:
                    if include.matches(match_path, direntry):
                        break
                else:
                    continue
            excluded = False
            for exclude in excludes:
                if exclude.matches(match_path, direntry):
                    excluded = True
                    break
            if not excluded:
                yield match_path, direntry

    def copy_to(
        self,
        *,
        destdir: Path,
        destprefix: str = "",
        verbose: bool = False,
        always_copy: bool = False,
        remove_dest: bool = True,
    ):
        if remove_dest and destdir.exists():
            if verbose:
                print(f"rmtree {destdir}", file=sys.stderr)
            shutil.rmtree(destdir)
        destdir.mkdir(parents=True, exist_ok=True)

        for relpath, direntry in self.matches():
            try:
                destpath = destdir / PurePosixPath(destprefix + relpath)
                if direntry.is_dir(follow_symlinks=False):
                    # Directory.
                    if verbose:
                        print(f"mkdir {destpath}", file=sys.stderr, end="")
                    destpath.mkdir(parents=True, exist_ok=True)
                elif direntry.is_symlink():
                    # Symlink.
                    if not remove_dest and destpath.exists(follow_symlinks=False):
                        os.unlink(destpath)
                    targetpath = os.readlink(direntry.path)
                    if verbose:
                        print(
                            f"symlink {targetpath} -> {destpath}",
                            file=sys.stderr,
                            end="",
                        )
                    destpath.parent.mkdir(parents=True, exist_ok=True)
                    os.symlink(targetpath, destpath)
                else:
                    # Regular file.
                    if not remove_dest and destpath.exists(follow_symlinks=False):
                        os.unlink(destpath)
                    destpath.parent.mkdir(parents=True, exist_ok=True)
                    linked_file = False
                    if not always_copy:
                        # Attempt to link
                        try:
                            if verbose:
                                print(
                                    f"hardlink {direntry.path} -> {destpath}",
                                    file=sys.stderr,
                                    end="",
                                )
                            os.link(direntry.path, destpath, follow_symlinks=False)
                            linked_file = True
                        except OSError:
                            if verbose:
                                print(
                                    " (falling back to copy) ", file=sys.stderr, end=""
                                )
                    if not linked_file:
                        # Make a copy instead.
                        if verbose:
                            print(
                                f"copy {direntry.path} -> {destpath}",
                                file=sys.stderr,
                                end="",
                            )
                        shutil.copy2(direntry.path, destpath, follow_symlinks=False)
            finally:
                if verbose:
                    print("", file=sys.stderr)


def do_list(args: argparse.Namespace, pm: PatternMatcher):
    for relpath, direntry in pm.matches():
        print(relpath)


def do_copy(args: argparse.Namespace, pm: PatternMatcher):
    verbose = args.verbose
    destdir: Path = args.dest_dir
    pm.copy_to(
        destdir=destdir,
        verbose=verbose,
        always_copy=args.always_copy,
        remove_dest=args.remove_dest,
    )


def do_artifact(args):
    """Produces an 'artifact directory', which is a slice of installed stage/
    directories, split into components (i.e. run, dev, dbg, doc, test).

    The primary input is the artifact.toml file, which defines records like:

        "components" : dict of covered component names
            "{component_name}": dict of build/ relative paths to materialize
                "{stage_directory}":
                    "include": str or list[str] of include patterns
                    "exclude": str or list[str] of exclude patterns
                    "optional": if true and the directory does not exist, it
                      is not an error. Use for optionally built projects

    Most sections can typically be blank because by default they use
    component specific include/exclude patterns (see `COMPONENT_DEFAULTS` above)
    that cover most common cases. Local deviations must be added explicitly
    in the descriptor.

    This is called once per component and will create a directory for that
    component.
    """
    descriptor = load_toml_file(args.descriptor) or {}
    component_name = args.component
    # Set up output dir.
    output_dir: Path = args.output_dir
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get metadata for the component we are merging.
    try:
        component_record = descriptor["components"][component_name]
    except KeyError:
        # No components.
        component_record = {}

    all_basedir_relpaths = []
    for basedir_relpath, basedir_record in component_record.items():
        basedir = args.root_dir / Path(basedir_relpath)
        optional = basedir_record.get("optional")
        if optional and not basedir.exists():
            continue
        all_basedir_relpaths.append(basedir_relpath)

        # Includes.
        includes = _dup_list_or_str(basedir_record.get("include"))
        includes.extend(
            ComponentDefaults.ALL.get(component_name, ComponentDefaults()).includes
        )

        # Excludes.
        excludes = _dup_list_or_str(basedir_record.get("exclude"))
        excludes.extend(
            ComponentDefaults.ALL.get(component_name, ComponentDefaults()).excludes
        )

        pm = PatternMatcher(
            includes=includes,
            excludes=excludes,
        )
        pm.add_basedir(basedir)
        pm.copy_to(
            destdir=output_dir,
            destprefix=basedir_relpath + "/",
            remove_dest=False,
        )

    # Write a manifest containing relative paths of all base directories.
    manifest_path = args.manifest
    if manifest_path is None:
        manifest_path = output_dir / "artifact_manifest.txt"
    if manifest_path:
        manifest_path.write_text("\n".join(all_basedir_relpaths) + "\n")


def _dup_list_or_str(v: list[str] | str) -> list[str]:
    if not v:
        return []
    if isinstance(v, str):
        return [v]
    return list(v)


def load_toml_file(p: Path):
    try:
        import tomllib
    except ModuleNotFoundError:
        # Python <= 3.10 compatibility (requires install of 'toml' package)
        import toml as tomllib
    with open(p, "rb") as f:
        return tomllib.load(f)


def main(cl_args: list[str]):
    def add_pattern_matcher_args(p: argparse.ArgumentParser):
        p.add_argument("basedir", type=Path, nargs="*", help="Base directories to scan")
        p.add_argument("--include", nargs="+", help="Recursive glob pattern to include")
        p.add_argument("--exclude", nargs="+", help="Recursive glob pattern to exclude")
        p.add_argument("--verbose", action="store_true", help="Print verbose status")

    def pattern_matcher_action(
        action: Callable[[argparse.Namespace, PatternMatcher], None]
    ):
        def run_action(args: argparse.Namespace):
            if not args.basedir:
                # base dir is CWD
                args.basedir = [Path.cwd()]
            pm = PatternMatcher(args.include or [], args.exclude or [])
            for basedir in args.basedir:
                pm.add_basedir(basedir)
            action(args, pm)

        return run_action

    p = argparse.ArgumentParser(
        "fileset_tool.py", usage="fileset_tool.py {command} ..."
    )
    sub_p = p.add_subparsers(required=True)
    # 'copy' command
    copy_p = sub_p.add_parser("copy", help="Copy matching files to a destination dir")
    copy_p.add_argument("dest_dir", type=Path, help="Destination directory")
    copy_p.add_argument(
        "--always-copy", action="store_true", help="Always copy vs attempting to link"
    )
    copy_p.add_argument(
        "--remove-dest",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Remove the destination directory before copying",
    )
    add_pattern_matcher_args(copy_p)
    copy_p.set_defaults(func=pattern_matcher_action(do_copy))

    # 'list' command
    list_p = sub_p.add_parser("list", help="List matching files to stdout")
    add_pattern_matcher_args(list_p)
    list_p.set_defaults(func=pattern_matcher_action(do_list))

    # 'artifact' command
    artifact_p = sub_p.add_parser(
        "artifact", help="Merge artifacts based on a descriptor"
    )
    artifact_p.add_argument(
        "--output-dir", type=Path, required=True, help="Artifact output directory"
    )
    artifact_p.add_argument(
        "--root-dir",
        type=Path,
        required=True,
        help="Source directory to which all descriptor directories are relative",
    )
    artifact_p.add_argument(
        "--descriptor",
        type=Path,
        required=True,
        help="TOML file describing the artifact",
    )
    artifact_p.add_argument(
        "--component", required=True, help="Component within the descriptor to merge"
    )
    artifact_p.add_argument(
        "--manifest",
        type=Path,
        help="Manifest text file to write (contains base paths)",
    )
    artifact_p.set_defaults(func=do_artifact)

    args = p.parse_args(cl_args)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
