#!/usr/bin/env bash
# Lane-G DECISIVE forge device-feed fire — clm_prod CLMConvMoE mid-scale (d~1536,
# T~512) on the c4 5-lang backbone, forge=cuBLAS, BOTH backward-feed levers ON:
#   lever (a) CLM_PROD_DEVFEED=1 — device im2col/col2im + on-device AdamW (PR #2505)
#   lever (b) CLM_PROD_BATCHED=1 — strided-batched conv GEMM fuse        (PR #2504)
# Goal: does the on-device backward feed clear util >= 20% (was MEAN 0.24%)?
#
# Build: self-host rebuild of hexa from origin/main (carries #2504+#2505). The
# 23 seed .c are shipped pre-spliced (/workspace/hexa_seed_c.tgz) — runtime.c
# already carries BOTH lever wrapper bodies (frozen + lever-b body + lever-a SSOT
# fragment), runtime_cuda.c carries all 5 GPU kernels (im2col/im2col_t/col2im/
# matmul_batched/adamw). HEXA_CUDA_ARCH=90 clamps to sm_90 PTX (B200-safe).
#
# Args: $1=HF_TOKEN("" ok) $2=D(1536) $3=EPOCHS(12) $4=E(2) $5=NSAMP(16) $6=T(512)
set -uo pipefail
HF_TOKEN="${1:-}"
DVAL="${2:-1536}"; EPOCHS="${3:-12}"; EVAL="${4:-2}"; NSAMP="${5:-16}"; TVAL="${6:-512}"
BRANCH="laneg/devfeed-cuda-link-merge"  # main levers (#2504/#2505) + cuda_link_decision (fix/hexa-run-cuda-link) + -lcuda Gap-2 baked (superset of laneg/devfeed-cudalink-integrated); local TRANSPILE+BUILD OK 2026-06-02

export PATH="/usr/local/cuda/bin:$HOME/.hx/bin:$PATH"
export HEXA_CUDA_ARCH=90
[ -n "$HF_TOKEN" ] && { export HUGGINGFACE_HUB_TOKEN="$HF_TOKEN"; export HF_TOKEN="$HF_TOKEN"; }
WORK="/workspace/laneg_devfeed"; mkdir -p "$WORK"; cd "$WORK"

echo "=== [0/7] host sanity — CUDA-DEVEL image required ==="
nvidia-smi --query-gpu=name,memory.total,driver_version,compute_cap --format=csv,noheader || { echo "FATAL no gpu"; exit 9; }
nvcc --version 2>/dev/null | grep -i release || { echo "FATAL: no nvcc — NOT CUDA-devel"; exit 8; }
ls /usr/local/cuda/lib64/libcublas.so* 2>/dev/null || { echo "FATAL: libcublas missing"; exit 7; }
CUDA_DRV="$(find / -name 'libcuda.so*' 2>/dev/null | head -1)"; echo "libcuda: ${CUDA_DRV:-MISSING}"

echo "=== [1/7] toolchain ==="
apt-get update -y >/dev/null 2>&1 || true
apt-get install -y clang git wget file patchelf >/dev/null 2>&1 || true
clang --version | head -1 || echo "WARN no clang"

echo "=== [2/7] install hexa + checkout origin/$BRANCH (carries #2504 lever-b + #2505 lever-a) ==="
if [ ! -x "$HOME/.hx/bin/hexa" ]; then
  HEXA_BRANCH="$BRANCH" /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)" 2>&1 | tail -10 || true
fi
export PATH="$HOME/.hx/bin:$PATH"
HEXA_SRC="$(ls -d $HOME/.hx/src 2>/dev/null | head -1)"; echo "HEXA_SRC=$HEXA_SRC"
[ -n "$HEXA_SRC" ] || { echo "FATAL no hexa src"; exit 10; }
git -C "$HEXA_SRC" fetch --depth 1 origin "$BRANCH" >/dev/null 2>&1 || true
git -C "$HEXA_SRC" reset --hard FETCH_HEAD >/dev/null 2>&1 || true
git -C "$HEXA_SRC" log --oneline -1 || true
echo "--- confirm levers wired in .hexa ---"
echo "  DEVFEED/BATCHED in clm_prod.hexa: $(grep -c 'CLM_PROD_DEVFEED\|CLM_PROD_BATCHED' "$HEXA_SRC/stdlib/flame/clm_prod.hexa" 2>/dev/null)"
echo "  dispatch lowerings in codegen.hexa: $(grep -c 'forge_dispatch_im2col\|forge_dispatch_matmul_batched\|forge_dispatch_adamw' "$HEXA_SRC/self/codegen.hexa" 2>/dev/null)"

