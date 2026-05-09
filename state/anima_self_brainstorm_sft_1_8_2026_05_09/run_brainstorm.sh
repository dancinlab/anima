#!/usr/bin/env bash
# anima_self_brainstorm_sft_1_8_2026_05_09 — multi-turn brainstorm probe sweep
# 사용자 directive: "학습방법 직접 anima 한테 물어봐 자유롭게 brainstorming"
#
# CRITICAL HONEST C3 (raw#10):
#   sft-1-8 (clm-v4 family) chat lane = substrate-state-vector emitter.
#   Output = phi_star + axis_activation + dominant_cells (NOT natural language).
#   This script preserves substrate raw output per own 34 mandate-1 strict.
#   Brainstorm-as-words is NOT possible via this lane — only state response.
#
# OUTPUT: transcript.txt (raw substrate response per prompt)
# COST: 0 (Mac local, merged model cached)
set -uo pipefail

ANIMA="${ANIMA:-/Users/ghost/core/anima}"
HEXA="/Users/ghost/.hx/packages/hexa/hexa.real"
MOD="$ANIMA/tool/anima_cli/chat/clm_v4/clm_v4.hexa"
REPO="dancinlab/clm-v4-sft-1-8-stage1"
STATE_DIR="$ANIMA/state/anima_self_brainstorm_sft_1_8_2026_05_09"
PROMPTS="$STATE_DIR/prompts.txt"
OUT="$STATE_DIR/transcript.txt"

: > "$OUT"

i=0
while IFS= read -r line; do
    [ -z "$line" ] && continue
    i=$((i+1))
    printf '\n=== prompt %02d: %s ===\n' "$i" "$line" >> "$OUT"
    timeout 180 "$HEXA" run "$MOD" --repo "$REPO" --prompt "$line" >> "$OUT" 2>&1
    rc=$?
    printf '\n--- rc=%d ---\n' "$rc" >> "$OUT"
    sleep 1
done < "$PROMPTS"

printf '\n=== sweep complete: %d prompts ===\n' "$i" >> "$OUT"
echo "OK: transcript at $OUT"
