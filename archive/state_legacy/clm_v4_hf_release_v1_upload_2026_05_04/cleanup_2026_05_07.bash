#!/usr/bin/env bash
# anima HF Cycle 2 cleanup — scheduled execution date 2026-05-07 (post 48h review window close)
# scope: ubu1 staging dir /home/aiden/anima_clm_release_v1_staging (~7GB) + (optional) mac stage mirror
# gates: 2-gate verify before any rm; verb=DELETE_SCRIPT per feedback_cleanup_bg_guards.md
# REPO context: https://huggingface.co/need-singularity/clm-v4-mk2-v1 (private at v1; promote-public is separate)

set -euo pipefail
shopt -s failglob 2>/dev/null || true

CYCLE="clm_v4_hf_release_v1_upload_2026_05_04"
REPO_ID="need-singularity/clm-v4-mk2-v1"
COMMIT_SHA="80440a1d38db9addc4445bb959057558a57f4230"
EXPECTED_SIBLINGS=16
UBU1_STAGE="/home/aiden/anima_clm_release_v1_staging"
MAC_STAGE_MIRROR="state/clm_v4_hf_release_v1_upload_stage_2026_05_04"
REVIEW_WINDOW_ENDS_48H_UTC="2026-05-06T23:26:12Z"

err()  { printf '[cleanup ERR] %s\n' "$*" >&2; exit 1; }
log()  { printf '[cleanup    ] %s\n' "$*"; }
warn() { printf '[cleanup WRN] %s\n' "$*" >&2; }

# ============================================================================
# GATE 1 — review window has elapsed (48h post upload)
# ============================================================================
NOW_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
log "GATE 1 review window check: now=$NOW_UTC ends=$REVIEW_WINDOW_ENDS_48H_UTC"
if [[ "$NOW_UTC" < "$REVIEW_WINDOW_ENDS_48H_UTC" ]]; then
  err "GATE 1 FAIL: review window not yet elapsed (now $NOW_UTC < ends $REVIEW_WINDOW_ENDS_48H_UTC); abort"
fi
log "GATE 1 PASS"

# ============================================================================
# GATE 2 — HF repo intact (siblings == 15, commit_sha matches)
# ============================================================================
log "GATE 2 HF repo intact check: $REPO_ID"

if ! command -v secret >/dev/null 2>&1; then
  err "GATE 2 FAIL: 'secret' CLI not on PATH; cannot fetch HF token (expected /Users/ghost/core/secret/bin/secret)"
fi

HF_TOKEN="$(secret get huggingface.token --raw 2>/dev/null || true)"
if [[ -z "$HF_TOKEN" ]]; then
  err "GATE 2 FAIL: HF token not retrievable from secret CLI"
fi

API_JSON="$(curl -sS -H "Authorization: Bearer $HF_TOKEN" \
  "https://huggingface.co/api/models/$REPO_ID" || true)"
if [[ -z "$API_JSON" ]]; then
  err "GATE 2 FAIL: HF API returned empty response for $REPO_ID"
fi

# parse with python3 (jq may not be present on mac); minimal stdlib
PY_PARSE="$(/usr/bin/env python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
sib = d.get('siblings', [])
sha = d.get('sha', '')
print(f'siblings_count={len(sib)}')
print(f'commit_sha={sha}')
print(f'private={d.get(\"private\", False)}')
" <<<"$API_JSON")"

log "$PY_PARSE"

SIBLINGS_COUNT="$(grep '^siblings_count=' <<<"$PY_PARSE" | cut -d= -f2)"
REPO_SHA="$(grep '^commit_sha=' <<<"$PY_PARSE" | cut -d= -f2)"

if [[ "$SIBLINGS_COUNT" != "$EXPECTED_SIBLINGS" ]]; then
  err "GATE 2 FAIL: siblings_count=$SIBLINGS_COUNT != expected $EXPECTED_SIBLINGS"
fi
if [[ "$REPO_SHA" != "$COMMIT_SHA" ]]; then
  warn "GATE 2 WARN: repo HEAD sha=$REPO_SHA != upload-time sha=$COMMIT_SHA — repo may have been re-pushed; review before delete"
  err "GATE 2 FAIL: commit sha mismatch (manual review required)"
fi
log "GATE 2 PASS (siblings=$SIBLINGS_COUNT sha=$REPO_SHA)"

# ============================================================================
# CLEANUP — verb=DELETE_SCRIPT (record pre-state, delete, verify post-state)
# ============================================================================
PRE_REPORT="state/$CYCLE/cleanup_pre_state_$(date -u +%Y%m%dT%H%M%SZ).txt"
mkdir -p "$(dirname "$PRE_REPORT")"

log "CLEANUP-A ubu1 staging dir: $UBU1_STAGE"
{
  echo "# pre-cleanup state $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## ubu1 staging:"
  ssh ubu1 "test -d $UBU1_STAGE && du -sh $UBU1_STAGE && ls -la $UBU1_STAGE | head -30 || echo 'NOT_PRESENT'" 2>&1 || true
  echo
  echo "## mac stage mirror:"
  test -d "$MAC_STAGE_MIRROR" && du -sh "$MAC_STAGE_MIRROR" && ls -la "$MAC_STAGE_MIRROR" || echo 'NOT_PRESENT'
} > "$PRE_REPORT"
log "pre-state recorded: $PRE_REPORT"

# ubu1 delete
if ssh ubu1 "test -d $UBU1_STAGE" 2>/dev/null; then
  log "deleting ubu1:$UBU1_STAGE ..."
  ssh ubu1 "rm -rf $UBU1_STAGE"
  if ssh ubu1 "test -d $UBU1_STAGE" 2>/dev/null; then
    err "CLEANUP-A FAIL: ubu1:$UBU1_STAGE still present after rm"
  fi
  log "CLEANUP-A PASS (ubu1 stage deleted + post-verify NOT_PRESENT)"
else
  log "CLEANUP-A SKIP (ubu1:$UBU1_STAGE already absent)"
fi

# mac stage mirror — small (3 files), keep by default; flag --delete-mac-mirror to remove
if [[ "${1:-}" == "--delete-mac-mirror" ]]; then
  log "CLEANUP-B mac mirror: $MAC_STAGE_MIRROR (--delete-mac-mirror flag set)"
  if [[ -d "$MAC_STAGE_MIRROR" ]]; then
    rm -rf "$MAC_STAGE_MIRROR"
    [[ -d "$MAC_STAGE_MIRROR" ]] && err "CLEANUP-B FAIL: mac mirror still present"
    log "CLEANUP-B PASS"
  else
    log "CLEANUP-B SKIP (already absent)"
  fi
else
  log "CLEANUP-B SKIP (mac mirror retained; pass --delete-mac-mirror to remove)"
fi

# ============================================================================
# POST-STATE
# ============================================================================
POST_REPORT="state/$CYCLE/cleanup_post_state_$(date -u +%Y%m%dT%H%M%SZ).txt"
{
  echo "# post-cleanup state $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## ubu1 staging:"
  ssh ubu1 "test -d $UBU1_STAGE && echo 'STILL_PRESENT' || echo 'DELETED_OK'" 2>&1 || true
  echo
  echo "## mac stage mirror:"
  test -d "$MAC_STAGE_MIRROR" && echo 'STILL_PRESENT' || echo 'ABSENT_OR_DELETED'
} > "$POST_REPORT"
log "post-state recorded: $POST_REPORT"

log "DONE — HF Cycle 2 cleanup complete; reports at state/$CYCLE/cleanup_{pre,post}_state_*.txt"
