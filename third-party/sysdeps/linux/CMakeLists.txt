# All system deps (alpha unless if different dependency order needed).
add_subdirectory(bzip2)
add_subdirectory(libdrm)
add_subdirectory(zlib)
add_subdirectory(zstd)

# System deps that depend on the above.
add_subdirectory(elfutils)

therock_provide_artifact(sysdeps
  TARGET_NEUTRAL
  DESCRIPTOR artifact.toml
  COMPONENTS
    dev
    doc
    lib
    run
  SUBPROJECT_DEPS
    therock-bzip2
    therock-libdrm
    therock-zlib
    therock-zstd
)
