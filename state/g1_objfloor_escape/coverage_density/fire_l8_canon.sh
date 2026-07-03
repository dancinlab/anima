#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# fire_l8_canon.sh — H_6185 coverage-density G1 escape · 303M L8-RF retrain fire.
#
# Steps (3)+(4): warm-FT clm303 (h1129 G0-🟢 trunk) at L8 dilated-conv (RF≈511B)
# on the combination-coverage corpus, then judge frozen G1 engine-native.
#
# ── CANONICAL RETRAIN PATH = `anima train --py` (torch Lane-P, cli/train.py) ──
#   The hexa trainer (cli/train.hexa MODE_CANON, L_canon patched 4→8 in this
#   worktree) is under GPU-util fix (CPU-scalar-bound #2598/#2600) AND OOMs on
#   12GB GPUs (fp64 farr, convergence train-hexa-1). The WORKING production path
#   is the torch trainer via --py (fp32/bf16 — fits 12GB), whose RF is the CLI
#   arg  --L 8  (n_trunk_layers → CLMConfig → CausalDilatedConv1d dilation
#   min(2^l,512): L8 dils [1,2,4,8,16,32,64,128] Σ255 → RF = 1+2·255 = 511B).
#
# ⚠️ HOST GATE — heavy 303M GPU job → POOL/POD, never mini (swap 🔴 OOM rc=137):
#   summer/aiden = RTX5070 12GB (torch 303M fits, but heavy-job OOM/wedge risk
#   under load — summer-overfire; run SOLO, OMP_NUM_THREADS cap). Preferred =
#   24GB+ rented pod (A100), but pod rental is cost/explicit-go gated this
#   session ("💸 4th pod 렌트 금지", memory h9107) → this fire is NOT autonomous.
#   Est. A100-40GB ~$1.2/h × ~2–4h warm-FT (2000 steps) ≈ $2.5–5.
#
# Prereqs on the GPU host: hx install anima ; corpus + h1129c_chat.pt present.
# NOTE: on a fresh checkout the anima CLI needs the EngineConfig `forward_model`
#   fix (cli/anima.hexa:1643-1644 — 2 struct literals missing the H_9119 field;
#   applied in this worktree). Without it `anima <verb>` fails to compile.
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORPUS="$HERE/corpus"
INIT="${INIT:-state/chat_303m/h1129c_chat.pt}"          # warm-FT trunk (G0🟢)
OUT_CLM="${OUT_CLM:-$HERE/clm303_l8_covdens.clm}"
OUT_PT="${OUT_PT:-$HERE/clm303_l8_covdens.pt}"
D="${D:-768}"   # match h1129 d_model (verify via serialize header; --d 0 = auto)

# (3) retrain — torch Lane-P, L8 trunk, warm-FT h1129, held-out val, --sample
#     proportional (memorization guard, a_savant_train / clm303-clean).
anima train --py --arch clm \
    --L 8 --d "$D" \
    --init "$INIT" \
    --corpus "$CORPUS/en_block.txt" --corpus "$CORPUS/ko_block.txt" \
    --sample proportional \
    --steps 2000 --seq-len 1024 \
    --out "$OUT_CLM" --ckpt-out "$OUT_PT" \
    > "$HERE/train_l8_covdens.log" 2>&1

# ── teardown-BEFORE ckpt PULL (a_fire_recover_complete): pull $OUT_CLM + $OUT_PT
#    to pool host / HF BEFORE any pod teardown. ──

# (4) frozen G1 judge — engine-native, py canonical path (a_eval_py_canonical).
#     G1 RECOMBINATION passes iff some k: composed_distinct ≥2 AND >max_single AND
#     coherent, on the held-out gate pairs (UNEXPOSED in corpus = memorization-free).
#     --gen 80 (not 0 → collapses to 40) for a wide budget.
anima evaluate --py "$OUT_CLM" \
    --corpus "$CORPUS/en_block.txt" --gen 80 \
    > "$HERE/g1_judge_l8_covdens.json" 2>&1
cat "$HERE/g1_judge_l8_covdens.json"
# ≥threshold (A.novel best_distinct≥2 across ≥ seeds) → coverage-density POSITIVE
# confirmed (G1 opens as data-coverage+RF lever). below → coverage is also floor.
