#################################################################################
# roctracer
#################################################################################

therock_cmake_subproject_declare(roctracer
  EXTERNAL_SOURCE_DIR "roctracer"
  BACKGROUND_BUILD
  CMAKE_ARGS
    -DHIP_PLATFORM=amd
    -DROCM_PATH=
    -DROCM_DIR=
  COMPILER_TOOLCHAIN
    amd-hip
  BUILD_DEPS
    rocm-cmake
  RUNTIME_DEPS
    hip-clr
)

therock_cmake_subproject_activate(roctracer)
