add_test(
  NAME therock-examples-cpp-sdk-user
  COMMAND
    "${CMAKE_COMMAND}" -E env "CMAKE_PREFIX_PATH=${THEROCK_BINARY_DIR}/dist/rocm" --
    "${CMAKE_COMMAND}"
        "-DSOURCE_DIR=${CMAKE_CURRENT_SOURCE_DIR}/cpp-sdk-user"
        "-DBINARY_DIR=${CMAKE_CURRENT_BINARY_DIR}/cpp-sdk-user"
        "-DGENERATOR=${CMAKE_GENERATOR}"
      -P "${CMAKE_CURRENT_SOURCE_DIR}/clean_configure_test_project.cmake"
)
