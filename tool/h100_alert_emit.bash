#!/usr/bin/env bash
# tool/h100_alert_emit.bash — pure-bash alert emitter for h100_cost_watchdog
#
# Used as the watchdog's --alert-script. Pure bash (NOT hexa) per spec C4 to
# avoid recursive Anthropic 429 cascade — if hexa or the parent agent is
# rate-limited, the alert sink must still be runnable.
#
# Inputs (positional):
#   $1 = ALERT_TYPE   (STALE_HEARTBEAT | COST_OVERRUN_2X | COST_OVERRUN_3X_AUTOPAUSE | ...)
#   $2 = POD_ID
#   $3 = DETAILS     (free-form k=v string)
#
# Side effects:
#   - prints "[h100-alert <ts>] <TYPE> pod=<id> <details>" to stderr
#   - appends one JSON row to state/h100_alert_ledger_<YYYY_MM>.jsonl
#
# Exit codes:
#   0  ok (alert emitted to stderr + ledger)
#   1  ledger write failed
#
# Future wiring: push notification channel (anima notifier) — TODO marker
# below; ledger-only this cycle.

set -uo pipefail

ALERT_TYPE="${1:-unknown}"
POD_ID="${2:-unknown}"
DETAILS="${3:-}"
TS=$(date -u +%FT%TZ)

# stderr line (line-oriented so launchd/supervisord can grep)
echo "[h100-alert ${TS}] ${ALERT_TYPE} pod=${POD_ID} ${DETAILS}" >&2

# Ledger append
LEDGER_DIR="/Users/ghost/core/anima/state"
LEDGER="${LEDGER_DIR}/h100_alert_ledger_$(date -u +%Y_%m).jsonl"
mkdir -p "${LEDGER_DIR}" || exit 1

# Use jq if present (preferred — escapes correctly); else hand-roll a row.
if command -v jq >/dev/null 2>&1; then
    if ! jq -nc \
        --arg ts "${TS}" \
        --arg type "${ALERT_TYPE}" \
        --arg pod "${POD_ID}" \
        --arg details "${DETAILS}" \
        '{ts: $ts, type: $type, pod: $pod, details: $details}' >> "${LEDGER}"; then
        echo "[h100-alert ${TS}] ledger-write-failed via jq" >&2
        exit 1
    fi
else
    # naive fallback — escape backslashes + double quotes
    esc_details="${DETAILS//\\/\\\\}"
    esc_details="${esc_details//\"/\\\"}"
    if ! printf '{"ts":"%s","type":"%s","pod":"%s","details":"%s"}\n' \
        "${TS}" "${ALERT_TYPE}" "${POD_ID}" "${esc_details}" >> "${LEDGER}"; then
        echo "[h100-alert ${TS}] ledger-write-failed via printf" >&2
        exit 1
    fi
fi

# TODO(phase 2+): push notification wire (anima notifier) — currently ledger-only.

exit 0
