#!/usr/bin/env bash
# d768 GPU fire — FAST variant (3 epochs x 8 windows) for the CE-descent + .clm
# artifact. The util characteristic is IDENTICAL to the 12-epoch run (host-bound,
# forge-on-GPU); fewer steps only bounds wall-time. Reuses the already-built
# GPU-linked d768 binary on the pod.
set -uo pipefail
SRC=/root/.hx/src
export HEXA_LANG=$SRC PATH=/root/.hx/bin:$PATH
cd $SRC
WORK=/workspace/laneg_d768; mkdir -p $WORK
CORPUS=$SRC/stdlib/flame/testdata/clm_semantic_parallel.txt
CLM_BIN=$WORK/clm_d768
[ -x "$CLM_BIN" ] || { echo "FATAL: no d768 binary (run laneg_d768_run.sh build first)"; exit 3; }
echo "d768 binary cuda libs: $(ldd "$CLM_BIN" 2>/dev/null | grep -ciE 'cublas|cudart|libcuda')"

export CLM_PROD_CORPUS=$CORPUS CLM_PROD_D=768 CLM_PROD_E=2 CLM_PROD_EPOCHS=3 CLM_PROD_NSAMP=8
export CLM_PROD_OUT=$WORK/d768_5lang_c4.clm
UCSV=$WORK/util_fast.csv; : > $UCSV
( while :; do nvidia-smi --query-gpu=utilization.gpu,utilization.memory,power.draw,clocks.sm --format=csv,noheader,nounits >> $UCSV 2>/dev/null; sleep 0.2; done ) & SAMPLER=$!
RUN_LOG=$WORK/train_fast.log
( cd $SRC && "$CLM_BIN" ) 2>&1 | tee $RUN_LOG
RUN_RC=${PIPESTATUS[0]}
kill $SAMPLER 2>/dev/null; wait $SAMPLER 2>/dev/null

echo "=== artifact + sha256 ==="
if [ -f "$CLM_PROD_OUT" ]; then sha256sum "$CLM_PROD_OUT" | tee $WORK/ckpt.sha256; ls -la "$CLM_PROD_OUT"; else echo "FATAL: no .clm"; fi
echo "=== F-CLM-PROD-DESCENT ==="
grep -E "mean CE|F-CLM-PROD-DESCENT|PASS|FAIL|CLM_PROD_OUT wrote|config d=" $RUN_LOG || true
echo "=== UTIL (n=$(wc -l < $UCSV)) ==="
awk -F',' 'NF>=1{u=$1+0;a[n++]=u;s+=u;if(u>mx)mx=u;if(u>20)g++} END{if(n>0){asort(a);printf "UTIL: n=%d min=%d med=%d max=%d mean=%.3f pct_gt20=%.2f%%\n",n,a[1],a[int(n/2)],mx,s/n,(g*100.0/n)} else print "UTIL n=0"}' $UCSV
echo "=== peak power/clock (GPU-context proxy) ==="; sort -t, -k3 -nr $UCSV | head -2
echo "=== mem peak ==="; sort -t, -k2 -nr $UCSV | head -2
echo "RUN_RC=$RUN_RC"
echo "=== DONE ==="
