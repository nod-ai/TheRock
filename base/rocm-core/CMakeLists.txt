################################################################################
# rocm-core
################################################################################

therock_cmake_subproject_declare(rocm-core
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/rocm-core"
  CMAKE_ARGS
    "-DBUILD_SHARED_LIBS=ON"
    "-DROCM_VERSION=${ROCM_MAJOR_VERSION}.${ROCM_MINOR_VERSION}.${ROCM_PATCH_VERSION}"
)
therock_cmake_subproject_glob_c_sources(rocm-core
  SUBDIRS .
)
therock_cmake_subproject_provide_package(rocm-core rocm-core lib/cmake/rocm-core)
therock_cmake_subproject_activate(rocm-core)
