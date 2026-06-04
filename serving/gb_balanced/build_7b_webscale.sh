#!/usr/bin/env bash
# build_7b_webscale.sh — one-shot 7B-scale web-extended default-lane corpus build.
#
# EXTENDS the gb_balanced ladder (serving/gb_balanced/build_all.sh) with a web-scale
# ODC-BY BULK tier (user decision 2026-06-05 — web-scale SANCTIONED for 7B). The
# curated tiers (wiki / Gutenberg / persona / shaping) are UNCHANGED and re-run from
# the SAME generators; only the new `web` tier is added and it becomes the majority.
#
#   tier web  = FineWeb-2 (fr/de/ko) + mC4/c4 (en/es), ODC-BY   [NEW, MAJORITY]
#   t0   wiki baseline   = wiki 5-lang (CC-BY-SA)               [re-run, curated]
#   t100 cosmic          = wiki science-filtered (CC-BY-SA)     [re-run, curated]
#   t77  art             = Gutenberg literature/poetry (PD)     [re-run, curated]
#   t91  consciousness   = Gutenberg philosophy/meditation (PD) [re-run, curated]
#   t52  social          = authored persona/SNS CAPPED          [re-run, curated]
#   shaping              = authored dialogue-act/emotion/...    [re-run, curated]
#
# DISK SAFETY (CRITICAL): web shards are tens of GB. Each lang's shard cache is
# PRUNED before the next lang so transient disk stays bounded. A disk-floor guard
# aborts the build if free space drops below DISK_FLOOR_GB. Override the MB knobs to
# retune scale vs disk.
#
# Usage:  HF_TOKEN=$(secret get hf.token) bash serving/gb_balanced/build_7b_webscale.sh
set -euo pipefail
cd "$(dirname "$0")/../.."   # repo root

SRC=serving/corpus/_src
OUT=serving/corpus/default_lane_7b_webscale.txt
mkdir -p "$SRC"

# disk floor (GB) — abort if free space drops below this. The box has ~44GB free;
# keep >=30GB free per the task DISK SAFETY directive.
DISK_FLOOR_GB=${DISK_FLOOR_GB:-30}

# transient shard caches (pruned aggressively). web shards are large -> per-lang prune.
export WEB_SHARD_CACHE=${WEB_SHARD_CACHE:-/tmp/anima_web_shards}
export WIKI_SHARD_CACHE=${WIKI_SHARD_CACHE:-/tmp/anima_wiki_shards}
export GUT_SHARD_CACHE=${GUT_SHARD_CACHE:-/tmp/anima_gut_shards}
export WEB_MAX_SHARDS=${WEB_MAX_SHARDS:-1}   # 1 shard/lang (each ~1-5GB); cap kept tight
export WIKI_MAX_SHARDS=${WIKI_MAX_SHARDS:-2}
export GUT_MAX_SHARDS=${GUT_MAX_SHARDS:-3}
cleanup() { rm -rf "$WEB_SHARD_CACHE" "$WIKI_SHARD_CACHE" "$GUT_SHARD_CACHE" 2>/dev/null || true; }
trap cleanup EXIT

disk_guard() {
    local free_gb
    free_gb=$(df -g . | awk 'NR==2{print $4}')
    echo "   [disk] ${free_gb}GB free (floor ${DISK_FLOOR_GB}GB)"
    if [ "$free_gb" -lt "$DISK_FLOOR_GB" ]; then
        echo "!! DISK FLOOR breached (${free_gb}GB < ${DISK_FLOOR_GB}GB) — pruning + aborting fetch"
        rm -rf "$WEB_SHARD_CACHE" "$WIKI_SHARD_CACHE" "$GUT_SHARD_CACHE" 2>/dev/null || true
        return 1
    fi
    return 0
}

# ladder knobs (MB per language). web bulk is the majority -> large per-lang budget;
# curated tiers stay modest (they are the minority by design).
MB_WEB=${MB_WEB:-1700}     # web bulk per lang (5 langs -> ~8.3GB target pre-balance)
MB_T0=${MB_T0:-90}         # wiki baseline
MB_T100=${MB_T100:-18}     # wiki science
MB_ART=${MB_ART:-60}       # Gutenberg art (en/fr/de/es; ko=0)
MB_CON=${MB_CON:-30}       # Gutenberg consciousness (en/fr/de/es; ko=0)
SHAPING_MB=${SHAPING_MB:-24}
PERSONA_MB=${PERSONA_MB:-60}

# ---- web bulk: fetch PER-LANG and prune the cache between langs (disk safety) ----
echo "== tier web (FineWeb-2 fr/de/ko + mC4 en/es, ODC-BY) — per-lang, prune-between =="
: > "$SRC/web_bulk.txt"
for L in en fr de es ko; do
    disk_guard || { echo "web: stopping at $L (disk)"; break; }
    echo "  -- web $L --"
    python3 serving/gb_balanced/fetch_web_bulk.py \
        --out "$SRC/web_$L.txt" --mb-per-lang "$MB_WEB" --langs "$L"
    cat "$SRC/web_$L.txt" >> "$SRC/web_bulk.txt"
    rm -f "$SRC/web_$L.txt"
    rm -rf "$WEB_SHARD_CACHE"   # prune this lang's shards before the next
done
echo "  web_bulk total: $(ls -la "$SRC/web_bulk.txt" | awk '{print $5}') bytes"

# ---- curated tiers (re-run the SAME generators; unchanged sources) ----
echo "== t0 wiki baseline =="
disk_guard && python3 serving/gb_balanced/fetch_wiki_tiers.py --tier 0   --out "$SRC/wiki_t0.txt"   --mb-per-lang "$MB_T0"
rm -rf "$WIKI_SHARD_CACHE"
echo "== t100 wiki science =="
disk_guard && python3 serving/gb_balanced/fetch_wiki_tiers.py --tier 100 --out "$SRC/wiki_t100.txt" --mb-per-lang "$MB_T100"
rm -rf "$WIKI_SHARD_CACHE"
echo "== t77 gutenberg art =="
disk_guard && python3 serving/gb_balanced/fetch_gutenberg_tiers.py --tier art           --out "$SRC/gut_art.txt" --mb-per-lang "$MB_ART"
rm -rf "$GUT_SHARD_CACHE"
echo "== t91 gutenberg consciousness =="
disk_guard && python3 serving/gb_balanced/fetch_gutenberg_tiers.py --tier consciousness --out "$SRC/gut_con.txt" --mb-per-lang "$MB_CON"
rm -rf "$GUT_SHARD_CACHE"

echo "== authored register-shaping =="
python3 serving/corpus_enrichment_5lang_gen.py --target-mb "$SHAPING_MB" \
    --anchors HEXAD/UNIVERSE-BRAIN-MAP/anchors/e7_31 --out "$SRC/shaping.txt"
echo "== authored persona/SNS (CAPPED) =="
python3 serving/persona_sns_corpus_5lang_gen.py --target-mb "$PERSONA_MB" --out "$SRC/persona.txt"

echo "== balance + merge (web MAJORITY, curated floor-protected) + account =="
python3 serving/gb_balanced/balance_merge_7b.py \
    --src-dir "$SRC" --web "$SRC/web_bulk.txt" \
    --shaping "$SRC/shaping.txt" --persona "$SRC/persona.txt" \
    --out "$OUT" --report "$SRC/7b_webscale_report.json"

echo "== DONE: $OUT =="
ls -la "$OUT"
df -h . | tail -1
