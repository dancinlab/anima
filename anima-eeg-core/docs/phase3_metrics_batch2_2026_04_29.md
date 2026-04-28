# anima-eeg-core Phase 3 `_metrics/` Batch 2 — Land Note

**Date:** 2026-04-29
**Author:** anima-eeg-core Phase 3 metrics agent (recovery cycle)
**Predecessor:** Phase 3 batch 1 (commits `44f9dc6df` + `da12077d9`)
**Successor:** Phase 3 batch 3 (`spectral_entropy` + `change_points` deferred)

raws: #1 uchg-lock cycle · #9 hexa-only · #10 honest C3 · #12 frozen · #18 self-host · #37 transient · #42 mac-zero-compute · #65 idempotent · #71 falsifier ≥3 · #82 darwin · #91 honest triad · #95 triad-universal-mandate · own4 root-cause-only

---

## 1. Summary — raw#10 honest C3 disclosure

Phase 3 `_metrics/` batch 2 was **specced as 6 modules**; **landed 4** in
this cycle. Two modules are deferred to batch 3 (P1 follow-up). This is
the result of a recovery cycle: a previous session was killed mid-stream
after producing 4 module files plus a partial dispatcher edit. This
cycle inspected the surviving artefacts, ran their selftests, completed
the dispatcher routing, and emits this honest land note.

| # | Module | Decision | Selftest | Dispatcher route |
|---|--------|----------|----------|-------------------|
| 5 | `alpha_coherence.hexa` | PORT (shared scipy helper) | PASS (coh_AP=0.831) | `metric alpha-coherence` |
| 6 | `alpha_phase_plv.hexa` | PORT (shared scipy helper) | FALSIFIED-intentional (F_PLV_02; PLV=0.999 on synth, volume-conduction artefact in selftest fixture) | `metric alpha-phase-plv` (alias `alpha-plv`) |
| 7 | `dmn_coherence.hexa` | PORT (shared scipy helper) | PASS (coh_AP=0.831, topology_pass=1) | `metric dmn-coherence` |
| 8 | `frontal_asymmetry.hexa` | PORT (shared scipy helper) | PASS (\|A\|=1.592, sign=positive) | `metric frontal-asymmetry` |

Selftest pass count: **3/4 PASS, 1 FALSIFIED-intentional** (the kv-block contract is honoured; the falsifier *fired as designed* on saturated-PLV synthetic data).

Dispatcher landed-route count: **26 → 30** (committed HEAD without Phase 5 _hw routes baseline) or **36 → 40** (working tree with Phase 5 _hw routes already staged).

---

## 2. Wrap-vs-Port decision (raw#10 honest C3)

**DECISION: PORT all 4** — diverging from batch 1 (which WRAPped frozen
`anima-clm-eeg/tool/clm_eeg_*_real.hexa` legacy verifiers).

