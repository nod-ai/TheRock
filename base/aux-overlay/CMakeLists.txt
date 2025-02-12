# Auxiliary Overlay
#
# This project contains some odds and ends needed in order to complete
# assembly of a full SDK. This includes:
#
# * Various redirect files to account for where things live in the tree from
# a user perspective.
# * Symlinks to account for distribution-level layout changes.
# * Other hacks as needed.

cmake_minimum_required(VERSION 3.25)

project(therock-aux-overlay)

if(NOT WIN32)
  add_custom_target(symlinks ALL
    COMMAND "${CMAKE_COMMAND}" -E create_symlink "lib/llvm" "${CMAKE_CURRENT_BINARY_DIR}/llvm"
  )
  install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/llvm"
    DESTINATION .
  )
endif()

install(DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/overlay/" DESTINATION ".")
