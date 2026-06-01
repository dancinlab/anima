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
# Extract glibc version robustly: grab the FIRST x.y on the ldd banner, strip any
# stray whitespace/newlines (the `(Ubuntu GLIBC 2.35-...)` token is the version).
GLIBC_RAW="$(ldd --version 2>/dev/null | head -1)"
GMAJ="$(printf '%s' "$GLIBC_RAW" | grep -oE 'GLIBC [0-9]+' | grep -oE '[0-9]+' | head -1)"
GMIN="$(printf '%s' "$GLIBC_RAW" | grep -oE 'GLIBC [0-9]+\.[0-9]+' | grep -oE '\.[0-9]+' | tr -d '.' | head -1)"
[ -z "$GMAJ" ] && GMAJ=0; [ -z "$GMIN" ] && GMIN=0
echo "GLIBC banner: $GLIBC_RAW"
echo "GLIBC maj=$GMAJ min=$GMIN"
# need shim iff glibc < 2.38 (prebuilt hexa ELF needs GLIBC_2.38+)
NEED_SHIM=0
if [ "$GMAJ" -lt 2 ]; then NEED_SHIM=1; fi
if [ "$GMAJ" -eq 2 ] && [ "$GMIN" -lt 38 ]; then NEED_SHIM=1; fi
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
# SYS_LIBS is baked into each hexa ELF's rpath by patchelf below, so once the
# binaries are patched they run DIRECTLY (the patched interpreter + rpath carry
# the 2.39 libc and cuBLAS/cudart). Do NOT re-wrap a patched ELF with an explicit
# loader invocation — that yields "file too short" (the v4 RUN_RC=127). run_hexa
# therefore just execs directly; the patch is the shim.
SYS_LIBS="/usr/local/cuda/lib64:/usr/lib/x86_64-linux-gnu:/lib/x86_64-linux-gnu"
run_hexa() { "$@"; }

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
patch_all_hexa_elfs() {
  # patchelf EVERY hexa ELF (under ~/.hx and $HEXA_SRC) to the staged 2.39 loader.
  # `hexa run` self-spawns child binaries (hexat transpiler, module_loader, sub
  # hexa) at varied paths — patching ONLY a hand-listed few leaves a child on the
  # system loader → GLIBC_2.38 error mid-run. So we discover them: any regular
  # file whose `head -c4` is the ELF magic gets patched (no `file` cmd needed —
  # it is NOT preinstalled on the CUDA image; that guard was the prior silent skip).
  [ -z "$SHIM_LD" ] && return 0
  apt-get install -y patchelf >/dev/null 2>&1 || true
  local RPATH="$SHIM_LIB:$SYS_LIBS" n=0
  local f magic
  for f in $(find "$HOME/.hx" "$HEXA_SRC/build" -type f \( -perm -u+x -o -name '*.real' -o -name 'hexat' -o -name 'hexa*' \) 2>/dev/null | sort -u); do
    magic="$(head -c4 "$f" 2>/dev/null | od -An -tx1 2>/dev/null | tr -d ' \n')"
    if [ "$magic" = "7f454c46" ]; then
      patchelf --set-interpreter "$SHIM_LD" --set-rpath "$RPATH" "$f" 2>/dev/null && n=$((n+1))
    fi
  done
  echo "  patchelf'd $n hexa ELF(s) -> 2.39 loader"
  echo "  hexa.real interp = $(patchelf --print-interpreter "$HOME/.hx/bin/hexa.real" 2>/dev/null)"
}
if [ -n "$SHIM_LD" ]; then
  echo "--- patchelf ALL hexa ELFs -> glibc-2.39 loader (discovered, covers self-spawn) ---"
  patch_all_hexa_elfs
fi

