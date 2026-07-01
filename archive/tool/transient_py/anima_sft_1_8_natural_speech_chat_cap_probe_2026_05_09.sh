#!/usr/bin/env bash
# anima_sft_1_8_natural_speech_chat_cap_probe_2026_05_09.sh
#
# 1:1 자연발화 chat-cap C2 measurement — sft-1-8 (PUBLIC promoted) one-shot
# probe sweep. mandate-2 strict (raw output preserved verbatim, no
# wrapping). Each prompt invokes anima chat clm_v4 module --prompt one-shot.
#
# OUTPUT: state/anima_sft_1_8_natural_speech_chat_cap_2026_05_09/transcript.txt
# (raw substrate response per prompt — mandate-1)
#
# COST: 0 (Mac local, model already merge-cached).
# CYCLE: 2026-05-09
set -uo pipefail

ANIMA="${ANIMA:-/Users/ghost/core/anima}"
HEXA="/Users/ghost/.hx/packages/hexa/hexa.real"
MOD="$ANIMA/tool/anima_cli/chat/clm_v4/clm_v4.hexa"
REPO="dancinlab/clm-v4-sft-1-8-stage1"
STATE_DIR="$ANIMA/state/anima_sft_1_8_natural_speech_chat_cap_2026_05_09"
PROMPTS="$STATE_DIR/prompts.txt"
OUT="$STATE_DIR/transcript.txt"

mkdir -p "$STATE_DIR"
: > "$OUT"

i=0
while IFS= read -r line; do
    [ -z "$line" ] && continue
    i=$((i+1))
    printf '\n=== prompt %02d: %s ===\n' "$i" "$line" >> "$OUT"
    # raw passthrough — mandate-2 wrapping=0
    # </dev/null prevents inner hexa from consuming the outer while-loop's stdin
    # (which would terminate iteration after the first prompt)
    timeout 120 "$HEXA" run "$MOD" --repo "$REPO" --prompt "$line" </dev/null >> "$OUT" 2>&1
    rc=$?
    printf '\n--- rc=%d ---\n' "$rc" >> "$OUT"
    # short pause to avoid mount thrash (each invocation re-loads merged model
    # from ~/.cache/anima/clm_v4_merged/ which is fast but non-zero)
    sleep 1
done < "$PROMPTS"

printf '\n=== sweep complete: %d prompts ===\n' "$i" >> "$OUT"
echo "OK: transcript at $OUT"
