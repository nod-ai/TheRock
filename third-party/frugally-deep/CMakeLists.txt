therock_subproject_fetch(therock-frugally-deep-sources
  CMAKE_PROJECT
  # Originally mirrored from: https://github.com/Dobiasd/frugally-deep/archive/refs/tags/v0.16.2.tar.gz
  URL https://rocm-third-party-deps.s3.us-east-2.amazonaws.com/frugally-deep-0.16.2.tar.gz
  URL_HASH SHA256=b16af09606dcf02359de53b7c47323baaeda9a174e1c87e126c3127c55571971
)

therock_cmake_subproject_declare(therock-frugally-deep
  BACKGROUND_BUILD
  EXCLUDE_FROM_ALL
  NO_MERGE_COMPILE_COMMANDS
  OUTPUT_ON_FAILURE
  EXTERNAL_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/source"
  BUILD_DEPS
    therock-eigen
    therock-nlohmann-json
    therock-FunctionalPlus
)
therock_cmake_subproject_provide_package(
  therock-frugally-deep frugally-deep lib/cmake/frugally-deep)
therock_cmake_subproject_activate(therock-frugally-deep)

add_dependencies(therock-third-party therock-frugally-deep)
