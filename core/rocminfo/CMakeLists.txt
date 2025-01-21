################################################################################
# rocminfo
################################################################################

therock_cmake_subproject_declare(rocminfo
  EXTERNAL_SOURCE_DIR "${ROCM_GIT_DIR}/rocminfo"
  RUNTIME_DEPS
    ROCR-Runtime
)
therock_cmake_subproject_glob_c_sources(rocminfo SUBDIRS .)
therock_cmake_subproject_activate(rocminfo)
