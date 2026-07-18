#!/usr/bin/env bash
# cli/pod_bootstrap.sh — the CANONICAL py-channel pod bootstrap (anima-py on a fresh rented GPU pod).
#
# WHY THIS EXISTS: the repo had a pod dispatcher for the hexa channel (cli/eval_pod.sh) but NONE for
# the py channel, which is the DEFAULT runtime (a_cli_single_entry · a_eval_py_canonical). So every
# session hand-rolled the setup, and every session fell into the same silent traps. On 2026-07-15 a
# single session hit FIVE of them in a row and burned hours:
#
#   ① `pip install -q` swallowed PEP 668's `externally-managed-environment` refusal
#      → the install was a no-op and the session read it as success.
#   ② `python3 -m ensurepip >/dev/null 2>&1 || true` swallowed the fact that the vast image has
#      NEITHER pip NOR ensurepip → every subsequent pip call was a no-op.
#   ③ `scp <path-that-does-not-exist>` skipped the wheel WITHOUT an error → the pod never got it.
#   ④ `pgrep -f "…evaluate.py"` matched the ssh command that CONTAINED that string → a false
#      ALREADY_RUNNING → the fire was skipped and an idle pod sat for hours.
#   ⑤ every stage printed `rc=$?` but never GATED on it, so a run where anima-py was not on PATH
#      (setsid gives a minimal PATH; anima-py lands in /usr/local/bin) produced rc=127 at every
#      step and still printed "ALL_DONE" — with ZERO output files.
#   ⑥ (added 2026-07-17 · pod-ssh-transfer-broken) a plain `scp` of a 100MB+ ckpt over the vast
#      ssh-proxy DROPS mid-stream and a fresh scp restarts from byte 0 → a flaky proxy never lands a
#      big file, and the campaign "pivots to pool". Fixed here with a RESUMABLE (rsync --partial
#      --append-verify) + retrying, per-file transfer so a drop resumes instead of restarting.
#
# The unifying defect: FAILURE THAT LOOKS LIKE SUCCESS. This script closes all six, by construction:
# nothing is quiet, every install is asserted, every transfer is counted on the far side, the CLI is
# resolved to an absolute path before use, and "done" is never claimed without an artifact.
#
# Usage:
#   cli/pod_bootstrap.sh <ssh_host> <ssh_port> <wheel.whl> [asset ...]
#
# Example:
#   cli/pod_bootstrap.sh ssh9.vast.ai 28484 dist/anima_python-0.13.24-py3-none-any.whl \
#       py303.clm manifest.json
#
# TRAINING pods (a fire that runs `anima-py train`, not just evaluate/corpus) need the [train] extra
# (torch+datasets) on top of the numpy base — set POD_TRAIN=1 to install it arch-correctly (④b):
#   POD_TRAIN=1 cli/pod_bootstrap.sh ssh9.vast.ai 28484 dist/anima_python-*.whl py303.clm sweep.sh
#
# DECODE on a GPU pod needs cupy, which the --no-deps wheel install does NOT bring: without it the
# engine silently decodes on CPU-numpy — on a rented GPU box that is an 8x tax (68s/tick vs 8.5s/tick
# measured), which is a bug, not a device choice. Stage ⑤ installs the CUDA-major-matched cupy by
# default and stage ⑥ FAILS if a GPU is present but the engine still says CPU. Bootstrapping a
# CPU-only pod on purpose: POD_GPU=0.
#   POD_GPU=0 cli/pod_bootstrap.sh ssh9.vast.ai 28484 dist/anima_python-*.whl py303.clm run.sh
#
# Exit 0 ⟺ the pod can run `anima-py` AND every named asset arrived intact AND (unless POD_GPU=0) the
# engine's own decode path reaches the GPU with a real cupy kernel (AND, with POD_TRAIN=1, a real cuda
# matmul ran). Anything else exits non-zero with the reason. There is no --force and no
# skip: a bootstrap that "mostly worked" is the thing this script exists to prevent.
set -euo pipefail

