#!/bin/bash
# launch_trainer.sh — pod-side wrapper that GUARANTEES env-var passthrough.
# Called by dispatch_s187_3b_runpod.sh attempt9+. Pod-side path.
#
# Why a wrapper file: the shell-string `$SSH "VAR=val nohup python3 ..."`
# pattern silently drops VAR somewhere between sh -c, nohup, and the python
# child on some runpod images (verified empirically 2026-05-21 attempt8:
# /proc/$PID/environ returned empty for PYTORCH_CUDA_ALLOC_CONF). A scp'd
# wrapper using `export` + `exec` is the canonical fix.
#
# See: ~/core/wilson/inbox/notes/2026-05-21-hexa-cloud-typed-env-var-passing.md
set -euo pipefail

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
# expose to log so dispatch.log can verify
echo "[launch] PYTORCH_CUDA_ALLOC_CONF=$PYTORCH_CUDA_ALLOC_CONF"

# attempt10 (2026-05-21): install bitsandbytes for PagedAdamW8bit.
# Replaces torch.optim.AdamW (f32 m+v ≈ 8× params) with 8-bit Paged variant
# (≈ 2× params) — fits 3B on 80GB H100 with headroom. Runs once per pod
# (subsequent reboots cached in /usr/local site-packages). Pinned to 0.43.1
# for CUDA 12.4 / torch 2.4 compatibility (runpod base image).
if ! python3 -c "import bitsandbytes" 2>/dev/null; then
  echo "[launch] pip install bitsandbytes==0.43.1"
  pip install -q --no-cache-dir bitsandbytes==0.43.1
fi
python3 -c "import bitsandbytes as bnb; print(f'[launch] bitsandbytes={bnb.__version__}')"

echo "[launch] python3 -u $@"
exec python3 -u "$@"
