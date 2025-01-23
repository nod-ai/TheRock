################################################################################
# rocm-cmake
################################################################################

therock_cmake_subproject_declare(rocm-cmake
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/rocm-cmake"
)
therock_cmake_subproject_provide_package(rocm-cmake
  ROCM share/rocmcmakebuildtools/cmake)
therock_cmake_subproject_activate(rocm-cmake)
