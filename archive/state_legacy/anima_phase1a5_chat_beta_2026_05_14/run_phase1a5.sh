#!/bin/bash
# run_phase1a5.sh — Phase 1A.5 chat-beta on ubu-2 RTX 5070
# anima OWN substrate path (not foundation borrow):
#   base ckpt = Phase 1A.4 lr5e6 SFT (already V5.8 5/5 PASS, but conversational
#   coherence 0/6 per BENCHMARK.md)
#   delta    = anima-persona-balanced corpus 1.3MB (more diverse than
#              anima_fact 13499 lines narrow) × 2000 steps × lr 5e-6
#   target   = ≥4/6 conversational-pass on free-form 6-probe
set -euo pipefail

# Phase 1A.4 trainer + arch from anima repo
WORK="$HOME/anima_bench"
TRAIN="$WORK/training"
PHASE1A4="$WORK/state/anima_phase1a4_lr5e6_2026_05_12"
OUT="$WORK/state/anima_phase1a5_chat_beta_2026_05_14"
mkdir -p "$OUT"

# Need engine_a_g_arch.py from training/
ls "$TRAIN/engine_a_g_arch.py" || { echo "ERROR: missing engine arch"; exit 1; }
ls "$PHASE1A4/train_phase1a4.py" || { echo "ERROR: missing Phase 1A.4 trainer"; exit 1; }
ls "$PHASE1A4/ckpts/ckpt_phase1a4_lr5e6_sft.pt" || { echo "ERROR: missing base ckpt"; exit 1; }

# Phase 1A.4 trainer expects --base-ckpt and --chat-corpus, --steps etc.
# We use anima-persona-balanced.txt as the diverse corpus.
CORPUS="$WORK/state/anima_v5mitosis_cotrain_2026_05_12/corpus_persona_balanced.txt"
ls "$CORPUS" || { echo "ERROR: missing corpus"; exit 1; }

STEPS="${STEPS:-2000}"
LR="${LR:-5e-6}"
BSZ="${BSZ:-2}"
GA="${GA:-4}"
CTX="${CTX:-1024}"
WARMUP="${WARMUP:-100}"
SEED="${SEED:-42}"

cd "$TRAIN"
python3 "$PHASE1A4/train_phase1a4.py" \
  --base-ckpt "$PHASE1A4/ckpts/ckpt_phase1a4_lr5e6_sft.pt" \
  --chat-corpus "$CORPUS" \
  --output "$OUT" \
  --steps "$STEPS" --bsz "$BSZ" --grad-accum "$GA" --ctx "$CTX" \
  --lr "$LR" --warmup "$WARMUP" --seed "$SEED" \
  --cost-cap-usd 999 --cost-per-hr 0.27 \
  2>&1 | tee "$OUT/train.log"
