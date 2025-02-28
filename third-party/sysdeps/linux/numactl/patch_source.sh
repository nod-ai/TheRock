#!/usr/bin/bash
set -e

SOURCE_DIR="${1:?Source directory must be given}"

echo "Patching sources..."
sed -i -E 's|\b(libnuma_)|AMDROCM_SYSDEPS_1.0_\1|' $SOURCE_DIR/versions.ldscript
sed -i -E 's|@(libnuma_)|@AMDROCM_SYSDEPS_1.0_\1|' $SOURCE_DIR/*.c
