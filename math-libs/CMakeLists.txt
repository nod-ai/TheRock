if(THEROCK_ENABLE_BLAS)
  # Many things need to be configured with paths to additional LLVM tools.
  # If a project is using an amd-hip or amd-llvm toolchain, then it will already
  # have an implicit dep on the toolchain, so it is safe to reference binaries
  # here without worrying about build deps.
  therock_cmake_subproject_dist_dir(_blas_hack_hip_dir hip-clr)
  cmake_path(APPEND _blas_hack_hip_dir lib/llvm OUTPUT_VARIABLE _toolchain_dir)

  ##############################################################################
  # hipBLAS-common
  ##############################################################################
  set(_blas_subproject_names)

  therock_cmake_subproject_declare(hipBLAS-common
    EXTERNAL_SOURCE_DIR "hipBLAS-common"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DROCM_PATH=
      -DROCM_DIR=
    COMPILER_TOOLCHAIN
      amd-hip
    IGNORE_PACKAGES
      # The current version of rccl needs to download a 2y old version of rocm-cmake
      # to work and it will only do so if the system resolver reports it not found
      # without any other error (which due to the signature, our resolver will
      # hard fail). Once fixed, `rocm-core` should be added to the BUILD_DEPS
      # and this removed: https://github.com/nod-ai/TheRock/issues/18
      ROCM
    RUNTIME_DEPS
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(hipBLAS-common
    SUBDIRS
      library
  )
  therock_cmake_subproject_provide_package(hipBLAS-common hipblas-common lib/cmake/hipblas-common)
  therock_cmake_subproject_activate(hipBLAS-common)
  list(APPEND _blas_subproject_names hipBLAS-common)

  ##############################################################################
  # hipBLASLt
  ##############################################################################

  therock_cmake_subproject_declare(hipBLASLt
    EXTERNAL_SOURCE_DIR "hipBLASLt"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
      -DTensile_LOGIC=
      -DTensile_CODE_OBJECT_VERSION=default
      -DTensile_CPU_THREADS=
      -DTensile_LIBRARY_FORMAT=msgpack
      -DTensile_HIP_CONFIG=${_blas_hack_hip_dir}/bin/hipconfig
      "-DTensile_C_COMPILER=${_toolchain_dir}/bin/clang"
      "-DTensile_CXX_COMPILER=${_toolchain_dir}/bin/clang++"
      "-DTensile_ASSEMBLER=${_toolchain_dir}/bin/clang++"
      "-DTensile_OFFLOAD_BUNDLER=${_toolchain_dir}/bin/clang-offload-bundler"
      # TODO(#55): Enable once roctracer is added
      -DHIPBLASLT_ENABLE_MARKER=OFF
      # TODO: Enable clients.
    COMPILER_TOOLCHAIN
      amd-hip
    BUILD_DEPS
      hipBLAS-common
      therock-msgpack-cxx
    RUNTIME_DEPS
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(hipBLASLt
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(hipBLASLt hipblaslt lib/cmake/hipblaslt)
  therock_cmake_subproject_activate(hipBLASLt)
  list(APPEND _blas_subproject_names hipBLASLt)


  ##############################################################################
  # rocBLAS
  ##############################################################################

  therock_cmake_subproject_declare(rocBLAS
    EXTERNAL_SOURCE_DIR "rocBLAS"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
      # TODO: Fix passing TENSILE_ROCM_ASSEMBLER_PATH.
      #       Enable building with hipBLASLt afterwards.
      -DBUILD_WITH_TENSILE=OFF
      -DBUILD_WITH_HIPBLASLT=OFF
      # -DTensile_LOGIC=
      # -DTensile_CODE_OBJECT_VERSION=default
      # -DTensile_CPU_THREADS=
      # -DTensile_LIBRARY_FORMAT=msgpack
      # "-DTensile_ROCM_ASSEMBLER_PATH=${_toolchain_dir}/bin/clang++"
      # "-DTensile_ROCM_OFFLOAD_BUNDLER_PATH=${_toolchain_dir}/bin/clang-offload-bundler"
      # TODO: Enable clients.
    IGNORE_PACKAGES
      ROCM
    COMPILER_TOOLCHAIN
      amd-hip
    RUNTIME_DEPS
      #hipBLAS-common
      #hipBLASLt
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(rocBLAS
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(rocBLAS rocblas lib/cmake/rocblas)
  therock_cmake_subproject_activate(rocBLAS)
  list(APPEND _blas_subproject_names rocBLAS)


  ##############################################################################
  # hipBLAS
  ##############################################################################

  therock_cmake_subproject_declare(hipBLAS
    EXTERNAL_SOURCE_DIR "hipBLAS"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
      -DBUILD_WITH_SOLVER=OFF  # TODO: add/enable rocSOLVER
    COMPILER_TOOLCHAIN
      amd-hip
    BUILD_DEPS
      hipBLAS-common
    RUNTIME_DEPS
      hip-clr
      rocBLAS
  )
  therock_cmake_subproject_glob_c_sources(hipBLAS
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(hipBLAS hipblas lib/cmake/hipblas)
  therock_cmake_subproject_activate(hipBLAS)
  list(APPEND _blas_subproject_names hipBLAS)


  ##############################################################################
  # blas artifact
  ##############################################################################

  therock_provide_artifact(blas
    DESCRIPTOR artifact-blas.toml
    COMPONENTS
      dbg
      dev
      doc
      lib
      run
    SUBPROJECT_DEPS ${_blas_subproject_names}
  )
endif(THEROCK_ENABLE_BLAS)

if(THEROCK_ENABLE_RAND)
  ##############################################################################
  # rocRAND
  ##############################################################################
  set(_rand_subproject_names)

  therock_cmake_subproject_declare(rocRAND
    EXTERNAL_SOURCE_DIR "rocRAND"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
    COMPILER_TOOLCHAIN
      amd-hip
    RUNTIME_DEPS
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(rocRAND
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(rocRAND rocrand lib/cmake/rocrand)
  therock_cmake_subproject_activate(rocRAND)
  list(APPEND _rand_subproject_names rocRAND)

  ##############################################################################
  # hipRAND
  ##############################################################################

  therock_cmake_subproject_declare(hipRAND
    EXTERNAL_SOURCE_DIR "hipRAND"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
    COMPILER_TOOLCHAIN
      amd-hip
    BUILD_DEPS
      rocRAND
    RUNTIME_DEPS
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(hipRAND
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(hipRAND hiprand lib/cmake/hiprand)
  therock_cmake_subproject_activate(hipRAND)
  list(APPEND _rand_subproject_names hipRAND)

  ##############################################################################
  # rand artifact
  ##############################################################################

  therock_provide_artifact(rand
    DESCRIPTOR artifact-rand.toml
    COMPONENTS
      dbg
      dev
      doc
      lib
      run
    SUBPROJECT_DEPS ${_rand_subproject_names}
  )
endif(THEROCK_ENABLE_RAND)

if(THEROCK_ENABLE_PRIM)
  ##############################################################################
  # rocPRIM
  ##############################################################################

  therock_cmake_subproject_declare(rocPRIM
    EXTERNAL_SOURCE_DIR "rocPRIM"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
    COMPILER_TOOLCHAIN
      amd-hip
    RUNTIME_DEPS
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(rocPRIM
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(rocPRIM rocprim lib/cmake/rocprim)
  therock_cmake_subproject_activate(rocPRIM)

  therock_provide_artifact(prim
    DESCRIPTOR artifact-prim.toml
    COMPONENTS
      dev
      doc
    SUBPROJECT_DEPS rocPRIM
  )
endif(THEROCK_ENABLE_PRIM)

if(THEROCK_ENABLE_SPARSE)
  ##############################################################################
  # rocSPARSE
  ##############################################################################
  set(_sparse_subproject_names)

  therock_cmake_subproject_declare(rocSPARSE
    EXTERNAL_SOURCE_DIR "rocSPARSE"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
      -DBUILD_WITH_ROCBLAS=ON
      -DBUILD_CLIENTS_SAMPLES=OFF
      -DBUILD_CLIENTS_BENCHMARKS=OFF
      -DBUILD_CLIENTS_SAMPLES=OFF
    COMPILER_TOOLCHAIN
      amd-hip
    BUILD_DEPS
      rocBLAS
      rocPRIM
    RUNTIME_DEPS
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(rocSPARSE
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(rocSPARSE rocsparse lib/cmake/rocsparse)
  therock_cmake_subproject_activate(rocSPARSE)
  list(APPEND _sparse_subproject_names rocSPARSE)

  ##############################################################################
  # hipSPARSE
  ##############################################################################

  therock_cmake_subproject_declare(hipSPARSE
    EXTERNAL_SOURCE_DIR "hipSPARSE"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
      -DBUILD_CLIENTS_SAMPLES=OFF
      -DBUILD_CLIENTS_BENCHMARKS=OFF
      -DBUILD_CLIENTS_SAMPLES=OFF
    COMPILER_TOOLCHAIN
      amd-hip
    BUILD_DEPS
      rocSPARSE
    RUNTIME_DEPS
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(hipSPARSE
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(hipSPARSE hipsparse lib/cmake/hipsparse)
  therock_cmake_subproject_activate(hipSPARSE)
  list(APPEND _sparse_subproject_names hipSPARSE)

  ##############################################################################
  # sparse artifact
  ##############################################################################

  therock_provide_artifact(sparse
    DESCRIPTOR artifact-sparse.toml
    COMPONENTS
      dbg
      dev
      doc
      lib
      run
    SUBPROJECT_DEPS ${_sparse_subproject_names}
  )
endif(THEROCK_ENABLE_SPARSE)

if(THEROCK_ENABLE_SOLVER)
  ##############################################################################
  # rocSOLVER
  ##############################################################################

  therock_cmake_subproject_declare(rocSOLVER
    EXTERNAL_SOURCE_DIR "rocSOLVER"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
      # Requires LAPACK
      -DBUILD_CLIENTS_BENCHMARKS=OFF
      -DBUILD_CLIENTS_TESTS=OFF
    COMPILER_TOOLCHAIN
      amd-hip
    BUILD_DEPS
      rocBLAS
      rocPRIM
      therock-fmt
    RUNTIME_DEPS
      hip-clr
  )
  therock_cmake_subproject_glob_c_sources(rocSOLVER
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(rocSOLVER rocsolver lib/cmake/rocsolver)
  therock_cmake_subproject_activate(rocSOLVER)
  list(APPEND _solver_subproject_names rocSOLVER)

  ##############################################################################
  # hipSOLVER
  ##############################################################################

  therock_cmake_subproject_declare(hipSOLVER
    EXTERNAL_SOURCE_DIR "hipSOLVER"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
      -DBUILD_HIPSPARSE_TESTS=OFF
      # BUILD_WITH_SPARSE converts rocsparse and cholmod to build time vs
      # runtime/dlopen deps.
      -DBUILD_WITH_SPARSE=ON
      # Requires LAPACK
      -DBUILD_CLIENTS_BENCHMARKS=OFF
      -DBUILD_CLIENTS_TESTS=OFF
    COMPILER_TOOLCHAIN
      amd-hip
    RUNTIME_DEPS
      hip-clr
      rocBLAS
      rocSOLVER
      rocSPARSE
      therock-SuiteSparse
  )
  therock_cmake_subproject_glob_c_sources(hipSOLVER
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(hipSOLVER hipsolver lib/cmake/hipsolver)
  therock_cmake_subproject_activate(hipSOLVER)
  list(APPEND _solver_subproject_names hipSOLVER)

  therock_provide_artifact(solver
    DESCRIPTOR artifact-solver.toml
    COMPONENTS
      dbg
      dev
      doc
      lib
      run
    SUBPROJECT_DEPS ${_solver_subproject_names}
  )
endif(THEROCK_ENABLE_SOLVER)

if(THEROCK_ENABLE_FFT)
  ##############################################################################
  # rocFFT
  ##############################################################################
  set(_fft_subproject_names)

  therock_cmake_subproject_declare(rocFFT
    EXTERNAL_SOURCE_DIR "rocFFT"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
      -DBUILD_CLIENTS=OFF
      -DUSE_HIPRAND=ON
    COMPILER_TOOLCHAIN
      amd-hip
    RUNTIME_DEPS
      hip-clr
      hipRAND
  )
  therock_cmake_subproject_glob_c_sources(rocFFT
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(rocFFT rocfft lib/cmake/rocfft)
  therock_cmake_subproject_activate(rocFFT)
  list(APPEND _fft_subproject_names rocFFT)

  ##############################################################################
  # hipFFT
  ##############################################################################

  therock_cmake_subproject_declare(hipFFT
    EXTERNAL_SOURCE_DIR "hipFFT"
    BACKGROUND_BUILD
    CMAKE_ARGS
      -DHIP_PLATFORM=amd
      -DROCM_PATH=
      -DROCM_DIR=
    COMPILER_TOOLCHAIN
      amd-hip
    RUNTIME_DEPS
      hip-clr
      rocFFT
  )
  therock_cmake_subproject_glob_c_sources(hipFFT
    SUBDIRS
      .
  )
  therock_cmake_subproject_provide_package(hipFFT hipfft lib/cmake/hipfft)
  therock_cmake_subproject_activate(hipFFT)
  list(APPEND _fft_subproject_names hipFFT)

  ##############################################################################
  # fft artifact
  ##############################################################################

  therock_provide_artifact(fft
    DESCRIPTOR artifact-fft.toml
    COMPONENTS
      dbg
      dev
      doc
      lib
      run
    SUBPROJECT_DEPS ${_fft_subproject_names}
  )
endif(THEROCK_ENABLE_FFT)
