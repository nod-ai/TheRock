if(WIN32)
  set(LLVM_LINK_LLVM_DYLIB OFF)
else()
  set(LLVM_LINK_LLVM_DYLIB ON)
endif()

# The comgr tests have a circular dependency on the HIP runtime.
# https://github.com/nod-ai/TheRock/issues/67
set(BUILD_TESTING OFF CACHE BOOL "DISABLE BUILDING TESTS IN SUBPROJECTS" FORCE)

set(CMAKE_INSTALL_RPATH "$ORIGIN;$ORIGIN/llvm/lib;$ORIGIN/rocm_sysdeps/lib")
