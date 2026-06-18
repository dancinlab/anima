#!/usr/bin/env bash
# ── Lane-G lever-5 SWEEP driver: workload-bound (B) disambiguation ──
# Uses cached lever-4 clm_prod (adamw_group fused, minimal host crossings).
# Apples config = EXACT lever-4 (d1536/T512/nsamp32/ep3). Larger configs use
# fewer windows/epochs so wall time stays bounded — util MEAN/PEAK is a
# steady-state per-step measure, not a convergence measure (descent still
# checked over the run). If MEAN lifts with bigger per-step work -> B.
set -u
exec > /root/lever5_sweep.log 2>&1
echo "=== LEVER-5 SWEEP START $(date -u +%FT%TZ) ==="
REPO=/root/hexa-lang
export PATH="/usr/local/cuda-12.4/bin:$PATH"; export CUDA_HOME=/usr/local/cuda-12.4
CLM=$REPO/clm_prod
CORPUS="$REPO/stdlib/flame/testdata/clm_mid_5lang_c4.txt"
[ -f "$CORPUS" ] || CORPUS="$REPO/stdlib/flame/testdata/clm_semantic_parallel.txt"
echo "clm_prod=$(ls -la $CLM | awk '{print $5}')B  corpus=$CORPUS"
nvidia-smi --query-gpu=name,compute_cap --format=csv,noheader | head -1

run_cfg () {
  local TAG="$1" D="$2" T="$3" E="$4" NS="$5" EP="$6"
  echo ""
  echo "############ CONFIG $TAG : d=$D T=$T E=$E nsamp=$NS epochs=$EP ############"
  pkill -f clm_prod 2>/dev/null; pkill -f "nvidia-smi --query-gpu=utilization" 2>/dev/null; sleep 1
  local SAMP=/root/util_lever5_${TAG}.csv; rm -f "$SAMP"
  local OUT="$REPO/exports/clm_lever5_${TAG}.clm"; mkdir -p "$REPO/exports"
  local TLOG=/root/train_lever5_${TAG}.log
  local MEMLOG=/root/mem_lever5_${TAG}.csv; rm -f "$MEMLOG"
  nohup bash -c 'while true; do nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits -i 0 2>/dev/null; sleep 0.1; done' > "$SAMP" 2>/dev/null &
  local SPID=$!
  nohup bash -c 'while true; do nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i 0 2>/dev/null; sleep 0.5; done' > "$MEMLOG" 2>/dev/null &
  local MPID=$!
  local t0=$(date +%s)
  env CLM_PROD_D=$D CLM_PROD_T=$T CLM_PROD_E=$E CLM_PROD_NSAMP=$NS CLM_PROD_EPOCHS=$EP \
    CLM_PROD_CORPUS="$CORPUS" CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1 CLM_PROD_OUT="$OUT" \
    HEXA_CUDA_LINK=1 "$CLM" > "$TLOG" 2>&1
  local RC=$?
  local t1=$(date +%s)
  kill $SPID $MPID 2>/dev/null
  echo "FIRE_RC=$RC  tag=$TAG  wall=$((t1-t0))s"
  python3 - "$SAMP" "$MEMLOG" "$TAG" <<'PY'
import sys
samp,mem,tag=sys.argv[1],sys.argv[2],sys.argv[3]
vals=[]
for l in open(samp):
    l=l.strip()
    if l.isdigit(): vals.append(int(l))
mvals=[]
try:
  for l in open(mem):
    l=l.strip()
    if l.isdigit(): mvals.append(int(l))
except: pass
if vals:
    n=len(vals); peak=max(vals); mean=sum(vals)/n
    ge20=sum(1 for v in vals if v>=20); ge50=sum(1 for v in vals if v>=50)
    print(f"UTIL[{tag}] n={n} PEAK={peak}% MEAN={mean:.4f}% busy_ge20={ge20} pct_ge20={100*ge20/n:.2f}% pct_ge50={100*ge50/n:.2f}%")
else:
    print(f"UTIL[{tag}] n=0 (no samples)")
if mvals:
    print(f"DEVMEM[{tag}] peak_used={max(mvals)}MiB min={min(mvals)}MiB")
PY
  echo "--- descent[$TAG] ---"
  grep -E "epoch-1 mean CE|mean CE|F-CLM-PROD-DESCENT|PASS|FAIL|wrote|config d=" "$TLOG" | tail -8
  echo "--- ckpt[$TAG] ---"
  ls -la "$OUT" 2>&1 | tail -1; sha256sum "$OUT" 2>/dev/null
}

# CONFIG-A apples : EXACT lever-4 (d1536/T512/nsamp32/ep3)
run_cfg apples 1536 512 2 32 3
# CONFIG-B1 d3072 : 2x model dim — ~4x per-step GEMM work; fewer windows for wall time
run_cfg d3072  3072 512 2 12 3
# CONFIG-B2 t1024 : 2x seqlen at lever-4 d — ~4x per-step GEMM work
run_cfg t1024  1536 1024 2 16 3
# CONFIG-B3 big   : d3072/T1024 — largest per-step work; minimal windows
run_cfg big    3072 1024 2 8 3

echo ""
echo "=== LEVER-5 SWEEP DONE $(date -u +%FT%TZ) ==="
