#!/usr/bin/env bash
# tool/h100_idle_guard.bash — H100 idle reclaim wrapper for launchd.
#
# Combines the two pieces previously left separate:
#   1) refresh pod registry (h100_pods_sync.bash)
#   2) probe + STOP idle pods (h100_auto_kill.hexa --apply)
#
# Why this wrapper exists:
#   - 2026-04-30 incident: a single H100 SXM (r2krrcoosdmccy) sat idle for
#     23h burning credits. Root cause was a 3-way gap:
#       a) launchd plist invoked hexa with --dry-run (never STOP)
#       b) pods_sync was not chained, so the registry was stale
#       c) hexa-exec on darwin host failed (rc=76) without
#          HEXA_SHIM_NO_DARWIN_LANDING=1
#   - This script closes a/b/c in one call so the launchd job either runs
#     end-to-end or fails loudly.
#
# Exit codes:
#   0 sync + auto-kill both succeeded
#   1 sync failed (pod registry not refreshed; auto-kill skipped)
#   2 auto-kill failed (pods registry was refreshed; STOP path may be partial)

set -u
set -o pipefail

ROOT="/Users/ghost/core/anima"
HEXA="/Users/ghost/core/hexa-lang/hexa"
SYNC="${ROOT}/tool/h100_pods_sync.bash"
KILL="${ROOT}/tool/h100_auto_kill.hexa"

export HEXA_SHIM_NO_DARWIN_LANDING=1
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:${PATH:-}"

ts() { date -u +%Y-%m-%dT%H:%M:%SZ; }

echo "── h100_idle_guard $(ts) ──"

if ! bash "${SYNC}"; then
    echo "h100_idle_guard: pods_sync FAILED — skipping auto-kill"
    exit 1
fi

if ! "${HEXA}" run "${KILL}" --apply; then
    echo "h100_idle_guard: auto-kill FAILED"
    exit 2
fi

echo "── h100_idle_guard $(ts) done ──"
exit 0
