# Standalone CMake script to merge a list of directories into one output
# directory, respecting symbolic links and warning on namespace collisions.
# By default, this hard links files vs copying. The contents of the out
# directory will be recursively deleted.
#
# Usage:
#   cmake -P merge_dist_dir.cmake {out_directory} {src_directory...}
# Do not follow symlinks by default.
cmake_policy(SET CMP0009 NEW)

function(parse_args)
  # Parse cmake args. Script invocation is like: ... -P this.cmake <args>
  set(_all_args)
  set(_index 0)
  while(_index LESS ${CMAKE_ARGC})
    list(APPEND _all_args "${CMAKE_ARGV${_index}}")
    math(EXPR _index "${_index} + 1")
  endwhile()
  list(FIND _all_args "-P" _index)
  if(_index LESS 0)
    message(FATAL_ERROR "Could not find -P argument")
  endif()
  math(EXPR _index "${_index} + 2")
  list(SUBLIST _all_args ${_index} -1 _all_args)

  list(POP_FRONT _all_args _out_dir)
  list(REVERSE _all_args)
  set(link_out_dir "${_out_dir}" PARENT_SCOPE)
  set(link_from_dirs "${_all_args}" PARENT_SCOPE)
endfunction()

parse_args()

# Remove the directory children (we do this vs removing the directory itself
# so as to cause less churn to tools that may have it as a cwd).
file(MAKE_DIRECTORY "${link_out_dir}")
file(GLOB existing_children "${link_out_dir}/*")
foreach(existing_child ${existing_children})
  file(REMOVE_RECURSE "${existing_child}")
endforeach()

foreach(from_dir ${link_from_dirs})
  file(GLOB_RECURSE rel_paths LIST_DIRECTORIES true RELATIVE "${from_dir}"
    "${from_dir}/*")
  foreach(rel_path ${rel_paths})
    set(src_path "${from_dir}/${rel_path}")
    set(dst_path "${link_out_dir}/${rel_path}")
    if(IS_DIRECTORY "${src_path}")
      make_directory("${dst_path}")
    else()
      if(EXISTS "${dst_path}")
        message(WARNING "Distribution directory path already exists: ${rel_path} (in ${dst_path}). "
                        "This typically means that more than one sub-project provided the same file.")
      endif()
      if(IS_SYMLINK "${src_path}")
        file(READ_SYMLINK "${src_path}" symlink)
        file(CREATE_LINK "${symlink}" "${dst_path}" SYMBOLIC)
      else()
        # Hard link regular files.
        file(CREATE_LINK "${src_path}" "${dst_path}" COPY_ON_ERROR)
      endif()
    endif()
  endforeach()
endforeach()
