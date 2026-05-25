#!/usr/bin/env bash
# _resolve_anu_key.sh — try ANU API key resolution via secret CLI.
#
# Source this script (don't exec) so exported env reaches the parent shell.
# Sets these env vars when keys are found:
#   NEXUS_QMIRROR_ANU_KEY          (T1.b direct keyed,    free 100 req/min)
#   AWS_MARKETPLACE_ANU_API_KEY    (T1.c paid,            $0.005/req)
#   AWS_MARKETPLACE_ANU_TRIAL_KEY  (T1.d trial,           free 1 req/sec)
#
# When all keys are absent (default for most users), entropy_pull's 4-tier
# chain falls through to T1.a legacy (qrng.anu.edu.au, keyless, 1 req/min)
# automatically — no error. qrng_bits's inline path falls to mock_lcg.
#
# Canonical secret key names (try in order; first hit wins per tier):
#   T1.c:  qmirror.anu_aws_paid_key   |  AWS_MARKETPLACE_ANU_API_KEY (env)
#   T1.d:  qmirror.anu_aws_trial_key  |  AWS_MARKETPLACE_ANU_TRIAL_KEY (env)
#   T1.b:  qmirror.anu_api_key  |  anu.api_key  |  NEXUS_QMIRROR_ANU_KEY (env)

SECRET_BIN="${SECRET_BIN:-/Users/ghost/core/secret/bin/secret}"

# helper: try secret get for several key names; first hit wins.
_try_secret() {
    local var_name="$1"
    shift
    # Skip if already set in env.
    if [[ -n "${!var_name:-}" ]]; then
        return 0
    fi
    if [[ ! -x "$SECRET_BIN" ]]; then
        return 1
    fi
    local k
    for k in "$@"; do
        if "$SECRET_BIN" check "$k" 2>/dev/null; then
            local v
            v="$("$SECRET_BIN" get "$k" 2>/dev/null)"
            if [[ -n "$v" ]]; then
                export "$var_name"="$v"
                echo "[anu-resolve] $var_name <- secret/$k" >&2
                return 0
            fi
        fi
    done
    return 1
}

# T1.c paid (AWS Marketplace) — `|| true` so set -e callers stay alive.
_try_secret AWS_MARKETPLACE_ANU_API_KEY    qmirror.anu_aws_paid_key  || true
# T1.d trial (AWS Marketplace)
_try_secret AWS_MARKETPLACE_ANU_TRIAL_KEY  qmirror.anu_aws_trial_key || true
# T1.b direct keyed (api.quantumnumbers.anu.edu.au)
_try_secret NEXUS_QMIRROR_ANU_KEY          qmirror.anu_api_key  anu.api_key || true

# Summary line for transparency (no key contents, just which tiers are armed).
_armed=()
[[ -n "${AWS_MARKETPLACE_ANU_API_KEY:-}" ]]   && _armed+=("T1.c-paid")
[[ -n "${AWS_MARKETPLACE_ANU_TRIAL_KEY:-}" ]] && _armed+=("T1.d-trial")
[[ -n "${NEXUS_QMIRROR_ANU_KEY:-}" ]]         && _armed+=("T1.b-direct")
_armed+=("T1.a-legacy(always)")
echo "[anu-resolve] tiers armed: ${_armed[*]}" >&2
unset _armed _try_secret
