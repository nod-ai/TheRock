#!/bin/bash
# Patches installed binaries from the external build system.
# Args: install_dir patchelf_binary
set -e
set -o pipefail

prefix="$1"
patchelf="$2"

function prefix_soname() {
  local lib_path="$1"
  shift

  lib_name="$(basename $lib_path)"
  orig_so="$(readlink -f $lib_path)"
  orig_soname="$($patchelf --print-soname $orig_so)"
  new_soname="rocm_sysdeps_$orig_soname"
  new_so="$prefix/lib/$new_soname"
  echo "Renaming $orig_so -> $new_so ($orig_soname -> $new_soname)"
  cp -a "$orig_so" "$new_so"
  rm -f $lib_path $lib_path.*

  $patchelf --set-soname "$new_soname" "$new_so"
  # Symlink the original libname to this one so dev linking finds it.
  ln -s "$new_soname" "$(dirname $lib_path)/$lib_name"

  # And handle deps.
  for dep_file in "$@"; do
    echo "Patching $dep_file: $orig_soname -> $new_soname"
    $patchelf --replace-needed "$orig_soname" "$new_soname" "$dep_file"
  done
}

prefix_soname $prefix/lib/libdrm.so $prefix/lib/libdrm_*.so
for plat_so in $prefix/lib/libdrm_*.so; do
  prefix_soname "$plat_so"
done
