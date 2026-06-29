#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════
#  H_1824 — compositional-data-coverage THRESHOLD (G1, orthogonal family #1).
#
#  3 density VARIANTS (LOW/MID/HIGH) × 2 SEEDS {7,4302} = 6 runs.
#  Each: cli/train.py --canon (303M CLMConvMoE, L4·d3784·E2->Emax3) --steps 4000.
#  proportional sampling + held-out val (4/4 DESCENT overfit guard) + bf16.
#  Then engine-native-py G0-G6 (cli/evaluate.py --gen 80).
#
#  FROZEN DECISION TEST (pre-registered, p7 no tune-to-green):
#    G1 composed_distinct >=2 ∧ >max_single ∧ coherent on >=2/3  per variant,
#    AND MONOTONE G1(LOW) < G1(MID) < G1(HIGH).  4/4 register DESCENT required
#    for a valid verdict (else overfit -> void).
#
#  USAGE (on pod after ~/anima/ synced + variants built):
#    bash ~/anima/state/g1_coverage_threshold/run_pod.sh [smoke|train|eval|all]
# ════════════════════════════════════════════════════════════════════════════
set -uo pipefail
cd ~/anima || { echo "FATAL: ~/anima not found"; exit 1; }
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
export PYTHONPATH=core:cli:train/clm/model

LANE="state/g1_coverage_threshold"
VARDIR="$LANE/variants"
CKPT_DIR="$LANE/ckpt"
TRAINER="cli/train.py"
LBL="ko-general en-general ko-sns en-sns"
PHASE="${1:-all}"
mkdir -p "$CKPT_DIR"

variant_corpus() {  # $1=VARIANT -> echoes the 4 cell paths
  local v=$1
  echo "$VARDIR/$v/gen_ko.txt $VARDIR/$v/gen_en.txt $VARDIR/$v/sns_ko.txt $VARDIR/$v/sns_en.txt"
}

N_GPU=$(python3 -c "import torch; print(torch.cuda.device_count())" 2>/dev/null || echo 0)
echo "  [init] N_GPU=${N_GPU}  PHASE=${PHASE}"

check_corpus() {
  echo "  [corpus-check] variant byte counts:"
  for v in LOW MID HIGH; do
    for f in $(variant_corpus "$v"); do
      if [ -f "$f" ]; then echo "    $(wc -c < "$f") bytes — $f"
      else echo "    MISSING: $f  FATAL"; exit 1; fi
    done
  done
}

train_run() {  # $1=VARIANT $2=seed $3=gpu
  local v=$1 sd=$2 gpu=${3:-0}
  local base="$CKPT_DIR/${v}_seed${sd}"
  local corpus; corpus=$(variant_corpus "$v")
  echo "=== TRAIN variant=${v} seed=${sd} GPU=${gpu} ===" | tee -a /tmp/cov_train.log
  # cli/train.py uses a fixed seed (42) internally; vary via PYTHONHASHSEED + a
  # per-seed env the trainer reads (we pass --lr unchanged, seed via TORCH seed).
  CUDA_VISIBLE_DEVICES="${gpu}" ANIMA_SEED="${sd}" python3 "$TRAINER" \
    --out "${base}.clm" --ckpt-out "${base}.pt" \
    --corpus $corpus --cell-label $LBL --require-cells 4 \
    --canon --steps 4000 --seq-len 1024 --batch-size 8 \
    --e0 2 --emax 3 --sample proportional --bf16 \
    --val-frac 0.05 --val-every 200 --log-every 100 \
    --min-corpus-bytes 1000000 \
    > "${base}.train.log" 2>&1
  local rc=$?
  echo "  RC=${rc}  -> ${base}.clm" | tee -a /tmp/cov_train.log
  grep -E "FINAL val_CE|registers_DESCENT|DESCENT|NO-DESCENT|clm_decodable|PASS —|FAIL —" \
    "${base}.train.log" | tail -12 | tee -a /tmp/cov_train.log
  return $rc
}

