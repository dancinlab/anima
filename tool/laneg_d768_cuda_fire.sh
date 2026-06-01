#!/usr/bin/env bash
# Lane-G d768 CUDA-DEVEL fire — clm_prod CLMConvMoE d768 on the c4 5-lang
# backbone corpus, forge=cuBLAS. ROOT-CAUSE FIX over the prior bare-image fire:
# this pod runs a CUDA-DEVEL image (nvcc + cuBLAS + clang present) so forge's
# device path actually COMPILES on the GPU instead of silently degrading to CPU.
#
# hexa is built FROM the integrated branch `fix/hexa-run-cuda-link` which has:
#   - cuda_link_decision() in self/main.hexa (forge GPU link path for `hexa run`)
#   - clm_prod.hexa PR4 (env d/E/epochs/corpus override + CLM_PROD_OUT .clm save)
# HEXA_CUDA_LINK=1 forces the forge GPU link ON; the TOOLKIT GATE then passes
# because this image ships nvcc + libcublas. Continuous nvidia-smi util sampling.
#
# Args: $1=HF_TOKEN(optional, "" ok)  $2=D  $3=EPOCHS  $4=E  $5=NSAMP
set -uo pipefail
HF_TOKEN="${1:-}"
DVAL="${2:-768}"; EPOCHS="${3:-12}"; EVAL="${4:-2}"; NSAMP="${5:-16}"
BRANCH="fix/hexa-run-cuda-link"

export PATH="/usr/local/cuda/bin:$HOME/.hx/bin:$PATH"
[ -n "$HF_TOKEN" ] && { export HUGGINGFACE_HUB_TOKEN="$HF_TOKEN"; export HF_TOKEN="$HF_TOKEN"; }
WORK="/workspace/laneg_d768"; mkdir -p "$WORK"; cd "$WORK"

echo "=== [0/7] host sanity — CUDA-DEVEL image required ==="
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader || { echo "FATAL no gpu"; exit 9; }
echo "--- nvcc ---"; nvcc --version 2>/dev/null | grep -i release || { echo "FATAL: no nvcc — NOT a CUDA-devel image (forge cannot build GPU path)"; exit 8; }
echo "--- cuda root ---"; ls -d /usr/local/cuda 2>/dev/null && ls /usr/local/cuda/lib64/libcublas.so* 2>/dev/null || { echo "FATAL: libcublas missing — toolkit gate will fail"; exit 7; }
ldd --version 2>/dev/null | head -1 || true

echo "=== [1/7] toolchain + glibc shim check (linux hexa ELF needs >=2.38) ==="
apt-get update -y >/dev/null 2>&1 || true
apt-get install -y clang wget git python3 python3-pip >/dev/null 2>&1 || true
command -v clang >/dev/null 2>&1 && clang --version | head -1 || echo "WARN no clang"
GLIBC_VER="$(ldd --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+$' || echo 0)"
GMAJ="${GLIBC_VER%%.*}"; GMIN="${GLIBC_VER#*.}"
echo "GLIBC_VER=$GLIBC_VER (maj=$GMAJ min=$GMIN)"
# robust integer compare: need shim iff glibc < 2.38 (prebuilt hexa ELF needs 2.38+)
NEED_SHIM=0
if [ "$GMAJ" -lt 2 ] 2>/dev/null; then NEED_SHIM=1; fi
if [ "$GMAJ" -eq 2 ] 2>/dev/null && [ "$GMIN" -lt 38 ] 2>/dev/null; then NEED_SHIM=1; fi
echo "NEED_SHIM=$NEED_SHIM"
SHIM_LD=""; SHIM_LIB=""
if [ "$NEED_SHIM" = "1" ]; then
  echo "glibc<2.38 -> staging glibc-2.39 loader shim (libc6 2.39 noble deb)"
  mkdir -p "$WORK/glibc239"; cd "$WORK/glibc239"
  for u in \
    "http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/libc6_2.39-0ubuntu8.5_amd64.deb" \
    "http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/libc6_2.39-0ubuntu8.4_amd64.deb" \
    "http://archive.ubuntu.com/ubuntu/pool/main/g/glibc/libc6_2.39-0ubuntu8_amd64.deb" ; do
    wget -q "$u" -O g.deb 2>/dev/null && dpkg -x g.deb x 2>/dev/null && break || true
  done
  LD="$(find "$WORK/glibc239/x" -name 'ld-linux-x86-64.so.2' 2>/dev/null | head -1)"
  GLIBLIB="$(find "$WORK/glibc239/x" -name 'libc.so.6' 2>/dev/null | head -1)"
  if [ -n "$LD" ] && [ -f "$LD" ] && [ -n "$GLIBLIB" ]; then
    SHIM_LD="$LD"; SHIM_LIB="$(dirname "$GLIBLIB")"
    echo "SHIM_LD=$SHIM_LD  SHIM_LIB=$SHIM_LIB"
    "$SHIM_LD" --version 2>&1 | head -1 || true
  else
    echo "FATAL: glibc-2.39 shim not staged (LD=$LD GLIBLIB=$GLIBLIB) — prebuilt hexa ELF cannot run"; exit 6
  fi
  cd "$WORK"
