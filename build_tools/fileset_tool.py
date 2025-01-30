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


def do_list(args: argparse.Namespace, pm: PatternMatcher):
    for relpath, direntry in pm.matches():
        print(relpath)


def do_copy(args: argparse.Namespace, pm: PatternMatcher):
    verbose = args.verbose
    destdir: Path = args.dest_dir
    if args.remove_dest and destdir.exists():
        if verbose:
            print(f"rmtree {destdir}", file=sys.stderr)
        shutil.rmtree(destdir)
    destdir.mkdir(parents=True, exist_ok=True)
    for relpath, direntry in pm.matches():
        try:
            destpath = destdir / PurePosixPath(relpath)
            if direntry.is_dir(follow_symlinks=False):
                # Directory.
                if verbose:
                    print(f"mkdir {destpath}", file=sys.stderr, end="")
                destpath.mkdir(parents=True, exist_ok=True)
            elif direntry.is_symlink():
                # Symlink.
                if not args.remove_dest and destpath.exists(follow_symlinks=False):
                    os.unlink(destpath)
                targetpath = os.readlink(direntry.path)
                if verbose:
                    print(
                        f"symlink {targetpath} -> {destpath}", file=sys.stderr, end=""
                    )
                os.symlink(targetpath, destpath)
            else:
                # Regular file.
                if not args.remove_dest and destpath.exists(follow_symlinks=False):
                    os.unlink(destpath)
                destpath.parent.mkdir(parents=True, exist_ok=True)
                linked_file = False
                if not args.always_copy:
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
                            print(" (falling back to copy) ", file=sys.stderr, end="")
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

    args = p.parse_args(cl_args)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
