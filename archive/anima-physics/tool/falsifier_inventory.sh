#!/usr/bin/env bash
# falsifier_inventory.sh — auto-grep F-<NAME>-N pattern across anima-physics
#
# Goal: enumerate every falsifier declaration (in .hexa + .py sources) plus
#       PASS/FAIL run results (in state/ logs), produce a markdown table, and
#       cross-check against PLAN.md G2 expected count.
#
# Usage:
#   ./tool/falsifier_inventory.sh           # human-readable markdown to stdout
#   ./tool/falsifier_inventory.sh --md      # same as default (explicit)
#
# Constraints: pure bash; no python, no jq. Scans state/**/*.log + .json + .md.
# Pattern: F-<NAME>-<N> where <NAME> = [A-Z0-9_]+ and <N> = digits.

set -u

ROOT="${ROOT:-/Users/ghost/core/anima/anima-physics}"
PATTERN='F-[A-Z0-9_]+-[0-9]+'

# ---- 0. header ----------------------------------------------------------
printf '# anima-physics falsifier inventory\n\n'
printf '_root_: `%s`\n' "$ROOT"
printf '_pattern_: `%s`\n' "$PATTERN"
printf '_generated_: %s\n\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# ---- 1. SW falsifier declarations per substrate (.hexa) ----------------
printf '## 1. SW falsifier declarations (.hexa, per substrate)\n\n'
printf '| substrate | family | distinct F-* | total occurrences | source file |\n'
printf '|---|---|---:|---:|---|\n'

TOTAL_HEXA_DECL_UNIQUE=0
TOTAL_HEXA_DECL_OCC=0
SUBSTRATES_WITH_F=0

# iterate every .hexa file under root, skip .venv + build artifacts
while IFS= read -r f; do
    [ -z "$f" ] && continue
    occ=$(grep -hoE "$PATTERN" "$f" 2>/dev/null | wc -l | tr -d ' ')
    [ "$occ" -eq 0 ] && continue
    uniq=$(grep -hoE "$PATTERN" "$f" 2>/dev/null | sort -u | wc -l | tr -d ' ')
    family=$(grep -hoE "$PATTERN" "$f" 2>/dev/null | sed 's/-[0-9]*$//' | sort -u | tr '\n' ',' | sed 's/,$//')
    # substrate = first dir component after root
    rel="${f#$ROOT/}"
    substrate=$(printf '%s' "$rel" | awk -F/ '{print $1}')
    # if hw/<target>/*.hexa, use hw/<target> as substrate
    if [ "$substrate" = "hw" ]; then
        substrate="hw/$(printf '%s' "$rel" | awk -F/ '{print $2}')"
    fi
    fname=$(basename "$f")
    printf '| %s | %s | %d | %d | %s |\n' "$substrate" "$family" "$uniq" "$occ" "$fname"
    TOTAL_HEXA_DECL_UNIQUE=$((TOTAL_HEXA_DECL_UNIQUE + uniq))
    TOTAL_HEXA_DECL_OCC=$((TOTAL_HEXA_DECL_OCC + occ))
    SUBSTRATES_WITH_F=$((SUBSTRATES_WITH_F + 1))
done < <(find "$ROOT" -name "*.hexa" -type f \
            -not -path "*/.venv/*" \
            -not -path "*/build/artifacts/*" \
            -not -path "*/engines/build/*" \
            2>/dev/null | sort)

printf '\n_subtotal_: %d files, %d unique F-* IDs, %d total occurrences\n\n' \
    "$SUBSTRATES_WITH_F" "$TOTAL_HEXA_DECL_UNIQUE" "$TOTAL_HEXA_DECL_OCC"

# ---- 2. SW falsifier declarations (.py) --------------------------------
printf '## 2. SW falsifier declarations (.py)\n\n'
printf '| file | distinct F-* | total occurrences |\n'
printf '|---|---:|---:|\n'

