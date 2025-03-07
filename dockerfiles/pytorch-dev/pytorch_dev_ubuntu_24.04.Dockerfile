# Multi-stage build which builds rocm, then pytorch, and finally produces
# a docker image with the built pytorch installed.
# Build with:
#   docker buildx --build-arg AMDGPU_TARGETS=gfx1100 \
#     --file dockerfiles/pytorch-dev/pytorch_dev_ubuntu_24.04.Dockerfile .
FROM ubuntu:24.04 AS build_rocm
ARG AMDGPU_TARGETS
WORKDIR /
RUN apt update && apt install -y \
  python3 python3-pip python3-pip-whl \
  gfortran git-lfs ninja-build cmake g++ pkg-config \
  xxd libgtest-dev patchelf automake
# TODO: Remove once https://github.com/ROCm/TheRock/issues/160 is resolved.
RUN apt install -y libgl-dev
# TODO: Remove once https://github.com/ROCm/TheRock/issues/161 is resolved.
RUN apt install -y python3-venv

RUN python3 -m pip install --break-system-packages \
  CppHeaderParser==2.7.4 meson==1.7.0
COPY dockerfiles/pytorch-dev/build_rocm.sh /
# TODO: The ROCM components still output some things to the source dir. Remove
# "rw" when fixed. See https://github.com/ROCm/TheRock/issues/159
RUN --mount=type=bind,target=/therock/src,rw bash /build_rocm.sh "$AMDGPU_TARGETS"


################################################################################
# PyTorch sources
################################################################################

FROM ubuntu:24.04 AS pytorch_sources
WORKDIR /

RUN apt update && apt install -y \
  python3 python3-pip python3-pip-whl python3-venv git \
  ninja-build cmake g++ pkg-config && \
  apt clean

RUN git config --global user.email "you@example.com" && \
    git config --global user.name "Your Name"

# Prepare PyTorch sources. We do this in two steps so that we get an image
# checkpoint with clean sources first (faster iteration).
RUN --mount=type=bind,target=/therock/src \
  python3 /therock/src/external-builds/pytorch/ptbuild.py checkout \
    --repo /therock/pytorch --depth 1 --jobs 10 --no-patch --no-hipify
RUN --mount=type=bind,target=/therock/src \
  python3 /therock/src/external-builds/pytorch/ptbuild.py checkout \
    --repo /therock/pytorch --depth 1 --jobs 10

# Copy ROCM
COPY --from=build_rocm /therock/build/dist/rocm /opt/rocm

# Setup environment.
ENV PATH="/opt/rocm/bin:$PATH"
RUN (echo "/opt/rocm/lib" > /etc/ld.so.conf.d/rocm.conf) && \
    (echo "/opt/rocm/lib/rocm_sysdeps/lib" >> /etc/ld.so.conf.d/rocm.conf) && \
    ldconfig -v


################################################################################
# PyTorch Build
################################################################################

FROM pytorch_sources AS pytorch_build
ARG AMDGPU_TARGETS

RUN python3 -m pip install --break-system-packages -r /therock/pytorch/requirements.txt

ENV CMAKE_PREFIX_PATH=/opt/rocm
ENV USE_KINETO=OFF
ENV PYTORCH_ROCM_ARCH=$AMDGPU_TARGETS

WORKDIR /therock/pytorch
# TODO: PYTORCH_ROCM_ARCH from environment variables seems broken. So we
# configure it manually for now.
RUN python3 setup.py build --cmake-only
RUN (cd build && cmake "-DPYTORCH_ROCM_ARCH=$AMDGPU_TARGETS" .)
RUN python3 setup.py bdist_wheel

################################################################################
# PyTorch Install
################################################################################

FROM ubuntu:24.04 AS pytorch

RUN apt update && apt install -y \
  python3 python3-pip python3-pip-whl python3-venv python3-numpy

# Copy ROCM
COPY --from=build_rocm /therock/build/dist/rocm /opt/rocm

# Setup environment.
ENV PATH="/opt/rocm/bin:$PATH"
RUN (echo "/opt/rocm/lib" > /etc/ld.so.conf.d/rocm.conf) && \
    (echo "/opt/rocm/lib/rocm_sysdeps/lib" >> /etc/ld.so.conf.d/rocm.conf) && \
    ldconfig -v

# Install pytorch.
# TODO: It would be better to bind mount the prior stage somehow to avoid
# leaving the wheel behind in a layer and wasting a half gig.
COPY --from=pytorch_build /therock/pytorch/dist/torch-*.whl /wheels/
RUN ls /wheels/
RUN python3 -m pip install --break-system-packages \
    $(find /wheels -name '*.whl') && \
    rm -Rf /wheels