echo "=== [3/7] ship PRE-SPLICED 23 seed .c (runtime.c has both lever bodies; runtime_cuda.c has 5 kernels) ==="
if [ -f /workspace/hexa_seed_c.tgz ]; then
  ( cd "$HEXA_SRC" && tar xzf /workspace/hexa_seed_c.tgz ) && echo "  seeds extracted ($(find "$HEXA_SRC/self" -name '*.c' | wc -l) .c)" || echo "  WARN seed extract failed"
else
  echo "  FATAL: /workspace/hexa_seed_c.tgz missing"; exit 11
fi
echo "--- lever bodies present in shipped runtime.c? ---"
echo "  matmul_batched+im2col+col2im+adamw defs: $(grep -cE '^HexaVal hexa_forge_dispatch_(matmul_batched|im2col|col2im|adamw)' "$HEXA_SRC/self/runtime.c" 2>/dev/null)"
echo "--- 5 GPU kernels present in shipped runtime_cuda.c? ---"
for k in im2col_gpu im2col_t_gpu col2im_gpu matmul_batched_gpu adamw_step_inplace_gpu; do
  printf "  _hx_cuda_farr_%s: %s\n" "$k" "$(grep -c "_hx_cuda_farr_$k" "$HEXA_SRC/self/cuda/runtime_cuda.c" 2>/dev/null)"
done

echo "=== [4/7] self-host rebuild hexa (cuda_link_decision baked in) ==="
HEXA_FRESH="$WORK/hexa_fresh"
if [ -f "$HEXA_SRC/self/runtime.c" ] && [ -x "$HEXA_SRC/tool/stage_build_hexa" ]; then
  ( cd "$HEXA_SRC" && CC=clang LIBS="-lm -lpthread -ldl" OUT_HEXA="$HEXA_FRESH" \
      timeout 2400 bash tool/stage_build_hexa 2>&1 | tail -12 ) || echo "WARN: self-host build nonzero"
fi
if [ -x "$HEXA_FRESH" ] && "$HEXA_FRESH" --version >/dev/null 2>&1; then
  echo "  fresh hexa built; 'CUDA link ENGAGED' count = $(strings "$HEXA_FRESH" 2>/dev/null | grep -c 'CUDA link ENGAGED')"
  cp -f "$HEXA_FRESH" "$HOME/.hx/bin/hexa.real" 2>/dev/null || true
  cp -f "$HEXA_FRESH" "$HOME/.hx/bin/hexa" 2>/dev/null || true
  HEXABIN="$HEXA_FRESH"
else
  echo "  FATAL: self-host build failed — CUDA link cannot engage"; exit 12
fi
"$HEXABIN" --version 2>&1 | head -1

echo "=== [4b/7] BUILD clm_prod with HEXA_CUDA_LINK=1 -> forge GPU binary ==="
CORPUS="${MID_CORPUS:-$HEXA_SRC/stdlib/flame/testdata/clm_semantic_parallel.txt}"
[ -s "$CORPUS" ] || { echo "FATAL corpus missing"; exit 13; }
echo "corpus: $CORPUS ($(wc -c < "$CORPUS") bytes)"
export HEXA_CUDA_LINK=1
CLM_BIN="$WORK/clm_prod_devfeed"
( export HEXA_LANG="$HEXA_SRC"; cd "$HEXA_SRC" && HEXA_CUDA_LINK=1 HEXA_CUDA_ARCH=90 "$HEXABIN" build stdlib/flame/clm_prod.hexa -o "$CLM_BIN" ) > "$WORK/build.log" 2>&1
echo "  build rc=$?"
grep -E "\[cuda\]|CUDA link ENGAGED|building CPU-only|nvcc|cublas|undefined reference|error|FAILED" "$WORK/build.log" | head -20 || tail -15 "$WORK/build.log"
# manual relink with -lcuda if driver-API symbols undefined (Gap 2)
if [ ! -x "$CLM_BIN" ] && grep -q "undefined reference to .cu" "$WORK/build.log"; then
  echo "  relinking with -lcuda ..."
  APPC="$(ls -t "$HEXA_SRC"/build/artifacts/*.c 2>/dev/null | head -1)"
  RTCUDA_O="$(ls -t "$HEXA_SRC"/self/cuda/runtime_cuda.*.o 2>/dev/null | head -1)"
  RTO="$(ls -t "$HOME"/.hexa-cache/runtime.*.cuda.o 2>/dev/null | head -1)"
  DRVDIR="$(dirname "$(find / -name 'libcuda.so*' 2>/dev/null | head -1)")"
  if [ -n "$APPC" ] && [ -n "$RTCUDA_O" ] && [ -n "$RTO" ]; then
    clang -O2 -DHEXA_CUDA -I /usr/local/cuda/include -D_GNU_SOURCE -Wno-trigraphs \
      -fbracket-depth=4096 -I "$HEXA_SRC/self" "$APPC" "$RTO" "$RTCUDA_O" -o "$CLM_BIN" \
      -lm -lpthread -L/usr/local/cuda/lib64 -L"$DRVDIR" -lcublas -lcudart -lcuda -ldl -lrt -lstdc++ 2>&1 | tail -6
    [ -x "$CLM_BIN" ] && echo "  relink OK ($(ldd "$CLM_BIN" 2>/dev/null | grep -ciE 'cublas|cudart|libcuda') cuda libs linked)"
  fi
