#!/usr/bin/env bash
# bin/check_licenses.sh — license firewall enforcer (Part A, Sprint 1)
#
# Reads vendor/external_deps.yaml + vendor/license_policy.yaml. Walks the 4
# protected layers (eeg/, eeg_core/, core/, tool/) and greps each
# blocked_import_pattern against `.hexa` and `.py` source files. Emits a
# marker + jsonl ledger row. Skips '//' comment-only matches.
#
# Modes:
#   bin/check_licenses.sh             # scan tree, exit 0 on clean / 2 on viol.
#   bin/check_licenses.sh --selftest  # run F_LF_01/02/03 falsifiers
#   bin/check_licenses.sh --help      # show usage
#
# Marker:
#   state/markers/license_firewall_check_<ts>[_FAILED].marker
#     { "source":"bin/check_licenses.sh", "exit":0|2,
#       "fingerprint":"<sha8 of external_deps.yaml>", "ts":<unixts>,
#       "checked_files":<N>, "violations":<M> }
#
# Ledger:
#   state/license_firewall_checks.jsonl  (append-only)
#
# raw#9 strict: this file is the explicit opt-out — it must run BEFORE any
# .hexa file is invoked, so it cannot depend on the hexa runtime itself.
# raw#37: any /tmp helper this script writes is named license_firewall_*.py
# and is removed on exit.
# raw#65: idempotent — repeated calls on a clean tree all PASS identically.

set -uo pipefail

# ── Resolve repo root ────────────────────────────────────────────────────
if [[ -n "${HEXA_BRAIN_ROOT:-}" && -d "$HEXA_BRAIN_ROOT" ]]; then
    ROOT="$HEXA_BRAIN_ROOT"
elif [[ -L "${BASH_SOURCE[0]}" ]]; then
    SELF="$(readlink -f "${BASH_SOURCE[0]}" 2>/dev/null || readlink "${BASH_SOURCE[0]}")"
    ROOT="$(cd "$(dirname "$SELF")/.." && pwd)"
else
    ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
fi

DEPS_YAML="$ROOT/vendor/external_deps.yaml"
POLICY_YAML="$ROOT/vendor/license_policy.yaml"
MARKERS_DIR="$ROOT/state/markers"
LEDGER="$ROOT/state/license_firewall_checks.jsonl"

PROTECTED_LAYERS=(eeg eeg_core core tool)

mkdir -p "$MARKERS_DIR" "$ROOT/state"

print_help() {
    cat <<EOF
bin/check_licenses.sh — hexa-brain license firewall enforcer

USAGE:
  bin/check_licenses.sh            scan tree, emit marker + ledger row
  bin/check_licenses.sh --selftest run F_LF_01/02/03 falsifiers
  bin/check_licenses.sh --help     this text

EXIT:
  0  clean (no blocked imports in protected layers)
  2  violation(s) found (printed to stderr + marker _FAILED)
  3  configuration error (missing yaml, etc.)

Reads:
  vendor/external_deps.yaml
  vendor/license_policy.yaml

Writes:
  state/markers/license_firewall_check_<ts>[_FAILED].marker
  state/license_firewall_checks.jsonl

Docs:
  LICENSE_FIREWALL.md
  design/license_firewall.md
EOF
}

# ── Pre-flight ───────────────────────────────────────────────────────────
if [[ ! -f "$DEPS_YAML" ]]; then
    echo "FATAL: catalog missing: $DEPS_YAML" >&2
    exit 3
fi
if [[ ! -f "$POLICY_YAML" ]]; then
    echo "FATAL: policy missing: $POLICY_YAML" >&2
    exit 3
fi

# ── Fingerprint catalog (first 8 chars of sha256) ────────────────────────
catalog_fingerprint() {
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum "$DEPS_YAML" | cut -c1-8
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 "$DEPS_YAML" | cut -c1-8
    else
        # Last-ditch python3 fallback (we already require python3 below)
        python3 -c "import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()[:8])" "$DEPS_YAML"
    fi
}

