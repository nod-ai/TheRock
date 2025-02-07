if(EXISTS "${BINARY_DIR}")
  message(STATUS "Removing build dir ${BINARY_DIR}")
  file(REMOVE_RECURSE "${BINARY_DIR}")
endif()

execute_process(
  COMMAND "${CMAKE_CTEST_COMMAND}" --build-and-test
    "${SOURCE_DIR}"
    "${BINARY_DIR}"
    --build-generator "${GENERATOR}"
    --test-command "${CMAKE_CTEST_COMMAND}" --output-on-failure
  RESULT_VARIABLE CMD_RESULT
)

if(CMD_RESULT)
  message(FATAL_ERROR "Failed to execute test process")
endif()
