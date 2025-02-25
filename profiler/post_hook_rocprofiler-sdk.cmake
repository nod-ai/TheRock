list(APPEND CMAKE_MODULE_PATH "${THEROCK_SOURCE_DIR}/cmake")
include(therock_rpath)

# Lives in lib/rocprofiler-sdk
therock_set_install_rpath(
  TARGETS
    rocprofiler-sdk-tool
  PATHS
    .
    ..
    ../rocm_sysdeps/lib
)

# Lives in lib
therock_set_install_rpath(
  TARGETS
    rocprofiler-sdk-shared-library
  PATHS
    .
    rocm_sysdeps/lib
)

# Lives in lib
therock_set_install_rpath(
  TARGETS
    rocprofiler-sdk-roctx-shared-library
  PATHS
    .
    rocm_sysdeps/lib
)
