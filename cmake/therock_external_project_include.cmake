# This file is injected into each ExternalProject in the super project.
# It sets up various toolchain details.

message(STATUS "TheRock external project configuration injection (${CMAKE_PROJECT_NAME})")

if(EXISTS "${THEROCK_SOURCE_DIR}/cmake/extensions/${CMAKE_PROJECT_NAME}_pre.cmake")
  message(STATUS "Including project extensions: ${CMAKE_PROJECT_NAME}_pre.cmake")
  include("${THEROCK_SOURCE_DIR}/cmake/extensions/${CMAKE_PROJECT_NAME}_pre.cmake")
endif()
cmake_language(DEFER CALL therock_post_external_project)

function(therock_post_external_project)
  if(EXISTS "${THEROCK_SOURCE_DIR}/cmake/extensions/${CMAKE_PROJECT_NAME}_post.cmake")
    message(STATUS "Including project extensions: ${CMAKE_PROJECT_NAME}_post.cmake")
    # Note that because of the way defer processing works, we include in a 
    # function scope, which usually wouldn't make sense. But since this will
    # by definition be the last thing evaluated, there is nothing to observe
    # the top level scope after this anyway, so it is ok to do here.
    include("${THEROCK_SOURCE_DIR}/cmake/extensions/${CMAKE_PROJECT_NAME}_post.cmake")
  endif()
endfunction()
