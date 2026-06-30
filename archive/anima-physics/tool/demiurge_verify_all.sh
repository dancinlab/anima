#!/usr/bin/env bash
# demiurge_verify_all.sh — batch dispatch `demiurge cli action verify <domain>`
#                          across 15 domains in parallel and aggregate the result.
#
# Usage:
#   ./demiurge_verify_all.sh              # human-readable table (default)
#   ./demiurge_verify_all.sh --md         # markdown table
#   ./demiurge_verify_all.sh --json       # JSON
#   ./demiurge_verify_all.sh --raw <dir>  # also save per-domain raw stdout/stderr
#
# Aggregates: gate_state (CLOSED_MEASURED / OPEN / ABSORBED / NONE) +
#             record_id (if any) + exit code.
#
# - 15 domains hard-coded (engineering-relevant subset of demiurge's 20-domain list)
# - parallel via xargs -P 8
# - timeout 120s per domain via `timeout` (gtimeout fallback for macOS coreutils)
# - thread-safety: each xargs worker writes a single line atomically; final
#   aggregation reads the unified file after xargs returns. demiurge CLI
#   writes records into ISO-second-stamped dirs (collision: same wall-second
#   across two domains, surfaced as identical timestamp prefix in raw/).

set -u

DOMAINS=(
  chip
  component
  firmware
  materials
  antimatter
  aura
  bio
  bot
  brain
  cern
  chem
  energy
  fusion
  grid
  mobility
)

# ---- arg parse -------------------------------------------------------------
MODE="table"
RAW_DIR=""
PARALLEL=4   # default — SwiftPM .build lock thrashes above P=4
while [[ $# -gt 0 ]]; do
  case "$1" in
    --md)   MODE="md";   shift ;;
    --json) MODE="json"; shift ;;
    --table) MODE="table"; shift ;;
    --raw)  RAW_DIR="$2"; shift 2 ;;
    -P)     PARALLEL="$2"; shift 2 ;;
    --help|-h)
      sed -n '2,16p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

# ---- timeout binary (macOS may have gtimeout via coreutils) ----------------
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"
if [[ -z "$TIMEOUT_BIN" ]]; then
  echo "WARN: no timeout(1) found — domain dispatch may hang" >&2
  TIMEOUT_BIN=""
fi

# ---- workspace -------------------------------------------------------------
WORK="$(mktemp -d -t demiurge_verify_all.XXXXXX)"
trap 'rm -rf "$WORK"' EXIT
OUT_TXT="$WORK/lines.txt"
: > "$OUT_TXT"

if [[ -n "$RAW_DIR" ]]; then
  mkdir -p "$RAW_DIR"
fi

T0=$(date +%s)

# ---- per-domain worker (exported via env) ----------------------------------
export TIMEOUT_BIN OUT_TXT RAW_DIR

run_one() {
  local d="$1"
  local raw
  local exit_code
  local start
  local elapsed
  start=$(date +%s)
  if [[ -n "$TIMEOUT_BIN" ]]; then
    raw=$("$TIMEOUT_BIN" 120 demiurge cli action verify "$d" 2>&1)
  else
    raw=$(demiurge cli action verify "$d" 2>&1)
  fi
  exit_code=$?
  elapsed=$(( $(date +%s) - start ))

  if [[ -n "$RAW_DIR" ]]; then
    printf '%s\n' "$raw" > "$RAW_DIR/${d}.log"
  fi

  # extract gate_state — pattern set: GATE_CLOSED_MEASURED, GATE_OPEN, GATE_ABSORBED
  local gate
  gate=$(printf '%s\n' "$raw" | grep -oE 'GATE_(CLOSED_MEASURED|OPEN|ABSORBED)' | head -1)
  [[ -z "$gate" ]] && gate="NONE"

  # extract record id — patterns:
  #   📸 new record ID(s): sB_mesh88_uniform_22nm, sD_mesh_d4_tornado_22nm
  #   "record_id":"foo"
  local rec
  rec=$(printf '%s\n' "$raw" | grep -E 'new record ID\(s\):' | head -1 | sed -E 's/.*new record ID\(s\):[[:space:]]*//' | tr -d '\r')
  if [[ -z "$rec" ]]; then
    rec=$(printf '%s\n' "$raw" | grep -oE '"record_id"[[:space:]]*:[[:space:]]*"[^"]+"' | head -1 | sed -E 's/.*"record_id"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')
  fi
  [[ -z "$rec" ]] && rec="-"

  # crude "engine tool gap" / "no producer" detection — patterns:
  #   ko: "엔진 도구: 없음", "엔진 부재", "verify producer.*미작성", "엔진이 없습니다"
  #   en: "no producer", "engine tool gap", "no engine"
  local note=""
  if printf '%s' "$raw" | grep -qE '엔진 도구.*없음|엔진 부재|엔진.*없습니다|no producer|engine tool gap|verify producer.*미작성|skeleton emit'; then
    note="gap"
  fi
  # if gate not found in stdout, try to infer from "no new measured record" / "GATE_OPEN" prose
  if [[ "$gate" == "NONE" ]]; then
    if printf '%s' "$raw" | grep -qE 'no new measured record|gate_state[^_]*OPEN|gate=.*OPEN'; then
      gate="GATE_OPEN"
    fi
  fi
  if [[ -z "$note" && "$gate" == "NONE" ]]; then
    note="unknown"
  fi
  [[ -z "$note" ]] && note="-"

  # atomic single-line append (PIPE-safe; line < 4KB typically)
  printf '%s|%s|%s|%s|%s|%s\n' "$d" "$gate" "$rec" "$exit_code" "${elapsed}s" "$note" >> "$OUT_TXT"
}
export -f run_one

