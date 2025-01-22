# ################################################################################
# # HIPIFY
# ################################################################################

therock_cmake_subproject_declare(hipify
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/HIPIFY"
  CMAKE_ARGS
    -DHIPIFY_INSTALL_CLANG_HEADERS=ON
  RUNTIME_DEPS
    amd-llvm
)
therock_cmake_subproject_glob_c_sources(hipify
  SUBDIRS
    src
)
# therock_cmake_subproject_provide_package(ROCR-Runtime hsakmt lib/cmake/hsakmt)
# therock_cmake_subproject_provide_package(ROCR-Runtime hsa-runtime64 lib/cmake/hsa-runtime64)
therock_cmake_subproject_activate(hipify)

# ExternalProject_Add(
#   hipify
#   PREFIX ${CMAKE_CURRENT_BINARY_DIR}/hipify
#   SOURCE_DIR "${ROCM_GIT_DIR}/HIPIFY"
#   DEPENDS
#     amd-llvm
#     clr
#   CMAKE_ARGS
#     ${DEFAULT_CMAKE_ARGS}
#     ${FIND_PACKAGE_OPTIONS}
#     -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}
#   USES_TERMINAL_CONFIGURE TRUE
#   USES_TERMINAL_BUILD TRUE
#   BUILD_ALWAYS ${ALWAYS_BUILD_SUBPROJECTS}
# )
