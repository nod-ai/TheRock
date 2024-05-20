# TheRock
The HIP Environment and ROCm Kit - A lightweight open source build system for HIP and ROCm

# Install Deps

## Common
```
pip install CppHeaderParser
```

## On Ubuntu

```
sudo apt install \
  repo git-lfs libnuma-dev ninja-build cmake g++ pkg-config libdrm-dev \
  libelf-dev xxd libgl1-mesa-dev
```

# Checkout Sources

We want ROCm sources checked out into the sources/ directory or if you check it out elsewhere create a symlink called `ln -s /path/to/rocm sources`

## Via script

```
python ./build_tools/fetch_sources.py
```

This will use the [repo](https://source.android.com/docs/setup/reference/repo)
tool with modified ROCm [manifest](https://github.com/nod-ai/ROCm/blob/the-rock-main/default.xml).
It will also apply patches to some of the repositories.

Alternatively, for a specific ROCm version e.g. 6.1.0

```
python ./build_tools/fetch_sources.py \
  --manifest-url https://github.com/ROCm/ROCm.git \
  --manifest-branch refs/tags/rocm-6.1.0
```

This will also apply the patches to the downloaded source files.

## Manually

Checkout the latest development branch with
```
mkdir ~/github/rocm
cd ~/github/rocm
repo init -u https://github.com/ROCm/ROCm.git
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

# Build

```
cmake -B build -GNinja .
# Or if iterating and wishing to cache:
#   cmake -Bbuild -GNinja -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache .
cmake --build build

# Install per component.
cmake --install build --component amdgpu-runtime
cmake --install build --component amdgpu-runtime-dev
cmake --install build --component amdgpu-compiler

# Create archives.
(cd build && cpack -G TBZ2)
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

# Development Notes

## Building in a manylinux container

Our CI builds run in such a container, and it can be useful to run locally.

```
docker run --rm -it -v $PWD:$PWD --entrypoint /bin/bash ghcr.io/nod-ai/manylinux_ghr_x86_64:main
```

Packages needed:

```
yum install -y numactl-devel elfutils-libelf-devel vim-common git-lfs
pip install CppHeaderParser
```