# ─── CRITICAL: rebuild hexa FROM SOURCE (cuda_link_decision is NOT in the
# prebuilt release hexa.real — it lives only in self/main.hexa). Without this
# the forge GPU link path can never engage; `hexa run`/`hexa build` execute the
# stale prebuilt binary that links CPU-only. The patched prebuilt (above) only
# bootstraps Stage-0; the fresh self-hosted binary links the system 2.35 libc
# NATIVELY (no glibc shim for it) AND contains the CUDA link decision. ───
# Need the gitignored seed .c (runtime.c + hexa_cc.c + native/*.c + forge/*.c);
# the dispatcher scp's them as /workspace/hexa_seed_c.tgz (extracted to src/self).
echo "--- extract seed .c (runtime.c + seeds) into src/self ---"
if [ -f /workspace/hexa_seed_c.tgz ]; then
  ( cd "$HEXA_SRC" && tar xzf /workspace/hexa_seed_c.tgz ) && echo "  seeds extracted" || echo "  WARN seed extract failed"
fi
echo "--- self-host rebuild hexa (Stage 0/1/2; cuda_link_decision baked in) ---"
HEXA_FRESH="$WORK/hexa_fresh"
if [ -f "$HEXA_SRC/self/runtime.c" ] && [ -x "$HEXA_SRC/tool/stage_build_hexa" ]; then
  ( cd "$HEXA_SRC" && CC=clang LIBS="-lm -lpthread -ldl" OUT_HEXA="$HEXA_FRESH" \
      timeout 1800 bash tool/stage_build_hexa 2>&1 | tail -8 ) || echo "WARN: self-host build returned nonzero"
fi
if [ -x "$HEXA_FRESH" ] && "$HEXA_FRESH" --version >/dev/null 2>&1; then
  HAS_CUDA_FN="$(strings "$HEXA_FRESH" 2>/dev/null | grep -c 'CUDA link ENGAGED')"
  echo "  fresh hexa built; 'CUDA link ENGAGED' string count = $HAS_CUDA_FN (>0 = fix present)"
  # also build a fresh module_loader from the fresh hexa (stdlib use resolution)
  ( cd "$HEXA_SRC" && "$HEXA_FRESH" build self/module_loader.hexa -o "$HEXA_SRC/build/hexa_module_loader" >/dev/null 2>&1 ) || true
  # swap the fresh binary into the hexa entrypoint so `hexa run/build` use it
  cp -f "$HEXA_FRESH" "$HOME/.hx/bin/hexa.real" 2>/dev/null || true
  cp -f "$HEXA_FRESH" "$HOME/.hx/bin/hexa" 2>/dev/null || true
  HEXABIN="$HEXA_FRESH"
else
  echo "  WARN: self-host build failed — falling back to patched prebuilt (cuda link will NOT engage)"
  HEXABIN="$HOME/.hx/bin/hexa"
fi
echo "--- hexa --version smoke ---"
HV="$("$HEXABIN" --version 2>&1 | head -1)"
echo "  $HV"
case "$HV" in hexa*) : ;; *) echo "FATAL hexa broken: $HV"; exit 11 ;; esac

echo "=== [3/7] corpus — c4 5-lang backbone (in-repo fixture) ==="
CORPUS="$HEXA_SRC/stdlib/flame/testdata/clm_semantic_parallel.txt"
[ -s "$CORPUS" ] || { echo "FATAL: in-repo corpus fixture missing"; exit 12; }
echo "corpus: $CORPUS ($(wc -c < "$CORPUS") bytes, 5-lang en zh ru ja ko)"

