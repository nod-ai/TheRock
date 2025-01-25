# Many things need to be configured with paths to additional LLVM tools.
# If a project is using an amd-hip or amd-llvm toolchain, then it will already
# have an implicit dep on the toolchain, so it is safe to reference binaries
# here without worrying about build deps.
therock_cmake_subproject_dist_dir(_toolchain_dir amd-llvm)
cmake_path(APPEND _toolchain_dir lib/llvm)

#################################################################################
# hipBLAS-common
#################################################################################

therock_cmake_subproject_declare(hipBLAS-common
  EXTERNAL_SOURCE_DIR "hipBLAS-common"
  CMAKE_ARGS
    -DROCM_PATH=
    -DROCM_DIR=
  COMPILER_TOOLCHAIN
    amd-hip
  IGNORE_PACKAGES
    # The current version of rccl needs to download a 2y old version of rocm-cmake
    # to work and it will only do so if the system resolver reports it not found
    # without any other error (which due to the signature, our resolver will
    # hard fail). Once fixed, `rocm-core` should be added to the BUILD_DEPS
    # and this removed: https://github.com/nod-ai/TheRock/issues/18
    ROCM
  RUNTIME_DEPS
    hip-clr
)
therock_cmake_subproject_glob_c_sources(hipBLAS-common
  SUBDIRS
    library
)
therock_cmake_subproject_provide_package(hipBLAS-common hipblas-common lib/cmake/hipblas-common)
therock_cmake_subproject_activate(hipBLAS-common)

#################################################################################
# hipBLASLt
#################################################################################

therock_cmake_subproject_declare(hipBLASLt
  EXTERNAL_SOURCE_DIR "hipBLASLt"
  CMAKE_ARGS
    -DHIP_PLATFORM=amd
    -DROCM_PATH=
    -DROCM_DIR=
    -DTensile_LOGIC=
    -DTensile_CODE_OBJECT_VERSION=default
    -DTensile_CPU_THREADS=
    -DTensile_LIBRARY_FORMAT=msgpack
    "-DTensile_ROCM_ASSEMBLER_PATH=${_toolchain_dir}/bin/clang++"
    "-DTensile_ROCM_OFFLOAD_BUNDLER_PATH=${_toolchain_dir}/bin/clang-offload-bundler"
    # TODO: Enable clients.
  COMPILER_TOOLCHAIN
    amd-hip
  BUILD_DEPS
    hipBLAS-common
  RUNTIME_DEPS
    hip-clr
)
therock_cmake_subproject_glob_c_sources(hipBLASLt
  SUBDIRS
    .
)
therock_cmake_subproject_provide_package(hipBLASLt hipblaslt lib/cmake/hipblaslt)
therock_cmake_subproject_activate(hipBLASLt)

#################################################################################
# rocBLAS
#################################################################################

therock_cmake_subproject_declare(rocBLAS
  EXTERNAL_SOURCE_DIR "rocBLAS"
  CMAKE_ARGS
    -DHIP_PLATFORM=amd
    -DROCM_PATH=
    -DROCM_DIR=
    # TODO: Fix passing TENSILE_ROCM_ASSEMBLER_PATH.
    #       Enable building with hipBLASLt afterwards.
    -DBUILD_WITH_TENSILE=OFF
    -DBUILD_WITH_HIPBLASLT=OFF
    # -DTensile_LOGIC=
    # -DTensile_CODE_OBJECT_VERSION=default
    # -DTensile_CPU_THREADS=
    # -DTensile_LIBRARY_FORMAT=msgpack
    # "-DTensile_ROCM_ASSEMBLER_PATH=${_toolchain_dir}/bin/clang++"
    # "-DTensile_ROCM_OFFLOAD_BUNDLER_PATH=${_toolchain_dir}/bin/clang-offload-bundler"
    # TODO: Enable clients.
  IGNORE_PACKAGES
    ROCM
  COMPILER_TOOLCHAIN
    amd-hip
  RUNTIME_DEPS
    #hipBLAS-common
    #hipBLASLt
    hip-clr
)
therock_cmake_subproject_glob_c_sources(rocBLAS
  SUBDIRS
    .
)
therock_cmake_subproject_provide_package(rocBLAS rocblas lib/cmake/rocblas)
therock_cmake_subproject_activate(rocBLAS)

#################################################################################
# rocRAND
#################################################################################

therock_cmake_subproject_declare(rocRAND
  EXTERNAL_SOURCE_DIR "rocRAND"
  CMAKE_ARGS
    -DHIP_PLATFORM=amd
    -DROCM_PATH=
    -DROCM_DIR=
  COMPILER_TOOLCHAIN
    amd-hip
  RUNTIME_DEPS
    hip-clr
)
therock_cmake_subproject_glob_c_sources(rocRAND
  SUBDIRS
    .
)
therock_cmake_subproject_provide_package(rocRAND rocrand lib/cmake/rocrand)
therock_cmake_subproject_activate(rocRAND)

#################################################################################
# hipBLAS
#################################################################################

therock_cmake_subproject_declare(hipBLAS
  EXTERNAL_SOURCE_DIR "hipBLAS"
  CMAKE_ARGS
    -DHIP_PLATFORM=amd
    -DROCM_PATH=
    -DROCM_DIR=
    -DBUILD_WITH_SOLVER=OFF  # TODO: add/enable rocSOLVER
  COMPILER_TOOLCHAIN
    amd-hip
  BUILD_DEPS
    hipBLAS-common
  RUNTIME_DEPS
    hip-clr
    rocBLAS
)
therock_cmake_subproject_glob_c_sources(hipBLAS
  SUBDIRS
    .
)
therock_cmake_subproject_provide_package(hipBLAS hipblas lib/cmake/hipblas)
therock_cmake_subproject_activate(hipBLAS)
