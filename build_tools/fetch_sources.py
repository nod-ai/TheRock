#!/usr/bin/env python
# Fetches sources from a specified branch/set of projects.
# This script is available for users, but it is primarily the mechanism
# the CI uses to get to a clean state.

import argparse
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys
import urllib.request

THIS_SCRIPT_DIR = Path(__file__).resolve().parent
THEROCK_DIR = THIS_SCRIPT_DIR.parent
DEFAULT_SOURCES_DIR = THEROCK_DIR / "sources"
PATCHES_DIR = THEROCK_DIR / "patches"


def is_windows() -> bool:
    return platform.system() == "Windows"


def exec(args: list[str | Path], cwd: Path):
    args = [str(arg) for arg in args]
    print(f"++ Exec [{cwd}]$ {shlex.join(args)}")
    subprocess.check_call(args, cwd=str(cwd), stdin=subprocess.DEVNULL)


def get_enabled_projects(args) -> list[str]:
    projects = list(args.projects)
    if args.include_math_libs:
        projects.extend(args.math_lib_projects)
    if args.include_ml_frameworks:
        projects.extend(args.ml_framework_projects)
    return projects


def run(args):
    projects = get_enabled_projects(args)
    exec(["git", "config", "submodule.active", " ".join(projects)], cwd=THEROCK_DIR)
    depth_args = []
    if args.depth:
        depth_args = ["--depth", str(args.depth)]
    exec(
        ["git", "submodule", "update", "--init", "--recursive"] + depth_args,
        cwd=THEROCK_DIR,
    )
    apply_patches(args)


def apply_patches(args):
    if not args.patch_tag:
        print("Not patching (no --patch-tag specified)")
    patch_version_dir: Path = PATCHES_DIR / args.patch_tag
    if not patch_version_dir.exists():
        print(f"ERROR: Patch directory {patch_version_dir} does not exist")
    for patch_project_dir in patch_version_dir.iterdir():
        print(f"* Processing project patch directory {patch_project_dir}:")
        project_dir = get_submodule_path(patch_project_dir.name)
        if not project_dir.exists():
            print(f"WARNING: Source directory {project_dir} does not exist. Skipping.")
            continue
        patch_files = list(patch_project_dir.glob("*.patch"))
        patch_files.sort()
        print(f"Applying {len(patch_files)} patches")
        exec(["git", "am", "--whitespace=nowarn"] + patch_files, cwd=project_dir)


# Gets the the absolute path to a submodule given its name.
# Raises an exception on failure.
def get_submodule_path(name: str) -> Path:
    relpath = (
        subprocess.check_output(
            [
                "git",
                "config",
                "--file",
                ".gitmodules",
                "--get",
                f"submodule.{name}.path",
            ],
            cwd=str(THEROCK_DIR),
        )
        .decode()
        .strip()
    )
    return THEROCK_DIR / relpath


def main(argv):
    parser = argparse.ArgumentParser(prog="fetch_sources")
    parser.add_argument(
        "--dir", type=Path, help="Repo dir", default=DEFAULT_SOURCES_DIR
    )
    parser.add_argument(
        "--manifest-url",
        type=str,
        help="Manifest repository location of ROCm",
        default="https://github.com/ROCm/ROCm.git",
    )
    parser.add_argument(
        "--manifest-name",
        type=str,
        help="Repo manifest name",
        default="default.xml",
    )
    parser.add_argument(
        "--manifest-branch",
        type=str,
        help="Branch to sync with repo tool",
        default="amd-mainline",
    )
    parser.add_argument(
        "--patch-tag",
        type=str,
        default="amd-mainline",
        help="Patch tag to apply to sources after sync",
    )
    parser.add_argument(
        "--depth", type=int, help="Git depth to pass to repo", default=None
    )
    parser.add_argument(
        "--include-math-libs",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Include supported math libraries",
    )
    parser.add_argument(
        "--include-ml-frameworks",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Include machine learning frameworks that are part of ROCM",
    )
    parser.add_argument(
        "--projects",
        nargs="+",
        type=str,
        default=[
            "clr",
            "half",
            "HIP",
            "HIPIFY",
            "llvm-project",
            "rccl",
            "rocm_smi_lib",
            "rocm-cmake",
            "rocm-core",
            "rocminfo",
            "rocprofiler-register",
            # TODO: Re-enable when used.
            # "rocprofiler-compute",
            "rocprofiler-sdk",
            # TODO: Re-enable when used.
            # "rocprofiler-systems",
            "ROCR-Runtime",
        ],
    )
    parser.add_argument(
        "--math-lib-projects",
        nargs="+",
        type=str,
        default=[
            "hipBLAS-common",
            "hipBLAS",
            "hipBLASLt",
            "hipCUB",
            "hipFFT",
            "hipRAND",
            "hipSOLVER",
            "hipSPARSE",
            "Tensile",
            "rocBLAS",
            "rocFFT",
            "rocPRIM",
            "rocRAND",
            "rocSOLVER",
            "rocSPARSE",
            "rocThrust",
        ],
    )
    parser.add_argument(
        "--ml-framework-projects",
        nargs="+",
        type=str,
        default=[
            "MIOpen",
        ],
    )
    args = parser.parse_args(argv)
    run(args)


if __name__ == "__main__":
    main(sys.argv[1:])
