#!/usr/bin/env bash
# H_1449 v2 — robust orchestrator: rent vast H100 -> setup -> train 3 seeds -> pull -> teardown.
# Fixes vs v1: parse "created instance NNN"; use --port/--insecure exec form; retry fire on
# transient ssh refusal; re-resolve port each retry; teardown trap scoped to OUR id only.
# SAFETY: numeric id = vast only (c11); never list-last; never touch sibling pods.
set -uo pipefail
cd "$(dirname "$0")"
HERE="$(pwd)"; REPO="$(cd ../.. && pwd)"
LOG="$HERE/run_h1449_v2.log"
PROV=vast
ID="${REUSE_ID:-}"
echo "[run] $(date) HERE=$HERE" | tee "$LOG"

cleanup() {
  if [ -n "$ID" ]; then
    echo "[teardown] hexa cloud rm $ID" | tee -a "$LOG"
    hexa cloud rm "$ID" --provider "$PROV" --force 2>&1 | tee -a "$LOG" || true
  fi
  echo "[teardown] H_1449 rows remaining:" | tee -a "$LOG"
  hexa cloud list --provider "$PROV" 2>&1 | grep -E "${ID:-NOPE}|H_1449" | tee -a "$LOG" || echo "  (none)" | tee -a "$LOG"
}
trap cleanup EXIT

# ── rent (unless REUSE_ID) ──
if [ -z "$ID" ]; then
  echo "[rent] vast H100 pytorch devel ..." | tee -a "$LOG"
  RENT_OUT="$(hexa cloud rent "$PROV" --gpu H100 \
    --image pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel \
    --disk 60 --volume-gb 60 --desc 'H_1449 G6 attention-injection root-fix' \
    --owner h1449 --project anima --max-wait-sec 900 2>&1)"
  echo "$RENT_OUT" | tee -a "$LOG"
  ID="$(echo "$RENT_OUT" | grep -oE 'created instance [0-9]+' | grep -oE '[0-9]+' | head -1)"
  [ -z "$ID" ] && ID="$(echo "$RENT_OUT" | grep -oE 'instance_id=[0-9]+' | grep -oE '[0-9]+' | head -1)"
  if [ -z "$ID" ]; then echo "[FATAL] no instance_id parsed" | tee -a "$LOG"; exit 1; fi
fi
echo "[rent] ID=$ID" | tee -a "$LOG"

# ── resolve host:port (retry; vast assigns lazily) ──
HOST=""; PORT=""
resolve_hp() {
  local r; r="$(hexa cloud resolve "$ID" --provider "$PROV" 2>&1)"
  HOST="$(echo "$r" | grep -oE '^host=[^ ]+' | cut -d= -f2 | head -1)"
  PORT="$(echo "$r" | grep -oE '^port=[0-9]+' | cut -d= -f2 | head -1)"
  if [ -z "$HOST" ]; then
    local hp; hp="$(echo "$r" | grep -oE '[a-z0-9.]+\.vast\.ai:[0-9]+' | head -1)"
    HOST="${hp%%:*}"; PORT="${hp##*:}"
  fi
}

EXC() { hexa cloud exec "$HOST" --port "$PORT" --insecure -- "$@" 2>&1 | tee -a "$LOG"; }
EXC_Q() { hexa cloud exec "$HOST" --port "$PORT" --insecure -- "$@" 2>/dev/null; }
CPTO() { hexa cloud copy-to "$HOST" "$1" "$2" --port "$PORT" --insecure 2>&1 | tee -a "$LOG"; }
CPFROM() { hexa cloud copy-from "$HOST" "$1" "$2" --port "$PORT" --insecure 2>&1 | tee -a "$LOG"; }

echo "[wait] ssh-ready ..." | tee -a "$LOG"
ok=0
for i in $(seq 1 80); do
  resolve_hp
  if [ -n "$HOST" ] && [ -n "$PORT" ]; then
    if EXC_Q 'echo READY' | grep -q READY; then ok=1; echo "[wait] ssh up iter $i ($HOST:$PORT)" | tee -a "$LOG"; break; fi
  fi
  sleep 15
done
if [ "$ok" != 1 ]; then echo "[FATAL] ssh never came up" | tee -a "$LOG"; exit 1; fi

