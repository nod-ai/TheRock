#!/bin/bash
# Applies patches that we are maintaining on the ROCM sources.
# These are developed against HEAD.
set -euxo pipefail

this_dir="$(cd $(dirname $0) && pwd)"

function stash_changes() {
  local repo_name="$1"
  cd $this_dir/sources/$repo_name
  git add -A
  git stash
}

function apply_patch() {
  local repo_name="$1"
  local patch_file="$2"
  cd $this_dir/sources/$repo_name
  echo "Applying $patch_file to $repo_name"
  patch -p1 < $this_dir/patches/$patch_file
}

stash_changes clr
apply_patch clr clr-disable-hipconfig-check.patch

stash_changes rocm-cmake
apply_patch rocm-cmake rocm-cmake-nocheck.patch

stash_changes ROCT-Thunk-Interface
apply_patch ROCT-Thunk-Interface ROCT-Thunk-Interface-header-nest.patch
apply_patch ROCT-Thunk-Interface ROCT-Thunk-Interface-export-hsaKmtGetAMDGPUDeviceHandle.patch

stash_changes ROCR-Runtime
apply_patch ROCR-Runtime ROCR-Runtime-intree-build.patch
