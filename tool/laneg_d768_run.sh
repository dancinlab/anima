#!/usr/bin/env bash
# Focused d768 GPU fire — env already provisioned (fresh hexa + cuda seeds +
# nvcc'd runtime_cuda.90.o on the pod). Builds clm_prod at d768 with the forge
# cuBLAS+driver link, then runs with continuous util sampling + .clm save.
set -uo pipefail
SRC=/root/.hx/src
export HEXA_LANG=$SRC
export PATH=/root/.hx/bin:$PATH
cd $SRC
HEXA=/workspace/hexa_fresh
WORK=/workspace/laneg_d768; mkdir -p $WORK
CORPUS=$SRC/stdlib/flame/testdata/clm_semantic_parallel.txt
DVAL=768; EPOCHS=12; EVAL=2; NSAMP=16

echo "=== build d$DVAL with HEXA_CUDA_LINK=1 ==="
rm -rf /root/.hexa-cache/hexa_run.* 2>/dev/null
HEXA_CUDA_LINK=1 timeout 500 $HEXA build stdlib/flame/clm_prod.hexa -o $WORK/clm_d$DVAL > $WORK/build.log 2>&1
grep -E "\[cuda\]|CUDA link ENGAGED|undefined reference|OK: built|FAILED" $WORK/build.log | head

CLM_BIN=$WORK/clm_d$DVAL
if [ ! -x "$CLM_BIN" ]; then
  echo "=== relink with -lcuda (driver API) ==="
  APPC="$(ls -t $SRC/build/artifacts/*.c 2>/dev/null | head -1)"
  RTCUDA_O="$(ls -t $SRC/self/cuda/runtime_cuda.*.o 2>/dev/null | head -1)"
  RTO="$(ls -t /root/.hexa-cache/runtime.*.cuda.o 2>/dev/null | head -1)"
  DRV="$(dirname "$(find / -name 'libcuda.so*' 2>/dev/null | head -1)")"
  echo "  APPC=$APPC"; echo "  RTCUDA_O=$RTCUDA_O"; echo "  RTO=$RTO"; echo "  DRV=$DRV"
  clang -O2 -DHEXA_CUDA -I /usr/local/cuda/include -D_GNU_SOURCE -Wno-trigraphs \
    -fbracket-depth=4096 -I $SRC/self "$APPC" "$RTO" "$RTCUDA_O" -o "$CLM_BIN" \
    -lm -lpthread -L/usr/local/cuda/lib64 -L"$DRV" -lcublas -lcudart -lcuda -ldl -lrt -lstdc++ 2>&1 | tail -6
fi
[ -x "$CLM_BIN" ] || { echo "FATAL: no d$DVAL binary"; exit 3; }
echo "  binary: $CLM_BIN  cuda libs linked: $(ldd "$CLM_BIN" 2>/dev/null | grep -ciE 'cublas|cudart|libcuda')"

echo "=== run d$DVAL E=$EVAL epochs=$EPOCHS with continuous util sampling ==="
export CLM_PROD_CORPUS=$CORPUS CLM_PROD_D=$DVAL CLM_PROD_E=$EVAL CLM_PROD_EPOCHS=$EPOCHS CLM_PROD_NSAMP=$NSAMP
export CLM_PROD_OUT=$WORK/d768_5lang_c4.clm
UCSV=$WORK/util.csv; : > $UCSV
( while :; do nvidia-smi --query-gpu=utilization.gpu,utilization.memory,power.draw,clocks.sm --format=csv,noheader,nounits >> $UCSV 2>/dev/null; sleep 0.2; done ) & SAMPLER=$!
RUN_LOG=$WORK/train.log
( cd $SRC && "$CLM_BIN" ) 2>&1 | tee $RUN_LOG
RUN_RC=${PIPESTATUS[0]}
kill $SAMPLER 2>/dev/null; wait $SAMPLER 2>/dev/null

echo "=== artifact + sha256 ==="
if [ -f "$CLM_PROD_OUT" ]; then sha256sum "$CLM_PROD_OUT" | tee $WORK/ckpt.sha256; ls -la "$CLM_PROD_OUT"; else echo "FATAL: no .clm"; fi

echo "=== F-CLM-PROD-DESCENT ==="
grep -E "mean CE|F-CLM-PROD-DESCENT|PASS|FAIL|CLM_PROD_OUT wrote|config d=" $RUN_LOG || true
echo "=== UTIL (n=$(wc -l < $UCSV)) ==="
awk -F',' 'NF>=1{u=$1+0;a[n++]=u;s+=u;if(u>mx)mx=u;if(u>20)g++} END{if(n>0){asort(a);printf "UTIL: n=%d min=%d med=%d max=%d mean=%.2f pct_gt20=%.1f%%\n",n,a[1],a[int(n/2)],mx,s/n,(g*100.0/n)} else print "UTIL n=0"}' $UCSV
echo "=== top util samples ==="; sort -t, -k1 -nr $UCSV | head -8
echo "=== peak power/clock (forge GPU activity proxy) ==="; sort -t, -k3 -nr $UCSV | head -3
echo "RUN_RC=$RUN_RC"
echo "=== DONE ==="
