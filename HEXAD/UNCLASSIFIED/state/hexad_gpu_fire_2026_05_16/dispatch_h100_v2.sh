#!/bin/bash
# dispatch_h100_v2.sh — Phase D real GPU fire, HARDENED rev.
#
# v1 (dispatch_h100.sh) outcomes:
#   - devel image fix WORKED: cublas_v2.h + cuda_runtime.h PRESENT
#   - runtime_cuda.c compiled cleanly (OBJ_RC=0, all _hx_cuda_* symbols
#     + cublasCreate_v2/cublasDgemm_v2 referenced) — Phase D integration
#     proof CAPTURED.
#   - bench FAILED: gcc cannot compile cudaDeviceProp (CUDA C++ struct);
#     needs nvcc. v1 used gcc → build error, BUILD_RC=0 false positive.
#   - H100 NVL (reliability 0.893, lowest avail) DIED mid-fire (SSH
#     Connection refused at pull retry 2/3). No cost leak.
#
# v2 fixes:
#   1. nvcc -x cu (NOT gcc) for the bench — handles cudaDeviceProp.
#   2. Prefer highest-reliability H100/H200 offer (-o reliability-).
#   3. Build + run + JSON-capture + nvidia-smi-during ALL in ONE SSH
#      session, result echoed inline to local log — so even if the box
#      dies right after, the numbers are already in our local log.
#   4. devel image (v1-proven: nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04)

set -uo pipefail
PHASE_ID="hexad_gpu_fire_h100_v2"
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_2026_05_16"
PHASE_LABEL="anima-rfc040-phaseD-h100-v2"
VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} dispatch (Phase D H100 v2, 2026-05-16) ==="; date -u

echo "[1/8] Search H100/H200 — highest reliability first..."
OFFER_JSON=$($VASTAI search offers \
    'gpu_name in [H100_SXM,H100_PCIE,H100_NVL,H100,H200,H200_SXM] num_gpus=1 rentable=true dph_total<6.5 cuda_max_good>=12.4 disk_space>40' \
    -o 'reliability-' --raw 2>&1)
OFFER_PARSED=$(echo "$OFFER_JSON" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('parse_err\n'); sys.exit(1)
if not d: sys.stderr.write('no_offers\n'); sys.exit(1)
b=d[0]
print('%s %.4f %s %s %.4f' % (b['id'],b['dph_total'],b['gpu_name'].replace(' ','_'),b.get('cuda_max_good','?'),b.get('reliability',0)))
")
OFFER_ID=$(echo "$OFFER_PARSED" | awk '{print $1}')
OFFER_DPH=$(echo "$OFFER_PARSED" | awk '{print $2}')
OFFER_GPU=$(echo "$OFFER_PARSED" | awk '{print $3}')
OFFER_REL=$(echo "$OFFER_PARSED" | awk '{print $5}')
[ -z "$OFFER_ID" ] && { echo "ERR: no offer"; exit 1; }
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$OFFER_GPU reliability=$OFFER_REL"
echo "$OFFER_ID" > offer_id_v2.txt

echo "[2/8] Rent (devel image, headers preinstalled)..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image nvidia/cuda:12.4.1-cudnn-devel-ubuntu22.04 \
    --disk 45 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('pf: '+sys.stdin.read()+'\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id',''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERR: id parse fail: $CREATE_OUT"; exit 1; }
echo "  Instance: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id_v2.txt

cleanup() {
    local rc=$?
    if [ "${SAVE_POD:-0}" = "1" ]; then
        echo "[cleanup] SAVE_POD=1 keep $INSTANCE_ID (rc=$rc)"
    else
        echo "[cleanup] destroy $INSTANCE_ID (exit=$rc)"
        $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
    fi
}
trap cleanup EXIT INT TERM

