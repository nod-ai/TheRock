#!/usr/bin/env python
# Scripted solution for building different variants of PyTorch ROCM.

import argparse
from pathlib import Path
import shlex
import subprocess
import sys

THIS_DIR = Path(__file__).resolve().parent
REPO_ROOT = THIS_DIR.parent.parent
FILESET_TOOL = REPO_ROOT / "build_tools" / "fileset_tool.py"


def exec(args: list[str | Path], cwd: Path):
    args = [str(arg) for arg in args]
    print(f"++ Exec [{cwd}]$ {shlex.join(args)}")
    subprocess.check_call(args, cwd=str(cwd), stdin=subprocess.DEVNULL)


def do_import(args: argparse.Namespace):
    # The pytorch-internal tool for hipifying includes options that appear to
    # support incremental/copying modes, but they also seem to break on
    # symlinks, etc. We use our fileset_tool because it handles all forms of
    # links properly, is fast, and supports exclude patterns.
    exec(
        [
            sys.executable,
            FILESET_TOOL,
            "copy",
            args.src_dir,  # copy dest
            args.git_dir,  # copy source
            # Because hipify modifies in-place versus unlink/modify, we can't use the
            # hardlink default.
            # TODO: fix hipify to unlink/update for better ergonomics all around.
            # TODO: Disable always-copy on CI when the git repo is throw-away.
            "--always-copy",
            "--exclude",
            "**/.git/**",
        ],
        cwd=THIS_DIR,
    )
    build_amd_path = args.src_dir / "tools" / "amd_build" / "build_amd.py"
    exec(
        [
            sys.executable,
            build_amd_path,
            "--project-directory",
            args.src_dir,
        ],
        cwd=args.src_dir,
    )
    # Hard-link our overlay directory.
    exec(
        [
            sys.executable,
            FILESET_TOOL,
            "copy",
            "--no-remove-dest",
            args.src_dir,
            THIS_DIR / "overlay",
        ],
        cwd=THIS_DIR,
    )


def main(cl_args: list[str]):
    p = argparse.ArgumentParser("ptbuild.py")
    sub_p = p.add_subparsers(required=True)
    import_p = sub_p.add_parser("import", help="Import PyTorch sources")
    import_p.add_argument(
        "--git-dir", required=True, type=Path, help="Path of PyTorch git checkout"
    )
    import_p.add_argument(
        "--src-dir",
        default=THIS_DIR / "src",
        type=Path,
        help="Path of imported PyTorch sources",
    )
    import_p.set_defaults(func=do_import)

    args = p.parse_args(cl_args)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
