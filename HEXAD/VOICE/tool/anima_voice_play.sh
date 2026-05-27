#!/usr/bin/env bash
# tool/anima_voice_play.sh — VOICE Phase 2 CoreAudio wrapper
#
# Runs anima_voice_smoke.hexa to (a) verify F-VOICE-1..5 5/5 PASS and
# (b) emit /tmp/anima_voice_demo_{loud,silent}.wav, then plays both via
# Mac CoreAudio (afplay).
#
# USAGE
#   bash tool/anima_voice_play.sh
#
# Skip-playback (CI / verify only):
#   bash tool/anima_voice_play.sh --no-play
set -euo pipefail

ANIMA_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ANIMA_ROOT"

NO_PLAY=0
for arg in "$@"; do
    case "$arg" in
        --no-play) NO_PLAY=1 ;;
        *) echo "unknown arg: $arg"; exit 2 ;;
    esac
done

echo "[1/3] hexa smoke + WAV emit ..."
RESOURCE_LOCAL_HEXA=1 hexa run tool/anima_voice_smoke.hexa | tail -25

echo ""
echo "[2/3] verify WAV files emitted ..."
for f in /tmp/anima_voice_demo_loud.wav /tmp/anima_voice_demo_silent.wav; do
    if [ ! -f "$f" ]; then
        echo "  MISSING: $f"
        exit 1
    fi
    bytes=$(wc -c < "$f" | tr -d ' ')
    echo "  $f  ($bytes bytes)"
done

if [ "$NO_PLAY" = "1" ]; then
    echo ""
    echo "[3/3] --no-play set, skipping afplay"
    exit 0
fi

echo ""
echo "[3/3] afplay (loud → silent) ..."
echo "  $ afplay /tmp/anima_voice_demo_loud.wav"
afplay /tmp/anima_voice_demo_loud.wav
echo "  $ afplay /tmp/anima_voice_demo_silent.wav"
afplay /tmp/anima_voice_demo_silent.wav

echo ""
echo "DONE."
