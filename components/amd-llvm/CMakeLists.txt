cmake_minimum_required(VERSION 3.18)
project(THEROCK-AMD-LLVM)

# Build LLVM and the comgr dependency.
# Note that in LLVM "BUILD_SHARED_LIBS" enables an unsupported development mode.
# The flag you want for a shared library build is LLVM_BUILD_LLVM_DYLIB.
set(BUILD_SHARED_LIBS OFF)
set(LLVM_BUILD_LLVM_DYLIB ON)
# TODO: Depending on what is getting released, it may or may not be paying
# for itself to dynamically link.
set(LLVM_LINK_LLVM_DYLIB OFF)
set(LLVM_DIR "${ROCM_GIT_DIR}/llvm-project")
message(STATUS "LLVM_DIR is set to: ${LLVM_DIR}")

# Set the LLVM_ENABLE_PROJECTS variable before including LLVM's CMakeLists.txt
set(BUILD_TESTING OFF CACHE BOOL "DISABLE BUILDING TESTS IN SUBPROJECTS" FORCE)
set(LLVM_ENABLE_PROJECTS "compiler-rt;lld;clang" CACHE STRING "Enable LLVM projects" FORCE)
set(LLVM_TARGETS_TO_BUILD "AMDGPU;X86" CACHE STRING "Enable LLVM Targets" FORCE)
set(LLVM_EXTERNAL_DEVICE_LIBS_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/device-libs" CACHE STRING "Device libs path" FORCE)
set(LLVM_EXTERNAL_PROJECTS "amddevice-libs;amdcomgr" CACHE STRING "Enable extra projects" FORCE)
set(LLVM_EXTERNAL_AMDCOMGR_SOURCE_DIR "${LLVM_DIR}/amd/comgr")
set(LLVM_EXTERNAL_AMDDEVICE_LIBS_SOURCE_DIR "${ROCM_GIT_DIR}/llvm-project/amd/device-libs")
#set(ROCM_DEVICE_LIBS_BITCODE_INSTALL_LOC_NEW "llvm/amdgcn-new")
# hipcc expects bit codes under amdgcn.
#set(ROCM_DEVICE_LIBS_BITCODE_INSTALL_LOC_OLD "amdgcn")

# Now include LLVM's source directory
add_subdirectory(${LLVM_DIR}/llvm ${CMAKE_BINARY_DIR}/llvm)

# add_custom_target(
#    amd-bitcodes-symlink ALL
#    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
#    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_INSTALL_PREFIX}/..
#    COMMAND ${CMAKE_COMMAND} -E create_symlink amdgcn ${CMAKE_INSTALL_PREFIX}/../amdgcn
# )
install(CODE "execute_process( \
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_INSTALL_PREFIX}/.. \
    COMMAND ${CMAKE_COMMAND} -E create_symlink llvm/amdgcn ${CMAKE_INSTALL_PREFIX}/../amdgcn \
    COMMAND_ERROR_IS_FATAL ANY \
    )"
)
