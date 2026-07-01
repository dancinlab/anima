#!/usr/bin/env bash
# H_1456 (orig task-id "H_1453 IDEA-METACOGNITION") — local orchestrator:
# rent vast H100 -> setup -> continued-pretrain on META-CONCEPT corpus + shuffle-ctrl
# -> evaluate frozen 5-bar (3 seeds internal) -> PULL ckpt+result -> teardown.
# Safety (teammate contract): hexa cloud ONLY (c11); parse instance_id from rent stdout
# (NOT list-last); numeric id = vast only; teardown trap; verify pod 0 after; ckpt PULL
# before teardown (a_fire_recover_complete); no credential logging (c7).
# ★ DOES NOT touch other agents' live pods (41792045 / 41790357 / 41790525) — only my ID.
set -uo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"
REPO="$(cd ../.. && pwd)"
LOG="$HERE/run_h1456.local.log"
echo "[run] $(date) HERE=$HERE REPO=$REPO" | tee "$LOG"

PROV=vast
ID=""
cleanup() {
  if [ -n "$ID" ]; then
    echo "[teardown] hexa cloud rm $ID" | tee -a "$LOG"
    hexa cloud rm "$ID" --provider "$PROV" --force 2>&1 | tee -a "$LOG" || true
  fi
  echo "[teardown] remaining pods:" | tee -a "$LOG"
  hexa cloud list --provider "$PROV" 2>&1 | tee -a "$LOG" || true
}
trap cleanup EXIT

echo "[rent] cuda devel H100 ..." | tee -a "$LOG"
RENT_OUT="$(hexa cloud rent "$PROV" --gpu H100 \
  --image pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel \
  --disk 60 --volume-gb 60 \
  --desc 'H_1456 G6 idea-metacognition continued-pretrain' \
  --owner h1456 --project anima --max-wait-sec 900 2>&1)"
echo "$RENT_OUT" | tee -a "$LOG"

ID="$(echo "$RENT_OUT" | grep -oE 'instance_id=[0-9]+' | head -1 | cut -d= -f2)"
if [ -z "$ID" ]; then
  # vast stdout variant: 'created instance <ID>' / 'pod=<ID>'
  ID="$(echo "$RENT_OUT" | grep -oE 'created instance [0-9]{6,}' | grep -oE '[0-9]{6,}' | head -1)"
fi
if [ -z "$ID" ]; then
  ID="$(echo "$RENT_OUT" | grep -oE 'pod=[0-9]{6,}' | grep -oE '[0-9]{6,}' | head -1)"
fi
if [ -z "$ID" ]; then
  ID="$(echo "$RENT_OUT" | grep -oE '\bid[ =:]+[0-9]{6,}' | grep -oE '[0-9]{6,}' | head -1)"
fi
if [ -z "$ID" ]; then
  echo "[FATAL] could not parse numeric instance_id from rent stdout — abort" | tee -a "$LOG"
  exit 1
fi
echo "[rent] ID=$ID (vast numeric)" | tee -a "$LOG"

# hexa cloud verbs take <host> [--port N] as SEPARATE args (host:port-in-one fails
# hostname resolution). Parse clean host= / port= from the rent stdout.
HOST="$(echo "$RENT_OUT" | grep -oE '^host=[^ ]+' | head -1 | cut -d= -f2)"
PORT="$(echo "$RENT_OUT" | grep -oE '^port=[0-9]+' | head -1 | cut -d= -f2)"
if [ -z "$HOST" ] || [ -z "$PORT" ]; then
  # fallback: resolve, split host:port
  HP="$(hexa cloud resolve "$ID" --provider "$PROV" 2>&1 | grep -oE '[^ ]+:[0-9]+' | head -1)"
  HOST="${HP%%:*}"; PORT="${HP##*:}"
fi
echo "[ssh] HOST=$HOST PORT=$PORT" | tee -a "$LOG"
if [ -z "$HOST" ] || [ -z "$PORT" ]; then echo "[FATAL] no ssh host/port" | tee -a "$LOG"; exit 1; fi

hexa cloud exec "$HOST" --port "$PORT" -- 'command -v git >/dev/null 2>&1 || (apt-get update -y && apt-get install -y git)' 2>&1 | tee -a "$LOG" || true
hexa cloud exec "$HOST" --port "$PORT" -- 'mkdir -p /workspace/g6/out /workspace/g6/ckpt /workspace/g6/probes' 2>&1 | tee -a "$LOG"

echo "[upload] driver + common + reused probes -> /workspace/g6/probes" | tee -a "$LOG"
for f in g6_common.py h1456_idea_metacognition.py; do
  hexa cloud copy-to "$HOST" --port "$PORT" "$HERE/$f" "/workspace/g6/probes/$f" 2>&1 | tee -a "$LOG"
done
for f in gauge_lib.py h1129_midcap_broad_converged_recombination.py \
         h1305_g6_ideation_falsifiability.py; do
  hexa cloud copy-to "$HOST" --port "$PORT" "$HERE/probes/$f" "/workspace/g6/probes/$f" 2>&1 | tee -a "$LOG"
done
echo "[upload] base ckpt (606MB) ..." | tee -a "$LOG"
hexa cloud copy-to "$HOST" --port "$PORT" "$REPO/state/chat_303m/h1129c_chat.pt" \
  /workspace/g6/ckpt/h1129c_chat.pt --verify-sha 2>&1 | tee -a "$LOG"

