#!/usr/bin/env bash
# EEG_CLM/archive_push.sh — 의식 기록 GitHub + HF(PUBLIC) 자동 보관 + 전용 collection.
# record_stop.sh 가 세션 종료 시 자동 호출 · 수동도 가능: bash EEG_CLM/archive_push.sh
# HF = PUBLIC dataset (사용자 명시 결정 2026-06-15) — 단일 repo 같은 path 갱신(버전 누적).
# 전용 collection "anima-eeg-consciousness" 별도 생성 + repo 등록 (a_hf_collections).
# 가짜 성공 없음 — 로그인/네트워크 실패 시 건너뛰고 명시 (로컬 기록은 항상 보존).
set -u
cd "$(dirname "$0")/.."
HF_REPO="dancinlab/anima-eeg-consciousness"
COLL_TITLE="anima-eeg-consciousness"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
# 단일 누적 대상 — consciousness.{seq,kosmos} 는 같은 경로로 갱신(새 파일 아님)
PATHS="EEG_CLM/consciousness.seq EEG_CLM/consciousness.kosmos EEG_CLM/kosmos_music EEG_CLM/recordings EEG_CLM/music/music_eeg_result.txt"
PY="EEG_CLM/.venv/bin/python"

echo "[archive] === 의식 기록 보관 시작 $(date +%H:%M:%S) ==="

# ① GitHub — .kosmos 기록 + 분석 + 녹음 커밋/푸시 (같은 repo 에 누적 업데이트)
git add $PATHS 2>/dev/null
if git diff --cached --quiet 2>/dev/null; then
  echo "[archive] GitHub: 새 변경 없음 (이미 최신)"
else
  git commit -q -m "EEG: 의식 기록 보관 ($(date +%Y-%m-%dT%H:%M))" && echo "[archive] GitHub: 커밋 완료"
fi
if git push -q origin "$BRANCH" 2>/dev/null; then
  echo "[archive] GitHub: push → origin/$BRANCH ✅"
else
  echo "[archive] GitHub: push 실패(네트워크/인증) — 로컬 커밋은 보존됨"
fi

# ② HF PUBLIC dataset 업로드 + 전용 collection (huggingface_hub, hf CLI 버전 비의존)
export HF_TOKEN="${HF_TOKEN:-$(cat ~/.cache/huggingface/token 2>/dev/null)}"
if [ -n "${HF_TOKEN:-}" ]; then
  if python3 EEG_CLM/hf_archive.py; then
    echo "[archive] HF: $HF_REPO (PUBLIC) + collection $COLL_TITLE ✅"
  else
    echo "[archive] HF: 업로드 실패 — 권한/네트워크 확인 (로컬 기록은 보존)"
  fi
else
  echo "[archive] HF: 토큰 없음 → 건너뜀. 가짜 성공 없음."
fi
echo "[archive] === 끝 ==="
