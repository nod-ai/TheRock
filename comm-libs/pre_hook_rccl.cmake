# RCCL uses "GPU_TARGETS", not "AMDGPU_TARGETS" like we automatically pass.
# Since this is notoriously hard to pass from the command line and get escaping
# right, we just short-circuit it here and force. If this ever gets renamed
# to AMDGPU_TARGETS like the rest, this can be removed.
set(GPU_TARGETS "${AMDGPU_TARGETS}" CACHE STRING "From super-project" FORCE)
unset(AMDGPU_TARGETS)
