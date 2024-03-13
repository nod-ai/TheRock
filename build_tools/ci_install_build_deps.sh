#!/bin/bash

curl https://storage.googleapis.com/git-repo-downloads/repo > /usr/local/bin/repo
chmod a+x /usr/local/bin/repo
yum install -y numactl-devel elfutils-libelf-devel vim-common git-lfs
pip install CppHeaderParser
