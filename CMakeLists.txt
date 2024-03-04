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

set(LLVM_DIR "${ROCM_GIT_DIR}/llvm-project/llvm")
message(STATUS "LLVM_DIR is set to: ${LLVM_DIR}")

# Set the LLVM_ENABLE_PROJECTS variable before including LLVM's CMakeLists.txt
set(LLVM_ENABLE_PROJECTS "compiler-rt;lld;clang" CACHE STRING "Enable LLVM projects" FORCE)
set(LLVM_TARGETS_TO_BUILD "AMDGPU;X86" CACHE STRING "Enable LLVM Targets" FORCE)

# Build rocm-core
add_subdirectory(${ROCM_GIT_DIR}/rocm-core ${CMAKE_BINARY_DIR}/rocm-core)

# Now include LLVM's source directory
add_subdirectory(${LLVM_DIR} ${CMAKE_BINARY_DIR}/llvm)

# Build roct-thunk-interface
add_subdirectory(${ROCM_GIT_DIR}/ROCT-Thunk-Interface ${CMAKE_BINARY_DIR}/ROCT-Thunk-Interface)