echo "=== [4/7] BUILD clm_prod with HEXA_CUDA_LINK=1 (hexa build -> cuda_link_decision) ==="
# Use `hexa build` (NOT `hexa run`) — cmd_build calls cuda_link_decision, while
# cmd_run's binary cache key does NOT fold HEXA_CUDA_LINK (a CPU-cached binary
# would be silently reused). Build → a real binary linked -DHEXA_CUDA + cuBLAS.
export HEXA_CUDA_LINK=1
CLM_BIN="$WORK/clm_prod_d${DVAL}"
( export HEXA_LANG="$HEXA_SRC"; cd "$HEXA_SRC" && HEXA_CUDA_LINK=1 "$HEXABIN" build stdlib/flame/clm_prod.hexa -o "$CLM_BIN" ) > "$WORK/build.log" 2>&1
echo "  build rc=$?  bin=$CLM_BIN"
echo "--- build.log cuda-link decision ---"
grep -E "\[cuda\]|CUDA link ENGAGED|building CPU-only|nvcc|cublas|error|FAILED" "$WORK/build.log" | head -15 || tail -10 "$WORK/build.log"
# cuda_link_decision links -lcublas -lcudart but NOT -lcuda (the CUDA *driver*
# API: cuInit/cuModuleLoadData/cuLaunchKernel live in libcuda.so). On a CUDA
# image that yields "undefined reference to cuInit". Manual relink fallback adds
# -lcuda + the driver-lib dir; reuses the transpiled C + nvcc'd runtime_cuda.o.
if [ ! -x "$CLM_BIN" ] && grep -q "undefined reference to .cu" "$WORK/build.log"; then
  echo "  build hit undefined cuDriver symbols — relinking with -lcuda ..."
  APPC="$(ls -t "$HEXA_SRC"/build/artifacts/*.c 2>/dev/null | head -1)"
  RTCUDA_O="$(ls -t "$HEXA_SRC"/self/cuda/runtime_cuda.*.o 2>/dev/null | head -1)"
  RTO="$(ls -t "$HOME"/.hexa-cache/runtime.*.cuda.o 2>/dev/null | head -1)"
  CUDA_DRV_DIR="$(dirname "$(find / -name 'libcuda.so*' 2>/dev/null | head -1)")"
  if [ -n "$APPC" ] && [ -n "$RTCUDA_O" ] && [ -n "$RTO" ]; then
    clang -O2 -DHEXA_CUDA -I /usr/local/cuda/include -D_GNU_SOURCE -Wno-trigraphs \
      -fbracket-depth=4096 -I "$HEXA_SRC/self" "$APPC" "$RTO" "$RTCUDA_O" -o "$CLM_BIN" \
      -lm -lpthread -L/usr/local/cuda/lib64 -L"$CUDA_DRV_DIR" \
      -lcublas -lcudart -lcuda -ldl -lrt -lstdc++ 2>&1 | tail -6
    [ -x "$CLM_BIN" ] && echo "  relink OK -> $CLM_BIN  (links: $(ldd "$CLM_BIN" 2>/dev/null | grep -ciE 'cublas|cudart|libcuda') cuda libs)"
  fi
fi
if [ ! -x "$CLM_BIN" ]; then
  echo "  WARN: build produced no binary — falling back to hexa run"
fi

echo "=== [5/7] run clm_prod d=$DVAL E=$EVAL epochs=$EPOCHS, CONTINUOUS util sampling ==="
export CLM_PROD_CORPUS="$CORPUS"
export CLM_PROD_D="$DVAL" CLM_PROD_E="$EVAL" CLM_PROD_EPOCHS="$EPOCHS" CLM_PROD_NSAMP="$NSAMP"
export CLM_PROD_OUT="$WORK/d768_5lang_c4.clm"
echo "CLM_PROD_D=$DVAL E=$EVAL EPOCHS=$EPOCHS NSAMP=$NSAMP  OUT=$CLM_PROD_OUT  HEXA_CUDA_LINK=1"
UTIL_CSV="$WORK/util.csv"; : > "$UTIL_CSV"
( while :; do nvidia-smi --query-gpu=utilization.gpu,utilization.memory,power.draw,clocks.sm --format=csv,noheader,nounits >> "$UTIL_CSV" 2>/dev/null; sleep 0.2; done ) &
SAMPLER=$!
RUN_LOG="$WORK/train.log"
if [ -x "$CLM_BIN" ]; then
  ( export HEXA_LANG="$HEXA_SRC"; cd "$HEXA_SRC" && "$CLM_BIN" ) 2>&1 | tee "$RUN_LOG"
  RUN_RC=${PIPESTATUS[0]}
else
  ( export HEXA_LANG="$HEXA_SRC"; cd "$HEXA_SRC" && HEXA_CUDA_LINK=1 "$HEXABIN" run stdlib/flame/clm_prod.hexa ) 2>&1 | tee "$RUN_LOG"
  RUN_RC=${PIPESTATUS[0]}
fi
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
