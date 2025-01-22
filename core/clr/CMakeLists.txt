################################################################################
# clr
################################################################################

therock_cmake_subproject_declare(hip-clr
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/clr"
  CMAKE_ARGS
    -DHIP_PLATFORM=amd
    "-DHIP_COMMON_DIR=${ROCM_GIT_DIR}/HIP"
    -DCLR_BUILD_HIP=ON
    -DHIPCC_BIN_DIR="${THEROCK_BINARY_DIR}/compiler/hipify/dist/lib/llvm/bin/"
  BUILD_DEPS
    rocm-cmake
  RUNTIME_DEPS
    amd-llvm
    rocprofiler-register
    ROCR-Runtime
  INTERFACE_LINK_DIRS
    "lib"
)
therock_cmake_subproject_glob_c_sources(hip-clr SUBDIRS .)
therock_cmake_subproject_provide_package(hip-clr hip lib/cmake/hip)
therock_cmake_subproject_provide_package(hip-clr HIP lib/cmake/hip)
therock_cmake_subproject_activate(hip-clr)
