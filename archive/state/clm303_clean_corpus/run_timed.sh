#!/usr/bin/env bash
# run_timed.sh — POD-side timed ON/OFF cache-hit decode comparison for device-resident decode.
#
# Runs on the GPU pod AFTER cli/eval_pod.sh has pushed core/cli/ckpt and built once (cache warm).
# Measures: OFF#1, OFF#2 (determinism control), ON (CLM_PROD_DEVRESIDENT=1) — wall + gate lines +
# OWN-GEMM DEVICE firing. Writes /root/anima/RESULT.txt for harvest.
#
# Usage (on pod):  cd /root/anima && bash run_timed.sh <ckpt_name> <gen>
set -uo pipefail
CKPT="${1:?usage: run_timed.sh <ckpt_name> <gen>}"
GEN="${2:-4}"
cd /root/anima
export PATH=/root/.hx/bin:$PATH HEXA_FRAG_LOG=1

run_one() {  # $1=label $2=devresident(0|1) -> writes <label>.txt, echoes wall sec
  local label="$1" dev="$2" t0 t1
  t0=$(date +%s.%N)
  if [ "$dev" = 1 ]; then
    CLM_PROD_DEVRESIDENT=1 hexa run cli/anima.hexa -- eval "$CKPT" --gen "$GEN" > "$label.txt" 2>&1
  else
    hexa run cli/anima.hexa -- eval "$CKPT" --gen "$GEN" > "$label.txt" 2>&1
  fi
  t1=$(date +%s.%N)
  awk -v a="$t0" -v b="$t1" 'BEGIN{printf "%.2f", b-a}'
}

# RAW decode output minus run-to-run noise (timing/PID/wall/FRAG-log/transient WARN) — the gate
# score lines (G0..G6 · kwr · coherent · fab · distinct) stay. Comparing the RAW stripped output
# (not a fragile gate-grep) avoids the empty-vs-empty false-PASS trap (2026-06-25: a gate-grep that
# extracted nothing made diff trivially PASS while the real gates diverged).
strip_noise() { grep -avE 'sec|PID=|WALL|elapsed|FRAG|OWN-GEMM|\[psi_loader\]|^\[' "$1" 2>/dev/null; }
owngemm() { grep -c 'OWN-GEMM-FIRED.*DEVICE path' "$1" 2>/dev/null || echo 0; }

echo "[run_timed] OFF#1 ..."; OFF1=$(run_one off1 0)
echo "[run_timed] OFF#2 (determinism) ..."; OFF2=$(run_one off2 0)
echo "[run_timed] ON (CLM_PROD_DEVRESIDENT=1) ..."; ON=$(run_one on 1)

strip_noise off1 > off1.gates; strip_noise off2 > off2.gates; strip_noise on > on.gates
# empty-guard: a comparison over empty extractions is NOT a pass (fail-loud)
if [ ! -s off1.gates ] || [ ! -s on.gates ]; then
  OFF_DET="INDETERMINATE(empty-extract)"; BYTE_EXACT="INDETERMINATE(empty-extract — inspect raw off1.txt/on.txt)"
else
  OFF_DET=$(diff -q off1.gates off2.gates >/dev/null 2>&1 && echo IDENTICAL || echo DIFFER)
  BYTE_EXACT=$(diff -q off1.gates on.gates  >/dev/null 2>&1 && echo PASS || echo FAIL)
fi

{
  echo "CKPT=$CKPT GEN=$GEN"
  echo "OFF1_WALL_SEC=$OFF1"
  echo "OFF2_WALL_SEC=$OFF2"
  echo "ON_WALL_SEC=$ON"
  echo "OFF_DETERMINISM=$OFF_DET           # OFF#1 vs OFF#2 gate lines (IDENTICAL = eval deterministic)"
  echo "BYTE_EXACT_OFF_VS_ON=$BYTE_EXACT    # PASS = device decode == host (a_clm_gen_pipeline)"
  echo "OFF1_OWNGEMM_DEVICE=$(owngemm off1)"
  echo "ON_OWNGEMM_DEVICE=$(owngemm on)"
  echo "HEXA_VERSION=$(hexa --version 2>/dev/null | head -1)"
  echo "--- OFF#1 gates ---"; cat off1.gates
  echo "--- ON gates ---";   cat on.gates
  echo "ALL_DONE=1"
} > RESULT.txt
echo "[run_timed] done → RESULT.txt"
cat RESULT.txt
