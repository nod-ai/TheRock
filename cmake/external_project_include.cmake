# This file is injected into each ExternalProject in the super project.
# It sets up various toolchain details.

message(STATUS "TheRock external project configuration injection")

################################################################################
# Set up RPATH entries so that we load our bundled libraries first.
#
# bin/
# lib/
# llvm/
#   lib/
#
# We want anything in the top-level bin/ or lib/ dirs to find sibling libraries
# in lib/ and llvm/lib/.
#
# Therefore, we set platform specific relative RPATHs for:
#   ../lib
#   ../llvm/lib
#
# We set this via cmake injection vs passing on a CL because escaping is
# especially tricky and this avoids the issues.
################################################################################

if(WIN32)
  # Do nothing.
elseif(${CMAKE_SYSTEM_NAME} MATCHES "Darwin")
  # Assume @loader_path style RPATH.
  set(CMAKE_INSTALL_RPATH "@loader_path/../lib;@loader_path/../llvm/lib")
else()
  # Assume ${ORIGIN} style RPATH.
  set(CMAKE_INSTALL_RPATH "$ORIGIN/../lib;$ORIGIN/../llvm/lib")
endif()
