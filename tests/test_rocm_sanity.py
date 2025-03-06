import pytest
import subprocess
import re
from pathlib import Path

THIS_DIR = Path(__file__).parent


def run_command(command):
    process = subprocess.run(command, capture_output=True, check=False)
    if process.returncode != 0:
        pytest.fail(f"The command {command} failed. Failing this test...")
    return str(process.stdout)


class TestROCmSanity:
    def test_rocminfo(self):
        output = run_command(["rocminfo"])

        pytest.assume(re.search(r"Device\s*Type:\s*GPU", output))
        pytest.assume(re.search(r"Name:\s*gfx", output))
        pytest.assume(re.search(r"Vendor\s*Name:\s*AMD", output))

    def test_clinfo(self):
        output = run_command(["clinfo"])

        pytest.assume(
            re.search(r"Device(\s|\\t)*Type:(\s|\\t)*CL_DEVICE_TYPE_GPU", output)
        )
        pytest.assume(re.search(r"Name:(\s|\\t)*gfx", output))
        pytest.assume(
            re.search(r"Vendor:(\s|\\t)*Advanced Micro Devices, Inc.", output)
        )

    def test_hip_printf(self):
        # Compiling .cpp file using hipcc
        run_command(
            [
                "hipcc",
                f"{str(THIS_DIR)}/hip_printf.cpp",
                "-o",
                f"{str(THIS_DIR)}/hip_printf",
            ]
        )

        # Running the executable
        output = run_command([f"{str(THIS_DIR)}/hip_printf"])
        pytest.assume(re.search(r"Thread.*is\swriting", output))
