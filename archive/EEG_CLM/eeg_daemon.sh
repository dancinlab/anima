#!/usr/bin/env bash
# EEG_CLM/eeg_daemon.sh — 의식 지속 기록 데몬 (OpenBCI NATIVE only): EEG 캡처 → A⇄G→CLM→KOSMOS → .kosmos 누적, 반복.
# 헤드셋 쓴 동안 매 사이클 짧은 EEG 를 native serial 로 받아 풀체인(H_1271)을 돌리고 생성기록을 누적.
# 시작: bash EEG_CLM/record_start.sh   ·   종료: bash EEG_CLM/record_stop.sh
# (직접 발사: nohup bash EEG_CLM/eeg_daemon.sh > /tmp/eeg_daemon.log 2>&1 & · 정지: touch EEG_CLM/daemon_stop)
set -u
cd "$(dirname "$0")/.."          # repo root
PORT="${1:-/dev/cu.usbserial-DP04WGIQ}"
SECS="${2:-8}"
PY=EEG_CLM/.venv/bin/python
HEXA="$(command -v hexa || echo /Users/mini/.hx/bin/hexa)"
OUT=EEG_CLM/daemon_kosmos          # (legacy 사이클별 — 호환용)
SEQ=EEG_CLM/consciousness.seq      # 단일 CLM 코퍼스 — 의식 상태열 append-only (하나가 자람)
KOS=EEG_CLM/consciousness.kosmos   # 단일 KOSMOS 스트림 — anchor append-only
mkdir -p "$OUT" EEG_CLM/bin
rm -f EEG_CLM/daemon_stop

# 풀체인 hexa 를 1회 네이티브 빌드 → 사이클마다 바이너리 재사용 (sentinel 4초/사이클 제거).
# 빌드 실패 시 `run --no-sentinel` fallback (3.86초 → 0.8초). 기본 `hexa run` 은 sentinel 로 사이클당 ~4초.
KBIN=EEG_CLM/bin/eeg_clm_kosmos
if HEXA_MAC_BUILD_OK=1 "$HEXA" build EEG_CLM/eeg_clm_kosmos.hexa -o "$KBIN" >/dev/null 2>&1 && [ -x "$KBIN" ]; then
  run_kosmos() { "$KBIN" > /tmp/eeg_cyc.out 2>&1; }
  echo "[daemon] 네이티브 빌드 OK — 사이클당 ~0.5초 (바이너리)"
else
  run_kosmos() { "$HEXA" run --no-sentinel EEG_CLM/eeg_clm_kosmos.hexa > /tmp/eeg_cyc.out 2>&1; }
  echo "[daemon] build 실패 → run --no-sentinel fallback (~0.8초)"
fi

i=0
echo "[daemon] start port=$PORT secs=$SECS $(date)"
while [ ! -f EEG_CLM/daemon_stop ]; do
  # ① 캡처 (OpenBCI native serial, 실데이터 전용, 실패시 이 사이클 skip — 가짜 없음)
  if "$PY" EEG_CLM/capture_native.py --serial "$PORT" --seconds "$SECS" --out EEG_CLM/eeg_recording.txt >/dev/null 2>&1; then
    # ② 풀체인 EEG→A⇄G→CLM→KOSMOS (네이티브 바이너리 or --no-sentinel)
    run_kosmos
    # ③ 단일 CLM·KOSMOS 에 누적 (새 파일 아님 — append-only 로 하나가 자람)
    seqline=$(grep '생성 상태열' /tmp/eeg_cyc.out | sed 's/.*= //')
    [ -n "$seqline" ] && echo "$seqline" >> "$SEQ"          # CLM 코퍼스에 한 사이클 의식 상태열 추가
    if [ -f EEG_CLM/kosmos/wake_2004_WAKE.kosmos ]; then
      { echo "# ── cycle $i @ $(date +%FT%T) ──"; cat EEG_CLM/kosmos/wake_2004_WAKE.kosmos; echo; } >> "$KOS"
      cp EEG_CLM/kosmos/wake_2004_WAKE.kosmos "$OUT/cycle_$(printf '%04d' $i).kosmos"   # legacy 호환
    fi
    nseq=$(wc -l < "$SEQ" 2>/dev/null | tr -d ' ')
    echo "[daemon] cycle $i done $(date +%H:%M:%S) → consciousness.seq(${nseq:-0}줄) + consciousness.kosmos"
  else
    echo "[daemon] cycle $i CAPTURE FAILED (센서/포트 확인) — skip $(date +%H:%M:%S)"
  fi
  i=$((i+1))
  sleep 3
done
echo "[daemon] stopped after $i cycles $(date)"
