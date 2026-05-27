#!/usr/bin/env bash
# anima HF Cycle 2 PUBLIC promote — scheduled execution AT OR AFTER 2026-05-06T23:26:12Z
# repo: need-singularity/clm-v4-mk2-v1 (PRIVATE since 2026-05-04T23:26:12Z, commit 80440a1d)
# scope: PRIVATE → PUBLIC visibility flip via HF API PUT /settings, gated by own 15 6-gate verification
# manual sign-off mandatory: operator must type 'PROMOTE-clm-v4-mk2-v1' to proceed
# raw#9 (md+bash carve-out OK), raw#10 honest C3 inline, own 15 hf-release-private-then-public-after-verification
set -uo pipefail

REVIEW_CLOSE_UTC="2026-05-06T23:26:12Z"
REPO_ID="need-singularity/clm-v4-mk2-v1"
EXPECTED_SHA="80440a1d38db9addc4445bb959057558a57f4230"
# verdict.json L5_post_upload_verification_pass had siblings_count=15 (off-by-one bug)
# but its enumerated siblings list contained 16 entries. Actual HF API returns 16
# (verified by BG-HF-CYCLE-2-CLEANUP-DRY-RUN 2026-05-05). Both cleanup + promote
# scripts now use 16 = ground-truth. The verdict count field is stale.
EXPECTED_SIBLINGS=16

err()  { printf '[promote ERR] %s\n' "$*" >&2; exit 1; }
log()  { printf '[promote    ] %s\n' "$*"; }
warn() { printf '[promote WRN] %s\n' "$*" >&2; }

NOW_UTC="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
log "starting public promote pre-check at $NOW_UTC"

# ============================================================================
# GATE 1 — review window has elapsed (48h post upload)
# ============================================================================
if [[ "$NOW_UTC" < "$REVIEW_CLOSE_UTC" ]]; then
    err "GATE 1 FAIL: review window not yet elapsed (now $NOW_UTC < ends $REVIEW_CLOSE_UTC)"
fi
log "GATE 1 PASS (review window elapsed: $NOW_UTC >= $REVIEW_CLOSE_UTC)"

# ============================================================================
# GATE 2 — HF Hub state intact (not silently mutated during review window)
# ============================================================================
if ! command -v secret >/dev/null 2>&1; then
    err "GATE 2 FAIL: 'secret' CLI not on PATH (expected /Users/ghost/core/secret/bin/secret)"
fi

TOKEN="$(secret get huggingface.token --raw 2>/dev/null || true)"
if [[ -z "$TOKEN" ]]; then
    err "GATE 2 FAIL: HF token empty from secret CLI"
fi
if [[ "$TOKEN" != hf_* ]]; then
    err "GATE 2 FAIL: token shape unexpected (not hf_* prefix; redacted=${TOKEN:0:3}...)"
fi

HF_STATE="$(curl -sS -H "Authorization: Bearer $TOKEN" \
    "https://huggingface.co/api/models/$REPO_ID" || true)"
if [[ -z "$HF_STATE" ]]; then
    err "GATE 2 FAIL: HF API returned empty response for $REPO_ID"
fi

# parse with python3 (jq may not be present on mac); minimal stdlib
PY_PARSE="$(/usr/bin/env python3 -c "
import json, sys
d = json.loads(sys.stdin.read())
sib = d.get('siblings', [])
print(f'siblings_count={len(sib)}')
print(f'commit_sha={d.get(\"sha\", \"\")}')
print(f'private={d.get(\"private\", False)}')
print(f'gated={d.get(\"gated\", False)}')
" <<<"$HF_STATE")"

log "$PY_PARSE"

ACTUAL_SHA="$(grep '^commit_sha=' <<<"$PY_PARSE" | cut -d= -f2)"
ACTUAL_PRIVATE="$(grep '^private=' <<<"$PY_PARSE" | cut -d= -f2)"
ACTUAL_SIBLINGS="$(grep '^siblings_count=' <<<"$PY_PARSE" | cut -d= -f2)"

