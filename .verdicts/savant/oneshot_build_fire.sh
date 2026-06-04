#!/usr/bin/env bash
# SAVANT-7B rung0 — ONE-SHOT build+fire (all 5 blockers pre-solved). Runs detached on pod.
set -uo pipefail
exec > /workspace/oneshot.log 2>&1
echo "=== ONESHOT START $(date -u +%FT%TZ) ==="
export PATH="/usr/local/cuda/bin:/usr/local/cuda-12.4/bin:$PATH"; export CUDA_HOME=/usr/local/cuda
apt-get install -y file clang >/dev/null 2>&1 || true
SRC=/root/hxsrc
rm -rf "$SRC"; mkdir -p "$SRC" /workspace; cd "$SRC"
tar xzf /root/hexa_full_src.tgz
# blocker #5 fix: inject the 7 forge dispatch impls (forge_extra.c) into runtime.c
cp /root/forge_extra.c "$SRC/self/forge/forge_extra.c"
grep -q 'forge_extra.c' self/runtime.c || sed -i 's#\#include "forge/forge_tier_v1.c"#\#include "forge/forge_tier_v1.c"\n\#include "forge/forge_extra.c"#' self/runtime.c
echo "fragment injected: $(grep -c forge_extra self/runtime.c)"
export HEXA_LANG="$SRC" CC=clang LIBS="-lm -ldl"
echo "--- build stage1 (transpiler+driver) ---"
CC=clang LIBS="-lm -ldl" OUT_HEXA="$SRC/hexa" bash tool/stage_build_hexa > /workspace/ob_build1.log 2>&1; echo "BUILD1_RC=$?"
# blocker #4 fix: regen hexa_cc.c so the transpiler knows the forge builtins
./hexa cc --regen > /workspace/ob_regen.log 2>&1; echo "REGEN_RC=$?"
if [ -f self/native/hexa_cc.c.new ]; then cp self/native/hexa_cc.c self/native/hexa_cc.c.bak; cp self/native/hexa_cc.c.new self/native/hexa_cc.c; fi
rm -rf build/hexa_v2 build/hexat build/stage1
CC=clang LIBS="-lm -ldl" OUT_HEXA="$SRC/hexa" bash tool/stage_build_hexa > /workspace/ob_build2.log 2>&1; echo "BUILD2_RC=$?"
"$SRC/hexa" --version
echo "--- build clm_prod ---"
./hexa build stdlib/flame/clm_prod.hexa > /workspace/ob_clmbuild.log 2>&1
echo "CLM_BUILD_RC=$?  errors=$(grep -cE 'error:' /workspace/ob_clmbuild.log)"
tail -2 /workspace/ob_clmbuild.log

# ---- FIRE ----
CORPUS=/workspace/savant_5lang_starter.txt
DRIVER="$SRC/stdlib/flame/clm_prod.hexa"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | head -1
echo "corpus=$CORPUS ($(wc -c < $CORPUS)B)"
fire_cfg () {
  local TAG="$1" D="$2" T="$3" E="$4" NS="$5" EP="$6" TIMEOUT="$7"
  echo ""; echo "############ rung0 $TAG : d=$D T=$T E=$E nsamp=$NS epochs=$EP ############"
  local SAMP=/workspace/util_${TAG}.csv; : > "$SAMP"
  local OUT=/workspace/savant_rung0_${TAG}.clm
  local TLOG=/workspace/train_${TAG}.log
  ( while :; do nvidia-smi --query-gpu=utilization.gpu,power.draw,memory.used --format=csv,noheader,nounits -i 0 >> "$SAMP" 2>/dev/null; sleep 0.2; done ) & local SPID=$!
  local t0=$(date +%s); cd "$SRC"
  timeout "$TIMEOUT" env CLM_PROD_D=$D CLM_PROD_T=$T CLM_PROD_E=$E CLM_PROD_NSAMP=$NS CLM_PROD_EPOCHS=$EP \
    CLM_PROD_CORPUS="$CORPUS" CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1 CLM_PROD_OUT="$OUT" \
    HEXA_CUDA_LINK=1 HEXA_LANG="$SRC" "$SRC/hexa" run stdlib/flame/clm_prod.hexa > "$TLOG" 2>&1
  local RC=$?; local t1=$(date +%s); kill $SPID 2>/dev/null
  echo "FIRE_RC=$RC tag=$TAG wall=$((t1-t0))s"
  awk -F',' 'NF>=1{u=$1+0;n++;s+=u;if(u>mx)mx=u;if(u>=20)g++} END{if(n>0)printf "UTIL[%s] n=%d PEAK=%d%% MEAN=%.4f%% pct_ge20=%.2f%%\n","'$TAG'",n,mx,s/n,100*g/n}' "$SAMP"
  awk -F',' 'NF>=3{m=$3+0;if(m>mm)mm=m} END{printf "DEVMEM[%s] peak=%dMiB\n","'$TAG'",mm}' "$SAMP"
  echo "--- descent[$TAG] (g63) ---"
  grep -E "epoch-1 mean CE|epoch-.* mean CE|F-CLM-PROD-DESCENT|PASS|FAIL|wrote|windows|corpus|out of memory" "$TLOG" | tail -14
  echo "--- ckpt[$TAG] ---"; ls -la "$OUT" 2>&1 | tail -1; sha256sum "$OUT" 2>/dev/null
}
fire_cfg rung0_d768 768 256 2 96 8 2700
echo ""; echo "=== ONESHOT DONE $(date -u +%FT%TZ) ==="
