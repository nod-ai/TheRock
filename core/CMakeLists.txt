if(THEROCK_ENABLE_CORE_RUNTIME)
  ##############################################################################
  # ROCR-Runtime
  ##############################################################################

  therock_cmake_subproject_declare(ROCR-Runtime
    EXTERNAL_SOURCE_DIR "ROCR-Runtime"
    BACKGROUND_BUILD
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

  ##############################################################################
  # rocminfo
  ##############################################################################

  therock_cmake_subproject_declare(rocminfo
    EXTERNAL_SOURCE_DIR "rocminfo"
    BACKGROUND_BUILD
    RUNTIME_DEPS
      ROCR-Runtime
  )
  therock_cmake_subproject_glob_c_sources(rocminfo SUBDIRS .)
  therock_cmake_subproject_activate(rocminfo)

  therock_provide_artifact(core-runtime
    TARGET_NEUTRAL
    DESCRIPTOR artifact-core-runtime.toml
    COMPONENTS
      dbg
      dev
      doc
      lib
      run
    SUBPROJECT_DEPS
      ROCR-Runtime
      rocminfo
  )

endif(THEROCK_ENABLE_CORE_RUNTIME)

if(THEROCK_ENABLE_HIP_RUNTIME)
  ##############################################################################
  # clr
  # The primary HIP compiler and runtime target. This is also the project used
  # to root the "amd-hip" compiler toolchain and is a superset of amd-llvm.
  # As a particularly sharp edge, the `hipconfig` tool is really only fully
  # functional from this project (which contributes version and metadata).
  ##############################################################################

  therock_cmake_subproject_declare(hip-clr
    EXTERNAL_SOURCE_DIR "clr"
    INTERFACE_PROGRAM_DIRS
      bin
    BACKGROUND_BUILD
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
      amd-comgr
      hipcc     # For hipconfig
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


  therock_provide_artifact(core-hip
    TARGET_NEUTRAL
    DESCRIPTOR artifact-core-hip.toml
    COMPONENTS
      dbg
      dev
      doc
      lib
      run
    SUBPROJECT_DEPS
      hip-clr
  )
endif(THEROCK_ENABLE_HIP_RUNTIME)
