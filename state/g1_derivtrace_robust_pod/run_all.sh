#!/usr/bin/env bash
# H_9124 lever#1 derivtrace robustness — pod orchestrator.
# 5 held pairs x {DERIV,FLAT} warm-FT h1129 303M + engine-native robustness eval.
set -u
ROOT=${ROOT:-$HOME/g1robust}
BUNDLE=$ROOT/bundle
H1129=${H1129:-$ROOT/h1129.bin}
export ANIMA_SRC=$BUNDLE
cd $ROOT
mkdir -p work ckpt evals logs
PAIRS="${PAIRS:-0,1 1,2 2,3 3,4 0,3}"
GEN=40
LR=2e-5
SEED=7
STEPS="${STEPS:-2000}"       # canon default 2000; SMOKE overrides small
STEPARG=""; [ "$STEPS" != "0" ] && STEPARG="--steps $STEPS"

echo "=== H_9124 derivtrace robustness — $(date) ==="
python3 -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')" 2>&1
ls -la $H1129
echo "dict words: $(wc -l < /usr/share/dict/words 2>/dev/null || echo MISSING)"

train_one () {  # arm corpus_file out_bin log
  local arm=$1 corpus=$2 out=$3 log=$4
  echo "  [train $arm] -> $out"
  python3 $BUNDLE/cli/train.py --arch bytegpt --arm ctrl --canon $STEPARG \
      --d 1024 --L 24 --seq-len 512 --n-head 16 \
      --corpus "$corpus" --cell-label "$arm" \
      --seed $SEED --lr $LR --sample proportional --val-frac 0.05 --val-every 200 \
      --init $H1129 --out "$out" > "$log" 2>&1
  echo "    rc=$? ($(ls -la $out 2>/dev/null | awk '{print $5}') bytes)"
}

eval_one () {  # ckpt held corpus_file json log
  local ckpt=$1 held=$2 corpus=$3 json=$4 log=$5
  echo "  [eval] $ckpt held=$held"
  python3 $BUNDLE/robust_eval.py "$ckpt" --held "$held" --corpus "$corpus" \
      --gen $GEN --json "$json" > "$log" 2>&1
  echo "    rc=$?"
}

for PAIR in $PAIRS; do
  I=${PAIR%,*}; J=${PAIR#*,}
  TAG=${I}_${J}
  echo "===== PAIR {$I,$J} ====="
  WD=$ROOT/work/pair_$TAG
  mkdir -p $WD
  python3 $BUNDLE/derivtrace_corpus.py $WD $I $J $SEED > $ROOT/logs/corpus_$TAG.log 2>&1
  head -2 $ROOT/logs/corpus_$TAG.log

  train_one deriv $WD/deriv.txt $ROOT/ckpt/deriv_$TAG.bin $ROOT/logs/train_deriv_$TAG.log
  train_one flat  $WD/flat.txt  $ROOT/ckpt/flat_$TAG.bin  $ROOT/logs/train_flat_$TAG.log

  eval_one $ROOT/ckpt/deriv_$TAG.bin $PAIR $WD/deriv.txt $ROOT/evals/deriv_$TAG.json $ROOT/logs/eval_deriv_$TAG.log
  eval_one $ROOT/ckpt/flat_$TAG.bin  $PAIR $WD/flat.txt  $ROOT/evals/flat_$TAG.json  $ROOT/logs/eval_flat_$TAG.log

  echo "--- DERIV $TAG ---"; grep -E '"best_distinct"|"max_single"|"pass"|"n_novel"|"control_novel"' $ROOT/evals/deriv_$TAG.json 2>/dev/null | head
  echo "--- FLAT  $TAG ---"; grep -E '"best_distinct"|"max_single"|"pass"|"n_novel"|"control_novel"' $ROOT/evals/flat_$TAG.json 2>/dev/null | head
done

echo "=== ALL DONE $(date) ==="
python3 $BUNDLE/summarize.py $ROOT/evals > $ROOT/SUMMARY.txt 2>&1
cat $ROOT/SUMMARY.txt
touch $ROOT/DONE
