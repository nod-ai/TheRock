therock_subproject_fetch(therock-FunctionalPlus-sources
  CMAKE_PROJECT
  URL https://github.com/Dobiasd/FunctionalPlus/archive/refs/tags/v0.2.25.tar.gz
  URL_HASH SHA256=9b5e24bbc92f43b977dc83efbc173bcf07dbe07f8718fc2670093655b56fcee3
)

therock_cmake_subproject_declare(therock-FunctionalPlus
  BACKGROUND_BUILD
  EXCLUDE_FROM_ALL
  EXTERNAL_SOURCE_DIR "${CMAKE_CURRENT_BINARY_DIR}/source"
)
therock_cmake_subproject_provide_package(
  therock-FunctionalPlus FunctionalPlus lib/cmake/FunctionalPlus)
therock_cmake_subproject_activate(therock-FunctionalPlus)
