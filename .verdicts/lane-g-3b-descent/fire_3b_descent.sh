#!/usr/bin/env bash
# ── Lane-G 3B forge descent — campaign rung A-1 ───────────────────────────────
# substrate=GPU (Lane G) · forge flame · a_train_flame_forge (GPU REQUIRED, no CPU
# fallback) · a_scale_honest_scope (3B = a rung, bounded N, util-RED honest).
# Uses the warm byte-identical lever-4/5 clm_prod build (3-GATE PASS verified).
#
# CLMConvMoE param formula (single-block, V=256 K=3):
#   params ≈ 2*(256*d) + 2*(d^2*3) + E*d + E*(d^2*3) ≈ (2+E)*3*d^2 + ...
# forge fp64 4-copy (W+grad+m+v) + per-expert qcache → ~3B (d=15811,E=2) needs
# ~169GB > 80GB. So we PROBE the true-3B-dim allocation (records exact OOM
# ceiling) THEN fire the largest H100-80GB-feasible descent rung as the artifact.
set -u
exec > /root/fire_3b_descent.log 2>&1
echo "=== LANE-G 3B DESCENT FIRE START $(date -u +%FT%TZ) ==="
REPO=/root/hexa-lang
export PATH="/usr/local/cuda-12.4/bin:$PATH"; export CUDA_HOME=/usr/local/cuda-12.4
CLM=$REPO/clm_prod
CORPUS=/root/clm_mid_5lang_c4.txt
[ -f "$CORPUS" ] || CORPUS="$REPO/stdlib/flame/testdata/clm_mid_5lang_c4.txt"
echo "clm_prod=$(ls -la $CLM | awk '{print $5}')B  corpus=$CORPUS ($(wc -c < $CORPUS)B)"
nvidia-smi --query-gpu=name,compute_cap,memory.total --format=csv,noheader | head -1

fire_cfg () {
  local TAG="$1" D="$2" T="$3" E="$4" NS="$5" EP="$6" TIMEOUT="$7"
  echo ""
  echo "############ CONFIG $TAG : d=$D T=$T E=$E nsamp=$NS epochs=$EP (~$(python3 -c "print(round(((2+$E)*3*$D*$D+2*256*$D+$E*$D)/1e9,3))")B params) ############"
  pkill -f clm_prod 2>/dev/null; pkill -f "nvidia-smi --query-gpu=utilization" 2>/dev/null; sleep 1
  local SAMP=/root/util_3b_${TAG}.csv; rm -f "$SAMP"
  local MEM=/root/mem_3b_${TAG}.csv; rm -f "$MEM"
  local OUT=/root/clm_3b_${TAG}.clm
  local TLOG=/root/train_3b_${TAG}.log
  nohup bash -c 'while true; do nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits -i 0 2>/dev/null; sleep 0.1; done' > "$SAMP" 2>/dev/null &
  local SPID=$!
  nohup bash -c 'while true; do nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i 0 2>/dev/null; sleep 0.5; done' > "$MEM" 2>/dev/null &
  local MPID=$!
  local t0=$(date +%s)
  timeout "$TIMEOUT" env CLM_PROD_D=$D CLM_PROD_T=$T CLM_PROD_E=$E CLM_PROD_NSAMP=$NS CLM_PROD_EPOCHS=$EP \
    CLM_PROD_CORPUS="$CORPUS" CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1 CLM_PROD_OUT="$OUT" \
    HEXA_CUDA_LINK=1 "$CLM" > "$TLOG" 2>&1
  local RC=$?
  local t1=$(date +%s)
  kill $SPID $MPID 2>/dev/null
  echo "FIRE_RC=$RC  tag=$TAG  wall=$((t1-t0))s"
  python3 - "$SAMP" "$MEM" "$TAG" <<'PY'
import sys
samp,mem,tag=sys.argv[1],sys.argv[2],sys.argv[3]
vals=[int(l) for l in open(samp) if l.strip().isdigit()]
mvals=[int(l) for l in open(mem) if l.strip().isdigit()] if True else []
try: mvals=[int(l) for l in open(mem) if l.strip().isdigit()]
except: mvals=[]
if vals:
    n=len(vals); ge20=sum(1 for v in vals if v>=20); ge50=sum(1 for v in vals if v>=50)
    print(f"UTIL[{tag}] n={n} PEAK={max(vals)}% MEAN={sum(vals)/n:.4f}% busy_ge20={ge20} pct_ge20={100*ge20/n:.2f}% pct_ge50={100*ge50/n:.2f}%")
else: print(f"UTIL[{tag}] n=0")
if mvals: print(f"DEVMEM[{tag}] peak_used={max(mvals)}MiB")
PY
  echo "--- descent[$TAG] ---"
  grep -E "epoch-1 mean CE|epoch-.* mean CE|F-CLM-PROD-DESCENT|PASS|FAIL|wrote|corpus:|windows:|out of memory|bad_alloc|cannot allocate" "$TLOG" | tail -12
  echo "--- ckpt[$TAG] ---"
  ls -la "$OUT" 2>&1 | tail -1; sha256sum "$OUT" 2>/dev/null
}

# PROBE: true-3B-dim allocation (d=15811 E=2 ~3.0B). Expect OOM on 80GB fp64 —
# records the exact ceiling honestly (short timeout, 1 step).
fire_cfg probe3B 15811 8 2 2 1 120

# A-1 PRIMARY: largest H100-80GB-feasible forge fp64 rung, bounded N≈400 steps.
# d=3840 E=32 ≈ 1.51B params (max feasible under ~74GB). DESCENT axis rung.
fire_cfg a1_1p5b 3840 256 32 16 16 2400

echo ""
echo "=== LANE-G 3B DESCENT FIRE DONE $(date -u +%FT%TZ) ==="
