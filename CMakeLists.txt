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

################################################################################
# Options
################################################################################

option(THEROCK_INTERACTIVE "Enable interactive build mode which will cause all sub-project invocations to stream to the console (reducing parallelism)" OFF)

set(THEROCK_PACKAGE_VERSION "git" CACHE STRING "Sets the package version string")
set(ROCM_GIT_DIR "${THEROCK_SOURCE_DIR}/sources" CACHE PATH "Directory of rocm-org repo checkout")
message(STATUS "ROCM_GIT_DIR is set to: ${ROCM_GIT_DIR}")

# Initialize the install directory.
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${THEROCK_SOURCE_DIR}/install" CACHE PATH "" FORCE)
  message(STATUS "Defaulted CMAKE_INSTALL_PREFIX to ${CMAKE_INSTALL_PREFIX}")
endif()

set(ROCM_MAJOR_VERSION 6)
set(ROCM_MINOR_VERSION 3)
set(ROCM_PATCH_VERSION 1)
set(ROCM_VERSION
  "${ROCM_MAJOR_VERSION}.${ROCM_MINOR_VERSION}.${ROCM_PATCH_VERSION}")
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

option(ALWAYS_BUILD_SUBPROJECTS
  "Don't let the brittle CMake external project machinery decide if a sub-project needs to rebuild. Always run the underlying build."
  OFF)
set(FIND_PACKAGE_OPTIONS)

macro(add_package_path PackageName path)
  list(APPEND FIND_PACKAGE_OPTIONS "-D${PackageName}_DIR=${path}")
endmacro()

set(DEFAULT_CMAKE_ARGS
  -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  -DCMAKE_PLATFORM_NO_VERSIONED_SONAME=${CMAKE_PLATFORM_NO_VERSIONED_SONAME}
  -DPython3_EXECUTABLE=${Python3_EXECUTABLE}
  -DPython3_FIND_VIRTUALENV=${Python3_FIND_VIRTUALENV}
  -DTHEROCK_SOURCE_DIR=${THEROCK_SOURCE_DIR}
  -DROCM_GIT_DIR=${ROCM_GIT_DIR}
  -DROCM_MAJOR_VERSION=${ROCM_MAJOR_VERSION}
  -DROCM_MINOR_VERSION=${ROCM_MINOR_VERSION}
  -DROCM_PATCH_VERSION=${ROCM_PATCH_VERSION}
  -DROCM_VERSION=${ROCM_VERSION}
  "-DROCM_PATH=${STAGING_INSTALL_DIR}"
  "-DCPACK_PACKAGING_INSTALL_PREFIX=${STAGING_INSTALL_DIR}"
  "-DAMDGPU_TARGETS=${AMDGPU_TARGETS}"
  -DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
  -DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
  -DCMAKE_C_COMPILER_LAUNCHER=${CMAKE_C_COMPILER_LAUNCHER}
  -DCMAKE_CXX_COMPILER_LAUNCHER=${CMAKE_CXX_COMPILER_LAUNCHER}
   # On some distributions, this will install to lib64. We would like
   # consistency in built packages, so hard-code it.
   -DCMAKE_INSTALL_LIBDIR=lib
   -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=${CMAKE_CURRENT_SOURCE_DIR}/cmake/therock_external_project_include.cmake
)
if(CMAKE_C_VISIBILITY_PRESET)
  list(APPEND DEFAULT_CMAKE_ARGS ${CMAKE_C_VISIBILITY_PRESET})
endif()
if(CMAKE_CXX_VISIBILITY_PRESET)
  list(APPEND DEFAULT_CMAKE_ARGS ${CMAKE_CXX_VISIBILITY_PRESET})
endif()

# Add subdirectories in dependency DAG order.
add_subdirectory(base)
add_subdirectory(compiler)
add_subdirectory(core)

# ################################################################################
# # HIPCC
# ################################################################################

# ExternalProject_Add(
#   hipcc
#   PREFIX ${CMAKE_CURRENT_BINARY_DIR}/hipcc
#   # Can't build directly as part of LLVM, because we want hipcc staged under
#   # bin, not llvm/bin.
#   SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/hipcc"
#   DEPENDS
#     amd-llvm # runtime
#     rocminfo # runtime
#   CMAKE_ARGS
#     ${DEFAULT_CMAKE_ARGS}
#     ${FIND_PACKAGE_OPTIONS}
#     -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
#     # We install llvm in its own sub-directory.
#     -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}
#   USES_TERMINAL_CONFIGURE TRUE
#   USES_TERMINAL_BUILD TRUE
#   BUILD_ALWAYS ${ALWAYS_BUILD_SUBPROJECTS}
# )

# ################################################################################
# # CLR
# ################################################################################

