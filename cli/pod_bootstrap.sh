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
# Exit 0 ⟺ the pod can run `anima-py` AND every named asset arrived intact. Anything else exits
# non-zero with the reason. There is no --force and no skip: a bootstrap that "mostly worked" is the
# thing this script exists to prevent.
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
  local f="$1" base; base=$(basename "$f"); local n=0
  if command -v rsync >/dev/null 2>&1 && [ "$POD_HAS_RSYNC" = 1 ]; then
    until rsync --partial --append-verify --timeout=180 \
          -e "ssh -p $PORT -o StrictHostKeyChecking=no -o ServerAliveInterval=20" \
          "$f" "root@$HOST:/root/$base"; do
      n=$((n+1)); [ "$n" -ge 8 ] && { echo "FATAL: rsync failed 8× on $base" >&2; return 1; }
      echo "[pod]   rsync retry $n/8: $base (resuming)"; sleep 5
    done
  else
    until "${SCP[@]}" "$f" "root@$HOST:/root/$base"; do
      n=$((n+1)); [ "$n" -ge 8 ] && { echo "FATAL: scp failed 8× on $base" >&2; return 1; }
      echo "[pod]   scp retry $n/8: $base"; sleep 5
    done
  fi
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

# ── ⑤ device: ask the ENGINE, not 'does any GPU op work' (a cupy precompiled kernel runs without
#      the CUDA headers that anima's NVRTC-JIT path actually needs — pod-bootstrap-gpu-1) ─────────
echo "[pod] device probe (engine path) …"
"${SSH[@]}" "export PATH=/usr/local/bin:\$PATH
  python3 -c \"
import importlib.util, os, anima_py
p = os.path.dirname(anima_py.__file__)
s = importlib.util.spec_from_file_location('dec', p + '/core/decode.py')
D = importlib.util.module_from_spec(s); s.loader.exec_module(D)
ok = D.cuda_available()
print('  cuda_available():', ok)
print('  DEVICE =', 'GPU' if ok else 'CPU-numpy (correctness-identical · TERMINAL-eligible)')\" 2>&1 | tail -2" || true

echo "[pod] BOOTSTRAP_OK — anima-py $WHEEL_VER is live on $HOST:$PORT"
echo "[pod] fire with:  ssh -p $PORT root@$HOST 'cd /root && setsid bash <your>.sh > fire.log 2>&1 < /dev/null &'"
echo "[pod]   ⛔ after firing, NEVER kill/pkill by pattern — a pattern check matches your own ssh"
echo "[pod]      command (false ALREADY_RUNNING). Read with: ps -eo args | grep -c '[e]valuate[.]py'"
echo "[pod]   ⛔ 'DONE' in a log is not evidence — judge completion by the OUTPUT FILES."