# ── Read blocked patterns from YAML via python3 ──────────────────────────
# Returns lines: "<dep_id>\t<pattern>" for every entry whose
# blocked_import_patterns list is non-empty AND coupling is not purely loose
# AGAINST in_process tight coupling. The firewall blocks an import iff:
#   the source file is inside a protected layer AND
#   the import matches one of the patterns AND
#   the dep's coupling_modes do NOT include in_process for that license.
# In practice (Sprint 1): we list patterns ONLY for deps whose tight import
# would violate the layer allow-list (AGPL, CC-NC, no-license). The YAML
# author manages this — we trust the catalog.
TMP_HELPER="/tmp/license_firewall_load_$$.py"
trap 'rm -f /tmp/license_firewall_*_$$.py' EXIT

cat >"$TMP_HELPER" <<'PYEOF'
import os, re, sys, json
deps_path, policy_path = sys.argv[1], sys.argv[2]

def load_yaml(p):
    try:
        import yaml
        with open(p, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except ImportError:
        # Trivial fallback parser — supports the exact schema we own.
        # Skipped at runtime if pyyaml is available.
        return _fallback_parse(p)

def _fallback_parse(p):
    # Minimal subset: top-level scalar `schema:`, `deps:` list of mappings,
    # `layers:` list of mappings. Values are scalar strings, lists of
    # strings (flow `[a, b]`), or block lists. No nested non-list mappings.
    with open(p, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    out = {}
    cur_list = None
    cur_item = None
    cur_key = None
    multiline_buf = None
    for raw in lines:
        line = raw.rstrip('\n')
        # Strip pure-comment lines but preserve indentation-only blanks.
        if line.lstrip().startswith('#'):
            continue
        if line.strip() == '':
            if multiline_buf is not None:
                cur_item[cur_key] = '\n'.join(multiline_buf)
                multiline_buf = None
                cur_key = None
            continue
        # Multiline pipe continuation
        if multiline_buf is not None:
            if line.startswith('      ') or line.startswith('    '):
                multiline_buf.append(line.lstrip())
                continue
            else:
                cur_item[cur_key] = '\n'.join(multiline_buf)
                multiline_buf = None
                cur_key = None
        # Top-level key
        if not line.startswith(' ') and line.endswith(':'):
            key = line[:-1].strip()
            out[key] = []
            cur_list = out[key]
            cur_item = None
            continue
        if not line.startswith(' ') and ':' in line:
            k, v = line.split(':', 1)
            out[k.strip()] = v.strip()
            continue
        # New list item
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if stripped.startswith('- '):
            cur_item = {}
            cur_list.append(cur_item)
            stripped = stripped[2:]
            if ':' in stripped:
                k, v = stripped.split(':', 1)
                v = v.strip()
                if v.startswith('[') and v.endswith(']'):
                    inner = v[1:-1].strip()
                    cur_item[k.strip()] = [x.strip() for x in inner.split(',') if x.strip()]
                elif v == '|':
                    multiline_buf = []
                    cur_key = k.strip()
                else:
                    cur_item[k.strip()] = v
            continue
        if ':' in stripped and cur_item is not None:
            k, v = stripped.split(':', 1)
            v = v.strip()
            if v.startswith('[') and v.endswith(']'):
                inner = v[1:-1].strip()
                cur_item[k.strip()] = [x.strip() for x in inner.split(',') if x.strip()]
            elif v == '|':
                multiline_buf = []
                cur_key = k.strip()
            else:
                cur_item[k.strip()] = v
            continue
        if stripped.startswith('- ') and cur_item is not None:
            # nested list item under prev key — Sprint 1 schema does not use
            pass
    if multiline_buf is not None and cur_item is not None and cur_key is not None:
        cur_item[cur_key] = '\n'.join(multiline_buf)
    return out

deps = load_yaml(deps_path)
policy = load_yaml(policy_path)

# Emit lines: "<dep_id>\t<pattern>\t<spdx>\t<coupling_csv>"
patterns = []
for d in (deps.get('deps') or []):
    pats = d.get('blocked_import_patterns') or []
    if not isinstance(pats, list):
        continue
    for p in pats:
        patterns.append((d.get('id') or '', p, d.get('spdx') or '', ','.join(d.get('coupling_modes') or [])))

for did, pat, spdx, coup in patterns:
    print(f"{did}\t{pat}\t{spdx}\t{coup}")
PYEOF

# Read patterns into bash arrays.
mapfile -t PATTERN_LINES < <(python3 "$TMP_HELPER" "$DEPS_YAML" "$POLICY_YAML")

if [[ "${#PATTERN_LINES[@]}" -eq 0 ]]; then
    : # nothing to block — catalog is policy-empty
fi

# ── Scan function ────────────────────────────────────────────────────────
# Returns 0 if clean, 2 if violations. Sets globals CHECKED_FILES,
# VIOLATIONS_COUNT, VIOLATIONS_LIST (newline-separated "file:line:msg").
CHECKED_FILES=0
VIOLATIONS_COUNT=0
VIOLATIONS_LIST=""

scan_tree() {
    local extra_root="${1:-}"   # optional sandbox root override for selftest

    local scan_root="${extra_root:-$ROOT}"
    local layer
    local files=()
    for layer in "${PROTECTED_LAYERS[@]}"; do
        local dir="$scan_root/$layer"
        if [[ ! -d "$dir" ]]; then
            continue
        fi
        # find .hexa and .py files; null-delim safe
        while IFS= read -r -d '' f; do
            files+=("$f")
        done < <(find "$dir" -type f \( -name '*.hexa' -o -name '*.py' \) -print0 2>/dev/null)
    done

    CHECKED_FILES="${#files[@]}"

    if [[ "${#PATTERN_LINES[@]}" -eq 0 ]]; then
        return 0
    fi

    local f line lineno content pat dep_id spdx coup
    local hit_msg
    for f in "${files[@]}"; do
        # Read once
        local fcontent
        fcontent="$(cat "$f")"
        lineno=0
        while IFS= read -r line; do
            lineno=$((lineno + 1))
            # Strip leading whitespace
            local stripped="${line#"${line%%[![:space:]]*}"}"
            # Skip pure-comment lines (// ... or # ... — both common in hexa
            # + python). raw#9 hexa-only uses // exclusively but .py uses #.
            case "$stripped" in
                "//"*|"#"*) continue ;;
            esac
            for entry in "${PATTERN_LINES[@]}"; do
                dep_id="${entry%%$'\t'*}"
                rest="${entry#*$'\t'}"
                pat="${rest%%$'\t'*}"
                rest2="${rest#*$'\t'}"
                spdx="${rest2%%$'\t'*}"
                coup="${rest2#*$'\t'}"
                [[ -z "$pat" ]] && continue
                # Regex: ^[^/]*import\s+<pat>|^[^/]*from\s+<pat>
                # Note: <pat> is a regex fragment from YAML.
                if [[ "$line" =~ ^[^/]*import[[:space:]]+${pat} ]] || \
                   [[ "$line" =~ ^[^/]*from[[:space:]]+${pat} ]]; then
                    hit_msg="$f:$lineno: blocked import for dep=$dep_id spdx=$spdx coupling=$coup pattern=$pat"
                    VIOLATIONS_LIST+="${hit_msg}"$'\n'
                    VIOLATIONS_COUNT=$((VIOLATIONS_COUNT + 1))
                fi
            done
        done <<<"$fcontent"
    done

    if [[ "$VIOLATIONS_COUNT" -gt 0 ]]; then
        return 2
    fi
    return 0
}

# ── Emit marker + ledger row ─────────────────────────────────────────────
emit_marker_and_ledger() {
    local exit_code="$1"
    local checked="$2"
    local violations="$3"
    local label="${4:-license_firewall_check}"

    local ts; ts="$(date +%s)"
    local fp; fp="$(catalog_fingerprint)"
    local suffix=""
    if [[ "$exit_code" -ne 0 ]]; then
        suffix="_FAILED"
    fi
    local marker="$MARKERS_DIR/${label}_${ts}${suffix}.marker"
    printf '{"source":"bin/check_licenses.sh","exit":%d,"fingerprint":"%s","ts":%d,"checked_files":%d,"violations":%d}\n' \
        "$exit_code" "$fp" "$ts" "$checked" "$violations" > "$marker"

    # Ledger row (jsonl)
    printf '{"schema":"hexa-brain/license_firewall_check/1","ts":%d,"fingerprint":"%s","exit":%d,"checked_files":%d,"violations":%d,"label":"%s"}\n' \
        "$ts" "$fp" "$exit_code" "$checked" "$violations" "$label" >> "$LEDGER"

    echo "$marker"
}

# ── Self-test mode ───────────────────────────────────────────────────────
run_selftest() {
    local pass=0 fail=0
    local sandbox; sandbox="$(mktemp -d /tmp/license_firewall_selftest_XXXXXX)"
    trap "rm -rf '$sandbox'; rm -f /tmp/license_firewall_*_$$.py" EXIT

    echo "=== bin/check_licenses.sh --selftest (F_LF_01/02/03) ==="

    # ── F_LF_01: empty sandbox tree → PASS (exit 0) ──
    echo "[F_LF_01] clean tree → expect exit 0"
    mkdir -p "$sandbox/eeg" "$sandbox/eeg_core" "$sandbox/tool"
    CHECKED_FILES=0; VIOLATIONS_COUNT=0; VIOLATIONS_LIST=""
    if scan_tree "$sandbox"; then
        echo "  PASS: F_LF_01 clean tree exit 0 (checked_files=$CHECKED_FILES)"
        pass=$((pass + 1))
    else
        echo "  FAIL: F_LF_01 expected exit 0, got 2 (violations=$VIOLATIONS_COUNT)"
        echo "$VIOLATIONS_LIST"
        fail=$((fail + 1))
    fi

    # ── F_LF_02: plant `from braingenix import x` → expect exit 2 ──
    echo "[F_LF_02] plant 'from braingenix import x' → expect exit 2"
    echo 'from braingenix import x' > "$sandbox/eeg/_lf02_fixture.hexa"
    CHECKED_FILES=0; VIOLATIONS_COUNT=0; VIOLATIONS_LIST=""
    scan_tree "$sandbox"
    local rc=$?
    if [[ "$rc" -eq 2 && "$VIOLATIONS_COUNT" -ge 1 ]]; then
        echo "  PASS: F_LF_02 caught violation (count=$VIOLATIONS_COUNT)"
        pass=$((pass + 1))
    else
        echo "  FAIL: F_LF_02 expected rc=2 violations>=1, got rc=$rc count=$VIOLATIONS_COUNT"
        fail=$((fail + 1))
    fi
    rm -f "$sandbox/eeg/_lf02_fixture.hexa"

    # ── F_LF_03: comment-only mention → expect exit 0 ──
    echo "[F_LF_03] '// import cl_sdk' inside comment → expect exit 0"
    printf '// import cl_sdk should be ignored\n// from cortical_labs import y\n' > "$sandbox/eeg/_lf03_fixture.hexa"
    CHECKED_FILES=0; VIOLATIONS_COUNT=0; VIOLATIONS_LIST=""
    if scan_tree "$sandbox"; then
        echo "  PASS: F_LF_03 comment-only ignored (checked_files=$CHECKED_FILES)"
        pass=$((pass + 1))
    else
        echo "  FAIL: F_LF_03 expected exit 0, got 2 (violations=$VIOLATIONS_COUNT)"
        echo "$VIOLATIONS_LIST"
        fail=$((fail + 1))
    fi
    rm -f "$sandbox/eeg/_lf03_fixture.hexa"

    echo "=== selftest summary: PASS=$pass FAIL=$fail ==="
    # Emit a synthetic marker so CI has evidence
    if [[ "$fail" -eq 0 ]]; then
        emit_marker_and_ledger 0 "$pass" 0 license_firewall_selftest >/dev/null
        rm -rf "$sandbox"
        return 0
    else
        emit_marker_and_ledger 2 "$pass" "$fail" license_firewall_selftest >/dev/null
        rm -rf "$sandbox"
        return 2
    fi
}

# ── Arg parse ────────────────────────────────────────────────────────────
case "${1:-}" in
    -h|--help|help)
        print_help
        exit 0
        ;;
    --selftest)
        run_selftest
        exit $?
        ;;
    "")
        : # default scan
        ;;
    *)
        echo "Unknown flag: $1" >&2
        print_help >&2
        exit 1
        ;;
esac

# ── Default: real scan ───────────────────────────────────────────────────
scan_tree ""
RC=$?

if [[ "$RC" -eq 0 ]]; then
    MARKER="$(emit_marker_and_ledger 0 "$CHECKED_FILES" 0)"
    echo "license-check PASS  checked=$CHECKED_FILES violations=0  marker=$MARKER"
    exit 0
else
    MARKER="$(emit_marker_and_ledger 2 "$CHECKED_FILES" "$VIOLATIONS_COUNT")"
    echo "license-check FAIL  checked=$CHECKED_FILES violations=$VIOLATIONS_COUNT  marker=$MARKER" >&2
    printf '%s' "$VIOLATIONS_LIST" >&2
    exit 2
fi
