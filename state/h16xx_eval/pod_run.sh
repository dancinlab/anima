#!/usr/bin/env bash
# pod_run.sh — drive H_1620/1630/1631/1632 binding-mouth 303M trainings + G0-G6 eval on a CUDA pod.
# Run ON THE POD after ~/anima/ is rsynced + corpus present. Detached-friendly (nohup).
#   phases: smoke | h1620 | h1630 | h1631 | h1632 | eval | all
set -u
cd ~/anima || exit 1
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8
CORPUS="state/clm303_clean_corpus/gen_ko.txt state/clm303_clean_corpus/gen_en.txt state/clm303_clean_corpus/sns_ko.txt state/clm303_clean_corpus/sns_en.txt"
LBL="ko-general en-general ko-sns en-sns"
PHASE="${1:-all}"

declare -A TR ARMS
TR[1620]=state/h1620_hopfield_mouth/trainer.py;  ARMS[1620]="arm k1 asym"
TR[1630]=state/h1630_tropical_mouth/trainer.py;  ARMS[1630]="arm soft mid"
TR[1631]=state/h1631_sheaf_mouth/trainer.py;     ARMS[1631]="arm ident k1"
TR[1632]=state/h1632_galois_mouth/trainer.py;    ARMS[1632]="arm orpool k1"
declare -A OD
OD[1620]=state/h1620_hopfield_mouth/ckpt
OD[1630]=state/h1630_tropical_mouth/ckpt
OD[1631]=state/h1631_sheaf_mouth/ckpt
OD[1632]=state/h1632_galois_mouth/ckpt
SEEDS="7 4302 4303"
mkdir -p ${OD[1620]} ${OD[1630]} ${OD[1631]} ${OD[1632]} state/h16xx_eval

py() { python3 "$@"; }

train_full() {  # $1=hid $2=arm $3=seed
  local hid=$1 arm=$2 sd=$3 tr=${TR[$1]} od=${OD[$1]}
  echo "=== TRAIN H_$hid $tr arm=$arm seed=$sd ==="
  py "$tr" --arm "$arm" --seed "$sd" --corpus $CORPUS --cell-label $LBL \
    --canon --steps 2000 --seq-len 1024 --batch-size 8 --e0 2 --emax 3 \
    --val-frac 0.05 --val-every 200 --sample proportional --bf16 \
    --out "$od/${arm}_seed${sd}.clm" --ckpt-out "$od/${arm}_seed${sd}.pt" \
    --gauges-out "$od/${arm}_seed${sd}.json" > "$od/${arm}_seed${sd}.train.log" 2>&1
  echo "  RC=$? -> $od/${arm}_seed${sd}.clm"
  tail -3 "$od/${arm}_seed${sd}.train.log"
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
  grep -E "G0|G1|G2|G6|CLOSURE|composed|distinct" "$2" | head -20
}

# ───────────────────────── SMOKE (tiny, RC gate) ─────────────────────────────
if [ "$PHASE" = smoke ] || [ "$PHASE" = all ]; then
  echo "############ SMOKE ############"
  for hid in 1620 1630 1631 1632; do
    arm=$(echo ${ARMS[$hid]} | awk '{print $1}')
    echo "--- smoke H_$hid (${TR[$hid]}) arm=$arm ---"
    py "${TR[$hid]}" --arm "$arm" --seed 7 --corpus $CORPUS --cell-label $LBL \
      --d 16 --L 1 --steps 30 --seq-len 64 --batch-size 4 --e0 2 --emax 3 \
      --val-frac 0.05 --val-every 30 --sample proportional \
      --out /tmp/sm_${hid}.clm --gauges-out /tmp/sm_${hid}.json 2>&1 | tail -8
    echo "  smoke H_$hid RC=$?"
  done
  [ "$PHASE" = smoke ] && exit 0
fi

# ───────────────────── full trainings (9 arms each) ──────────────────────────
for hid in 1620 1630 1631 1632; do
  if [ "$PHASE" = "h$hid" ] || [ "$PHASE" = all ]; then
    echo "############ H_$hid FULL ############"
    for arm in ${ARMS[$hid]}; do for sd in $SEEDS; do
      train_full "$hid" "$arm" "$sd"
      descent "${OD[$hid]}/${arm}_seed${sd}.clm"
    done; done
  fi
done

# ───────────────────────── G0-G6 eval (arm seed 7 first; then all) ───────────
if [ "$PHASE" = eval ] || [ "$PHASE" = all ]; then
  echo "############ G0-G6 EVAL ############"
  for hid in 1620 1630 1631 1632; do
    for arm in ${ARMS[$hid]}; do for sd in $SEEDS; do
      clm="${OD[$hid]}/${arm}_seed${sd}.clm"
      [ -f "$clm" ] && eval_g0g6 "$clm" "state/h16xx_eval/H${hid}_${arm}_seed${sd}.g0g6.txt"
    done; done
  done
fi
echo "ALL DONE phase=$PHASE"
