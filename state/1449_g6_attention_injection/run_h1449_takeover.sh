#!/usr/bin/env bash
# H_1449 TAKEOVER — the first orchestrator FAILED to parse instance_id and exited,
# leaving pod 41790442 orphaned (RENTING, no teardown). This script adopts the
# ALREADY-RENTED pod by its EXPLICIT id (NO re-rent, NO list-last) and drives it.
#
# SAFETY: ID is hardcoded to MY pod 41790442 only (resolved ssh8.vast.ai:30442).
# The other live pods (41790357 H_1440, 41790394 H_1441, 41790525 H_1439) belong to
# PARALLEL agents and are NEVER touched. Teardown trap removes 41790442 only.
set -uo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"
REPO="$(cd ../.. && pwd)"
LOG="$HERE/run_h1449_takeover.log"
PROV=vast
ID=41790442
HOST=ssh8.vast.ai
PORT=30442
echo "[takeover] $(date) pod=$ID host=$HOST:$PORT" | tee "$LOG"

cleanup() {
  echo "[teardown] hexa cloud rm $ID --provider $PROV --force" | tee -a "$LOG"
  hexa cloud rm "$ID" --provider "$PROV" --force 2>&1 | tee -a "$LOG" || true
  echo "[teardown] remaining pods:" | tee -a "$LOG"
  hexa cloud list --provider "$PROV" 2>&1 | tee -a "$LOG" || true
}
trap cleanup EXIT

EXC() { hexa cloud exec "$HOST" --port "$PORT" --insecure -- "$@" 2>&1 | tee -a "$LOG"; }
CPTO() { hexa cloud copy-to "$HOST" "$1" "$2" --port "$PORT" --insecure 2>&1 | tee -a "$LOG"; }
CPFROM() { hexa cloud copy-from "$HOST" "$1" "$2" --port "$PORT" --insecure 2>&1 | tee -a "$LOG"; }

# ── wait for ssh to come up (pod may still be provisioning) ──
echo "[wait] ssh reachability" | tee -a "$LOG"
ok=0
for i in $(seq 1 60); do
  if hexa cloud exec "$HOST" --port "$PORT" --insecure -- 'echo READY' 2>/dev/null | grep -q READY; then
    ok=1; echo "[wait] ssh up at iter $i" | tee -a "$LOG"; break
  fi
  sleep 15
done
if [ "$ok" != 1 ]; then echo "[FATAL] ssh never came up" | tee -a "$LOG"; exit 1; fi

# ── setup ──
EXC 'mkdir -p /workspace/g6/out /workspace/g6/ckpt /workspace/g6/probes'
EXC 'python3 -c "import torch;print(\"torch\",torch.__version__,\"cuda\",torch.cuda.is_available(),torch.cuda.get_device_name(0))" 2>&1 | head -3'

echo "[upload] code+probes" | tee -a "$LOG"
for f in g6_common.py h1435_continued_pretrain.py h1449_attention_injection.py \
         gauge_lib.py h1129_midcap_broad_converged_recombination.py \
         h1305_g6_ideation_falsifiability.py; do
  CPTO "$HERE/$f" "/workspace/g6/probes/$f"
done
echo "[upload] base ckpt (606MB) ..." | tee -a "$LOG"
CPTO "$REPO/state/chat_303m/h1129c_chat.pt" /workspace/g6/ckpt/h1129c_chat.pt

# ── pod driver: 3 seeds sequential ──
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
CPTO "$HERE/_pod_driver.sh" /workspace/g6/_pod_driver.sh

echo "[fire] background driver" | tee -a "$LOG"
FIRE_OUT="$(hexa cloud fire "$HOST" --log /workspace/g6/driver.log --port "$PORT" --insecure \
  -- bash /workspace/g6/_pod_driver.sh 2>&1)"
echo "$FIRE_OUT" | tee -a "$LOG"
PID="$(echo "$FIRE_OUT" | grep -oE 'pid[ =:]+[0-9]+' | grep -oE '[0-9]+' | head -1)"
echo "[fire] PID=$PID" | tee -a "$LOG"

# ── inline poll (a_cpu_local_no_waiter) ──
for i in $(seq 1 360); do  # up to 360*30s = 3h
  sleep 30
  alive=1
  if [ -n "$PID" ]; then
    hexa cloud poll "$HOST" "$PID" --port "$PORT" --insecure >/dev/null 2>&1 || alive=0
  else
    # no pid -> check for completion sentinel
    EXC 'grep -q "ALL SEEDS DONE" /workspace/g6/driver.log 2>/dev/null && echo DONE || echo RUN' | grep -q DONE && alive=0
  fi
  if [ "$alive" = 0 ]; then echo "[poll] done at iter $i" | tee -a "$LOG"; break; fi
  if [ $((i % 8)) -eq 0 ]; then
    echo "[poll] iter $i tail:" | tee -a "$LOG"
    EXC 'tail -4 /workspace/g6/driver.log'
  fi
done

# ── PULL before teardown (a_fire_recover_complete) ──
echo "[pull] driver log + results + ckpts" | tee -a "$LOG"
CPFROM /workspace/g6/driver.log "$HERE/driver.log"
for SEED in 7 4302 4303; do
  CPFROM "/workspace/g6/out/h1449_result_seed${SEED}.json" "$HERE/h1449_result_seed${SEED}.json"
  CPFROM "/workspace/g6/out/h1449_seed${SEED}.log" "$HERE/h1449_seed${SEED}.log"
  CPFROM "/workspace/g6/out/h1449_attention_injection_seed${SEED}.pt" "$HERE/h1449_attention_injection_seed${SEED}.pt"
done
echo "[pull] local files:" | tee -a "$LOG"
ls -la "$HERE"/h1449_result_seed*.json "$HERE"/h1449_*.pt 2>&1 | tee -a "$LOG" || true
echo "[run] complete — teardown via trap" | tee -a "$LOG"
