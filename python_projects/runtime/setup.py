from pathlib import Path
import os
import subprocess
import sys

from distutils.command.build import build as _build
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext as _build_ext
from setuptools.command.build_py import build_py as _build_py

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            # this is a universal, but platform-specific package; a combination
            # that wheel does not recognize, thus simply fool it
            from distutils.util import get_platform

            self.plat_name = get_platform()
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = True

except ImportError:
    bdist_wheel = None


VERSION = os.getenv("THEROCK_PY_VERSION", None)
SUFFIX = os.getenv("THEROCK_PY_SUFFIX", "")
if not VERSION:
    VERSION = "0.1.dev1"
SETUPPY_DIR = Path(__file__).resolve().parent
SOURCE_DIR = SETUPPY_DIR.parent.parent
# Note that setuptools always builds into a "build" directory that
# is a sibling of setup.py, so we just colonize a sub-directory of that
# by default.
CMAKE_BUILD_DIR = Path(os.getenv(
    "THEROCK_CMAKE_BUILD_DIR", SETUPPY_DIR / "build" / "cmake-build"
))
CMAKE_INSTALL_DIR = Path(os.getenv(
    "THEROCK_CMAKE_INSTALL_DIR", SETUPPY_DIR / "build" / "dist-install"
))

with open(SETUPPY_DIR / "README.md", "rt") as f:
    README = f.read()


def getenv_bool(key, default_value="OFF"):
    value = os.getenv(key, default_value)
    return value.upper() in ["ON", "1", "TRUE"]


class CMakeBuilder:
    def run(self):
        print("*****************************", file=sys.stderr)
        print("* Building base runtime     *", file=sys.stderr)
        print("*****************************", file=sys.stderr)
        if not getenv_bool("THEROCK_PY_SKIP_CMAKE"):
            self.cmake_build()
        else:
            print("Skipping CMake build because THEROCK_PY_SKIP_CMAKE is set")
        self.cmake_install()

    def cmake_build(self):
        subprocess.check_call(["cmake", "--version"])
        install_dir = CMAKE_INSTALL_DIR
        cmake_args = [
            f"-S{SOURCE_DIR}",
            f"-B{CMAKE_BUILD_DIR}",
            "-GNinja",
            "--log-level=VERBOSE",
            f"-DCMAKE_BUILD_TYPE=Release",
            f"-DCMAKE_INSTALL_PREFIX={str(install_dir)}",
            # Versioned SONAMEs get duplicated in Python wheels. And this use
            # case is really aimed at dynamically loading of a hermetic runtime
            # library.
            "-DCMAKE_PLATFORM_NO_VERSIONED_SONAME=ON",
            # TODO: Also enable visibility=hidden preset and other distribution
            # armor.
        ]
        subprocess.check_call(["cmake"] + cmake_args, cwd=SOURCE_DIR)
        subprocess.check_call(
            ["cmake", "--build", CMAKE_BUILD_DIR], cwd=CMAKE_BUILD_DIR
        )

    def cmake_install(self):
        with open(CMAKE_INSTALL_DIR / "version.py", "wt") as f:
            f.write(f"py_version = '{VERSION}'\n")
            # TODO: Add ROCM version, etc
        for component in ["amdgpu-runtime"]:
            subprocess.check_call(
                ["cmake", "--install", CMAKE_BUILD_DIR, "--component", component],
                cwd=CMAKE_BUILD_DIR,
            )


packages = find_packages(where=".")
print("Found packages:", packages)

CMAKE_INSTALL_DIR.mkdir(parents=True, exist_ok=True)
(CMAKE_INSTALL_DIR / "__init__.py").touch()
CMAKE_BUILD_DIR.mkdir(parents=True, exist_ok=True)
# In order to reliably package the built files, it is best to run the build
# prior to setup. All built artifacts go into the _therock top level
# package so that source and built trees are distinct.
CMakeBuilder().run()

package_name = "TheRock-runtime"
if SUFFIX:
    package_name += f"-{SUFFIX}"

setup(
    name=package_name,
    version=f"{VERSION}",  # TODO: Get from env var.
    author="TheRock Authors",
    author_email="stdin@nod.ai",
    description="Minimal ROCM runtime components",
    long_description=README,
    long_description_content_type="text/markdown",
    license="Apache-2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    url="https://github.com/nod-ai/TheRock",
    python_requires=">=3.6",
    cmdclass={
        "bdist_wheel": bdist_wheel,
    },
    zip_safe=False,
    packages=["therock", "_therock"],
    package_dir={
        "": ".",
        "_therock": "build/dist-install",
    },
    # Matching the native extension as a data file keeps setuptools from
    # "building" it (i.e. turning it into a static binary).
    package_data={
        "_therock": [
            "**/*",
        ],
    },
    entry_points={},
    install_requires=[],
)
