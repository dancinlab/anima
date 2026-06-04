#!/usr/bin/env bash
# tooluse_copy_scale_fire.sh — Lever B SCALE-LADDER fire on a POOL GPU host ($0, NOT a pod).
#
# Pulls the SAME argcopy corpus as #1835 (dancinlab/anima-agent-lane-argcopy-corpus) from HF,
# then runs the from-scratch compute-matched scale ladder (training/tooluse_copy_scale.py).
# nvidia-smi busy is REQUIRED (a_train_flame_forge: no silent CPU fallback — the driver
# SystemExit(3)'s if no CUDA). Logs to a /tmp file; harvested inline by sleep-poll (no waiter).
set -euo pipefail

WORK="${WORK:-$HOME/copyscale-fire}"
CORPUS_REPO="dancinlab/anima-agent-lane-argcopy-corpus"
HF_TOKEN_ARG="${HF_TOKEN:-}"
STEPS="${STEPS:-3000}"
BATCH="${BATCH:-32}"
VRAM_CAP="${VRAM_CAP:-11.0}"
LADDER="${LADDER:-}"   # empty = full ladder until VRAM cap

mkdir -p "$WORK/out"
cd "$WORK"

echo "[fire] host=$(hostname) work=$WORK"
nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu --format=csv,noheader

# ── pull corpus from HF (the with-argcopy full corpus) ──
if [ -n "$HF_TOKEN_ARG" ]; then export HF_TOKEN="$HF_TOKEN_ARG"; fi
echo "[fire] pulling corpus $CORPUS_REPO"
hf download "$CORPUS_REPO" --repo-type dataset --local-dir "$WORK/corpus" 2>&1 | tail -8
echo "[fire] corpus dir contents:"; ls -la "$WORK/corpus"

# locate the corpus .txt (the with-argcopy full corpus)
CORPUS_TXT=$(find "$WORK/corpus" -name '*.txt' | head -1)
echo "[fire] corpus txt = $CORPUS_TXT"
python3 - "$CORPUS_TXT" <<'PY'
import sys, hashlib
p = sys.argv[1]
b = open(p, "rb").read()
print(f"[fire] corpus bytes={len(b)} sha256={hashlib.sha256(b).hexdigest()}")
# leak re-check: held-out PB keys must NOT be in the corpus
heldout = [f"PB{n:02d}".encode() for n in range(1, 37)]
leak = [k.decode() for k in heldout if k in b]
print(f"[fire] held-out-key leak in corpus = {len(leak)} {leak[:5]}")
assert not leak, "held-out key LEAKED in corpus — abort"
PY

echo "[fire] launching scale ladder (steps=$STEPS batch=$BATCH vram_cap=$VRAM_CAP ladder='${LADDER:-ALL}')"
python3 -u "$WORK/tooluse_copy_scale.py" \
  --corpus "$CORPUS_TXT" \
  --out-dir "$WORK/out" \
  --steps "$STEPS" --batch "$BATCH" --vram-cap-gb "$VRAM_CAP" \
  ${LADDER:+--ladder "$LADDER"}

echo "[fire] DONE — summary:"
cat "$WORK/out/summary.json"
