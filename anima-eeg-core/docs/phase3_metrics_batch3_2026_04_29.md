# anima-eeg-core Phase 3 `_metrics/` Batch 3 — Land Note

**Date:** 2026-04-29
**Author:** anima-eeg-core Phase 3 metrics agent (P1 follow-up cycle)
**Predecessor:** Phase 3 batch 2 (commit `3ac47185a`, doc `phase3_metrics_batch2_2026_04_29.md` — 4/6 honest C3 disclosure)
**Closes:** P1 follow-up roadmap entry from batch 2 §7 deferred

raws: #1 uchg-lock cycle · #9 hexa-only · #10 honest C3 · #12 frozen · #18 self-host · #37 transient · #42 mac-zero-compute · #65 idempotent · #71 falsifier ≥3 · #82 darwin · #91 honest triad · #95 triad-universal-mandate · own4 root-cause-only

---

## 1. Summary — closure of batch 2 honest disclosure

Batch 2 was specced as **6 modules** but landed only **4** in cycle 2026-04-28T15:35:00Z. The two deferred modules — `spectral_entropy` and `change_points` — already had their kernels emitted in the shared `/tmp/anima_eeg_core_metrics_helper.py` transient (raw#37) by every batch 2 module, but no hexa wrapper consumed those JSON keys. This batch lands the two thin wrapper modules and closes the P1 follow-up.

| # | Module | Decision | Selftest verdict | Dispatcher route |
|---|--------|----------|------------------|-------------------|
| 9 | `spectral_entropy.hexa` | PORT (shared scipy helper consumer) | PASS (h_mean=0.656) | `metric spectral-entropy` (aliases `spectral_entropy`, `spec-entropy`) |
| 10 | `change_points.hexa`    | PORT (shared scipy helper consumer) | FALSIFIED-intentional (F_CP_01; change_count=0 on stationary synth fixture) | `metric change-points` (aliases `change_points`, `cp`) |

Selftest pass count: **1/2 PASS, 1/2 FALSIFIED-intentional**. The change_points FALSIFIED verdict is honest C3 by design — synth_corr produces a stationary 16-ch × 8 s × 125 Hz fixture; with a 4 s/1 s sliding window only 5 windows are produced, and adjacent-window |Δb(n)| stays below the 0.1 threshold (max 0.016 on this fixture). F_CP_01 fires exactly as preregistered. Same FALSIFIED-by-design pattern as `alpha_phase_plv` F_PLV_02 from batch 2.

Dispatcher landed-route count: **30 → 32** (+2 distinct nouns; 6 alias variants in `_resolve_backend` share 2 `_print_list` rows).

---

## 2. Kernel divergence vs `/tmp` reference helper — raw#91 honest C3

**ZERO divergence.** Both modules byte-for-byte re-emit the same shared helper as batch 2 siblings (`alpha_coherence`, `alpha_phase_plv`, `dmn_coherence`, `frontal_asymmetry`). The kernels `spec_entropy(x, fs)` and `change_points(X, fs, win_s=4.0, step_s=1.0)` are unchanged from `/tmp/anima_eeg_core_metrics_helper.py` (the design-doc reference at HEAD `3ac47185a`). raw#65 idempotent overwrite holds.

Hexa wrapper layer per module:
- `spectral_entropy.hexa`: parses `"spec_entropy_mean"` from helper JSON → x1000 fixed-point → kv-block.
- `change_points.hexa`: parses nested `"change_count"`, `"n_windows"`, `"mean_norm"`, `"max_diff"` from helper JSON. Integer keys recovered via `_x1000_to_int` (divide x1000 fixed-point by 1000); floats stored at x1000.

---

## 3. raw#71 falsifiers (frozen 2026-04-29)

```
spectral_entropy:
  F_SE_01: h_mean_x1000 < 300         → narrowband floor (degenerate single-frequency)
  F_SE_02: h_mean_x1000 > 990         → white-saturation (flat PSD; ref-short / DC-coupled)
  F_SE_03: h_mean_x1000 == sentinel   → helper-fail (raw#12)

change_points:
  F_CP_01: change_count == 0           → degenerate stillness (stationary fixture)
  F_CP_02: change_count > n_windows/2  → over-segmentation (artifact-ridden)
  F_CP_03: mean_norm == sentinel       → helper-fail (raw#12)
```

6 falsifiers across 2 modules.

---

## 4. Selftest evidence (2026-04-29T00:55:00Z, fs=125 Hz, dur=8 s, synth_corr seed=0)

```
== _metrics/spectral_entropy selftest (synthetic_corr mode) ==
  h_mean_x1000=656  → verdict=PASS

== _metrics/change_points selftest (synthetic_corr mode) ==
  change_count=0, n_windows=5, mean_norm_x1000=759, max_diff_x1000=16
  → verdict=FALSIFIED (F_CP_01 — intentional honest C3)
```

Dispatcher route smoke tests (both new routes + alias coverage):
- `metric spectral-entropy --selftest` → BACKEND_PASS ✓
- `metric spec-entropy --selftest` → BACKEND_PASS ✓ (alias)
- `metric change-points --selftest` → BACKEND_PASS ✓ (rc=0; FALSIFIED contract honoured)
- `metric cp --selftest` → BACKEND_PASS ✓ (alias)

Audit ledger: 2 new rows appended to `state/anima_eeg_core_phase3_metrics_integration_audit.jsonl` (8 → 10 rows).

Dispatcher selftest `eeg_core selftest` → DISPATCHER_SELFTEST_PASS (4/4 T1-T4) post-edit. List total: 71 → 73 rows; landed= 47 → 49.

---

## 5. Files

```
anima-eeg-core/tool/modules/_metrics/
  spectral_entropy.hexa            (~330 LoC; PORT, shared helper consumer)
  change_points.hexa               (~360 LoC; PORT, sliding-window LZ76)

anima-eeg-core/tool/eeg_core.hexa  (dispatcher: +6 noun aliases, +2 list rows, +1 usage line)
anima-eeg-core/docs/phase3_metrics_batch3_2026_04_29.md  (this doc)
state/anima_eeg_core_phase3_metrics_integration_audit.jsonl  (raw#77 audit, +2 rows)
```

raw#1 chflags uchg cycle (unlock → edit → re-lock) applied to: dispatcher, audit ledger, and this doc.

---

## 6. RAW Compliance

| RAW | Compliance |
|-----|------------|
| #1 uchg-lock cycle | unlock → edit → re-lock applied to dispatcher + audit + this doc |
| #9 hexa-only | Both modules + dispatcher edit pure hexa; helper is raw#37 transient .py |
| #10 honest C3 | change_points FALSIFIED-intentional disclosed; zero kernel divergence vs /tmp helper |
| #12 silent-error-ban | Helper-fail → sentinel `-2147483647` → verdict=FAIL via F_*_03 |
| #18 self-host fixpoint | PORT (consumes shared helper emitted by sibling batch 2 modules) |
| #37 transient | Same `/tmp/anima_eeg_core_metrics_helper.py` re-emitted (idempotent overwrite) |
| #42 mac-zero-compute | Heavy compute delegated to `.venv-eeg/bin/python`; selftest only |
| #65 idempotent | Helper byte-identical to batch 2 (4 prior modules emit same content) |
| #71 falsifier ≥3 | 3 falsifiers preregistered per module = 6 total |
| #82 darwin | `.venv-eeg/bin/python` resolver-bypass declared in module headers |
| #91 honest triad | `raw91_evidence` + `raw91_limit` in every kv-block; FALSIFIED-by-design surfaced |
| #95 triad-universal | `raw95_enforce_layer=in_module` in every kv-block |
| #137 80% Pareto | Phase 3 cumulative: 10/10 specced metrics now landed (100%; closes batch 2 disclosure) |
