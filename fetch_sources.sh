#!/bin/bash
# Fetches the rocm-org sources with repo.
set -euxo pipefail

this_dir="$(cd $(dirname $0) && pwd)"
sources_dir="$this_dir/sources"

mkdir -p "$sources_dir"
cd "$sources_dir"
repo init -u https://github.com/RadeonOpenCompute/ROCm.git
repo sync -j16

# LLVM needs to be on the amd-staging branch.
cd llvm-project
git fetch --all
git checkout rocm-org/amd-staging
