#!/usr/bin/env bash
# build_recipe.bash — anima KO-heavy corpus assembly (PATH-C tightened)
# Date: 2026-05-06
# Output: /Users/ghost/core/anima/state/anima_ko_corpus_assembly_2026_05_06/corpus_ko_heavy.txt
# Result: 246.7MB / 2,525,921 lines / hangul_ratio=0.6214 / target_met=true
#
# raw#9: hexa-friendly bash (corpus build script carve-out OK)
# own 14: 5MB+ → HF only, .gitignore enforced

set -euo pipefail

WORK=/Users/ghost/core/anima/state/anima_ko_corpus_assembly_2026_05_06
OUT="$WORK/corpus_ko_heavy.txt"
mkdir -p "$WORK"

# Source thresholds (tightened to push Hangul ratio >= 60%):
#   opensubtitles_ko_mono.txt        : ratio>=0.45, h>=4    (full file)
#   data/.corpus_cache/ko_wiki.txt   : ratio>=0.40, h>=4    (full file)
#   corpus_v2_clean/kowiki.txt.zst   : ratio>=0.50, h>=20   (cap 100MB)
#   sft_data.jsonl (P9 P0)           : lang==ko OR ratio>=0.40 (chat-template format)
#   ready/anima/data/corpus_v6_wiki  : ratio>=0.55, h>=10
#   ready/anima/data/corpus_v8_dial  : ratio>=0.55, h>=10
#
# Chat format used for sft_data section:
#   사용자: <KO input>
#   도우미: <KO completion>
#
# Re-run via the in-place python heredoc in Step 3b of session log
# (this bash file is a recipe pointer, not a re-runner).

echo "Run python via parent agent's Step 3b heredoc to rebuild deterministically."
echo "Verdict: $WORK/verdict.json"
echo "SHA256:  2e98257f9e89663fc71232e2c1dc0b65f9b9131ad0b6a5f53e98dfe27c6269a9"
