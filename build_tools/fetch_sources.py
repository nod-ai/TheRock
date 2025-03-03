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


def log(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


def exec(args: list[str | Path], cwd: Path):
    args = [str(arg) for arg in args]
    log(f"++ Exec [{cwd}]$ {shlex.join(args)}")
    sys.stdout.flush()
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
    submodule_paths = [get_submodule_path(project) for project in projects]
    update_args = []
    if args.depth:
        update_args += ["--depth", str(args.depth)]
    if args.jobs:
        update_args += ["--jobs", str(args.jobs)]
    exec(
        ["git", "submodule", "update", "--init", "--recursive"]
        + update_args
        + ["--"]
        + submodule_paths,
        cwd=THEROCK_DIR,
    )

    # Because we allow local patches, if a submodule is in a patched state,
    # we manually set it to skip-worktree since recording the commit is
    # then meaningless. Here on each fetch, we reset the flag so that if
    # patches are aged out, the tree is restored to normal.
    submodule_paths = [get_submodule_path(name) for name in projects]
    exec(
        ["git", "update-index", "--no-skip-worktree", "--"] + submodule_paths,
        cwd=THEROCK_DIR,
    )

    apply_patches(args)


def apply_patches(args):
    if not args.patch_tag:
        log("Not patching (no --patch-tag specified)")
    patch_version_dir: Path = PATCHES_DIR / args.patch_tag
    if not patch_version_dir.exists():
        log(f"ERROR: Patch directory {patch_version_dir} does not exist")
    for patch_project_dir in patch_version_dir.iterdir():
        log(f"* Processing project patch directory {patch_project_dir}:")
        submodule_path = get_submodule_path(patch_project_dir.name)
        project_dir = THEROCK_DIR / submodule_path
        if not project_dir.exists():
            log(f"WARNING: Source directory {project_dir} does not exist. Skipping.")
            continue
        patch_files = list(patch_project_dir.glob("*.patch"))
        patch_files.sort()
        log(f"Applying {len(patch_files)} patches")
        exec(["git", "am", "--whitespace=nowarn"] + patch_files, cwd=project_dir)
        # Since it is in a patched state, make it invisible to changes.
        exec(
            ["git", "update-index", "--skip-worktree", "--", submodule_path],
            cwd=THEROCK_DIR,
        )


# Gets the the relative path to a submodule given its name.
# Raises an exception on failure.
def get_submodule_path(name: str) -> str:
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
    return relpath


def main(argv):
    parser = argparse.ArgumentParser(prog="fetch_sources")
    parser.add_argument(
        "--patch-tag",
        type=str,
        default="amd-mainline",
        help="Patch tag to apply to sources after sync",
    )
    parser.add_argument(
        "--depth", type=int, help="Git depth when updating submodules", default=None
    )
    parser.add_argument(
        "--jobs",
        type=int,
        help="Number of jobs to use for updating submodules",
        default=None,
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
