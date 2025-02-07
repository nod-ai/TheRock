therock_subproject_fetch(therock-nlohmann-json-sources
  CMAKE_PROJECT
  URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz
  URL_HASH SHA256=d6c65aca6b1ed68e7a182f4757257b107ae403032760ed6ef121c9d55e81757d
)

therock_cmake_subproject_declare(therock-nlohmann-json
  EXCLUDE_FROM_ALL
  EXTERNAL_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/source"
  CMAKE_ARGS
    -DJSON_BuildTests=OFF
)
therock_cmake_subproject_provide_package(
  therock-nlohmann-json nlohmann_json share/cmake/nlohmann_json)
therock_cmake_subproject_activate(therock-nlohmann-json)

add_dependencies(therock-third-party therock-nlohmann-json)
