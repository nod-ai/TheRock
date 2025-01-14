#!/usr/bin/env python
# Fetches sources from a specified branch/set of projects.
# This script is available for users, but it is primarily the mechanism
# the CI uses to get to a clean state.

import argparse
from pathlib import Path
import shlex
import subprocess
import sys

DEFAULT_SOURCES_DIR = Path(__file__).resolve().parent.parent / "sources"


def exec(args: list[str | Path], cwd: Path):
    args = [str(arg) for arg in args]
    print(f"++ Exec [{cwd}]$ {shlex.join(args)}")
    subprocess.check_call(args, cwd=str(cwd))


def run(args):
    repo_dir: Path = args.dir
    print(f"Setting up repo in {repo_dir}")
    repo_dir.mkdir(exist_ok=True, parents=True)
    repo_args = [
        "repo",
        "init",
        "-v",
        "-u",
        args.manifest_url,
        "-m",
        args.manifest_name,
        "-b",
        args.manifest_branch,
    ]
    if args.depth:
        repo_args.extend(["--depth", str(args.depth)])
    exec(
        repo_args,
        cwd=repo_dir,
    )
    exec(["repo", "sync", "-j16"] + args.projects, cwd=repo_dir)

    # Patches.
    if not args.no_patch:
        apply_patches(args)


def apply_patches(args):
    # TODO: Can just merge this script in here if it survives.
    script = Path(__file__).resolve().parent / "apply_patches.sh"
    exec([script], cwd=args.dir)


def main(argv):
    parser = argparse.ArgumentParser(prog="fetch_sources")
    parser.add_argument(
        "--dir", type=Path, help="Repo dir", default=DEFAULT_SOURCES_DIR
    )
    parser.add_argument(
        "--manifest-url",
        type=str,
        help="Manifest repository location of ROCm",
        default="http://github.com/ROCm/ROCm.git",
    )
    parser.add_argument(
        "--manifest-name",
        type=str,
        help="Repo manifest name",
        default="tools/rocm-build/rocm-6.3.1.xml",
    )
    parser.add_argument(
        "--manifest-branch",
        type=str,
        help="Branch to sync with repo tool",
        default="roc-6.3.x",
    )
    parser.add_argument("--no-patch", action="store_true", help="Disable patching")
    parser.add_argument(
        "--depth", type=int, help="Git depth to pass to repo", default=None
    )
    parser.add_argument(
        "--projects",
        nargs="+",
        type=str,
        default=[
            "clr",
            "HIP",
            "HIPIFY",
            "llvm-project",
            "rccl",
            "rocm_smi_lib",
            "rocm-cmake",
            "rocm-core",
            "rocminfo",
            "rocprofiler-register",
            "ROCR-Runtime",
        ],
    )
    args = parser.parse_args(argv)
    run(args)


if __name__ == "__main__":
    main(sys.argv[1:])
