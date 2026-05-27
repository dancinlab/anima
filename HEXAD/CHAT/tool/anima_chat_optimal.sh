#!/usr/bin/env bash
# anima_chat_optimal — 최선 세팅 launcher (cycle 2026-05-12)
#
# 기본값 (V5.8 std_greedy + V4-lite 결과 기준):
#   ckpt:    Phase 1A.1 color/cosmology boost (V5.8 std_greedy 4/5, 자연 한국어)  ⭐
#   mode:    M4_force_include (5/5 PASS @ V5.8 4-mode benchmark)
#   max-new: 80 tokens
#   multi-turn state: enabled (anima_chat.py 내장)
#
# 사용:
#   ./tool/anima_chat_optimal.sh                       # REPL
#   ./tool/anima_chat_optimal.sh "안녕! 너는 누구야?"  # one-shot
#   ./tool/anima_chat_optimal.sh --mode greedy "..."   # mode override
#   ./tool/anima_chat_optimal.sh --smoke               # 5-prompt smoke
#
# 권장 alias (~/.zshrc 또는 ~/.bashrc):
#   alias anima-chat='~/core/anima/tool/anima_chat_optimal.sh'

set -euo pipefail
ANIMA_ROOT="${ANIMA_ROOT:-$HOME/core/anima}"
CHAT_PY="$ANIMA_ROOT/anima_chat.py"

if [[ ! -f "$CHAT_PY" ]]; then
    echo "anima_chat.py not found at: $CHAT_PY" >&2
    exit 1
fi

if [[ $# -eq 0 ]]; then
    exec /usr/bin/python3 "$CHAT_PY"
fi

if [[ "$1" != --* && "$1" != -* ]]; then
    exec /usr/bin/python3 "$CHAT_PY" --prompt "$@"
else
    exec /usr/bin/python3 "$CHAT_PY" "$@"
fi
