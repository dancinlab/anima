#!/usr/bin/env bash
# anima_hf_promotes_2026_05_06_auto_fire.bash
# 2026-05-05 written
#
# Auto-fire HF clm-v4-mk2-v1 + Pβ PUBLIC promotes after review windows.
#
# Mode 1: --check-only (default) - verify both windows + state, no fire
# Mode 2: --fire-clm           - fire clm promote (after manual sign-off prompt)
# Mode 3: --fire-pbeta         - fire Pβ promote (clm public 후)
# Mode 4: --fire-all           - fire both sequentially with sign-off
#
# Review windows:
#   clm-v4-mk2-v1: ends 2026-05-06T23:26:12Z
#   pbeta: ends 2026-05-07T03:48:00Z
#
# own 15 6 gates verification (G1-G6) + F-SHIM-V4-4 RETIRE (G3 carve-out):
#   G1 benchmark: random-floor band (substrate-research artifact disclosed)
#   G2 falsifier: F-SHIM-V4-1/2/3 PASS + V4-4 RETIRED (3-path closure)
#   G3 shim compat carve-out: PASS_WITH_CARVE_OUT
#   G4 24-48h review: time-gated below
#   G5 honest C3 model card: README chat-incapability + 2-cycle empirical FAIL
#   G6 cross-substrate: Pβ φ★ + CLM-2 LoRA forgetting + φ★ NO_FLIP

set -uo pipefail

MODE="${1:---check-only}"
REPO_ROOT="/Users/ghost/core/anima"
CLM_SCRIPT="$REPO_ROOT/state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash"
PBETA_SCRIPT="$REPO_ROOT/state/p9_pbeta_hf_upload_2026_05_05/public_promote_pbeta_2026_05_08.bash"

CLM_WINDOW_END="2026-05-06T23:26:12Z"
PBETA_WINDOW_END="2026-05-07T03:48:00Z"

NOW_UTC=$(date -u +%FT%TZ)

echo "==============================="
echo "  anima HF promote auto-fire"
echo "==============================="
echo "Now UTC:               $NOW_UTC"
echo "clm window ends:       $CLM_WINDOW_END"
echo "pbeta window ends:     $PBETA_WINDOW_END"

clm_fire_able="NO"
pbeta_fire_able="NO"
[[ "$NOW_UTC" > "$CLM_WINDOW_END" ]] && clm_fire_able="YES"
[[ "$NOW_UTC" > "$PBETA_WINDOW_END" ]] && pbeta_fire_able="YES"

echo "clm fire-able now:     $clm_fire_able"
echo "pbeta fire-able now:   $pbeta_fire_able"
echo "==============================="

if [[ ! -x "$CLM_SCRIPT" ]]; then
  echo "ERROR: clm script not executable: $CLM_SCRIPT"
  exit 2
fi
if [[ ! -x "$PBETA_SCRIPT" ]]; then
  echo "ERROR: pbeta script not executable: $PBETA_SCRIPT"
  exit 2
fi

case "$MODE" in
  --check-only)
    echo
    echo "Mode: check-only. NO fire."
    echo
    echo "=== clm cleanup dry-run (head -10) ==="
    bash "$CLM_SCRIPT" 2>&1 | head -10
    echo
    echo "=== pbeta promote dry-run (head -10) ==="
    bash "$PBETA_SCRIPT" 2>&1 | head -10
    ;;
  --fire-clm)
    if [[ "$clm_fire_able" != "YES" ]]; then
      echo "ABORT: clm review window not yet elapsed."
      exit 1
    fi
    echo "Mode: fire-clm. Manual sign-off required by promote script."
    bash "$CLM_SCRIPT"
    ;;
  --fire-pbeta)
    if [[ "$pbeta_fire_able" != "YES" ]]; then
      echo "ABORT: pbeta review window not yet elapsed."
      exit 1
    fi
    echo "Mode: fire-pbeta. Manual sign-off required."
    echo "NOTE: pbeta promote requires clm-v4-mk2-v1 already public (PEFT base)."
    bash "$PBETA_SCRIPT"
    ;;
  --fire-all)
    if [[ "$clm_fire_able" != "YES" ]] || [[ "$pbeta_fire_able" != "YES" ]]; then
      echo "ABORT: one or both review windows not yet elapsed."
      exit 1
    fi
    echo "Mode: fire-all. Sequential clm -> pbeta with sign-off prompts."
    bash "$CLM_SCRIPT" || { echo "clm promote failed, aborting pbeta"; exit 1; }
    sleep 5
    bash "$PBETA_SCRIPT"
    ;;
  *)
    echo "Usage: $0 [--check-only | --fire-clm | --fire-pbeta | --fire-all]"
    exit 2
    ;;
esac
