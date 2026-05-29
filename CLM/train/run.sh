#!/usr/bin/env bash
# ════════════════════════════════════════════════════════════════════════════
#  run.sh — CLM P2 QAT 학습 run 글루 (dojo 패턴 적응 · 페이로드 = custom QAT)
#
#  dojo run.sh 의 d16 dry-run + hexa-cloud dispatch 패턴을 재사용하되,
#  페이로드는 CLM 전용 train_clm.py (custom conv-MoE byte QAT) 다.
#  HF train.py(AutoModel/tokenizer/wikitext)는 버렸다.
#
#  사용:
#    ./run.sh dryrun                # $0 local CPU dry-run smoke (forward+QAT+backward 1-step)
#    ./run.sh local  [ARM] [RUNG] [STEPS]   # $0 local toy 학습 (intuition only)
#    ./run.sh fire   [HOST]         # GPU pod full-fire (3-arm × ladder) — cost-bearing, 다음 step
#
#  ⚠ GPU pod rent 는 cost-bearing fire — fire 서브커맨드는 명시 실행시에만.
#  추론 AKIDA-int4-only 불변 — 이 스크립트는 GPU/CPU QAT pretrain 만 다룬다.
# ════════════════════════════════════════════════════════════════════════════
set -euo pipefail
cd "$(dirname "$0")"

CMD="${1:-dryrun}"

case "$CMD" in
  dryrun)
    # d16 governance — FREE local dry-run BEFORE any cost-bearing remote launch
    # (catches import/path errors without renting GPU time). 1-step
    # forward+QAT-loss+backward + step-rate measure (d5 honest re-measure).
    ARM="${2:-AB}"; RUNG="${3:-tiny}"
    echo "[d16 dry-run] python3 train_clm.py --dry-run --arm $ARM --rung $RUNG"
    exec python3 train_clm.py --dry-run --arm "$ARM" --rung "$RUNG"
    ;;

  local)
    # $0 local toy QAT train (intuition only — toy != scale, H_666/H_847 Q4).
    ARM="${2:-AB}"; RUNG="${3:-tiny}"; STEPS="${4:-200}"
    echo "[local] python3 train_clm.py --arm $ARM --rung $RUNG --steps $STEPS"
    exec python3 train_clm.py --arm "$ARM" --rung "$RUNG" --steps "$STEPS" \
      --json-out "clm_p2_${ARM}_${RUNG}.json"
    ;;

  fire)
    # GPU pod full-fire: 3-arm (A/B/AB) × scale-ladder (tiny/small) — the real
    # F-CLM-MONO / F-CLM-SCALE judgment matrix (P0 Q4, wall-first / no-cap).
    # WARNING cost-bearing — this dispatches multiple background pods. Run the
    # d16 dry-run on the pool FIRST (per a_fire_autonomous + d16):
    #   pool on ubu-1 'cd ~/core/anima/CLM/train && python3 train_clm.py --dry-run'
    HOST="${2:-ubu-1}"
    echo "[fire] 3-arm x ladder full-fire -> $HOST (background, via hexa cloud nohup)"
    for ARM in A B AB; do
      for RUNG in tiny small; do
        LOG="train.clm-p2.${ARM}.${RUNG}.log"
        echo "  dispatch ARM=$ARM RUNG=$RUNG -> $LOG"
        hexa cloud nohup "$HOST" "$LOG" -- \
          python3 train_clm.py --arm "$ARM" --rung "$RUNG" --steps 2000 \
            --json-out "clm_p2_${ARM}_${RUNG}.json"
      done
    done
    echo "poll/tail: hexa cloud poll $HOST <pid> / hexa cloud tail $HOST <log>"
    ;;

  *)
    echo "usage: $0 {dryrun|local|fire} [args]" >&2
    exit 2
    ;;
esac
