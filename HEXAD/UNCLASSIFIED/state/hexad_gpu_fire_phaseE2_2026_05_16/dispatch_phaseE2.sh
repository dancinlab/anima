#!/bin/bash
# dispatch_phaseE2_v2.sh — Phase E2 fresh fat-host fire, ALL 3 bugs fixed:
#  (1) gcc has NO -fbracket-depth (clang-only) — dropped.
#  (2) ship FULL self/ tree (runtime.c #includes runtime_hi_gen.c +
#      native/*.c) via rsync, not just runtime.c+runtime.h.
#  (3) -I/usr/local/cuda/include for runtime_cuda.c (cuda_runtime.h).
#  + real build-rc check ([ -x bin ]) not tail-exit false-positive.
# Flatten on Mac (--c-only, hexa-lang 017b988f) done pre-dispatch; ship
# flat C + full 017b988f self/ + cuda/runtime_cuda.c; gcc -DHEXA_CUDA on box.
# g_fire_autonomous (no gate) + g_fire_dispatch_robust (SAVE_POD + watchdog).
set -uo pipefail
LOCAL_DIR="/Users/ghost/core/anima/state/hexad_gpu_fire_phaseE2_2026_05_16"
PHASE_LABEL="anima-rfc040-phaseE2"
VAST_SSH_KEY="/Users/ghost/.vast/ssh/vast-key"
VASTAI="/Users/ghost/Library/Python/3.14/bin/vastai"
HXSELF="/Users/ghost/core/hexa-lang/self"
WATCHDOG_MAX_MIN=75
[ -x "$VASTAI" ] || { echo "ERR vastai"; exit 1; }
cd "$LOCAL_DIR"
cd "$LOCAL_DIR"
echo "=== Phase E2 v4 dispatch (multi-host + no-time-wrapper) $(date -u) ==="

