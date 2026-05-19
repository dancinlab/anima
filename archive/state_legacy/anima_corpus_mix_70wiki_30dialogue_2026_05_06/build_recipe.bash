#!/usr/bin/env bash
# anima_corpus_mix_70wiki_30dialogue build recipe — PATH-B-1 concat
# Date: 2026-05-06
# Spec: docs/anima_clm_3_original_byte_level_redesign_spec_2026_05_05.md §3.3 (lines 142, 183, 246-250)
# Reproducibility: deterministic (no random shuffle); idempotent on identical sources
#
# Sources (mac local):
#   wiki:     /Users/ghost/core/anima/ready/anima/data/corpus_v6_wiki.txt
#   dialogue: /Users/ghost/core/anima/ready/anima/data/corpus_v8_dialogue.txt
#
# Target ratio: 70% wiki / 30% dialogue (line-anchor)
# Anchor: ALL of v6_wiki (2,141,063 lines) → 70%
# Derived: head -n 917,598 of v8_dialogue → 30%
#
# Output sha256 (expected): 2d15ca7d277aaaef95c7dbc9eb810ec38f0510e0578269810aa4eb879f51e0e8

set -euo pipefail

WIKI_SRC="/Users/ghost/core/anima/ready/anima/data/corpus_v6_wiki.txt"
DIALOGUE_SRC="/Users/ghost/core/anima/ready/anima/data/corpus_v8_dialogue.txt"
OUT_DIR="/Users/ghost/core/anima/state/anima_corpus_mix_70wiki_30dialogue_2026_05_06"
OUT="${OUT_DIR}/corpus_mix.txt"

WIKI_LINES=$(wc -l < "${WIKI_SRC}" | tr -d ' ')
DIALOGUE_LINES=$(( WIKI_LINES * 30 / 70 ))

echo "[recipe] wiki_lines=${WIKI_LINES}"
echo "[recipe] dialogue_lines=${DIALOGUE_LINES}"
echo "[recipe] total=$(( WIKI_LINES + DIALOGUE_LINES ))"

mkdir -p "${OUT_DIR}"
cat "${WIKI_SRC}" > "${OUT}"
head -n ${DIALOGUE_LINES} "${DIALOGUE_SRC}" >> "${OUT}"

echo "[recipe] build done"
wc -l -c "${OUT}"
shasum -a 256 "${OUT}"
