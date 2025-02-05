# TODO: hipSOLVER includes <suitesparse/cholmod.h> but the include directory
# specified via `-I` already points to the subdirectory. Needs a fix.
include_directories("${THEROCK_BINARY_DIR}/third-party/SuiteSparse/stage/include")
