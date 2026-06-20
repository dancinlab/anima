#!/usr/bin/env bash
# H_1449 — local orchestrator: rent vast H100 -> setup -> train 3 seeds -> pull -> teardown.
# Safety (teammate contract): hexa cloud only (c11); parse instance_id from rent stdout;
# numeric id = vast only; teardown trap; verify pod 0 after.
set -uo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"
REPO="$(cd ../.. && pwd)"
LOG="$HERE/run_h1449.local.log"
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
  echo "[rent] cuda devel H100 ..." | tee -a "$LOG"
  RENT_OUT="$(hexa cloud rent "$PROV" --gpu H100 \
    --image pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel \
    --disk 60 --volume-gb 60 \
    --desc 'H_1449 G6 attention-injection root-fix' \
    --owner h1449 --project anima --max-wait-sec 900 2>&1)"
  echo "$RENT_OUT" | tee -a "$LOG"
  # vast rent stdout forms: "created instance NNNNN" | "instance_id=NNN" | "id NNN"
  ID="$(echo "$RENT_OUT" | grep -oE 'created instance [0-9]+' | grep -oE '[0-9]+' | head -1)"
  [ -z "$ID" ] && ID="$(echo "$RENT_OUT" | grep -oE 'instance_id=[0-9]+' | grep -oE '[0-9]+' | head -1)"
  [ -z "$ID" ] && ID="$(echo "$RENT_OUT" | grep -oE 'instance [0-9]{6,}' | grep -oE '[0-9]{6,}' | head -1)"
  if [ -z "$ID" ]; then
    echo "[FATAL] could not parse numeric instance_id from rent stdout — abort" | tee -a "$LOG"
    exit 1
  fi
fi
echo "[rent] ID=$ID (vast numeric)" | tee -a "$LOG"

# wait for ssh-ready (pod may still be provisioning)
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

# resolve ssh host:port
HOST="$(hexa cloud resolve "$ID" --provider "$PROV" 2>&1 | grep -oE '[^ ]+:[0-9]+' | head -1)"
echo "[ssh] HOST=$HOST" | tee -a "$LOG"
if [ -z "$HOST" ]; then echo "[FATAL] no ssh host" | tee -a "$LOG"; exit 1; fi

# ── setup: git (devel image may lack), upload probes + base ckpt ──
hexa cloud exec "$HOST" -- 'mkdir -p /workspace/g6/out /workspace/g6/ckpt' 2>&1 | tee -a "$LOG"

echo "[upload] probe dir" | tee -a "$LOG"
for f in g6_common.py h1435_continued_pretrain.py h1449_attention_injection.py \
         gauge_lib.py h1129_midcap_broad_converged_recombination.py \
         h1305_g6_ideation_falsifiability.py; do
  hexa cloud copy-to "$HOST" "$HERE/$f" "/workspace/g6/probes/$f" 2>&1 | tee -a "$LOG"
done
echo "[upload] base ckpt (1.2GB) ..." | tee -a "$LOG"
hexa cloud copy-to "$HOST" "$REPO/state/chat_303m/h1129c_chat.pt" \
  /workspace/g6/ckpt/h1129c_chat.pt --verify-sha 2>&1 | tee -a "$LOG"

# ── fire 3 seeds sequentially on the pod (single GPU) ──
cat > "$HERE/_pod_driver.sh" <<'POD'
#!/usr/bin/env bash
set -uo pipefail
export G6_PROBES=/workspace/g6/probes
export G6_CKPT=/workspace/g6/ckpt/h1129c_chat.pt
export G6_OUT=/workspace/g6/out
cd /workspace/g6/probes
for SEED in 7 4302 4303; do
  echo "==== H_1449 SEED $SEED ===="
  python3 h1449_attention_injection.py --device cuda:0 --steps 600 --lines 6000 --seed $SEED \
    2>&1 | tee /workspace/g6/out/h1449_seed${SEED}.log
done
echo "==== ALL SEEDS DONE ===="
POD
hexa cloud copy-to "$HOST" "$HERE/_pod_driver.sh" /workspace/g6/_pod_driver.sh 2>&1 | tee -a "$LOG"

echo "[fire] background driver" | tee -a "$LOG"
FIRE_OUT="$(hexa cloud fire "$HOST" --log /workspace/g6/driver.log \
  -- bash /workspace/g6/_pod_driver.sh 2>&1)"
echo "$FIRE_OUT" | tee -a "$LOG"
PID="$(echo "$FIRE_OUT" | grep -oE 'pid[ =:]+[0-9]+' | grep -oE '[0-9]+' | head -1)"
echo "[fire] PID=$PID" | tee -a "$LOG"

# ── inline poll until done (a_cpu_local_no_waiter: poll here, no Monitor) ──
for i in $(seq 1 240); do  # up to 240*30s = 2h
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

# ── PULL results + ckpts BEFORE teardown (a_fire_recover_complete) ──
echo "[pull] driver log + results + ckpts" | tee -a "$LOG"
hexa cloud copy-from "$HOST" /workspace/g6/driver.log "$HERE/driver.log" 2>&1 | tee -a "$LOG" || true
for SEED in 7 4302 4303; do
  hexa cloud copy-from "$HOST" "/workspace/g6/out/h1449_result_seed${SEED}.json" \
    "$HERE/h1449_result_seed${SEED}.json" 2>&1 | tee -a "$LOG" || true
  hexa cloud copy-from "$HOST" "/workspace/g6/out/h1449_seed${SEED}.log" \
    "$HERE/h1449_seed${SEED}.log" 2>&1 | tee -a "$LOG" || true
  hexa cloud copy-from "$HOST" "/workspace/g6/out/h1449_attention_injection_seed${SEED}.pt" \
    "$HERE/h1449_attention_injection_seed${SEED}.pt" 2>&1 | tee -a "$LOG" || true
done
echo "[pull] done. local files:" | tee -a "$LOG"
ls -la "$HERE"/h1449_result_seed*.json "$HERE"/h1449_*.pt 2>&1 | tee -a "$LOG" || true
echo "[run] complete — teardown via trap" | tee -a "$LOG"
