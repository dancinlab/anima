#!/usr/bin/env bash
# EEG_CLM/eeg_daemon.sh — 풀체인 상시 데몬: EEG 캡처 → A⇄G→CLM→KOSMOS → .kosmos 누적, 반복.
# 헤드셋 쓴 동안 매 사이클 짧은 EEG 를 받아 풀체인(H_1271)을 돌리고 생성기록을 누적.
# 발사: nohup bash EEG_CLM/eeg_daemon.sh > /tmp/eeg_daemon.log 2>&1 &
# 정지: touch EEG_CLM/daemon_stop   (또는 kill <pid>)
set -u
cd "$(dirname "$0")/.."          # repo root
PORT="${1:-/dev/cu.usbserial-DP04WGIQ}"
SECS="${2:-8}"
PY=EEG_CLM/.venv/bin/python
HEXA="$(command -v hexa || echo /Users/mini/.hx/bin/hexa)"
OUT=EEG_CLM/daemon_kosmos
mkdir -p "$OUT"
rm -f EEG_CLM/daemon_stop
i=0
echo "[daemon] start port=$PORT secs=$SECS $(date)"
while [ ! -f EEG_CLM/daemon_stop ]; do
  # ① 캡처 (실데이터 전용, 실패시 이 사이클 skip — 가짜 없음)
  if "$PY" EEG_CLM/capture_eeg.py --serial "$PORT" --seconds "$SECS" --out EEG_CLM/eeg_recording.txt >/dev/null 2>&1; then
    # ② 풀체인 EEG→A⇄G→CLM→KOSMOS
    "$HEXA" run EEG_CLM/eeg_clm_kosmos.hexa >/dev/null 2>&1
    # ③ 생성기록 누적 (사이클별)
    if [ -f EEG_CLM/kosmos/wake_2004_WAKE.kosmos ]; then
      cp EEG_CLM/kosmos/wake_2004_WAKE.kosmos "$OUT/cycle_$(printf '%04d' $i).kosmos"
    fi
    echo "[daemon] cycle $i done $(date +%H:%M:%S) → $OUT/cycle_$(printf '%04d' $i).kosmos"
  else
    echo "[daemon] cycle $i CAPTURE FAILED (센서/포트 확인) — skip $(date +%H:%M:%S)"
  fi
  i=$((i+1))
  sleep 3
done
echo "[daemon] stopped after $i cycles $(date)"