# ---- parallel dispatch -----------------------------------------------------
printf '%s\n' "${DOMAINS[@]}" | xargs -n 1 -P "$PARALLEL" -I {} bash -c 'run_one "$@"' _ {}

WALL=$(( $(date +%s) - T0 ))

# ---- sort by canonical domain order ----------------------------------------
SORTED="$WORK/sorted.txt"
: > "$SORTED"
for d in "${DOMAINS[@]}"; do
  grep -E "^${d}\|" "$OUT_TXT" >> "$SORTED" || \
    printf '%s|NONE|-|-|-|missing\n' "$d" >> "$SORTED"
done

# ---- aggregate counts ------------------------------------------------------
N_TOTAL=${#DOMAINS[@]}
N_CLOSED=$(awk -F'|' '$2=="GATE_CLOSED_MEASURED"' "$SORTED" | wc -l | tr -d ' ')
N_ABSORBED=$(awk -F'|' '$2=="GATE_ABSORBED"' "$SORTED" | wc -l | tr -d ' ')
N_OPEN=$(awk -F'|' '$2=="GATE_OPEN"' "$SORTED" | wc -l | tr -d ' ')
N_GAP=$(awk -F'|' '$6=="gap"' "$SORTED" | wc -l | tr -d ' ')
N_NONE=$(awk -F'|' '$2=="NONE"' "$SORTED" | wc -l | tr -d ' ')

# ---- render ----------------------------------------------------------------
case "$MODE" in
  md)
    echo "| Domain | Gate | Record ID | Exit | Wall | Note |"
    echo "|---|---|---|---|---|---|"
    while IFS='|' read -r d g r e w n; do
      printf '| %s | %s | %s | %s | %s | %s |\n' "$d" "$g" "$r" "$e" "$w" "$n"
    done < "$SORTED"
    echo ""
    echo "**aggregate:** ${N_CLOSED} CLOSED_MEASURED · ${N_ABSORBED} ABSORBED · ${N_OPEN} OPEN · ${N_NONE} NONE · ${N_GAP} engine-gap · wall ${WALL}s (parallel P=${PARALLEL}, ${N_TOTAL} domains)"
    ;;

  json)
    printf '{\n'
    printf '  "wall_seconds": %s,\n' "$WALL"
    printf '  "parallelism": %s,\n' "$PARALLEL"
    printf '  "n_domains": %s,\n' "$N_TOTAL"
    printf '  "aggregate": {\n'
    printf '    "closed_measured": %s,\n' "$N_CLOSED"
    printf '    "absorbed": %s,\n' "$N_ABSORBED"
    printf '    "open": %s,\n' "$N_OPEN"
    printf '    "none": %s,\n' "$N_NONE"
    printf '    "gap": %s\n' "$N_GAP"
    printf '  },\n'
    printf '  "rows": [\n'
    first=1
    while IFS='|' read -r d g r e w n; do
      [[ $first -eq 0 ]] && printf ',\n'
      first=0
      rec_json=$(printf '%s' "$r" | sed 's/"/\\"/g')
      printf '    {"domain":"%s","gate":"%s","record_id":"%s","exit":"%s","wall":"%s","note":"%s"}' \
        "$d" "$g" "$rec_json" "$e" "$w" "$n"
    done < "$SORTED"
    printf '\n  ]\n}\n'
    ;;

  table|*)
    printf '%-12s %-22s %-50s %-6s %-6s %-8s\n' Domain Gate "Record ID" Exit Wall Note
    printf '%-12s %-22s %-50s %-6s %-6s %-8s\n' "------" "----" "---------" "----" "----" "----"
    while IFS='|' read -r d g r e w n; do
      rt="$r"
      if [[ ${#rt} -gt 48 ]]; then rt="${rt:0:45}..."; fi
      printf '%-12s %-22s %-50s %-6s %-6s %-8s\n' "$d" "$g" "$rt" "$e" "$w" "$n"
    done < "$SORTED"
    echo ""
    echo "=== aggregate ==="
    echo "  CLOSED_MEASURED: ${N_CLOSED}"
    echo "  ABSORBED:        ${N_ABSORBED}"
    echo "  OPEN:            ${N_OPEN}"
    echo "  NONE:            ${N_NONE}"
    echo "  engine-gap note: ${N_GAP}"
    echo "  wall:            ${WALL}s  (parallel P=${PARALLEL}, ${N_TOTAL} domains)"
    ;;
esac
