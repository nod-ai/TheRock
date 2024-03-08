#include <dlfcn.h>
#include <stdio.h>

int main(int argc, char **argv) {
  if (argc != 2) {
    printf("Syntax error: Expected library path\n");
    return 1;
  }
  char *lib_path = argv[1];
  int rc;
  void *h = dlopen(lib_path, RTLD_NOW);
  int(*hipRuntimeGetVersion)(int*) = (int(*)(int*))dlsym(h, "hipRuntimeGetVersion");
  if (!hipRuntimeGetVersion) {
    printf("ERROR: Could not resolve symbol hipRuntimeGetVersion\n");
    return 1;
  }
  int version = -1;
  rc = hipRuntimeGetVersion(&version);
  if (rc != 0) {
    fprintf("ERROR: hipRuntimeGetVersion returned %d\n", rc);
    return 2;
  }
  printf("HIP VERSION: %x\n", version);

  rc = dlclose(h);
  if (rc != 0) {
    printf("ERROR: dlclose(): %d\n", rc);
    return 3;
  }
  return 0;
}
