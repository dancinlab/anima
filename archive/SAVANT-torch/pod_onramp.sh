#!/usr/bin/env bash
# SAVANT torch-cuda lane — single-pod ONRAMP (runs detached ON the pod).
# Sequence on ONE pod, leak-safe (no re-rent anywhere):
#   1. deps + 5-lang euro corpus build under /workspace (persistent)
#   2. rung0  — SMALL d512/8L validation (proves recipe+corpus+ckpt, clean descent)
#   3. rung-7B — durable d4096/36L/32H/block512 = 7.25B train as a detached nohup
#                with --ckpt-every under /workspace (survives preemption, --resume able)
# All under /workspace so a persistent volume keeps every artifact across reboots.
# This script is itself launched via nohup by the rent onstart; it never re-rents.
set -uo pipefail

WS=/workspace/savant
mkdir -p "$WS"
cd "$WS"
LOG="$WS/onramp.log"
exec > >(tee -a "$LOG") 2>&1

echo "=== [onramp] start $(date -u +%FT%TZ) ==="
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader || true

echo "=== [onramp] deps ==="
pip install -q --no-input torch datasets huggingface_hub bitsandbytes 2>&1 | tail -3 || true

# ---- corpus (small for rung0 first; 7B reuses a bigger build) ----
# rung0 corpus: small slice (4 MB/lang ~= 20 MB) — fast, proves the pipeline.
echo "=== [onramp] rung0 corpus build (4 MB/lang) ==="
python "$WS/build_corpus_5lang_euro.py" \
    --out "$WS/corpus_rung0.txt" --mb-per-lang 4 --date 20231101 \
    2>&1 | tee "$WS/corpus_rung0_build.log" || true

# ---- rung0: SMALL validation (d512/8L ~ 85M, bounded steps) ----
echo "=== [onramp] rung0 train (d512/8L, 120 steps) ==="
python "$WS/savant_train_torch_cuda.py" \
    --corpus "$WS/corpus_rung0.txt" \
    --d 512 --n_layer 8 --n_head 8 --block 512 \
    --batch 16 --steps 120 --warmup 10 --eval_every 20 \
    --model_dtype bf16 --opt adamw8bit \
    --out "$WS/rung0/savant_rung0.pt" \
    --log "$WS/rung0/savant_rung0.log.json" \
    2>&1 | tee "$WS/rung0_train.log"

# parse rung0 descent verdict
RUNG0_PASS=$(python - <<'PY'
import json,sys
try:
    r=json.load(open("/workspace/savant/rung0/savant_rung0.log.json"))
    print(r["descent"]["F_CLM_REF_7B_DESCENT"])
except Exception as e:
    print(0)
PY
)
echo "=== [onramp] rung0 descent F=$RUNG0_PASS ==="

if [ "$RUNG0_PASS" != "1" ]; then
    echo "=== [onramp] rung0 did NOT descend — ABORT 7B (recipe/corpus issue, fail-loud) ==="
    echo "FAILED_RUNG0" > "$WS/ONRAMP_STATE"
    exit 1
fi
echo "RUNG0_PASS" > "$WS/ONRAMP_STATE"

# ---- 7B corpus (bigger build, 80 MB/lang ~ 400 MB) ----
echo "=== [onramp] 7B corpus build (80 MB/lang ~400MB) ==="
python "$WS/build_corpus_5lang_euro.py" \
    --out "$WS/corpus_5lang.txt" --mb-per-lang 80 --date 20231101 \
    2>&1 | tee "$WS/corpus_5lang_build.log" || true

# ---- rung-7B: durable detached nohup, ckpt every 200 steps under /workspace ----
echo "=== [onramp] launch 7B durable nohup ==="
mkdir -p "$WS/rung7b"
nohup python "$WS/savant_train_torch_cuda.py" \
    --corpus "$WS/corpus_5lang.txt" \
    --d 4096 --n_layer 36 --n_head 32 --block 512 \
    --batch 8 --grad_accum 4 --steps 6000 --warmup 100 --eval_every 50 \
    --lr 1.6e-4 --model_dtype bf16 --opt adamw8bit \
    --ckpt-every 200 \
    --out "$WS/rung7b/savant_5lang_7b.pt" \
    --log "$WS/rung7b/savant_5lang_7b_train.log.json" \
    > "$WS/rung7b/train_7b.out" 2>&1 &
echo $! > "$WS/rung7b/train_7b.pid"
echo "7B_LAUNCHED pid=$(cat $WS/rung7b/train_7b.pid)" >> "$WS/ONRAMP_STATE"
echo "=== [onramp] 7B launched pid=$(cat $WS/rung7b/train_7b.pid) — onramp done $(date -u +%FT%TZ) ==="
