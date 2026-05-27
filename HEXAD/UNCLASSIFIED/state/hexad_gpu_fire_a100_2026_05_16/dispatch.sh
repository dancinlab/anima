#!/bin/bash
# state/hexad_gpu_fire_a100_2026_05_16/dispatch.sh
# Phase D PARALLEL/A100 RETRY fire (prior attempt server-throttled mid-run).
#
# Complementary to the H100 fire in state/hexad_gpu_fire_2026_05_16/.
# Isolation: writes ONLY into state/hexad_gpu_fire_a100_2026_05_16/.
#
# What this does (mission RETRY spec):
#   1. Rent cheapest verified A100_PCIE (≤$1.5/hr) — fallback A100_SXM4.
#   2. pytorch cuda12 devel image (cuda_runtime.h + cublas_v2.h preinstalled).
#   3. Build hexa-lang interp FROM SOURCE with -DHEXA_CUDA, linking
#      runtime_cuda.c (real cuBLAS Dgemm) + -lcublas -lcudart.
#      The two `static` farr-table symbols are sed-promoted to extern
#      so the runtime_cuda.c TU links (build-time only; no perm edit).
#   4. Real-GPU smoke: tmp_rfc040_realgpu_smoke.hexa asserts
#      cuda_available()==1 + real cuBLAS Dgemm == CPU oracle within
#      measured tolerance → F-RFC040 5/5 REAL GPU path.
#   5. Fire d_corpus_fire_a100.hexa: d=384·6L (nh=6 nkv=2 h=1024 T=64
#      nsamp=16, 80 AdamW steps, seed=43). nvidia-smi util sampled.
#   6. Harvest RESULT_JSON from stdout → result.json; scp logs; destroy
#      clean. Commit state/hexad_gpu_fire_a100_2026_05_16/{result.json,
#      fire.log}.
#
# Orphan watchdog: auto-destroys any anima-rfc040* instance whose age
# exceeds 75min — death won't bleed money even if SSH dies mid-run.
#
# AGENTS.tape g_fire_autonomous (2026-05-16): cost-bearing, no gate.
# g3 honesty: real nvidia-smi util, measured cuBLAS tolerance, no fake.

set -uo pipefail

PHASE_ID="hexad_gpu_fire_a100"
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_a100_2026_05_16"
PHASE_LABEL="anima-rfc040-phaseD-a100-retry"
VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
HEXA_SRC_TGZ="/tmp/hexa_cuda_src.tgz"
cd "$LOCAL_DIR"
exec > >(tee "$LOCAL_DIR/fire.log") 2>&1
echo "=== ${PHASE_ID} dispatch (Phase D A100 RETRY, 2026-05-16) ==="
date -u

# ── Orphan watchdog: kill any anima-rfc040* instance older than 75min ──
orphan_watchdog() {
    local mine="$1"
    local LST
    LST=$($VASTAI show instances --raw 2>/dev/null || echo "[]")
    echo "$LST" | python3 -c "
import json,sys,time
try: d=json.load(sys.stdin)
except: sys.exit(0)
now=time.time()
for i in d:
    lbl=str(i.get('label') or '')
    if not lbl.startswith('anima-rfc040'): continue
    iid=i.get('id')
    st=i.get('start_date') or 0
    try: st=float(st)
    except: st=0
    age=(now-st)/60.0 if st>0 else 0
    if iid is not None and age>75:
        print('%s %.1f' % (iid,age))
" | while read iid age; do
        if [ -n "$iid" ] && [ "$iid" != "$mine" ]; then
            echo "[watchdog] destroying orphan anima-rfc040* id=$iid age=${age}min"
            $VASTAI destroy instance "$iid" 2>&1 | head -2 || true
        fi
    done
}

echo "[0/8] Orphan sweep (pre-flight)..."
orphan_watchdog "none" || true

echo "[1/8] Build minimal hexa-lang source tree (CUDA single-TU build)..."
# The real .hexa interpreter = transpiled self/hexa_full.hexa with
# runtime.c inlined (single TU). interpreter.hexa.c is the COMPILER
# shim, NOT a script runner — do not use it. We pre-transpiled
# hexa_full_singletu.c (#include "runtime.c") locally; the box just
# gcc's it with -DHEXA_CUDA + links runtime_cuda.c + cuBLAS.
rm -rf /tmp/cuda_src_stage && mkdir -p /tmp/cuda_src_stage/native
cp /Users/ghost/core/hexa-lang/self/runtime.c \
   /Users/ghost/core/hexa-lang/self/runtime.h \
   /Users/ghost/core/hexa-lang/self/runtime_hi_gen.c /tmp/cuda_src_stage/
