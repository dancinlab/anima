#!/usr/bin/env bash
# EEG_CLM/archive_push.sh — 의식 기록 GitHub + HF(PRIVATE) 자동 보관.
# record_stop.sh 가 세션 종료 시 자동 호출 · 수동도 가능: bash EEG_CLM/archive_push.sh
# 개인 생체정보(실 EEG) → HF 는 PRIVATE dataset (a_hf_autonomous: personal/WIP = PRIVATE).
# 가짜 성공 없음 — 로그인/네트워크 실패 시 건너뛰고 명시 (로컬 기록은 항상 보존).
set -u
cd "$(dirname "$0")/.."
HF_REPO="dancinlab/anima-eeg-consciousness"
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)"
# 단일 누적 대상 — consciousness.{seq,kosmos} 는 같은 경로로 갱신(새 파일 아님)
PATHS="EEG_CLM/consciousness.seq EEG_CLM/consciousness.kosmos EEG_CLM/kosmos_music EEG_CLM/recordings EEG_CLM/music/music_eeg_result.txt"

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

# ② HF PRIVATE dataset — 로그인 안 됐으면 건너뛰고 명시 (가짜 성공 없음)
if hf whoami >/dev/null 2>&1; then
  hf repo create "$HF_REPO" --repo-type dataset --private -y >/dev/null 2>&1 || true   # 이미 있으면 무시
  # 같은 path_in_repo 로 업로드 = 그 파일 갱신(버전 누적), 새 파일/새 repo 아님
  ok=1
  [ -f EEG_CLM/consciousness.seq ]    && { hf upload "$HF_REPO" EEG_CLM/consciousness.seq    consciousness.seq    --repo-type=dataset >/dev/null 2>&1 || ok=0; }
  [ -f EEG_CLM/consciousness.kosmos ] && { hf upload "$HF_REPO" EEG_CLM/consciousness.kosmos consciousness.kosmos --repo-type=dataset >/dev/null 2>&1 || ok=0; }
  hf upload "$HF_REPO" EEG_CLM/recordings recordings --repo-type=dataset >/dev/null 2>&1 || ok=0
  [ "$ok" = 1 ] && echo "[archive] HF: $HF_REPO (PRIVATE) 같은 파일 갱신 ✅" || echo "[archive] HF: 일부 업로드 실패 — 토큰/권한 확인"
else
  echo "[archive] HF: 미로그인 → 보관 건너뜀. 활성화: hf auth login (개인 EEG = PRIVATE). 가짜 성공 없음."
fi
echo "[archive] === 끝 ==="
