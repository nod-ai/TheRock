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

# If defining a new option, ensure it is in the outer CMakeLists.txt and
# the clean_configure_test_project.cmake to ensure it is passed from the
# parent when testing.
option(THEROCK_ENABLE_BLAS "Whether hipblas/hipblaslt/rocblas are available" ON)
option(THEROCK_ENABLE_FFT "Whether the FFT libraries are available" ON)
option(THEROCK_ENABLE_HIP "Whether the HIP runtime and compiler are available" ON)
option(THEROCK_ENABLE_MIOPEN "Whether MIOpen is available" ON)
option(THEROCK_ENABLE_PRIM "Whether rocprim is available" ON)
option(THEROCK_ENABLE_RAND "Whether rocrand/hiprand are available" ON)
option(THEROCK_ENABLE_RCCL "Whether rccl is available" ON)
option(THEROCK_ENABLE_SOLVER "Whether rocsolver/hipsolver are available" ON)
option(THEROCK_ENABLE_SPARSE "Whether rocsparse/hipsparse are available" ON)

# Because we use this project as a test, we include validation that the found
# packages are sound. Users do not need to include this or call any of the
# `validate_*` functions.
include(validate_rocm_sdk)

if(THEROCK_ENABLE_HIP)
    # TODO: Don't require HIP_PLATFORM https://github.com/nod-ai/TheRock/issues/68
    set(HIP_PLATFORM "amd")
    find_package(hip CONFIG REQUIRED)
    validate_hip_package_found()
endif()

if(THEROCK_ENABLE_RAND)
    find_package(hiprand CONFIG REQUIRED)
    find_package(rocrand CONFIG REQUIRED)
    message(STATUS "hiprand version: ${hiprand_VERSION}")
    message(STATUS "rocrand version: ${rocrand_VERSION}")
endif()

if(THEROCK_ENABLE_SPARSE)
    find_package(hipsparse CONFIG REQUIRED)
    find_package(rocsparse CONFIG REQUIRED)
    message(STATUS "hipsparse version: ${hipsparse_VERSION}")
    message(STATUS "rocsparse version: ${rocsparse_VERSION}")
endif()

if(THEROCK_ENABLE_PRIM)
    find_package(rocprim CONFIG REQUIRED)
    message(STATUS "rocprim version: ${rocprim_VERSION}")
endif()

if(THEROCK_ENABLE_SOLVER)
    find_package(hipsolver CONFIG REQUIRED)
    find_package(rocsolver CONFIG REQUIRED)
    message(STATUS "hipsolver version: ${hipsolver_VERSION}")
    message(STATUS "rocsolver version: ${rocsolver_VERSION}")
endif()

if(THEROCK_ENABLE_RCCL)
    find_package(rccl CONFIG REQUIRED)
    message(STATUS "rccl version: ${rccl_VERSION}")
endif()

if(THEROCK_ENABLE_BLAS)
    find_package(hipblaslt CONFIG REQUIRED)
    find_package(hipblas CONFIG REQUIRED)
    find_package(rocblas CONFIG REQUIRED)
    message(STATUS "hipblaslt version: ${hipblaslt_VERSION}")
    message(STATUS "hipblas version: ${hipblas_VERSION}")
    message(STATUS "rocblas version: ${rocblas_VERSION}")
endif()

if(THEROCK_ENABLE_MIOPEN)
    find_package(miopen CONFIG REQUIRED)
    message(STATUS "miopen version: ${miopen_VERSION}")
endif()

if(THEROCK_ENABLE_FFT)
    find_package(hipfft CONFIG REQUIRED)
    find_package(rocfft CONFIG REQUIRED)
    message(STATUS "hipfft version: ${hipfft_VERSION}")
    message(STATUS "rocfft version: ${rocfft_VERSION}")
endif()

if(THEROCK_ENABLE_HIP)
    add_executable(
        hip-host-test
        hip-host-test.cpp
    )
    target_link_libraries(hip-host-test PRIVATE hip::host)
    add_test(NAME hip-host-test COMMAND hip-host-test)
endif()
