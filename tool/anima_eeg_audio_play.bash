#!/usr/bin/env bash
# Play pre-generated audio cue (zero synthesis overhead)
# Usage: anima_eeg_audio_play.bash <cue_key>
# Example: anima_eeg_audio_play.bash countdown_3_2_1_start
# raw#9 bash carve-out (audio playback macOS native).
set -uo pipefail
CACHE="/Users/ghost/core/anima/state/anima_eeg_audio_cache_2026_05_05"
KEY="${1:-}"
if [[ -z "$KEY" ]]; then
  echo "Usage: $0 <cue_key>" >&2
  echo "Available cues:" >&2
  ls -1 "$CACHE" 2>/dev/null | sed 's/\.aiff$//' | sed 's/^/  /' >&2
  exit 1
fi
FILE="$CACHE/$KEY.aiff"
if [[ ! -f "$FILE" ]]; then
  echo "[audio-play ERR] cue not cached: $KEY ($FILE)" >&2
  echo "Run: bash /Users/ghost/core/anima/tool/anima_eeg_audio_cache_generate.bash" >&2
  exit 1
fi
afplay "$FILE"