if [[ "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
    err "GATE 2 FAIL: sha mismatch (actual=$ACTUAL_SHA expected=$EXPECTED_SHA — repo may have been re-pushed; manual review required)"
fi
if [[ "$ACTUAL_PRIVATE" != "True" && "$ACTUAL_PRIVATE" != "true" ]]; then
    err "GATE 2 FAIL: repo already public (private=$ACTUAL_PRIVATE; race condition or prior promote)"
fi
if [[ "$ACTUAL_SIBLINGS" != "$EXPECTED_SIBLINGS" ]]; then
    warn "GATE 2 WARN: siblings count drift (actual=$ACTUAL_SIBLINGS expected=$EXPECTED_SIBLINGS) — review before promote"
    err "GATE 2 FAIL: siblings count mismatch ($ACTUAL_SIBLINGS vs $EXPECTED_SIBLINGS)"
fi
log "GATE 2 PASS (sha=$ACTUAL_SHA private=$ACTUAL_PRIVATE siblings=$ACTUAL_SIBLINGS)"

# ============================================================================
# GATE 3 — own 15 6-gate verification (manual sign-off required)
# ============================================================================
echo
echo "[promote] Gate 1 (review window) + Gate 2 (HF state intact) PASS."
echo "[promote] own 15 (HF release lifecycle PRIVATE→PUBLIC) requires 6 gates manually re-affirmed:"
echo
echo "  G1 benchmark suite PASS — hellaswag/mmlu/triviaqa/openbookqa"
echo "     evidence: state/clm_v4_baseline_eval_2026_05_05/verdict.json"
echo "     status: CONFIRMED_RANDOM_FLOOR (substrate-research artifact, NOT chat-NLP capability claim)"
echo
echo "  G2 falsifier pre-register satisfied — F-SHIM-V4-1/2/3 PASS"
echo "     evidence: state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_*.json"
echo "     status: F-SHIM-V4-3 PASS bit-exact (max_abs_diff=0.0); F-SHIM-V4-4 DEFERRED to BG-Σ"
echo
echo "  G3 shim v4 hf_format compatibility — F-SHIM-V4-1/2/3 PASS"
echo "     evidence: same as G2; shim v3 logit equivalence confirmed deterministic"
echo
echo "  G4 24-48h human review window — ACTIVE 2026-05-04T23:26:12Z to 2026-05-06T23:26:12Z"
echo "     status: review window elapsed at script runtime (verified GATE 1 above)"
echo
echo "  G5 honest C3 model card — README.md draft includes 5+ caveats (incl. #115 chat-incapability)"
echo "     evidence: docs/anima_clm_hf_release_v1_README_draft.md uploaded as repo README.md"
echo "     status: 5 H2 sections (Origin/Falsifiers/Substrate/Caveats/Composability), 9-bullet Caveats"
echo
echo "  G6 cross-substrate validation — phi★ baseline preserved across substrates"
echo "     evidence: Pβ φ★=42.37 (paradigm v11 G3) + CLM-2 LoRA forgetting_index=0.0196 stable"
echo "     status: substrate-stable per Pβ + CLM-2 LoRA verdicts"
echo
echo "[promote] If ANY of G1-G6 has degraded since 2026-05-04T23:26:12Z upload, ABORT this promote."
echo
read -rp "Type 'PROMOTE-clm-v4-mk2-v1' to confirm public promotion (anything else aborts): " CONFIRM
if [[ "$CONFIRM" != "PROMOTE-clm-v4-mk2-v1" ]]; then
    log "aborted by operator (confirm-string mismatch); repo remains PRIVATE"
    exit 0
fi

# ============================================================================
# PROMOTE — HF API PUT /api/models/<repo>/settings {"private": false}
# ============================================================================
log "executing PUT /api/models/$REPO_ID/settings {\"private\": false}"
RESULT="$(curl -sS -X PUT \
    -H "Authorization: Bearer $TOKEN" \
    -H 'Content-Type: application/json' \
    "https://huggingface.co/api/models/$REPO_ID/settings" \
    -d '{"private": false}' || true)"
log "HF API response: $RESULT"

# ============================================================================
# POST-PROMOTE VERIFICATION
# ============================================================================
sleep 3
POST_STATE="$(curl -sS -H "Authorization: Bearer $TOKEN" \
    "https://huggingface.co/api/models/$REPO_ID" || true)"
POST_PRIVATE="$(/usr/bin/env python3 -c "
import json, sys
d = json.loads(sys.stdin.read() or '{}')
print(d.get('private', 'unknown'))
" <<<"$POST_STATE")"

log "post-promote private flag: $POST_PRIVATE (expect: False/false)"

PROMOTE_LOG="/Users/ghost/core/anima/state/clm_v4_hf_release_v1_upload_2026_05_04/promote_log.txt"
if [[ "$POST_PRIVATE" == "False" || "$POST_PRIVATE" == "false" ]]; then
    log "PUBLIC PROMOTE SUCCESS — $REPO_ID is now PUBLIC"
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] PUBLIC_PROMOTE_VERIFIED repo=$REPO_ID sha=$EXPECTED_SHA private=false" >> "$PROMOTE_LOG"
    log "audit trail appended: $PROMOTE_LOG"
else
    err "private flag did NOT change (post-promote private=$POST_PRIVATE) — investigate manually via Hub UI Settings"
fi
