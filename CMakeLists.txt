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

################################################################################
# Core deps
################################################################################

# Build rocm-core
add_subdirectory(${ROCM_GIT_DIR}/rocm-core ${CMAKE_BINARY_DIR}/rocm-core)

# Build roct-thunk-interface
add_subdirectory(${ROCM_GIT_DIR}/ROCT-Thunk-Interface ${CMAKE_BINARY_DIR}/ROCT-Thunk-Interface)

# Build rocm-cmake
add_subdirectory(${ROCM_GIT_DIR}/rocm-cmake ${CMAKE_BINARY_DIR}/rocm-cmake)

################################################################################
# LLVM
################################################################################

# Build LLVM and the comgr dependency.
# Note that in LLVM "BUILD_SHARED_LIBS" enables an unsupported development mode.
# The flag you want for a shared library build is LLVM_BUILD_LLVM_DYLIB.
set(BUILD_SHARED_LIBS OFF)
set(LLVM_BUILD_LLVM_DYLIB ON)
# TODO: Depending on what is getting released, it may or may not be paying
# for itself to dynamically link.
set(LLVM_LINK_LLVM_DYLIB OFF)
set(LLVM_DIR "${ROCM_GIT_DIR}/llvm-project")
message(STATUS "LLVM_DIR is set to: ${LLVM_DIR}")

# Set the LLVM_ENABLE_PROJECTS variable before including LLVM's CMakeLists.txt
set(BUILD_TESTING OFF CACHE BOOL "DISABLE BUILDING TESTS IN SUBPROJECTS" FORCE)
set(LLVM_ENABLE_PROJECTS "compiler-rt;lld;clang" CACHE STRING "Enable LLVM projects" FORCE)
set(LLVM_TARGETS_TO_BUILD "AMDGPU;X86" CACHE STRING "Enable LLVM Targets" FORCE)
set(LLVM_EXTERNAL_DEVICE_LIBS_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/device-libs" CACHE STRING "Device libs path" FORCE)
set(LLVM_EXTERNAL_PROJECTS "amddevice-libs;amdcomgr" CACHE STRING "Enable extra projects" FORCE)
set(LLVM_EXTERNAL_AMDCOMGR_SOURCE_DIR "${LLVM_DIR}/amd/comgr")
set(LLVM_EXTERNAL_AMDDEVICE_LIBS_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/device-libs")

# Now include LLVM's source directory
add_subdirectory(${LLVM_DIR}/llvm ${CMAKE_BINARY_DIR}/llvm)

################################################################################
# Sub-projects that depend on built LLVM
################################################################################

# Build ROCR-Runtime
# This requires clang and llvm-objcopy and target detects them as part of
# configure. Note that we must explicitly have the code generation depend on
# the device libs to get build ordering right. That list of deps comes from the
# magic AMD_DEVICE_LIBS global property.
set(BUILD_SHARED_LIBS ON)
set(ROCR_RUNTIME_DEVICE_LIB_PATH "${CMAKE_BINARY_DIR}/llvm/tools/amddevice-libs/amdgcn/bitcode")
get_property(ROCR_RUNTIME_DEVICE_LIB_DEPS GLOBAL PROPERTY AMD_DEVICE_LIBS)

#set(ROCR_RUNTIME_DEVICE_LIB_DEPS "rocm-device-libs")
add_subdirectory(${ROCM_GIT_DIR}/ROCR-Runtime/src ${CMAKE_BINARY_DIR}/ROCR-Runtime)
