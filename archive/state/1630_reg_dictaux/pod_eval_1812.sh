#!/usr/bin/env bash
# H_1812 engine-native G0-G6 eval (torch-free numpy via core/g_gates.py <- core/clm_decode.py).
# cli/evaluate.py is the single-entry that imports g_gates.g_eval_all (TERMINAL-eligible).
set -u
cd ~/anima
CORP=state/clm303_clean_corpus
CKPT=state/1630_reg_dictaux/ckpt
GEN=80
log=state/1630_reg_dictaux/eval_1812.log
: > "$log"
echo "=== H_1812 engine-native eval START $(date -u) gen=$GEN ===" >> "$log"
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
echo "=== H_1812 eval COMPLETE $(date -u) ===" >> "$log"
