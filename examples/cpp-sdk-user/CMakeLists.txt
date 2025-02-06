# Build with:
#   cmake -GNinja -S. -Bbuild -DCMAKE_PREFIX_PATH=path/to/rocm
if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are not allowed. Please create a separate build directory.")
endif()

cmake_minimum_required(VERSION 3.25)

project(rocm-cpp-sdk-user)
set(CMAKE_CXX_STANDARD 17)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

# Because we use this project as a test, we include validation that the found
# packages are sound. Users do not need to include this or call any of the
# `validate_*` functions.
include(validate_rocm_sdk)

# TODO: Don't require HIP_PLATFORM https://github.com/nod-ai/TheRock/issues/68
set(HIP_PLATFORM "amd")
find_package(hip CONFIG REQUIRED)
validate_hip_package_found()

find_package(hipsparse CONFIG REQUIRED)
find_package(rocsolver CONFIG REQUIRED)
find_package(rocprim CONFIG REQUIRED)
find_package(rocrand CONFIG REQUIRED)

find_package(rccl CONFIG REQUIRED)
find_package(hipblaslt CONFIG REQUIRED)
find_package(hipblas CONFIG REQUIRED)
find_package(miopen CONFIG REQUIRED)
