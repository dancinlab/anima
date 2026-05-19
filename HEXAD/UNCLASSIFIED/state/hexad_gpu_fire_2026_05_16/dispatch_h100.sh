#!/bin/bash
# state/hexad_gpu_fire_2026_05_16/dispatch_h100.sh — anima Phase D real GPU
# fire on vast.ai H100. user directive 2026-05-16 "3090 중단 → H100 재dispatch".
# Prior dispatch.sh (3090 attempt) failed because pytorch:cuda12.1-runtime
# image lacks cuBLAS dev headers, and apt-get could not find
# libcublas-dev-12-1 in default Ubuntu repos. This rewrite:
#   - selects an H100 / H100_NVL / H100_PCIE offer
#   - uses nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 (devel = ALL dev headers
#     preinstalled, no apt-get gymnastics)
#   - builds + runs gpu_matmul_bench (real cuBLAS Dgemm, FP64 H100 ~67 TFLOPs)
#   - compile-tests runtime_cuda.c against headers (links into hexa-lang
#     under -DHEXA_CUDA — separate full-rebuild deferred)
#   - pulls bench result JSON + logs + nvidia-smi traces
#
# AGENTS.tape g_fire_autonomous (2026-05-16): cost-bearing GPU fire is
# fully autonomous. g_fire_dispatch_robust: SAVE_POD=1 retain on partial.

set -uo pipefail

PHASE_ID="hexad_gpu_fire_h100"
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_2026_05_16"
PHASE_LABEL="anima-rfc040-phaseD-h100-cublas"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found at $VASTAI"; exit 1; }
[ -f "$VAST_SSH_KEY" ] || { echo "ERROR: vast ssh key missing"; exit 1; }
[ -f "$LOCAL_DIR/runtime_cuda.c" ] || { echo "ERROR: runtime_cuda.c missing"; exit 1; }
[ -f "$LOCAL_DIR/gpu_matmul_bench.c" ] || { echo "ERROR: gpu_matmul_bench.c missing"; exit 1; }

cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai dispatch (Phase D H100, 2026-05-16) ==="
date -u

# ── 1) Search H100 offers ─────────────────────────────────────────────
echo "[1/9] Searching H100 / H100_NVL / H100_PCIE offers under \$5/hr ..."
OFFER_JSON=$($VASTAI search offers \
    'gpu_name in [H100_SXM,H100_PCIE,H100_NVL,H100,H200] num_gpus=1 rentable=true dph_total<5.0 cuda_max_good>=12.4 disk_space>50 inet_down>200' \
    -o dph_total --raw 2>&1)
OFFER_PARSED=$(echo "$OFFER_JSON" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('parse_err\n'); sys.exit(1)
if not d: sys.stderr.write('no_offers\n'); sys.exit(1)
b = d[0]
print('%s %.4f %s %s' % (b['id'], b['dph_total'], b['gpu_name'].replace(' ','_'), b.get('cuda_max_good','?')))
")
OFFER_ID=$(echo "$OFFER_PARSED" | awk '{print $1}')
OFFER_DPH=$(echo "$OFFER_PARSED" | awk '{print $2}')
OFFER_GPU=$(echo "$OFFER_PARSED" | awk '{print $3}')
OFFER_CUDA=$(echo "$OFFER_PARSED" | awk '{print $4}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$OFFER_GPU cuda=$OFFER_CUDA"
echo "$OFFER_ID" > offer_id.txt

# ── 2) Rent instance with CUDA devel image (headers preinstalled) ─────
# devel image = ALL CUDA dev headers + libs + gcc preinstalled. No
# apt-get gymnastics needed. nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04
# is the canonical FP64-supporting devel base.
echo "[2/9] Renting instance with CUDA 12.4 DEVEL image..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 \
    --disk 50 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('parse_fail: '+sys.stdin.read()+'\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id',''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERROR: instance id parse failed: $CREATE_OUT"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

cleanup() {
    local rc=$?
    if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[cleanup] SAVE_POD=1 — keep instance $INSTANCE_ID (rc=$rc)"
    else
        echo "[cleanup] Destroying instance $INSTANCE_ID (exit=$rc)..."
        $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    fi
}
trap cleanup EXIT INT TERM

# ── 3) Wait for SSH (direct-IP) ──────────────────────────────────────
echo "[3/9] Waiting for SSH (max 13 min)..."
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 160); do
    INFO=$($VASTAI show instance "$INSTANCE_ID" --raw 2>/dev/null || true)
    [ -z "$INFO" ] && INFO="{}"
    STATUS=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('actual_status',''))
