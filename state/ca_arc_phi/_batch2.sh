#!/bin/bash
cd /Users/mini/dancinlab/anima/.worktrees/ca-arc
D=state/ca_arc_phi
for h in 300 302 303 301 304 299; do
  echo "[b2] running H_$h @ $(date +%H:%M:%S)"
  hexa run $D/run_h${h}.hexa > $D/out_h${h}.log 2>&1
  echo "[b2] H_$h rc=$? @ $(date +%H:%M:%S)"
done
echo "DONE @ $(date +%H:%M:%S)" > $D/_batch2_done.txt
