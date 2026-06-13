#!/usr/bin/env bash
# convmoe_303m_en_queue.sh — QUEUE GUARD: fire the ConvMoE sweep the MOMENT aiden's
# ByteGPT 303M sweep finishes, WITHOUT competing for the GPU while it runs.
#
# Runs DETACHED on aiden (nohup). Polls the ByteGPT sweep ledger every 5 min for the
# FIRE CONDITION: all 4 ByteGPT configs {baseline_fast,reg_fast,baseline_gentle,
# reg_gentle} have a status=done row. (Belt-and-suspenders: also accepts the orch
# log's "ALL DONE" line.) On fire it execs convmoe_303m_en_run.sh in the foreground
# of this detached process, so the whole ConvMoE sweep then runs nohup-safe too.
#
# Idempotent: a sentinel file ($SENT) blocks a double-fire; safe to relaunch.
set -u
ROOT="${CONVMOE_ROOT:-/home/aiden/core/anima_convmoe303}"
BYTEGPT_LEDGER="${BYTEGPT_LEDGER:-/home/aiden/core/anima_sweep303/state/sweep_303m_en/ledger.jsonl}"
BYTEGPT_ORCHLOG="${BYTEGPT_ORCHLOG:-/tmp/sweep_303m/orch.log}"
LOGDIR="${CONVMOE_LOGDIR:-/tmp/convmoe_303m}"
RUN="$ROOT/CLM/train/convmoe_303m_en_run.sh"
SENT="$LOGDIR/queue_fired.sentinel"
POLL="${POLL:-300}"
mkdir -p "$LOGDIR"
QLOG="$LOGDIR/queue.log"

echo "[queue] $(date) watcher START pid=$$ poll=${POLL}s ledger=$BYTEGPT_LEDGER" >> "$QLOG"

bytegpt_done () {
  # all 4 configs have a status=done row?
  local n
  n=$(python3 - "$BYTEGPT_LEDGER" <<'PY' 2>/dev/null
import json,sys
need={"baseline_fast","reg_fast","baseline_gentle","reg_gentle"}
done=set()
try:
    for l in open(sys.argv[1]):
        try: r=json.loads(l)
        except: continue
        if r.get("status")=="done" and r.get("config") in need:
            done.add(r["config"])
except FileNotFoundError:
    pass
print(len(need & done))
PY
)
  [ "${n:-0}" -ge 4 ] && return 0
  # fallback: orchestrator wrote ALL DONE
  grep -q "ALL DONE" "$BYTEGPT_ORCHLOG" 2>/dev/null && return 0
  return 1
}

if [ -f "$SENT" ]; then
  echo "[queue] $(date) sentinel present — already fired, exiting" >> "$QLOG"
  exit 0
fi

while true; do
  if bytegpt_done; then
    echo "[queue] $(date) FIRE CONDITION MET — aiden ByteGPT sweep done; launching ConvMoE sweep" >> "$QLOG"
    touch "$SENT"
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader >> "$QLOG" 2>&1
    bash "$RUN" >> "$QLOG" 2>&1
    echo "[queue] $(date) ConvMoE sweep run.sh returned rc=$?" >> "$QLOG"
    exit 0
  fi
  sleep "$POLL"
done
