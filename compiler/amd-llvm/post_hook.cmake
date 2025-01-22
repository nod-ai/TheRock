list(APPEND CMAKE_MODULE_PATH "${THEROCK_SOURCE_DIR}/cmake")
include(therock_rpath)

# This should be fixed upstream to use LLVM's native RPATH setting logic (since
# the LLVM layout is already correct and we shouldn't have to muck with it).
# https://github.com/nod-ai/TheRock/issues/19
therock_set_install_rpath(
  TARGETS
    amd_comgr
  PATHS
    .
)
