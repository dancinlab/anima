#!/usr/bin/env bash
# pod_run.sh — drive H_1640/1641 binding-mouth 303M trainings + H_1602 G0-G6 eval on a CUDA pod.
# Run ON THE POD after `~/anima/` is rsynced + corpus present. Detached-friendly (nohup).
set -u
cd ~/anima || exit 1
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
CORPUS="state/clm303_clean_corpus/gen_ko.txt state/clm303_clean_corpus/gen_en.txt state/clm303_clean_corpus/sns_ko.txt state/clm303_clean_corpus/sns_en.txt"
LBL="ko-general en-general ko-sns en-sns"
PHASE="${1:-all}"

H1640=state/binding_arch_census/h1640_hamiltonian
H1641=state/binding_arch_census/h1641_laminar
mkdir -p $H1640/ckpt $H1641/ckpt state/binding_arch_census/h1602_eval

py() { python3 "$@"; }

train_full() {  # $1=trainer $2=arm $3=seed $4=outdir
  local tr=$1 arm=$2 sd=$3 od=$4
  echo "=== TRAIN $tr arm=$arm seed=$sd ==="
  py "$tr" --arm "$arm" --seed "$sd" --corpus $CORPUS --cell-label $LBL \
    --canon --steps 2000 --seq-len 1024 --batch-size 8 --e0 2 --emax 3 \
    --val-frac 0.05 --val-every 200 --sample proportional --bf16 \
    --out "$od/${arm}_seed${sd}.clm" --ckpt-out "$od/${arm}_seed${sd}.pt" \
    --gauges-out "$od/${arm}_seed${sd}.json" > "$od/${arm}_seed${sd}.train.log" 2>&1
  echo "  RC=$? -> $od/${arm}_seed${sd}.clm"
}

descent() {  # $1=clm
  echo "--- DESCENT $1 ---"
  py train/clm/model/verify_clm_v2.py descent "$1" \
    state/clm303_clean_corpus/gen_ko.txt 2>&1 | grep -iE "DESCENT|model_ce|uniform|shuffle|overfit" | head
}

eval_g0g6() {  # $1=clm $2=outtxt
  echo "=== EVAL G0-G6 $1 ==="
  PYTHONPATH=core:cli:train/clm/model py cli/evaluate.py "$1" --corpus $CORPUS --gen 80 \
    > "$2" 2>&1
  echo "  RC=$? -> $2"
  grep -E "G0|G1|G2|G6|CLOSURE" "$2" | head
}

# ───────────────────────── SMOKE (tiny, RC gate) ─────────────────────────────
if [ "$PHASE" = smoke ] || [ "$PHASE" = all ]; then
  echo "############ SMOKE ############"
  for trpair in "$H1640/trainer.py:arm" "$H1641/trainer.py:arm"; do
    tr="${trpair%%:*}"; arm="${trpair##*:}"
    echo "--- smoke $tr ---"
    py "$tr" --arm "$arm" --seed 7 --corpus $CORPUS --cell-label $LBL \
      --d 16 --L 1 --steps 30 --seq-len 64 --batch-size 4 --e0 2 --emax 3 \
      --val-frac 0.05 --val-every 30 --sample proportional \
      --out /tmp/sm_${arm}.clm --ckpt-out /tmp/sm_${arm}.pt --gauges-out /tmp/sm_${arm}.json 2>&1 | tail -8
    echo "  smoke RC=$?"
  done
  [ "$PHASE" = smoke ] && exit 0
fi

# ───────────────────── H_1640 full (9 arms) ──────────────────────────────────
if [ "$PHASE" = h1640 ] || [ "$PHASE" = all ]; then
  echo "############ H_1640 HAMILTONIAN ############"
  for arm in arm ctrl diss; do for sd in 7 4302 4303; do
    train_full "$H1640/trainer.py" "$arm" "$sd" "$H1640/ckpt"
    descent "$H1640/ckpt/${arm}_seed${sd}.clm"
    eval_g0g6 "$H1640/ckpt/${arm}_seed${sd}.clm" "$H1640/ckpt/${arm}_seed${sd}.g0g6.txt"
  done; done
fi

# ───────────────────── H_1641 full (9 arms) ──────────────────────────────────
if [ "$PHASE" = h1641 ] || [ "$PHASE" = all ]; then
  echo "############ H_1641 LAMINAR ############"
  for arm in arm nofb noln; do for sd in 7 4302 4303; do
    train_full "$H1641/trainer.py" "$arm" "$sd" "$H1641/ckpt"
    descent "$H1641/ckpt/${arm}_seed${sd}.clm"
    eval_g0g6 "$H1641/ckpt/${arm}_seed${sd}.clm" "$H1641/ckpt/${arm}_seed${sd}.g0g6.txt"
  done; done
fi

# ───────────────────── H_1602 G0-G6 engine-native (9 existing clms) ──────────
if [ "$PHASE" = h1602 ] || [ "$PHASE" = all ]; then
  echo "############ H_1602 G0-G6 (existing clms) ############"
  WD=state/binding_arch_census/h1602_eval
  for f in ~/anima-weights/recomb_obj_303m/*.clm state/h1602_clm/*.clm; do
    [ -f "$f" ] || continue
    b=$(basename "$f" .clm)
    descent "$f"
    eval_g0g6 "$f" "$WD/${b}.g0g6.txt"
  done
fi
echo "############ pod_run.sh DONE ($PHASE) ############"
