cmake_minimum_required(VERSION 3.18)

# Set the default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

project(THEROCK)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(ExternalProject)

################################################################################
# Options
################################################################################

set(PACKAGE_VERSION "git" CACHE PATH "Sets the package version string")
set(ROCM_GIT_DIR "${THEROCK_SOURCE_DIR}/sources" CACHE PATH "Directory of rocm-org repo checkout")
message(STATUS "ROCM_GIT_DIR is set to: ${ROCM_GIT_DIR}")

# Initialize the install directory.
if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
  set(CMAKE_INSTALL_PREFIX "${THEROCK_SOURCE_DIR}/install" CACHE PATH "" FORCE)
  message(STATUS "Defaulted CMAKE_INSTALL_PREFIX to ${CMAKE_INSTALL_PREFIX}")
endif()

set(ROCM_MAJOR_VERSION 6)
set(ROCM_MINOR_VERSION 0)
set(ROCM_PATCH_VERSION 0)
set(ROCM_VERSION "${ROCM_MAJOR_VERSION}.0.0" CACHE STRING "ROCM version")
set(AMDGPU_TARGETS "gfx90a gfx942 gfx1100" CACHE STRING "AMDGPU Targets")

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

set(ALWAYS_BUILD_SUBPROJECTS OFF)
set(FIND_PACKAGE_OPTIONS)

macro(add_package_path PackageName path)
  list(APPEND FIND_PACKAGE_OPTIONS "-D${PackageName}_DIR=${path}")
endmacro()

set(DEFAULT_CMAKE_ARGS
  -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  -DPython3_EXECUTABLE=${Python3_EXECUTABLE}
  -DPython3_FIND_VIRTUALENV=${Python3_FIND_VIRTUALENV}
  -DTHEROCK_SOURCE_DIR=${THEROCK_SOURCE_DIR}
  -DROCM_GIT_DIR=${ROCM_GIT_DIR}
  -DROCM_MAJOR_VERSION=${ROCM_MAJOR_VERSION}
  -DROCM_MINOR_VERSION=${ROCM_MINOR_VERSION}
  -DROCM_PATCH_VERSION=${ROCM_PATCH_VERSION}
  -DROCM_VERSION=${ROCM_VERSION}
  "-DAMDGPU_TARGETS=${AMDGPU_TARGETS}"
  -DCMAKE_C_COMPILER_LAUNCHER=${CMAKE_C_COMPILER_LAUNCHER}
  -DCMAKE_CXX_COMPILER_LAUNCHER=${CMAKE_CXX_COMPILER_LAUNCHER}
   # On some distributions, this will install to lib64. We would like
   # consistency in built packages, so hard-code it.
   -DCMAKE_INSTALL_LIBDIR=lib
   -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=${CMAKE_CURRENT_SOURCE_DIR}/cmake/external_project_include.cmake
)

################################################################################
# LLVM
################################################################################

ExternalProject_Add(
  amd-llvm
  PREFIX ${CMAKE_CURRENT_BINARY_DIR}/amd-llvm
  SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/components/amd-llvm"
  CMAKE_ARGS
    ${DEFAULT_CMAKE_ARGS}
    ${FIND_PACKAGE_OPTIONS}
    -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
    -DCMAKE_C_COMPILER_LAUNCHER=${CMAKE_C_COMPILER_LAUNCHER}
    -DCMAKE_CXX_COMPILER_LAUNCHER=${CMAKE_CXX_COMPILER_LAUNCHER}
    # We install llvm in its own sub-directory.
    -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}/llvm
  USES_TERMINAL_CONFIGURE TRUE
  USES_TERMINAL_BUILD TRUE
  BUILD_ALWAYS ${ALWAYS_BUILD_SUBPROJECTS}
)

add_package_path(amd_comgr "${STAGING_INSTALL_DIR}/llvm/lib/cmake/amd_comgr")
add_package_path(Clang "${STAGING_INSTALL_DIR}/llvm/lib/cmake/clang")
add_package_path(LLD "${STAGING_INSTALL_DIR}/llvm/lib/cmake/lld")
add_package_path(LLVM "${STAGING_INSTALL_DIR}/llvm/lib/cmake/llvm")
add_package_path(AMDDeviceLibs "${STAGING_INSTALL_DIR}/llvm/lib/cmake/AMDDeviceLibs")

################################################################################
# rocm-core-libs
################################################################################

