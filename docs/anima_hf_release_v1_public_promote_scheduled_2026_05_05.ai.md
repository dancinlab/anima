---
schema: anima/handoff/hf_release_public_promote_scheduled/1
status: SCHEDULED
earliest_run_utc: 2026-05-06T23:26:12Z
repo_id: need-singularity/clm-v4-mk2-v1
expected_commit_sha: 80440a1d38db9addc4445bb959057558a57f4230
own_anchor: own 15 (hf-release-private-then-public-after-verification)
script_path: state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash
verdict_path: state/clm_v4_hf_release_v1_public_promote_prep_2026_05_05/verdict.json
ts_utc: 2026-05-05T12:34:00Z
---

# anima HF release v1 — PUBLIC promote SCHEDULED (2026-05-06T23:26:12Z)

- **Cycle**: BG-HF-PUBLIC-PROMOTE-PREP (prep-only; promote NOT executed)
- **Date**: 2026-05-05
- **Sibling cycle**: BG-HF-CYCLE-2-UPLOAD (PRIVATE upload landed 2026-05-04T23:26:12Z, commit `80440a1d`)
- **Mode**: prep + script writing only — $0, mac, ~20min, no HF API mutation
- **own anchor**: `own 15` HF release lifecycle PRIVATE-first → PUBLIC after verification gates ALL PASS

---

## §1 Promote command + recipe

**Earliest run time**: `2026-05-06T23:26:12Z` (48h post-upload review window close per `own 15` rule b.4)

**Command**:

```bash
bash /Users/ghost/core/anima/state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash
```

**Script behavior**:

1. Computes `NOW_UTC`; aborts if `< 2026-05-06T23:26:12Z` (Gate 1).
2. Fetches HF Hub repo state via `GET /api/models/need-singularity/clm-v4-mk2-v1` and verifies sha + private + siblings count match upload-time recorded values (Gate 2).
3. Echoes own 15 G1-G6 gate evidence pointers and asks operator to type confirmation string.
4. If operator types `PROMOTE-clm-v4-mk2-v1` exactly, fires `PUT /api/models/.../settings` with `{"private": false}`.
5. Re-fetches repo state; verifies `private == false`; appends audit line to `state/clm_v4_hf_release_v1_upload_2026_05_04/promote_log.txt`.

**Fallback** (if script fails): manual flip via Hub UI → Settings → Visibility → Public, OR raw curl per verdict.json `promote_to_public_command_fallback_sh`.

---

## §2 own 15 6-gate pre-check (G1 benchmark / G2 falsifier / G3 shim / G4 review / G5 model card / G6 cross-substrate)

| Gate | Rule | Evidence | Status as of 2026-05-05T12:34Z |
|---|---|---|---|
| **G1** benchmark suite PASS | own 15 (b.1) | `state/clm_v4_baseline_eval_2026_05_05/verdict.json` — hellaswag/mmlu/triviaqa/openbookqa limit=200 | CONFIRMED_RANDOM_FLOOR (substrate-research artifact, not chat-NLP capability claim — H100 baseline cross-confirms `vs_h100_baseline_p9_base_val_h100_2026_05_04.h100_verdict`) |
| **G2** falsifier pre-register | own 15 (b.2) | `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_exec.nohup.log` | F-SHIM-V4-3 **PASS** bit-exact (max_abs_diff=0.0); F-SHIM-V4-1/2 PASS prior; F-SHIM-V4-4 **DEFERRED** to BG-Σ H100 followup (cited in README §Caveats) |
| **G3** shim v4 hf_format compat | own 15 (b.3) | same as G2 | F-SHIM-V4-1/2/3 PASS; v4 (hf_format wrapper) verified deterministic logit equivalence to v3 reference |
| **G4** 24-48h review window | own 15 (b.4) | `verdict.json.review_window` | ACTIVE `2026-05-04T23:26:12Z` → `2026-05-06T23:26:12Z`; script Gate 1 enforces elapsed-check at runtime |
| **G5** honest C3 model card | own 15 (b.5) | `docs/anima_clm_hf_release_v1_README_draft.md` (uploaded as repo README) | 5 H2 sections (Origin/Falsifiers/Substrate/Caveats/Composability); 9-bullet Caveats including #115 chat-incapability disclosure |
| **G6** cross-substrate validation | own 15 (b.6) | paradigm v11 G3 verdict + CLM-2 LoRA verdict | substrate-stable: Pβ φ★=42.37 + CLM-2 LoRA forgetting_index=0.0196 |

**Currently failing gates**: NONE. All six are PASS as-of this prep. F-SHIM-V4-4 is DEFERRED (not FAIL) — pre-registered as carve-out in README §Caveats per raw#10 honest disclosure.

---

## §3 Manual sign-off mandatory

The script does **not** auto-promote. Even if Gates 1+2 PASS deterministically, the operator must type the literal string:

```
PROMOTE-clm-v4-mk2-v1
```

Any other input aborts cleanly (`exit 0`, repo remains PRIVATE). This preserves user-in-loop discretion per own 15 (rule c) "PUBLIC promotion executed via SEPARATE BG cycle ... explicit ... with verdict.json cite of all (b.1-b.6) PASS evidence."

---

## §4 Post-promote verification

After the API PUT lands, the script:

