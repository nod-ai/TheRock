import pytest
import subprocess
import re
from pathlib import Path
from pytest_check import check

THIS_DIR = Path(__file__).resolve().parent

def run_command(command):
    process = subprocess.run(command, capture_output=True, check=False)
    if process.returncode != 0:
        pytest.fail(f"The command {command} failed. Failing this test...")
    return str(process.stdout)

@pytest.fixture(scope = "session")
def rocm_info_output():
    return run_command(["rocminfo"])

@pytest.fixture(scope = "session")
def clinfo_info_output():
    return run_command(["clinfo"])

class TestROCmSanity:
        
    @pytest.mark.parametrize(
        "to_search",
        [
            (r"Device\s*Type:\s*GPU"),
            (r"Name:\s*gfx"),
            (r"Vendor\s*Name:\s*AMD"),
        ],
        ids=[
            "rocminfo - GPU Device Type Search",
            "rocminfo - GFX Name Search",
            "rocminfo - AMD Vendor Name Search"
        ],
    )
    def test_rocm_output(self, rocm_info_output, to_search):        
        check.is_not_none(re.search(to_search, rocm_info_output))
        
        
    @pytest.mark.parametrize(
        "to_search",
        [
            (r"Device(\s|\\t)*Type:(\s|\\t)*CL_DEVICE_TYPE_GPU"),
            (r"Name:(\s|\\t)*gfx"),
            (r"Vendor:(\s|\\t)*Advanced Micro Devices, Inc."),
        ],
        ids=[
            "clinfo - GPU Device Type Search",
            "clinfo - GFX Name Search",
            "clinfo - AMD Vendor Name Search"
        ],
    )
    def test_clinfo_output(self, clinfo_info_output, to_search):        
        check.is_not_none(re.search(to_search, clinfo_info_output))
        

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
        check.is_not_none(re.search(r"Thread.*is\swriting", output))
