# Right now we only support OpenBLAS as the host BLAS library.
# This will be extended later, including allowing to use the system BLAS of
# your choice.

therock_subproject_fetch(therock-OpenBLAS-sources
  CMAKE_PROJECT
  # Originally mirrored from: https://github.com/OpenMathLib/OpenBLAS/releases/download/v0.3.29/OpenBLAS-0.3.29.tar.gz
  URL https://rocm-third-party-deps.s3.us-east-2.amazonaws.com/OpenBLAS-0.3.29.tar.gz
  URL_HASH SHA256=38240eee1b29e2bde47ebb5d61160207dc68668a54cac62c076bb5032013b1eb
  # Originally posted MD5 was recomputed as SHA256 manually:
  # URL_HASH MD5=853a0c5c0747c5943e7ef4bbb793162d
)

therock_cmake_subproject_declare(therock-host-blas
  BACKGROUND_BUILD
  EXCLUDE_FROM_ALL
  NO_MERGE_COMPILE_COMMANDS
  OUTPUT_ON_FAILURE
  EXTERNAL_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/source"
  INSTALL_DESTINATION "lib/host-math"
  INTERFACE_LINK_DIRS "lib/host-math/lib"
  CMAKE_ARGS
    -DBUILD_SHARED_LIBS=ON
    # TODO: DYNAMIC_ARCH=ON produces illegal elf files
    # See: https://github.com/nod-ai/TheRock/issues/83
    -DDYNAMIC_ARCH=OFF
    -DC_LAPACK=ON
    -DBUILD_TESTING=OFF
)
therock_cmake_subproject_provide_package(therock-host-blas OpenBLAS lib/host-math/lib/cmake/OpenBLAS)
therock_cmake_subproject_activate(therock-host-blas)

therock_provide_artifact(host-blas
  DESCRIPTOR artifact-host-OpenBLAS.toml
  COMPONENTS
    dbg
    dev
    doc
    lib
    run
  SUBPROJECT_DEPS therock-host-blas
)
