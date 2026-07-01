#!/usr/bin/env bash
# H_1456 ADOPT — the rent succeeded (pod 41797592) but the orchestrator's
# instance_id parser failed on the 'created instance <ID>' stdout variant and
# trap-exited with empty ID (orphan, alive). Rather than waste it + re-rent into a
# congested provider, ADOPT the live pod: setup -> upload -> fire -> SSH-flap-
# resilient poll/pull -> KEEP-ALIVE-guard -> teardown. Only touches MY pod 41797592.
set -uo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"; REPO="$(cd ../.. && pwd)"
LOG="$HERE/adopt_h1456.local.log"
PROV=vast
ID=41797592
HOST=ssh9.vast.ai
PORT=37592
echo "[adopt] $(date) ID=$ID HOST=$HOST:$PORT" | tee "$LOG"

cleanup() {
  echo "[teardown] (cleanup invoked)" | tee -a "$LOG"
}
trap cleanup EXIT

# wait for ssh-ready (pod may be RENTING)
echo "[wait] ssh-ready ..." | tee -a "$LOG"
for w in $(seq 1 40); do
  if hexa cloud exec "$HOST" --port "$PORT" -- 'echo READY' 2>/dev/null | grep -q READY; then
    echo "[wait] ssh up at iter $w" | tee -a "$LOG"; break
  fi
  sleep 15
done

hexa cloud exec "$HOST" --port "$PORT" -- 'command -v git >/dev/null 2>&1 || (apt-get update -y && apt-get install -y git)' 2>&1 | tee -a "$LOG" || true
hexa cloud exec "$HOST" --port "$PORT" -- 'mkdir -p /workspace/g6/out /workspace/g6/ckpt /workspace/g6/probes' 2>&1 | tee -a "$LOG"

echo "[upload] probes + driver" | tee -a "$LOG"
for f in g6_common.py h1456_idea_metacognition.py; do
  hexa cloud copy-to "$HOST" --port "$PORT" "$HERE/$f" "/workspace/g6/probes/$f" 2>&1 | tee -a "$LOG"
done
for f in gauge_lib.py h1129_midcap_broad_converged_recombination.py h1305_g6_ideation_falsifiability.py; do
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
echo "==== H_1456 idea-metacognition (base+trained+shuffle-ctrl, 3 seeds) ===="
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

# SSH-flap-resilient poll: done iff result.json present on pod
for i in $(seq 1 360); do
  sleep 30
  RES="$(hexa cloud exec "$HOST" --port "$PORT" -- 'test -f /workspace/g6/out/h1456_result.json && echo PRESENT || echo ABSENT' 2>/dev/null | grep -oE 'PRESENT|ABSENT' | head -1)"
  if [ "$RES" = "PRESENT" ]; then echo "[poll] result PRESENT iter $i" | tee -a "$LOG"; break; fi
  if [ $((i % 10)) -eq 0 ]; then
    echo "[poll] iter $i (res=$RES); tail:" | tee -a "$LOG"
    hexa cloud exec "$HOST" --port "$PORT" -- 'tail -3 /workspace/g6/driver.log' 2>&1 | tee -a "$LOG" || true
  fi
done

pull_retry() {
  local remote="$1" dst="$2" tries=8
  for t in $(seq 1 $tries); do
    if hexa cloud copy-from "$HOST" --port "$PORT" "$remote" "$dst" 2>&1 | tee -a "$LOG"; then
      [ -s "$dst" ] && { echo "[pull] OK $remote (try $t)" | tee -a "$LOG"; return 0; }
    fi
    echo "[pull] retry $t/$tries $remote — sleep 20" | tee -a "$LOG"; sleep 20
  done
  echo "[pull] FAILED $remote" | tee -a "$LOG"; return 1
}

echo "[pull] retry-hardened" | tee -a "$LOG"
pull_retry /workspace/g6/driver.log "$HERE/driver.log" || true
pull_retry /workspace/g6/out/h1456.log "$HERE/h1456.log" || true
RES_OK=0; CKPT_OK=0
pull_retry /workspace/g6/out/h1456_result.json "$HERE/h1456_result.json" && RES_OK=1
pull_retry /workspace/g6/out/h1456_idea_metacognition.pt "$HERE/h1456_idea_metacognition.pt" && CKPT_OK=1
echo "[pull] RES_OK=$RES_OK CKPT_OK=$CKPT_OK" | tee -a "$LOG"
ls -la "$HERE"/h1456_result.json "$HERE"/h1456_idea_metacognition.pt 2>&1 | tee -a "$LOG" || true

if [ "$RES_OK" != "1" ]; then
  echo "[KEEP-ALIVE] result NOT pulled — pod $ID ($HOST:$PORT) left ALIVE. Recover then:" | tee -a "$LOG"
  echo "[KEEP-ALIVE]   hexa cloud copy-from $HOST --port $PORT /workspace/g6/out/h1456_result.json $HERE/" | tee -a "$LOG"
  echo "[KEEP-ALIVE]   hexa cloud rm $ID --provider $PROV --force" | tee -a "$LOG"
  trap - EXIT; exit 2
fi

echo "[teardown] result recovered — rm $ID" | tee -a "$LOG"
hexa cloud rm "$ID" --provider "$PROV" --force 2>&1 | tee -a "$LOG" || true
hexa cloud list --provider "$PROV" 2>&1 | tee -a "$LOG" | grep -q "$ID" && echo "[teardown] WARN still present" | tee -a "$LOG" || echo "[teardown] $ID gone" | tee -a "$LOG"
trap - EXIT
echo "[adopt] complete" | tee -a "$LOG"
