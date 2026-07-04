#!/usr/bin/env bash
# H_9127 — gamma trained-constructive-bind DATA-channel, engine-native 303M.
# 2-arm (GAMMA-DATA vs ADD content-matched control) x 3 seeds {7,4302,4303}, warm-FT
# h1129, plain-CE (ce_marginal). FROZEN BAR eval = `evaluate.py <ckpt> --gen 40` (G1).
# role-key NEVER handed at test (evaluate.py seeds plain concept phrases).
set -u
ROOT=/root/anima
WD=/root/g1_gamma
BASE=/root/h1129.bin
mkdir -p $WD/ckpt
cd $ROOT

COMMON="--canon --arch bytegpt --arm ctrl --objective ce_marginal \
  --d 1024 --L 24 --seq-len 512 --n-head 16 --init $BASE \
  --steps 1500 --lr 2e-5 --batch-size 8 --sample proportional \
  --val-frac 0.05 --val-every 300"

echo "###### GPU at start ######"; date
nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>&1 || echo "no nvidia-smi"
python3 -c "import torch;print('cuda',torch.cuda.is_available(),torch.cuda.get_device_name(0) if torch.cuda.is_available() else '')" 2>&1

# base h1129 reference G1 (context: what warm-FT moves from)
echo "###### [BASE] eval h1129 reference (gen40) ######"; date
python3 cli/evaluate.py $BASE --gen 40 > $WD/base_eval.txt 2>&1; echo "BASE_EVAL_RC=$?"
grep -E "G0 |G1 |best_distinct|max_single" $WD/base_eval.txt | head

run_one () {  # $1=arm(gamma|add) $2=corpus $3=seed
  local arm=$1 corpus=$2 seed=$3
  local tag=${arm}_s${seed}
  echo "###### TRAIN $tag ######"; date
  python3 cli/train.py $COMMON --seed $seed --corpus $ROOT/$corpus \
    --out $WD/ckpt/$tag.bin --gauges-out $WD/ckpt/${tag}_train.json > $WD/${tag}_train.log 2>&1
  echo "${tag}_TRAIN_RC=$?"; tail -4 $WD/${tag}_train.log
  echo "###### EVAL $tag (engine-native gen40) ######"; date
  python3 cli/evaluate.py $WD/ckpt/$tag.bin --gen 40 > $WD/${tag}_eval.txt 2>&1
  echo "${tag}_EVAL_RC=$?"
  grep -E "G0 COHERENCE|G1 RECOMBINATION|best_distinct|max_single|kwr" $WD/${tag}_eval.txt | head
  sha256sum $WD/ckpt/$tag.bin >> $WD/ckpt/SHA256.txt 2>&1
}

for seed in 7 4302 4303; do
  run_one gamma gamma_data.txt $seed
  run_one add   add.txt        $seed
done

echo "###### SUMMARY ######"; date
for f in $WD/*_eval.txt; do
  echo "== $f =="
  grep -E "G0 COHERENCE|G1 RECOMBINATION|best_distinct=|max_single=" "$f" | head -4
done
echo "###### SHA ######"; cat $WD/ckpt/SHA256.txt
ls -la $WD/ckpt/
echo "###### ALL_DONE ######"; date
