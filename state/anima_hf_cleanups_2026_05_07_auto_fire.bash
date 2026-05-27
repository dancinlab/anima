#!/usr/bin/env bash
# Auto-fire HF Cycle 2 ubu1 staging cleanup after review windows + PUBLIC promotes.
# Mode: --check-only (default) / --fire-clm / --fire-pbeta / --fire-all
#
# Sequencing recommendation (per BG-HF-CLEANUP-AUTOFIRE-PREP):
#   1. clm PUBLIC promote (after 2026-05-06T23:26:12Z review window close)
#   2. 24h grace (consumer download time)
#   3. clm cleanup     (>= 2026-05-07T23:26:12Z)
#   4. pbeta PUBLIC promote (after 2026-05-07T03:48:00Z)
#   5. 24h grace
#   6. pbeta cleanup   (>= 2026-05-08T03:48:00Z)
#
# Cleanup scripts each contain 2 gates:
#   GATE 1 — review window elapsed (NOW_UTC >= REVIEW_WINDOW_ENDS_48H_UTC)
#   GATE 2 — HF repo intact (siblings count + commit sha match snapshot)
# Failure of either gate aborts before any rm.
#
# Author: 2026-05-05 (BG-HF-CLEANUP-AUTOFIRE-PREP)

set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

MODE="${1:-check-only}"

CLM_CLEANUP="state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash"
PBETA_CLEANUP="state/p9_pbeta_hf_upload_2026_05_05/cleanup_pbeta_2026_05_08.bash"

if [[ ! -f "$CLM_CLEANUP" ]]; then
  printf '[autofire ERR] missing %s\n' "$CLM_CLEANUP" >&2
  exit 2
fi
if [[ ! -f "$PBETA_CLEANUP" ]]; then
  printf '[autofire ERR] missing %s\n' "$PBETA_CLEANUP" >&2
  exit 2
fi

case "$MODE" in
  check-only|--check-only)
    printf '=== clm cleanup dry-run (GATE 1 expected FAIL until 2026-05-06T23:26:12Z) ===\n'
    bash "$CLM_CLEANUP" 2>&1 | head -10
    printf '\n=== pbeta cleanup dry-run (GATE 1 expected FAIL until 2026-05-07T03:48:00Z) ===\n'
    bash "$PBETA_CLEANUP" 2>&1 | head -10
    ;;
  fire-clm|--fire-clm)
    printf '=== firing clm cleanup ===\n'
    bash "$CLM_CLEANUP"
    ;;
  fire-pbeta|--fire-pbeta)
    printf '=== firing pbeta cleanup ===\n'
    bash "$PBETA_CLEANUP"
    ;;
  fire-all|--fire-all)
    printf '=== firing clm cleanup ===\n'
    bash "$CLM_CLEANUP" || { printf '[autofire ERR] clm cleanup failed; aborting pbeta\n' >&2; exit 1; }
    sleep 5
    printf '\n=== firing pbeta cleanup ===\n'
    bash "$PBETA_CLEANUP"
    ;;
  -h|--help|help)
    cat <<EOF
usage: $0 [check-only|fire-clm|fire-pbeta|fire-all]

  check-only  (default) dry-run both cleanups; expect GATE 1 FAIL until review windows close
  fire-clm    run clm cleanup only (after 2026-05-06T23:26:12Z + 24h grace recommended)
  fire-pbeta  run pbeta cleanup only (after 2026-05-07T03:48:00Z + 24h grace recommended)
  fire-all    run clm then pbeta sequentially with 5s spacer; abort pbeta on clm fail
EOF
    ;;
  *)
    printf '[autofire ERR] unknown mode: %s (try --help)\n' "$MODE" >&2
    exit 2
    ;;
esac
