################################################################################
# rocm_smi_lib
################################################################################

therock_cmake_subproject_declare(rocm_smi_lib
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/rocm_smi_lib"
  INTERFACE_LINK_DIRS
    "lib"
)
therock_cmake_subproject_glob_c_sources(rocm_smi_lib
  SUBDIRS
    include
    src
)
therock_cmake_subproject_provide_package(rocm_smi_lib rocm_smi lib/cmake/rocm_smi)
therock_cmake_subproject_activate(rocm_smi_lib)
