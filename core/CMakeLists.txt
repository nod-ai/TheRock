################################################################################
# ROCR-Runtime
################################################################################

therock_cmake_subproject_declare(ROCR-Runtime
  EXTERNAL_SOURCE_DIR "ROCR-Runtime"
  CMAKE_ARGS
    "-DBUILD_SHARED_LIBS=ON"
  BUILD_DEPS
    amd-llvm
  RUNTIME_DEPS
    rocprofiler-register
  INTERFACE_LINK_DIRS
    "lib"
)
therock_cmake_subproject_glob_c_sources(ROCR-Runtime
  SUBDIRS
    libhsakmt
    runtime
)
therock_cmake_subproject_provide_package(ROCR-Runtime hsakmt lib/cmake/hsakmt)
therock_cmake_subproject_provide_package(ROCR-Runtime hsa-runtime64 lib/cmake/hsa-runtime64)
therock_cmake_subproject_activate(ROCR-Runtime)


################################################################################
# clr
################################################################################

therock_cmake_subproject_declare(hip-clr
  EXTERNAL_SOURCE_DIR "clr"
  CMAKE_ARGS
    -DHIP_PLATFORM=amd
    "-DHIP_COMMON_DIR=${CMAKE_CURRENT_SOURCE_DIR}/HIP"
    -DCLR_BUILD_HIP=ON
    # Legacy: Disable various auto-detection logic that breaks out of jail
    # and can use local machine tools.
    -DHIPCC_BIN_DIR=
  BUILD_DEPS
    rocm-cmake
  RUNTIME_DEPS
    amd-llvm
    rocm-core
    rocprofiler-register
    ROCR-Runtime
  INTERFACE_LINK_DIRS
    "lib"
)
therock_cmake_subproject_glob_c_sources(hip-clr SUBDIRS .)
therock_cmake_subproject_provide_package(hip-clr hip lib/cmake/hip)
# TODO: Some projects resolve "hip" vs "HIP" so we advertise both, but this isn't
# great.
therock_cmake_subproject_provide_package(hip-clr HIP lib/cmake/hip)
therock_cmake_subproject_provide_package(hip-clr hip-lang lib/cmake/hip-lang)
therock_cmake_subproject_provide_package(hip-clr hiprtc lib/cmake/hiprtc)
therock_cmake_subproject_activate(hip-clr)


################################################################################
# rocminfo
################################################################################

therock_cmake_subproject_declare(rocminfo
  EXTERNAL_SOURCE_DIR "rocminfo"
  RUNTIME_DEPS
    ROCR-Runtime
)
therock_cmake_subproject_glob_c_sources(rocminfo SUBDIRS .)
therock_cmake_subproject_activate(rocminfo)
