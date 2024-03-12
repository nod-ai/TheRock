from pathlib import Path
import platform

__all__ = [
    "get_dist_dir",
    "get_library_dir",
    "get_hip_runtime_library",
]


def _get_library_parts() -> tuple[str, str]:
    s = platform.system()
    if s == "Linux":
        return "lib", ".so"
    elif s == "Windows":
        return "", ".dll"
    elif s == "Darwin":
        return "lib", ".dylib"


lib_prefix, lib_suffix = _get_library_parts()


def get_dist_dir() -> str:
    import _therock

    location = _therock.__file__
    assert location, "Could not find physical location for therock runtime"
    return str(Path(location).resolve().parent)


def get_library_dir() -> str:
    return str(Path(get_dist_dir()) / "lib")


def get_hip_runtime_library() -> str:
    return str(Path(get_library_dir()) / f"{lib_prefix}amdhip64{lib_suffix}")
