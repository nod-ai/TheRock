# Many things need to be configured with paths to additional LLVM tools.
# If a project is using an amd-hip or amd-llvm toolchain, then it will already
# have an implicit dep on the toolchain, so it is safe to reference binaries
# here without worrying about build deps.
therock_cmake_subproject_dist_dir(_toolchain_dir amd-llvm)
cmake_path(APPEND _toolchain_dir lib/llvm)

#################################################################################
# MIOpen
#################################################################################

therock_cmake_subproject_declare(MIOpen
  EXTERNAL_SOURCE_DIR "MIOpen"
  CMAKE_ARGS
    -DHIP_PLATFORM=amd
    -DROCM_PATH=
    -DROCM_DIR=
    -DMIOPEN_USE_COMPOSABLEKERNEL=OFF  # TODO: enable
    -DMIOPEN_USE_MLIR=OFF # TODO: enable
    -DMIOPEN_BUILD_DRIVER=OFF # TODO: enable
  COMPILER_TOOLCHAIN
    amd-hip
  BUILD_DEPS
    hipBLAS-common
    rocm-cmake
    rocm-half
    therock-boost
    therock-eigen
    therock-frugally-deep
    therock-nlohmann-json
    therock-FunctionalPlus
  RUNTIME_DEPS
    hip-clr
    hipBLAS
    hipBLASLt
    rocBLAS
    rocRAND
)

therock_cmake_subproject_activate(MIOpen)