eval_g0g6() {  # $1=VARIANT $2=seed
  local v=$1 sd=$2
  local clm="$CKPT_DIR/${v}_seed${sd}.clm"
  local out="$CKPT_DIR/${v}_seed${sd}.g0g6.txt"
  local corpus; corpus=$(variant_corpus "$v")
  if [ ! -f "$clm" ]; then echo "  SKIP $clm (not found)"; return 0; fi
  echo "=== EVAL G0-G6 ${v} seed${sd} ===" | tee -a /tmp/cov_eval.log
  python3 cli/evaluate.py "$clm" --corpus $corpus --gen 80 > "$out" 2>&1
  echo "  RC=$? -> ${out}" | tee -a /tmp/cov_eval.log
  grep -E "G0 |G1 |G2 |G6 |CLOSURE|best_distinct|max_single|falsifiable" "$out" \
    | head -20 | tee -a /tmp/cov_eval.log
  return 0
}

# ── SMOKE: tiny, checks imports + variant load + serialize + DESCENT machinery ─
if [ "$PHASE" = smoke ] || [ "$PHASE" = all ]; then
  echo "############ SMOKE ############"
  corpus=$(variant_corpus MID)
  python3 "$TRAINER" --out /tmp/cov_sm.clm --ckpt-out /tmp/cov_sm.pt \
    --corpus $corpus --cell-label $LBL --require-cells 4 \
    --steps 4 --seq-len 128 --batch-size 4 --e0 2 --emax 2 \
    --val-frac 0.1 --val-every 4 --log-every 2 --sample proportional 2>&1 | tail -16
  echo "  smoke RC=$?"
  python3 -c "
import sys; sys.path.insert(0,'core')
import clm_decode as cd
W = cd.clm_load_weights('/tmp/cov_sm.clm')
print('  smoke clm_load_weights ok=', W.get('ok', False))
assert W.get('ok', False), 'FATAL: not decodable'
print('  CLMB/CORE-loadable OK')
" 2>&1
  [ "$PHASE" = smoke ] && { echo "  SMOKE DONE"; exit 0; }
fi

# ── TRAIN: 3 variants × 2 seeds ───────────────────────────────────────────────
if [ "$PHASE" = train ] || [ "$PHASE" = all ]; then
  check_corpus
  echo "############ TRAINING (3 variants × 2 seeds, 4000 steps) ############"
  for sd in 7 4302; do
    echo "====== SEED ${sd} ======"
    if [ "$N_GPU" -ge 2 ]; then
      ( train_run LOW "$sd" 0; train_run HIGH "$sd" 0 ) &  pid0=$!
      train_run MID "$sd" 1 &  pid1=$!
      wait $pid0 || echo "WARN GPU0 seed${sd}"; wait $pid1 || echo "WARN GPU1 seed${sd}"
    else
      train_run LOW  "$sd" 0 || echo "WARN LOW seed${sd}"
      train_run MID  "$sd" 0 || echo "WARN MID seed${sd}"
      train_run HIGH "$sd" 0 || echo "WARN HIGH seed${sd}"
    fi
    echo "  seed ${sd} done — ckpts: $(ls -1 ${CKPT_DIR}/*.clm 2>/dev/null | wc -l)/6"
  done
  echo "############ TRAINING COMPLETE ############"
fi

# ── EVAL: G0-G6 on all 6 .clm ─────────────────────────────────────────────────
if [ "$PHASE" = eval ] || [ "$PHASE" = all ]; then
  echo "############ G0-G6 EVAL (engine-native-py, gen=80) ############"
  for v in LOW MID HIGH; do for sd in 7 4302; do eval_g0g6 "$v" "$sd"; done; done
  echo "############ G0-G6 EVAL COMPLETE ############"
fi

# ── SUMMARY: monotonicity decision test ───────────────────────────────────────
echo ""
echo "############ SUMMARY — DECISION TEST (G1 LOW<MID<HIGH) ############"
for v in LOW MID HIGH; do for sd in 7 4302; do
  g="$CKPT_DIR/${v}_seed${sd}.g0g6.txt"
  if [ -f "$g" ]; then
    g0=$(grep "G0 " "$g" | head -1 | tr -s ' ')
    g1=$(grep "G1 " "$g" | head -1 | tr -s ' ')
    clo=$(grep "CLOSURE" "$g" | head -1 | tr -s ' ')
    echo "  ${v}/seed${sd}: [$g1] [$g0] [$clo]"
  else echo "  ${v}/seed${sd}: g0g6.txt MISSING"; fi
done; done
echo ""
echo "############ run_pod.sh DONE ($PHASE) ############"
