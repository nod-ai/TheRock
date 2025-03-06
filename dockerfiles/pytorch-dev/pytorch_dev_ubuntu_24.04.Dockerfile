# Multi-stage build which builds rocm, then pytorch, and finally produces
# a docker image with the built pytorch installed.
# Build with:
#   docker buildx build --file dockerfiles/pytorch-dev/pytorch_dev_ubuntu_24.04.Dockerfile .
FROM ubuntu:24.04 AS build_rocm
WORKDIR /
RUN apt update && apt install -y \
  python3 python3-pip python3-pip-whl \
  gfortran git-lfs ninja-build cmake g++ pkg-config \
  xxd libgtest-dev patchelf automake
# TODO: Remove once https://github.com/ROCm/TheRock/issues/160 is resolved.
RUN apt install -y opengl-dev
# TODO: Remove once https://github.com/ROCm/TheRock/issues/161 is resolved.
RUN apt install -y python3-venv

RUN python3 -m pip install --break-system-packages \
  CppHeaderParser==2.7.4 meson==1.7.0
COPY dockerfiles/pytorch-dev/build_rocm.sh /
# TODO: The ROCM components still output some things to the source dir. Remove
# "rw" when fixed. See https://github.com/ROCm/TheRock/issues/159
RUN --mount=type=bind,target=/therock/src,rw bash /build_rocm.sh
