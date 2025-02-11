# TheRock

The HIP Environment and ROCm Kit - A lightweight open source build system for HIP and ROCm

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

# Install Deps

## Common

```
pip install CppHeaderParser
```

## On Ubuntu

```
sudo apt install \
  repo git-lfs libnuma-dev ninja-build cmake g++ pkg-config libdrm-dev \
  libelf-dev xxd libgl1-mesa-dev libbz2-dev libsqlite3-dev libgtest-dev

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

Alternatively, for a specific ROCm version e.g. 6.3.0

```
python ./build_tools/fetch_sources.py \
  --manifest-url https://github.com/ROCm/ROCm.git \
  --manifest-name tools/rocm-build/rocm-6.3.1.xml \
  --manifest-branch roc-6.3.x
```

This will also apply the patches to the downloaded source files.

## Manually

Checkout the latest development branch with

```
mkdir -p ~/github/rocm
cd ~/github/rocm
repo init -u https://github.com/ROCm/ROCm.git -m tools/rocm-build/rocm-6.3.1.xml -b roc-6.3.x
repo sync -j16
```

Checkout TheRock build tools

```
cd ~/github/
git clone https://github.com/nod-ai/TheRock
cd TheRock
ln -s </path/to/rocm> sources
```

# Build

Note that you must specify GPU targets or families to build for with either
`-DTHEROCK_AMDGPU_FAMILIES=` or `-DTHEROCK_AMDGPU_TARGETS=` and will get an
error if there is an issue. Supported families and targets are in the
[therock_amdgpu_targets.cmake](cmake/therock_amdgpu_targets.cmake) file. Not
all combinations are presently supported.

```
cmake -B build -GNinja . -DTHEROCK_AMDGPU_FAMILIES=gfx110X-dgpu
# Or if iterating and wishing to cache:
#   cmake -Bbuild -GNinja -DCMAKE_C_COMPILER_LAUNCHER=ccache -DCMAKE_CXX_COMPILER_LAUNCHER=ccache .
cmake --build build
```

## Feature Flags

By default, the project builds everything available. The following group flags
allow enable/disable of selected subsets:

- `-DTHEROCK_ENABLE_ALL=OFF`: Disables all optional components.
- `-DTHEROCK_ENABLE_CORE=OFF`: Disables all core components.
- `-DTHEROCK_ENABLE_COMM_LIBS=OFF`: Disables all communication libraries.
- `-DTHEROCK_ENABLE_MATH_LIBS=OFF`: Disables all math libraries.
- `-DTHEROCK_ENABLE_ML_LIBS=OFF`: Disables all ML libraries.

Individual features can be controlled separately (typically in combination with
`-DTHEROCK_ENABLE_ALL=OFF` or `-DTHEROCK_RESET_FEATURES=ON` to force a
minimal build):

- `-DTHEROCK_ENABLE_COMPILER=ON`: Enables the GPU+host compiler toolchain.
- `-DTHEROCK_ENABLE_HIPIFY=ON`: Enables the hipify tool.
- `-DTHEROCK_ENABLE_CORE_RUNTIME=ON`: Enables the core runtime components and tools.
- `-DTHEROCK_ENABLE_HIP_RUNTIME=ON`: Enables the HIP runtime components.
- `-DTHEROCK_ENABLE_RCCL=ON`: Enables RCCL.
- `-DTHEROCK_ENABLE_PRIM=ON`: Enables the PRIM library.
- `-DTHEROCK_ENABLE_BLAS=ON`: Enables the BLAS libraries.
- `-DTHEROCK_ENABLE_RAND=ON`: Enables the RAND libraries.
- `-DTHEROCK_ENABLE_SOLVER=ON`: Enables the SOLVER libraries.
- `-DTHEROCK_ENABLE_SPARSE=ON`: Enables the SPARSE libraries.
- `-DTHEROCK_ENABLE_MIOPEN=ON`: Enables MIOpen.

Enabling any features will implicitly enable its *minimum* dependencies. Some
libraries (like MIOpen) have a number of *optional* dependencies, which must
be enabled manually if enabling/disabling individual features.

A report of enabled/disabled features and flags will be printed on every
CMake configure.

## Sanity Checks

Tests of the integrity of the build are enabled by default and can be run
with ctest:

```
ctest --test-dir build
```

Testing functionality on an actual GPU is in progress and will be documented
separately.