echo "[3/8] Wait SSH (max 13min) — uses LIST endpoint (per-instance CLI crashes on start_date=None)..."
SSH_HOST=""; SSH_PORT=""
for i in $(seq 1 160); do
    # vastai show instance <id> crashes (start_date=None bug). Use the
    # list endpoint + filter by our id — it tolerates the null start_date.
    LIST=$($VASTAI show instances --raw 2>/dev/null || true)
    [ -z "$LIST" ] && LIST="[]"
    PARSED=$(echo "$LIST" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: print('PARSE_ERR||'); sys.exit(0)
if not isinstance(d,list): print('NOTLIST||'); sys.exit(0)
tgt=str($INSTANCE_ID)
for inst in d:
    if str(inst.get('id',''))==tgt:
        st=inst.get('actual_status','') or ''
        host=inst.get('public_ipaddr','') or inst.get('ssh_host','') or ''
        ports=inst.get('ports',{}) or {}
        m=ports.get('22/tcp')
        port=(m[0]['HostPort'] if m else (inst.get('direct_port_start','') or inst.get('ssh_port',''))) or ''
        print('%s|%s|%s'%(st,host,port)); sys.exit(0)
print('ABSENT||')
" 2>/dev/null || echo "PYERR||")
    STATUS="${PARSED%%|*}"
    REST="${PARSED#*|}"
    CAND_HOST="${REST%%|*}"
    CAND_PORT="${REST##*|}"
    if [ "$STATUS" = "running" ] && [ -n "$CAND_HOST" ] && [ -n "$CAND_PORT" ]; then
        if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
            -o ConnectTimeout=10 -p "$CAND_PORT" "root@$CAND_HOST" 'echo READY' 2>&1 | grep -q READY; then
            SSH_HOST="$CAND_HOST"; SSH_PORT="$CAND_PORT"
            echo "  SSH ready: $SSH_HOST:$SSH_PORT (after ${i}x5s)"; break
        fi
    fi
    # ABSENT for >12 consecutive polls (>1min) after creation = phantom instance
    if [ "$STATUS" = "ABSENT" ] && [ $i -gt 14 ]; then
        echo "ERR: instance $INSTANCE_ID ABSENT from list for >1min — phantom/rejected by host"; exit 2
    fi
    echo "  ... attempt $i/160 status=${STATUS:-empty}"; sleep 5
done
[ -z "$SSH_HOST" ] && { echo "ERR: SSH not ready"; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh_v2.txt
SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=30"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=900"

echo "[4/8] Upload sources..."
$SSH_CMD 'mkdir -p /workspace/gpu_fire'
$SCP_CMD "$LOCAL_DIR/gpu_matmul_bench.c" "root@$SSH_HOST:/workspace/gpu_fire/"
$SCP_CMD "$LOCAL_DIR/runtime_cuda.c"     "root@$SSH_HOST:/workspace/gpu_fire/"

echo "[5/8] Sanity + build + bench + runtime_cuda compile — ALL one session..."
# Everything in ONE ssh exec. nvidia-smi sampled in background during bench.
# result.json catted to stdout so it lands in our LOCAL log immediately.
$SSH_CMD 'set +e
  echo "=== nvidia-smi ==="; nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
  echo "=== nvcc ==="; nvcc --version | tail -2
  ls /usr/local/cuda/include/cublas_v2.h && echo CUBLAS_H_OK
  cd /workspace/gpu_fire
  echo "=== build bench (nvcc -x cu) ==="
  nvcc -O2 -x cu gpu_matmul_bench.c -lcublas -lcudart -o gpu_matmul_bench 2>&1 | tail -15
  echo "BENCH_BUILD_RC=$?"
  ls -la gpu_matmul_bench 2>&1
  echo "=== run bench (nvidia-smi sampled during) ==="
  rm -f nvidia_smi_during.csv
  ( for k in $(seq 1 90); do nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw --format=csv,noheader >> nvidia_smi_during.csv; sleep 1; done ) &
  SMIPID=$!
  LD_LIBRARY_PATH=/usr/local/cuda/lib64 ./gpu_matmul_bench
  echo "BENCH_RUN_RC=$?"
  kill $SMIPID 2>/dev/null
  echo "=== gpu_matmul_bench_result.json ==="
  cat /workspace/gpu_fire/gpu_matmul_bench_result.json 2>&1
  echo "=== nvidia-smi peak (sorted by util desc, top 8) ==="
  sort -t, -k1 -rn nvidia_smi_during.csv | head -8
  echo "=== compile-test runtime_cuda.c (nvcc, links cublas) ==="
  nvcc -O2 -x cu -c runtime_cuda.c -o runtime_cuda.o 2>&1 | tail -8
  echo "RUNTIME_CUDA_RC=$?"
  ls -la runtime_cuda.o 2>&1
  nm runtime_cuda.o 2>&1 | grep -E "_hx_cuda_|cublas|cudaMalloc" | head -20
  echo "ALLDONE"' 2>&1 | tee "$LOCAL_DIR/h100_v2_session.log"

echo "[6/8] Pull artifacts (result already in session log; pull files too)..."
SAVE_POD=1   # retain until pulls confirmed
pull() {
  local s="$1" d="$2" t=0
  while [ $t -lt 3 ]; do
    $SCP_CMD "root@$SSH_HOST:$s" "$d" 2>&1 && { echo "  pulled $s"; return 0; }
    t=$((t+1)); echo "  retry $t/3 $s"; [ $t -lt 3 ] && sleep 20
  done
  echo "  PULL-FAIL $s"; return 1
}
pull /workspace/gpu_fire/gpu_matmul_bench_result.json "$LOCAL_DIR/gpu_matmul_bench_result.json" || true
pull /workspace/gpu_fire/nvidia_smi_during.csv        "$LOCAL_DIR/nvidia_smi_during_h100.csv" || true
pull /workspace/gpu_fire/runtime_cuda.o               "$LOCAL_DIR/runtime_cuda_h100.o" || true

echo "[7/8] Destroy instance (result captured in session log regardless)..."
$VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
SAVE_POD=1  # already destroyed; skip trap re-destroy

echo "[8/8] === ${PHASE_ID} DONE ==="; date -u
if [ -f "$LOCAL_DIR/gpu_matmul_bench_result.json" ]; then
python3 -c "
import json
d=json.load(open('$LOCAL_DIR/gpu_matmul_bench_result.json'))
print('Device:',d.get('device_name'),'cc',d.get('device_cc'),d.get('device_mem_mb'),'MB')
for s in d.get('shapes',[]):
    print('  %dx%dx%d  GPU %.3fms %.1f GF/s  CPU %.1fms  max|d|=%.2e rel=%.2e'%(
        s['M'],s['K'],s['N'],s['gpu_ms_avg'],s['gpu_gflops'],s['cpu_ms'],
        s['max_abs_delta'],s['max_rel_delta']))
"
fi
echo "DONE_V2"