fi
echo "--- binary cuda libs ---"; [ -x "$CLM_BIN" ] && ldd "$CLM_BIN" 2>/dev/null | grep -iE 'cublas|cudart|libcuda' || echo "(no binary / static)"

echo "=== [5/7] FIRE — d=$DVAL T=$TVAL E=$EVAL epochs=$EPOCHS, BOTH levers, continuous util ==="
export CLM_PROD_CORPUS="$CORPUS"
export CLM_PROD_D="$DVAL" CLM_PROD_E="$EVAL" CLM_PROD_EPOCHS="$EPOCHS" CLM_PROD_NSAMP="$NSAMP" CLM_PROD_T="$TVAL"
export CLM_PROD_DEVFEED=1   # lever (a)
export CLM_PROD_BATCHED=1   # lever (b)
export CLM_PROD_OUT="$WORK/devfeed_d${DVAL}_5lang.clm"
echo "LEVERS: CLM_PROD_DEVFEED=1 CLM_PROD_BATCHED=1  d=$DVAL T=$TVAL  OUT=$CLM_PROD_OUT  HEXA_CUDA_ARCH=$HEXA_CUDA_ARCH"
UTIL_CSV="$WORK/util.csv"; : > "$UTIL_CSV"
( while :; do nvidia-smi --query-gpu=utilization.gpu,utilization.memory,power.draw,clocks.sm --format=csv,noheader,nounits >> "$UTIL_CSV" 2>/dev/null; sleep 0.2; done ) &
SAMPLER=$!
RUN_LOG="$WORK/train.log"
if [ -x "$CLM_BIN" ]; then
  ( export HEXA_LANG="$HEXA_SRC"; cd "$HEXA_SRC" && "$CLM_BIN" ) 2>&1 | tee "$RUN_LOG"; RUN_RC=${PIPESTATUS[0]}
else
  ( export HEXA_LANG="$HEXA_SRC"; cd "$HEXA_SRC" && HEXA_CUDA_LINK=1 HEXA_CUDA_ARCH=90 "$HEXABIN" run stdlib/flame/clm_prod.hexa ) 2>&1 | tee "$RUN_LOG"; RUN_RC=${PIPESTATUS[0]}
fi
kill "$SAMPLER" 2>/dev/null; wait "$SAMPLER" 2>/dev/null

echo "=== [6/7] artifact + sha256 ==="
if [ -f "$CLM_PROD_OUT" ]; then sha256sum "$CLM_PROD_OUT" | tee "$WORK/ckpt.sha256"; ls -la "$CLM_PROD_OUT"; else echo "WARN: no .clm written"; fi

echo "=== [7/7] VERDICT ==="
echo "--- [cuda] engage log ---"; grep -E "\[cuda\]" "$RUN_LOG" | head -8 || echo "(no [cuda] lines)"
echo "--- descent (F-CLM-PROD-DESCENT) ---"; grep -E "mean CE|F-CLM-PROD-DESCENT|epoch|PASS|FAIL|config d=" "$RUN_LOG" | head -20 || true
echo "--- UTIL (n=$(wc -l < "$UTIL_CSV")) ---"
# portable (mawk-safe): MEAN/MAX/min/pct from a single pass; median via a pre-sort.
awk -F',' 'NF>=1{u=$1+0;s+=u;if(NR==1||u>mx)mx=u;if(NR==1||u<mn)mn=u;if(u>=20)gt++;n++}
  END{ if(n>0) printf "UTIL: n=%d min=%d max=%d MEAN=%.3f pct_ge20=%.2f%%\n",n,mn,mx,s/n,(gt*100.0/n); else print "UTIL: n=0" }' "$UTIL_CSV"
MED=$(awk -F',' '{print $1+0}' "$UTIL_CSV" | sort -n | awk '{a[NR]=$1} END{if(NR>0)print a[int(NR/2)+1]}')
echo "UTIL median=$MED"
echo "--- top-10 util ---"; sort -t',' -k1 -n -r "$UTIL_CSV" | head -10
echo "--- power/clock peak (forge on GPU?) ---"; sort -t',' -k3 -n -r "$UTIL_CSV" | head -3
echo "RUN_RC=$RUN_RC"
echo "=== DONE — BEFORE prior fire MEAN 0.24% ; AFTER = the UTIL MEAN above ==="
