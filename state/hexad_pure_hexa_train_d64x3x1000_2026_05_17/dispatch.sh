#!/usr/bin/env bash
# dispatch.sh — pure-hexa hexa-cpu @ d=64·3L·1000-step on Mac local (ubu fallback)
#
# Context: original target was ubu d=96·3L or d=128·4L (RAM headroom), but
# d=96·3L on ubu triggered system-level OOM-thrash + 75+min sshd distress.
# This dispatch falls back to Mac local at the proven-safe d=64·3L width
# (12 GB peak per Agent #2a) with extended 1000-step horizon (3.33× #2a).
#
# Usage: HEXA_MAC_BUILD_OK=1 HEXA_MEM_UNLIMITED=1 ./dispatch.sh
#        or: /usr/bin/time -l ./dispatch.sh
#
# Expected wall ≈ 20 min on Mac M-series CPU per #2a scaling
# (300 step = 360s → 1000 step ≈ 1200s).

set -eu

HEXA_MAC_BUILD_OK=${HEXA_MAC_BUILD_OK:-1}
HEXA_MEM_UNLIMITED=${HEXA_MEM_UNLIMITED:-1}
export HEXA_MAC_BUILD_OK HEXA_MEM_UNLIMITED

cd /Users/ghost/core/anima

FIRE_SCRIPT="state/hexad_pure_hexa_train_d64x3x1000_2026_05_17/d_converge_fire_d64x3x1000.hexa"

if [ ! -f "$FIRE_SCRIPT" ]; then
    echo "FATAL: fire script not found: $FIRE_SCRIPT" >&2
    exit 1
fi

echo "[$(date)] launching d=64·3L·1000-step pure-hexa hexa-cpu fire"
echo "  HEXA_MAC_BUILD_OK=$HEXA_MAC_BUILD_OK HEXA_MEM_UNLIMITED=$HEXA_MEM_UNLIMITED"
echo "  fire: $FIRE_SCRIPT"

LOG="state/hexad_pure_hexa_train_d64x3x1000_2026_05_17/train.log"
/usr/bin/time -l hexa run "$FIRE_SCRIPT" 2>&1 | tee "$LOG"

echo "[$(date)] fire complete; log: $LOG"