cat > "$HERE/_pod_driver.sh" <<'POD'
#!/usr/bin/env bash
set -uo pipefail
export G6_PROBES=/workspace/g6/probes
export G6_CKPT=/workspace/g6/ckpt/h1129c_chat.pt
export G6_CORPUS=/workspace/g6/probes/corpus.txt
export G6_OUT=/workspace/g6/out
cd /workspace/g6/probes
[ -f "$G6_CORPUS" ] || echo "placeholder corpus for novelty grep" > "$G6_CORPUS"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
echo "==== H_1456 idea-metacognition (base + trained + shuffle-ctrl, 3 seeds internal) ===="
python3 h1456_idea_metacognition.py --device cuda:0 --steps 400 --lines 4000 \
  2>&1 | tee /workspace/g6/out/h1456.log
echo "==== H_1456 DONE ===="
POD
hexa cloud copy-to "$HOST" --port "$PORT" "$HERE/_pod_driver.sh" /workspace/g6/_pod_driver.sh 2>&1 | tee -a "$LOG"

echo "[fire] background driver" | tee -a "$LOG"
FIRE_OUT="$(hexa cloud fire "$HOST" --port "$PORT" --log /workspace/g6/driver.log \
  -- bash /workspace/g6/_pod_driver.sh 2>&1)"
echo "$FIRE_OUT" | tee -a "$LOG"
PID="$(echo "$FIRE_OUT" | grep -oE 'pid[ =:]+[0-9]+' | grep -oE '[0-9]+' | head -1)"
echo "[fire] PID=$PID" | tee -a "$LOG"

# ── SSH-flap-RESILIENT poll: the prior run lost the ckpt because an SSH-255
# transport outage was misread as PID-death → premature pull-fail → teardown.
# Fix: a poll iteration counts as DONE only when result.json EXISTS on the pod;
# SSH errors are tolerated as transient and DO NOT end the wait. ──
DONE=0
for i in $(seq 1 360); do  # up to 3h
  sleep 30
  RES="$(hexa cloud exec "$HOST" --port "$PORT" -- 'test -f /workspace/g6/out/h1456_result.json && echo PRESENT || echo ABSENT' 2>/dev/null | grep -oE 'PRESENT|ABSENT' | head -1)"
  if [ "$RES" = "PRESENT" ]; then
    echo "[poll] result.json PRESENT on pod at iter $i — proceed to pull" | tee -a "$LOG"
    DONE=1
    break
  fi
  if [ $((i % 10)) -eq 0 ]; then
    echo "[poll] iter $i (res=$RES); tail:" | tee -a "$LOG"
    hexa cloud exec "$HOST" --port "$PORT" -- 'tail -3 /workspace/g6/driver.log' 2>&1 | tee -a "$LOG" || true
  fi
done

# ── pull with RETRY (rides out transient SSH outages) ──
pull_retry() {
  local remote="$1" local_dst="$2" tries=8
  for t in $(seq 1 $tries); do
    if hexa cloud copy-from "$HOST" --port "$PORT" "$remote" "$local_dst" 2>&1 | tee -a "$LOG"; then
      [ -s "$local_dst" ] && { echo "[pull] OK $remote (try $t)" | tee -a "$LOG"; return 0; }
    fi
    echo "[pull] retry $t/$tries for $remote (SSH flap?) — sleep 20" | tee -a "$LOG"
    sleep 20
  done
  echo "[pull] FAILED after $tries: $remote" | tee -a "$LOG"
  return 1
}

echo "[pull] driver log + result + ckpt BEFORE teardown (retry-hardened)" | tee -a "$LOG"
pull_retry /workspace/g6/driver.log "$HERE/driver.log" || true
pull_retry /workspace/g6/out/h1456.log "$HERE/h1456.log" || true
RES_OK=0; CKPT_OK=0
pull_retry /workspace/g6/out/h1456_result.json "$HERE/h1456_result.json" && RES_OK=1
pull_retry /workspace/g6/out/h1456_idea_metacognition.pt "$HERE/h1456_idea_metacognition.pt" && CKPT_OK=1
echo "[pull] done. RES_OK=$RES_OK CKPT_OK=$CKPT_OK" | tee -a "$LOG"
ls -la "$HERE"/h1456_result.json "$HERE"/h1456_idea_metacognition.pt 2>&1 | tee -a "$LOG" || true

# ── TEARDOWN GUARD (a_fire_recover_complete > cost): do NOT destroy the pod if the
# result was not recovered. Keep it alive (billing) + LOUD recover instruction. ──
if [ "$RES_OK" != "1" ]; then
  echo "[KEEP-ALIVE] result.json NOT pulled — DISABLING teardown trap to protect the run." | tee -a "$LOG"
  echo "[KEEP-ALIVE] pod $ID ($HOST:$PORT) left ALIVE. Recover then rm:" | tee -a "$LOG"
  echo "[KEEP-ALIVE]   hexa cloud copy-from $HOST --port $PORT /workspace/g6/out/h1456_result.json $HERE/h1456_result.json" | tee -a "$LOG"
  echo "[KEEP-ALIVE]   hexa cloud copy-from $HOST --port $PORT /workspace/g6/out/h1456_idea_metacognition.pt $HERE/h1456_idea_metacognition.pt" | tee -a "$LOG"
  echo "[KEEP-ALIVE]   hexa cloud rm $ID --provider $PROV --force   # ONLY after recovery" | tee -a "$LOG"
  trap - EXIT
  exit 2
fi
echo "[run] complete — result recovered (RES_OK=$RES_OK CKPT_OK=$CKPT_OK) — teardown via trap" | tee -a "$LOG"
