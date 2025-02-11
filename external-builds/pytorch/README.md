# Build ROCM PyTorch

There is nothing special about this build procedure except that it is meant
to run as part of the ROCM CI and development flow and leaves less room for
interpretation with respect to golden path in upstream docs.

This incorporates advice from:

- https://github.com/pytorch/pytorch#from-source
- `.ci/manywheel/build_rocm.sh` and friends

Note that the above statement is currently aspirational as we contain some
overlay files and/or patches locally until they can be upstreamed. See the
`overlay` directory.

## Step 0: Prep venv

It is highly recommended to use a virtual environment unless if in a throw-away
container/CI environment.

```
python -m venv .venv
source .venv/bin/activate
```

## Step 1: Preparing sources

PyTorch on ROCM relies on pre-processing the sources. In order to avoid dirtying
the git repository (which will also dirty some submodules and makes a big mess),
we duplicate the tree and then make modifications on that:

```
# Checks out to the src/ dir in this directory
./ptbuild import --git-dir /path/to/pytorch/checkout
```

## Step 2: Install Deps

Python deps:

```
pip install -r src/requirements.txt
pip install mkl-static mkl-include
```

## Step 3: Setup and Build

```
export CMAKE_PREFIX_PATH="$(realpath ../../build/dist/rocm)"
(cd src && python setup.py build --cmake-only)
```
