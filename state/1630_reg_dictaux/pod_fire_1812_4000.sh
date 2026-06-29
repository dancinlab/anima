#!/usr/bin/env bash
# H_1812 4000-step multiseed CLOSURE test (n6n7 primary lever) + matched ce_marginal control.
# Runs SEQUENTIALLY on the single A40, detached. Polls externally.
set -u
cd /root/anima
export PYTHONPATH=train/clm/model:cli:core
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
CORP="state/clm303_clean_corpus"
CORPUS="$CORP/gen_ko.txt $CORP/gen_en.txt $CORP/sns_ko.txt $CORP/sns_en.txt"
LABELS="ko-general en-general ko-sns en-sns"
OUT=state/1630_reg_dictaux/ckpt4000
mkdir -p "$OUT"

ARMS="${ARMS:-n6n7}"
SEEDS="${SEEDS:-4307 4308 4309}"
STEPS="${STEPS:-4000}"

log=/root/anima/state/1630_reg_dictaux/fire_1812_4000.log
echo "=== H_1812 4000-step fire START $(date -u) arms=[$ARMS] seeds=[$SEEDS] steps=$STEPS ===" >> "$log"
for ARM in $ARMS; do
  for SEED in $SEEDS; do
    echo "--- arm=$ARM seed=$SEED steps=$STEPS $(date -u) ---" >> "$log"
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
echo "=== H_1812 4000-step fire COMPLETE $(date -u) ===" >> "$log"