except: print('parse_err')" 2>/dev/null || echo "")
    if [ "$STATUS" = "running" ]; then
        SSH_HOST=$(echo "$INFO" | python3 -c "import json,sys
try: d=json.load(sys.stdin); print(d.get('public_ipaddr','') or d.get('ssh_host',''))
except: pass" 2>/dev/null || echo "")
        SSH_PORT=$(echo "$INFO" | python3 -c "import json,sys
try:
 d=json.load(sys.stdin); ports=d.get('ports',{}) or {}
 m=ports.get('22/tcp')
 print(m[0]['HostPort'] if m else (d.get('direct_port_start','') or d.get('ssh_port','')))
except: pass" 2>/dev/null || echo "")
        if [ -n "$SSH_HOST" ] && [ -n "$SSH_PORT" ]; then
            if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
                -o ConnectTimeout=10 -p "$SSH_PORT" "root@$SSH_HOST" 'echo READY' 2>&1 | grep -q READY; then
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (after ${i}x5s)"
                break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... attempt $i/160 status=$STATUS"
    sleep 5
done
[ -z "$SSH_HOST" ] && { echo "ERROR: SSH not ready"; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt
SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=3600"

# ── 4) Sanity-check CUDA + cuBLAS headers ────────────────────────────
echo "[4/9] Remote toolchain sanity (devel image should have everything)..."
$SSH_CMD 'set +e
  nvidia-smi | head -8
  echo "---"
  nvcc --version | head -5
  echo "---"
  ls /usr/local/cuda/include/cublas_v2.h && echo "cublas_v2.h PRESENT"
  ls /usr/local/cuda/include/cuda_runtime.h && echo "cuda_runtime.h PRESENT"
  ls /usr/local/cuda/lib64/libcublas.so* 2>/dev/null | head -3
  echo "---"
  which gcc || apt-get update -qq && apt-get install -y -qq build-essential
  gcc --version | head -1
  echo "TOOLCHAIN_OK"' 2>&1 | tee remote_sanity_h100.log

# ── 5) Upload bench + runtime sources ────────────────────────────────
echo "[5/9] Upload sources..."
$SSH_CMD 'mkdir -p /workspace/gpu_fire'
$SCP_CMD "$LOCAL_DIR/gpu_matmul_bench.c" "root@$SSH_HOST:/workspace/gpu_fire/"
$SCP_CMD "$LOCAL_DIR/runtime_cuda.c"      "root@$SSH_HOST:/workspace/gpu_fire/"

# ── 6) Build cuBLAS bench + run on H100 ──────────────────────────────
echo "[6/9] Build + run gpu_matmul_bench (real cuBLAS Dgemm on $OFFER_GPU)..."
$SSH_CMD "cd /workspace/gpu_fire && \
    CUDA_INC=/usr/local/cuda/include ; \
    CUDA_LIB=/usr/local/cuda/lib64 ; \
    echo CUDA_INC=\$CUDA_INC CUDA_LIB=\$CUDA_LIB ; \
    gcc -O2 -std=gnu11 -I\$CUDA_INC gpu_matmul_bench.c \
        -L\$CUDA_LIB -lcublas -lcudart -lm -lrt \
        -o gpu_matmul_bench 2>&1 | tee build_h100.log ; \
    echo BUILD_RC=\$? ; \
    nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader > /workspace/gpu_fire/nvidia_smi_pre_h100.csv ; \
    LD_LIBRARY_PATH=\$CUDA_LIB ./gpu_matmul_bench 2>&1 | tee bench_h100.log ; \
    echo BENCH_RC=\$? ; \
    nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader > /workspace/gpu_fire/nvidia_smi_post_h100.csv ; \
    cat /workspace/gpu_fire/gpu_matmul_bench_result.json 2>/dev/null || echo 'NO RESULT JSON'" 2>&1 | tee dispatch_h100.log

# ── 7) Compile-test runtime_cuda.c (proves header path works) ────────
echo "[7/9] Compile-test runtime_cuda.c (object only — links to runtime _hx_farr_table externs)..."
$SSH_CMD "cd /workspace/gpu_fire && \
    CUDA_INC=/usr/local/cuda/include ; \
    gcc -O2 -std=gnu11 -c -I\$CUDA_INC runtime_cuda.c \
        -o runtime_cuda.o 2>&1 | tee runtime_cuda_build_h100.log ; \
    echo OBJ_RC=\$? ; \
    ls -la runtime_cuda.o 2>&1 ; \
    nm runtime_cuda.o 2>&1 | grep -E '_hx_cuda_|cublas' | head -30 | tee runtime_cuda_nm_h100.log"

# ── 8) Pull artifacts ────────────────────────────────────────────────
echo "[8/9] Pull artifacts back..."
SAVED=$($SSH_CMD 'test -f /workspace/gpu_fire/gpu_matmul_bench_result.json && echo SAVED' 2>/dev/null || true)
if [ "$SAVED" = "SAVED" ]; then
    echo "  bench_result.json exists on remote — SAVE_POD=1 to be safe until pulled"
    SAVE_POD=1
else
    echo "  WARNING: bench_result.json NOT found — SAVE_POD=1 for inspection"
    SAVE_POD=1
fi

pull_with_retry() {
    local src="$1" dst="$2" tries=0
    while [ $tries -lt 3 ]; do
        if $SCP_CMD "root@$SSH_HOST:$src" "$dst" 2>&1; then
            echo "  pulled $src (try $((tries+1)))"; return 0
        fi
        tries=$((tries+1)); echo "  ... pull retry $tries/3 for $src"
        [ $tries -lt 3 ] && sleep 30
    done
    echo "  pull FAILED after 3 tries: $src"; return 1
}
PULL_OK=1
pull_with_retry "/workspace/gpu_fire/gpu_matmul_bench_result.json" "$LOCAL_DIR/gpu_matmul_bench_result.json" || PULL_OK=0
pull_with_retry "/workspace/gpu_fire/bench_h100.log"                "$LOCAL_DIR/bench_h100.log" || PULL_OK=0
pull_with_retry "/workspace/gpu_fire/build_h100.log"                "$LOCAL_DIR/build_h100.log" || PULL_OK=0
pull_with_retry "/workspace/gpu_fire/runtime_cuda_build_h100.log"   "$LOCAL_DIR/runtime_cuda_build_h100.log" || true
pull_with_retry "/workspace/gpu_fire/runtime_cuda_nm_h100.log"      "$LOCAL_DIR/runtime_cuda_nm_h100.log" || true
pull_with_retry "/workspace/gpu_fire/nvidia_smi_pre_h100.csv"       "$LOCAL_DIR/nvidia_smi_pre_h100.csv" || true
pull_with_retry "/workspace/gpu_fire/nvidia_smi_post_h100.csv"      "$LOCAL_DIR/nvidia_smi_post_h100.csv" || true

if [ $PULL_OK -eq 0 ]; then
    echo "[WARN] artifact pull partial fail — pod RETAINED (SAVE_POD=1)"
    echo "[WARN] manual recovery: ssh -i $VAST_SSH_KEY -p $SSH_PORT root@$SSH_HOST"
else
    echo "[OK] core artifacts pulled — destroying instance now (explicit, pre-trap)"
    $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    SAVE_POD=1  # trap skip (already destroyed)
fi

# ── 9) Summary ───────────────────────────────────────────────────────
echo "[9/9] === ${PHASE_ID} DONE ==="
date -u
if [ -f "$LOCAL_DIR/gpu_matmul_bench_result.json" ]; then
    python3 -c "
import json
d = json.load(open('$LOCAL_DIR/gpu_matmul_bench_result.json'))
print('Device: ' + d.get('device_name','?') + ' (cc ' + str(d.get('device_cc','?')) + ')')
shapes = d.get('shapes', [])
print('Shape sweep (' + str(len(shapes)) + '):')
for s in shapes:
    print('  M=%d K=%d N=%d  GPU=%.3f ms (%.1f GF/s)  CPU=%.1f ms  max|delta|=%.2e  rel=%.2e' % (
        s['M'], s['K'], s['N'], s['gpu_ms_avg'], s['gpu_gflops'],
        s['cpu_ms'], s['max_abs_delta'], s['max_rel_delta']))
"
fi
echo "DONE"
