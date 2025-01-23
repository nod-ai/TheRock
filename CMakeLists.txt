if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are not allowed. Please create a separate build directory.")
endif()

cmake_minimum_required(VERSION 3.18)

# Set the default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

project(THEROCK)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(ExternalProject)
include(therock_subproject)
include(therock_job_pools)

################################################################################
# Options
################################################################################

option(THEROCK_INTERACTIVE "Enable interactive build mode which will cause all sub-project invocations to stream to the console (reducing parallelism)" OFF)
set(THEROCK_BACKGROUND_BUILD_JOBS "0" CACHE STRING "Number of jobs to reserve for projects marked for background building (empty=auto or a number)")

set(THEROCK_PACKAGE_VERSION "git" CACHE STRING "Sets the package version string")
set(ROCM_GIT_DIR "${THEROCK_SOURCE_DIR}/sources" CACHE PATH "Directory of rocm-org repo checkout")
message(STATUS "ROCM_GIT_DIR is set to: ${ROCM_GIT_DIR}")

# Library specific enable flags.
option(THEROCK_ENABLE_RCCL "Enable the comm_libs/rccl sub-project" ON)

# Initialize the install directory.
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${THEROCK_SOURCE_DIR}/install" CACHE PATH "" FORCE)
  message(STATUS "Defaulted CMAKE_INSTALL_PREFIX to ${CMAKE_INSTALL_PREFIX}")
endif()

set(ROCM_MAJOR_VERSION 6)
set(ROCM_MINOR_VERSION 3)
set(ROCM_PATCH_VERSION 1)
# set(AMDGPU_TARGETS "gfx90a gfx940 gfx942 gfx1100" CACHE STRING "AMDGPU Targets")
# TODO: Shard jobs by gfx family and have better ergonomics for multiple family
# specific packages.
set(AMDGPU_TARGETS "gfx1100" CACHE STRING "AMDGPU Targets")

################################################################################
# Global setup
################################################################################

# Some sub-projects need Python. Make sure it is found consistently.
find_package(Python3 3.9 COMPONENTS Interpreter REQUIRED)

configure_file(HIP_VERSION.in ${ROCM_GIT_DIR}/HIP/VERSION)

set(STAGING_INSTALL_DIR "${CMAKE_CURRENT_BINARY_DIR}/staging_install")

################################################################################
# External project setup
################################################################################

# On some distributions, this will install to lib64. We would like
# consistency in built packages, so hard-code it.
set(CMAKE_INSTALL_LIBDIR "lib")


if(CMAKE_C_VISIBILITY_PRESET)
  list(APPEND DEFAULT_CMAKE_ARGS ${CMAKE_C_VISIBILITY_PRESET})
endif()
if(CMAKE_CXX_VISIBILITY_PRESET)
  list(APPEND DEFAULT_CMAKE_ARGS ${CMAKE_CXX_VISIBILITY_PRESET})
endif()

# Add subdirectories in dependency DAG order (which happens to be semi-alpha:
# don't be fooled).
add_subdirectory(base)
add_subdirectory(compiler)
add_subdirectory(core)
add_subdirectory(comm_libs)


# ################################################################################
# # Testing
# ################################################################################

add_executable(
  dlopen-hip
  tests/dlopen-hip.c
)
target_link_libraries(dlopen-hip dl)

