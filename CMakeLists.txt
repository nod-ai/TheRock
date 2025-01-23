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
set(AMDGPU_TARGETS "gfx90a gfx940 gfx942 gfx1100" CACHE STRING "AMDGPU Targets")

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

# add_executable(
#   dlopen-hip
#   tests/dlopen-hip.c
# )
# target_link_libraries(dlopen-hip dl)

# ################################################################################
# # Packaging
# # Since our notion of packaging does not follow the actual sub-projects,
# # we repackage based on what they have installed.
# ################################################################################

# install(
#   CODE "set(STAGING_INSTALL_DIR ${STAGING_INSTALL_DIR})"
#   ALL_COMPONENTS
# )

# install(
#   SCRIPT "cmake/custom_install_amdgpu_runtime.cmake"
#   COMPONENT amdgpu-runtime
# )

# install(
#   SCRIPT "cmake/custom_install_amdgpu_runtime_dev.cmake"
#   COMPONENT amdgpu-runtime-dev
# )

# install(
#   SCRIPT "cmake/custom_install_amdgpu_compiler.cmake"
#   COMPONENT amdgpu-compiler
# )

# string(TOLOWER "${CMAKE_SYSTEM_NAME}-${CMAKE_SYSTEM_PROCESSOR}" _package_sysarch)
# message(STATUS "CPack: SYSARCH=${_package_sysarch}, PACKAGE_VERSION=${THEROCK_PACKAGE_VERSION}")

# set(CPACK_PACKAGE_NAME "TheRock")
# set(CPACK_PACKAGE_VENDOR "Advanced Micro Devices")
# set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Standalone amdgpu runtime packages")
# set(CPACK_PACKAGE_VERSION "${THEROCK_PACKAGE_VERSION}")
# set(CPACK_PACKAGE_VERSION_MAJOR "${ROCM_MAJOR_VERSION}")
# set(CPACK_PACKAGE_VERSION_MINOR "${ROCM_MINOR_VERSION}")
# set(CPACK_PACKAGE_VERSION_PATCH "${ROCM_PATCH_VERSION}")
# set(CPACK_PACKAGE_INSTALL_DIRECTORY "TheRock-amdgpu")
# set(CPACK_PACKAGE_FILE_NAME "")
# set(CPACK_COMPONENTS_ALL
#   amdgpu-compiler
#   amdgpu-runtime
#   amdgpu-runtime-dev
# )

# # CPack Archive Generation Options.
# set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
# set(CPACK_ARCHIVE_THREADS 0)
# set(
#   CPACK_ARCHIVE_AMDGPU-RUNTIME_FILE_NAME
#   "TheRock-amdgpu-runtime-${_package_sysarch}-${THEROCK_PACKAGE_VERSION}")
# set(
#   CPACK_ARCHIVE_AMDGPU-RUNTIME-DEV_FILE_NAME
#   "TheRock-amdgpu-runtime-dev-${_package_sysarch}-${THEROCK_PACKAGE_VERSION}")
# set(
#   CPACK_ARCHIVE_AMDGPU-COMPILER_FILE_NAME
#   "TheRock-amdgpu-compiler-${_package_sysarch}-${THEROCK_PACKAGE_VERSION}")

# include(CPack)

# cpack_add_component(
#   amdgpu-runtime
#   DISPLAY_NAME "AMD GPU Runtime"
#   ARCHIVE_FILE "${CPACK_ARCHIVE_AMDGPU-RUNTIME_FILE_NAME}"
# )
# cpack_add_component(
#   amdgpu-runtime-dev
#   DISPLAY_NAME "AMD GPU Development Components"
#   DEPENDS amdgpu-runtime
#   ARCHIVE_FILE "${CPACK_ARCHIVE_AMDGPU-RUNTIME-DEV_FILE_NAME}"
# )
# cpack_add_component(
#   amdgpu-compiler
#   DISPLAY_NAME "AMD GPU Compiler"
#   ARCHIVE_FILE "${CPACK_ARCHIVE_AMDGPU-COMPILER_FILE_NAME}"
# )
