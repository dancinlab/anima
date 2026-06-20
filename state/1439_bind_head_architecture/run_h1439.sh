#!/usr/bin/env bash
# H_1439 — local orchestrator: rent vast H100 -> setup -> train bind-head + shuffle-ctrl
# -> evaluate frozen 5-bar (3 seeds internal) -> PULL ckpt+result -> teardown.
# Safety (teammate contract): hexa cloud ONLY (c11); parse instance_id from rent stdout;
# numeric id = vast only; teardown trap; verify pod 0 after; ckpt PULL before teardown
# (a_fire_recover_complete); no credential logging (c7).
set -uo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"
REPO="$(cd ../.. && pwd)"
LOG="$HERE/run_h1439.local.log"
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
  --desc 'H_1439 G6 learnable bind-head architecture' \
  --owner h1439 --project anima --max-wait-sec 900 2>&1)"
echo "$RENT_OUT" | tee -a "$LOG"

ID="$(echo "$RENT_OUT" | grep -oE 'instance_id=[0-9]+' | head -1 | cut -d= -f2)"
if [ -z "$ID" ]; then
  ID="$(echo "$RENT_OUT" | grep -oE '\bid[ =:]+[0-9]{6,}' | grep -oE '[0-9]{6,}' | head -1)"
fi
if [ -z "$ID" ]; then
  echo "[FATAL] could not parse numeric instance_id from rent stdout — abort" | tee -a "$LOG"
  exit 1
fi
echo "[rent] ID=$ID (vast numeric)" | tee -a "$LOG"

HOST="$(hexa cloud resolve "$ID" --provider "$PROV" 2>&1 | grep -oE '[^ ]+:[0-9]+' | head -1)"
echo "[ssh] HOST=$HOST" | tee -a "$LOG"
if [ -z "$HOST" ]; then echo "[FATAL] no ssh host" | tee -a "$LOG"; exit 1; fi

# devel image may lack git
hexa cloud exec "$HOST" -- 'command -v git >/dev/null 2>&1 || (apt-get update -y && apt-get install -y git)' 2>&1 | tee -a "$LOG" || true
hexa cloud exec "$HOST" -- 'mkdir -p /workspace/g6/out /workspace/g6/ckpt /workspace/g6/probes' 2>&1 | tee -a "$LOG"

echo "[upload] probe dir (driver + bundled probes both land in /workspace/g6/probes)" | tee -a "$LOG"
# driver/common live flat in $HERE; the reused gauge/h1129/h1305 live in $HERE/probes/
for f in g6_common.py h1435_continued_pretrain.py h1439_bind_head_architecture.py; do
  hexa cloud copy-to "$HOST" "$HERE/$f" "/workspace/g6/probes/$f" 2>&1 | tee -a "$LOG"
done
for f in gauge_lib.py h1129_midcap_broad_converged_recombination.py \
         h1305_g6_ideation_falsifiability.py; do
  hexa cloud copy-to "$HOST" "$HERE/probes/$f" "/workspace/g6/probes/$f" 2>&1 | tee -a "$LOG"
done
echo "[upload] base ckpt (606MB) ..." | tee -a "$LOG"
hexa cloud copy-to "$HOST" "$REPO/state/chat_303m/h1129c_chat.pt" \
  /workspace/g6/ckpt/h1129c_chat.pt --verify-sha 2>&1 | tee -a "$LOG"

# ── single-invocation pod driver (3 seeds + train + shuffle-ctrl + ablation internal) ──
cat > "$HERE/_pod_driver.sh" <<'POD'
#!/usr/bin/env bash
set -uo pipefail
export G6_PROBES=/workspace/g6/probes
export G6_CKPT=/workspace/g6/ckpt/h1129c_chat.pt
export G6_CORPUS=/workspace/g6/probes/corpus.txt
export G6_OUT=/workspace/g6/out
cd /workspace/g6/probes
# corpus presence for NOVEL _corpus_absent (h1305) — gen a tiny placeholder if missing
[ -f "$G6_CORPUS" ] || echo "placeholder corpus for novelty grep" > "$G6_CORPUS"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
echo "==== H_1439 bind-head (3 seeds internal) ===="
python3 h1439_bind_head_architecture.py --device cuda:0 --steps 600 --lines 4000 --r 128 \
  2>&1 | tee /workspace/g6/out/h1439.log
echo "==== H_1439 DONE ===="
POD
hexa cloud copy-to "$HOST" "$HERE/_pod_driver.sh" /workspace/g6/_pod_driver.sh 2>&1 | tee -a "$LOG"

echo "[fire] background driver" | tee -a "$LOG"
FIRE_OUT="$(hexa cloud fire "$HOST" --log /workspace/g6/driver.log \
  -- bash /workspace/g6/_pod_driver.sh 2>&1)"
echo "$FIRE_OUT" | tee -a "$LOG"
PID="$(echo "$FIRE_OUT" | grep -oE 'pid[ =:]+[0-9]+' | grep -oE '[0-9]+' | head -1)"
echo "[fire] PID=$PID" | tee -a "$LOG"

# ── inline poll (a_cpu_local_no_waiter: poll here, no Monitor) ──
for i in $(seq 1 240); do  # up to 2h
  sleep 30
  if ! hexa cloud poll "$HOST" "$PID" >/dev/null 2>&1; then
    echo "[poll] pid $PID dead at iter $i" | tee -a "$LOG"
    break
  fi
  if [ $((i % 10)) -eq 0 ]; then
    echo "[poll] iter $i alive; tail:" | tee -a "$LOG"
    hexa cloud exec "$HOST" -- 'tail -3 /workspace/g6/driver.log' 2>&1 | tee -a "$LOG" || true
  fi
done

# ── PULL results + ckpt BEFORE teardown (a_fire_recover_complete) ──
echo "[pull] driver log + result + ckpt" | tee -a "$LOG"
hexa cloud copy-from "$HOST" /workspace/g6/driver.log "$HERE/driver.log" 2>&1 | tee -a "$LOG" || true
hexa cloud copy-from "$HOST" /workspace/g6/out/h1439.log "$HERE/h1439.log" 2>&1 | tee -a "$LOG" || true
hexa cloud copy-from "$HOST" /workspace/g6/out/h1439_result.json "$HERE/h1439_result.json" 2>&1 | tee -a "$LOG" || true
hexa cloud copy-from "$HOST" /workspace/g6/out/h1439_bind_head.pt "$HERE/h1439_bind_head.pt" 2>&1 | tee -a "$LOG" || true
echo "[pull] done. local files:" | tee -a "$LOG"
ls -la "$HERE"/h1439_result.json "$HERE"/h1439_bind_head.pt 2>&1 | tee -a "$LOG" || true
echo "[run] complete — teardown via trap" | tee -a "$LOG"
