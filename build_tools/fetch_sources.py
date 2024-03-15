#!/usr/bin/env python
# Fetches sources from a specified branch/set of projects.
# This script is available for users, but it is primarily the mechanism
# the CI uses to get to a clean state.

import argparse
from pathlib import Path
import subprocess
import sys
import shutil

THE_ROCK_SRC_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SOURCES_DIR = THE_ROCK_SRC_DIR / "sources"


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
            "-u",
            "https://github.com/RadeonOpenCompute/ROCm.git",
            "--depth=1",
        ],
        cwd=repo_dir,
    )

    # Copy the manifest and sync based on it.
    manifest_path = THE_ROCK_SRC_DIR / "develop_rocm_manifest.xml"
    shutil.copyfile(manifest_path, repo_dir / ".repo/manifests/develop_rocm_manifest.xml")
    exec(["repo", "sync", "-m", "develop_rocm_manifest.xml", "-j16"] + args.projects, cwd=repo_dir)

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
        "--branch", type=str, help="Branch to sync", default="amd-staging"
    )
    parser.add_argument("--no-patch", action="store_true", help="Disable patching")
    parser.add_argument(
        "--projects",
        nargs="+",
        type=str,
        default=[
            "clr",
            "HIP",
            "llvm-project",
            "rocm-cmake",
            "rocm-core",
            "ROCR-Runtime",
            "ROCT-Thunk-Interface",
        ],
    )
    args = parser.parse_args(argv)
    run(args)


if __name__ == "__main__":
    main(sys.argv[1:])
