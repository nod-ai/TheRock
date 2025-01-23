################################################################################
# rocprofiler-register
# This is a stub that helps runtime libraries and profiles rendezvous
################################################################################

therock_cmake_subproject_declare(rocprofiler-register
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/rocprofiler-register"
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
