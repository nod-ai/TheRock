add_custom_target(therock-third-party)

# No-dep third party libraries (alphabetical)
add_subdirectory(boost)
add_subdirectory(eigen)
add_subdirectory(fmt)
add_subdirectory(msgpack-cxx)
add_subdirectory(nlohmann-json)
add_subdirectory(FunctionalPlus)
add_subdirectory(SuiteSparse)

# frugally-deep depends on eigen, FunctionalPlus and nlohmann-json
add_subdirectory(frugally-deep)
