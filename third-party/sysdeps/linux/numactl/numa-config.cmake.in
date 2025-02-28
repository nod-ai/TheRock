# Traverse from lib/cmake/FOO -> the directory holding lib
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_DIR}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
if(_IMPORT_PREFIX STREQUAL "/")
  set(_IMPORT_PREFIX "")
endif()

if(NOT TARGET numa::numa)
  add_library(numa::numa SHARED IMPORTED)
  set_target_properties(numa::numa PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
    IMPORTED_LOCATION "${_IMPORT_PREFIX}/lib/libnuma.so"
  )
endif()

set(NUMA_INCLUDE_DIRS "${_IMPORT_PREFIX}/include")
set(NUMA_LIBRARIES numa::numa)

set(_IMPORT_PREFIX)
