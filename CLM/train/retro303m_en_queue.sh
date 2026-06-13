#!/usr/bin/env bash
# retro303m_en_queue.sh — QUEUE GUARD: fire the anima-303M-RETRO train the moment BOTH the
# aiden ByteGPT 303M sweep AND the ConvMoE queue have finished, WITHOUT contending for the GPU.
#
# Runs DETACHED on aiden (nohup). Polls every $POLL s for the FIRE CONDITION:
#   (1) all 4 ByteGPT configs {baseline_fast,reg_fast,baseline_gentle,reg_gentle} have a
#       status=done row in the ByteGPT sweep ledger  (axis-1 done)
#   AND
#   (2) the ConvMoE queue has fired+returned: its sentinel exists AND its queue.log shows
#       "run.sh returned" (axis-3 done) — OR (belt+suspenders) the GPU is idle (<1GB used).
# On fire it READS THE BYTEGPT WINNER (best G0>=0.5, then G1, G2, lowest val) from the sweep
# ledger and trains anima-303M-RETRO with that recipe, nohup-safe.
#
# Idempotent: a sentinel ($SENT) blocks a double-fire; safe to relaunch.
set -u
REPO="${RETRO_REPO:-/home/aiden/core/anima_retro303}"
SWEEP_UNIVERSE="${SWEEP_UNIVERSE:-/home/aiden/core/anima_sweep303/UNIVERSE}"
BYTEGPT_LEDGER="${BYTEGPT_LEDGER:-/home/aiden/core/anima_sweep303/state/sweep_303m_en/ledger.jsonl}"
CONVMOE_SENT="${CONVMOE_SENT:-/tmp/convmoe_303m/queue_fired.sentinel}"
CONVMOE_QLOG="${CONVMOE_QLOG:-/tmp/convmoe_303m/queue.log}"
CORPUS="${CORPUS:-/tmp/sweep_303m/en_wiki_120mb.txt}"
LEDGER="${LEDGER:-$REPO/state/retro303m_en/ledger.jsonl}"
CKDIR="${CKDIR:-$REPO/state/retro303m_en/ckpt}"
LOGDIR="${LOGDIR:-/tmp/retro303m}"
STEPS="${STEPS:-12000}"
POLL="${POLL:-300}"
SENT="$LOGDIR/queue_fired.sentinel"
mkdir -p "$LOGDIR" "$CKDIR" "$(dirname "$LEDGER")"
QLOG="$LOGDIR/queue.log"
echo "[retro-queue] $(date) watcher START pid=$$ poll=${POLL}s" >> "$QLOG"

bytegpt_done () {
  local n
  n=$(python3 - "$BYTEGPT_LEDGER" <<'PY' 2>/dev/null
import json,sys
need={"baseline_fast","reg_fast","baseline_gentle","reg_gentle"}; done=set()
try:
    for l in open(sys.argv[1]):
        try: r=json.loads(l)
        except: continue
        if r.get("status")=="done" and r.get("config") in need: done.add(r["config"])
except FileNotFoundError: pass
print(len(need & done))
PY
)
  [ "${n:-0}" -ge 4 ]
}
convmoe_done () {
  # ConvMoE queue fired AND its run.sh returned (axis-3 complete)
  if [ -f "$CONVMOE_SENT" ] && grep -q "returned" "$CONVMOE_QLOG" 2>/dev/null; then return 0; fi
  return 1
}
gpu_idle () {
  local used
  used=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)
  [ "${used:-9999}" -lt 1000 ]
}

if [ -f "$SENT" ]; then
  echo "[retro-queue] $(date) sentinel present — already fired, exiting" >> "$QLOG"; exit 0
fi
while true; do
  if bytegpt_done && { convmoe_done || gpu_idle; }; then
    echo "[retro-queue] $(date) FIRE: bytegpt 4/4 done AND (convmoe done OR gpu idle)" >> "$QLOG"
    touch "$SENT"
    nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader >> "$QLOG" 2>&1
    cd "$REPO/CLM/train" || { echo "[retro-queue] no repo $REPO" >> "$QLOG"; exit 3; }
    python3 -u retro303m_en_train.py \
      --corpus "$CORPUS" \
      --sweep_universe "$SWEEP_UNIVERSE" \
      --sweep_ledger "$BYTEGPT_LEDGER" \
      --cfg retro303m_en --host aiden \
      --ledger "$LEDGER" --ckpt "$CKDIR/retro303m_en.pt" \
      --d 1024 --n_layer 24 --n_head 16 --block 512 \
      --bs 8 --accum 4 --steps "$STEPS" \
      --anchor_len 256 --anchor_gap 64 \
      --grad_ckpt --eval_every 500 \
      >> "$LOGDIR/retro303m_en.log" 2>&1
    echo "[retro-queue] $(date) retro303m train returned rc=$?" >> "$QLOG"
    exit 0
  fi
  sleep "$POLL"
done
