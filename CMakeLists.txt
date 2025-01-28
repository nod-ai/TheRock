if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are not allowed. Please create a separate build directory.")
endif()

cmake_minimum_required(VERSION 3.18)

# Set the default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

project(THEROCK)

cmake_policy(SET CMP0135 NEW)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(CMakeDependentOption)
include(ExternalProject)
include(therock_amdgpu_targets)
include(therock_subproject)
include(therock_job_pools)

################################################################################
# Options
################################################################################
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(THEROCK_BACKGROUND_BUILD_JOBS "0" CACHE STRING "Number of jobs to reserve for projects marked for background building (empty=auto or a number)")

set(THEROCK_PACKAGE_VERSION "git" CACHE STRING "Sets the package version string")
set(ROCM_GIT_DIR "${THEROCK_SOURCE_DIR}/sources" CACHE PATH "Directory of rocm-org repo checkout")
message(STATUS "ROCM_GIT_DIR is set to: ${ROCM_GIT_DIR}")

# Library specific enable flags.
option(THEROCK_ENABLE_RCCL "Enable the comm_libs/rccl sub-project" ON)
option(THEROCK_ENABLE_MATH_LIBS "Enable building of math libraries" ON)
cmake_dependent_option(THEROCK_ENABLE_ML_FRAMEWORKS "Enables building of ML frameworks" ON THEROCK_ENABLE_MATH_LIBS OFF)

# Initialize the install directory.
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${THEROCK_SOURCE_DIR}/install" CACHE PATH "" FORCE)
  message(STATUS "Defaulted CMAKE_INSTALL_PREFIX to ${CMAKE_INSTALL_PREFIX}")
endif()

set(ROCM_MAJOR_VERSION 6)
set(ROCM_MINOR_VERSION 3)
set(ROCM_PATCH_VERSION 1)

################################################################################
# GPU target selection
#
# GPU target selection can be done by specifying one of THEROCK_AMDGPU_FAMILIES
# or THEROCK_AMDGPU_TARGETS. Most targets are bundled into families that include
# several related targets.
#
# If exactly one family or target is specified, then that is also taken to be
# the THEROCK_AMDGPU_DIST_BUNDLE_NAME, if omitted (this is the identifier
# embedded into package names). If more than one family or discrete target is
# specified, then the bundle name must be specified manually.
#
# Once cache variable validation is done, THEROCK_AMDGPU_TARGETS will be the
# fully expanded list of targets (as a local variable). For convenience and
# because some parts of the tree use a space separated list,
# THEROCK_AMDGPU_TARGETS_SPACES will also be set.
#
# See therock_amdgpu_targets.cmake for further details.
################################################################################

set(THEROCK_AMDGPU_FAMILIES "" CACHE STRING "AMDGPU target families to build for")
set(THEROCK_AMDGPU_TARGETS "" CACHE STRING "AMDGPU targets to build for")
set(THEROCK_AMDGPU_DIST_BUNDLE_NAME "" CACHE STRING "Distribution bundle name for AMDGPU packages")

therock_validate_amdbpu_targets()

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
add_subdirectory(third-party)
add_subdirectory(base)
add_subdirectory(compiler)
add_subdirectory(core)
add_subdirectory(comm-libs)
if(THEROCK_ENABLE_MATH_LIBS)
  add_subdirectory(math-libs)
endif()
if(THEROCK_ENABLE_ML_FRAMEWORKS)
  add_subdirectory(ml-frameworks)
endif()

# ################################################################################
# # Testing
# ################################################################################

add_executable(
  dlopen-hip
  tests/dlopen-hip.c
)
target_link_libraries(dlopen-hip dl)


################################################################################
# Finalization
################################################################################
therock_subproject_merge_compile_commands()
