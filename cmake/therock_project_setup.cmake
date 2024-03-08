# Set the default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

get_filename_component(THEROCK_DIR "${CMAKE_CURRENT_LIST_DIR}/.." ABSOLUTE)

# Check if ROCM_GIT_DIR was passed in from the command line
if(NOT DEFINED ROCM_GIT_DIR)
  # Define the default path to the adjacent sources if not provided
  get_filename_component(ROCM_GIT_DIR "${THEROCK_DIR}/sources" ABSOLUTE)
endif()
message(STATUS "ROCM_GIT_DIR is set to: ${ROCM_GIT_DIR}")

#string(TIMESTAMP ROCM_MAJOR_VERSION "%Y%m%d")
set(ROCM_MAJOR_VERSION 6)
set(ROCM_MINOR_VERSION 0)
set(ROCM_PATCH_VERSION 0)
set(ROCM_VERSION "${ROCM_MAJOR_VERSION}.0.0" CACHE STRING "ROCM version")
set(AMDGPU_TARGETS "gfx90a gfx942 gfx1100" CACHE STRING "AMDGPU Targets")

if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${THEROCK_DIR}/install" CACHE PATH "" FORCE)
  message(STATUS "Defaulted CMAKE_INSTALL_PREFIX to ${CMAKE_INSTALL_PREFIX}")
endif()
