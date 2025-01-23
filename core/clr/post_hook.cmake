list(APPEND CMAKE_MODULE_PATH "${THEROCK_SOURCE_DIR}/cmake")
include(therock_rpath)

therock_set_install_rpath(
  TARGETS
    amdhip64
    hiprtc
  PATHS
    .
    llvm/lib
)

# See: https://github.com/nod-ai/TheRock/issues/21
if(HIPCC_BIN_DIR)
  message(FATAL_ERROR "The legacy HIPCC_BIN_DIR was somehow set, indicating a bug in the clr CMake files: ${HIPCC_BIN_DIR}")
endif()
