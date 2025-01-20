################################################################################
# ROCR-Runtime
################################################################################

therock_cmake_subproject_declare(ROCR-Runtime
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/ROCR-Runtime"
  CMAKE_ARGS
    "-DBUILD_SHARED_LIBS=ON"
  BUILD_DEPS
    amd-llvm
  RUNTIME_DEPS
    rocprofiler-register
)
therock_cmake_subproject_provide_package(ROCR-Runtime hsakmt lib/cmake/hsakmt)
therock_cmake_subproject_provide_package(ROCR-Runtime hsa-runtime64 lib/cmake/hsa-runtime64)
therock_cmake_subproject_activate(ROCR-Runtime)
