# Traverse from lib/cmake/FOO -> the directory holding lib
get_filename_component(_IMPORT_PREFIX "${CMAKE_CURRENT_LIST_DIR}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
get_filename_component(_IMPORT_PREFIX "${_IMPORT_PREFIX}" PATH)
if(_IMPORT_PREFIX STREQUAL "/")
  set(_IMPORT_PREFIX "")
endif()

if(NOT TARGET libdw::libdw)
  add_library(libdw::libdw SHARED IMPORTED)
  set_target_properties(libdw::libdw PROPERTIES
    INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"
    IMPORTED_LOCATION "${_IMPORT_PREFIX}/lib/libdw.so"
  )
endif()

set(_IMPORT_PREFIX)
