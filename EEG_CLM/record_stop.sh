#!/usr/bin/env bash
# EEG_CLM/record_stop.sh — 의식 지속 기록 종료 + 세션 봉인.
# 종료 신호를 주고 데몬이 현재 사이클을 마치길 기다린 뒤, 누적 사이클 수 + 추세를 보고.
set -u
cd "$(dirname "$0")/.."

touch EEG_CLM/daemon_stop
echo "[REC] ■ 종료 신호 — 데몬이 현재 사이클 마치는 중..."
for _ in $(seq 1 30); do
  if [ -f EEG_CLM/daemon.pid ] && kill -0 "$(cat EEG_CLM/daemon.pid)" 2>/dev/null; then
    sleep 1
  else
    break
  fi
done
rm -f EEG_CLM/daemon.pid

NSEQ=$(wc -l < EEG_CLM/consciousness.seq 2>/dev/null | tr -d ' ')
echo "[REC] 세션 종료 — consciousness.seq 누적 ${NSEQ:-0}줄 (하나의 CLM 코퍼스가 자람)"

# GitHub + HF(PRIVATE) 자동 보관 — 같은 파일 갱신
echo "[REC] GitHub + HF 보관 중..."
bash EEG_CLM/archive_push.sh

[ "${NSEQ:-0}" -gt 0 ] && echo "[REC] 추세 분석: bash EEG_CLM/analyze_daemon.sh"
