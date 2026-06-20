#!/usr/bin/env bash
# H_1459 retrieval-bind — DIRECT-ssh orchestrator (hexa cloud exec uses <host> --port N,
# not host:port; we use plain ssh/scp for transport and hexa cloud only for rent/teardown).
# Inference-only: upload probes + read-only base ckpt -> run 3-seed probe -> pull -> teardown.
set -uo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"; REPO="$(cd ../.. && pwd)"
LOG="$HERE/run_direct.local.log"
ID="${ID:?need ID}"; HOST="${HOST:?need HOST}"; PORT="${PORT:?need PORT}"
PROV=vast
SSH="ssh -o StrictHostKeyChecking=no -o ConnectTimeout=20 -p $PORT root@$HOST"
SCP="scp -o StrictHostKeyChecking=no -P $PORT"
echo "[run] $(date) ID=$ID HOST=$HOST:$PORT" | tee "$LOG"

cleanup() {
  echo "[teardown] hexa cloud rm $ID" | tee -a "$LOG"
  hexa cloud rm "$ID" --provider "$PROV" --force 2>&1 | tee -a "$LOG" || true
  echo "[teardown] remaining pods:" | tee -a "$LOG"
  hexa cloud list --provider "$PROV" 2>&1 | tee -a "$LOG" || true
}
trap cleanup EXIT

echo "[setup] mkdir + upload probes" | tee -a "$LOG"
$SSH 'mkdir -p /workspace/g6/probes /workspace/g6/ckpt /workspace/g6/out' 2>&1 | tee -a "$LOG"
$SCP "$HERE/g6_rb_common.py"        "root@$HOST:/workspace/g6/probes/" 2>&1 | tee -a "$LOG"
$SCP "$HERE/h1451_retrieval_bind.py" "root@$HOST:/workspace/g6/probes/" 2>&1 | tee -a "$LOG"
$SCP "$REPO/tool/gauge_lib.py"      "root@$HOST:/workspace/g6/probes/" 2>&1 | tee -a "$LOG"
$SCP "$REPO/state/universe-probes/h1129_midcap_broad_converged_recombination.py" "root@$HOST:/workspace/g6/probes/" 2>&1 | tee -a "$LOG"
$SCP "$REPO/state/universe-probes/h1305_g6_ideation_falsifiability.py" "root@$HOST:/workspace/g6/probes/" 2>&1 | tee -a "$LOG"
echo "[setup] upload base ckpt (606MB, read-only)" | tee -a "$LOG"
$SCP "$REPO/state/chat_303m/h1129c_chat.pt" "root@$HOST:/workspace/g6/ckpt/h1129c_chat.pt" 2>&1 | tee -a "$LOG"
echo "[setup] ckpt sha on pod:" | tee -a "$LOG"
$SSH 'sha256sum /workspace/g6/ckpt/h1129c_chat.pt' 2>&1 | tee -a "$LOG"

echo "[run] fire probe (3 seeds internal)" | tee -a "$LOG"
$SSH 'cd /workspace/g6/probes && \
  G6_PROBES=/workspace/g6/probes G6_CKPT=/workspace/g6/ckpt/h1129c_chat.pt G6_OUT=/workspace/g6/out \
  python3 h1451_retrieval_bind.py --device cuda:0' 2>&1 | tee "$HERE/h1451_run.log" | tee -a "$LOG"

echo "[pull] result json" | tee -a "$LOG"
$SCP "root@$HOST:/workspace/g6/out/h1451_result.json" "$HERE/h1451_result.json" 2>&1 | tee -a "$LOG" || true
echo "[pull] done:" | tee -a "$LOG"
ls -la "$HERE/h1451_result.json" 2>&1 | tee -a "$LOG" || true
echo "[run] complete — teardown via trap" | tee -a "$LOG"
