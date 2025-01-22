# Build LLVM and the comgr dependency.
# Note that in LLVM "BUILD_SHARED_LIBS" enables an unsupported development mode.
# The flag you want for a shared library build is LLVM_BUILD_LLVM_DYLIB.
set(BUILD_SHARED_LIBS OFF)
set(LLVM_BUILD_LLVM_DYLIB ON)
set(LLVM_LINK_LLVM_DYLIB ON)

# Set the LLVM_ENABLE_PROJECTS variable before including LLVM's CMakeLists.txt
set(BUILD_TESTING OFF CACHE BOOL "DISABLE BUILDING TESTS IN SUBPROJECTS" FORCE)
set(LLVM_ENABLE_PROJECTS "compiler-rt;lld;clang" CACHE STRING "Enable LLVM projects" FORCE)
set(LLVM_TARGETS_TO_BUILD "AMDGPU;X86" CACHE STRING "Enable LLVM Targets" FORCE)
set(LLVM_EXTERNAL_DEVICE_LIBS_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/device-libs" CACHE STRING "Device libs path" FORCE)
set(LLVM_EXTERNAL_PROJECTS "amddevice-libs;amdcomgr;hipcc" CACHE STRING "Enable extra projects" FORCE)
set(LLVM_EXTERNAL_AMDDEVICE_LIBS_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/device-libs")
set(LLVM_EXTERNAL_AMDCOMGR_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/comgr")
set(LLVM_EXTERNAL_HIPCC_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/hipcc")

#set(ROCM_DEVICE_LIBS_BITCODE_INSTALL_LOC_NEW "llvm/amdgcn-new")
# hipcc expects bit codes under amdgcn.
#set(ROCM_DEVICE_LIBS_BITCODE_INSTALL_LOC_OLD "amdgcn")

# add_custom_target(
#    amd-bitcodes-symlink ALL
#    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
#    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_INSTALL_PREFIX}/..
#    COMMAND ${CMAKE_COMMAND} -E create_symlink amdgcn ${CMAKE_INSTALL_PREFIX}/../amdgcn
# )
# install(CODE "execute_process( \
#     COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_INSTALL_PREFIX}/.. \
#     COMMAND ${CMAKE_COMMAND} -E create_symlink llvm/amdgcn ${CMAKE_INSTALL_PREFIX}/../amdgcn \
#     COMMAND_ERROR_IS_FATAL ANY \
#     )"
# )
