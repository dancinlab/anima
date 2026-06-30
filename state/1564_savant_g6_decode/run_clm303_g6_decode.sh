#!/usr/bin/env bash
# run_clm303_g6_decode.sh — engine-native G6 frozen-bar decode for clm303 (.clm 303M).
#
# LAUNCH-READY for a summer host with HEADROOM (do NOT run while rbfe + a2138 still burn
# CPU/GPU — discipline: wait until a5b39/a2138 complete; check `uptime` load + `nvidia-smi`).
# Detached (nohup) into ~/clm303_g6_gates/. Engine-native: live core/clm_decode.hexa via
# state/1564_savant_g6_decode/engine_decode_batch_clm_cli.hexa (clm_decode_batch_to_file).
#
# Prereq on host (mac→host rsync): rsync -az cli/ core/ state/1564_savant_g6_decode/ \
#   state/clm303_savant_mitosis_train/clm303.clm <host>:~/anima/...
set -euo pipefail
cd ~/anima
OUT=~/clm303_g6_gates
mkdir -p "$OUT"
CLM=~/anima/state/clm303_savant_mitosis_train/clm303.clm
JOBS=~/anima/state/1564_savant_g6_decode/jobs.tsv
CLI=~/anima/state/1564_savant_g6_decode/engine_decode_batch_clm_cli.hexa
# G6 frozen decode params (match the H_1464 bytegpt arm: gen=110, top_k=40, temp=0.700)
GEN=110; TOPK=40; TEMP_MILLI=700
echo "[$(date)] clm303 G6 decode start  gen=$GEN top_k=$TOPK temp=$(echo "$TEMP_MILLI/1000"|bc -l)"
# clm303 = TRAINED arm (savant+mitosis). No separate base/shuffle .clm yet => single-arm decode.
# (B3 cross-shuffle is computed in-driver from the TRAINED fragments; B5 vs-base needs a base
#  .clm — register as follow-on if a base clm303 ckpt is pulled.)
nohup hexa run "$CLI" -- "$CLM" "$JOBS" "$OUT/out_clm303_trained.txt" $GEN $TOPK $TEMP_MILLI \
  > "$OUT/decode.log" 2>&1 &
echo "PID=$!  log=$OUT/decode.log  out=$OUT/out_clm303_trained.txt"
