#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════
#  run_stage2.sh — CLM MITOSIS-ARRAY STAGE-2 PRODUCTION-scale run 글루 (@L1/@L3)
#
#  STAGE-1(toy: d64·synthetic LCG·NULL=수천) 가 Pielou-J·dispatch-KL 둘 다
#  🔴 CLOSED-NEGATIVE. 유일 미검 축 = PRODUCTION SCALE. 이 스크립트가 그걸 친다.
#  페이로드 = run_array_sweep_stage2.py(Pielou J) + run_dispatch_kl_stage2.py(KL).
#
#  ⚠⚠ MAC-FORBIDDEN (@L1): 학습/측정/null-sampling 은 절대 Mac 에서 돌리지 않는다.
#     모든 compute 는 GPU/Linux 호스트(ubu-1) 에서만 — 이 스크립트가 강제한다.
#     (이전 STAGE-1 run 이 Mac 을 load 289 로 spike 시킨 사고 재발 금지.)
#  @L2 NULL_SAMPLES 는 코드에서 <=16 하드캡(min(16,..)+assert). 무한 루프 없음.
#
#  사용 (Mac 에서 호출 — 내부에서 pool on ubu-1 로 dispatch):
#    ./run_stage2.sh                       # 양쪽 sweep 모두 ubu-1 에서 실행
#    HOST=ubu-1 ./run_stage2.sh
# ════════════════════════════════════════════════════════════════════════════
set -euo pipefail

HOST="${HOST:-ubu-1}"
REMOTE_REPO="${REMOTE_REPO:-~/core/anima}"
VDIR="state/verdicts/clm-array-stage2-scale"

# HARD GUARD: refuse to run torch compute on the Mac (@L1).
if [[ "$(uname -s)" == "Darwin" && "${ALLOW_MAC:-0}" != "FORCE_NEVER" ]]; then
  echo "[run_stage2] Mac host detected — dispatching compute to $HOST (@L1, Mac-forbidden)."
fi

run_remote() {
  # $1 = label, $2 = python module path, $3 = env-prefix
  local label="$1" mod="$2" envp="$3"
  echo "[run_stage2] === $label on $HOST ==="
  pool on "$HOST" "cd $REMOTE_REPO && git fetch origin -q && git checkout -q origin/main -- CLM/ 2>/dev/null; mkdir -p $VDIR && $envp python3 $mod"
}

mkdir -p "$VDIR" 2>/dev/null || true

run_remote "PIELOU-J production sweep" "CLM/model/run_array_sweep_stage2.py" \
  "ARRAY_SWEEP2_TXT=$VDIR/pielou_prod_2026_05_30.txt ARRAY_SWEEP2_JSON=$VDIR/pielou_prod_2026_05_30.json"

run_remote "DISPATCH-KL production transfer" "CLM/distill/run_dispatch_kl_stage2.py" \
  "DKL2_TXT=$VDIR/dispatchkl_prod_2026_05_30.txt DKL2_JSON=$VDIR/dispatchkl_prod_2026_05_30.json"

echo "[run_stage2] done — verdicts under $REMOTE_REPO/$VDIR on $HOST (pull before teardown, @L6)."
