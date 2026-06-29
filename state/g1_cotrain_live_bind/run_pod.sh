#!/usr/bin/env bash
# H_1818 run_pod.sh — co-trained live-retained bind op experiment.
# Run ON THE POD after ~/anima/ is synced. Drives bind + ctrl × 3 seeds,
# serializes (bind via CLMB, ctrl standard), runs engine-native-py G0-G6,
# writes all results to state/g1_cotrain_live_bind/ckpt/.
#
# USAGE (on pod):
#   bash ~/anima/state/g1_cotrain_live_bind/run_pod.sh [smoke|bind|ctrl|eval|all]
#   default: all (smoke-gate then full run)
set -uo pipefail
cd ~/anima || { echo "FATAL: ~/anima not found"; exit 1; }
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 PYTHONPATH=core:cli:train/clm/model

CORPUS="state/clm303_clean_corpus/gen_ko.txt state/clm303_clean_corpus/gen_en.txt state/clm303_clean_corpus/sns_ko.txt state/clm303_clean_corpus/sns_en.txt"
LBL="ko-general en-general ko-sns en-sns"
TRAINER="state/g1_cotrain_live_bind/trainer.py"
CKPT_DIR="state/g1_cotrain_live_bind/ckpt"
PHASE="${1:-all}"
mkdir -p "$CKPT_DIR"

py() { python3 "$@"; }

# ── train one arm/seed combination ──────────────────────────────────────────
train_full() {   # $1=arm $2=seed
  local arm=$1 sd=$2
  local base="$CKPT_DIR/${arm}_seed${sd}"
  echo "=== TRAIN arm=${arm} seed=${sd} ==="
  py "$TRAINER" --arm "$arm" --seed "$sd" \
    --corpus $CORPUS --cell-label $LBL \
    --canon --steps 2000 --seq-len 1024 --batch-size 8 \
    --e0 2 --emax 3 --val-frac 0.05 --val-every 200 \
    --sample proportional --bf16 \
    --out "${base}.clm" \
    --ckpt-out "${base}.pt" \
    --gauges-out "${base}.json" \
    > "${base}.train.log" 2>&1
  local rc=$?
  echo "  RC=${rc}  -> ${base}.clm"
  # quick descent echo from log
  grep -E "DESCENT|val_CE|registers_DESCENT|clm_decodable" "${base}.train.log" | tail -8
  return $rc
}

# ── G0-G6 engine-native-py eval ──────────────────────────────────────────────
eval_g0g6() {   # $1=clm $2=outtxt
  local clm=$1 out=$2
  echo "=== EVAL G0-G6 ${clm} ==="
  py cli/evaluate.py "$clm" --corpus $CORPUS --gen 80 > "$out" 2>&1
  local rc=$?
  echo "  RC=${rc} -> ${out}"
  grep -E "G0|G1|G2|G3|G5|G6|CLOSURE|a7b_pass|composed_distinct|falsifiable|kwr" "$out" | head -20
  return $rc
}

# ── smoke gate (tiny, RC check only) ────────────────────────────────────────
if [ "$PHASE" = smoke ] || [ "$PHASE" = all ]; then
  echo "############ SMOKE (tiny) ############"
  for arm in bind ctrl; do
    echo "--- smoke ${arm} ---"
    py "$TRAINER" --arm "$arm" --seed 7 --corpus $CORPUS --cell-label $LBL \
      --d 16 --L 1 --steps 30 --seq-len 64 --batch-size 4 \
      --e0 2 --emax 3 --val-frac 0.05 --val-every 30 \
      --out "/tmp/h1818_sm_${arm}.clm" --ckpt-out "/tmp/h1818_sm_${arm}.pt" \
      --gauges-out "/tmp/h1818_sm_${arm}.json" 2>&1 | tail -12
    echo "  smoke RC=$?"
  done
  # verify clm_decode CLMB parsing on smoke bind .clm
  echo "--- smoke CLMB decode check ---"
  py -c "
import sys; sys.path.insert(0,'core')
import clm_decode as cd
W = cd.clm_load_weights('/tmp/h1818_sm_bind.clm')
bt = W.get('bind_type',0)
ok = W.get('ok',False)
print(f'  clm_load_weights ok={ok} bind_type={bt}')
assert ok, 'FATAL: not decodable'
assert bt == 1, f'FATAL: expected bind_type=1 got {bt}'
print('  CLMB parse OK — bind op will execute at decode')
"
  echo "  CLMB check RC=$?"
  [ "$PHASE" = smoke ] && exit 0
fi

# ── bind arms × 3 seeds ──────────────────────────────────────────────────────
if [ "$PHASE" = bind ] || [ "$PHASE" = all ]; then
  echo "############ BIND ARMS ############"
  for sd in 7 4302 4303; do
    train_full bind "$sd" || echo "WARNING: bind seed${sd} non-zero RC"
  done
fi

# ── ctrl arms × 3 seeds ──────────────────────────────────────────────────────
if [ "$PHASE" = ctrl ] || [ "$PHASE" = all ]; then
  echo "############ CTRL ARMS ############"
  for sd in 7 4302 4303; do
    train_full ctrl "$sd" || echo "WARNING: ctrl seed${sd} non-zero RC"
  done
fi

# ── G0-G6 engine-native-py eval on all 6 .clm files ────────────────────────
if [ "$PHASE" = eval ] || [ "$PHASE" = all ]; then
  echo "############ G0-G6 EVAL (engine-native-py) ############"
  for arm in bind ctrl; do
    for sd in 7 4302 4303; do
      clm="$CKPT_DIR/${arm}_seed${sd}.clm"
      out="$CKPT_DIR/${arm}_seed${sd}.g0g6.txt"
      if [ -f "$clm" ]; then
        eval_g0g6 "$clm" "$out"
      else
        echo "  SKIP $clm (not found)"
      fi
    done
  done
fi

# ── collect summary ──────────────────────────────────────────────────────────
echo ""
echo "############ SUMMARY ############"
echo "Held-out descent (all arms):"
for arm in bind ctrl; do
  for sd in 7 4302 4303; do
    j="$CKPT_DIR/${arm}_seed${sd}.json"
    [ -f "$j" ] && python3 -c "
import json,sys
d=json.load(open('$j'))
rd=d.get('registers_descent','?')
fv=d.get('final_val_ce_pooled','?')
print(f'  ${arm}/seed${sd}: descent={rd} pooled_val_ce={fv}')
" 2>/dev/null || echo "  ${arm}/seed${sd}: json missing"
  done
done

echo ""
echo "G0-G6 G1 composed_distinct (per arm):"
for arm in bind ctrl; do
  for sd in 7 4302 4303; do
    g="$CKPT_DIR/${arm}_seed${sd}.g0g6.txt"
    if [ -f "$g" ]; then
      g1=$(grep -i "G1\|composed_distinct\|recomb" "$g" | head -3)
      echo "  ${arm}/seed${sd}: $g1"
    else
      echo "  ${arm}/seed${sd}: g0g6.txt missing"
    fi
  done
done

echo "############ run_pod.sh DONE ($PHASE) ############"
