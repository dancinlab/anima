#!/usr/bin/env bash
# PREREG co-trained bind op × recomb objective — 3-arm 4000-step decisive experiment.
#
# 3 ARMS × 3 SEEDS {7,4302,4303} = 9 runs.
# Uses 2× GPU if available (parallel arms on GPU0/GPU1 for same seed).
#
# USAGE (on pod after ~/anima/ is synced):
#   bash ~/anima/state/g1_cotrain_recomb_bind/run_pod.sh [smoke|train|eval|all]
#   default: all (smoke → train → eval → summary)
#
# DECISION TEST (PREREG FROZEN):
#   (op_obj) > (op_plaince) AND (op_obj) > (obj_only) on G1 best_distinct, same seeds
#   → "bind op + recomb objective TOGETHER lift G1"
set -uo pipefail
cd ~/anima || { echo "FATAL: ~/anima not found"; exit 1; }
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
export PYTHONPATH=core:cli:train/clm/model

CORPUS="state/clm303_clean_corpus/gen_ko.txt state/clm303_clean_corpus/gen_en.txt state/clm303_clean_corpus/sns_ko.txt state/clm303_clean_corpus/sns_en.txt"
LBL="ko-general en-general ko-sns en-sns"
TRAINER="state/g1_cotrain_recomb_bind/trainer.py"
CKPT_DIR="state/g1_cotrain_recomb_bind/ckpt"
PHASE="${1:-all}"
mkdir -p "$CKPT_DIR"

py() { python3 "$@"; }

# Detect GPU count
N_GPU=$(python3 -c "import torch; print(torch.cuda.device_count())" 2>/dev/null || echo 0)
echo "  [init] N_GPU=${N_GPU}  PHASE=${PHASE}"

# ── corpus byte-count check (a_chat_registers fail-loud) ──────────────────
check_corpus() {
  echo "  [corpus-check] 4-register byte counts:"
  for f in $CORPUS; do
    if [ -f "$f" ]; then
      echo "    $(wc -c < "$f") bytes — $f"
    else
      echo "    MISSING: $f  FATAL"
      exit 1
    fi
  done
}

# ── train one arm/seed on a specific CUDA device ──────────────────────────
train_arm() {    # $1=arm $2=seed $3=gpu_id
  local arm=$1 sd=$2 gpu=${3:-0}
  local base="$CKPT_DIR/${arm}_seed${sd}"
  echo "=== TRAIN arm=${arm} seed=${sd} GPU=${gpu} ===" | tee -a /tmp/recomb_train.log
  CUDA_VISIBLE_DEVICES="${gpu}" py "$TRAINER" \
    --arm "$arm" --seed "$sd" \
    --corpus $CORPUS --cell-label $LBL \
    --canon --steps 4000 --seq-len 1024 --batch-size 8 \
    --e0 2 --emax 3 --val-frac 0.05 --val-every 200 \
    --sample proportional --bf16 \
    --out "${base}.clm" \
    --ckpt-out "${base}.pt" \
    --gauges-out "${base}.json" \
    > "${base}.train.log" 2>&1
  local rc=$?
  echo "  RC=${rc}  -> ${base}.clm" | tee -a /tmp/recomb_train.log
  # Echo DESCENT gate result
  grep -E "DESCENT|val_CE|registers_DESCENT|clm_decodable|verify_descent" \
    "${base}.train.log" | tail -10 | tee -a /tmp/recomb_train.log
  return $rc
}

# ── G0-G6 engine-native-py eval ──────────────────────────────────────────────
eval_g0g6() {    # $1=clm $2=outtxt
  local clm=$1 out=$2
  echo "=== EVAL G0-G6 ${clm} ===" | tee -a /tmp/recomb_eval.log
  py cli/evaluate.py "$clm" --corpus $CORPUS --gen 80 > "$out" 2>&1
  local rc=$?
  echo "  RC=${rc} -> ${out}" | tee -a /tmp/recomb_eval.log
  grep -E "G0|G1|G2|G3|G5|G6|CLOSURE|a7b_pass|composed_distinct|falsifiable|kwr" \
    "$out" | head -25 | tee -a /tmp/recomb_eval.log
  return $rc
}

# ── smoke gate (tiny, checks imports + CLMB + obj_only serialization) ─────
if [ "$PHASE" = smoke ] || [ "$PHASE" = all ]; then
  echo "############ SMOKE ############"
  for arm in op_plaince obj_only op_obj; do
    echo "--- smoke ${arm} ---"
    py "$TRAINER" --arm "$arm" --seed 7 \
      --corpus $CORPUS --cell-label $LBL \
      --steps 4 --seq-len 128 --batch-size 4 \
      --e0 2 --emax 2 --val-every 4 --log-every 2 \
      --out "/tmp/h_recomb_sm_${arm}.clm" \
      --ckpt-out "/tmp/h_recomb_sm_${arm}.pt" 2>&1 | tail -8
    echo "  smoke ${arm} RC=$?"
  done

  # Check CLMB parse for bind arms
  for arm in op_plaince op_obj; do
    py -c "
