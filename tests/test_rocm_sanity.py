import pytest
import subprocess
import re
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent


def run_command(command):
    process = subprocess.run(command, capture_output=True, check=False)
    if process.returncode != 0:
        pytest.fail(f"The command {command} failed. Failing this test...")
    return str(process.stdout)


rocm_info_output = run_command(["rocminfo"])
cli_info_output = run_command(["clinfo"])


class TestROCmSanity:
    @pytest.mark.parametrize(
        "to_search, output",
        [
            (r"Device\s*Type:\s*GPU", rocm_info_output),
            (r"Name:\s*gfx", rocm_info_output),
            (r"Vendor\s*Name:\s*AMD", rocm_info_output),
            (r"Device(\s|\\t)*Type:(\s|\\t)*CL_DEVICE_TYPE_GPU", cli_info_output),
            (r"Name:(\s|\\t)*gfx", cli_info_output),
            (r"Vendor:(\s|\\t)*Advanced Micro Devices, Inc.", cli_info_output),
        ],
        ids=[
            "rocminfo - GPU Device Type Search",
            "rocminfo - GFX Name Search",
            "rocminfo - AMD Vendor Name Search",
            "clinfo - GPU Device Type Search",
            "clinfo - GFX Name Search",
            "clinfo - AMD Vendor Name Search",
        ],
    )
    def test_info_output(self, to_search, output):
        pytest.assume(re.search(to_search, output))

    def test_hip_printf(self):
        # Compiling .cpp file using hipcc
        run_command(
            [
                "hipcc",
                str(THIS_DIR / "hip_printf.cpp"),
                "-o",
                str(THIS_DIR / "hip_printf"),
            ]
        )

        # Running the executable
        output = run_command([str(THIS_DIR / "hip_printf")])
        pytest.assume(re.search(r"Thread.*is\swriting", output))
