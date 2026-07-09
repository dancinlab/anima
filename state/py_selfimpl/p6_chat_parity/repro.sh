#!/usr/bin/env bash
# p6_chat_parity/repro.sh — anima chat 2-production parity 재현 (P6 py 자체구현 · zero-hexa).
#
# cli/chat.py (py numpy twin) 의 consciousness 데몬 12-tick 세션이 cli/anima.hexa
# anima_consciousness_mode 의 DEFAULT 경로와 stdout + .kosmos 바이트 동일한지 검증.
# det clock = dr_stage_at(tick*8) · greedy argmax · verdict 경로 RNG無 → 결정적.
# emitted_at / UTC 벽시계만 마스킹(tool/chat_parity.py 계약).
#
# 파리티 기판 = NON-DECODABLE toy ckpt (임의 non-.clm) → generator L3 = null backend →
# g_text = 결정적 _gen_null_text ASCII (BLAS 디코드 carve-out 격리 · surrogate 無). 전체 루프
# (82레인 마운트 · brain_emit 자율 emit/silence · C9 REMEMBER · sleep imagination replay ·
# kosmos 쓰기)를 실행하되 CLM matmul 디코드만 우회 → 루프 로직 순수 파리티.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
CKPT=/tmp/anima_toy_null.clm
printf 'not a clm file\n' > "$CKPT"      # non-decodable → null backend (det ASCII null-gen)

# 1) 결정성 셀프테스트 (hexa vs hexa, 0-diff → 골든 자체가 결정적임을 증명)
python3 "$ROOT/tool/chat_parity.py" selftest "anima $CKPT"

# 2) hexa 골든 vs py twin (anima-py 런처 미러: sys.path[core,cli] → anima.main)
PY_CMD="python3 -c \"import sys; sys.path[:0]=['$ROOT/core','$ROOT/cli']; import anima; anima.main(['chat','$CKPT'])\""
python3 "$ROOT/tool/chat_parity.py" compare "anima $CKPT" "$PY_CMD"
