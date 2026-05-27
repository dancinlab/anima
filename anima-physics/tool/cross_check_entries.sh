#!/usr/bin/env bash
# G3 entry cross-check tool — anima-physics
# 작성 2026-05-21 (PLAN.md G3 ☑ 목표)
#
# entries/{root,docs,substrate,recovered}/**/*.md  ↔  실 *.hexa 파일 1:1 매핑 검증.
# drift 발견 시 report 만 출력 (자동 추가/삭제 X — lint only).
#
# Mapping rules:
#   - depth-1 *.hexa  (e.g. physics.hexa)         → entries/root/<basename>.md
#   - sub-dir *.hexa  (e.g. fpga/strange_loop.hexa) → entries/substrate/<rel_path>.md
#   - docs/*.md (no .hexa)                        → docs-only entry, skip
#   - recovered/<family>/*.md (no .hexa)          → archive-only entry, skip
#   - scripts/*.py (no .hexa)                     → substrate entry (basename match)
#
# Exit: 0 = clean (no drift),  1 = drift found

set -uo pipefail

ROOT="${ROOT:-/Users/ghost/core/anima/anima-physics}"
OUT_DIR="${OUT_DIR:-$ROOT/state/g3_entry_cross_check_2026_05_21}"
REPORT="$OUT_DIR/lint_report.txt"

mkdir -p "$OUT_DIR"

# Inventory --------------------------------------------------------------------
HEXA_LIST="$(mktemp -t cross_check_hexa.XXXXXX)"
ENTRY_LIST="$(mktemp -t cross_check_entry.XXXXXX)"
EXPECTED_LIST="$(mktemp -t cross_check_expected.XXXXXX)"
trap 'rm -f "$HEXA_LIST" "$ENTRY_LIST" "$EXPECTED_LIST"' EXIT

# All .hexa under anima-physics (exclude entries/, state/, build/, recovered/, scripts/)
find "$ROOT" -type f -name "*.hexa" \
  -not -path "*/entries/*" \
  -not -path "*/state/*" \
  -not -path "*/build/*" \
  -not -path "*/recovered/*" \
  | sort > "$HEXA_LIST"

# All entry .md files
find "$ROOT/entries" -type f -name "*.md" | sort > "$ENTRY_LIST"

