#!/usr/bin/env bash
# tool/anima_heartbeat_emit.sh — periodic liveness emit for h100_auto_kill probe.
#
# Usage:
#   bash tool/anima_heartbeat_emit.sh &              # default 30s, /workspace/.heartbeat
#   ANIMA_HEARTBEAT_INTERVAL=10 \
#   ANIMA_HEARTBEAT_PATH=/tmp/.hb \
#       bash tool/anima_heartbeat_emit.sh &
#
# Convention (matches anima_stuck_self_kill_lib.hexa):
#   - touches mtime every N seconds while the parent training process is alive
#   - h100_auto_kill probe (last_activity_source=heartbeat) reads stat -c %Y
#     and computes age = now - mtime; if age >= threshold_minutes → STOP
#   - missing file → stat rc!=0 → -1 (UNKNOWN, no kill) per probe contract;
#     this protects pods that have not yet started emitting
#
# Why a separate emitter (instead of letting the trainer itself touch):
#   - decouples liveness from the trainer's main loop — a stuck inner step
#     does NOT keep emitting (the parent shell still runs but has no progress)
#   - if the user wants stricter "training step heartbeat" they can call
#     `touch ${ANIMA_HEARTBEAT_PATH}` from the step callback instead of running
#     this background loop
#
# Exits cleanly on SIGTERM/SIGINT so the launch script can supervise it.

set -u

INTERVAL="${ANIMA_HEARTBEAT_INTERVAL:-30}"
HB_PATH="${ANIMA_HEARTBEAT_PATH:-/workspace/.heartbeat}"

mkdir -p "$(dirname "${HB_PATH}")" 2>/dev/null || true

touch "${HB_PATH}"
echo "[anima_heartbeat_emit] pid=$$ path=${HB_PATH} interval=${INTERVAL}s"

cleanup() {
    echo "[anima_heartbeat_emit] pid=$$ exit on signal"
    exit 0
}
trap cleanup TERM INT HUP

while true; do
    touch "${HB_PATH}"
    sleep "${INTERVAL}"
done
