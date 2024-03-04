# TheRock
The HIP Environment and ROCm Kit - A lightweight open source build system for HIP and ROCm

# Install Deps

On Ubuntu

```
sudo apt install repo git-lfs libnuma-dev ninja-build cmake g++ pkg-config libdrm-dev
```

# Checkout Sources

Checkout the latest development branch with
```
mkdir ~/github/rocm
cd ~/github/rocm
repo init -u https://github.com/RadeonOpenCompute/ROCm.git
repo sync -j16
```
Use `-b roc-6.0.x` if you need a specific branch of ROCm sources.  

Checkout out LLVM 6.1 sources

```
cd cd ~/github/rocm/llvm-project
llvm-project$ git checkout rocm-org/amd-staging
```

Checkout TheRock build tools
```
cd ~/github/
git clone https://github.com/nod-ai/TheRock
```

Build

```
cmake -B build -GNinja .
cmake --build build
```
