#!/bin/bash
# H_1393 fresh-process per-frame G6 FALS re-score driver. Each frame = its OWN hexa process
# (exit resets the bump-allocator leak), so the full 23-frame re-score COMPLETES on the 303M
# ConvMoE. Aggregates the FALS counts + applies the FROZEN M1-M5 bars (VERBATIM, no bar moved).
cd "$(dirname "$0")/../.."   # repo root
PROBE=state/1393_convmoe_streaming_decode/g6_one_frame_fresh.hexa
OUT=state/1393_convmoe_streaming_decode/g6_fresh_frames.log
: > "$OUT"
GEN=110
run_arm () {  # $1=arm  $2=nframes
  local arm=$1 n=$2 i=0
  while [ $i -lt $n ]; do
    ARM=$arm IDX=$i GEN=$GEN hexa run "$PROBE" 2>&1 | grep -E "^FRAME " | tee -a "$OUT"
    i=$((i+1))
  done
}
echo "### C_strong" | tee -a "$OUT";  run_arm C_strong 6
echo "### B_composed" | tee -a "$OUT"; run_arm B_composed 5
echo "### C_shuffle" | tee -a "$OUT";  run_arm C_shuffle 6
echo "### C_ablate" | tee -a "$OUT";   run_arm C_ablate 6
echo "ALL_FRAMES_DONE" | tee -a "$OUT"
