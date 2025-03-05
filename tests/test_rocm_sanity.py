import pytest
import subprocess
import re

def run_command_with_search(command, to_search):
    process = subprocess.run(command, capture_output=True, check=False)
    if process.returncode != 0:
        pytest.fail(f"The command {command} failed. Failing this test...")
    return re.search(to_search, str(process.stdout))


class TestROCmSanity:
    def test_rocminfo(self):
        assert run_command_with_search(["rocminfo"], r"Device\s*Type:\s*GPU")
        
        assert run_command_with_search(["rocminfo"], r"Name:\s*gfx")
        
        assert run_command_with_search(["rocminfo"], r"Vendor\s*Name:\s*AMD")

    def test_clinfo(self):
        assert run_command_with_search(["clinfo"], r"Device(\s|\\t)*Type:(\s|\\t)*CL_DEVICE_TYPE_GPU")
        
        assert run_command_with_search(["clinfo"], r"Name:(\s|\\t)*gfx")
        
        assert run_command_with_search(["clinfo"], r"Vendor:(\s|\\t)*Advanced Micro Devices, Inc.")
        
