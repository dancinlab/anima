#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════
#  run.sh — CLM BRIDGE distill run 글루 (P0 §11.4/§11.6 · F-CLM-BRIDGE-XFER)
#
#  MITOSIS-ARRAY 의 SECONDARY arm(BRIDGE). teacher(유효 측정 scale) escape 측정
#  → KD distill → chip-fit student → routing-diversity transfer Δ 검증.
#  페이로드 = CLM/distill/run_bridge_transfer.py (teacher train + KD + z 측정).
#
#  사용:
#    ./run.sh smoke               # $0 local CPU toy distill (plumbing 검증)
#    ./run.sh fire   [HOST]       # GPU pod teacher distill fire (longer steps) — cost-bearing
#
#  ⚠ GPU pod rent 는 cost-bearing fire — fire 서브커맨드는 명시 실행시에만.
#  추론 AKIDA-int4-only 불변 — 이 스크립트는 GPU/CPU distill pretrain 만 다룬다.
# ════════════════════════════════════════════════════════════════════════════
set -euo pipefail
cd "$(dirname "$0")"

CMD="${1:-smoke}"

case "$CMD" in
  smoke)
    # d16 governance — FREE local toy distill BEFORE any cost-bearing launch
    # (teacher train + KD distill + transfer Δ z, $0 CPU). toy != scale (H_666).
    STEPS="${2:-60}"
    echo "[smoke] python3 run_bridge_transfer.py --steps $STEPS"
    exec python3 run_bridge_transfer.py --steps "$STEPS"
    ;;

  fire)
    # GPU pod fire: valid-scale teacher (E=32 d=128) train -> KD distill ->
    # chip-fit student (E=8 d=64) -> transfer Δ. The real F-CLM-BRIDGE-XFER run.
    # WARNING cost-bearing. d16 dry-run on the pool FIRST:
    #   pool on <HOST> 'cd ~/core/anima/CLM/distill && python3 run_bridge_transfer.py --steps 5'
    HOST="${2:-ubu-1}"
    LOG="bridge.transfer.fire.log"
    echo "[fire] BRIDGE teacher->student distill -> $HOST (background, via hexa cloud nohup)"
    hexa cloud nohup "$HOST" "$LOG" -- \
      env BRIDGE_TXT=bridge_transfer_fire.txt BRIDGE_JSON=bridge_transfer_fire.json \
      python3 run_bridge_transfer.py --fire
    echo "poll/tail: hexa cloud poll $HOST <pid> / hexa cloud tail $HOST $LOG"
    ;;

  *)
    echo "usage: $0 {smoke|fire} [args]" >&2
    exit 2
    ;;
esac
