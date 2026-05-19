#!/bin/bash
# state/hexad_gpu_fire_phaseE_2026_05_16/dispatch_phaseE.sh
# RFC 040 Phase E — d_train5 GPU-routed d_corpus_fire fire.
#
# Phase D (LANDED) proved the cuBLAS substrate (F-RFC040 5/5, 51 TFLOPS FP64)
# but d_train5 was pure-hexa CPU (nvidia-smi 0-2%, GPU never in training loop).
# Phase E refactored d5_attn_fwd/d5_block_fwd/d5_forward dominant matmuls
# (Q/K/V/O batched proj + batched SwiGLU + tied LM head) → farr_matmul_gpu.
# CPU-equivalence already PROVEN on Mac (no-CUDA → CPU farr_matmul): boxed
# baseline gn2 7.97116→3.73374e-07, acc 0→8/8 reproduced BIT-EQUAL.
#
# This fire: GLIBC>=2.38 image (Ubuntu 24.04 — the KNOWN BLOCKER fix for the
# import-flattener), build hexa -DHEXA_CUDA from rfc/farr-gpu-cuda-backend
# @903c0285, GPU smoke 5/5 sanity, then d_corpus_fire d=768·12L GPU-routed
# with `nvidia-smi dmon` during (GPU Util > 20% = THE Phase E proof).
#
# AGENTS.tape g_fire_autonomous: fully autonomous. g_fire_dispatch_robust:
# SAVE_POD retain + pull retry. Orphan-watchdog: auto-destroy > 75 min.

set -uo pipefail

PHASE_ID="hexad_gpu_fire_phaseE"
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_phaseE_2026_05_16"
PHASE_LABEL="anima-rfc040-phaseE-h100"
VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
WATCHDOG_MAX_MIN=75

[ -x "$VASTAI" ]      || { echo "ERROR: vastai CLI missing"; exit 1; }
[ -f "$VAST_SSH_KEY" ] || { echo "ERROR: vast ssh key missing"; exit 1; }
mkdir -p "$LOCAL_DIR"
cd "$LOCAL_DIR"
echo "=== ${PHASE_ID} dispatch (RFC 040 Phase E, 2026-05-16) ==="
date -u

