import ctypes
from pathlib import Path
import unittest

import therock


class TestVersion(unittest.TestCase):
    def testVersion(self):
        import _therock.version as v

        py_version = v.py_version
        print("Found py_version =", py_version)
        self.assertTrue(py_version)


class TestLocations(unittest.TestCase):
    def testLibDir(self):
        lib_dir = therock.get_library_dir()
        print(lib_dir)
        self.assertTrue(Path(lib_dir).is_dir(), msg=lib_dir)

    def testHipRuntimeLibrary(self):
        rtl = Path(therock.get_hip_runtime_library())
        self.assertTrue(rtl.is_file, msg=rtl)


class TestLoadRuntimeLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dylib = ctypes.CDLL(therock.get_hip_runtime_library())
        cls.dylib.hipRuntimeGetVersion.restype = ctypes.c_int
        cls.dylib.hipRuntimeGetVersion.argtypes = [ctypes.POINTER(ctypes.c_int)]
        cls.dylib.hipDriverGetVersion.restype = ctypes.c_int
        cls.dylib.hipDriverGetVersion.argtypes = [ctypes.POINTER(ctypes.c_int)]

    def testRuntimeVersion(self):
        v = ctypes.c_int()
        rc = self.dylib.hipRuntimeGetVersion(v)
        print("RuntimeVersion =", v.value)
        self.assertEqual(rc, 0)
        self.assertGreaterEqual(v.value, 60000000)

    def testDriverVersion(self):
        v = ctypes.c_int()
        rc = self.dylib.hipDriverGetVersion(v)
        print("DriverVersion =", v.value)
        self.assertEqual(rc, 0)
        self.assertGreaterEqual(v.value, 60000000)


if __name__ == "__main__":
    unittest.main()