# ── setup + upload ──
EXC 'mkdir -p /workspace/g6/out /workspace/g6/ckpt /workspace/g6/probes'
EXC 'python3 -c "import torch;print(\"torch\",torch.__version__,\"cuda\",torch.cuda.is_available(),torch.cuda.get_device_name(0))"'
echo "[upload] probes" | tee -a "$LOG"
for f in g6_common.py h1435_continued_pretrain.py h1449_attention_injection.py \
         gauge_lib.py h1129_midcap_broad_converged_recombination.py \
         h1305_g6_ideation_falsifiability.py; do CPTO "$HERE/$f" "/workspace/g6/probes/$f"; done
echo "[upload] base ckpt ..." | tee -a "$LOG"
CPTO "$REPO/state/chat_303m/h1129c_chat.pt" /workspace/g6/ckpt/h1129c_chat.pt

cat > "$HERE/_pod_driver.sh" <<'POD'
#!/usr/bin/env bash
set -uo pipefail
export G6_PROBES=/workspace/g6/probes G6_CKPT=/workspace/g6/ckpt/h1129c_chat.pt G6_OUT=/workspace/g6/out
cd /workspace/g6/probes
for SEED in 7 4302 4303; do
  echo "==== H_1449 SEED $SEED ===="
  python3 h1449_attention_injection.py --device cuda:0 --steps 600 --lines 6000 --seed $SEED \
    2>&1 | tee /workspace/g6/out/h1449_seed${SEED}.log
done
echo "==== ALL SEEDS DONE ===="
POD
CPTO "$HERE/_pod_driver.sh" /workspace/g6/_pod_driver.sh

# ── fire with retry (transient ssh refusal tolerated) ──
PID=""
for attempt in 1 2 3 4 5; do
  resolve_hp
  FIRE_OUT="$(hexa cloud fire "$HOST" --port "$PORT" --insecure --log /workspace/g6/driver.log \
    -- bash /workspace/g6/_pod_driver.sh 2>&1)"
  echo "[fire attempt $attempt] $FIRE_OUT" | tee -a "$LOG"
  PID="$(echo "$FIRE_OUT" | grep -oE 'pid[ =:]+[0-9]+' | grep -oE '[0-9]+' | head -1)"
  if [ -n "$PID" ]; then echo "[fire] PID=$PID" | tee -a "$LOG"; break; fi
  # maybe it launched anyway — check for the log
  sleep 10
  if EXC_Q 'test -f /workspace/g6/driver.log && echo HASLOG' | grep -q HASLOG; then
    echo "[fire] driver.log exists despite parse miss — proceeding" | tee -a "$LOG"; break
  fi
  echo "[fire] retry in 20s ..." | tee -a "$LOG"; sleep 20
done

# ── inline poll ──
for i in $(seq 1 360); do
  sleep 30
  if EXC_Q 'grep -q "ALL SEEDS DONE" /workspace/g6/driver.log 2>/dev/null && echo DONE || echo RUN' | grep -q DONE; then
    echo "[poll] DONE at iter $i" | tee -a "$LOG"; break
  fi
  # guard: if pod vanished, stop
  if ! hexa cloud alive "$ID" --provider "$PROV" 2>/dev/null | grep -qiE 'RUNNING'; then
    echo "[poll] pod not RUNNING at iter $i — abort poll" | tee -a "$LOG"; break
  fi
  if [ $((i % 8)) -eq 0 ]; then echo "[poll] iter $i tail:" | tee -a "$LOG"; EXC 'tail -4 /workspace/g6/driver.log'; fi
done

# ── PULL before teardown ──
echo "[pull] ..." | tee -a "$LOG"
CPFROM /workspace/g6/driver.log "$HERE/driver.log"
for SEED in 7 4302 4303; do
  CPFROM "/workspace/g6/out/h1449_result_seed${SEED}.json" "$HERE/h1449_result_seed${SEED}.json"
  CPFROM "/workspace/g6/out/h1449_seed${SEED}.log" "$HERE/h1449_seed${SEED}.log"
  CPFROM "/workspace/g6/out/h1449_attention_injection_seed${SEED}.pt" "$HERE/h1449_attention_injection_seed${SEED}.pt"
done
echo "[pull] local:" | tee -a "$LOG"
ls -la "$HERE"/h1449_result_seed*.json 2>&1 | tee -a "$LOG" || true
echo "[run] complete — teardown via trap" | tee -a "$LOG"
