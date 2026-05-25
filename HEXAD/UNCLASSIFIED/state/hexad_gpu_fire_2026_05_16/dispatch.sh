#!/bin/bash
# state/hexad_gpu_fire_2026_05_16/dispatch.sh — anima Phase D real GPU
# fire on vast.ai. Lands the cuBLAS Dgemm impl (runtime_cuda.c) +
# verifies equivalence vs CPU oracle on real RTX 3090 hardware.
#
# AGENTS.tape g_fire_autonomous (2026-05-16): cost-bearing GPU fire is
# fully autonomous. RFC 040 Phase A scope: real `farr_matmul_gpu` via
# cuBLAS Dgemm + equivalence harness on the GPU host.
#
# Scope (honest, per RFC 040 §"Phase A" alone):
#   - cuBLAS Dgemm impl in runtime_cuda.c works on real GPU
#   - Numerical equivalence to RFC 032 CPU oracle within TOL_MATMUL
#   - Benchmark on d_train5-representative shapes (d=64..1024)
#   - PROVES real GPU usage (nvidia-smi util > 0, GFLOP/s measured)
#
# Out of scope (honest C3, deferred to Phase B+C):
#   - hexa-lang bootstrap on the box (we ship runtime_cuda.c + bench
#     compiled standalone; runtime.c-side wire is in the commit)
#   - d_train5 full GPU wire (Phase C — d_train5 currently uses
#     pure-hexa list math c3_matvec, NOT farr_matmul, so a true
#     GPU-routed d_train5 needs Phase B+C refactor)
#   - softmax/rmsnorm/adamw GPU kernels (Phase B)

set -uo pipefail   # NOT -e: we want to capture failures + continue cleanup

PHASE_ID="hexad_gpu_fire"
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_2026_05_16"
PHASE_LABEL="anima-rfc040-phaseA-real-gpu"

VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
[ -x "$VASTAI" ] || { echo "ERROR: vastai CLI not found at $VASTAI"; exit 1; }
[ -f "$VAST_SSH_KEY" ] || { echo "ERROR: vast ssh key missing"; exit 1; }
[ -f "$LOCAL_DIR/runtime_cuda.c" ] || { echo "ERROR: runtime_cuda.c missing"; exit 1; }
[ -f "$LOCAL_DIR/gpu_matmul_bench.c" ] || { echo "ERROR: gpu_matmul_bench.c missing"; exit 1; }

cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} vast.ai dispatch (Phase D, 2026-05-16) ==="
date -u