TOTAL_PY_DECL_UNIQUE=0
TOTAL_PY_DECL_OCC=0
PY_FILES=0

while IFS= read -r f; do
    [ -z "$f" ] && continue
    occ=$(grep -hoE "$PATTERN" "$f" 2>/dev/null | wc -l | tr -d ' ')
    [ "$occ" -eq 0 ] && continue
    uniq=$(grep -hoE "$PATTERN" "$f" 2>/dev/null | sort -u | wc -l | tr -d ' ')
    rel="${f#$ROOT/}"
    printf '| %s | %d | %d |\n' "$rel" "$uniq" "$occ"
    TOTAL_PY_DECL_UNIQUE=$((TOTAL_PY_DECL_UNIQUE + uniq))
    TOTAL_PY_DECL_OCC=$((TOTAL_PY_DECL_OCC + occ))
    PY_FILES=$((PY_FILES + 1))
done < <(find "$ROOT" -name "*.py" -type f \
            -not -path "*/.venv/*" \
            -not -path "*/build/artifacts/*" \
            2>/dev/null | sort)

printf '\n_subtotal_: %d files, %d unique F-* IDs, %d total occurrences\n\n' \
    "$PY_FILES" "$TOTAL_PY_DECL_UNIQUE" "$TOTAL_PY_DECL_OCC"

# ---- 3. state/ run results (PASS/FAIL/TIMEOUT) -------------------------
printf '## 3. state/ run results (PASS / FAIL / TIMEOUT lines)\n\n'
printf '| state dir | PASS | FAIL | TIMEOUT | F-* in dir |\n'
printf '|---|---:|---:|---:|---:|\n'

TOTAL_PASS=0
TOTAL_FAIL=0
TOTAL_TIMEOUT=0

