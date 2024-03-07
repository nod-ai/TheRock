#!/bin/bash
# Applies patches that we are maintaining on the ROCM sources.
# These are developed against HEAD.
set -euxo pipefail

this_dir="$(cd $(dirname $0) && pwd)"

function checkout_head() {
  local repo_name="$1"
  local head="$2"

  echo "Checking out $head on $repo_name"
  cd $this_dir/../rocm/$repo_name
  git add -A
  git stash
  git checkout "$head"
}

function apply_patch() {
  local repo_name="$1"
  local patch_file="$2"
  cd $this_dir/../rocm/$repo_name
  echo "Applying $patch_file to $repo_name"
  patch -p1 < $this_dir/patches/$patch_file
}

checkout_head rocm-cmake rocm-org/master
apply_patch rocm-cmake rocm-cmake-nocheck.patch

checkout_head ROCT-Thunk-Interface rocm-org/master
apply_patch ROCT-Thunk-Interface ROCT-Thunk-Interface-header-nest.patch

checkout_head ROCR-Runtime m/develop
apply_patch ROCR-Runtime ROCR-Runtime-intree-build.patch
