#!/usr/bin/bash
# Temporary script while transitioning to submodules. This was manually
# transcribed from a mainline repo manifest.

unsymlink() {
  dir="$1"
  if [[ -L $dir ]]; then
    echo "Unlinking $1"
    unlink $dir
    git add $dir
  fi
}

add_submodule() {
  name="$1"
  branch="$2"
  path="$3"
  url="$4"
  unsymlink $path
  git submodule add -b "$branch" --name "$name" -- "$url" "$path"
}

add_submodule clr amd-mainline core/clr https://github.com/ROCm/clr
add_submodule half rocm base/half https://github.com/ROCm/half.git
add_submodule HIP amd-mainline core/HIP https://github.com/ROCm/HIP.git
add_submodule HIPIFY amd-mainline compiler/hipify https://github.com/ROCm/HIPIFY.git
add_submodule llvm-project amd-mainline compiler/amd-llvm https://github.com/ROCm/llvm-project.git
add_submodule rccl mainline comm-libs/rccl https://github.com/ROCm/rccl.git
add_submodule rocm_smi_lib amd-mainline base/rocm_smi_lib https://github.com/ROCm/rocm_smi_lib.git
add_submodule rocm-cmake mainline base/rocm-cmake https://github.com/ROCm/rocm-cmake.git
add_submodule rocm-core amd-master base/rocm-core https://github.com/ROCm/rocm-core.git
add_submodule rocminfo amd-master core/rocminfo https://github.com/ROCm/rocminfo.git
add_submodule rocprofiler-register amd-mainline base/rocprofiler-register https://github.com/ROCm/rocprofiler-register.git
add_submodule rocprofiler-sdk amd-mainline profiler/rocprofiler-sdk https://github.com/ROCm/rocprofiler-sdk.git
add_submodule ROCR-Runtime amd-master core/ROCR-Runtime https://github.com/ROCm/ROCR-Runtime.git

# Math libs.
add_submodule hipBLAS-common mainline math-libs/BLAS/hipBLAS-common https://github.com/ROCm/hipBLAS-common.git
add_submodule hipBLAS mainline math-libs/BLAS/hipBLAS https://github.com/ROCm/hipBLAS.git
add_submodule hipBLASLt mainline math-libs/BLAS/hipBLASLt https://github.com/ROCm/hipBLASLt.git
add_submodule hipCUB mainline math-libs/hipCUB https://github.com/ROCm/hipCUB.git
add_submodule hipFFT mainline math-libs/hipFFT https://github.com/ROCm/hipFFT.git
add_submodule hipRAND mainline math-libs/hipRAND https://github.com/ROCm/hipRAND.git
add_submodule hipSOLVER mainline math-libs/BLAS/hipSOLVER https://github.com/ROCm/hipSOLVER.git
add_submodule hipSPARSE mainline math-libs/BLAS/hipSPARSE https://github.com/ROCm/hipSPARSE.git
add_submodule Tensile master math-libs/BLAS/Tensile https://github.com/ROCm/Tensile.git
add_submodule rocBLAS mainline math-libs/BLAS/rocBLAS https://github.com/ROCm/rocBLAS.git
add_submodule rocFFT mainline math-libs/rocFFT https://github.com/ROCm/rocFFT.git
add_submodule rocPRIM mainline math-libs/rocPRIM https://github.com/ROCm/rocPRIM.git
add_submodule rocRAND mainline math-libs/rocRAND https://github.com/ROCm/rocRAND.git
add_submodule rocSOLVER mainline math-libs/BLAS/rocSOLVER https://github.com/ROCm/rocSOLVER.git
add_submodule rocSPARSE mainline math-libs/BLAS/rocSPARSE https://github.com/ROCm/rocSPARSE.git
add_submodule rocThrust mainline math-libs/rocThrust https://github.com/ROCm/rocThrust.git

# ml-libs
add_submodule MIOpen amd-master ml-libs/MIOpen https://github.com/ROCm/MIOpen.git
