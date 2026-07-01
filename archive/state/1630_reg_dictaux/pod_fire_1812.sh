#!/usr/bin/env bash
# H_1812 (slug 1630_reg_dictaux) — 303M arm sweep on A40.
# Runs arms x seeds SEQUENTIALLY on the single A40, detached. Polls externally.
set -u
cd ~/anima
CORP="state/clm303_clean_corpus"
CORPUS="$CORP/gen_ko.txt $CORP/gen_en.txt $CORP/sns_ko.txt $CORP/sns_en.txt"
LABELS="ko-general en-general ko-sns en-sns"
OUT=state/1630_reg_dictaux/ckpt
mkdir -p "$OUT"

ARMS="${ARMS:-ce_marginal n6n7 n7_dictaux n6_grok}"
SEEDS="${SEEDS:-4307}"
STEPS="${STEPS:-4000}"

log=~/anima/state/1630_reg_dictaux/fire_1812.log
echo "=== H_1812 fire START $(date -u) arms=[$ARMS] seeds=[$SEEDS] steps=$STEPS ===" >> "$log"
for ARM in $ARMS; do
  for SEED in $SEEDS; do
    echo "--- arm=$ARM seed=$SEED $(date -u) ---" >> "$log"
    python3 state/1630_reg_dictaux/trainer.py \
      --arm "$ARM" --seed "$SEED" --canon --steps "$STEPS" \
      --corpus $CORPUS --cell-label $LABELS \
      --sample proportional --val-frac 0.05 --val-every 200 \
      --bf16 --dbes --n4-set-search 8 \
      --out      "$OUT/${ARM}_seed${SEED}.clm" \
      --ckpt-out "$OUT/${ARM}_seed${SEED}.pt" \
      --gauges-out "$OUT/${ARM}_seed${SEED}.json" >> "$log" 2>&1
    echo "--- DONE arm=$ARM seed=$SEED rc=$? $(date -u) ---" >> "$log"
  done
done
echo "=== H_1812 fire COMPLETE $(date -u) ===" >> "$log"
