#!/usr/bin/env bash
# build_all.sh — one-shot GB-balanced default-lane corpus build.
#
# Tier -> real source (KOSMOS ladder preserved at scale):
#   t0  baseline  = wiki 8-band breadth (5-lang, CC-BY-SA)
#   t100 cosmic   = wiki science-filtered (5-lang, CC-BY-SA)
#   t77 art       = Gutenberg literature/poetry (PD; en/fr/de/es, ko gap)
#   t91 conscious = Gutenberg philosophy/meditation (PD; en/fr/de/es, ko gap)
#   t52 social    = authored persona/SNS CAPPED small (5-lang)
#   shaping       = authored dialogue-act/emotion/code-switch/genre + carving-seed def
#
# DISK SAFETY: each fetch is byte-capped (--mb-per-lang); _src/ holds intermediates.
# Set MB_T0 / MB_T100 / MB_ART / MB_CON / SHAPING_MB / PERSONA_MB to retune the ladder.
#
# Usage:  HF_TOKEN=$(secret get hf.token) bash serving/gb_balanced/build_all.sh
set -euo pipefail
cd "$(dirname "$0")/../.."   # repo root

SRC=serving/corpus/_src
OUT=serving/corpus/default_lane_gb_balanced.txt
mkdir -p "$SRC"

# parquet shards are downloaded to a local cache (anti read-amplification) then
# deleted at the end (DISK SAFETY — transient ~1-2GB). Override the caps to retune.
export WIKI_SHARD_CACHE=${WIKI_SHARD_CACHE:-/tmp/anima_wiki_shards}
export GUT_SHARD_CACHE=${GUT_SHARD_CACHE:-/tmp/anima_gut_shards}
export WIKI_MAX_SHARDS=${WIKI_MAX_SHARDS:-2}
export GUT_MAX_SHARDS=${GUT_MAX_SHARDS:-3}
cleanup() { rm -rf "$WIKI_SHARD_CACHE" "$GUT_SHARD_CACHE" 2>/dev/null || true; }
trap cleanup EXIT

# ladder knobs (MB per language for fetched tiers; total for authored slices).
# Bulk tiers read HF parquet via duckdb httpfs (GB-scale, no REST 429).
MB_T0=${MB_T0:-90}         # wiki baseline floor  (5 langs -> ~450MB)
MB_T100=${MB_T100:-18}     # wiki science         (5 langs -> ~90MB)
MB_ART=${MB_ART:-30}       # Gutenberg art        (en/fr/de/es; ko=0 -> ~120MB)
MB_CON=${MB_CON:-18}       # Gutenberg conscious  (en/fr/de/es; ko=0 -> ~72MB)
SHAPING_MB=${SHAPING_MB:-24}   # authored shaping total  (capped)
PERSONA_MB=${PERSONA_MB:-40}   # authored persona/SNS total (tier 52, capped)

echo "== t0 wiki baseline =="
python3 serving/gb_balanced/fetch_wiki_tiers.py --tier 0   --out "$SRC/wiki_t0.txt"   --mb-per-lang "$MB_T0"
echo "== t100 wiki science =="
python3 serving/gb_balanced/fetch_wiki_tiers.py --tier 100 --out "$SRC/wiki_t100.txt" --mb-per-lang "$MB_T100"
echo "== t77 gutenberg art =="
python3 serving/gb_balanced/fetch_gutenberg_tiers.py --tier art           --out "$SRC/gut_art.txt" --mb-per-lang "$MB_ART"
echo "== t91 gutenberg consciousness =="
python3 serving/gb_balanced/fetch_gutenberg_tiers.py --tier consciousness --out "$SRC/gut_con.txt" --mb-per-lang "$MB_CON"

echo "== authored register-shaping (carving-seed def + dialogue-act + emotion + code-switch + genre) =="
python3 serving/corpus_enrichment_5lang_gen.py --target-mb "$SHAPING_MB" \
    --anchors HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31 --out "$SRC/shaping.txt"
echo "== authored persona/SNS (tier 52 social/daily, CAPPED) =="
python3 serving/persona_sns_corpus_5lang_gen.py --target-mb "$PERSONA_MB" --out "$SRC/persona.txt"

echo "== balance + merge + account =="
python3 serving/gb_balanced/balance_merge.py \
    --src-dir "$SRC" --shaping "$SRC/shaping.txt" --persona "$SRC/persona.txt" \
    --persona-cap-mb "$PERSONA_MB" --shaping-cap-mb "$SHAPING_MB" \
    --out "$OUT" --report "$SRC/gb_balanced_report.json"

echo "== DONE: $OUT =="
ls -la "$OUT"
df -h . | tail -1
