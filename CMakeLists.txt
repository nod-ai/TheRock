cmake_minimum_required(VERSION 3.18)
project(TheRock)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(therock_project_setup)
include(ExternalProject)

################################################################################
# Global setup
################################################################################

configure_file(HIP_VERSION.in ${ROCM_GIT_DIR}/HIP/VERSION)

################################################################################
# External project setup
################################################################################

set(FIND_PACKAGE_OPTIONS)

macro(add_package_path PackageName path)
  list(APPEND FIND_PACKAGE_OPTIONS "-D${PackageName}_DIR=${path}")
endmacro()

set(DEFAULT_CMAKE_ARGS
  -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
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
    -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}/llvm
  USES_TERMINAL_CONFIGURE TRUE
  USES_TERMINAL_BUILD TRUE
  #BUILD_ALWAYS TRUE
)

add_package_path(amd_comgr "${CMAKE_INSTALL_PREFIX}/llvm/lib/cmake/amd_comgr")
add_package_path(Clang "${CMAKE_INSTALL_PREFIX}/llvm/lib/cmake/clang")
add_package_path(LLD "${CMAKE_INSTALL_PREFIX}/llvm/lib/cmake/lld")
add_package_path(LLVM "${CMAKE_INSTALL_PREFIX}/llvm/lib/cmake/llvm")
add_package_path(AMDDeviceLibs "${CMAKE_INSTALL_PREFIX}/llvm/lib/cmake/AMDDeviceLibs")

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
    -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
  USES_TERMINAL_CONFIGURE TRUE
  USES_TERMINAL_BUILD TRUE
  #BUILD_ALWAYS TRUE
)

add_package_path(hsakmt "${CMAKE_INSTALL_PREFIX}/lib/cmake/hsakmt")
add_package_path(hsa-runtime64 "${CMAKE_INSTALL_PREFIX}/lib/cmake/hsa-runtime64")

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
    -DCMAKE_INSTALL_PREFIX=${CMAKE_INSTALL_PREFIX}
    -DHIP_PLATFORM=amd
    "-DOFFLOAD_ARCH_STR=${AMDGPU_TARGETS}"
    "-DHIP_CLANG_PATH=${CMAKE_INSTALL_PREFIX}/llvm/bin"
    # Some junk needs this to be defined but is special cased so if empty,
    # bad things don't happen.
    "-DHIPCC_BIN_DIR="
    "-DHIP_COMMON_DIR=${ROCM_GIT_DIR}/HIP"
    "-DROCM_PATH=${CMAKE_INSTALL_PREFIX}"
    # What is this?
    -DROCM_PATCH_VERSION=99999
    -D__HIP_ENABLE_PCH=OFF
    -DCLR_BUILD_HIP=ON
    # Force CMake to reconfigure if key values change.
    "-D_STAMP=${ROCM_MAJOR_VERSION}.${ROCM_MINOR_VERSION}.${ROCM_PATCH_VERSION}"

  USES_TERMINAL_CONFIGURE TRUE
  USES_TERMINAL_BUILD TRUE    
)

add_package_path(HIP "${CMAKE_INSTALL_PREFIX}/lib/cmake/hip")
add_package_path(hip-lang "${CMAKE_INSTALL_PREFIX}/lib/cmake/hip-lang")
add_package_path(hiprtc "${CMAKE_INSTALL_PREFIX}/lib/cmake/hiprtc")

################################################################################
# CLR
################################################################################

add_executable(
  dlopen-hip
  tests/dlopen-hip.c
)
target_link_libraries(dlopen-hip dl)
