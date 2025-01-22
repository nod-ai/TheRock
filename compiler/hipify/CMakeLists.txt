#################################################################################
# HIPIFY
#################################################################################

therock_cmake_subproject_declare(hipify
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/HIPIFY"
  CMAKE_ARGS
    -DHIPIFY_INSTALL_CLANG_HEADERS=OFF
  RUNTIME_DEPS
    amd-llvm
)
therock_cmake_subproject_glob_c_sources(hipify
  SUBDIRS
    src
)
therock_cmake_subproject_activate(hipify)