# ExternalProject_Add(
#   clr
#   PREFIX ${CMAKE_CURRENT_BINARY_DIR}/clr
#   SOURCE_DIR "${ROCM_GIT_DIR}/clr"
#   DEPENDS
#     amd-llvm
#     hipcc
#     rocm-core
#   CMAKE_ARGS
#     ${DEFAULT_CMAKE_ARGS}
#     ${FIND_PACKAGE_OPTIONS}
#     -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}
#     -DHIP_PLATFORM=amd
#     "-DOFFLOAD_ARCH_STR=${AMDGPU_TARGETS}"
#     "-DHIP_CLANG_PATH=${STAGING_INSTALL_DIR}/llvm/bin"
#     # Some junk needs this to be defined but is special cased so if empty,
#     # bad things don't happen.
#     "-DHIPCC_BIN_DIR=${STAGING_INSTALL_DIR}/bin"
#     "-DHIP_COMMON_DIR=${ROCM_GIT_DIR}/HIP"
#     # What is this?
#     -DROCM_PATCH_VERSION=99999
#     -D__HIP_ENABLE_PCH=OFF
#     -DCLR_BUILD_HIP=ON
#     # Force CMake to reconfigure if key values change.
#     "-D_STAMP=${ROCM_MAJOR_VERSION}.${ROCM_MINOR_VERSION}.${ROCM_PATCH_VERSION}"

#   USES_TERMINAL_CONFIGURE TRUE
#   USES_TERMINAL_BUILD TRUE
#   BUILD_ALWAYS ${ALWAYS_BUILD_SUBPROJECTS}
# )

# add_package_path(HIP "${STAGING_INSTALL_DIR}/lib/cmake/hip")
# add_package_path(hip-lang "${STAGING_INSTALL_DIR}/lib/cmake/hip-lang")
# add_package_path(hiprtc "${STAGING_INSTALL_DIR}/lib/cmake/hiprtc")

# ################################################################################
# # ROCm SMI
# ################################################################################

# ExternalProject_Add(
#   rocm_smi_lib
#   PREFIX ${CMAKE_CURRENT_BINARY_DIR}/rocm_smi_lib
#   SOURCE_DIR "${ROCM_GIT_DIR}/rocm_smi_lib"
#   DEPENDS
#     rocm-core
#   CMAKE_ARGS
#     ${DEFAULT_CMAKE_ARGS}
#     ${FIND_PACKAGE_OPTIONS}
#     -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}
#   USES_TERMINAL_CONFIGURE TRUE
#   USES_TERMINAL_BUILD TRUE
#   BUILD_ALWAYS ${ALWAYS_BUILD_SUBPROJECTS}
# )

# add_package_path(rocm-smi "${STAGING_INSTALL_DIR}/lib/cmake/rocm-smi")

# ################################################################################
# # HIPIFY
# ################################################################################

# ExternalProject_Add(
#   hipify
#   PREFIX ${CMAKE_CURRENT_BINARY_DIR}/hipify
#   SOURCE_DIR "${ROCM_GIT_DIR}/HIPIFY"
#   DEPENDS
#     amd-llvm
#     clr
#   CMAKE_ARGS
#     ${DEFAULT_CMAKE_ARGS}
#     ${FIND_PACKAGE_OPTIONS}
#     -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}
#   USES_TERMINAL_CONFIGURE TRUE
#   USES_TERMINAL_BUILD TRUE
#   BUILD_ALWAYS ${ALWAYS_BUILD_SUBPROJECTS}
# )

# ################################################################################
# # RCCL
# ################################################################################

# # TODO: Re-enable rccl after adapting to 6.3.x build option differences.
# # Now seems to depend on rocprofiler.
# # ExternalProject_Add(
# #   rccl
# #   PREFIX ${CMAKE_CURRENT_BINARY_DIR}/rccl
# #   SOURCE_DIR "${ROCM_GIT_DIR}/rccl"
# #   DEPENDS
# #     clr
# #     hipcc
# #     hipify
# #     rocminfo
# #   CMAKE_ARGS
# #     ${DEFAULT_CMAKE_ARGS}
# #     ${FIND_PACKAGE_OPTIONS}
# #     # TODO: Audit how the 6.3.x build finds its C++ compiler.
# #     #-DCMAKE_CXX_COMPILER=${STAGING_INSTALL_DIR}/bin/hipcc
# #     -DCMAKE_CXX_COMPILER=${STAGING_INSTALL_DIR}/lib/llvm/bin/clang++
# #     -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}
# #     -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
# #   USES_TERMINAL_CONFIGURE TRUE
# #   USES_TERMINAL_BUILD TRUE
# #   BUILD_ALWAYS ${ALWAYS_BUILD_SUBPROJECTS}
# # )

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
