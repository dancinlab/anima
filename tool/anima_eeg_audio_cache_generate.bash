#!/usr/bin/env bash
# Generate anima-eeg audio cue cache (run once, idempotent)
# Pre-renders Korean voice cues to .aiff to eliminate `say` startup overhead
# (~1s/invocation × 4 cues = ~6s wall) → afplay cached file (~0.5s).
# raw#9 bash carve-out (audio I/O macOS native).
# bash 3.2 compatible (no assoc arrays — parallel index arrays).
set -uo pipefail
CACHE="/Users/ghost/core/anima/state/anima_eeg_audio_cache_2026_05_05"
mkdir -p "$CACHE"

# Korean voice cues — rate 220 wpm (한국어 적정)
KEYS=(
  "countdown_3_2_1_start"
  "ec_start"
  "eo_start"
  "phase_end"
  "final_complete"
  "failure"
  "impedance_pass"
  "impedance_fail"
)
TEXTS=(
  "삼, 이, 일, 측정 시작"
  "눈을 감으세요"
  "눈을 뜨고 정면을 바라보세요"
  "측정 종료"
  "측정 완료. 수고하셨습니다"
  "측정 실패"
  "임피던스 정상"
  "임피던스 실패. 헬멧 재조절 필요"
)

generated=0
skipped=0
total=${#KEYS[@]}
i=0
while [ $i -lt $total ]; do
  key="${KEYS[$i]}"
  text="${TEXTS[$i]}"
  out="$CACHE/$key.aiff"
  if [ ! -f "$out" ]; then
    say -v Yuna -r 220 -o "$out" "$text"
    sz=$(stat -f%z "$out" 2>/dev/null || echo "?")
    echo "[cache-gen] $key.aiff ($sz bytes) text='$text'"
    generated=$((generated+1))
  else
    echo "[cache-skip] $key.aiff already exists"
    skipped=$((skipped+1))
  fi
  i=$((i+1))
done
echo "===CACHE READY: $CACHE generated=$generated skipped=$skipped total=$total==="
