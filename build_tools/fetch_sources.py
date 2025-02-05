#!/usr/bin/env python
# Fetches sources from a specified branch/set of projects.
# This script is available for users, but it is primarily the mechanism
# the CI uses to get to a clean state.

import argparse
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import urllib.request

THIS_SCRIPT_DIR = Path(__file__).resolve().parent
THEROCK_DIR = THIS_SCRIPT_DIR.parent
DEFAULT_SOURCES_DIR = THEROCK_DIR / "sources"
PATCHES_DIR = THEROCK_DIR / "patches"


def setup_repo_tool() -> Path:
    """Sets up https://gerrit.googlesource.com/git-repo/, downloading as needed."""

    repo_path = shutil.which("repo")
    if repo_path:
        print(f"Found 'repo' on PATH at '{repo_path}', using it")
        return repo_path

    repo_path = THIS_SCRIPT_DIR / "repo"
    if repo_path.exists():
        print(f"Found 'repo' in script dir at '{repo_path}', using it")
        return repo_path

    print(f"Unable to find 'repo', downloading into script dir at '{repo_path}'")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/git-repo-downloads/repo", repo_path
    )
    os.chmod(repo_path, 0o744)
    return repo_path


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
    repo_tool_path = setup_repo_tool()

    repo_dir: Path = args.dir
    print(f"Setting up repo in {repo_dir}")
    repo_dir.mkdir(exist_ok=True, parents=True)
    repo_args = [
        sys.executable,
        str(repo_tool_path),
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
    exec(
        [
            sys.executable,
            str(repo_tool_path),
            "sync",
            "-j16",
        ]
        + get_enabled_projects(args),
        cwd=repo_dir,
    )

    populate_ancillary_sources(args)
    apply_patches(args)


def apply_patches(args):
    if not args.patch_tag:
        print("Not patching (no --patch-tag specified)")
    patch_version_dir: Path = PATCHES_DIR / args.patch_tag
    if not patch_version_dir.exists():
        print(f"ERROR: Patch directory {patch_version_dir} does not exist")
    for patch_project_dir in patch_version_dir.iterdir():
        print(f"* Processing project patch directory {patch_project_dir}:")
        project_dir: Path = args.dir / patch_project_dir.name
        if not project_dir.exists():
            print(f"WARNING: Source directory {project_dir} does not exist. Skipping.")
            continue
        patch_files = list(patch_project_dir.glob("*.patch"))
        patch_files.sort()
        print(f"Applying {len(patch_files)} patches")
        exec(["git", "am", "--whitespace=nowarn"] + patch_files, cwd=project_dir)


def populate_ancillary_sources(args):
    """Various subprojects have their own mechanisms for populating ancillary sources
    needed to build. There is often something in CMake that attempts to automate it,
    but it is also often broken. So we just do the right thing here as a transitionary
    step to fixing the underlying software packages."""
    populate_submodules_if_exists(args.dir / "rocprofiler-register")


def populate_submodules_if_exists(git_dir: Path):
    if not git_dir.exists():
        print(f"Not populating submodules for {git_dir} (does not exist)")
        return
    print(f"Populating submodules for {git_dir}:")
    exec(["git", "submodule", "update", "--init"], cwd=git_dir)


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
            "hipSPARSE",
            "rocBLAS",
            "rocPRIM",
            "rocRAND",
            "rocSOLVER",
            "rocSPARSE",
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
