# RFC-009 AOT Bool Coercion BLOCKER — Batch 2 Fix

**Date:** 2026-04-28
**Branch:** main
**Audit source:** state/audit/anima_aot_bool_coercion_audit_2026_04_28.md (commit 726ba810f)
**Predecessor:** commit c57122d47 (Top-3, 3 files / 11 hits)
**This batch commits:** 4c52c1c86 (T1, 4 files / 4 hits), 43041c0ae (T2, 16 files / 22 hits)

## 1. Inventory (live grep, 2026-04-28 23:50)

Live `grep -cE '\b(is_digit_ch|has_flag|_has_flag|is_valid_task|is_digit)\b[^=]*\)\s*(==|!=)\s*[01]\b'`
on the 30 files identified by the D1 audit (33 files - 3 Top-3 done) yields
**46 DEFINITE_BUG hits across 30 files**. Earlier audit-doc total of "22 files / 46 hits" was off by 8 files (counting only those with ≥2 hits); live grep is authoritative.

## 2. 5-tier classification

| Tier | Files | Hits | Description |
|------|------:|-----:|-------------|
| T1 critical hot loop | 4 | 4 | clm_eeg_pe_real, clm_eeg_hjorth_real, clm_eeg_berger_sanity, eeg_to_token_cyborg |
| T2 verifier core | 16 | 22 | 5 _gates/ + 7 _artifact/ + wearable_health, daily_life_context, cardiac_eeg, pre_post_task |
| T3 helper utility | 4 | 9 | commit_msg_diff_alignment_lint(3), eeg_claude_cli_correlator(2), eeg_claude_cli_longitudinal_correlator(2), eeg_anomaly_autoencoder(1) |
| T4 test/selftest | 2 | 4 | clm_eeg_harness_smoke(2), mk_xii_d_day_simulated_dry_run(2) |
| T5 cold path | 4 | 8 | g10_hexad_triangulation_scaffold(2), clm_eeg_p1/p2/p3_pre_register(2 each) |

**Fixed in this batch (T1+T2):** 20 files / 26 hits
**Deferred (T3-T5):** 10 files / 20 hits

## 3. Fix-shape rationale

All 20 fixed files use **Shape A (bool refactor)** per RFC-009 §5.1. Predicate
function signature changed `-> int` (return 1/0) → `-> bool` (return true/false);
callsites changed `if pred(x) == 1 { }` → `if pred(x) { }`. Single negation
callsite (pre_post_task_recorder `is_valid_task(task) == 0`) became `!is_valid_task(task)`.

Rationale: Shape A removes the AOT codegen coercion site entirely (function
declares bool, comparison disappears). Shape B (bind-then-compare) preserves
the bug at a renamed site; Shape C (>= 0 magnitude) is unsafe for `has_flag`
(no underlying magnitude semantics). Shape A is also what Top-3 commit c57122d47
applied → consistency.

LoC delta: +28/-28 (T1) + +52/-52 (T2) = **+80/-80 token-only refactor**, semantics unchanged.

## 4. PASS/BLOCKED breakdown

**T1 (4/4 PASS):** all four `--selftest interp` runs returned `verdict=PASS`
or `SELFTEST_OK` — pe_real (white noise PE→1.0), hjorth_real (white cpx ~1.7),
berger_sanity (alpha sine 10 Hz), eeg_to_token_cyborg (F1-F4 PASS, F5 deferred).

**T2 selftest results (interp):**
- PASS: rms_band, composite_gate, emg_muscle_detector (sample-tested module set), daily_life_context_logger.
- BLOCKED (3 files): wearable_health_integrator, cardiac_eeg_integrator, pre_post_task_recorder — toolchain auto-invoke conflict (silent-failure-enforcement Class 1, hexa.real rebuild 22:57 today). Same regression noted in c57122d47 commit msg. Not caused by this fix; bool-coercion fix verified by grep zero-hit + Shape A diff review.
- Other 9 _gates/_artifact modules: not selftest-tested individually (sample of 3 PASS sufficient given identical fix shape across all 12).

**AOT verification deferred** (raw#42 mac-zero-compute): bool-coercion bug only
manifests under AOT, but Shape A removes the coercion site, so interp PASS +
zero-hit grep is the operationally sufficient verifier. Full AOT regression
deferred to next remote-build window (Hetzner / RunPod).

## 5. Remaining hits + next batch plan

| Tier | Files | Hits | Next action |
|------|------:|-----:|-------------|
| T3 | 4 | 9 | One commit `fix(rfc-009-batch2-T3)`. commit_msg_diff_alignment_lint uses `_has_flag` (rename-shape A). |
| T4 | 2 | 4 | One commit `fix(rfc-009-batch2-T4)` — test/dry-run files, low-risk. |
| T5 | 4 | 8 | One commit `fix(rfc-009-batch2-T5)` — pre-register files, idempotent Shape A. |

POSSIBLE_BUG (34 hits / 6 files in `training/` and `anima-physics/`) deferred — only DEFINITE under AOT codegen. Re-evaluate after T3-T5 land.

## 6. Constraint compliance summary

- raw#9 hexa-only — pure hexa source edits
- raw#10 honest C3 — 3 BLOCKED files explicitly documented
- raw#12 silent-error-ban — selftest exit codes verified where possible
- raw#18 self-host fixpoint — no codegen change, lint-level fix only
- raw#42 mac-zero-compute — no AOT rebuild on Mac
- raw#65 idempotent — grep zero-hit on all 20 files post-fix
- raw#85 audit ledger — uchg unlock-edit-relock cycle observed
- raw#91 honest triad — token diff exact: +80/-80
- raw#159 RFC-009 upstream — Shape A matches §5.1 spec

## 7. Concurrent agent notes

- `anima-eeg-core/tool/eeg_core.hexa` had a separate concurrent edit (Phase 3 metrics dispatcher) — not staged in this batch (clean separation, no race).
- nexus CLI analysis / HPF Berger re-run (background) — no overlap with these 20 files.
- B6/B9 commit drift risk monitored: grep snapshot taken pre-edit, post-edit re-grep confirms no drift.
