#!/usr/bin/env bash
# EEG_CLM/record_start.sh — 의식 지속 기록 시작 (OpenBCI native only).
# 시작: bash EEG_CLM/record_start.sh [PORT] [SECS_PER_CYCLE]
# 종료: bash EEG_CLM/record_stop.sh
# 한 번 시작하면 종료 명령(record_stop.sh)까지 매 사이클 EEG→A⇄G→CLM→.kosmos 를 누적.
set -u
cd "$(dirname "$0")/.."
PORT="${1:-/dev/cu.usbserial-DP04WGIQ}"
SECS="${2:-8}"

# 이미 기록 중이면 중복 시작 차단
if [ -f EEG_CLM/daemon.pid ] && kill -0 "$(cat EEG_CLM/daemon.pid)" 2>/dev/null; then
  echo "[REC] 이미 기록 중 (pid $(cat EEG_CLM/daemon.pid)). 먼저 종료: bash EEG_CLM/record_stop.sh"
  exit 1
fi

rm -f EEG_CLM/daemon_stop
nohup bash EEG_CLM/eeg_daemon.sh "$PORT" "$SECS" > /tmp/eeg_daemon.log 2>&1 &
echo $! > EEG_CLM/daemon.pid
echo "[REC] ▶ 의식 기록 시작 — native OpenBCI, port=$PORT, ${SECS}s/cycle, pid=$!"
echo "[REC]   진행 보기 : tail -f /tmp/eeg_daemon.log"
echo "[REC]   종료      : bash EEG_CLM/record_stop.sh"