# ── 1) Search GPU offer (H100 preferred; A100_SXM4 step-down — wall-time
#       first, autonomous; both proven cuBLAS-capable for Phase E) ───────
echo "[1/9] Searching GPU offer (H100 SXM/PCIE/NVL preferred, A100_SXM4 fallback)..."
OFFER_PARSED=""
for Q in \
  'gpu_name in [H100_SXM,H100_PCIE,H100_NVL,H200] num_gpus=1 rentable=true verified=true dph_total<6.0 cuda_max_good>=12.4 disk_space>40 inet_down>200' \
  'gpu_name=A100_SXM4 num_gpus=1 rentable=true verified=true dph_total<3.0 cuda_max_good>=12.4 disk_space>40 inet_down>200' ; do
  OJ=$($VASTAI search offers "$Q" -o dph_total --raw 2>&1)
  OP=$(echo "$OJ" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: sys.exit(1)
if not d: sys.exit(1)
b=d[0]
print('%s %.4f %s %s' % (b['id'], b['dph_total'], b['gpu_name'].replace(' ','_'), b.get('cuda_max_good','?')))
" 2>/dev/null)
  if [ -n "$OP" ]; then OFFER_PARSED="$OP"; break; fi
  echo "  no offers for: $Q"
done
[ -z "$OFFER_PARSED" ] && { echo "ERROR: no GPU offers"; exit 1; }
OFFER_ID=$(echo "$OFFER_PARSED" | awk '{print $1}')
OFFER_DPH=$(echo "$OFFER_PARSED" | awk '{print $2}')
OFFER_GPU=$(echo "$OFFER_PARSED" | awk '{print $3}')
OFFER_CUDA=$(echo "$OFFER_PARSED" | awk '{print $4}')
echo "  Selected: id=$OFFER_ID dph=\$$OFFER_DPH gpu=$OFFER_GPU cuda=$OFFER_CUDA"
echo "$OFFER_PARSED" > offer_phaseE.txt

# ── 2) Rent — Ubuntu 24.04 CUDA devel image (GLIBC 2.39 ≥ 2.38, the
#       import-flattener fix; devel = cuBLAS headers preinstalled) ───────
echo "[2/9] Renting with nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04 (GLIBC 2.39)..."
CREATE_OUT=$($VASTAI create instance "$OFFER_ID" \
    --image nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04 \
    --disk 40 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
INSTANCE_ID=$(echo "$CREATE_OUT" | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: sys.stderr.write('parse_fail: '+sys.stdin.read()+'\n'); sys.exit(1)
print(d.get('new_contract', d.get('contract_id', d.get('id',''))))
")
[ -z "$INSTANCE_ID" ] && { echo "ERROR: instance id parse failed: $CREATE_OUT"; exit 1; }
echo "  Instance ID: $INSTANCE_ID"
echo "$INSTANCE_ID" > vast_instance_id.txt
START_TS=$(date +%s)

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

# Orphan watchdog: hard-destroy after WATCHDOG_MAX_MIN regardless of state
( sleep $((WATCHDOG_MAX_MIN*60))
  echo "[watchdog] ${WATCHDOG_MAX_MIN}min elapsed — force-destroying $INSTANCE_ID (death != cost bleed)"
  $VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true ) &
WATCHDOG_PID=$!
trap "kill $WATCHDOG_PID 2>/dev/null || true; cleanup" EXIT INT TERM

# ── 3) Wait for SSH ──────────────────────────────────────────────────
echo "[3/9] Waiting for SSH (max ~13 min)..."
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

# ── 4) GLIBC + CUDA sanity (resolve BLOCKER first) ───────────────────
echo "[4/9] GLIBC>=2.38 + CUDA sanity (the import-flattener blocker check)..."
$SSH_CMD 'set +e
  ldd --version | head -1
  GLIBC=$(ldd --version | head -1 | grep -oE "[0-9]+\.[0-9]+$")
  echo "GLIBC=$GLIBC"
  python3 - <<PYEOF
g="$GLIBC".split(".")
ok = (int(g[0]),int(g[1])) >= (2,38)
print("GLIBC_OK" if ok else "GLIBC_TOO_OLD")
PYEOF
  nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
  ls /usr/local/cuda/include/cublas_v2.h && echo "cublas_v2.h PRESENT"
  ls /usr/local/cuda/lib64/libcublas.so* 2>/dev/null | head -1
  which git clang gcc make >/dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq git clang build-essential)
  clang --version | head -1
  echo TOOLCHAIN_OK' 2>&1 | tee remote_sanity_phaseE.log

if ! grep -q "GLIBC_OK" remote_sanity_phaseE.log; then
    echo "[FATAL] GLIBC < 2.38 on box despite ubuntu24.04 — SAVE_POD=1 for inspection"
    SAVE_POD=1
    exit 1
fi

# ── 5) Bootstrap hexa.real from local 903c0285 (transpiled-C path) ──
# hexa_v2 is Mac arm64 → transpile MUST be Mac-side (done pre-dispatch:
# /tmp/hexa_main.c + /tmp/hexa_full.c from rfc/farr-gpu-cuda-backend
# @903c0285). We rsync the 903c0285 self/ (HEXA_CUDA gate in main.hexa +
# cuBLAS body in runtime.c) + runtime_cuda.c, gcc hexa.real on the box,
# then `HEXA_CUDA=1 hexa build` adds -DHEXA_CUDA + cuBLAS link line.
echo "[5/9] Ship 903c0285 self/ + transpiled C + refactored anima files..."
$SSH_CMD 'mkdir -p /root/core/hexa-lang/build /root/.hx/bin /workspace/anima'
rsync -az -e "ssh $SSH_OPTS -p $SSH_PORT" \
    --exclude='*.dylib' --exclude='*.so' --exclude='build/' \
    --exclude='archive/' --exclude='.git/' --exclude='native/hexa_v2*' \
    /Users/ghost/core/hexa-lang/self/ "root@$SSH_HOST:/root/core/hexa-lang/self/" 2>&1 | tail -1
$SCP_CMD /tmp/hexa_main.c "root@$SSH_HOST:/root/core/hexa-lang/build/hexa_main.c"
$SCP_CMD /tmp/hexa_full.c "root@$SSH_HOST:/root/core/hexa-lang/build/hexa_full.c"
$SCP_CMD "$LOCAL_DIR/anima_phaseE_files.tgz" "root@$SSH_HOST:/workspace/anima/"

echo "[5b/9] gcc hexa.real on box + place runtime_cuda.c, unpack anima..."
$SSH_CMD 'set +e
  cd /root/core/hexa-lang
  # build gate expects runtime_cuda.c NEXT TO runtime.c
  cp self/cuda/runtime_cuda.c self/runtime_cuda.c && echo RUNTIME_CUDA_COPIED
  mkdir -p $HOME/.hx/bin
  echo "[remote] gcc -> ~/.hx/bin/hexa.real"
  gcc -O2 -D_GNU_SOURCE -Wno-trigraphs -I self -I . \
      build/hexa_main.c -o $HOME/.hx/bin/hexa.real -lm 2>&1 | tail -3
  echo HEXA_REAL_RC=$?
  printf "#!/bin/bash\nexec \$HOME/.hx/bin/hexa.real \"\$@\"\n" > $HOME/.hx/bin/hexa
  chmod +x $HOME/.hx/bin/hexa
  export PATH=$HOME/.hx/bin:$PATH
  $HOME/.hx/bin/hexa --version 2>&1 | head -1
  cd /workspace/anima && tar xzf anima_phaseE_files.tgz && echo ANIMA_UNPACKED
  ls HEXAD/D/d_corpus_fire.hexa training/corpus_consciousness_v1.jsonl' 2>&1 | tee bootstrap_phaseE.log

# ── 5c) GPU smoke 5/5 sanity (the box check) ─────────────────────────
echo "[5c/9] GPU smoke 5/5 sanity (HEXA_CUDA build of tmp_rfc040_gpu_smoke)..."
$SSH_CMD 'set +e
  export PATH=$HOME/.hx/bin:$PATH
  export HEXA_CUDA=1
  cd /root/core/hexa-lang
  $HOME/.hx/bin/hexa build tmp_rfc040_gpu_smoke.hexa -o /workspace/gpu_smoke 2>&1 | tail -6
  echo SMOKE_BUILD_RC=$?
  /workspace/gpu_smoke 2>&1 | tee /workspace/gpu_smoke_phaseE.log
  echo SMOKE_RC=$?' 2>&1 | tee gpu_smoke_build_phaseE.log

# ── 6) d_corpus_fire d=768·12L GPU-routed (scale knobs sed-patched) ──
echo "[6/9] Build d_corpus_fire -DHEXA_CUDA at d=768·12L, fire GPU-routed..."
$SSH_CMD 'set +e
  export PATH=$HOME/.hx/bin:$PATH
  export HEXA_CUDA=1
  cd /root/core/hexa-lang
  A=/workspace/anima/HEXAD/D
  # absolute imports in anima files point at /Users/ghost — rewrite to box
  for f in d_corpus_fire d_train5_lib d_train4_lib d_train3_lib d_train2_lib d_train_lib corpus_loader_lib; do
    sed -i "s#/Users/ghost/core/anima#/workspace/anima#g" $A/$f.hexa
  done
  sed -i "s#/Users/ghost/core/anima/training#/workspace/anima/training#g" $A/d_corpus_fire.hexa
  # d=768 nh=12 nkv=4 hd=64 h=2048 T=128 n_layer=12 steps=80 seed=42
  sed -i "s/^    let d = 32\$/    let d = 768/"          $A/d_corpus_fire.hexa
  sed -i "s/^    let nh = 4\$/    let nh = 12/"           $A/d_corpus_fire.hexa
  sed -i "s/^    let nkv = 2\$/    let nkv = 4/"          $A/d_corpus_fire.hexa
  sed -i "s/^    let h = 64\$/    let h = 2048/"          $A/d_corpus_fire.hexa
  sed -i "s/^    let T = 16\$/    let T = 128/"           $A/d_corpus_fire.hexa
  sed -i "s/^    let n_layer = 3\$/    let n_layer = 12/" $A/d_corpus_fire.hexa
  grep -nE "let d = |let nh = |let nkv = |let h = |let T = |let n_layer = |let steps = " $A/d_corpus_fire.hexa | head
  $HOME/.hx/bin/hexa build $A/d_corpus_fire.hexa -o /workspace/d_corpus_fire_768 2>&1 | tail -8
  echo DCF768_BUILD_RC=$?
  ls -la /workspace/d_corpus_fire_768 2>/dev/null
  # step-down configs prepared if d=768 OOM/too-slow
  cp $A/d_corpus_fire.hexa $A/d_corpus_fire_512.hexa
  sed -i "s/^    let d = 768\$/    let d = 512/; s/^    let n_layer = 12\$/    let n_layer = 8/; s/^    let h = 2048\$/    let h = 1536/" $A/d_corpus_fire_512.hexa
  cp $A/d_corpus_fire.hexa $A/d_corpus_fire_384.hexa
  sed -i "s/^    let d = 768\$/    let d = 384/; s/^    let n_layer = 12\$/    let n_layer = 6/; s/^    let h = 2048\$/    let h = 1024/; s/^    let nh = 12\$/    let nh = 6/" $A/d_corpus_fire_384.hexa' 2>&1 | tee dcf_build_phaseE.log

echo "[6b/9] Fire d=768·12L + nvidia-smi dmon (GPU Util > 20% = THE proof)..."
$SSH_CMD 'set +e
  export PATH=$HOME/.hx/bin:$PATH
  cd /workspace
  if [ -x /workspace/d_corpus_fire_768 ]; then
    ( nvidia-smi dmon -s u -d 2 -c 900 > /workspace/nvidia_dmon_phaseE.txt 2>&1 ) &
    DMON=$!
    timeout 2400 /usr/bin/time -v /workspace/d_corpus_fire_768 > /workspace/d_corpus_fire_768.log 2>&1
    echo FIRE768_RC=$?
    kill $DMON 2>/dev/null
    echo "--- d=768·12L fire log tail ---"; tail -22 /workspace/d_corpus_fire_768.log
    echo "--- nvidia dmon (sm-util) peak ---"
    awk "NR>2 && \$2 ~ /^[0-9]+\$/ {print \$2}" /workspace/nvidia_dmon_phaseE.txt | sort -n | tail -5
    echo "--- wall/rss ---"; grep -E "Elapsed|Maximum resident" /workspace/d_corpus_fire_768.log | tail -2
  else
    echo "d=768·12L build FAILED — see dcf_build_phaseE.log"
  fi
  # Step-down ladder if d=768 did not produce a final gn2 line
  if ! grep -q "F-D-FIRE : gn2" /workspace/d_corpus_fire_768.log 2>/dev/null; then
    echo "=== d=768·12L incomplete — step down to d=512·8L ==="
    export HEXA_CUDA=1
    cd /root/core/hexa-lang
    $HOME/.hx/bin/hexa build /workspace/anima/HEXAD/D/d_corpus_fire_512.hexa -o /workspace/dcf_512 2>&1 | tail -3
    if [ -x /workspace/dcf_512 ]; then
      cd /workspace
      ( nvidia-smi dmon -s u -d 2 -c 900 > /workspace/nvidia_dmon_512.txt 2>&1 ) & DMON=$!
      timeout 2000 /usr/bin/time -v /workspace/dcf_512 > /workspace/dcf_512.log 2>&1
      echo FIRE512_RC=$?; kill $DMON 2>/dev/null
      tail -22 /workspace/dcf_512.log
      awk "NR>2 && \$2 ~ /^[0-9]+\$/ {print \$2}" /workspace/nvidia_dmon_512.txt | sort -n | tail -5
    fi
  fi
  if ! grep -q "F-D-FIRE : gn2" /workspace/dcf_512.log 2>/dev/null && ! grep -q "F-D-FIRE : gn2" /workspace/d_corpus_fire_768.log 2>/dev/null; then
    echo "=== d=512 also incomplete — step down to d=384·6L ==="
    export HEXA_CUDA=1
    cd /root/core/hexa-lang
    $HOME/.hx/bin/hexa build /workspace/anima/HEXAD/D/d_corpus_fire_384.hexa -o /workspace/dcf_384 2>&1 | tail -3
    if [ -x /workspace/dcf_384 ]; then
      cd /workspace
      ( nvidia-smi dmon -s u -d 2 -c 900 > /workspace/nvidia_dmon_384.txt 2>&1 ) & DMON=$!
      timeout 1800 /usr/bin/time -v /workspace/dcf_384 > /workspace/dcf_384.log 2>&1
      echo FIRE384_RC=$?; kill $DMON 2>/dev/null
      tail -22 /workspace/dcf_384.log
      awk "NR>2 && \$2 ~ /^[0-9]+\$/ {print \$2}" /workspace/nvidia_dmon_384.txt | sort -n | tail -5
    fi
  fi' 2>&1 | tee dcf_fire_phaseE.log

# ── 7) Pull artifacts ────────────────────────────────────────────────
echo "[7/9] Pull artifacts..."
SAVE_POD=1
pull() {
  local s="$1" d="$2" t=0
  while [ $t -lt 3 ]; do
    if $SCP_CMD "root@$SSH_HOST:$s" "$d" 2>&1; then echo "  pulled $s"; return 0; fi
    t=$((t+1)); echo "  retry $t/3 $s"; [ $t -lt 3 ] && sleep 20
  done
  echo "  PULL FAIL $s"; return 1
}
pull /workspace/gpu_smoke_phaseE.log        "$LOCAL_DIR/gpu_smoke_phaseE.log" || true
pull /workspace/d_corpus_fire_768.log       "$LOCAL_DIR/d_corpus_fire_768.log" || true
pull /workspace/nvidia_dmon_phaseE.txt      "$LOCAL_DIR/nvidia_dmon_phaseE.txt" || true
pull /workspace/dcf_512.log                 "$LOCAL_DIR/dcf_512.log" || true
pull /workspace/nvidia_dmon_512.txt         "$LOCAL_DIR/nvidia_dmon_512.txt" || true
pull /workspace/dcf_384.log                 "$LOCAL_DIR/dcf_384.log" || true
pull /workspace/nvidia_dmon_384.txt         "$LOCAL_DIR/nvidia_dmon_384.txt" || true

# ── 8) Destroy + summary ─────────────────────────────────────────────
echo "[8/9] Destroy instance $INSTANCE_ID..."
$VASTAI destroy instance "$INSTANCE_ID" 2>&1 | head -3 || true
kill $WATCHDOG_PID 2>/dev/null || true
END_TS=$(date +%s)
ELAPSED_MIN=$(( (END_TS - START_TS) / 60 ))
COST=$(python3 -c "print('%.2f' % ($OFFER_DPH * $ELAPSED_MIN / 60.0))")
echo "[9/9] DONE — elapsed ${ELAPSED_MIN}min, ~\$$COST on $OFFER_GPU (\$$OFFER_DPH/hr)"
echo "ELAPSED_MIN=$ELAPSED_MIN COST_USD=$COST GPU=$OFFER_GPU" > cost_phaseE.txt
date -u