# include state/<sub>/ + hw/<target>/state/
for sdir in "$ROOT"/state/*/ "$ROOT"/hw/*/state/; do
    [ -d "$sdir" ] || continue
    # count PASS/FAIL/TIMEOUT across .log + .json + .md (case-sensitive whole word)
    pass=$(grep -rhwE "PASS" "$sdir" --include="*.log" --include="*.json" --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
    fail=$(grep -rhwE "FAIL" "$sdir" --include="*.log" --include="*.json" --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
    tout=$(grep -rhwE "TIMEOUT" "$sdir" --include="*.log" --include="*.json" --include="*.md" 2>/dev/null | wc -l | tr -d ' ')
    fids=$(grep -rhoE "$PATTERN" "$sdir" --include="*.log" --include="*.json" --include="*.md" 2>/dev/null | sort -u | wc -l | tr -d ' ')
    if [ "$pass" -gt 0 ] || [ "$fail" -gt 0 ] || [ "$tout" -gt 0 ] || [ "$fids" -gt 0 ]; then
        # build label as last-2 path components
        parent=$(basename "$(dirname "$sdir")")
        leaf=$(basename "$sdir")
        if [ "$parent" = "state" ]; then
            label="state/$leaf"
        else
            label="hw/$parent/$leaf"
        fi
        printf '| %s | %d | %d | %d | %d |\n' "$label" "$pass" "$fail" "$tout" "$fids"
        TOTAL_PASS=$((TOTAL_PASS + pass))
        TOTAL_FAIL=$((TOTAL_FAIL + fail))
        TOTAL_TIMEOUT=$((TOTAL_TIMEOUT + tout))
    fi
done

printf '\n_subtotal_: PASS=%d, FAIL=%d, TIMEOUT=%d\n\n' \
    "$TOTAL_PASS" "$TOTAL_FAIL" "$TOTAL_TIMEOUT"

# ---- 4. unique F-* family roll-up across the whole tree ----------------
printf '## 4. Unique F-* family roll-up (across all .hexa + .py)\n\n'
printf '| family (F-<NAME>) | members (count) | files |\n'
printf '|---|---:|---|\n'

# build a temp index: family -> distinct IDs -> files
TMP_FAMILY=$(mktemp -t falsifier_family.XXXXXX)
trap 'rm -f "$TMP_FAMILY"' EXIT

while IFS= read -r f; do
    [ -z "$f" ] && continue
    grep -hoE "$PATTERN" "$f" 2>/dev/null | sort -u | while read -r id; do
        family=$(printf '%s' "$id" | sed 's/-[0-9]*$//')
        printf '%s\t%s\t%s\n' "$family" "$id" "${f#$ROOT/}" >> "$TMP_FAMILY"
    done
done < <(find "$ROOT" \( -name "*.hexa" -o -name "*.py" \) -type f \
            -not -path "*/.venv/*" \
            -not -path "*/build/artifacts/*" \
            -not -path "*/engines/build/*" \
            2>/dev/null | sort)

# aggregate per family
awk -F'\t' '{
    fam=$1; id=$2; file=$3;
    ids[fam]=ids[fam] " " id;
    files[fam]=files[fam] " " file;
}
END {
    for (fam in ids) {
        n=split(ids[fam], a, " ");
        # dedupe ids
        delete seen;
        ucount=0;
        for (i=1;i<=n;i++) if (a[i]!="" && !seen[a[i]]++) ucount++;
        # dedupe files
        m=split(files[fam], b, " ");
        delete fseen;
        fout="";
        for (i=1;i<=m;i++) if (b[i]!="" && !fseen[b[i]]++) fout=fout " " b[i];
        print fam "\t" ucount "\t" fout;
    }
}' "$TMP_FAMILY" | sort > "${TMP_FAMILY}.agg"

TOTAL_FAMILIES=0
TOTAL_UNIQUE_IDS=0
while IFS=$'\t' read -r fam ucount fout; do
    printf '| %s | %d |%s |\n' "$fam" "$ucount" "$fout"
    TOTAL_FAMILIES=$((TOTAL_FAMILIES + 1))
    TOTAL_UNIQUE_IDS=$((TOTAL_UNIQUE_IDS + ucount))
done < "${TMP_FAMILY}.agg"
rm -f "${TMP_FAMILY}.agg"

printf '\n_subtotal_: %d distinct families, %d unique F-* IDs declared\n\n' \
    "$TOTAL_FAMILIES" "$TOTAL_UNIQUE_IDS"

# ---- 4b. §188 substrate T<N> PASS/FAIL convention (legacy/parallel naming) -
# §188 21-substrate fire used `T1..T5` in selftest println, not F-<NAME>-N.
# Capture that too for honest accounting.
printf '## 4b. §188 substrate T<N> PASS/FAIL declarations (.hexa)\n\n'
printf '| substrate file | T<N> PASS literals | T<N> FAIL literals |\n'
printf '|---|---:|---:|\n'

TOTAL_T_PASS=0
TOTAL_T_FAIL=0
T_FILES=0

while IFS= read -r f; do
    [ -z "$f" ] && continue
    tpass=$(grep -hoE 'T[0-9]+ PASS' "$f" 2>/dev/null | wc -l | tr -d ' ')
    tfail=$(grep -hoE 'T[0-9]+ FAIL' "$f" 2>/dev/null | wc -l | tr -d ' ')
    [ "$tpass" -eq 0 ] && [ "$tfail" -eq 0 ] && continue
    rel="${f#$ROOT/}"
    printf '| %s | %d | %d |\n' "$rel" "$tpass" "$tfail"
    TOTAL_T_PASS=$((TOTAL_T_PASS + tpass))
    TOTAL_T_FAIL=$((TOTAL_T_FAIL + tfail))
    T_FILES=$((T_FILES + 1))
done < <(find "$ROOT" -name "*.hexa" -type f \
            -not -path "*/.venv/*" \
            -not -path "*/build/artifacts/*" \
            -not -path "*/engines/build/*" \
            2>/dev/null | sort)

printf '\n_subtotal_: %d files, %d "T<N> PASS" literals, %d "T<N> FAIL" literals\n' \
    "$T_FILES" "$TOTAL_T_PASS" "$TOTAL_T_FAIL"
printf '_note_: each substrate selftest typically prints 5 PASS + 5 FAIL literals (one each per branch); divide by 2 for distinct T-tests.\n\n'

# ---- 5. aggregate + PLAN.md cross-check --------------------------------
printf '## 5. Aggregate + PLAN.md G2 cross-check\n\n'

# PLAN.md expected per task brief: §188 21 + §188g 35 + G2 add 30 = 86
PLAN_EXPECTED=86

# §188 substrate count: each file has 5 T-tests → unique T-tests = T_PASS_LITERALS / 2
# (PASS + FAIL literals are mirrored in if/else branches, so distinct tests = PASS_count
#  when each test branch prints PASS once and FAIL once → distinct tests ≈ PASS literal count)
T_DISTINCT_TESTS=$TOTAL_T_PASS

# Total substrate-level falsifier count (the §188 + §188g + G2 universe):
# - T<N>-style substrate selftests (§188 + later substrates)
# - F-<NAME>-N declarations (§188g engines + G2 6-substrate + E2E)
TOTAL_FALSIFIERS=$((TOTAL_UNIQUE_IDS + T_DISTINCT_TESTS))

printf -- '- total F-* declarations (.hexa, occurrences): **%d**\n' "$TOTAL_HEXA_DECL_OCC"
printf -- '- total F-* declarations (.hexa, unique-per-file): **%d**\n' "$TOTAL_HEXA_DECL_UNIQUE"
printf -- '- total F-* declarations (.py, occurrences): **%d**\n' "$TOTAL_PY_DECL_OCC"
printf -- '- total unique F-* IDs across tree: **%d**\n' "$TOTAL_UNIQUE_IDS"
printf -- '- total F-* distinct families: **%d**\n' "$TOTAL_FAMILIES"
printf -- '- §188 T<N> substrate selftests (distinct, from %d files): **%d**\n' \
    "$T_FILES" "$T_DISTINCT_TESTS"
printf -- '- **combined falsifier-tests universe (F-* unique + T<N>)**: **%d**\n' "$TOTAL_FALSIFIERS"
printf -- '- state/ PASS lines: **%d**, FAIL: **%d**, TIMEOUT: **%d**\n' \
    "$TOTAL_PASS" "$TOTAL_FAIL" "$TOTAL_TIMEOUT"
printf -- '- PLAN.md G2 expected (§188 21 + §188g 35 + G2 add 30): **%d**\n' "$PLAN_EXPECTED"

DRIFT=$((TOTAL_FALSIFIERS - PLAN_EXPECTED))
if [ "$DRIFT" -eq 0 ]; then
    printf -- '- **drift (combined vs PLAN 86)**: 0 (exact match)\n'
elif [ "$DRIFT" -gt 0 ]; then
    printf -- '- **drift (combined vs PLAN 86)**: +%d (more declared than PLAN expected — additional E2E / cross-engine / aux falsifiers post-G2)\n' "$DRIFT"
else
    printf -- '- **drift (combined vs PLAN 86)**: %d (fewer declared than PLAN expected — investigate missing substrates / pattern mismatch)\n' "$DRIFT"
fi

# also report F-* only drift (the strictest interpretation)
F_ONLY_DRIFT=$((TOTAL_UNIQUE_IDS - PLAN_EXPECTED))
if [ "$F_ONLY_DRIFT" -lt 0 ]; then
    printf -- '- **F-* only drift vs PLAN 86**: %d — gap is because §188 21-substrate baseline uses T<N> selftest convention rather than F-<NAME>-N IDs; modern §188g/G2/E2E suites are the ones using F-<NAME>-N.\n' "$F_ONLY_DRIFT"
fi

printf '\n_done_\n'
