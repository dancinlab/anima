#!/bin/bash
# H_1814/1632 N4+N8 303M matrix runner — runs on summer pool GPU (RTX 5070, grad-checkpoint).
# spine = 4 arms seed7; robustness = key arms (n8_jamo/G1, n4_set/G6) on seeds 4302,4303.
set -u
cd ~/anima_1632/state/1632_g6setsearch_g1jamo
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUDA_VISIBLE_DEVICES=0
C="../clm303_clean_corpus/gen_ko.txt ../clm303_clean_corpus/gen_en.txt ../clm303_clean_corpus/sns_ko.txt ../clm303_clean_corpus/sns_en.txt"
L="ko-general en-general ko-sns en-sns"
run(){ arm=$1; seed=$2
  echo "[$(date +%H:%M:%S)] START arm=$arm seed=$seed"
  python3 -u trainer.py --arm "$arm" --seed "$seed" --canon --grad-checkpoint \
    --corpus $C --cell-label $L --sample proportional \
    --steps 2000 --val-frac 0.05 --val-every 500 --bf16 \
    --out "ckpt/${arm}_seed${seed}.clm" --ckpt-out "ckpt/${arm}_seed${seed}.pt" \
    --gauges-out "ckpt/${arm}_seed${seed}.json" > "ckpt/${arm}_seed${seed}.log" 2>&1
  rc=$?
  echo "[$(date +%H:%M:%S)] DONE arm=$arm seed=$seed rc=$rc clm=$(stat -c%s "ckpt/${arm}_seed${seed}.clm" 2>/dev/null)"
}
for arm in baseline n8_jamo n4_set n4n8_both; do run "$arm" 7; done
for seed in 4302 4303; do run n8_jamo "$seed"; run n4_set "$seed"; done
echo "[$(date +%H:%M:%S)] ALL_RUNS_COMPLETE"