ExternalProject_Add(
  rocm-core-libs
  DEPENDS
    amd-llvm
  PREFIX ${CMAKE_CURRENT_BINARY_DIR}/rocm-core-libs
  SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/components/rocm-core-libs"
  CMAKE_ARGS
    ${DEFAULT_CMAKE_ARGS}
    ${FIND_PACKAGE_OPTIONS}
    -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}
  USES_TERMINAL_CONFIGURE TRUE
  USES_TERMINAL_BUILD TRUE
  BUILD_ALWAYS ${ALWAYS_BUILD_SUBPROJECTS}
)

add_package_path(hsakmt "${STAGING_INSTALL_DIR}/lib/cmake/hsakmt")
add_package_path(hsa-runtime64 "${STAGING_INSTALL_DIR}/lib/cmake/hsa-runtime64")

################################################################################
# CLR
################################################################################

ExternalProject_Add(
  clr
  PREFIX ${CMAKE_CURRENT_BINARY_DIR}/clr
  SOURCE_DIR "${ROCM_GIT_DIR}/clr"
  DEPENDS
    amd-llvm
    rocm-core-libs
  BUILD_ALWAYS TRUE
  CMAKE_ARGS
    ${DEFAULT_CMAKE_ARGS}
    ${FIND_PACKAGE_OPTIONS}
    -DCMAKE_INSTALL_PREFIX=${STAGING_INSTALL_DIR}
    -DHIP_PLATFORM=amd
    "-DOFFLOAD_ARCH_STR=${AMDGPU_TARGETS}"
    "-DHIP_CLANG_PATH=${STAGING_INSTALL_DIR}/llvm/bin"
    # Some junk needs this to be defined but is special cased so if empty,
    # bad things don't happen.
    "-DHIPCC_BIN_DIR="
    "-DHIP_COMMON_DIR=${ROCM_GIT_DIR}/HIP"
    "-DROCM_PATH=${STAGING_INSTALL_DIR}"
    # What is this?
    -DROCM_PATCH_VERSION=99999
    -D__HIP_ENABLE_PCH=OFF
    -DCLR_BUILD_HIP=ON
    # Force CMake to reconfigure if key values change.
    "-D_STAMP=${ROCM_MAJOR_VERSION}.${ROCM_MINOR_VERSION}.${ROCM_PATCH_VERSION}"

  USES_TERMINAL_CONFIGURE TRUE
  USES_TERMINAL_BUILD ${ALWAYS_BUILD_SUBPROJECTS}    
)

add_package_path(HIP "${STAGING_INSTALL_DIR}/lib/cmake/hip")
add_package_path(hip-lang "${STAGING_INSTALL_DIR}/lib/cmake/hip-lang")
add_package_path(hiprtc "${STAGING_INSTALL_DIR}/lib/cmake/hiprtc")

################################################################################
# Testing
################################################################################

add_executable(
  dlopen-hip
  tests/dlopen-hip.c
)
target_link_libraries(dlopen-hip dl)

################################################################################
# Packaging
# Since our notion of packaging does not follow the actual sub-projects,
# we repackage based on what they have installed.
################################################################################

install(
  CODE "set(STAGING_INSTALL_DIR ${STAGING_INSTALL_DIR})"
  ALL_COMPONENTS
)

install(
  SCRIPT "cmake/custom_install_amdgpu_runtime.cmake" 
  COMPONENT amdgpu-runtime
)

install(
  SCRIPT "cmake/custom_install_amdgpu_runtime_dev.cmake"
  COMPONENT amdgpu-runtime-dev
)

install(
  SCRIPT "cmake/custom_install_amdgpu_compiler.cmake"
  COMPONENT amdgpu-compiler
)

set(CPACK_PACKAGE_NAME "TheRock")
set(CPACK_PACKAGE_VENDOR "Advanced Micro Devices")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Standalone amdgpu runtime packages")
set(CPACK_PACKAGE_VERSION "${PACKAGE_VERSION}")
set(CPACK_PACKAGE_VERSION_MAJOR "${ROCM_MAJOR_VERSION}")
set(CPACK_PACKAGE_VERSION_MINOR "${ROCM_MINOR_VERSION}")
set(CPACK_PACKAGE_VERSION_PATCH "${ROCM_PATCH_VERSION}")
set(CPACK_PACKAGE_INSTALL_DIRECTORY "TheRock-amdgpu")

set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)

include(CPack)

cpack_add_component(
  amdgpu-runtime 
  DISPLAY_NAME "AMD GPU Runtime"
)
cpack_add_component(
  amdgpu-runtime-dev 
  DISPLAY_NAME "AMD GPU Development Components"
  DEPENDS amdgpu-runtime
)
cpack_add_component(
  amdgpu-compiler 
  DISPLAY_NAME "AMD GPU Compiler"
)
