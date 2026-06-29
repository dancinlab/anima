#!/usr/bin/env bash
# eval_pool.sh — CPU-bound: G0-G6 engine-native eval for every .clm, SEQUENTIALLY (one at a time
# to avoid CPU oversubscription). Loops until all expected clms are evaluated. Decoupled from GPU train.
set -u
cd ~/anima || exit 1
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
CORPUS="state/clm303_clean_corpus/gen_ko.txt state/clm303_clean_corpus/gen_en.txt state/clm303_clean_corpus/sns_ko.txt state/clm303_clean_corpus/sns_en.txt"
H1640=state/binding_arch_census/h1640_hamiltonian/ckpt
H1641=state/binding_arch_census/h1641_laminar/ckpt
H1602W=state/binding_arch_census/h1602_eval
mkdir -p "$H1602W"

eval_one() {  # $1=clm $2=outtxt
  local clm=$1 out=$2
  [ -f "$out" ] && [ -s "$out" ] && { echo "SKIP done $out"; return; }
  [ -f "$clm" ] || { return 1; }
  echo "=== EVAL $clm $(date +%H:%M:%S) ==="
  PYTHONPATH=core:cli:train/clm/model python3 cli/evaluate.py "$clm" --corpus $CORPUS --gen 80 > "$out" 2>&1
  echo "  RC=$? -> $out"; grep -E "G0 |G1 |G2 |G6 |CLOSURE" "$out" | head -6
}

# expected work list: H_1602 (9 existing clms) + H_1640 (9) + H_1641 (9) = 27 evals
ALL_DONE=0
PASS=0
while [ "$ALL_DONE" = 0 ] && [ $PASS -lt 200 ]; do
  PASS=$((PASS+1))
  PENDING=0
  # H_1602 existing clms
  for f in ~/anima-weights/recomb_obj_303m/*.clm; do
    [ -f "$f" ] || continue
    b=$(basename "$f" .clm); o="$H1602W/${b}.g0g6.txt"
    if [ ! -s "$o" ]; then eval_one "$f" "$o"; PENDING=$((PENDING+1)); fi
  done
  # H_1640 / H_1641 trained clms (as they appear)
  for d in "$H1640" "$H1641"; do
    for f in "$d"/*.clm; do
      [ -f "$f" ] || continue
      b=$(basename "$f" .clm); o="$d/${b}.g0g6.txt"
      if [ ! -s "$o" ]; then eval_one "$f" "$o"; PENDING=$((PENDING+1)); fi
    done
  done
  n1602=$(ls "$H1602W"/*.g0g6.txt 2>/dev/null | wc -l)
  n40=$(ls "$H1640"/*.g0g6.txt 2>/dev/null | wc -l)
  n41=$(ls "$H1641"/*.g0g6.txt 2>/dev/null | wc -l)
  echo "[pool pass $PASS] h1602=$n1602/9 h1640=$n40/9 h1641=$n41/9 pending_this_pass=$PENDING $(date +%H:%M:%S)"
  if [ "$n1602" -ge 9 ] && [ "$n40" -ge 9 ] && [ "$n41" -ge 9 ]; then ALL_DONE=1; break; fi
  [ "$PENDING" = 0 ] && sleep 120   # nothing new; wait for trainer to emit more clms
done
echo "############ eval_pool.sh ALL DONE $(date +%H:%M:%S) ############"
