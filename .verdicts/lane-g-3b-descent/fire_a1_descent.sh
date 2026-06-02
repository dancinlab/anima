#!/usr/bin/env bash
# ── Lane-G rung A-1 DESCENT — forge ~1B descent rung (E=2 proven-descend family) ─
# The E=32 ~1.5B run showed util-RED (workload-bound) cleanly but did NOT descend
# in 16 steps (epoch-1 4.645 -> epoch-2 4.885, F=0) — too few steps. This rung
# uses the lever-chain's proven E=2 descend family at d=9216 (~1.02B, fits 58GB)
# with enough bounded steps for CE to actually descend. DESCENT axis (a_scale_honest_scope);
# util RED expected/recorded. E=2 steps are far cheaper than E=32 so N can be larger.
set -u
exec > /root/fire_a1_descent.log 2>&1
echo "=== A-1 DESCENT FIRE START $(date -u +%FT%TZ) ==="
REPO=/root/hexa-lang
export PATH="/usr/local/cuda-12.4/bin:$PATH"; export CUDA_HOME=/usr/local/cuda-12.4
CLM=$REPO/clm_prod
CORPUS=/root/clm_mid_5lang_c4.txt
nvidia-smi --query-gpu=name,compute_cap,memory.total --format=csv,noheader | head -1
TAG=a1desc; D=9216; T=256; E=2; NS=16; EP=6
OUT=/root/clm_3b_${TAG}.clm; TLOG=/root/train_3b_${TAG}.log
SAMP=/root/util_3b_${TAG}.csv; MEM=/root/mem_3b_${TAG}.csv; rm -f "$SAMP" "$MEM"
echo "############ $TAG : d=$D T=$T E=$E nsamp=$NS epochs=$EP (~$(python3 -c "print(round(((2+$E)*3*$D*$D+2*256*$D+$E*$D)/1e9,3))")B params, $((EP*NS)) steps) ############"
nohup bash -c 'while true; do nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits -i 0 2>/dev/null; sleep 0.1; done' > "$SAMP" 2>/dev/null & SPID=$!
nohup bash -c 'while true; do nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i 0 2>/dev/null; sleep 0.5; done' > "$MEM" 2>/dev/null & MPID=$!
t0=$(date +%s)
env CLM_PROD_D=$D CLM_PROD_T=$T CLM_PROD_E=$E CLM_PROD_NSAMP=$NS CLM_PROD_EPOCHS=$EP \
  CLM_PROD_CORPUS="$CORPUS" CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1 CLM_PROD_OUT="$OUT" \
  HEXA_CUDA_LINK=1 "$CLM" > "$TLOG" 2>&1
RC=$?; t1=$(date +%s); kill $SPID $MPID 2>/dev/null
echo "FIRE_RC=$RC wall=$((t1-t0))s"
python3 - "$SAMP" "$MEM" "$TAG" <<'PY'
import sys; samp,mem,tag=sys.argv[1],sys.argv[2],sys.argv[3]
v=[int(l) for l in open(samp) if l.strip().isdigit()]
m=[int(l) for l in open(mem) if l.strip().isdigit()]
if v: print(f"UTIL[{tag}] n={len(v)} PEAK={max(v)}% MEAN={sum(v)/len(v):.4f}% pct_ge20={100*sum(1 for x in v if x>=20)/len(v):.2f}% pct_ge50={100*sum(1 for x in v if x>=50)/len(v):.2f}%")
if m: print(f"DEVMEM[{tag}] peak_used={max(m)}MiB")
PY
echo "--- descent[$TAG] ---"
grep -E "mean CE|F-CLM-PROD-DESCENT|PASS|FAIL|wrote|windows:" "$TLOG"
echo "--- ckpt[$TAG] ---"; ls -la "$OUT" 2>&1 | tail -1; sha256sum "$OUT" 2>/dev/null
echo "=== A-1 DESCENT DONE $(date -u +%FT%TZ) ==="
