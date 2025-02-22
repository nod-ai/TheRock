if(NOT CMAKE_SOURCE_DIR STREQUAL CMAKE_CURRENT_SOURCE_DIR)
    # When included in TheRock, we download sources and set up the sub-project.
    set(_source_dir "${CMAKE_CURRENT_BINARY_DIR}/source")
    set(_download_stamp "${_source_dir}/download.stamp")

    therock_subproject_fetch(therock-elfutils-sources
      SOURCE_DIR "${_source_dir}"
      URL "https://sourceware.org/elfutils/ftp/0.192/elfutils-0.192.tar.bz2"
      URL_HASH "SHA512=543188f5f2cfe5bc7955a878416c5f252edff9926754e5de0c6c57b132f21d9285c9b29e41281e93baad11d4ae7efbbf93580c114579c182103565fe99bd3909"
      TOUCH "${_download_stamp}"
    )

    therock_cmake_subproject_declare(therock-elfutils
      EXTERNAL_SOURCE_DIR .
      BINARY_DIR build
      NO_MERGE_COMPILE_COMMANDS
      BACKGROUND_BUILD
      OUTPUT_ON_FAILURE

      CMAKE_ARGS
        "-DSOURCE_DIR=${_source_dir}"
        "-DPATCHELF=${PATCHELF}"
      INSTALL_DESTINATION
        lib/rocm_sysdeps
      INTERFACE_LINK_DIRS
        lib/rocm_sysdeps/lib
    EXTRA_DEPENDS
        "${_download_stamp}"
    )
    therock_cmake_subproject_activate(therock-elfutils)

    # Add tests to validate that the shared libraries load.
    # foreach(lib_name libdrm.so libdrm_amdgpu.so)
    #   add_test(
    #     NAME "therock-libdrm-validate-${lib_name}"
    #     COMMAND
    #       "${Python3_EXECUTABLE}" "${THEROCK_SOURCE_DIR}/build_tools/validate_shared_library.py"
    #         "${CMAKE_CURRENT_BINARY_DIR}/build/dist/lib/rocm_sysdeps/lib/${lib_name}"
    #   )
    # endforeach()
    return()
endif()

# Otherwise, this is the sub-project build.
cmake_minimum_required(VERSION 3.25)
project(ELFUTILS_BUILD)

# if(NOT PATCHELF OR NOT MESON_BUILD)
#   message(FATAL_ERROR "Missing PATCHELF or MESON_BUILD from super-project")
# endif()

# add_custom_target(
#   meson_build ALL
#   WORKING_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}"
#   COMMAND
#     "${CMAKE_COMMAND}" -E chdir "${SOURCE_DIR}"
#     "${CMAKE_COMMAND}" -E env
#       # Escaping hack: experimentally determined to persist through the layers.
#       "LDFLAGS=-Wl,-rpath='$$ORIGIN' -Wl,--version-script=${CMAKE_CURRENT_SOURCE_DIR}/version.lds"
#       --
#       "${MESON_BUILD}" setup "${CMAKE_CURRENT_BINARY_DIR}"
#         --reconfigure
#         # We generate relocatable, arch neutral directory layouts and use
#         # DESTDIR to install int ot the lib/rocm_sysdeps tree.
#         --prefix "/"
#         -Dpkgconfig.relocatable=true
#         -Dlibdir=lib
#         # Only enable the libraries we want.
#         -Damdgpu=enabled
#         -Dintel=disabled
#         -Dnouveau=disabled
#         -Dradeon=disabled
#         -Dvmwgfx=disabled
#   COMMAND
#     "${MESON_BUILD}" compile --verbose
#   COMMAND
#     "${CMAKE_COMMAND}" -E env "DESTDIR=${CMAKE_INSTALL_PREFIX}/lib/rocm_sysdeps" --
#       "${MESON_BUILD}" install
#   COMMAND
#     "${CMAKE_CURRENT_SOURCE_DIR}/patch_install_binaries.sh"
#       ${CMAKE_INSTALL_PREFIX}/lib/rocm_sysdeps "${PATCHELF}"
# )