else
  echo "glibc OK (>=2.38) — no shim needed"
fi
# run_hexa wraps under the shim loader; --library-path includes the 2.39 libs FIRST,
# then the system lib dirs so libcublas/libcudart/libstdc++ still resolve.
SYS_LIBS="/usr/local/cuda/lib64:/usr/lib/x86_64-linux-gnu:/lib/x86_64-linux-gnu"
run_hexa() { if [ -n "$SHIM_LD" ]; then "$SHIM_LD" --library-path "$SHIM_LIB:$SYS_LIBS" "$@"; else "$@"; fi; }

echo "=== [2/7] install hexa, checkout $BRANCH (cuda_link_decision + PR4 trainer) ==="
if [ ! -x "$HOME/.hx/bin/hexa" ]; then
  HEXA_BRANCH="$BRANCH" /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/dancinlab/hexa-lang/main/install.sh)" 2>&1 | tail -15 || true
fi
export PATH="$HOME/.hx/bin:$PATH"
HEXA_SRC="$(ls -d $HOME/.hx/src 2>/dev/null | head -1)"
echo "HEXA_SRC=$HEXA_SRC"
[ -n "$HEXA_SRC" ] || { echo "FATAL no hexa src"; exit 10; }
git -C "$HEXA_SRC" fetch --depth 1 origin "$BRANCH" >/dev/null 2>&1 || true
git -C "$HEXA_SRC" checkout -q -B laneg FETCH_HEAD 2>/dev/null || git -C "$HEXA_SRC" checkout -q "$BRANCH" 2>/dev/null || true
git -C "$HEXA_SRC" reset --hard FETCH_HEAD >/dev/null 2>&1 || true
git -C "$HEXA_SRC" log --oneline -1 || true
echo "--- confirm cuda_link_decision present in src (the forge GPU link fix) ---"
grep -c "cuda_link_decision" "$HEXA_SRC/self/main.hexa" 2>/dev/null || echo "WARN: cuda_link_decision grep miss"
echo "--- confirm CLM_PROD_OUT save path present ---"
grep -c "CLM_PROD_OUT" "$HEXA_SRC/stdlib/flame/clm_prod.hexa" 2>/dev/null || echo "WARN: no save path"

# patchelf ALL hexa ELFs to the staged glibc-2.39 loader IN-PLACE, so every
# invocation — including hexa's self-spawned children (sub-hexa build/run during
# the runtime_cuda emit + module_loader) — runs under 2.39 without a wrapper.
# This is the proven prior-fire workaround (inbox d768-recovery Gap 2).
if [ -n "$SHIM_LD" ]; then
  echo "--- patchelf hexa ELFs -> glibc-2.39 loader (in-place, covers self-spawn) ---"
  apt-get install -y patchelf >/dev/null 2>&1 || true
  RPATH="$SHIM_LIB:$SYS_LIBS"
  for f in "$HOME/.hx/bin/hexa.real" "$HOME/.hx/bin/hexa" "$HEXA_SRC/build/hexat" "$HEXA_SRC/build/hexa_module_loader" "$HOME/.hx/bin/hx"; do
    if [ -f "$f" ] && file "$f" 2>/dev/null | grep -q ELF; then
      patchelf --set-interpreter "$SHIM_LD" --set-rpath "$RPATH" "$f" 2>/dev/null && echo "  patched $f" || echo "  (skip $f)"
    fi
  done
  # if hexa is a wrapper script calling hexa.real, leave it; otherwise it's the ELF.
fi

# DO NOT re-run install.sh — it re-fetches the prebuilt glibc-2.38 ELF and
# re-breaks the patch. The branch SOURCE is already checked out at $HEXA_SRC
# (cuda_link_decision lives in self/main.hexa, interpreted from source by `hexa
# run` — no binary rebuild needed for the trainer path). We only need the
# module_loader (so stdlib `use` resolves) — rebuild it natively from source.
echo "--- (re)build hexa_module_loader from source (native glibc, stdlib use) ---"
if [ -x "$HEXA_SRC/tool/build_hexa_module_loader.sh" ]; then
  ( cd "$HEXA_SRC" && bash tool/build_hexa_module_loader.sh 2>&1 | tail -6 ) || echo "WARN: module_loader build returned nonzero"
  # patch the freshly built loader too (in case it linked an old libc somehow)
  [ -n "$SHIM_LD" ] && [ -f "$HEXA_SRC/build/hexa_module_loader" ] && \
    patchelf --set-interpreter "$SHIM_LD" --set-rpath "$SHIM_LIB:$SYS_LIBS" "$HEXA_SRC/build/hexa_module_loader" 2>/dev/null || true