# ── 1) Search RTX 3090 offers ────────────────────────────────────────
echo "[1/9] Searching RTX 3090 offers under \$0.50/hr ..."
OFFER_JSON=$($VASTAI search offers \
    'gpu_name in [RTX_4090,RTX_3090] num_gpus=1 reliability>0.98 dph_total<0.5 disk_space>50 inet_down>200 cuda_max_good>=12.0' \
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

# ── 2) Rent instance with CUDA image ─────────────────────────────────
echo "[2/9] Renting instance with CUDA 12.x image..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-runtime \
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

# ── 4) Sanity-check CUDA + GCC + ensure cuBLAS headers ───────────────
echo "[4/9] Remote toolchain sanity + cublas dev install if needed..."
$SSH_CMD 'set +e
  nvidia-smi | head -5
  ls /usr/local/cuda/include/cublas_v2.h 2>/dev/null && echo "cublas_v2.h PRESENT" || {
    echo "cublas_v2.h MISSING — installing dev headers"
    apt-get update -qq
    apt-get install -y -qq --no-install-recommends libcublas-dev-12-1 libcurand-dev-12-1 build-essential 2>&1 | tail -5
    ls /usr/local/cuda/include/cublas_v2.h && echo "cublas_v2.h NOW PRESENT" || \
       ls /usr/include/cublas_v2.h && echo "cublas_v2.h in /usr/include"
  }
  which gcc || apt-get install -y -qq build-essential
  gcc --version | head -1
  ls /usr/local/cuda/lib64/libcublas.so* 2>/dev/null | head -2
  ls /usr/lib/x86_64-linux-gnu/libcublas.so* 2>/dev/null | head -2
  echo "TOOLCHAIN_OK"' 2>&1 | tee remote_sanity.log

# ── 5) Upload bench source ───────────────────────────────────────────
echo "[5/9] Upload sources..."
$SSH_CMD 'mkdir -p /workspace/gpu_fire'
$SCP_CMD "$LOCAL_DIR/gpu_matmul_bench.c" "root@$SSH_HOST:/workspace/gpu_fire/"
$SCP_CMD "$LOCAL_DIR/runtime_cuda.c"      "root@$SSH_HOST:/workspace/gpu_fire/"

# ── 6) Build cuBLAS bench + run ──────────────────────────────────────
echo "[6/9] Build + run gpu_matmul_bench (real cuBLAS Dgemm on RTX 3090)..."
$SSH_CMD "cd /workspace/gpu_fire && \
    CUDA_INC=/usr/local/cuda/include ; \
    [ -f \$CUDA_INC/cublas_v2.h ] || CUDA_INC=/usr/include ; \
    CUDA_LIB=/usr/local/cuda/lib64 ; \
    [ -e \$CUDA_LIB/libcublas.so ] || CUDA_LIB=/usr/lib/x86_64-linux-gnu ; \
    echo CUDA_INC=\$CUDA_INC CUDA_LIB=\$CUDA_LIB ; \
    gcc -O2 -std=gnu11 -I\$CUDA_INC gpu_matmul_bench.c \
        -L\$CUDA_LIB -lcublas -lcudart -lm -lrt \
        -o gpu_matmul_bench 2>&1 | tee build.log ; \
    echo BUILD_RC=\$? ; \
    nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader > /workspace/gpu_fire/nvidia_smi_pre.csv ; \
    LD_LIBRARY_PATH=\$CUDA_LIB ./gpu_matmul_bench 2>&1 | tee bench.log ; \
    echo BENCH_RC=\$? ; \
    nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader > /workspace/gpu_fire/nvidia_smi_post.csv ; \
    cat /workspace/gpu_fire/gpu_matmul_bench_result.json 2>/dev/null || echo 'NO RESULT JSON'" 2>&1 | tee dispatch.log

# ── 7) Compile-test runtime_cuda.c too (does it link cleanly?) ───────
echo "[7/9] Compile-test runtime_cuda.c (object only — links to runtime _hx_farr_table symbols)..."
$SSH_CMD "cd /workspace/gpu_fire && \
    CUDA_INC=/usr/local/cuda/include ; \
    [ -f \$CUDA_INC/cublas_v2.h ] || CUDA_INC=/usr/include ; \
    gcc -O2 -std=gnu11 -c -I\$CUDA_INC runtime_cuda.c \
        -o runtime_cuda.o 2>&1 | tee runtime_cuda_build.log ; \
    echo OBJ_RC=\$? ; \
    nm runtime_cuda.o | grep -E '_hx_cuda_|T ' | head -30 | tee runtime_cuda_nm.log"

# ── 8) Pull artifacts ────────────────────────────────────────────────
echo "[8/9] Pull artifacts back..."
SAVED=$($SSH_CMD 'test -f /workspace/gpu_fire/gpu_matmul_bench_result.json && echo SAVED' 2>/dev/null || true)
if [ "$SAVED" = "SAVED" ]; then
    echo "  ✓ bench_result.json exists on remote — SAVE_POD=1 to be safe until pulled"
    SAVE_POD=1
else
    echo "  ⚠ bench_result.json NOT found — SAVE_POD=1 for inspection"
    SAVE_POD=1
fi

pull_with_retry() {
    local src="$1" dst="$2" tries=0
    while [ $tries -lt 3 ]; do
        if $SCP_CMD "root@$SSH_HOST:$src" "$dst" 2>&1; then
            echo "  ✓ pulled $src (try $((tries+1)))"; return 0
        fi
        tries=$((tries+1)); echo "  ... pull retry $tries/3 for $src"
        [ $tries -lt 3 ] && sleep 30
    done
    echo "  ✗ pull FAILED after 3 tries: $src"; return 1
}
PULL_OK=1
pull_with_retry "/workspace/gpu_fire/gpu_matmul_bench_result.json" "$LOCAL_DIR/gpu_matmul_bench_result.json" || PULL_OK=0
pull_with_retry "/workspace/gpu_fire/bench.log"                    "$LOCAL_DIR/bench.log" || PULL_OK=0
pull_with_retry "/workspace/gpu_fire/build.log"                    "$LOCAL_DIR/build.log" || PULL_OK=0
pull_with_retry "/workspace/gpu_fire/runtime_cuda_build.log"       "$LOCAL_DIR/runtime_cuda_build.log" || true
pull_with_retry "/workspace/gpu_fire/runtime_cuda_nm.log"          "$LOCAL_DIR/runtime_cuda_nm.log" || true
pull_with_retry "/workspace/gpu_fire/nvidia_smi_pre.csv"           "$LOCAL_DIR/nvidia_smi_pre.csv" || true
pull_with_retry "/workspace/gpu_fire/nvidia_smi_post.csv"          "$LOCAL_DIR/nvidia_smi_post.csv" || true

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
print('Device: ' + d.get('device_name','?') + ' (cc ' + d.get('device_cc','?') + ')')
shapes = d.get('shapes', [])
print('Shape sweep (' + str(len(shapes)) + '):')
for s in shapes:
    print('  M=%d K=%d N=%d  GPU=%.3f ms (%.1f GF/s)  CPU=%.1f ms  max|Δ|=%.2e  rel=%.2e' % (
        s['M'], s['K'], s['N'], s['gpu_ms_avg'], s['gpu_gflops'],
        s['cpu_ms'], s['max_abs_delta'], s['max_rel_delta']))
"
fi
echo "DONE"
