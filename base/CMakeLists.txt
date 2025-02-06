################################################################################
# rocm-cmake
################################################################################

therock_cmake_subproject_declare(rocm-cmake
  EXTERNAL_SOURCE_DIR "rocm-cmake"
)
therock_cmake_subproject_provide_package(rocm-cmake
  ROCmCMakeBuildTools share/rocmcmakebuildtools/cmake)
therock_cmake_subproject_provide_package(rocm-cmake
  ROCM share/rocm/cmake)
therock_cmake_subproject_activate(rocm-cmake)


################################################################################
# rocm-core
################################################################################

therock_cmake_subproject_declare(rocm-core
  EXTERNAL_SOURCE_DIR "rocm-core"
  CMAKE_ARGS
    "-DBUILD_SHARED_LIBS=ON"
    "-DROCM_VERSION=${ROCM_MAJOR_VERSION}.${ROCM_MINOR_VERSION}.${ROCM_PATCH_VERSION}"
)
therock_cmake_subproject_glob_c_sources(rocm-core
  SUBDIRS .
)
therock_cmake_subproject_provide_package(rocm-core rocm-core lib/cmake/rocm-core)
therock_cmake_subproject_activate(rocm-core)


################################################################################
# rocm_smi_lib
################################################################################

therock_cmake_subproject_declare(rocm_smi_lib
  EXTERNAL_SOURCE_DIR "rocm_smi_lib"
  INTERFACE_LINK_DIRS
    "lib"
)
therock_cmake_subproject_glob_c_sources(rocm_smi_lib
  SUBDIRS
    include
    src
)
therock_cmake_subproject_provide_package(rocm_smi_lib rocm_smi lib/cmake/rocm_smi)
therock_cmake_subproject_activate(rocm_smi_lib)


################################################################################
# rocprofiler-register
# This is a stub that helps runtime libraries and profiles rendezvous
################################################################################

therock_cmake_subproject_declare(rocprofiler-register
  EXTERNAL_SOURCE_DIR "rocprofiler-register"
  INTERFACE_LINK_DIRS
    "lib"
)
therock_cmake_subproject_glob_c_sources(rocprofiler-register
  SUBDIRS
    source/include
    source/lib
)
therock_cmake_subproject_provide_package(rocprofiler-register
  rocprofiler-register lib/cmake/rocprofiler-register)
therock_cmake_subproject_activate(rocprofiler-register)


################################################################################
# rocm-half
################################################################################

therock_cmake_subproject_declare(rocm-half
  EXTERNAL_SOURCE_DIR "half"
  BUILD_DEPS
    rocm-cmake
)
therock_cmake_subproject_glob_c_sources(rocm-half
  SUBDIRS
    include
)
therock_cmake_subproject_activate(rocm-half)


################################################################################
# Artifacts
################################################################################

therock_provide_artifact(base
  TARGET_NEUTRAL
  DESCRIPTOR artifact.toml
  COMPONENTS
    dbg
    dev
    doc
    lib
    run
    test
  SUBPROJECT_DEPS
    rocm-cmake
    rocm-core
    rocm_smi_lib
    rocprofiler-register
    rocm-half
)
