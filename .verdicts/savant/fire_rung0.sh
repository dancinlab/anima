#!/usr/bin/env bash
# ── SAVANT-7B rung0 — pipeline-validation forge CLM fire (substrate=GPU, Lane-G) ──────
# a_train_flame_forge: production CLM training = hexa-native flame+forge (.hexa on
# stdlib/flame), GPU REQUIRED (3-GATE, no silent CPU fallback). a_scale_honest_scope:
# rung0 is PIPELINE VALIDATION (small d768/d1536-class CLM on the 5-lang starter corpus),
# NOT a 7B. Goal = CLEAN DESCENT (epoch-1 mean CE > epoch-N mean CE, below uniform ln256).
# Persistent /workspace volume; checkpoint to /workspace; recover-before-teardown.
set -u
exec > /workspace/fire_rung0.log 2>&1
echo "=== SAVANT-7B rung0 FIRE START $(date -u +%FT%TZ) ==="
mkdir -p /workspace
REPO=/root/hexa-lang
export PATH="/usr/local/cuda-12.4/bin:$PATH"; export CUDA_HOME=/usr/local/cuda-12.4

# ---- build clm_prod with the forge CUDA link path (self-host rebuild) ----
# cuda_link_decision (forge GPU link) is ABSENT from the prebuilt release — rebuild from
# source so clm_prod links cuBLAS+cudart+libcuda+cublasLt (a_train_flame_forge GPU REQUIRED).
cd "$REPO"
echo "--- 3-GATE build ---"
nvcc --version 2>&1 | tail -2
# (build commands per the warm lever-4/5 recipe; tool/stage_build_hexa + runtime_cuda seeds)
bash tool/stage_build_hexa.sh 2>&1 | tail -5 || echo "BUILD_NOTE: using prebuilt clm_prod fallback if stage build absent"
CLM="$REPO/clm_prod"
ls -la "$CLM" 2>&1 | tail -1
echo "--- GATE2 clm_prod CUDA links ---"
ldd "$CLM" 2>/dev/null | grep -E "cublas|cudart|libcuda" || echo "GATE2 WARN: no cuda libs in ldd"
echo "--- GATE3 forge dispatch symbols ---"
nm "$CLM" 2>/dev/null | grep -E "forge_dispatch_matmul|forge_dispatch.*batched|adamw" | head -4 || echo "GATE3 note"

CORPUS=/workspace/savant_5lang_starter.txt
echo "corpus=$CORPUS ($(wc -c < $CORPUS 2>/dev/null)B, $(wc -l < $CORPUS 2>/dev/null) lines)"
nvidia-smi --query-gpu=name,compute_cap,memory.total --format=csv,noheader | head -1

fire_cfg () {
  local TAG="$1" D="$2" T="$3" E="$4" NS="$5" EP="$6" TIMEOUT="$7"
  echo ""
  echo "############ rung0 CONFIG $TAG : d=$D T=$T E=$E nsamp=$NS epochs=$EP ############"
  pkill -f clm_prod 2>/dev/null; pkill -f "nvidia-smi --query-gpu=utilization" 2>/dev/null; sleep 1
  local SAMP=/workspace/util_${TAG}.csv; rm -f "$SAMP"
  local OUT=/workspace/savant_rung0_${TAG}.clm
  local TLOG=/workspace/train_${TAG}.log
  nohup bash -c 'while true; do nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits -i 0 2>/dev/null; sleep 0.2; done' > "$SAMP" 2>/dev/null &
  local SPID=$!
  local t0=$(date +%s)
  timeout "$TIMEOUT" env CLM_PROD_D=$D CLM_PROD_T=$T CLM_PROD_E=$E CLM_PROD_NSAMP=$NS CLM_PROD_EPOCHS=$EP \
    CLM_PROD_CORPUS="$CORPUS" CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1 CLM_PROD_OUT="$OUT" \
    HEXA_CUDA_LINK=1 "$CLM" > "$TLOG" 2>&1
  local RC=$?
  local t1=$(date +%s)
  kill $SPID 2>/dev/null
  echo "FIRE_RC=$RC  tag=$TAG  wall=$((t1-t0))s"
  python3 - "$SAMP" "$TAG" <<'PY'
import sys
samp,tag=sys.argv[1],sys.argv[2]
vals=[int(l) for l in open(samp) if l.strip().isdigit()]
if vals:
    n=len(vals); ge20=sum(1 for v in vals if v>=20)
    print(f"UTIL[{tag}] n={n} PEAK={max(vals)}% MEAN={sum(vals)/n:.4f}% pct_ge20={100*ge20/n:.2f}%")
else: print(f"UTIL[{tag}] n=0")
PY
  echo "--- descent[$TAG] (g63 verbatim) ---"
  grep -E "epoch-1 mean CE|epoch-.* mean CE|F-CLM-PROD-DESCENT|PASS|FAIL|wrote|windows:|corpus:" "$TLOG" | tail -12
  echo "--- ckpt[$TAG] ---"
  ls -la "$OUT" 2>&1 | tail -1; sha256sum "$OUT" 2>/dev/null
}

# rung0 PRIMARY: d768 class, ENOUGH epochs for a clean descent on the small starter corpus.
# (d768 E2 is the proven-descending forge config; 6 epochs over the 5-lang starter.)
fire_cfg rung0_d768 768 256 2 64 6 2400

echo ""
echo "=== SAVANT-7B rung0 FIRE DONE $(date -u +%FT%TZ) ==="