# Compute expected entry path per .hexa --------------------------------------
while IFS= read -r hexa; do
  rel="${hexa#$ROOT/}"        # e.g. fpga/strange_loop.hexa or physics.hexa
  base_noext="${rel%.hexa}"   # e.g. fpga/strange_loop  or physics
  if [[ "$base_noext" != */* ]]; then
    # depth-1 → root
    echo "$ROOT/entries/root/${base_noext}.md"
  else
    # sub-dir → substrate
    echo "$ROOT/entries/substrate/${base_noext}.md"
  fi
done < "$HEXA_LIST" | sort -u > "$EXPECTED_LIST"

# Diffs ------------------------------------------------------------------------
# missing = expected entry not present in entries/
MISSING="$(comm -23 "$EXPECTED_LIST" "$ENTRY_LIST")"
# orphan = entry present but expected path NOT generated from any .hexa.
# Caveat: docs/, recovered/, scripts/*.py-only and 2 root special (readme,manifest)
# are docs-only/archive-only entries — we filter them out before flagging.
ORPHAN_RAW="$(comm -13 "$EXPECTED_LIST" "$ENTRY_LIST")"

# Filter orphan: keep only those expected from a .hexa
# (i.e. exclude entries/docs/*, entries/recovered/*, entries/root/{readme,manifest}.md,
#  entries/substrate/scripts/*.md, entries/substrate/esp32/QRNG_SPEC.md spec sidecars)
ORPHAN="$(
  echo "$ORPHAN_RAW" | awk -v root="$ROOT" '
    {
      p = $0
      if (p == "") next
      # docs-only category
      if (index(p, root "/entries/docs/") == 1) next
      # archive-only category
      if (index(p, root "/entries/recovered/") == 1) next
      # root specials (no .hexa counterpart by design)
      if (p == root "/entries/root/readme.md") next
      if (p == root "/entries/root/manifest.md") next
      # substrate-scripts (.py sidecars)
      if (index(p, root "/entries/substrate/scripts/") == 1) next
      # ALL_CAPS spec sidecars (e.g. QRNG_SPEC.md)
      n = split(p, parts, "/")
      bn = parts[n]
      if (bn ~ /^[A-Z][A-Z0-9_]+\.md$/) next
      print p
    }
  '
)"

# Counts -----------------------------------------------------------------------
N_HEXA=$(wc -l < "$HEXA_LIST" | tr -d ' ')
N_ENTRY=$(wc -l < "$ENTRY_LIST" | tr -d ' ')
N_ROOT=$(find "$ROOT/entries/root" -type f -name "*.md" | wc -l | tr -d ' ')
N_DOCS=$(find "$ROOT/entries/docs" -type f -name "*.md" | wc -l | tr -d ' ')
N_SUB=$(find "$ROOT/entries/substrate" -type f -name "*.md" | wc -l | tr -d ' ')
N_REC=$(find "$ROOT/entries/recovered" -type f -name "*.md" | wc -l | tr -d ' ')
N_MISSING=$(printf "%s\n" "$MISSING" | sed '/^$/d' | wc -l | tr -d ' ')
N_ORPHAN=$(printf "%s\n" "$ORPHAN" | sed '/^$/d' | wc -l | tr -d ' ')

# Report -----------------------------------------------------------------------
{
  echo "# G3 entry cross-check lint report"
  echo "date: 2026-05-21"
  echo "tool: tool/cross_check_entries.sh"
  echo "root: $ROOT"
  echo
  echo "## Counts"
  echo "- .hexa files (excl. entries/state/build/recovered): $N_HEXA"
  echo "- entry .md files: $N_ENTRY"
  echo "  - root:       $N_ROOT"
  echo "  - docs:       $N_DOCS"
  echo "  - substrate:  $N_SUB"
  echo "  - recovered:  $N_REC"
  echo
  echo "## Missing entries (have .hexa but no entry md) — $N_MISSING"
  if [ "$N_MISSING" -eq 0 ]; then
    echo "  (none)"
  else
    printf "%s\n" "$MISSING" | sed '/^$/d' | sed "s|^$ROOT/|  - |"
  fi
  echo
  echo "## Orphan entries (entry md present but no .hexa, filtered) — $N_ORPHAN"
  if [ "$N_ORPHAN" -eq 0 ]; then
    echo "  (none)"
  else
    printf "%s\n" "$ORPHAN" | sed '/^$/d' | sed "s|^$ROOT/|  - |"
  fi
  echo
  echo "## Notes"
  echo "- Filtered out (by design, docs-only/archive-only):"
  echo "  - entries/docs/*.md (19 spec/landing reports, no .hexa)"
  echo "  - entries/recovered/*.md (3 chip-family archive entries)"
  echo "  - entries/root/{readme,manifest}.md (README_legacy + signal_corpus_manifest.json)"
  echo "  - entries/substrate/scripts/*.md (.py sidecars: anima_physics_braket_{ionq,quera}_probe)"
  echo "  - entries/substrate/<dir>/ALL_CAPS.md (e.g. esp32/QRNG_SPEC.md)"
  if [ "$N_MISSING" -eq 0 ] && [ "$N_ORPHAN" -eq 0 ]; then
    echo
    echo "## Verdict: CLEAN — 1:1 mapping holds (excluding docs-only categories)"
  else
    echo
    echo "## Verdict: DRIFT — see lists above"
  fi
} > "$REPORT"

cat "$REPORT"

if [ "$N_MISSING" -eq 0 ] && [ "$N_ORPHAN" -eq 0 ]; then
  exit 0
else
  exit 1
fi
