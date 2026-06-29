#!/usr/bin/env bash
# H_1812 4000-step engine-native G0-G6 eval (torch-free numpy via core/g_gates.py).
# gen=80 (same condition as 2000-step run where G1 0->1 appeared).
set -u
cd /root/anima
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
CORP=state/clm303_clean_corpus
CKPT=state/1630_reg_dictaux/ckpt4000
GEN=80
log=/root/anima/state/1630_reg_dictaux/eval_1812_4000.log
: > "$log"
echo "=== H_1812 4000-step engine-native eval START $(date -u) gen=$GEN ===" >> "$log"
for CLM in $CKPT/*.clm; do
  [ -e "$CLM" ] || continue
  echo "" >> "$log"
  echo "############## $CLM ##############" >> "$log"
  PYTHONPATH=core:cli:train/clm/model python3 cli/evaluate.py "$CLM" \
    --corpus $CORP/gen_ko.txt $CORP/gen_en.txt $CORP/sns_ko.txt $CORP/sns_en.txt \
    --gen $GEN >> "$log" 2>&1
  echo "---- descent gate (held-out tails) ----" >> "$log"
  for REG in gen_ko gen_en sns_ko sns_en; do
    echo "## descent $REG" >> "$log"
    python3 train/clm/model/verify_clm_v2.py descent "$CLM" $CORP/$REG.txt >> "$log" 2>&1
  done
done
echo "" >> "$log"
echo "=== H_1812 4000-step eval COMPLETE $(date -u) ===" >> "$log"
