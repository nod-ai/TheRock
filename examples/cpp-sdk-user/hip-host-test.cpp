#include <hip/hip_runtime_api.h>

#include <iostream>

int main(int argc, char **argv) {
  int runtime_version;
  auto err = hipRuntimeGetVersion(&runtime_version);
  if (err != hipSuccess) {
    std::cerr << "Error getting runtime version: " << err << "\n";
    return 2;
  }
  std::cout << "HIP runtime version: " << runtime_version << "\n";
  err = hipInit(0);
  if (err != hipSuccess) {
    // Since this is primarily run on CI to verify that linkage works, we
    // just ignore any error (this lets us run the test on machines that
    // lack a GPU).
    std::cerr << "Error initializing HIP: " << err << " (ignored)\n";
  }
  return 0;
}
