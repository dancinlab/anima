#!/usr/bin/env bash
# H_6186 engine-native fals_bound via PER-FRAME process isolation (54 processes).
# Each (arm,seed,frame) is one hexa-run process (k=3 decodes ~8GB) that EXITS -> GPU frees.
set -uo pipefail
source /workspace/cudaenv.sh
cd /workspace/anima
OUT=/workspace/g6_frame_out; mkdir -p "$OUT"
declare -A CK=( [base]=/workspace/ckpt/h1129.bin [targeted]=/workspace/ckpt/g6tc_targeted.bin [shuf]=/workspace/ckpt/g6tc_shuf.bin )
SEEDS="7 4302 4303"; FRAMES="0 1 2 3 4 5"
echo "=== preflight cuda ==="; hexa run /tmp/ck.hexa 2>&1 | tail -1
for arm in base targeted shuf; do
  for s in $SEEDS; do
    for fi in $FRAMES; do
      tag="${arm}_${s}_${fi}"
      ( for i in $(seq 1 40); do nvidia-smi --query-gpu=memory.used --format=csv,noheader; sleep 5; done ) > "$OUT/${tag}.smi" 2>&1 &
      SMIPID=$!
      hexa run cli/g6_frame_probe.hexa -- "${CK[$arm]}" "$arm" "$s" "$fi" > "$OUT/${tag}.out" 2>"$OUT/${tag}.err"
      RC=$?
      kill $SMIPID 2>/dev/null
      PEAK=$(sort -t, -k1 -n "$OUT/${tag}.smi" 2>/dev/null | tail -1)
      OG=$(grep -c OWN-GEMM "$OUT/${tag}.err" 2>/dev/null)
      FB=$(grep -o 'fb=[0-9]' "$OUT/${tag}.out" 2>/dev/null | tail -1)
      K=$(grep -c Killed "$OUT/${tag}.err" 2>/dev/null)
      echo "=== $tag rc=$RC peak=[$PEAK] og=$OG $FB killed=$K $(date -u +%H:%M:%S) ==="
      sleep 1
    done
  done
done
echo "=== ALL 54 FRAMES DONE ==="
grep -h FRAMEBOUND "$OUT"/*.out 2>/dev/null
