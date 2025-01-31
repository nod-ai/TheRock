################################################################################
# amd-llvm
################################################################################

therock_cmake_subproject_declare(amd-llvm
  EXTERNAL_SOURCE_DIR "amd-llvm"
  # Note that LLVM top level CMakeLists.txt is in the llvm subdir of the
  # monorepo.
  CMAKE_LISTS_RELPATH "llvm"
  CMAKE_ARGS
    -DLLVM_INCLUDE_TESTS=OFF
  INTERFACE_PROGRAM_DIRS
    lib/llvm/bin
  BUILD_DEPS
    rocm-cmake
  # The entire LLVM install tree is placed inside of the overall ROCM lib/llvm
  # directory.
  INSTALL_DESTINATION "lib/llvm"
  INTERFACE_LINK_DIRS
    "lib/llvm/lib"
)
# Note that we do not trigger on LLVM source changes because the monorepo is
# too large to glob like that. Consider having a project dev mode option for
# enabling better ergonomics here.

therock_cmake_subproject_provide_package(amd-llvm amd_comgr lib/llvm/lib/cmake/amd_comgr)
therock_cmake_subproject_provide_package(amd-llvm Clang lib/llvm/lib/cmake/clang)
therock_cmake_subproject_provide_package(amd-llvm LLD lib/llvm/lib/cmake/lld)
therock_cmake_subproject_provide_package(amd-llvm LLVM lib/llvm/lib/cmake/llvm)
therock_cmake_subproject_provide_package(amd-llvm AMDDeviceLibs lib/llvm/lib/cmake/AMDDeviceLibs)
therock_cmake_subproject_activate(amd-llvm)


#################################################################################
# HIPIFY
#################################################################################

therock_cmake_subproject_declare(hipify
  EXTERNAL_SOURCE_DIR "hipify"
  BACKGROUND_BUILD
  INTERFACE_PROGRAM_DIRS
    bin
  CMAKE_ARGS
    -DHIPIFY_INSTALL_CLANG_HEADERS=OFF
  RUNTIME_DEPS
    amd-llvm
)
therock_cmake_subproject_glob_c_sources(hipify
  SUBDIRS
    src
)
therock_cmake_subproject_activate(hipify)


################################################################################
# Artifacts
################################################################################

therock_provide_artifact(amd-llvm
  TARGET_NEUTRAL
  DESCRIPTOR artifact-amd-llvm.toml
  COMPONENTS
    dbg
    dev
    doc
    lib
    run
  SUBPROJECT_DEPS
    amd-llvm
)

therock_provide_artifact(hipify
  TARGET_NEUTRAL
  DESCRIPTOR artifact-hipify.toml
  COMPONENTS
    run
    dbg
  SUBPROJECT_DEPS
    hipify
)
