cmake_minimum_required(VERSION 3.18)
project(TheRock)

# Set the default build type to Release if not specified
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Build type" FORCE)
endif()

# Check if ROCM_GIT_DIR was passed in from the command line
if(NOT DEFINED ROCM_GIT_DIR)
  # Define the default path to the adjacent sources if not provided
  get_filename_component(ROCM_GIT_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../rocm" ABSOLUTE)
endif()
message(STATUS "ROCM_GIT_DIR is set to: ${ROCM_GIT_DIR}")

string(TIMESTAMP ROCM_MAJOR_VERSION "%Y%m%d")
set(ROCM_VERSION "${ROCM_MAJOR_VERSION}.0.0" CACHE STRING "ROCM version")
set(AMDGPU_TARGETS "gfx90a gfx942 gfx1100" CACHE STRING "AMDGPU Targets")

set(LLVM_DIR "${ROCM_GIT_DIR}/llvm-project")
message(STATUS "LLVM_DIR is set to: ${LLVM_DIR}")

# Set the LLVM_ENABLE_PROJECTS variable before including LLVM's CMakeLists.txt
set(LLVM_ENABLE_PROJECTS "compiler-rt;lld;clang" CACHE STRING "Enable LLVM projects" FORCE)
set(LLVM_TARGETS_TO_BUILD "AMDGPU;X86" CACHE STRING "Enable LLVM Targets" FORCE)
set(LLVM_EXTERNAL_DEVICE_LIBS_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/device-libs" CACHE STRING "Device libs path" FORCE)
set(LLVM_EXTERNAL_PROJECTS "device-libs" CACHE STRING "Enable device-libs" FORCE)

# Build rocm-core
add_subdirectory(${ROCM_GIT_DIR}/rocm-core ${CMAKE_BINARY_DIR}/rocm-core)

# Now include LLVM's source directory
add_subdirectory(${LLVM_DIR}/llvm ${CMAKE_BINARY_DIR}/llvm)

# Build roct-thunk-interface
add_subdirectory(${ROCM_GIT_DIR}/ROCT-Thunk-Interface ${CMAKE_BINARY_DIR}/ROCT-Thunk-Interface)

# Build rocm-cmake
add_subdirectory(${ROCM_GIT_DIR}/rocm-cmake ${CMAKE_BINARY_DIR}/rocm-cmake)

# BUILD COMGR
set(BUILD_TESTING OFF CACHE BOOL "DISABLE BUILDING TESTS IN SUBPROJECTS" FORCE)
include_directories(${LLVM_DIR}/llvm/include)
include_directories(${CMAKE_BINARY_DIR}/llvm/include)
#LINK_DIRECTORIES(${CMAKE_BINARY_DIR}/LLVM/LIB)
set(LLVM_INCLUDE_DIRS "${CMAKE_BINARY_DIR}/llvm/include" CACHE STRING "Include LLVM Headers" FORCE)
set(LLVM_LIBRARY_DIRS "${CMAKE_BINARY_DIR}/llvm/lib" CACHE STRING "Include LLVM Libs" FORCE)
#SET(LLVM_LINK_LLVM_DYLIB ON CACHE BOOL "ENABLE LLVM DYLIB" FORCE)
add_subdirectory(${LLVM_DIR}/amd/comgr ${CMAKE_BINARY_DIR}/comgr)
