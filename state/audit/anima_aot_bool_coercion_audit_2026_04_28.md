# Anima AOT Bool Coercion Bug — Impact Audit (24+ verifier)

**Date:** 2026-04-28
**Repo:** /Users/ghost/core/anima
**Branch:** main
**Auditor:** own 4 root-cause-only (NO AUTO-FIX)
**Bug origin:** T17 `mk_xii_eeg_corroboration.hexa` (raw#106) — surfaced during corroboration aggregator development
**Cross-link:** RFC-009 (anima/hexa-lang AOT bool coercion semantics — to be drafted)

---

## 1. Bug Pattern (root cause)

In hexa AOT mode, an `int`-returning function whose body emits `return 1` / `return 0`
**may be coerced to `bool`** by the AOT codegen when the call appears in a comparison
context. The downstream comparison `int_returning_fn() == 1` then becomes
`bool == int_literal` and silently fails (returns false even when the function
returned 1).

```hexa
// BUGGY (AOT only — interp mode silently passes)
fn is_digit_ch(c: string) -> int {
    if c >= "0" && c <= "9" { return 1 }
    return 0
}
if is_digit_ch(c) == 1 { ... }   // AOT: comparison broken
```

The interp mode treats both sides as `int` and the equality is exact, so the
bug is invisible in `hexa run` (development) but materialises only when the
file is encoded by `hxc_aXX_*` AOT pipelines (live-fire / shipping path).

PROPER pattern (raw#86 audit cross-reference): `exec_with_status(...)` returns
`int` exit code that is **always** numerically meaningful and is never re-bound
to a 0/1 truth value, so it is excluded from this audit (NOT a bug).

---

## 2. Methodology

1. Enumerated **3 431** `.hexa` files under `/Users/ghost/core/anima` excluding
   `.claude/`, `.git/`, `.venv*`, `references/` (vendor/ephemeral).
2. Three-phase grep:
   - **Phase A (DEFINITE):** Functions known to return `int` semantically as a
     bool predicate, compared with `== 0/1` or `!= 0/1`.
     Names matched:
     `is_digit_ch`, `is_digit`, `sa_is_digit`, `is_speech_active`, `is_speaking`,
     `is_power_of_2`, `is_prng`, `is_bin_idx`, `has_flag`, `_has_flag`,
     `is_valid_task`.
   - **Phase B (POSSIBLE):** Predicate-named test functions
     (`test_t[0-9]_*`) returning int compared with `== 1`.
   - **Phase C (SAFE):** All other `fn() OP int_literal` patterns
     (`len(...)`, `index_of(...)`, `gcd(...)`, `cos_ppm(...)`,
     `pack_total(...)`, `id_*()`, `op_*()`, `to_int(...)`, etc.) where return
     value is a numerically-meaningful int (length, index, hash, count, id) and
     **not** a bool-shaped 0/1 — these survive AOT coercion because the codegen
     does not bool-coerce non-predicate ints.
3. Defensive guard form `to_int(x) == 1 || x == true` (see
   `edu/lora/corpus_4gate.hexa`) classified **SAFE**: the disjunction tolerates
   both interp and AOT representations.

---

## 3. Inventory

### 3.1 Totals

| Category        | Hits | Files |
|-----------------|------|-------|
| **DEFINITE_BUG** | 57   | 33    |
| **POSSIBLE_BUG** | 34   | 6     |
| **SAFE**         | ~3 400 (rest) | — |
| Total .hexa scanned | — | 3 431 |

### 3.2 DEFINITE_BUG breakdown by file (sorted by hit count)

| Hits | Path |
|------|------|
| 4 | `/Users/ghost/core/anima/anima-eeg/tool/eye_tracker_webcam.hexa` |
| 4 | `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_lz76_real.hexa` |
| 3 | `/Users/ghost/core/anima/anima-eeg/tool/wearable_health_integrator.hexa` |
| 3 | `/Users/ghost/core/anima/anima-eeg/tool/daily_life_context_logger.hexa` |
| 3 | `/Users/ghost/core/anima/anima-eeg/tool/commit_msg_diff_alignment_lint.hexa` |
| 3 | `/Users/ghost/core/anima/anima-eeg/tool/cardiac_eeg_integrator.hexa` |
| 3 | `/Users/ghost/core/anima/anima-eeg/tool/behavioral_correlates_logger.hexa` |
| 2 | `/Users/ghost/core/anima/anima-clm-eeg/tool/mk_xii_d_day_simulated_dry_run.hexa` |
| 2 | `/Users/ghost/core/anima/anima-clm-eeg/tool/g10_hexad_triangulation_scaffold.hexa` |
| 2 | `/Users/ghost/core/anima/anima-clm-eeg/tool/eeg_claude_cli_longitudinal_correlator.hexa` |
| 2 | `/Users/ghost/core/anima/anima-clm-eeg/tool/eeg_claude_cli_correlator.hexa` |
| 2 | `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_p3_gcg_pre_register.hexa` |
| 2 | `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_p2_tlr_pre_register.hexa` |
| 2 | `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_p1_lz_pre_register.hexa` |
| 2 | `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_harness_smoke.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_gates/rms_band.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_gates/pe_saturation.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_gates/hjorth_band.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_gates/composite_gate.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_gates/berger_alpha.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_artifact/reference_drift_detector.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_artifact/motion_artifact_detector.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_artifact/eye_blink_detector.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_artifact/environmental_emi_classifier.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_artifact/emg_muscle_detector.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_artifact/electrode_aging_classifier.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg-core/tool/modules/_artifact/ecg_heart_artifact_detector.hexa` |
| 1 | `/Users/ghost/core/anima/anima-clm-eeg/tool/eeg_to_token_cyborg.hexa` |
| 1 | `/Users/ghost/core/anima/anima-clm-eeg/tool/eeg_anomaly_autoencoder.hexa` |
| 1 | `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_pe_real.hexa` |
| 1 | `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_hjorth_real.hexa` |
| 1 | `/Users/ghost/core/anima/anima-clm-eeg/tool/clm_eeg_berger_sanity.hexa` |
| 1 | `/Users/ghost/core/anima/anima-eeg/tool/pre_post_task_recorder.hexa` |

### 3.3 POSSIBLE_BUG (predicate-style int test fns compared to 1)

| Hits | Path |
|------|------|
| 5 | `/Users/ghost/core/anima/anima-physics/hw_engine_bridge.hexa` (T1..T5) |
| 5 | `/Users/ghost/core/anima/training/run_ablation.hexa` |
| 5 | `/Users/ghost/core/anima/training/ablation_search.hexa` |
| 5 | `/Users/ghost/core/anima/training/train_clm_emergent.hexa` |
| ~7 | `/Users/ghost/core/anima/training/engine_ablation.hexa` |
| ~7 | `/Users/ghost/core/anima/training/engine_integration.hexa` |

These reach DEFINITE only if the test runner is built via `hxc_aXX` AOT
pipeline; in `hexa run` they are SAFE.

---

## 4. Top-3 critical files

1. **`anima-eeg/tool/eye_tracker_webcam.hexa`** (4 hits)
   `has_flag("--falsifiers"/"--selftest"/"--calibrate"/"--tick") == 1`
   — entire CLI dispatch is bool-coercion-fragile under AOT.

2. **`anima-clm-eeg/tool/clm_eeg_lz76_real.hexa`** (4 hits)
   `is_digit_ch(c) == 1` and `is_digit_ch(blob[q]) == 1` inside hot LZ76
   complexity loop; AOT could silently skip digit accumulation → wrong LZ76.

3. **`anima-eeg/tool/behavioral_correlates_logger.hexa`** (3 hits)
   Same `has_flag(...) == 1` dispatch pattern, plus this is a daily-life
   recorder (own 4 user-facing path).

Equally urgent (3 hits each): `wearable_health_integrator`,
`daily_life_context_logger`, `commit_msg_diff_alignment_lint`,
`cardiac_eeg_integrator`.

---

## 5. Recommended fix patterns (manual application — own 4 root-cause-only)

### 5.1 Predicate-int → boolean predicate (preferred)

```hexa
// before
fn is_digit_ch(c: string) -> int {
    if c >= "0" && c <= "9" { return 1 }
    return 0
}
if is_digit_ch(c) == 1 { ... }

// after — change return type to bool
fn is_digit_ch(c: string) -> bool {
    return c >= "0" && c <= "9"
}
if is_digit_ch(c) { ... }
```

### 5.2 Bind-then-compare (when API stability matters)

```hexa
// before
if has_flag("--selftest") == 1 { ... }

// after — capture int, compare locally (no implicit coercion site)
let f = has_flag("--selftest")
if f == 1 { ... }
```

### 5.3 Predicate guard (mk_xii pattern, defensive)

```hexa
// digit_val(s[i]) >= 0  — the canonical anima fix shape
//   • returns int (the digit value 0..9 or -1)
//   • compared with >= 0 (a magnitude check, not a 0/1 bool coercion)
//   • survives both interp and AOT
while i < n && digit_val(s[i]) >= 0 { ... }
```

This shape is **already used in T17 `mk_xii_eeg_corroboration.hexa`** and is the
empirical workaround that motivated this audit. Recommend promoting it as the
canonical "predicate-via-magnitude" idiom in RFC-009.

---

## 6. RFC-009 priority strengthening recommendation

1. **Promote priority to BLOCKER.** 33 DEFINITE_BUG files include the entire
   `anima-eeg-core/_gates/` and `_artifact/` module families (12 files,
   gate composition + artifact classification). All AOT-shipped EEG analytics
   are exposed.
2. **Codegen fix path:** AOT must preserve declared `-> int` return types and
   must not bool-coerce return values at comparison sites. If coercion is
   required for performance, it must be opt-in via an annotation
   (e.g. `@bool_coerce_ok`) — not implicit.
3. **Lint rule (RFC-007 cross-link):** Add a hexa lint that flags
   `int_returning_fn() == 0|1` shapes and recommends either (a) bool return
   refactor, (b) bind-then-compare, or (c) `>= 0` magnitude predicate.
4. **Selftest fixture:** Ship a 5-line AOT regression fixture that exercises
   `is_digit_ch(c) == 1` and asserts the AOT binary produces the same result as
   the interp run (current divergence is the smoking gun).
5. **Cross-cut audit:** Re-run this audit on `hexa-lang/` and `airgenome/` to
   measure full workspace blast radius before RFC-009 lands.

---

## 7. Constraint compliance

- raw#9   hexa-only — audit pure grep, no python
- raw#10  honest C3 — only DEFINITE shapes counted; POSSIBLE explicitly separated
- raw#65  idempotent — same grep set, same input → same audit output
- raw#91  high-variance — supermajority of EEG modules implicated (12+ files)
- own 4   root-cause-only — **NO AUTO-FIX**, manual verification mandatory

