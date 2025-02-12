# This dockerfile builds automatically upon push to the main branch. It can be built
# interactively for testing via:
#   docker buildx build --file dockerfiles/build_manylinux_x86_64.Dockerfile dockerfiles
# This will print a SHA image id, which you can run with (or equiv):
#   sudo docker run --rm -it --entrypoint /bin/bash <<IMAGE>>
#
# To build and push to a test branch, create a pull request on a branch named:
#   docker*
# We build our portable linux releases on the manylinux (RHEL-based)
# images, with custom additional packages installed. We switch to
# new upstream versions as needed.
FROM quay.io/pypa/manylinux_2_28_x86_64@sha256:9042a22d33af2223ff7a3599f236aff1e4ffd07e1ed1ac93a58877638317515f

######## Python setup #######
# These images come with multiple python versions. We pin one for
# default use.
ENV PATH="/opt/python/cp312-cp312/bin:${PATH}"

######## Pip Packages ########
RUN pip install CppHeaderParser

######## Repo ########
RUN curl https://storage.googleapis.com/git-repo-downloads/repo > /usr/local/bin/repo && chmod a+x /usr/local/bin/repo

######## CCache ########
WORKDIR /install-ccache
COPY install_ccache.sh ./
RUN ./install_ccache.sh "4.9" && rm -rf /install-ccache

######## CMake ########
WORKDIR /install-cmake
ENV CMAKE_VERSION="3.25.2"
COPY install_cmake.sh ./
RUN ./install_cmake.sh "${CMAKE_VERSION}" && rm -rf /install-cmake

######## Ninja ########
WORKDIR /install-ninja
ENV CMAKE_VERSION="1.12.1"
COPY install_ninja.sh ./
RUN ./install_ninja.sh "${CMAKE_VERSION}" && rm -rf /install-ninja

######## Yum Packages #######
# TODOs:
#   * Figure out why having openblas-devel installed makes the fortran compiler
#     behave (https://github.com/nod-ai/TheRock/issues/82)
RUN yum install -y epel-release && \
    yum install -y clang lld && \
    yum install -y numactl-devel elfutils-libelf-devel vim-common git-lfs && \
    yum install -y bzip2-devel && \
    yum install -y gtest-devel && \
    yum install -y openblas-devel && \
    yum clean all && \
    rm -rf /var/cache/yum

######## GIT CONFIGURATION ########
# Git started enforcing strict user checking, which thwarts version
# configuration scripts in a docker image where the tree was checked
# out by the host and mapped in. Disable the check.
# See: https://github.com/openxla/iree/issues/12046
# We use the wildcard option to disable the checks. This was added
# in git 2.35.3
RUN git config --global --add safe.directory '*'
