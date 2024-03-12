# Script run to install the amdgpu_runtime_dev component.
# This runs at install time and has access to the staging tree files.
message(STATUS "Custom installing amdgpu-runtime-dev to: ${CMAKE_INSTALL_PREFIX}")
message(STATUS "Staging install dir: ${STAGING_INSTALL_DIR}")
if(NOT IS_DIRECTORY "${STAGING_INSTALL_DIR}")
  message(FATAL_ERROR "Did not get STAGING_INSTALL_DIR from super-project")
endif()

set(LIB_PREFIX "lib")
set(SO_SUFFIX ".so")

set(RUNTIME_DYNAMIC_STAGING_DIR "${STAGING_INSTALL_DIR}/runtime_dynamic")

file(INSTALL ${RUNTIME_DYNAMIC_STAGING_DIR}/include DESTINATION ${CMAKE_INSTALL_PREFIX})

# # Assemble file lists.
file(
  GLOB_RECURSE DEV_FILES
  LIST_DIRECTORIES FALSE
  RELATIVE RUNTIME_DYNAMIC_STAGING_DIR
  ${RUNTIME_DYNAMIC_STAGING_DIR}/bin/hipcc_cmake_linker_helper
  ${RUNTIME_DYNAMIC_STAGING_DIR}/bin/hipdemangleatp
  ${RUNTIME_DYNAMIC_STAGING_DIR}/bin/roc-obj
  ${RUNTIME_DYNAMIC_STAGING_DIR}/bin/roc-obj-extract
  ${RUNTIME_DYNAMIC_STAGING_DIR}/bin/roc-obj-ls
  ${RUNTIME_DYNAMIC_STAGING_DIR}/lib/cmake/*
  ${RUNTIME_DYNAMIC_STAGING_DIR}/lib/pkgconfig/*
)

foreach(_relpath ${DEV_FILES})
  cmake_path(GET _relpath PARENT_PATH _parent_rel_path)
  file(
    INSTALL ${RUNTIME_DYNAMIC_STAGING_DIR}/${_relpath} 
    DESTINATION ${CMAKE_INSTALL_PREFIX}/${_parent_rel_path}
    USE_SOURCE_PERMISSIONS
  )
endforeach()
