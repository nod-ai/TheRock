if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are not allowed. Please create a separate build directory.")
endif()

cmake_minimum_required(VERSION 3.25)

# Set the default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

project(THEROCK)

cmake_policy(SET CMP0135 NEW)
enable_testing()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(CMakeDependentOption)
include(ExternalProject)
include(therock_amdgpu_targets)
include(therock_artifacts)
include(therock_features)
include(therock_subproject)
include(therock_job_pools)

################################################################################
# Options
################################################################################
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(THEROCK_BACKGROUND_BUILD_JOBS "0" CACHE STRING "Number of jobs to reserve for projects marked for background building (empty=auto or a number)")

set(THEROCK_PACKAGE_VERSION "git" CACHE STRING "Sets the package version string")
set(ROCM_GIT_DIR "${THEROCK_SOURCE_DIR}/sources" CACHE PATH "Directory of rocm-org repo checkout")
# Disable compatibility symlinks created in default ROCM cmake project wide
set(ROCM_SYMLINK_LIBS OFF)
message(STATUS "ROCM_GIT_DIR is set to: ${ROCM_GIT_DIR}")

set(THEROCK_ARTIFACT_ARCHIVE_SUFFIX "" CACHE STRING "Suffix to add to artifact archive file stem names")
set(THEROCK_ARTIFACT_ARCHIVE_TYPES "tar.xz" CACHE STRING "List of artifact archive types to generate")

# Feature groups.
option(THEROCK_ENABLE_ALL "Enables building of all feature groups" ON)
cmake_dependent_option(THEROCK_ENABLE_CORE "Enable building of core libraries" ON "THEROCK_ENABLE_ALL" OFF)
cmake_dependent_option(THEROCK_ENABLE_COMM_LIBS "Enable building of comm libraries" ON "THEROCK_ENABLE_ALL" OFF)
cmake_dependent_option(THEROCK_ENABLE_MATH_LIBS "Enable building of math libraries" ON "THEROCK_ENABLE_ALL" OFF)
cmake_dependent_option(THEROCK_ENABLE_ML_LIBS "Enable building of ML libraries" ON "THEROCK_ENABLE_ALL" OFF)
option(THEROCK_FORCE_DISABLE_ALL "One-shot flag which forces all feature flags to disabled for the current configure run" OFF)

# Base Features.
therock_add_feature(COMPILER
  GROUP ALL
  DESCRIPTION "Enables the AMDGPU+host compiler toolchain"
)
therock_add_feature(HIPIFY
  GROUP ALL
  DESCRIPTION "Enables the hipify tool"
  REQUIRES COMPILER
)

# Core Features.
therock_add_feature(CORE_RUNTIME
  GROUP CORE
  DESCRIPTION "Enables the core device runtime and tools"
)
therock_add_feature(HIP_RUNTIME
  GROUP CORE
  DESCRIPTION "Enables the HIP runtime"
  REQUIRES COMPILER CORE_RUNTIME
)

# Comm-libs Features.
therock_add_feature(RCCL
  GROUP COMM_LIBS
  DESCRIPTION "Enables rccl"
  REQUIRES COMPILER HIP_RUNTIME HIPIFY
)

# Math-libs Features.
therock_add_feature(PRIM
  GROUP MATH_LIBS
  DESCRIPTION "Enables prim libraries (rocprim)"
  REQUIRES COMPILER HIP_RUNTIME
)
therock_add_feature(BLAS
  GROUP MATH_LIBS
  DESCRIPTION "Enables blas libraries (hipblaslt, rocblas, hipblas)"
  REQUIRES COMPILER HIP_RUNTIME
)
therock_add_feature(RAND
  GROUP MATH_LIBS
  DESCRIPTION "Enables rand libraries (hiprand, rocrand)"
  REQUIRES COMPILER HIP_RUNTIME
)
therock_add_feature(SOLVER
  GROUP MATH_LIBS
  DESCRIPTION "Enables solver libraries (hipsolver, rocsolver)"
  REQUIRES COMPILER HIP_RUNTIME BLAS PRIM
)
therock_add_feature(SPARSE
  GROUP MATH_LIBS
  DESCRIPTION "Enables sparse libraries (hipsparse, rocsparse)"
  REQUIRES COMPILER HIP_RUNTIME BLAS PRIM
)

# ML-Libs Features.
therock_add_feature(MIOPEN
  GROUP ML_LIBS
  DESCRIPTION "Enables the MIOpen project (with minimal deps defaults to ON)"
  REQUIRES COMPILER HIP_RUNTIME BLAS RAND
)

# Finalize all feature flags.
therock_finalize_features()

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

therock_validate_amdgpu_targets()

################################################################################
# Global setup
################################################################################

# Some sub-projects need Python. Make sure it is found consistently.
find_package(Python3 3.9 COMPONENTS Interpreter REQUIRED)

configure_file(HIP_VERSION.in ${ROCM_GIT_DIR}/HIP/VERSION)

set(STAGING_INSTALL_DIR "${CMAKE_CURRENT_BINARY_DIR}/staging_install")

# On some distributions, this will install to lib64. We would like
# consistency in built packages, so hard-code it.
set(CMAKE_INSTALL_LIBDIR "lib")

if(CMAKE_C_VISIBILITY_PRESET)
  list(APPEND DEFAULT_CMAKE_ARGS ${CMAKE_C_VISIBILITY_PRESET})
endif()
if(CMAKE_CXX_VISIBILITY_PRESET)
  list(APPEND DEFAULT_CMAKE_ARGS ${CMAKE_CXX_VISIBILITY_PRESET})
endif()


################################################################################
# External project setup
################################################################################

# Add subdirectories in dependency DAG order (which happens to be semi-alpha:
# don't be fooled).
add_subdirectory(third-party)
add_subdirectory(base)

if(NOT WIN32)
  add_subdirectory(compiler)
  add_subdirectory(core)
  add_subdirectory(comm-libs)
  if(THEROCK_ENABLE_MATH_LIBS)
    add_subdirectory(math-libs)
  endif()
  if(THEROCK_ENABLE_ML_LIBS)
    add_subdirectory(ml-libs)
  endif()
else()
  # TODO(#36): Enable more project builds on Windows and/or make the full list configurable.
endif()

add_subdirectory(examples)

# ################################################################################
# # Testing
# ################################################################################

if(NOT WIN32)
  add_executable(
    dlopen-hip
    tests/dlopen-hip.c
  )
  target_link_libraries(dlopen-hip dl)
else()
  # TODO: Test that is compatible with Windows (LoadLibraryA instead of dlopen)
  #   then add instructions in the README to run with a command like
  #   `./build/dlopen-hip install/amdhip64.dll`
endif()


################################################################################
# Finalization
################################################################################
therock_subproject_merge_compile_commands()
therock_create_dist()
