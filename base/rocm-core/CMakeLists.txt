################################################################################
# rocm-core
################################################################################

therock_cmake_subproject_declare(rocm-core
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/rocm-core"
  CMAKE_ARGS
    "-DBUILD_SHARED_LIBS=ON"
)
therock_cmake_subproject_glob_c_sources(rocm-core
  SUBDIRS .
)
therock_cmake_subproject_provide_package(rocm-core rocm-core lib/cmake/rocm-core)
therock_cmake_subproject_activate(rocm-core)
