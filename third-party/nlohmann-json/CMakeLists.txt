# TODO: Extract this into a therock_cmake_subproject_fetch
ExternalProject_Add(
  nlohmann-json-sources
  EXCLUDE_FROM_ALL TRUE
  PREFIX "${CMAKE_CURRENT_BINARY_DIR}/fetch"
  SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/source"
  CONFIGURE_COMMAND ""
  BUILD_COMMAND ""
  TEST_COMMAND ""
  # therock_cmake_subproject_declare adds a dependency on CMakeLists.txt in
  # the source, so we have to make it known to CMake. This establishes the
  # command-level dependency chain to download the sources.
  INSTALL_COMMAND
    "${CMAKE_COMMAND}" -E touch "${CMAKE_CURRENT_BINARY_DIR}/source/CMakeLists.txt"
  INSTALL_BYPRODUCTS "${CMAKE_CURRENT_BINARY_DIR}/source/CMakeLists.txt"

  # Note: For some reason the corresponding git repo is hundreds of MB, even
  # when shallow-fetched. So just use a source snapshot.
  URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz
  URL_HASH SHA256=d6c65aca6b1ed68e7a182f4757257b107ae403032760ed6ef121c9d55e81757d
)

therock_cmake_subproject_declare(nlohmann-json
  EXTERNAL_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/source"
  CMAKE_ARGS
    -DJSON_BuildTests=OFF
)
therock_cmake_subproject_provide_package(nlohmann-json nlohmann_json share/cmake/nlohmann_json)
therock_cmake_subproject_activate(nlohmann-json)
