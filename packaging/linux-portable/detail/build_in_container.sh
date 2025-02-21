#!/bin/bash
# See corresponding build_portable.py which invokes this.
set -e
set -o pipefail
trap 'kill -TERM 0' INT

OUTPUT_DIR="/therock/output"
mkdir -p "$OUTPUT_DIR/caches"

export CCACHE_DIR="$OUTPUT_DIR/caches/container/ccache"
export PIP_CACHE_DIR="$OUTPUT_DIR/caches/container/pip"
mkdir -p "$CCACHE_DIR"
mkdir -p "$PIP_CACHE_DIR"

export CMAKE_C_COMPILER_LAUNCHER=ccache
export CMAKE_CXX_COMPILER_LAUNCHER=ccache

set -o xtrace
time cmake -GNinja -S /therock/src -B "$OUTPUT_DIR/build" "$@"
time cmake --build "$OUTPUT_DIR/build"
