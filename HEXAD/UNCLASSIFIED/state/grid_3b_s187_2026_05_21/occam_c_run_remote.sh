#!/bin/bash
# Launch OCCAM-C sweep on ubu-1 as nohup background job.

set -eu

CKPT=~/occam_c/vJ/ckpt_s187_3b_J.pt
OUT=~/occam_c/vJ/occam_c_sweep_results.json
LOG=~/occam_c/vJ/occam_c_sweep.log
SCRIPT=~/occam_c/vJ/occam_c_decode_sweep.py

cd ~/occam_c/vJ

echo "[run_remote] starting sweep at $(date)" | tee -a "$LOG"
echo "[run_remote] ckpt=$CKPT" | tee -a "$LOG"
echo "[run_remote] out=$OUT" | tee -a "$LOG"

nohup python3 -u "$SCRIPT" "$CKPT" "$OUT" >> "$LOG" 2>&1 &
PID=$!
echo "$PID" > occam_c_sweep.pid
echo "[run_remote] launched pid=$PID" | tee -a "$LOG"
echo "[run_remote] tail -f $LOG to monitor" | tee -a "$LOG"
