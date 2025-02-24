# Portable Linux Packaging

Build scripts for producing ready to run manylinux based bundles that feed into a variety of distribution packages.

These are all based on our `build_manylinux` docker containers (see `/dockerfiles/build_manylinux_x86_64.Dockerfile` and the corresponding packages in the registry). Such builds are generally compatible with any glibc based Linux distribution that is greater than or equal to that which was used to build. See the [manylinux](https://github.com/pypa/manylinux) project for more information.

## Invocation

Build with defaults:

```shell
python build_portable.py -- -DTHEROCK_AMDGPU_FAMILIES=gfx110X-dgpu
```

Build using podman instead of docker (preserves host permissions and does not
run as root):

```shell
python build_portable.py --docker=podman -- -DTHEROCK_AMDGPU_FAMILIES=gfx110X-dgpu
```

Drop into an interactive shell with podman:
```shell
python build_portable.py --docker=podman --interactive
```
