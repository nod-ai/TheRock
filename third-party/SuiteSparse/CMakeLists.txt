therock_subproject_fetch(therock-SuiteSparse-sources
  CMAKE_PROJECT
  URL https://github.com/DrTimothyAldenDavis/SuiteSparse/archive/refs/tags/v7.8.3.tar.gz
  URL_HASH SHA256=ce39b28d4038a09c14f21e02c664401be73c0cb96a9198418d6a98a7db73a259
)

therock_cmake_subproject_declare(therock-SuiteSparse
  BACKGROUND_BUILD
  EXCLUDE_FROM_ALL
  EXTERNAL_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/source"
  INSTALL_DESTINATION "lib/host-math"
  CMAKE_ARGS
    "-DSUITESPARSE_ENABLE_PROJECTS=\"suitesparse_config;cholmod\""
    -DBLA_VENDOR=OpenBLAS
    -DCHOLMOD_SUPERNODAL=OFF # requires Cholesky, BLAS, and LAPACK
    -DBUILD_STATIC_LIBS=OFF
    -DSUITESPARSE_USE_CUDA=OFF
    -DSUITESPARSE_USE_OPENMP=OFF
  RUNTIME_DEPS
    therock-host-blas
)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse AMD lib/host-math/lib/cmake/AMD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse CAMD lib/host-math/lib/cmake/CAMD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse CCOLAMD lib/host-math/lib/cmake/CCOLAMD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse CHOLMOD lib/host-math/lib/cmake/CHOLMOD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse COLAMD lib/host-math/lib/cmake/COLAMD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse SuiteSparse_config lib/host-math/lib/cmake/SuiteSparse_config)
therock_cmake_subproject_activate(therock-SuiteSparse)

therock_provide_artifact(host-suite-sparse
  DESCRIPTOR artifact-host-suite-sparse.toml
  COMPONENTS
    dbg
    dev
    doc
    lib
    run
  SUBPROJECT_DEPS therock-SuiteSparse
)