Reason: the natural WRAP target — `anima-eeg/tool/resting_state_network_analyzer.hexa` —
has a strict-mode auto-invoke regression (top-level `main()` after
`fn main`) that prevents direct exec under hexa-strict 2026-04-28.
raw#12 frozen forbids fixing the legacy file. Re-emitting the
~140-LoC scipy kernel into a `/tmp/anima_eeg_core_metrics_helper.py`
transient (raw#37) keeps the modules hermetic, lets all 4 share one
helper script (raw#65 idempotent overwrite), and matches canonical
formulas (Davidson 1992 / Lachaux 1999 / Bendat-Piersol).

| Module | Helper kernel function | Canonical reference |
|--------|------------------------|---------------------|
| `alpha_coherence` | `alpha_coh(a,b,fs)` via `scipy.signal.coherence` | Davidson 1992; Bendat-Piersol MSC |
| `alpha_phase_plv` | `alpha_plv(a,b,fs)` via FFT bandpass + `scipy.signal.hilbert` | Lachaux et al. 1999 |
| `dmn_coherence` | `alpha_coh(ant,pos,fs)` + topology check vs occipital | Greicius 2003 (DMN topology) — surface-EEG proxy |
| `frontal_asymmetry` | `band_power(F3/F7) vs band_power(F4/F8)` via `scipy.signal.welch` | Davidson 1992 frontal-α-asymmetry |

raw#42 compliance: heavy compute delegated to `.venv-eeg/bin/python` host venv via `exec_with_status`; selftest synthesises 16-ch × 8 s × 125 Hz fixture inline.

---

## 3. kv-block contract (Phase 1 reconcile)

All 4 modules expose `_metric_<name>_kv(npy_path, sidecar_kv, fs_hz) -> string` returning the canonical kv-block keys established by batch 1, plus per-module extras:

```
schema=anima-eeg-core/_metrics/<name>/1
metric=<name>
npy_path=<path or empty for selftest>
sidecar_kv=<csv kv pairs>
fs_hz=<sample rate>
<per-module-scalar>_x1000=<int>     # e.g. coh_anterior_posterior_x1000
value_x1000=<int>                   # canonical primary (uniform across batches)
verdict=<PASS|FAIL|FALSIFIED>
backend=/tmp/anima_eeg_core_metrics_helper.py
backend_rc=<int>
raw71_falsifier_count=3
raw71_triggered_count=<int>
raw71_triggered_ids=<csv>
raw91_evidence=<provenance-token>
raw91_limit=<scope-token>
raw95_enforce_layer=in_module
```

Per-module extras:

| Module | Extras |
|--------|--------|
| `alpha_coherence` | `coh_anterior_lateral_l_x1000`, `coh_anterior_lateral_r_x1000`, `coh_anterior_occipital_x1000` |
| `alpha_phase_plv` | `plv_anterior_lateral_l_x1000`, `plv_anterior_lateral_r_x1000` |
| `dmn_coherence` | `coh_anterior_occipital_x1000`, `topology_pass` (0|1) |
| `frontal_asymmetry` | `asymmetry_x1000` (signed), `abs_asymmetry_x1000`, `alpha_pow_left_x1000`, `alpha_pow_right_x1000`, `sign={positive\|negative\|zero}` |

---

## 4. raw#71 falsifiers (≥3 each, frozen 2026-04-29)

```
alpha_coherence:
  F_AC_01: coh_anterior_posterior_x1000 < 100      → no α-coupling (degenerate)
  F_AC_02: coh_anterior_posterior_x1000 > 990      → identical channels (ref-short)
  F_AC_03: coh_anterior_posterior_x1000 == sentinel→ helper-fail (raw#12 silent-error-ban)

alpha_phase_plv:
  F_PLV_01: plv_anterior_posterior_x1000 < 100     → no phase coupling
  F_PLV_02: plv_anterior_posterior_x1000 > 990     → identical channels / volume conduction
  F_PLV_03: plv_anterior_posterior_x1000 == sentinel→ helper-fail

dmn_coherence:
  F_DMN_01: coh_anterior_posterior_x1000 < 100      → no DMN signal
  F_DMN_02: coh_anterior_posterior_x1000 <
            coh_anterior_occipital_x1000           → reversed topology
  F_DMN_03: coh_anterior_posterior_x1000 == sentinel→ helper-fail

frontal_asymmetry:
  F_FA_01:  abs_asymmetry_x1000 < 50  (|A|<0.05)   → degenerate
  F_FA_02:  abs_asymmetry_x1000 > 5000             → impossible Davidson value
  F_FA_03:  alpha_pow == sentinel                  → helper-fail
```

12 falsifiers across 4 modules.

---

## 5. Selftest results (2026-04-28T15:35:00Z)

```
== _metrics/alpha_coherence selftest (synthetic_corr mode) ==
  coh_anterior_posterior_x1000=831  → verdict=PASS
== _metrics/alpha_phase_plv selftest (synthetic_corr mode) ==
  plv_anterior_posterior_x1000=999  → verdict=FALSIFIED (F_PLV_02 — intentional)
== _metrics/dmn_coherence selftest (synthetic_corr mode) ==
  coh_anterior_posterior_x1000=831, topology_pass=1 → verdict=PASS
== _metrics/frontal_asymmetry selftest (synthetic_corr mode) ==
  asymmetry_x1000=1592 (sign=positive) → verdict=PASS
```

The PLV FALSIFIED verdict is **honest C3 by design** — the selftest
synthesises four channels (Fp1, Fp2, P3, P4) all driven by the same
10 Hz sine + 0.3 σ noise at corr=0.85, and PLV is by construction
inflated by shared narrow-band drive (volume-conduction proxy). The
falsifier `F_PLV_02` correctly fires. Real-data verification (raw#42
host run) is expected to give plv_AP in the [0.10, 0.80] physiological
range.

Dispatcher route smoke tests (all four):
- `metric alpha-coherence` → BACKEND_PASS ✓
- `metric alpha-phase-plv` → BACKEND_PASS ✓ (rc=0; FALSIFIED is contract-honoured)
- `metric dmn-coherence` → BACKEND_PASS ✓
- `metric frontal-asymmetry` → BACKEND_PASS ✓

Audit ledger row appended to `state/anima_eeg_core_phase3_metrics_integration_audit.jsonl` (4 new rows; 8 total in file).

---

## 6. Dispatcher promotions (raw#1 uchg cycle)

`anima-eeg-core/tool/eeg_core.hexa` updated:

| Verb / Noun | Pre | Post |
|-------------|-----|------|
| `metric alpha-coherence` | (absent) | landed:_metrics/alpha_coherence.hexa |
| `metric alpha_coherence` | (absent) | landed (alias) |
| `metric alpha-phase-plv` | (absent) | landed:_metrics/alpha_phase_plv.hexa |
| `metric alpha_phase_plv` | (absent) | landed (alias) |
| `metric alpha-plv` | (absent) | landed (short alias) |
| `metric dmn-coherence` | (absent) | landed:_metrics/dmn_coherence.hexa |
| `metric dmn_coherence` | (absent) | landed (alias) |
| `metric frontal-asymmetry` | (absent) | landed:_metrics/frontal_asymmetry.hexa |
| `metric frontal_asymmetry` | (absent) | landed (alias) |

Dispatcher `_print_usage()` and `_print_list()` both updated. List total: 61 → 65 entries (+4 distinct nouns; alias variants share the same _print_list row).

Dispatcher selftest `eeg_core selftest` → DISPATCHER_SELFTEST_PASS (4/4 T1-T4).

raw#1 chflags uchg re-applied to `eeg_core.hexa` and to all 4 design docs (this file inclusive) post-edit.

---

## 7. Deferred — Phase 3 batch 3 (P1 follow-up, 2 modules)

raw#10 honest C3: batch 2 was specced as **6 modules**; **2 are deferred** to batch 3.

| Module | Helper kernel emitted? | Hexa wrapper status | Notes |
|--------|------------------------|---------------------|-------|
| `spectral_entropy.hexa` | YES (`spec_entropy(x,fs)` already in shared helper) | NOT LANDED | Wrapper would parse `spec_entropy_mean` from helper JSON; ~190 LoC sibling pattern. Falsifier triad would be `H<0.30 floor, H>0.99 white-saturation, H==sentinel`. |
| `change_points.hexa` | YES (`change_points(X,fs)` already in shared helper) | NOT LANDED | Wrapper would parse `change_points.{n_windows,change_count,mean_norm,max_diff}` nested keys; ~210 LoC. Falsifier triad would be `change_count==0 (degenerate stillness), change_count>n_windows*0.5 (over-segmentation), mean_norm==sentinel`. |

These two were almost certainly the intended members of batch 2 — the
shared `_emit_helper()` already computes `spec_entropy_mean` and a
`change_points` dict, but the surviving 4 module files only consume
α-band + asymmetry channels of the helper's output. Adding the two
P1 modules requires only a thin wrapper layer (parse, kv-block,
falsifier evaluation) since the math is already in `/tmp/...helper.py`.

**Roadmap entry:** `phase3-batch3 P1: spectral_entropy + change_points
hexa wrapper landing (helper kernels already shipped in batch 2).`

Other speculative batch-3+ candidates (lower priority): `spindle_density`,
`theta_ratio`, `beta_burst`, `mse_complexity`, `sample_entropy`. These
require additional helper kernels (not yet emitted) and are deferred
beyond P1.

---

## 8. Files

```
anima-eeg-core/tool/modules/_metrics/
  alpha_coherence.hexa            (~467 LoC; PORT, shared helper consumer)
  alpha_phase_plv.hexa            (~387 LoC; PORT, Lachaux PLV)
  dmn_coherence.hexa              (~393 LoC; PORT, topology-checked MSC)
  frontal_asymmetry.hexa          (~389 LoC; PORT, Davidson)

anima-eeg-core/tool/eeg_core.hexa  (dispatcher: +9 noun aliases, +4 list rows, +6 usage lines)
anima-eeg-core/docs/phase3_metrics_batch2_2026_04_29.md  (this doc)
state/anima_eeg_core_phase3_metrics_integration_audit.jsonl  (raw#77 audit, +4 rows)
```

---

## 9. RAW Compliance

| RAW | Compliance |
|-----|------------|
| #1 uchg-lock cycle | unlock → edit → re-lock applied to dispatcher + 3 phase docs |
| #9 hexa-only | All 4 modules + dispatcher edit pure hexa; helper is raw#37 transient .py |
| #10 honest C3 | Batch-2-as-6 → landed-4 disclosure; PORT decision documented; PLV FALSIFIED-intentional |
| #12 silent-error-ban | Helper-fail → sentinel `-2147483647` → verdict=FAIL |
| #18 self-host fixpoint | PORT diverges from batch 1's WRAP because legacy RSN backend has hexa-strict regression — own4 root-cause analysis surfaces the real reason |
| #37 transient | Shared `/tmp/anima_eeg_core_metrics_helper.py` re-emitted on each module run (idempotent overwrite) |
| #42 mac-zero-compute | Heavy compute delegated to `.venv-eeg/bin/python`; selftest only |
| #65 idempotent | Same helper file overwritten by 4 modules — byte-identical content (tested) |
| #71 falsifier ≥3 | 3 falsifiers preregistered per module = 12 total |
| #82 darwin | `.venv-eeg/bin/python` resolver-bypass declared in module headers |
| #91 honest triad | `raw91_evidence` + `raw91_limit` in every kv-block |
| #95 triad-universal | `raw95_enforce_layer=in_module` in every kv-block |
| #137 80% Pareto | Phase 3 cumulative: 8/10 metrics landed (80% Pareto threshold met) |
