#!/usr/bin/env bash
# H_9311 control campaign -- 4 arms (C1 rides free on E) x seeds x grow_max {10,320}
# $0 CPU on pool hosts (summer + aiden). NO GPU, NO rent, NO spend.
#   usage: launch.sh <parallelism> <seed...>
set -u
cd "$(dirname "$0")"
P=${1:-8}; shift
ARMS=${ARMS:-"E P0X P0Y P1"}
for s in "$@"; do
  for a in $ARMS; do
    for g in 10 320; do
      [ -f "results/${a}_s${s}_g${g}.json" ] && continue     # idempotent: skip finished runs
      echo "$a $s $g"
    done
  done
done | xargs -P "$P" -L1 bash -c 'python3 growth_pedestal_arms.py run $0 $1 $2 >> results/run.log 2>&1'
echo "ALL_DONE $(hostname) $(date -Is)" >> results/run.log
