#!/usr/bin/env bash
# H_1640 CLS-SEP-COMPLETE — 303M GPU launch (DO NOT run from the bio subagent;
# main dispatches after objrun lands, a_fire_autonomous). 3 arms x 3 seeds = 9.
# Canon = L4 d3784 E2->E3 (clm303_clean / H_1602 isomorphic). bf16 GPU.
#
# Corpus = clean language-split 4-cell register (a_chat_registers). Replace the
# 4 paths with the resolved clean-corpus local paths (HF: anima-corpus-{ko,en}-
# {general,sns}); resolve_corpus_path also accepts the canonical short specs.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="$HERE"; while [ "$REPO" != "/" ] && [ ! -e "$REPO/cli/train.py" ]; do REPO="$(dirname "$REPO")"; done
cd "$REPO"
OUT="$HERE/ckpt"; mkdir -p "$OUT"

# 4-cell corpus (EDIT to resolved clean-corpus paths before launch)
KO_GEN="${KO_GEN:?set KO_GEN to ko-general corpus path}"
EN_GEN="${EN_GEN:?set EN_GEN to en-general corpus path}"
KO_SNS="${KO_SNS:?set KO_SNS to ko-sns corpus path}"
EN_SNS="${EN_SNS:?set EN_SNS to en-sns corpus path}"

for OBJ in ce_marginal cls_sep cls_full; do
  for SEED in 7 4302 4303; do
    echo "=== H_1640 launch obj=$OBJ seed=$SEED ==="
    python3 "$HERE/trainer.py" --objective "$OBJ" --seed "$SEED" --canon \
      --corpus "$KO_GEN" "$EN_GEN" "$KO_SNS" "$EN_SNS" \
      --cell-label ko-general en-general ko-sns en-sns \
      --sample proportional --steps 2000 --val-every 200 --bf16 \
      --out "$OUT/${OBJ}_seed${SEED}.clm" \
      --ckpt-out "$OUT/${OBJ}_seed${SEED}.pt" \
      --gauges-out "$OUT/${OBJ}_seed${SEED}.json" 2>&1 | tee "$OUT/${OBJ}_seed${SEED}.log"
  done
done
echo "=== H_1640 ALL ARMS DONE -> engine-native: anima eval <clm> --corpus ... --gen 80 ==="
