if(THEROCK_ENABLE_PROFILER_SDK)

  ##############################################################################
  # rocprofiler-sdk
  ##############################################################################
  therock_cmake_subproject_declare(rocprofiler-sdk
    EXTERNAL_SOURCE_DIR "rocprofiler-sdk"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
    RUNTIME_DEPS
      hip-clr
      rocprofiler-register
      ${THEROCK_BUNDLED_LIBDRM}
  )
  therock_cmake_subproject_provide_package(rocprofiler-sdk rocprofiler-sdk lib/cmake/rocprofiler-sdk)
  therock_cmake_subproject_provide_package(rocprofiler-sdk rocprofiler-sdk-roctx lib/cmake/rocprofiler-sdk-roctx)
  therock_cmake_subproject_activate(rocprofiler-sdk)

  therock_provide_artifact(rocprofiler-sdk
    TARGET_NEUTRAL
    DESCRIPTOR artifact-rocprofiler-sdk.toml
    COMPONENTS
      dbg
      dev
      doc
      lib
      run
    SUBPROJECT_DEPS
      rocprofiler-sdk
  )

endif(THEROCK_ENABLE_PROFILER_SDK)
