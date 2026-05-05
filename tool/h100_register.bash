#!/usr/bin/env bash
# tool/h100_register.bash — convenience wrapper invoked by orchestrator hexa
# at boot to register a fresh pod with the cost watchdog.
#
# Usage:
#   bash tool/h100_register.bash <POD_ID> <OWNER> <TARGET_USD>
#
# Calls hexa run tool/h100_cost_watchdog.hexa --register POD_ID OWNER USD.
# Pure-bash carve-out (raw#9 .own opt-out) — kept lightweight so orchestrators
# can register without spawning a full hexa context for the bookkeeping path.

set -uo pipefail

if [[ $# -lt 3 ]]; then
    echo "usage: bash tool/h100_register.bash <POD_ID> <OWNER> <TARGET_USD>" >&2
    exit 2
fi

POD_ID="$1"
OWNER="$2"
TARGET_USD="$3"

ROOT="/Users/ghost/core/anima"
HEXA="/Users/ghost/core/hexa-lang/hexa"
WATCHDOG="${ROOT}/tool/h100_cost_watchdog.hexa"

export HEXA_SHIM_NO_DARWIN_LANDING=1
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

if ! "${HEXA}" run "${WATCHDOG}" --register "${POD_ID}" "${OWNER}" "${TARGET_USD}"; then
    echo "h100_register: watchdog --register failed for pod=${POD_ID}" >&2
    exit 1
fi

echo "[h100-register] $(date -u +%FT%TZ) pod=${POD_ID} owner=${OWNER} target=\$${TARGET_USD}"
exit 0