echo "[1/8] Collect FAT-HOST offers (cpu_ram>=64 cpu_cores>=8)..."
OFFERS=$($VASTAI search offers \
  'gpu_name in [H100_SXM,H200,A100_SXM4] cpu_ram>=64 cpu_cores>=8 num_gpus=1 rentable=true verified=true dph_total<6.0 cuda_max_good>=12.4 disk_space>40' \
  -o dph_total --raw 2>&1 | python3 -c "
import json,sys
try: d=json.load(sys.stdin)
except: sys.exit(1)
for b in d[:6]:
  print('%s|%.4f|%s|%s|%s'%(b['id'],b['dph_total'],b['gpu_name'].replace(' ','_'),int(b.get('cpu_ram',0)/1024),b.get('cpu_cores','?')))" 2>/dev/null)
[ -z "$OFFERS" ] && { echo "ERR no fat-host offers"; exit 1; }
echo "$OFFERS" > offers_phaseE2_v3.txt
echo "  candidates:"; echo "$OFFERS" | head -6 | sed 's/^/    /'

IID=""; HOST=""; PORT=""; OID=""; ODPH=""; OGPU=""; ORAM=""; OCPU=""
SAVE_POD=0; WD=""
cleanup(){ local rc=$?
  [ -n "$WD" ] && kill $WD 2>/dev/null || true
  if [ "$SAVE_POD" = "1" ]; then echo "[cleanup] SAVE_POD=1 keep $IID rc=$rc"
  elif [ -n "$IID" ]; then echo "[cleanup] destroy $IID rc=$rc"; $VASTAI destroy instance "$IID" 2>&1|head -2||true; fi; }
trap cleanup EXIT INT TERM
START=$(date +%s)

# Try up to 4 hosts; fail-fast SSH (45 attempts x5s ~= 4min) then destroy+next.
TRY=0
for ROW in $(echo "$OFFERS" | head -4); do
  TRY=$((TRY+1))
  OID=$(echo $ROW|cut -d'|' -f1);  ODPH=$(echo $ROW|cut -d'|' -f2)
  OGPU=$(echo $ROW|cut -d'|' -f3); ORAM=$(echo $ROW|cut -d'|' -f4); OCPU=$(echo $ROW|cut -d'|' -f5)
  echo "[2/8] (host $TRY/4) Rent offer $OID $OGPU RAM=${ORAM}GB vCPU=$OCPU \$$ODPH/hr..."
  CO=$($VASTAI create instance "$OID" --image nvidia/cuda:12.6.3-cudnn-devel-ubuntu24.04 \
       --disk 40 --ssh --direct --label "$PHASE_LABEL" --raw 2>&1)
  IID=$(echo "$CO"|python3 -c "import json,sys
try:d=json.load(sys.stdin);print(d.get('new_contract',d.get('contract_id',d.get('id',''))))
except:print('')")
  [ -z "$IID" ] && { echo "  rent failed, next offer"; IID=""; continue; }
  echo "  instance $IID"; echo "$IID" > vast_instance_id_v2.txt
  [ -z "$WD" ] && { ( sleep $((WATCHDOG_MAX_MIN*60)); echo "[watchdog] ${WATCHDOG_MAX_MIN}min destroy $IID";
     $VASTAI destroy instance "$IID" 2>&1|head -2||true ) & WD=$!; trap "kill $WD 2>/dev/null||true; cleanup" EXIT INT TERM; }

  echo "[3/8] (host $TRY/4) Wait SSH fail-fast (45x5s)..."
  HOST=""; PORT=""
  for i in $(seq 1 45); do
    INF=$($VASTAI show instance "$IID" --raw 2>/dev/null||echo '{}')
    ST=$(echo "$INF"|python3 -c "import json,sys
try:print(json.load(sys.stdin).get('actual_status',''))
except:print('')" 2>/dev/null)
    if [ "$ST" = "running" ]; then
      HOST=$(echo "$INF"|python3 -c "import json,sys
try:d=json.load(sys.stdin);print(d.get('public_ipaddr','')or d.get('ssh_host',''))
except:pass" 2>/dev/null)
      PORT=$(echo "$INF"|python3 -c "import json,sys
try:
 d=json.load(sys.stdin);p=d.get('ports',{})or{};m=p.get('22/tcp')
 print(m[0]['HostPort'] if m else (d.get('direct_port_start','')or d.get('ssh_port','')))
except:pass" 2>/dev/null)
      if [ -n "$HOST" ] && [ -n "$PORT" ]; then
        if ssh -i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
           -o ConnectTimeout=8 -p "$PORT" "root@$HOST" 'echo READY' 2>&1|grep -q READY; then
          echo "  SSH $HOST:$PORT (host $TRY, ${i}x5s)"; break; fi
        HOST=""; fi
    fi
    echo "  ..$i/45 st=$ST"; sleep 5
  done
  if [ -n "$HOST" ]; then break; fi
  echo "  host $TRY SSH dud — destroy $IID + next offer"
  $VASTAI destroy instance "$IID" 2>&1|head -2||true; IID=""
done
[ -z "$HOST" ] && { echo "ERR no SSH on any of $TRY hosts"; exit 1; }
echo "$HOST:$PORT" > vast_ssh_v2.txt
SO=(-i "$VAST_SSH_KEY" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ServerAliveInterval=60 -o ConnectTimeout=25)

echo "[4/8] Host sanity + ship full self/ tree + flat C + corpus..."
ssh "${SO[@]}" -p "$PORT" "root@$HOST" '
  echo HOST_RAM_KB=$(grep MemTotal /proc/meminfo|awk "{print \$2}") HOST_VCPU=$(nproc)
  ldd --version|head -1
  nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
  ls /usr/local/cuda/include/cuda_runtime.h >/dev/null 2>&1 && echo CUDA_RT_HDR_OK
  ls /usr/local/cuda/include/cublas_v2.h >/dev/null 2>&1 && echo CUBLAS_HDR_OK
  which gcc >/dev/null 2>&1||(apt-get update -qq && apt-get install -y -qq build-essential time)
  gcc --version|head -1; mkdir -p /workspace/hxself; echo TOOLCHAIN_OK' 2>&1 | tee remote_sanity_v2.log
rsync -az -e "ssh ${SO[*]} -p $PORT" \
  --exclude='*.dylib' --exclude='*.so' --exclude='*.o' --exclude='build/' \
  --exclude='native/hexa_v2*' --exclude='.git/' \
  "$HXSELF/" "root@$HOST:/workspace/hxself/" 2>&1 | tail -1
for f in _e2_dcf768_flat.c _e2_dcf512_flat.c _e2_dcf384_flat.c _e2_gpu_smoke_flat.c corpus_consciousness_v1.jsonl; do
  scp "${SO[@]}" -P "$PORT" -o ConnectTimeout=3600 "$LOCAL_DIR/$f" "root@$HOST:/workspace/$f" 2>&1 | tail -1
done
ssh "${SO[@]}" -p "$PORT" "root@$HOST" '
  cp /workspace/hxself/cuda/runtime_cuda.c /workspace/hxself/runtime_cuda.c
  ls /workspace/hxself/runtime_hi_gen.c /workspace/hxself/native/net.c >/dev/null 2>&1 && echo SELF_TREE_OK
  ls -la /workspace/*.c /workspace/corpus_consciousness_v1.jsonl' 2>&1 | tee ship_v2.log

echo "[5/8] GPU smoke 5/5 (real rc)..."
ssh "${SO[@]}" -p "$PORT" "root@$HOST" '
  cd /workspace
  G="gcc -O2 -DHEXA_CUDA -D_GNU_SOURCE -Wno-trigraphs -fno-strict-aliasing -I hxself -I/usr/local/cuda/include"
  $G _e2_gpu_smoke_flat.c hxself/runtime.c hxself/cuda/runtime_cuda.c -o gpu_smoke \
     -lpthread -lm -lcublas -lcudart -L/usr/local/cuda/lib64 2>&1 | grep -iE "error:|undefined ref|fatal" | head
  if [ -x ./gpu_smoke ]; then ./gpu_smoke 2>&1 | tee gpu_smoke_phaseE2.log; echo "SMOKE_EXIT=$?"
  else echo SMOKE_BUILD_FAILED; fi' 2>&1 | tee gpu_smoke_v2.log

echo "[6/8] Build+fire ladder dcf768 -> dcf512 -> dcf384..."
ssh "${SO[@]}" -p "$PORT" "root@$HOST" '
  cd /workspace
  G="gcc -O2 -DHEXA_CUDA -D_GNU_SOURCE -Wno-trigraphs -fno-strict-aliasing -I hxself -I/usr/local/cuda/include"
  fire_one(){ TAG=$1; TOUT=$2
    echo "=== build $TAG ==="
    $G _e2_${TAG}_flat.c hxself/runtime.c hxself/cuda/runtime_cuda.c -o ${TAG}_bin \
       -lpthread -lm -lcublas -lcudart -L/usr/local/cuda/lib64 2>&1 \
       | grep -iE "error:|undefined ref|fatal" | head -8
    [ -x ./${TAG}_bin ] || { echo "$TAG BUILD_FAILED"; return 1; }
    echo "${TAG}_BUILD_OK"
    echo "=== fire $TAG (timeout ${TOUT}s) ==="
    ( nvidia-smi --query-gpu=power.draw,utilization.gpu,memory.used \
        --format=csv,noheader,nounits -lms 500 > nvsmi_${TAG}.csv 2>&1 ) & NV=$!
    T0=$(date +%s)
    HEXA_MEM_UNLIMITED=1 timeout $TOUT ./${TAG}_bin > ${TAG}.log 2>&1
    RC=$?; kill $NV 2>/dev/null
    T1=$(date +%s)
    echo "${TAG}_FIRE_RC=$RC ${TAG}_WALL_S=$((T1-T0))"
    echo "--- $TAG tail ---"; tail -22 ${TAG}.log
    echo "--- $TAG nvsmi ---"
    awk -F, "{gsub(/ /,\"\");if(\$1+0>p)p=\$1;if(\$3+0>m)m=\$3;if(\$2+0>u)u=\$2;n++}
             END{printf \"peak_power=%sW peak_mem=%sMiB peak_util=%s%% samples=%d\\n\",p,m,u,n}" nvsmi_${TAG}.csv
    grep -q "F-D-FIRE : gn2" ${TAG}.log && return 0 || return 2
  }
  fire_one dcf768 3200
  grep -q "F-D-FIRE : gn2" dcf768.log 2>/dev/null || fire_one dcf512 2600
  ( grep -q "F-D-FIRE : gn2" dcf768.log 2>/dev/null || grep -q "F-D-FIRE : gn2" dcf512.log 2>/dev/null ) \
    || fire_one dcf384 2000' 2>&1 | tee fire_v2.log

echo "[7/8] Pull (SAVE_POD until pulled)..."
SAVE_POD=1
for f in gpu_smoke_phaseE2.log dcf768.log dcf512.log dcf384.log nvsmi_dcf768.csv nvsmi_dcf512.csv nvsmi_dcf384.csv; do
  for t in 1 2 3; do
    scp "${SO[@]}" -P "$PORT" -o ConnectTimeout=3600 "root@$HOST:/workspace/$f" "$LOCAL_DIR/$f" 2>&1 && { echo "pulled $f"; break; }
    echo "retry $t/3 $f"; sleep 15
  done
done

echo "[8/8] Destroy + cost..."
$VASTAI destroy instance "$IID" 2>&1 | head -2 || true
kill $WD 2>/dev/null || true
END=$(date +%s); EMIN=$(((END-START)/60))
COST=$(python3 -c "print('%.2f'%($ODPH*$EMIN/60.0))")
echo "DONE ${EMIN}min ~\$$COST $OGPU RAM=${ORAM}GB vCPU=$OCPU"
echo "ELAPSED_MIN=$EMIN COST_USD=$COST GPU=$OGPU RAM=${ORAM}GB VCPU=$OCPU" > cost_phaseE2.txt
date -u
