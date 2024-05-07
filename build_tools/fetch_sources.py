#!/usr/bin/env python
# Fetches sources from a specified branch/set of projects.
# This script is available for users, but it is primarily the mechanism
# the CI uses to get to a clean state.

import argparse
from pathlib import Path
import subprocess
import sys

DEFAULT_SOURCES_DIR = Path(__file__).resolve().parent.parent / "sources"


def exec(args: list[str], cwd: Path):
    print(f"++ Exec: {args} (in {cwd})")
    subprocess.check_call(args, cwd=str(cwd))


def run(args):
    repo_dir: Path = args.dir
    print(f"Setting up repo in {repo_dir}")
    repo_dir.mkdir(exist_ok=True, parents=True)
    exec(
        [
            "repo",
            "init",
            "--manifest-url",
            args.manifest_url,
            "--depth=1",
            "--manifest-branch",
            args.manifest_branch
        ],
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
        "--manifest-url", type=str, help="Manifest repository location of ROCm",
        default="https://github.com/nod-ai/ROCm.git"
    )
    parser.add_argument(
        "--manifest-branch", type=str, help="Branch to sync with repo tool",
        default="the-rock-main"
    )
    parser.add_argument("--no-patch", action="store_true", help="Disable patching")
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
            "ROCR-Runtime",
            "ROCT-Thunk-Interface",
        ],
    )
    args = parser.parse_args(argv)
    run(args)


if __name__ == "__main__":
    main(sys.argv[1:])
