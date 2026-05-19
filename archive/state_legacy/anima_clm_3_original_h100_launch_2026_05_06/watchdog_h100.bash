#!/usr/bin/env bash
# beta H100 watchdog (BG-EU, own 16)
# 5min heartbeat + pod 404 verify + cumulative spend tracking
# L23 (rate-limit recovery) + L24 (BG-done vs pod-down) + L25 (cost escalation)
# bash 3.2 compatible
set -uo pipefail

POD_NAME="${1:-}"
[ -z "$POD_NAME" ] && { echo "usage: $0 <pod_name>" >&2; exit 1; }

STATE_DIR="/Users/ghost/core/anima/state/anima_clm_3_original_h100_launch_2026_05_06"
HEART="$STATE_DIR/watchdog_heartbeat.log"
LEDGER="$STATE_DIR/watchdog_spend.jsonl"
BUDGET_CAP_USD=100
H100_RATE_PER_HR=2.49  # NVIDIA H100 80GB HBM3 RunPod community list

mkdir -p "$STATE_DIR"
START_TS=$(date +%s)

log() { printf '[wd %s] %s\n' "$(date -u +%H:%M:%S)" "$*" | tee -a "$HEART"; }

log "watchdog START pod=$POD_NAME cap=\$$BUDGET_CAP_USD rate=\$$H100_RATE_PER_HR/hr"

while true; do
    NOW=$(date +%s)
    ELAPSED_S=$(( NOW - START_TS ))
    # bash 3.2: integer-only arith for cents
    SPEND_CENTS=$(( ELAPSED_S * 249 / 3600 ))   # 2.49/hr in cents
    CAP_CENTS=$(( BUDGET_CAP_USD * 100 ))

    # L24: pod state probe (404 = pod terminated; not necessarily failure)
    POD_STATE="$(runpod pod get "$POD_NAME" 2>&1 || true)"
    case "$POD_STATE" in
        *"not found"*|*"404"*)
            log "L24 pod 404 — terminated (BG-completion or external kill)"
            log "FINAL spend=\$$(( SPEND_CENTS / 100 )).$(printf '%02d' $(( SPEND_CENTS % 100 )))"
            exit 0
            ;;
        *"rate limit"*|*"429"*)
            log "L23 rate-limit — backoff 60s"
            sleep 60
            continue
            ;;
    esac

    # L25 cost overrun escalation
    if [ "$SPEND_CENTS" -ge "$CAP_CENTS" ]; then
        log "L25 COST OVERRUN — spend=\$$(( SPEND_CENTS / 100 )) >= cap=\$$BUDGET_CAP_USD"
        log "L25 ESCALATION — operator must decide stop vs extend"
        echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event\":\"L25_OVERRUN\",\"spend_cents\":$SPEND_CENTS}" >> "$LEDGER"
        # do NOT auto-kill; emit signal only (own 16: human-in-loop)
    fi

    # heartbeat ledger entry
    echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"elapsed_s\":$ELAPSED_S,\"spend_cents\":$SPEND_CENTS,\"pod\":\"$POD_NAME\"}" >> "$LEDGER"
    log "heartbeat elapsed=${ELAPSED_S}s spend=\$$(( SPEND_CENTS / 100 )).$(printf '%02d' $(( SPEND_CENTS % 100 )))"

    sleep 300  # 5min cadence
done
