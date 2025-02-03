#!/bin/bash
# Saves patches that are maintained locally to make TheRock work with a given
# branch.
# Usage: save_patches.sh base_tag project_name patches_dir
# The base_tag must be checked out on the current branch. All commits above it
# will be dumped as patches.
set -euo pipefail

repo_dir="$(pwd)"
this_dir="$(cd $(dirname $0) && pwd)"
root_dir="$(cd $this_dir/.. && pwd)"

# Command line args.
set +eu
version_tag="$1"
shift
project_name="$1"
shift
patch_dir="$1"
shift
set -eu

if [ -z "$version_tag" ] || [ -z "$project_name" ]; then
  echo "Syntax: save_patches.sh <version_tag> <project_name>"
  exit 1
fi

# Directories.
patch_dir="$root_dir/patches/$version_tag/$project_name"
mkdir -p $patch_dir
source_dir="$root_dir/sources/$project_name"
if ! [ -d "$source_dir" ]; then
  echo "Source directory not found: $source_dir"
  exit 1
fi

# Remove existing patch files.
for existing in $patch_dir/*.patch; do
  if [ -f "$existing" ]; then
    rm "$existing"
  fi
done

# And format.
(cd $source_dir && git format-patch -o $patch_dir "$version_tag")
