#!/bin/bash
set -e

time cmake -GNinja -S/therock/src -B /therock/build \
  -DTHEROCK_BUNDLE_SYSDEPS=ON \
  -DTHEROCK_ENABLE_ALL=ON \
  -DTHEROCK_AMDGPU_FAMILIES=gfx1100
cmake --build /therock/build
ctest --test-dir /therock/build
