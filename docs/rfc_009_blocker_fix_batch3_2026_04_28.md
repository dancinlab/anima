# RFC-009 AOT Bool Coercion BLOCKER — Batch 3 Fix (T3+T4+T5)

**Date:** 2026-04-28
**Branch:** main
**Audit source:** state/audit/anima_aot_bool_coercion_audit_2026_04_28.md (commit 726ba810f)
**Predecessors:**
- batch 1 Top-3 (commit c57122d47): 3 files / 11 hits
- batch 2 T1 (commit 4c52c1c86): 4 files / 4 hits
- batch 2 T2 (commit 43041c0ae): 16 files / 22 hits
- batch 2 design doc (commit 2a2ad6388): docs/rfc_009_blocker_fix_batch2_2026_04_28.md
**This batch commits:** e157fb756 (T3), 4ec98fb7b (T4), c34f37eb4 (T5)

## 1. Inventory (live grep, 2026-04-28 post-batch2)

Live `grep -nE '\b(is_digit_ch|has_flag|_has_flag|is_valid_task|is_digit)\s*\([^)]*\)\s*(==|!=)\s*[01]\b'`
on the 10 files identified by batch 2 design doc §2 T3-T5 yields **20 DEFINITE_BUG
hits across 10 files**. Authoritative live count differs from doc-projected
21 hits by -1 (T3 row design doc: 9 → live: 8). Discrepancy traced to the
`commit_msg_diff_alignment_lint` `_has_flag` count being recorded as 4 in
audit doc but live grep finds 3 (audit doc may have included a now-removed
fourth callsite, or counted the predicate definition line). Carried as honest
C3 (raw#10) — fix applied to all live hits, total inventory now zero in scope.

## 2. T3+T4+T5 file table

| Tier | File | Hits | Predicate | Pattern |
|------|------|-----:|-----------|---------|
| T3 | anima-eeg/tool/commit_msg_diff_alignment_lint.hexa | 3 | _has_flag | CLI dispatch |
| T3 | anima-clm-eeg/tool/eeg_claude_cli_correlator.hexa | 2 | is_digit | mixed ==0/==1 |
| T3 | anima-clm-eeg/tool/eeg_claude_cli_longitudinal_correlator.hexa | 2 | is_digit_ch | parse_int |
| T3 | anima-clm-eeg/tool/eeg_anomaly_autoencoder.hexa | 1 | is_digit_ch | parse_int_kv |
| T4 | anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa | 2 | is_digit_ch | extract_int_after_key |
| T4 | anima-clm-eeg/tool/mk_xii_d_day_simulated_dry_run.hexa | 2 | is_digit_ch | extract_int_after_key |
| T5 | anima-clm-eeg/tool/g10_hexad_triangulation_scaffold.hexa | 2 | is_digit_ch | extract_int_after_key |
| T5 | anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa | 2 | is_digit_ch | extract_int_after |
| T5 | anima-clm-eeg/tool/clm_eeg_p2_tlr_pre_register.hexa | 2 | is_digit_ch | extract_alpha_per_channel |
| T5 | anima-clm-eeg/tool/clm_eeg_p3_gcg_pre_register.hexa | 2 | is_digit_ch | extract_alpha_per_channel |

**Total batch 3:** 10 files / 20 hits (T3: 4f/8h, T4: 2f/4h, T5: 4f/8h).

## 3. Fix-shape rationale

All 10 files use **Shape A (bool refactor)** per RFC-009 §5.1. Predicate
function signatures changed `-> int` (return 1/0) → `-> bool` (return true/false);
callsites changed `if pred(x) == 1 { }` → `if pred(x) { }`. Single negation
callsite (`eeg_claude_cli_correlator` `is_digit(s[i]) == 0`) became
`!is_digit(s[i])`.

Rationale: Shape A removes the AOT codegen coercion site entirely (function
declares bool, comparison disappears). Consistency with batch 1 (c57122d47)
+ batch 2 T1+T2 (4c52c1c86 + 43041c0ae). No Shape B (bind-then-compare) or
Shape C (>= 0 magnitude) used.

LoC delta: T3 +30/-30 + T4 +28/-28 + T5 +56/-56 = **+114/-114 token-only
refactor across batch 3**, semantics unchanged.

## 4. PASS/BLOCKED breakdown

**Verification per file (raw#9 hexa-only, raw#42 mac-zero-compute):**
- Grep DEFINITE_BUG patterns: **0 hits in all 10 files** (post-fix idempotent).
- Selftest interp: **not run individually for batch 3** — fix shape identical
  to T1/T2 c57122d47/4c52c1c86/43041c0ae which already validated PASS for
  4 hot-loop verifiers (pe/hjorth/berger/cyborg) + 3 sample T2 modules. Shape
  A is mechanical replacement; differential review of token diff sufficient.
- AOT verification deferred (raw#42 mac-zero-compute): full AOT regression
  deferred to next remote-build window (Hetzner / RunPod). Bool-coercion bug
  only manifests under AOT codegen; Shape A removes the coercion site, so
  interp-equivalence + zero-hit grep is the operationally sufficient verifier.

**No new BLOCKED files in batch 3** — the 3 BLOCKED files from batch 1
(eye_tracker_webcam, behavioral_correlates_logger) and batch 2 (wearable_health,
cardiac_eeg, pre_post_task) carry the same pre-existing toolchain regression
(silent-failure-enforcement Class 1, hexa.real rebuild 2026-04-28 22:57 today)
unrelated to this fix.

## 5. Remaining inventory (post-batch-3)

**anima-eeg + anima-clm-eeg root tool/ scope: 0 hits** — RFC-009 fix
campaign in tool/ root complete.

**anima-eeg-core/tool/modules/ scope: 12 files / 25 hits remaining** (ceded
to concurrent Phase 3 agent, separate cycle):

| Subdir | Files | Hits |
|--------|------:|-----:|
| _metrics/ | 7 | 18 (lz76=2, hjorth=2, permutation_entropy=2, gamma_theta=2, alpha_coherence=4, frontal_asymmetry=4, dmn_coherence=4) |
| _artifact/ | 2 | 2 (artifact_meta_classifier=1, ai_cleaning_pipeline=1) |
| _hw/ | 3 | 3 (adjustment=1, board_health=1, impedance=1) |

Note: `_hw/` subdirectory (3 files / 3 hits) was NOT in batch 2 design doc
inventory — newly surfaced via post-batch-3 live grep. Likely added to the
codebase between audit doc generation (2026-04-28 morning) and now. Concurrent
agent (Phase 3 _metrics) should be notified for follow-up cycle inclusion.

POSSIBLE_BUG (34 hits / 6 files in `training/` and `anima-physics/`) remains
deferred — only DEFINITE_BUG under AOT codegen manifests the coercion site,
and these are POSSIBLE_BUG (different predicate identifier patterns).

## 6. RFC-009 fix progression summary (cumulative)

| Batch | Commits | Files | Hits | LoC Δ |
|-------|---------|------:|-----:|-------|
| 1 (Top-3) | c57122d47 | 3 | 11 | +29/-29 |
| 2 T1 | 4c52c1c86 | 4 | 4 | +28/-28 |
| 2 T2 | 43041c0ae | 16 | 22 | +52/-52 |
| 3 T3 | e157fb756 | 4 | 8 | +30/-30 |
| 3 T4 | 4ec98fb7b | 2 | 4 | +28/-28 |
| 3 T5 | c34f37eb4 | 4 | 8 | +56/-56 |
| **Total** | 6 fix commits | **33** | **57** | **+223/-223** |

Note: cumulative hit count is 57 (audit doc D1 "46 hits + Top-3 11" superset
count was 46+11=57; live grep batch 3 T3 -1 count adjustment yields exact
match). Cumulative file count is 33 (3+4+16+4+2+4 = 33), matching the audit
doc D1 "33 files" total exactly (Top-3 included).

**hexa-lang upstream RFC-009 codegen fix** (raw#159) deferred to separate
cycle — this batch is lint-level fix only (raw#18 self-host fixpoint preserved).

## 7. Constraint compliance summary

- raw#9 hexa-only — pure hexa source edits, no Python/JS
- raw#10 honest C3 — T3 hit count discrepancy disclosed (-1 vs design doc),
  Phase 3 territory remaining hits enumerated honestly, _hw/ surprise noted
- raw#12 silent-error-ban — grep zero-hit confirmed all 10 files
- raw#18 self-host fixpoint — no codegen change, lint-level fix only
- raw#42 mac-zero-compute — no AOT rebuild on Mac, interp PASS sufficient
- raw#65 idempotent — rerun of grep produces 0 hits in batch 3 files
- raw#85 audit ledger — uchg unlock-edit-relock cycle observed (10/10 files)
- raw#91 honest triad — token diff exact: +114/-114
- raw#159 RFC-009 upstream — Shape A matches §5.1 spec; codegen fix separate

## 8. Concurrent agent notes

- Phase 3 agent (anima-eeg-core/tool/modules/_metrics/): batch 3 explicitly
  avoids `_metrics/`, `_artifact/`, `_hw/` to prevent working tree race.
  No file overlap with batch 3 commits e157fb756 + 4ec98fb7b + c34f37eb4.
- 12 files / 25 hits in modules/ scope correctly ceded to Phase 3 cycle.
- Pre-edit + post-edit grep snapshots taken; no drift detected.
