#include <hip/hip_runtime_api.h>

#include <iostream>

int main(int argc, char **argv) {
  int runtime_version;
  auto err = hipInit(0);
  if (err != hipSuccess) {
    std::cerr << "Error initializing HIP: " << err << "\n";
    return 1;
  }
  err = hipRuntimeGetVersion(&runtime_version);
  if (err != hipSuccess) {
    std::cerr << "Error getting runtime version: " << err << "\n";
    return 2;
  }
  std::cout << "HIP runtime version: " << runtime_version << "\n";
  return 0;
}
