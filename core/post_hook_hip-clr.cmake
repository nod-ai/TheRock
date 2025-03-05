# See: https://github.com/ROCm/TheRock/issues/21
if(HIPCC_BIN_DIR)
  message(FATAL_ERROR "The legacy HIPCC_BIN_DIR was somehow set, indicating a bug in the clr CMake files: ${HIPCC_BIN_DIR}")
endif()

# TODO: See hipamd/src/CMakeLists.txt where the rpath is hard-coded if depending
# on rocprofiler-register. This is wrong and needs to only be done if rpaths
# have not been setup at the project level.
set_target_properties(amdhip64 PROPERTIES INSTALL_RPATH "${CMAKE_INSTALL_RPATH}")