fi
echo "--- hexa --version smoke (must run under patched/shim loader) ---"
"$HOME/.hx/bin/hexa" --version 2>&1 | head -3 || { echo "FATAL hexa broken"; exit 11; }

echo "=== [3/7] corpus — c4 5-lang backbone (in-repo fixture) ==="
CORPUS="$HEXA_SRC/stdlib/flame/testdata/clm_semantic_parallel.txt"
[ -s "$CORPUS" ] || { echo "FATAL: in-repo corpus fixture missing"; exit 12; }
echo "corpus: $CORPUS ($(wc -c < "$CORPUS") bytes, 5-lang en zh ru ja ko)"

echo "=== [4/7] FORGE GPU-PATH SMOKE (force cuda link on a tiny forge program) ==="
export HEXA_CUDA_LINK=1
( export HEXA_LANG="$HEXA_SRC"; cd "$HEXA_SRC" && HEXA_CUDA_LINK=1 run_hexa "$HOME/.hx/bin/hexa" run stdlib/flame/clm_prod.hexa ) >/dev/null 2>&1 &
SMOKE=$!; sleep 8; kill "$SMOKE" 2>/dev/null; wait "$SMOKE" 2>/dev/null || true
echo "(smoke dispatched; real run below carries the cuda-link log)"

echo "=== [5/7] run clm_prod d=$DVAL E=$EVAL epochs=$EPOCHS, HEXA_CUDA_LINK=1, CONTINUOUS util sampling ==="
export CLM_PROD_CORPUS="$CORPUS"
export CLM_PROD_D="$DVAL" CLM_PROD_E="$EVAL" CLM_PROD_EPOCHS="$EPOCHS" CLM_PROD_NSAMP="$NSAMP"
export CLM_PROD_OUT="$WORK/d768_5lang_c4.clm"
export HEXA_CUDA_LINK=1
echo "CLM_PROD_D=$DVAL E=$EVAL EPOCHS=$EPOCHS NSAMP=$NSAMP  OUT=$CLM_PROD_OUT  HEXA_CUDA_LINK=1"
UTIL_CSV="$WORK/util.csv"; : > "$UTIL_CSV"
( while :; do nvidia-smi --query-gpu=utilization.gpu,utilization.memory,power.draw,clocks.sm --format=csv,noheader,nounits >> "$UTIL_CSV" 2>/dev/null; sleep 0.2; done ) &
SAMPLER=$!
RUN_LOG="$WORK/train.log"
( export HEXA_LANG="$HEXA_SRC"; cd "$HEXA_SRC" && HEXA_CUDA_LINK=1 run_hexa "$HOME/.hx/bin/hexa" run stdlib/flame/clm_prod.hexa ) 2>&1 | tee "$RUN_LOG"
RUN_RC=${PIPESTATUS[0]}
kill "$SAMPLER" 2>/dev/null; wait "$SAMPLER" 2>/dev/null

echo "=== [6/7] artifact + sha256 ==="
if [ -f "$CLM_PROD_OUT" ]; then
  sha256sum "$CLM_PROD_OUT" | tee "$WORK/ckpt.sha256"
  ls -la "$CLM_PROD_OUT"
else
  echo "FATAL: no .clm artifact written"
fi

echo "=== [7/7] gate eval ==="
echo "--- cuda-link log (did forge engage the GPU?) ---"
grep -E "\[cuda\]" "$RUN_LOG" || echo "(no [cuda] log lines — link decision did not print)"
echo "--- F-CLM-PROD-DESCENT ---"
grep -E "mean CE|F-CLM-PROD-DESCENT|PASS|FAIL|CLM_PROD_OUT wrote|config d=" "$RUN_LOG" || true
echo "--- util samples (n=$(wc -l < "$UTIL_CSV")) ---"
awk -F',' 'NF>=1{u=$1+0; a[n++]=u; s+=u; if(u>mx)mx=u; if(u>20)gt++} END{
  if(n>0){ n2=asort(a); printf "UTIL: n=%d min=%d med=%d max=%d mean=%.2f pct_gt20=%.1f%%\n",n,a[1],a[int(n/2)],mx,s/n,(gt*100.0/n) } else print "UTIL: n=0" }' "$UTIL_CSV"
echo "--- top-10 util samples ---"; sort -t',' -k1 -n -r "$UTIL_CSV" | head -10
echo "RUN_RC=$RUN_RC"
echo "=== DONE ==="
