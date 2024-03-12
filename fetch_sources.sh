#!/bin/bash
# Fetches the rocm-org sources with repo.
set -euxo pipefail

this_dir="$(cd $(dirname $0) && pwd)"
sources_dir="$this_dir/sources"

mkdir -p "$sources_dir"
cd "$sources_dir"
repo init -u https://github.com/RadeonOpenCompute/ROCm.git --depth=1
repo sync -j16 \
  clr HIP llvm-project rocm-cmake rocm-core ROCR-Runtime ROCT-Thunk-Interface

# LLVM needs to be on the amd-staging branch.
cd llvm-project
git fetch rocm-org amd-staging --depth=1
git checkout rocm-org/amd-staging
