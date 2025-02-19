#!/bin/bash
# Replaces symlinks for source folders with direct copies of files.
# This helps set up files for Windows CI runners that do not have symlinks
# fully configured. This should usually *NOT* be run on development machines
# since it makes destructive changes.

this_dir="$(cd $(dirname $0) && pwd)"
root_dir="$(cd $this_dir/.. && pwd)"

cd ${root_dir}

# Remove the original symlinks.
rm base/half
rm base/rocm-cmake
rm base/rocm-core
rm base/rocprofiler-register
rm compiler/hipify

# Delete .git folders which are symlinks too. CI doesn't need them.
rm -rf sources/half/.git
rm -rf sources/rocm-cmake/.git
rm -rf sources/rocm-core/.git
rm -rf sources/rocprofiler-register/.git
rm -rf sources/HIPIFY/.git

# Copy from sources/ to where the symlinks were.
cp -r sources/half base
cp -r sources/rocm-cmake base
cp -r sources/rocm-core base
cp -r sources/rocprofiler-register base
cp -r sources/HIPIFY compiler
