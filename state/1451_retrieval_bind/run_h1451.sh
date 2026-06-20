#!/usr/bin/env bash
# H_1451 — RETRIEVAL-BIND local orchestrator: rent vast GPU -> setup -> run inference probe
# (3 seeds, NO training — frozen base + retrieval weld) -> pull -> teardown.
# Safety (teammate contract): hexa cloud only (c11); parse instance_id DIRECTLY from rent
# stdout (NOT list-last); numeric id = vast only; teardown trap; verify pod 0 after.
# base ckpt PRESERVED (read-only on pod); inference-only so no ckpt to pull back (c5).
set -uo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"
REPO="$(cd ../.. && pwd)"
LOG="$HERE/run_h1451.local.log"
echo "[run] $(date) HERE=$HERE REPO=$REPO" | tee "$LOG"

PROV=vast
ID="${REUSE_ID:-}"
cleanup() {
  if [ -n "$ID" ]; then
    echo "[teardown] hexa cloud rm $ID" | tee -a "$LOG"
    hexa cloud rm "$ID" --provider "$PROV" --force 2>&1 | tee -a "$LOG" || true
  fi
  echo "[teardown] remaining pods:" | tee -a "$LOG"
  hexa cloud list --provider "$PROV" 2>&1 | tee -a "$LOG" || true
}
trap cleanup EXIT

if [ -n "$ID" ]; then
  echo "[reuse] using existing pod ID=$ID (no new rent)" | tee -a "$LOG"
else
  echo "[rent] cuda devel GPU (${GPU:-any}) ..." | tee -a "$LOG"
  RENT_OUT="$(hexa cloud rent "$PROV" ${GPU:+--gpu "$GPU"} \
    --image pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel \
    --disk 40 --volume-gb 40 \
    --onstart 'apt-get update -y && apt-get install -y git' \
    --desc 'H_1451 G6 retrieval-bind (inference-only)' \
    --owner h1451 --project anima --max-wait-sec 900 2>&1)"
  echo "$RENT_OUT" | tee -a "$LOG"
  # parse numeric instance_id DIRECTLY from rent stdout (NOT list-last)
  ID="$(echo "$RENT_OUT" | grep -oE 'created instance [0-9]+' | grep -oE '[0-9]+' | head -1)"
  [ -z "$ID" ] && ID="$(echo "$RENT_OUT" | grep -oE 'instance_id=[0-9]+' | grep -oE '[0-9]+' | head -1)"
  [ -z "$ID" ] && ID="$(echo "$RENT_OUT" | grep -oE 'instance [0-9]{6,}' | grep -oE '[0-9]{6,}' | head -1)"
  if [ -z "$ID" ]; then
    echo "[FATAL] could not parse numeric instance_id from rent stdout — abort" | tee -a "$LOG"
    exit 1
  fi
fi
echo "[rent] ID=$ID (vast numeric)" | tee -a "$LOG"

echo "[wait] ssh-ready ..." | tee -a "$LOG"
for w in $(seq 1 60); do
  if hexa cloud alive "$ID" --provider "$PROV" 2>&1 | grep -qiE 'RUNNING'; then
    HP="$(hexa cloud resolve "$ID" --provider "$PROV" 2>&1 | grep -oE '[^ ]+:[0-9]+' | head -1)"
    if [ -n "$HP" ] && hexa cloud exec "$HP" -- 'echo ssh_ok' 2>/dev/null | grep -q ssh_ok; then
      echo "[wait] ssh ready at iter $w" | tee -a "$LOG"; break
    fi
  fi
  sleep 15
done

HOST="$(hexa cloud resolve "$ID" --provider "$PROV" 2>&1 | grep -oE '[^ ]+:[0-9]+' | head -1)"
echo "[ssh] HOST=$HOST" | tee -a "$LOG"
if [ -z "$HOST" ]; then echo "[FATAL] no ssh host" | tee -a "$LOG"; exit 1; fi

# ── setup: upload probes + base ckpt (read-only) ──
hexa cloud exec "$HOST" -- 'mkdir -p /workspace/g6/out /workspace/g6/probes /workspace/g6/ckpt' 2>&1 | tee -a "$LOG"

