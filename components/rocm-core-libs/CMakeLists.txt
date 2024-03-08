cmake_minimum_required(VERSION 3.18)
project(TheRock-rocm-core-libs)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../cmake")
include(therock_project_setup)

# We build as much of the rocm core libraries together in one project as
# possible. There are ordering dependencies here because later projects
# do `if(TARGET)` checks to decide whether to `find_package` vs use in-tree.

# Build rocm-core
add_subdirectory(${ROCM_GIT_DIR}/rocm-core ${CMAKE_BINARY_DIR}/rocm-core)

# Build roct-thunk-interface
add_subdirectory(${ROCM_GIT_DIR}/ROCT-Thunk-Interface ${CMAKE_BINARY_DIR}/ROCT-Thunk-Interface)

# Build rocm-cmake
add_subdirectory(${ROCM_GIT_DIR}/rocm-cmake ${CMAKE_BINARY_DIR}/rocm-cmake)

# Build ROCR-Runtime
set(BUILD_SHARED_LIBS ON)
add_subdirectory(${ROCM_GIT_DIR}/ROCR-Runtime/src ${CMAKE_BINARY_DIR}/ROCR-Runtime)

# add_subdirectory(${ROCM_GIT_DIR}/clr)