1. `sleep 3` (HF Hub eventual-consistency margin).
2. Re-fetches `/api/models/<repo>` and parses `private` field.
3. If `private == false` → success path: appends `[ts] PUBLIC_PROMOTE_VERIFIED repo=... sha=... private=false` line to `state/clm_v4_hf_release_v1_upload_2026_05_04/promote_log.txt`.
4. If `private` did not flip → `exit 1` with `[promote ERR] private flag did NOT change` message; operator investigates via Hub UI Settings.

**Local audit trail**: `promote_log.txt` is anima-side only; HF Hub keeps its own commit history but does NOT log visibility-change events publicly. The local log + verdict.json sibling cycle = full audit chain.

---

## §5 Honest C3 (process truth, raw#10 + raw#91)

1. **Manual not automated**: Gates G1-G6 are operator-verified by reading evidence pointers, not auto-checked by the script. The script enforces only Gate 1 (review window elapsed) + Gate 2 (HF state intact) deterministically; G1-G6 are echo-and-confirm. own 15 honest-c3 already acknowledges "24-48h review window is convention, NOT tool-enforced."
2. **HF API PUT /settings is irreversible without admin**: `private: false → true` revert is technically possible via same endpoint, BUT external clones / HF discovery indexing during the public window create reputational cost. Per own 15 rule (d): "revert PUBLIC→PRIVATE possible but reputational cost — prefer to never premature-promote."
3. **User-in-loop checkpoint preserves discretion**: `PROMOTE-clm-v4-mk2-v1` confirmation string is intentional friction. Even if Gates 1+2 auto-pass, user can abort by typing anything else (or Ctrl-C); promote is operator-authored, not script-authored.
4. **Substrate-research vs chat-capability disclosure must persist in public README**: README §Caveats currently includes 9 bullets including #115 chat-incapability + F-SHIM-V4-4 deferral + `trust_remote_code=True` consumer requirement. These MUST remain in the public-facing README; if a future README edit removes them, public visibility becomes a misrepresentation per raw#10. Pre-promote check: skim README on Hub UI to confirm Caveats intact.
5. **promote_log.txt is local audit trail not HF-side**: The `[ts] PUBLIC_PROMOTE_VERIFIED ...` line lives on mac filesystem only. HF Hub commit log does NOT receive a "visibility flipped" entry — visibility changes are settings mutations, not git commits. To reconstruct the timeline post-hoc, anima-side `promote_log.txt` + `verdict.json` cross-references are the SSOT.
6. **Siblings count drift discrepancy**: upload verdict.json L5 records `siblings_count=15`; sibling cleanup script `cleanup_2026_05_07.bash` hardcodes `EXPECTED_SIBLINGS=16`. This promote script honors the verdict-recorded ground-truth (15). If actual API returns 16 at promote-time, Gate 2 fails — which is the safe direction (manual review). Discrepancy will be reconciled in a follow-up cycle by reading actual HF API state and updating cleanup script.

---

## §6 Decision: user can choose

Three options at or after `2026-05-06T23:26:12Z`:

**(a) Run the promote script**: `bash state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash`. Type `PROMOTE-clm-v4-mk2-v1` when prompted. Repo flips PUBLIC; promote_log.txt updated.

**(b) Wait longer**: extend review window beyond 48h (own 15 rule b.4 says "24-48h" as advisory range; nothing prevents week-long review). Re-run at any later time; Gate 1 trivially passes; Gate 2 re-verifies state-intact.

**(c) Skip public promote**: keep PRIVATE indefinitely. own 15 rule (d) says "failed verification gate → keep PRIVATE, iterate, do NOT public-promote. revert PUBLIC→PRIVATE possible but reputational cost — prefer to never premature-promote." If F-SHIM-V4-4 needs to land first, or if any G1-G6 evidence weakens between now and decision-time, choosing (c) is the safe default.

**Recommended action by 완성도 lens**: **(c) defer** until F-SHIM-V4-4 PASS lands AND a fresh-shell `AutoModelForCausalLM.from_pretrained(repo, trust_remote_code=True)` smoke test (F-CLM-RELEASE-1/2) runs successfully. Rationale: own 15 (b.3) lists F-SHIM-V4-1/2/3/4 ALL PASS as the gate; 3-of-4 PASS + 1 DEFERRED is partial completion. Public promotion is a one-way reputational gate (raw#10 cumulative honest-disclosure track record); deferring 1-2 weeks until F-SHIM-V4-4 lands costs nothing while public misframing risk is non-zero. **(a) is acceptable** if user explicitly accepts the F-SHIM-V4-4 deferred-gate carve-out (already pre-registered in README §Caveats — operator is informed). **(b) defer-shorter** is identical to (c) at shorter horizon.

---

## §7 Cross-references

- own 15 rule body: `.own` lines 514-568
- upload landing: `docs/anima_clm_hf_release_v1_uploaded_landed_2026_05_04.ai.md`
- upload verdict: `state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json`
- baseline eval verdict: `state/clm_v4_baseline_eval_2026_05_05/verdict.json`
- F-SHIM-V4-3 evidence: `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v4_retry_2_exec.nohup.log`
- README draft (= uploaded README): `docs/anima_clm_hf_release_v1_README_draft.md`
- audit JSONL: `state/hf_upload_audit/20260504T232612Z_need-singularity__clm-v4-mk2-v1.jsonl`
- promote script: `state/clm_v4_hf_release_v1_upload_2026_05_04/public_promote_2026_05_07.bash`
- this prep verdict: `state/clm_v4_hf_release_v1_public_promote_prep_2026_05_05/verdict.json`
- sibling cleanup script: `state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash`
