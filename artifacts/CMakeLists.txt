# ROCm Dist Artifacts
# A primary output of the build system is a set of archive slices of key
# components. In typical CI flows, these are archived into tarballs and made
# available to successor jobs as artifacts. Successor jobs can use them for
# a variety of things:
#
#   - Bootstrapping multi-stage builds with pre-built components.
#   - Driving successor platform/channel specific packaging flows (i.e. generate
#     debs, rpms, wheels, etc).
#   - Direct inputs to standalone build jobs.
#   - Distribution of flat archives to users who benefit from this.
#
# Generally, each artifact is an extract of the top level build tree, containing
# a subset of leaf project stage/ directories. In this way, simply extracting
# the artifacts over a build directory is sufficient in successor jobs to
# make that slice of projects be "pre-built". In this way, a monolithic build
# can be broken down and parallelized at sub-project granularity if desired.
#
# Naming Convention
# -----------------
# {slice}_{dist_bundle_name}_{component}_{variant}.tar.xz
#
#   - {slice}: For single sub-project slices, this is just the sub-project name
#     as known to TheRock (e.g. amd-llvm, hipify, hipBLASLt, etc). For multi
#     project slices, it is something descriptive and non-overlapping (e.g.
#     "base").
#   - {dist_bundle_name}: For slices that are AMDGPU target specific, this is
#     the value of -DTHEROCK_AMDGPU_DIST_BUNDLE_NAME, which by default is
#     derived from the gfx name (e.g. "gfx1100") for single target slices or
#     the family name for multi-target slices (e.g. "gfx103X-igpu"). See
#     therock_amdgpu_targets.cmake for derivations. The specific set of built
#     target and family slices is defined by the relevant CI setup (e.g. the
#     presubmit/smoketest pipeline may build a small multi-arch family for
#     basic validation, whereas the full test/postsubmit pipeline may build
#     families in parallel that cover all supported targets for nightly
#     channels, etc, and the weekly full channel may build bundles of all
#     supported architectures in one). We generally partition this in order to
#     match CI and testing fan-out parallelism needed in order to meet CI
#     latency SLAs for different channels.
#   - {variant}: The build variant. For normal release builds this will be
#     "release". Various sanitizer and debug variants are also defined. Not
#     all combinations are distinct (i.e. the "doc" component may be the same
#     for all santizer variants), but we assemble and publish them regardless.
#   - {component}: For distributed C++ artifacts, there will typically be a
#     standard set of components (e.g. "runfiles", "dev", "doc", "dbg", etc).
#     Different pipelines can include just the slices they need, reducing
#     CI churn and overhead. See `Components` below for more definition.
#
# Slices
# ------
# The standard ROCm build consists of the following slices:
#   - "third-party": stage directories of all needed third-party libraries.
#     All slices can be considered to conditionally depend on third-party.
#     Whether they do actually or not is build configuration dependent (i.e.
#     some builds may be configured to use system vs bundled deps, etc).
#     Dependencies: None
#     Target specifity: Target neutral
#
#   - "base": stage directories for sub-projects in the base/ directory.
#     Dependencies: None
#     Target specifity: Target neutral
#
#   - "compiler-amd-llvm": The compiler/amd-llvm sub-project.
#     Dependencies: base
#     Target specificity: Target neutral
#
#   - "compiler-hipify": The compiler/hipify sub-project.
#     Dependencies: base, compiler-amd-llvm
#     Target specificity: Target neutral
#
#   - "core-runtime": Core sub-projects that do not have a runtime dependency
#     on the compiler (e.g. ROCR-Runtime, rocminfo, etc).
#     Dependencies: base
#     Target specificity: Yes
#
#   - "core-hip": HIP runtime components, including compiler interfaces.
#     Dependencies: base, core-runtime, compiler-amd-llvm
#     Target specificity: Yes
#
#   - "comm-libs-rccl": The RCCL sub-project.
#     Dependencies: base, core-hip, compiler-hipify
#     Target specificity: Yes
#
#   - "math-libs-blas": Combination of all enabled BLAS libraries for the
#     target bundle.
#     Dependencies: base, compiler-amd-llvm, core-hip
#     Target specificity: Yes
#
#   - "math-libs-rand": Combination of enabled RAND math-libs.
#     Dependencies: base, compiler-amd-llvm, core-hip
#     Target specificity: Yes
#
#   - "ml-frameworks-miopen": MIOpen sub-project.
#     Dependencies: Variable
#     Target specificity: Yes
#
# Components
# ----------
# Most slices encapsulate the artifacts that make up a distributed C++ library
# or tool. We follow a standard layout of components for each such slice,
# deviating if the situation warrants (i.e. if a subproject has pre-compiled
# kernels, etc it might have an additional component).
#
#   - "runfiles": Files that must be present in order to execute dynamically
#     linked dependencies. This includes both shared-libraries/DLLs and any
#     inseparable data files that must be present for the slice to function.
#     This includes runnable binaries in the case of bundled tools.
#   - "dev": Files needed in order to compile dependent sub-projects. This
#     includes header trees, cmake directories, static libraries, import
#     libraries and the like. It is meant to layer with "runfiles" to produce
#     a complete set of files needed to build against the contained libraries.
#   - "dbg": If the build was performed with debug symbols and the "runfiles"
#     contains stripped binaries, this component will contain the corresponding
#     debug symbols in a platform specific arrangement.
#   - "doc", etc: Ancillary components that include any remaining parts.