echo "[upload] probe dir" | tee -a "$LOG"
hexa cloud copy-to "$HOST" "$HERE/g6_rb_common.py"        /workspace/g6/probes/g6_rb_common.py 2>&1 | tee -a "$LOG"
hexa cloud copy-to "$HOST" "$HERE/h1451_retrieval_bind.py" /workspace/g6/probes/h1451_retrieval_bind.py 2>&1 | tee -a "$LOG"
hexa cloud copy-to "$HOST" "$REPO/tool/gauge_lib.py"      /workspace/g6/probes/gauge_lib.py 2>&1 | tee -a "$LOG"
hexa cloud copy-to "$HOST" "$REPO/state/universe-probes/h1129_midcap_broad_converged_recombination.py" /workspace/g6/probes/h1129_midcap_broad_converged_recombination.py 2>&1 | tee -a "$LOG"
hexa cloud copy-to "$HOST" "$REPO/state/universe-probes/h1305_g6_ideation_falsifiability.py" /workspace/g6/probes/h1305_g6_ideation_falsifiability.py 2>&1 | tee -a "$LOG"

echo "[upload] base ckpt (606MB, read-only) ..." | tee -a "$LOG"
hexa cloud copy-to "$HOST" "$REPO/state/chat_303m/h1129c_chat.pt" \
  /workspace/g6/ckpt/h1129c_chat.pt --verify-sha 2>&1 | tee -a "$LOG"

# ── driver: single inference run (the probe loops 3 seeds internally) ──
cat > "$HERE/_pod_driver.sh" <<'POD'
#!/usr/bin/env bash
set -uo pipefail
export G6_PROBES=/workspace/g6/probes
export G6_CKPT=/workspace/g6/ckpt/h1129c_chat.pt
export G6_OUT=/workspace/g6/out
cd /workspace/g6/probes
echo "==== H_1451 retrieval-bind (inference, 3 seeds internal) ===="
python3 h1451_retrieval_bind.py --device cuda:0 2>&1 | tee /workspace/g6/out/h1451_run.log
echo "==== H_1451 DONE ===="
POD
hexa cloud copy-to "$HOST" "$HERE/_pod_driver.sh" /workspace/g6/_pod_driver.sh 2>&1 | tee -a "$LOG"

echo "[fire] background driver" | tee -a "$LOG"
FIRE_OUT="$(hexa cloud fire "$HOST" --log /workspace/g6/driver.log \
  -- bash /workspace/g6/_pod_driver.sh 2>&1)"
echo "$FIRE_OUT" | tee -a "$LOG"
PID="$(echo "$FIRE_OUT" | grep -oE 'pid[ =:]+[0-9]+' | grep -oE '[0-9]+' | head -1)"
echo "[fire] PID=$PID" | tee -a "$LOG"

# ── inline poll until done (a_cpu_local_no_waiter: poll here, no Monitor) ──
for i in $(seq 1 120); do  # up to 120*30s = 1h (inference-only, should be minutes)
  sleep 30
  if ! hexa cloud poll "$HOST" "$PID" >/dev/null 2>&1; then
    echo "[poll] pid $PID dead at iter $i" | tee -a "$LOG"
    break
  fi
  if [ $((i % 5)) -eq 0 ]; then
    echo "[poll] iter $i alive; tail:" | tee -a "$LOG"
    hexa cloud exec "$HOST" -- 'tail -4 /workspace/g6/driver.log' 2>&1 | tee -a "$LOG" || true
  fi
done

# ── PULL results BEFORE teardown (a_fire_recover_complete; no trained ckpt here) ──
echo "[pull] driver log + result json" | tee -a "$LOG"
hexa cloud copy-from "$HOST" /workspace/g6/driver.log "$HERE/driver.log" 2>&1 | tee -a "$LOG" || true
hexa cloud copy-from "$HOST" /workspace/g6/out/h1451_run.log "$HERE/h1451_run.log" 2>&1 | tee -a "$LOG" || true
hexa cloud copy-from "$HOST" /workspace/g6/out/h1451_result.json "$HERE/h1451_result.json" 2>&1 | tee -a "$LOG" || true
echo "[pull] done. local files:" | tee -a "$LOG"
ls -la "$HERE"/h1451_result.json "$HERE"/h1451_run.log 2>&1 | tee -a "$LOG" || true
echo "[run] complete — teardown via trap" | tee -a "$LOG"
