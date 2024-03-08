# TheRock
The HIP Environment and ROCm Kit - A lightweight open source build system for HIP and ROCm

# Install Deps

On Ubuntu

```
sudo apt install \
  repo git-lfs libnuma-dev ninja-build cmake g++ pkg-config libdrm-dev \
  libelf-dev
```

# Checkout Sources

We want ROCm sources checked out into the sources/ directory or if you check it out elsewhere create a symlink called `ln -s /path/to/rocm sources`

## Via script

```
./fetch_sources.sh
```

## Manually

Checkout the latest development branch with
```
mkdir ~/github/rocm
cd ~/github/rocm
repo init -u https://github.com/RadeonOpenCompute/ROCm.git
repo sync -j16
```
Use `-b roc-6.0.x` if you need a specific branch of ROCm sources.  

Checkout out latest LLVM sources

```
cd ~/github/rocm/llvm-project
git fetch --all
llvm-project$ git checkout rocm-org/amd-staging
```
Latest `HIP` and `clr` should be on the `develop` branch

Checkout TheRock build tools
```
cd ~/github/
git clone https://github.com/nod-ai/TheRock
cd TheRock
ln -s </path/to/rocm> sources
```

## Applying hacks/patches

Here are current patch topics that we are maintaining.

```
./apply_patches.sh
```

## Build

```
cmake -B build -GNinja .
# Or if iterating and wishing to cache:
#   cmake -Bbuild -GNinja -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache .
cmake --build build
```

## Sanity Checks

The following does not replace a robust test suite. However, it will tell you
whether the toolchain you have just crafted is viable at all (as in can load
and enumerate devices).

```
./build/dlopen-hip install/lib/libamdhip64.so
```

HIP enabled IREE can also be used to enumerate:

```
LD_LIBRARY_PATH=install/lib iree-run-module --dump_devices=hip
```
