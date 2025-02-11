# Build with:
#   cmake -GNinja -S. -Bbuild -DCMAKE_PREFIX_PATH=path/to/rocm
if ("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "In-source builds are not allowed. Please create a separate build directory.")
endif()

cmake_minimum_required(VERSION 3.25)

project(rocm-cpp-sdk-user)
enable_testing()

set(CMAKE_CXX_STANDARD 17)
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

option(HAVE_BLAS "Whether hipblas/hipblaslt/rocblas are available" ON)
option(HAVE_HIP "Whether the HIP runtime and compiler are available" ON)
option(HAVE_MIOPEN "Whether MIOpen is available" ON)
option(HAVE_PRIM "Whether rocprim is available" ON)
option(HAVE_RAND "Whether rocrand/hiprand are available" ON)
option(HAVE_RCCL "Whether rccl is available" ON)
option(HAVE_SOLVER "Whether rocsolver/hipsolver are available" ON)
option(HAVE_SPARSE "Whether rocsparse/hipsparse are available" ON)

# Because we use this project as a test, we include validation that the found
# packages are sound. Users do not need to include this or call any of the
# `validate_*` functions.
include(validate_rocm_sdk)

# TODO: Don't require HIP_PLATFORM https://github.com/nod-ai/TheRock/issues/68
set(HIP_PLATFORM "amd")
find_package(hip CONFIG REQUIRED)
validate_hip_package_found()

if(HAVE_RAND)
    find_package(hiprand CONFIG REQUIRED)
    find_package(rocrand CONFIG REQUIRED)
    message(STATUS "hiprand version: ${hiprand_VERSION}")
    message(STATUS "rocrand version: ${rocrand_VERSION}")
endif()

if(HAVE_SPARSE)
    find_package(hipsparse CONFIG REQUIRED)
    find_package(rocsparse CONFIG REQUIRED)
    message(STATUS "hipsparse version: ${hipsparse_VERSION}")
    message(STATUS "rocsparse version: ${rocsparse_VERSION}")
endif()

if(HAVE_PRIM)
    find_package(rocprim CONFIG REQUIRED)
    message(STATUS "rocprim version: ${rocprim_VERSION}")
endif()

if(HAVE_SOLVER)
    find_package(rocsolver CONFIG REQUIRED)
    message(STATUS "rocsolver version: ${rocsolver_VERSION}")
endif()

if(HAVE_RCCL)
    find_package(rccl CONFIG REQUIRED)
    message(STATUS "rccl version: ${rccl_VERSION}")
endif()

if(HAVE_BLAS)
    find_package(hipblaslt CONFIG REQUIRED)
    find_package(hipblas CONFIG REQUIRED)
    find_package(rocblas CONFIG REQUIRED)
    message(STATUS "hipblaslt version: ${hipblaslt_VERSION}")
    message(STATUS "hipblas version: ${hipblas_VERSION}")
    message(STATUS "rocblas version: ${rocblas_VERSION}")
endif()

if(HAVE_MIOPEN)
    find_package(miopen CONFIG REQUIRED)
    message(STATUS "miopen version: ${miopen_VERSION}")
endif()

if(HAVE_HIP)
    add_executable(
        hip-host-test
        hip-host-test.cpp
    )
    target_link_libraries(hip-host-test PRIVATE hip::host)
    add_test(NAME hip-host-test COMMAND hip-host-test)
endif()
