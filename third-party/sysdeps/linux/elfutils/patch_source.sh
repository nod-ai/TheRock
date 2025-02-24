#!/bin/bash

set -e

SOURCE_DIR="${1:?Source directory must be given}"
MAP_FILES="$(find $SOURCE_DIR -name '*.map')"
C_FILES="$(find $SOURCE_DIR -name '*.c')"
CONFIGURE_FILE="$SOURCE_DIR/configure"

# Prefix symbol version file symbols.
echo "Patching map files: $MAP_FILES"
sed -i -E 's|\b(ELFUTILS_[0-9\.]+)|AMDROCM_SYSDEPS_1.0_\1|' $MAP_FILES

# Prefix symbol version definitions in source files (configure contains a test
# too).
echo "Patching source files: $C_FILES"
sed -i -E 's@^((OLD_VERSION|NEW_VERSION|COMPAT_VERSION_NEWPROTO|COMPAT_VERSION).+)(ELFUTILS_[0-9\.]+.*)$@\1AMDROCM_SYSDEPS_1.0_\3@' \
    $C_FILES $CONFIGURE_FILE
