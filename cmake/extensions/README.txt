When the super-project build system configures a sub-project, it injects a
hook that performs additional pre and post-processing. A primary thing that
does is look for include files here:

  ${CMAKE_PROJECT_NAME}_pre.cmake
  ${CMAKE_PROJECT_NAME}_post.cmake

If found, they are included.