import sys; sys.path.insert(0,'core')
import clm_decode as cd
W = cd.clm_load_weights('/tmp/h_recomb_sm_${arm}.clm')
bt = W.get('bind_type', 0)
ok = W.get('ok', False)
print(f'  ${arm} clm_load_weights ok={ok} bind_type={bt}')
assert ok, 'FATAL: not decodable'
assert bt == 1, f'FATAL: expected bind_type=1 got {bt}'
print('  CLMB parse OK — bind op will execute at decode')
" 2>&1
  done
  # Check obj_only has NO CLMB (standard additive)
  py -c "
import sys; sys.path.insert(0,'core')
import clm_decode as cd
W = cd.clm_load_weights('/tmp/h_recomb_sm_obj_only.clm')
bt = W.get('bind_type', 0)
ok = W.get('ok', False)
print(f'  obj_only clm_load_weights ok={ok} bind_type={bt}')
assert ok, 'FATAL: not decodable'
assert bt == 0, f'FATAL: expected bind_type=0 (additive) got {bt}'
print('  obj_only OK — additive readout, no CLMB (as expected)')
" 2>&1

  [ "$PHASE" = smoke ] && { echo "  SMOKE DONE"; exit 0; }
fi

# ── main training: 3 arms × 3 seeds ─────────────────────────────────────────
if [ "$PHASE" = train ] || [ "$PHASE" = all ]; then
  check_corpus
  echo "############ TRAINING (3 arms × 3 seeds, 4000 steps) ############"

  for sd in 7 4302 4303; do
    echo "====== SEED ${sd} ======"
    if [ "$N_GPU" -ge 2 ]; then
      # 2+ GPUs: run all 3 arms in parallel across 2 GPUs
      # GPU0: op_plaince + op_obj sequential, GPU1: obj_only
      (
        train_arm op_plaince "$sd" 0
        train_arm op_obj     "$sd" 0
      ) &
      pid_gpu0=$!
      train_arm obj_only "$sd" 1 &
      pid_gpu1=$!
      wait $pid_gpu0 || echo "WARNING: GPU0 arm(s) for seed${sd} non-zero RC"
      wait $pid_gpu1 || echo "WARNING: GPU1 obj_only seed${sd} non-zero RC"
    else
      # Single GPU: run sequentially
      train_arm op_plaince "$sd" 0 || echo "WARNING: op_plaince seed${sd} RC non-zero"
      train_arm obj_only   "$sd" 0 || echo "WARNING: obj_only seed${sd} RC non-zero"
      train_arm op_obj     "$sd" 0 || echo "WARNING: op_obj seed${sd} RC non-zero"
    fi

    echo "  === seed ${sd} done — ckpts: $(ls -1 ${CKPT_DIR}/*.clm 2>/dev/null | wc -l)/9"
  done

  echo "############ TRAINING COMPLETE ############"
fi

# ── G0-G6 eval on all 9 .clm files ──────────────────────────────────────────
if [ "$PHASE" = eval ] || [ "$PHASE" = all ]; then
  echo "############ G0-G6 EVAL (engine-native-py, gen=80) ############"
  for arm in op_plaince obj_only op_obj; do
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
  echo "############ G0-G6 EVAL COMPLETE ############"
fi

# ── summary table (PREREG decision test) ──────────────────────────────────
echo ""
echo "############ SUMMARY — DECISION TEST ############"
echo "Held-out descent (4/4 required for valid verdict):"
for arm in op_plaince obj_only op_obj; do
  for sd in 7 4302 4303; do
    j="$CKPT_DIR/${arm}_seed${sd}.json"
    [ -f "$j" ] && python3 -c "
import json
d=json.load(open('$j'))
rd=d.get('registers_descent','?')
fv=d.get('final_val_ce_pooled','?')
lr=d.get('mean_l_recomb','—')
print(f'  ${arm}/seed${sd}: descent={rd} pooled_val_ce={fv} l_recomb={lr}')
" 2>/dev/null || echo "  ${arm}/seed${sd}: json missing"
  done
done

echo ""
echo "G1 composed_distinct (DECISION TEST: op_obj > op_plaince AND op_obj > obj_only):"
for arm in op_plaince obj_only op_obj; do
  for sd in 7 4302 4303; do
    g="$CKPT_DIR/${arm}_seed${sd}.g0g6.txt"
    if [ -f "$g" ]; then
      g0=$(grep -i "G0\|kwr" "$g" | head -1)
      g1=$(grep -i "G1\|composed_distinct" "$g" | head -2)
      echo "  ${arm}/seed${sd}: G0: $g0 | G1: $g1"
    else
      echo "  ${arm}/seed${sd}: g0g6.txt missing"
    fi
  done
done

echo ""
echo "############ run_pod.sh DONE ($PHASE) ############"
