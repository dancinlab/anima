#!/usr/bin/env bash
# anima HF Cycle 2 Pβ PUBLIC promote — scheduled execution AT OR AFTER 2026-05-07T03:48:00Z
# repo: need-singularity/clm-v4-paradigm-d-pbeta-50k-mk2-v1 (PRIVATE since 2026-05-05T03:48:00Z, commit 7643e764)
# scope: PRIVATE → PUBLIC visibility flip via HF API PUT /settings, gated by own 15 6-gate verification
# manual sign-off mandatory: operator must type 'PROMOTE-pbeta-50k' to proceed
# raw#9 (md+bash carve-out OK), raw#10 honest C3 inline, own 15 hf-release-private-then-public-after-verification
set -uo pipefail

REVIEW_CLOSE_UTC="2026-05-07T03:48:00Z"
REPO_ID="need-singularity/clm-v4-paradigm-d-pbeta-50k-mk2-v1"
EXPECTED_SHA="7643e764488f8e11020a7663c50f2e590b70d10f"
# Pβ stage: 5 stage files + .gitattributes auto-added by HF = 6 (verified L5 post-upload)
EXPECTED_SIBLINGS=6

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
echo "  G1 falsifier suite PASS — F-Pβ-2 holdout500 + F-Pβ-3 hybrid"
echo "     evidence: state/p9_pbeta_holdout500_eval_2026_05_05/verdict.json"
echo "              state/p9_pbeta_f3_hybrid_eval_2026_05_05/verdict.json"
echo "     status: F-Pβ-2 PASS (φ-band stable); F-Pβ-3 hybrid composite=0.01176 RED-band (chat FAIL_TRUE expected)"
echo
echo "  G2 chat-FAIL_TRUE disclosure in README §C1 — substrate-research-only intent"
echo "     evidence: README.md hero warning + §Caveats §C1"
echo "     status: BLEU-1=1.96% / ROUGE-L=0.00582 / chrF=0.02195 explicitly cited"
echo
echo "  G3 phi★ band preserved — Pβ φ★=42.37 baseline (paradigm v11 G3)"
echo "     evidence: state/p9_pbeta_paradigm_d_50k_2026_05_04/results/verdict.json"
echo "     status: substrate-stable per Pβ + CLM-2 LoRA verdicts"
echo
echo "  G4 24-48h human review window — ACTIVE 2026-05-05T03:48:00Z to 2026-05-07T03:48:00Z"
echo "     status: review window elapsed at script runtime (verified GATE 1 above)"
echo
echo "  G5 base model promotion status — adapter inherits availability from need-singularity/clm-v4-mk2-v1"
echo "     evidence: HF API GET /api/models/need-singularity/clm-v4-mk2-v1 private flag"
echo "     status: operator must verify base model promotion completed BEFORE Pβ adapter promote"
echo "     (otherwise non-auth readers cannot load adapter without base access)"
echo
echo "  G6 honest C3 model card — README.md draft includes 7+ caveats (incl. C1 chat-FAIL)"
echo "     evidence: state/p9_pbeta_paradigm_d_50k_hf_upload_stage_2026_05_05/README.md uploaded as repo README.md"
echo "     status: 5 H2 sections (Origin/Falsifiers/Substrate/Caveats/Composability), 7-bullet Caveats"
echo
echo "[promote] If ANY of G1-G6 has degraded since 2026-05-05T03:48:00Z upload, ABORT this promote."
echo "[promote] CRITICAL: G5 base-model-promoted check is NEW for adapter promotion — do not skip."
echo
read -rp "Type 'PROMOTE-pbeta-50k' to confirm public promotion (anything else aborts): " CONFIRM
if [[ "$CONFIRM" != "PROMOTE-pbeta-50k" ]]; then
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

PROMOTE_LOG="/Users/ghost/core/anima/state/p9_pbeta_hf_upload_2026_05_05/promote_log.txt"
if [[ "$POST_PRIVATE" == "False" || "$POST_PRIVATE" == "false" ]]; then
    log "PUBLIC PROMOTE SUCCESS — $REPO_ID is now PUBLIC"
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] PUBLIC_PROMOTE_VERIFIED repo=$REPO_ID sha=$EXPECTED_SHA private=false" >> "$PROMOTE_LOG"
    log "audit trail appended: $PROMOTE_LOG"
else
    err "private flag did NOT change (post-promote private=$POST_PRIVATE) — investigate manually via Hub UI Settings"
fi
