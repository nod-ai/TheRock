list(APPEND CMAKE_MODULE_PATH "${THEROCK_SOURCE_DIR}/cmake")
include(therock_rpath)

therock_set_install_rpath(
  TARGETS
    MIOpen
  PATHS
    .
    rocm_sysdeps/lib
)