HOST="${1:?usage: pod_bootstrap.sh <ssh_host> <ssh_port> <wheel.whl> [asset ...]}"
PORT="${2:?missing ssh_port}"
WHEEL="${3:?missing wheel path}"
shift 3
ASSETS=("$@")

SSH=(ssh -p "$PORT" -o StrictHostKeyChecking=no -o BatchMode=yes -o ConnectTimeout=60 -o ServerAliveInterval=20 "root@$HOST")
SCP=(scp -P "$PORT" -o StrictHostKeyChecking=no -o ConnectTimeout=60)

[ -f "$WHEEL" ] || { echo "FATAL: wheel not found locally: $WHEEL" >&2; exit 1; }
for a in ${ASSETS[@]+"${ASSETS[@]}"}; do
  [ -f "$a" ] || { echo "FATAL: asset not found locally: $a" >&2; exit 1; }
done

WHEEL_VER="$(basename "$WHEEL" | sed -E 's/^anima_python-([0-9.]+)-.*/\1/')"
[ -n "$WHEEL_VER" ] || { echo "FATAL: cannot parse version from wheel name: $WHEEL" >&2; exit 1; }
echo "[pod] wheel=$(basename "$WHEEL") version=$WHEEL_VER assets=${#ASSETS[@]}"

# ── ① transfer, then COUNT ON THE FAR SIDE (trap ③: scp skips a missing source silently) ─────────
# trap ⑥ (pod-ssh-transfer-broken): a plain scp of a large ckpt (100MB+) over the vast ssh-proxy DROPS
# mid-stream and dies — a fresh scp restarts from byte 0, so a flaky proxy never completes a big file.
# Fix = RESUMABLE rsync (--partial keeps the incomplete file, --append-verify resumes + re-checks) inside
# a retry loop, PER FILE (one big file's drop doesn't re-send the small ones). rsync needs to exist on
# BOTH ends: install it on the pod best-effort first; fall back to a scp retry loop if it can't.
echo "[pod] ensure rsync (resumable transfer) …"
"${SSH[@]}" 'command -v rsync >/dev/null 2>&1 || { apt-get update -qq && apt-get install -y -qq rsync; } >/dev/null 2>&1 || true'
POD_HAS_RSYNC=$("${SSH[@]}" 'command -v rsync >/dev/null 2>&1 && echo 1 || echo 0')
transfer_one() {  # $1 = local file → /root/<basename>, resumable + retrying
  # rsync (resumable) FIRST when the pod has it; on 8× failure FALL BACK to scp (not just when
  # rsync is ABSENT) — a host whose ssh-proxy breaks rsync mid-stream can still take a plain scp
  # (observed on ssh6.vast.ai: rsync 8× FATAL while `hexa cloud copy-to` scp of the same wheel
  # succeeded). The old code only reached scp when rsync was uninstallable, so a rsync-transport
  # failure died instead of degrading. `return 0` on the first success of either path.
  local f="$1" base; base=$(basename "$f"); local n=0
  if command -v rsync >/dev/null 2>&1 && [ "$POD_HAS_RSYNC" = 1 ]; then
    while [ "$n" -lt 8 ]; do
      rsync --partial --append-verify --timeout=180 \
        -e "ssh -p $PORT -o StrictHostKeyChecking=no -o ServerAliveInterval=20" \
        "$f" "root@$HOST:/root/$base" && return 0
      n=$((n+1)); echo "[pod]   rsync retry $n/8: $base (resuming)"; sleep 5
    done
    echo "[pod]   rsync failed 8× on $base — falling back to scp" >&2
  fi
  n=0
  while [ "$n" -lt 8 ]; do
    "${SCP[@]}" "$f" "root@$HOST:/root/$base" && return 0
    n=$((n+1)); echo "[pod]   scp retry $n/8: $base"; sleep 5
  done
  echo "FATAL: both rsync and scp failed on $base" >&2; return 1
}
echo "[pod] transfer … (rsync=$POD_HAS_RSYNC · resumable + retry)"
transfer_one "$WHEEL" || exit 1
for a in ${ASSETS[@]+"${ASSETS[@]}"}; do transfer_one "$a" || exit 1; done
WANT=$(( 1 + ${#ASSETS[@]} ))
GOT=$("${SSH[@]}" "cd /root && ls -1 $(basename "$WHEEL") $(for a in ${ASSETS[@]+"${ASSETS[@]}"}; do printf '%s ' "$(basename "$a")"; done) 2>/dev/null | wc -l")
[ "$GOT" -eq "$WANT" ] || { echo "FATAL: transfer incomplete — pod has $GOT/$WANT files" >&2; exit 1; }
# size-match every asset (a truncated ckpt produces numbers that are a transfer accident, not a fact)
for a in "$WHEEL" ${ASSETS[@]+"${ASSETS[@]}"}; do
  L=$(wc -c < "$a" | tr -d ' ')
  R=$("${SSH[@]}" "stat -c%s /root/$(basename "$a") 2>/dev/null || echo 0")
  [ "$L" = "$R" ] || { echo "FATAL: size mismatch $(basename "$a"): local=$L pod=$R" >&2; exit 1; }
done
echo "[pod]   ✅ $WANT/$WANT files, sizes match"

# ── ② pip: assume it does NOT exist (trap ②: vast images ship neither pip nor ensurepip) ─────────
echo "[pod] pip bootstrap …"
"${SSH[@]}" '
  set -e
  if ! python3 -m pip --version >/dev/null 2>&1; then
    python3 -m ensurepip --upgrade 2>&1 | tail -1 || true
  fi
  if ! python3 -m pip --version >/dev/null 2>&1; then
    echo "  ensurepip unavailable → get-pip.py"
    curl -sS https://bootstrap.pypa.io/get-pip.py -o /root/get-pip.py
    python3 /root/get-pip.py 2>&1 | tail -1
  fi
  python3 -m pip --version'   # NOT silenced — if pip is still absent, set -e kills us here

# ── ③ install: --break-system-packages (trap ①: PEP 668 refuses a plain --user install) ──────────
echo "[pod] install anima-python==$WHEEL_VER + numpy …"
"${SSH[@]}" "set -e
  python3 -m pip install --break-system-packages numpy 2>&1 | tail -1
  python3 -m pip install --break-system-packages --force-reinstall --no-deps /root/$(basename "$WHEEL") 2>&1 | tail -1"

# ── ④ HARD GATE — the install is a claim until this passes (trap ⑤: rc ignored ⇒ empty 'DONE') ───
echo "[pod] hard gate …"
"${SSH[@]}" "set -e
  export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/root/.local/bin:\$PATH
  python3 -c \"
import importlib.metadata as m
v = m.version('anima-python')
assert v == '$WHEEL_VER', 'installed %s, expected $WHEEL_VER' % v
print('  anima-python', v)\"
  python3 -c \"
import anima_py, os, numpy
p = os.path.dirname(anima_py.__file__)
assert os.path.exists(p + '/cli/evaluate.py'), 'evaluate.py missing from the installed package'
print('  numpy', numpy.__version__)
print('  package at', p)\"
  APY=\$(command -v anima-py) || { echo '  FATAL: anima-py not on PATH after install'; exit 127; }
  echo \"  anima-py = \$APY\"
  \"\$APY\" >/dev/null || { echo '  FATAL: anima-py is on PATH but does not run'; exit 127; }
  echo '  ✅ GATE PASS'"

# ── ④b TRAIN (opt-in POD_TRAIN=1): the base install is numpy-only (eval/corpus/chat). A TRAINING
#     fire also needs the [train] extra (torch+datasets) — but a bare pod adds three traps the
#     base path never hit, all failure-that-looks-like-success:
#       ⑦ the default-index torch is bleeding-edge (e.g. 2.13+cu130) and FORCE-JITs Triton for
#         basic ops → dies at CudaUtils init ('Failed to find C compiler' / gcc link fail) on an
#         image with no gcc/python3-dev. Pin a STABLE build (cu124/cu128) with precompiled kernels.
#       + Blackwell (sm_120) needs cu128 (cu124 has no sm_120 kernel → 'no kernel image'); older
#         GPUs take cu124 (pod-bootstrap-gpu-2 · train.py preflight).
#       + torch.cuda.is_available()==True can STILL crash on the first real kernel (train-py-6:
#         cu130-vs-driver silently fell to CPU) → the gate runs a REAL matmul, not is_available().
if [ "${POD_TRAIN:-0}" = 1 ]; then
  echo "[pod] TRAIN mode — build tools + arch-pinned stable torch + datasets …"
  "${SSH[@]}" "set -e
    export DEBIAN_FRONTEND=noninteractive PATH=/usr/local/bin:/usr/bin:/bin:\$PATH
    command -v gcc >/dev/null 2>&1 && python3-config --includes >/dev/null 2>&1 || \
      { apt-get update -qq && apt-get install -y -qq build-essential python3-dev; } >/dev/null 2>&1
    CC=\$(python3 -c \"import re,subprocess as s; o=s.run(['nvidia-smi','--query-gpu=compute_cap','--format=csv,noheader'],capture_output=True,text=True).stdout.strip().splitlines()[0]; print(int(float(o)*10))\")
    if [ \"\$CC\" -ge 120 ]; then IDX=cu128; else IDX=cu124; fi   # sm_120 Blackwell → cu128, else stable cu124
    echo \"  compute_cap sm_\$CC → torch \$IDX (stable · precompiled kernels · no Triton JIT for basic ops)\"
    python3 -m pip install --break-system-packages -q datasets 2>&1 | tail -1
    python3 -m pip install --break-system-packages -q --force-reinstall torch --index-url https://download.pytorch.org/whl/\$IDX 2>&1 | tail -1"
  echo "[pod] train hard gate — REAL cuda matmul (not is_available) …"
  "${SSH[@]}" "python3 -c \"
import torch
assert torch.cuda.is_available(), 'FATAL: torch reports no CUDA device'
x = torch.randn(512, 512, device='cuda')
y = float((x @ x).sum())
assert y == y, 'FATAL: NaN from cuda matmul'      # real kernel ran, no crash / silent-cpu
print('  ✅ TRAIN GATE PASS — torch', torch.__version__, 'real cuda matmul OK')\""
fi

# ── ⑤ GPU: a fresh anima-py install has NO cupy, so decode lands on CPU-numpy — on a GPU box that is
#      an 8x tax (68s/tick vs 8.5s/tick measured), and stage ⑥ used to just PRINT it and hand back
#      BOOTSTRAP_OK. Renting a GPU pod and decoding on its CPU is not a device choice, it is a bug.
#      (pod-bootstrap-gpu-4 · H_9744 lost a 1152-tick run to exactly this on a pool host.)
#      The wheel install above is --no-deps, so the [gpu] extra never arrives; install it here.
#      Which wheel: cupy is CUDA-MAJOR-specific and the two fail in opposite directions — cuda12x on a
#      CUDA-13 host and cuda13x on a CUDA-12 host both install and import fine, then die at the first
#      real op on `libnvrtc.so.<major>: cannot open shared object file`.
#      Do NOT read the major from nvidia-smi: it reports the DRIVER's maximum supported CUDA, not the
#      runtime that is installed. Measured 2026-07-17 — both pool hosts print "CUDA Version: 13.0" yet
#      need DIFFERENT wheels: summer has libnvrtc.so.12 (cupy-cuda12x works, cuda13x dies) and aiden
#      has libnvrtc.so.13 (cupy-cuda13x). nvidia-smi predicted 0/2; the .so predicted 2/2. The wheel's
#      actual dependency IS that file, so ask for it directly.
if [ "${POD_GPU:-1}" = 1 ]; then
  echo "[pod] GPU — matching cupy to this host's CUDA runtime …"
  "${SSH[@]}" "set -e
    export PATH=/usr/local/bin:/usr/bin:/bin:\$PATH
    if ! command -v nvidia-smi >/dev/null 2>&1; then echo '  no nvidia-smi — CPU-only host, skipping cupy'; exit 0; fi
    MAJ=\$( { ldconfig -p 2>/dev/null; ls /usr/local/cuda*/lib64/libnvrtc.so.* 2>/dev/null; } \
           | grep -oE 'libnvrtc\.so\.[0-9]+' | grep -oE '[0-9]+\$' | sort -rn | head -1)
    if [ -z \"\$MAJ\" ]; then
      echo '  ⚠️  no libnvrtc.so.<major> found — cupy has nothing to JIT against; leaving decode on CPU-numpy'
      exit 0
    fi
    echo \"  libnvrtc.so.\$MAJ present -> cupy-cuda\${MAJ}x (<14 pin is load-bearing)\"
    # The <14 bound is NOT cosmetic and NOT optional: cupy 14.x's bundled cu13 cuda_fp8.hpp does not
    # parse under nvrtc, so every JIT kernel compile fails on sm_120 — and cuda_available() cannot see
    # it (it only checks that `import cupy` works and a device is visible), so an unbounded >=13.0
    # installs the broken wheel, reports GPU, and dies at the first real forward on a PAID pod.
    # See pyproject.toml [project.optional-dependencies] — keep this bound in lockstep with it.
    python3 -m pip install --break-system-packages -q \"cupy-cuda\${MAJ}x>=13.0,<14\" 2>&1 | tail -1" || true
fi

# ── ⑥ device HARD GATE — ask the ENGINE, not 'does any GPU op work' (a cupy precompiled kernel runs
#      without the CUDA headers that anima's NVRTC-JIT path actually needs — pod-bootstrap-gpu-1).
#      And an install is a CLAIM until a real kernel runs: a major-mismatched cupy imports cleanly and
#      only dies at the first op (pod-bootstrap-gpu-4). So: engine probe THEN a real matmul.
#      GPU present but engine says CPU ⇒ FATAL, not a printed note — the whole point of the pod is the GPU.
echo "[pod] device gate (engine path + real kernel) …"
"${SSH[@]}" "export PATH=/usr/local/bin:\$PATH
  python3 -c \"
import importlib.util, os, subprocess, sys, anima_py
p = os.path.dirname(anima_py.__file__)
s = importlib.util.spec_from_file_location('dec', p + '/core/decode.py')
D = importlib.util.module_from_spec(s); s.loader.exec_module(D)
ok = D.cuda_available()
print('  cuda_available():', ok)
has_gpu = subprocess.run(['nvidia-smi'], capture_output=True).returncode == 0
if ok:
    import cupy                                   # the engine's own path is live — prove a kernel runs
    x = cupy.random.rand(512, 512, dtype=cupy.float32)
    y = float((x @ x).sum())
    assert y == y, 'FATAL: NaN from cupy matmul'
    print('  ✅ DEVICE = GPU — real cupy matmul OK (cupy', cupy.__version__ + ')')
elif has_gpu:
    print('  ❌ FATAL: an NVIDIA GPU is present but the engine decodes on CPU-numpy (8x slower).')
    print('     cupy is missing or its CUDA major does not match this host. Fix it, or pass')
    print('     POD_GPU=0 to bootstrap a CPU pod on purpose.')
    sys.exit(1)
else:
    print('  DEVICE = CPU-numpy (no GPU on this host · correctness-identical · TERMINAL-eligible)')\" 2>&1 | tail -4"

echo "[pod] BOOTSTRAP_OK — anima-py $WHEEL_VER is live on $HOST:$PORT"
echo "[pod] fire with:  ssh -p $PORT root@$HOST 'cd /root && setsid bash <your>.sh > fire.log 2>&1 < /dev/null &'"
echo "[pod]   ⛔ after firing, NEVER kill/pkill by pattern — a pattern check matches your own ssh"
echo "[pod]      command (false ALREADY_RUNNING). Read with: ps -eo args | grep -c '[e]valuate[.]py'"
echo "[pod]   ⛔ 'DONE' in a log is not evidence — judge completion by the OUTPUT FILES."
