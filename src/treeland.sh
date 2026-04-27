#!/usr/bin/env sh

script_path=$(realpath $(dirname "$0"))
cmd="$script_path/treeland"
# Include all user arguments in test to ensure consistent environment
output=$($cmd --try-exec "$@" 2>&1)

if echo "$output" | grep -Eq "failed to create dri2 screen|DRI2: failed to create screen|gbm_bo_create failed|Failed to allocate buffer"; then
    # In VirtualBox, if 3D acceleration is not enabled, calling `eglInitialize` will cause
    # the program to fail during renderer initialization. Fall back to pixman
    # when known GBM/DRI2 allocation errors are reported, even if try-exec exits 0.
    export WLR_RENDERER=pixman
    echo "Treeland renderer init failed, try fallback to software renderer."
fi

# Use exec to replace current process instead of creating a subprocess
# This ensures treeland directly replaces treeland.sh process, avoiding dual processes
exec $cmd "$@"
