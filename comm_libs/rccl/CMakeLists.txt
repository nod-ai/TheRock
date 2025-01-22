#################################################################################
# rccl
#################################################################################

therock_cmake_subproject_declare(rccl
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/rccl"
  # High latency LTO link of a single library.
  BACKGROUND_BUILD
  COMPILER_TOOLCHAIN
    amd-llvm
  IGNORE_PACKAGES
    # The current version of rccl needs to download a 2y old version of rocm-cmake
    # to work and it will only do so if the system resolver reports it not found
    # without any other error (which due to the signature, our resolver will
    # hard fail). Once fixed, `rocm-core` should be added to the BUILD_DEPS
    # and this removed: https://github.com/nod-ai/TheRock/issues/18
    ROCM
  RUNTIME_DEPS
    hip-clr
    hipify
    rocm_smi_lib
    rocprofiler-register
)
therock_cmake_subproject_glob_c_sources(rccl
  SUBDIRS
    src
)
therock_cmake_subproject_activate(rccl)
