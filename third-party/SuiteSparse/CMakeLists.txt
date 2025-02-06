therock_subproject_fetch(therock-SuiteSparse-sources
  CMAKE_PROJECT
  URL https://github.com/DrTimothyAldenDavis/SuiteSparse/archive/refs/tags/v7.8.3.tar.gz
  URL_HASH SHA256=ce39b28d4038a09c14f21e02c664401be73c0cb96a9198418d6a98a7db73a259
)

therock_cmake_subproject_declare(therock-SuiteSparse
  BACKGROUND_BUILD
  EXCLUDE_FROM_ALL
  EXTERNAL_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/source"
  CMAKE_ARGS
    "-DSUITESPARSE_ENABLE_PROJECTS=\"suitesparse_config;cholmod\""
    -DCHOLMOD_SUPERNODAL=OFF # requires Cholesky, BLAS, and LAPACK
    -DBUILD_STATIC_LIBS=OFF
    -DSUITESPARSE_USE_CUDA=OFF
)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse AMD lib/cmake/AMD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse CAMD lib/cmake/CAMD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse CCOLAMD lib/cmake/CCOLAMD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse CHOLMOD lib/cmake/CHOLMOD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse COLAMD lib/cmake/COLAMD)
therock_cmake_subproject_provide_package(
  therock-SuiteSparse SuiteSparse_config lib/cmake/SuiteSparse_config)
therock_cmake_subproject_activate(therock-SuiteSparse)
