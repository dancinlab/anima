#!/bin/bash
cd /Users/mini/dancinlab/anima/.worktrees/ca-arc
D=state/ca_arc_phi
# order: fast bio first, then ECA sweeps (306-310 fast; 300,301,302,303,311 medium; 299,304 slow)
for h in 306 307 308 309 310 311 300 302 303 301 299 304; do
  echo "[batch] running H_$h @ $(date +%H:%M:%S)"
  hexa run $D/run_h${h}.hexa > $D/out_h${h}.log 2>&1
  echo "[batch] H_$h rc=$? @ $(date +%H:%M:%S)"
done
echo "[batch] ALL DONE @ $(date +%H:%M:%S)" > $D/_batch_done.txt