cp /Users/ghost/core/hexa-lang/self/native/*.c /tmp/cuda_src_stage/native/ 2>/dev/null || true
( cd /tmp/cuda_src_stage/native && rm -f *.bak.* *.hexanoport 2>/dev/null || true )
tar czf "$HEXA_SRC_TGZ" -C /tmp/cuda_src_stage .
ls -la "$HEXA_SRC_TGZ" "$LOCAL_DIR/hexa_full_singletu.c"

echo "[2/8] Search cheapest verified A100_PCIE (<=\$1.5/hr; SXM4 fallback)..."
OFFER_JSON=$($VASTAI search offers \
    'gpu_name=A100_PCIE num_gpus=1 verified=true rentable=true dph_total<1.5 cuda_max_good>=12.1 disk_space>50' \
    -o dph --raw 2>&1)
OFFER_PARSED=$(echo "$OFFER_JSON" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: print('PARSE_ERR'); sys.exit(0)
if not d: print('NONE'); sys.exit(0)
b=d[0]
print('%s %.4f %s' % (b['id'],b['dph_total'],b['gpu_name'].replace(' ','_')))
")
if [ "$OFFER_PARSED" = "NONE" ] || [ "$OFFER_PARSED" = "PARSE_ERR" ] || [ -z "$OFFER_PARSED" ]; then
    echo "  A100_PCIE none — trying A100_SXM4..."
    OFFER_JSON=$($VASTAI search offers \
        'gpu_name=A100_SXM4 num_gpus=1 verified=true rentable=true dph_total<1.5 cuda_max_good>=12.1 disk_space>50' \
        -o dph --raw 2>&1)
    OFFER_PARSED=$(echo "$OFFER_JSON" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: print('NONE'); sys.exit(0)
if not d: print('NONE'); sys.exit(0)
b=d[0]
print('%s %.4f %s' % (b['id'],b['dph_total'],b['gpu_name'].replace(' ','_')))
")
fi
[ "$OFFER_PARSED" = "NONE" ] && { echo "ERR: no A100 offer <=\$1.5/hr"; exit 1; }
OFFER_ID=$(echo "$OFFER_PARSED" | awk '{print $1}')
OFFER_DPH=$(echo "$OFFER_PARSED" | awk '{print $2}')
OFFER_GPU=$(echo "$OFFER_PARSED" | awk '{print $3}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$OFFER_GPU"
echo "$OFFER_ID" > offer_id.txt

echo "[3/8] Rent (pytorch cuda12 devel image)..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel \
    --disk 55 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('pf: '+sys.stdin.read()+'\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id',''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERR: id parse fail: $CREATE_OUT"; exit 1; }
echo "  Instance: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt

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

echo "[4/8] Wait SSH (max 13min)..."
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
                echo "  SSH ready: $SSH_HOST:$SSH_PORT (after ${i}x5s)"; break
            fi
            SSH_HOST=""
        fi
    fi
    echo "  ... attempt $i/160 status=$STATUS"
    [ $((i % 12)) -eq 0 ] && orphan_watchdog "$INSTANCE_ID"
    sleep 5
done
[ -z "$SSH_HOST" ] && { echo "ERR: SSH not ready"; exit 1; }
echo "$SSH_HOST:$SSH_PORT" > vast_ssh.txt
SSH_OPTS="-i $VAST_SSH_KEY -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=30"
SSH_CMD="ssh $SSH_OPTS -p $SSH_PORT root@$SSH_HOST"
SCP_CMD="scp $SSH_OPTS -P $SSH_PORT -o ConnectTimeout=900"

echo "[5/8] Upload sources..."
$SSH_CMD 'mkdir -p /workspace/cuda_fire/self'
$SCP_CMD "$HEXA_SRC_TGZ"                              "root@$SSH_HOST:/workspace/cuda_fire/hexa_cuda_src.tgz"
$SCP_CMD "$LOCAL_DIR/hexa_full_singletu.c"            "root@$SSH_HOST:/workspace/cuda_fire/"
$SCP_CMD "$LOCAL_DIR/runtime_cuda.c"                  "root@$SSH_HOST:/workspace/cuda_fire/"
$SCP_CMD "$LOCAL_DIR/tmp_rfc040_realgpu_smoke.hexa"   "root@$SSH_HOST:/workspace/cuda_fire/"
$SCP_CMD "$LOCAL_DIR/d_corpus_fire_a100.hexa"         "root@$SSH_HOST:/workspace/cuda_fire/"
$SCP_CMD /Users/ghost/core/anima/HEXAD/D/d_train5_lib.hexa      "root@$SSH_HOST:/workspace/cuda_fire/"
$SCP_CMD /Users/ghost/core/anima/HEXAD/D/corpus_loader_lib.hexa "root@$SSH_HOST:/workspace/cuda_fire/"
$SCP_CMD /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl "root@$SSH_HOST:/workspace/cuda_fire/"

echo "[6/8] Build CUDA interp + smoke + d_corpus_fire — ALL one SSH session..."
$SSH_CMD 'set +e
  echo "=== nvidia-smi ==="; nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
  echo "=== nvcc ==="; (nvcc --version 2>/dev/null | tail -2) || echo "no nvcc"
  ls /usr/local/cuda/include/cublas_v2.h 2>/dev/null && echo CUBLAS_H_OK || echo CUBLAS_H_MISSING
  cd /workspace/cuda_fire
  tar xzf hexa_cuda_src.tgz -C self
  ls self/ | head
  # promote the two farr-table symbols to extern linkage so the
  # separately-compiled runtime_cuda.c TU resolves them (CUDA build only).
  sed -i "s/^static HexaFarrEntry\* _hx_farr_table     = NULL;/HexaFarrEntry* _hx_farr_table = NULL;/" self/runtime.c
  sed -i "s/^static int64_t        _hx_farr_count     = 0;/int64_t _hx_farr_count = 0;/" self/runtime.c
  grep -n "^HexaFarrEntry\* _hx_farr_table = NULL;\|^int64_t _hx_farr_count = 0;" self/runtime.c | head -3
  CUDA_INC=/usr/local/cuda/include
  CUDA_LIB=/usr/local/cuda/lib64
  echo "=== build hexa interp -DHEXA_CUDA (single-TU hexa_full + runtime_cuda) ==="
  cp runtime_cuda.c self/
  cp hexa_full_singletu.c self/        # so #include "runtime.c" resolves locally
  cd self
  # runtime_cuda.c (cuBLAS Dgemm) → object via nvcc (CUDA headers).
  nvcc -O2 -DHEXA_CUDA -I$CUDA_INC -c runtime_cuda.c -o runtime_cuda.o 2>&1 | tail -8
  echo "RUNTIME_CUDA_OBJ_RC=$?"
  ls -la runtime_cuda.o 2>&1
  # hexa_full_singletu.c #include "runtime.c" → single TU interp object.
  gcc -O2 -D_GNU_SOURCE -std=gnu11 -Wno-trigraphs -DHEXA_CUDA -I. -I$CUDA_INC \
      -c hexa_full_singletu.c -o hexa_full.o 2>&1 | tail -12
  echo "INTERP_OBJ_RC=$?"
  ls -la hexa_full.o 2>&1
  gcc -O2 -DHEXA_CUDA hexa_full.o runtime_cuda.o -o /workspace/cuda_fire/hexa_cuda \
      -L$CUDA_LIB -lcublas -lcudart -lm -ldl -lpthread 2>&1 | tail -8
  echo "LINK_RC=$?"
  ls -la /workspace/cuda_fire/hexa_cuda 2>&1
  cd /workspace/cuda_fire
  mkdir -p /Users/ghost/core/anima/HEXAD/D /Users/ghost/core/anima/training
  ln -sf /workspace/cuda_fire/d_train5_lib.hexa      /Users/ghost/core/anima/HEXAD/D/d_train5_lib.hexa
  ln -sf /workspace/cuda_fire/corpus_loader_lib.hexa /Users/ghost/core/anima/HEXAD/D/corpus_loader_lib.hexa
  ln -sf /workspace/cuda_fire/corpus_consciousness_v1.jsonl /Users/ghost/core/anima/training/corpus_consciousness_v1.jsonl
  export LD_LIBRARY_PATH=$CUDA_LIB:$LD_LIBRARY_PATH
  echo "=== F-RFC040 real-GPU smoke (nvidia-smi sampled) ==="
  rm -f smi_smoke.csv
  ( for k in $(seq 1 30); do nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw --format=csv,noheader >> smi_smoke.csv; sleep 1; done ) &
  SMI1=$!
  HEXA_MEM_UNLIMITED=1 /workspace/cuda_fire/hexa_cuda tmp_rfc040_realgpu_smoke.hexa 2>&1
  echo "SMOKE_RC=$?"
  kill $SMI1 2>/dev/null
  echo "=== smoke nvidia-smi peak (util desc top5) ==="
  sort -t, -k1 -rn smi_smoke.csv | head -5
  echo "=== d_corpus_fire_a100 d=384x6L seed=43 (nvidia-smi sampled) ==="
  rm -f smi_fire.csv
  ( for k in $(seq 1 1200); do nvidia-smi --query-gpu=utilization.gpu,memory.used,power.draw --format=csv,noheader >> smi_fire.csv; sleep 2; done ) &
  SMI2=$!
  FIRE_T0=$(date +%s)
  HEXA_MEM_UNLIMITED=1 /workspace/cuda_fire/hexa_cuda d_corpus_fire_a100.hexa 2>&1
  FRC=$?
  FIRE_T1=$(date +%s)
  echo "FIRE_RC=$FRC"
  echo "FIRE_WALL_SEC=$((FIRE_T1-FIRE_T0))"
  kill $SMI2 2>/dev/null
  echo "=== fire nvidia-smi peak (util desc top8) ==="
  sort -t, -k1 -rn smi_fire.csv | head -8
  echo "ALLDONE"' 2>&1 | tee "$LOCAL_DIR/a100_session.log"

echo "[7/8] Harvest result.json from session log; pull aux logs..."
SAVE_POD=1
python3 - "$LOCAL_DIR/a100_session.log" "$LOCAL_DIR/result.json" "$OFFER_ID" "$OFFER_DPH" "$OFFER_GPU" "$INSTANCE_ID" <<'PYEOF'
import json,sys,re
log,out,oid,dph,gpu,iid = sys.argv[1:7]
txt=open(log,encoding='utf-8',errors='replace').read()
m=re.search(r'RESULT_JSON\s+(\{.*\})', txt)
res={}
if m:
    try: res=json.loads(m.group(1))
    except Exception as e: res={"parse_err":str(e),"raw":m.group(1)}
smoke=re.search(r'RFC040 REAL-GPU smoke:\s*(\d+)/(\d+)\s*PASS', txt)
wall=re.search(r'FIRE_WALL_SEC=(\d+)', txt)
frc=re.search(r'FIRE_RC=(\d+)', txt)
util=[]
for mm in re.finditer(r'(\d+)\s*%,\s*(\d+)\s*MiB', txt):
    util.append(int(mm.group(1)))
out_obj={
  "phase":"D-a100-retry","seed":43,
  "offer_id":oid,"dph_usd":float(dph),"gpu":gpu,"instance_id":iid,
  "rfc040_smoke": (f"{smoke.group(1)}/{smoke.group(2)}" if smoke else "UNKNOWN"),
  "rfc040_smoke_pass": bool(smoke and smoke.group(1)==smoke.group(2)),
  "fire_rc": (int(frc.group(1)) if frc else None),
  "fire_wall_sec": (int(wall.group(1)) if wall else None),
  "nvidia_smi_util_max_pct": (max(util) if util else None),
  "fire": res,
}
json.dump(out_obj,open(out,'w'),indent=2)
print("result.json written:", json.dumps(out_obj)[:600])
PYEOF
pull() {
  local s="$1" d="$2" t=0
  while [ $t -lt 3 ]; do
    $SCP_CMD "root@$SSH_HOST:$s" "$d" 2>&1 && { echo "  pulled $s"; return 0; }
    t=$((t+1)); echo "  retry $t/3 $s"; [ $t -lt 3 ] && sleep 15
  done
  echo "  PULL-FAIL $s (result already harvested from session log)"; return 1
}
pull /workspace/cuda_fire/smi_fire.csv  "$LOCAL_DIR/nvidia_smi_fire_a100.csv" || true
pull /workspace/cuda_fire/smi_smoke.csv "$LOCAL_DIR/nvidia_smi_smoke_a100.csv" || true

echo "[8/8] Destroy instance (result captured regardless)..."
$VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
SAVE_POD=1
orphan_watchdog "none" || true

echo "=== ${PHASE_ID} DONE ==="
date -u
cat "$LOCAL_DIR/result.json" 2>/dev/null || echo "(no result.json)"
echo "DONE_A100"
