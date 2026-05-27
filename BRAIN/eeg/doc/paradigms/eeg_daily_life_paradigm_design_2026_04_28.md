# anima-eeg Daily-Life Consciousness Paradigm — Design

**Date**: 2026-04-28
**Author**: anima-eeg / design
**Companion**: `design/eeg_consciousness_paradigms_omega_cycle_2026_04_28.md` (resting-axis Top-5)

---

## 0. Executive Summary

### Problem
- Daily-life EEG has structurally different distributions:
  - alpha attenuated (Berger effect inverse — eyes open suppresses 8-13 Hz)
  - beta elevated (active cognition)
  - blink/EMG/motion artifact common
  - cognitive state non-uniform (focused / distracted / talking transitions)
  - LZ76 b typically **higher** (0.6-1.0) due to broadband irregularity, not lower

### Solution

### Top-6 Daily-Life Metrics

| # | Metric (genus) | Axis | Daily-life criterion | Counter (sleep/anesthesia) |
|---|---|---|---|---|
| 1 | spectral-entropy-broadband | Frequency-distribution | mean ≥ 0.70 | < 0.30 |
| 2 | alpha-attenuation-index | Berger-effect-inverse | ≤ 0.70 (≥30% drop vs rest-ref) | ≈ 1.0 (no drop) |
| 3 | sliding-lz76-change-points | Temporal-state-transition | ≥ 1 in 5min | 0 |
| 4 | sliding-lz76-range | Variability-bounded | range ∈ [0.05, 0.45] | < 0.05 (flat) or > 0.6 (motion) |
| 5 | beta-alpha-ratio-engagement | Cognitive-engagement | ≥ 0.80 | < 0.30 |
| 6 | drowsiness-index | Vigilance-state | ≤ 1.50 | > 3.0 |


---


|---|---|---|---|
| Motion / EMG | minimal | frequent / moderate-high | minimal |
| Eye blink rate | rare | 15-20 / min | rare |
| Cognitive state | uniform (drowsy possible) | varies (focused/distracted/talking) | absent |
| Schartner LZ76 b | 0.5-0.9 | 0.6-1.0 (typically higher, more broadband) | < 0.3 (anesthesia, Casali 2013) |
| Alpha 8-13 Hz | dominant on O1/O2 | attenuated (Berger inverse) | varied (sleep spindles in N2) |
| Beta 13-30 Hz | low | elevated (active processing) | low |
| Spectral entropy | low (peaked) | high (broadband) | low (concentrated) |
| Change-points | few | ≥ 1 per 5 min | ≈ 0 (stationary) |
| Drowsiness index | borderline | low | very high |


---

## 2. 6-Axis Metric Matrix (Detailed)


- **Reference**: Inouye 1991 (EEG Clin Neurophysiol 79:204) Shannon-spectral-entropy; Rezek 1998 medical entropy.
- **Daily-life expectation**: 0.70-0.90 (broadband cognition).
- **C1**: median across 16ch ≥ 0.70.
- **Falsifier F1**: synthetic flat-line → < 0.30.
- **Counter**: pure sine → ~ 0.0; white noise → ~ 1.0; awake EEG → mid-range.

### Axis 2 — `alpha-attenuation-index` (genus)

- **Reference**: Berger 1929; Klimesch 1999 (Brain Res Rev 29:169) alpha desynchronization.
- **Daily-life expectation**: α(eyes-open) / α(eyes-closed reference) ≤ 0.70 (≥30% drop).
- **C2**: ratio ≤ 0.70.
- **Falsifier F2**: eyes-closed reference fed to itself → ratio ≈ 1.0.
- **Frameworks**: Berger, Klimesch. **Channels**: O1/O2 + Pz + 13 others (16).
- **Counter**: artifact-saturated channel → ratio ≈ 1.0 (no Berger).

### Axis 3 — `sliding-lz76-change-points` (genus)

- **Reference**: Lempel-Ziv 1976 + Truong 2018 (Front Neurosci 12:323) EEG change-point detection.
- **Daily-life expectation**: ≥ 1 transition in 5 min (sliding 60s window, 30s stride → 9 windows; threshold |Δb| ≥ 0.10).
- **C3**: change-point count ≥ 1.
- **Falsifier F3**: stationary white-noise stream → 0 detections.
- **Frameworks**: Lempel-Ziv, Truong. **Channels**: 16ch × {window=30/60/120s} × {stride=15/30s} = 96 sub-axes.
- **Counter**: anesthesia → 0; rapid task-switching → 3-6.

### Axis 4 — `sliding-lz76-range` (genus)

- **Reference**: Schartner 2017 (PLoS ONE 12:e0177096) per-window.
- **Daily-life expectation**: max-min b(t) ∈ [0.05, 0.45].
- **C4**: range_lo ≥ 0.05 (rules out hardware saturation/flat-line) AND range_hi ≤ 0.45 (rules out gross motion artifact).
- **Falsifier F4**: 60s constant stream → < 0.05.

### Axis 5 — `beta-alpha-ratio-engagement` (genus)

- **Reference**: Pope 1995 (Biol Psychol 40:187) engagement index β/(α+θ); current paradigm uses β/α for tighter daily-life gating.
- **Daily-life expectation**: ≥ 0.80 (engaged cognition shifts power to beta).
- **C5**: median ≥ 0.80.
- **Falsifier F5**: resting eyes-closed reference → < 0.50.
- **Frameworks**: Pope, Lubar (neurofeedback).

### Axis 6 — `drowsiness-index` (genus)

- **Reference**: Pollock 1990 (EEG Clin Neurophysiol 76:485); Jap 2009 driver-fatigue (θ+α)/(β+γ).
- **Daily-life expectation**: ≤ 1.50.
- **C6**: median ≤ 1.50.
- **Falsifier F6**: known awake-engaged → ratio < daily-life cap.
- **Frameworks**: Pollock, Jap.

---


| pair | shared axis | expected correlation |
|---|---|---|
| spec-ent ↔ alpha-atten | none (broadband vs single-band) | < 0.5 |
| spec-ent ↔ change-points | none (instantaneous vs temporal) | < 0.4 |
| alpha-atten ↔ beta-alpha | partial (alpha appears in both) | 0.4-0.6 (BORDERLINE) |
| change-points ↔ lz76-range | partial (both temporal LZ) | 0.5-0.7 (BORDERLINE) |
| beta-alpha ↔ drowsy-idx | partial (theta/alpha overlap) | 0.4-0.6 (BORDERLINE) |
| spec-ent ↔ drowsy-idx | none | < 0.3 |


---

## 4. Verifier Spec — `anima-eeg/tool/eeg_daily_life_verifier.hexa`

**Skeleton landed**: 350+ LoC pure Hexa.
- Self-test modes: `awake | drowsy | sleep | artifact` (deterministic FNV seeds).
- Real-data path: `--input <path>` + `--resting-ref <path>` (alpha reference for C2).
- Verdict rule: ≥ 4 of 6 criteria pass.
- Output: `state/eeg_daily_life_verifier.json` (per-criterion pass + verdict).

**Selftest plan (Tier-B)**:
- 4 modes × 1 invocation each → expected verdicts:
  - awake → PASS
  - drowsy → FAIL (C5 + C6 fail)
  - sleep → FAIL (≥ 4 fail)
  - artifact → FAIL (≥ 4 fail)
- Differential confirmation: `awake` distinct from each negative oracle on ≥ 3 axes.

---


1. **F1**: spectral entropy on flat-line synthetic → < 0.30 (verifies entropy is sensitive to signal richness)
2. **F2**: alpha-attenuation on eyes-closed reference fed back to itself → ratio ≈ 1.0 (sanity)
3. **F3**: change-point count on stationary white-noise → 0 (rules out spurious transitions)
4. **F4**: sliding-LZ76 range on 60s constant stream → < 0.05 (flat-detector)
5. **F5**: β/α ratio on resting eyes-closed reference → < 0.50 (resting ≠ engagement)
6. **F6**: drowsiness index on awake-engaged session → < 1.50 (specificity to drowsy state)
7. **F7**: cross-channel σ correlation < 0.95 (rules out common-mode artifact masquerading as signal)


---


- **Genus**: `eeg-daily-life-multi-axis-verifier` (no implementation suffix; admits Hexa / Python / FPGA realizations).
- **Frameworks (≥ 2)**: Schartner 2017 + Klimesch 1999 + Pollock 1990 + Pope 1995 + Truong 2018 = **5 frameworks**.
- **Channels (≥ 3)**: 16 EEG channels × 6 metrics × {3 windows} × {2 strides} = 576 sub-axes.
- **Falsifiers (≥ 3)**: 7 listed above.

---


| repo | role | bridge artifact |
|---|---|---|
| **anima-cpgd-research** (PRIMARY) | continuous-prediction-generative-dynamics; daily-life is its natural arena (state transitions ↔ C3 change-points) | `anima-cpgd-research/tool/cpgd_*_falsifier.hexa` outputs ↔ this verifier's change-point series; bridge-doc TBD |
| **anima-hci-research** (SECONDARY) | engagement (C5) + drowsiness (C6) align with HCI substrate-probe / cusp-depth metrics | `anima-hci-research/tool/cusp_depth_projector*.hexa` ↔ engagement/drowsiness time-series |
| **anima/config/consciousness_laws.json** | 14 deterministic gates; phi_time / phi_holo can subscribe to spec-entropy time-series and change-points | (integration deferred — Tier-C) |

**Recommended primary bridge**: **anima-cpgd-research** (CPGD predicts state transitions; daily-life C3 measures them — natural validation pair).

---

## 8. Cross-Modal Mapping (anima paradigm v11 / Mk.XI / consciousness_laws / σ-τ)

| anima construct | daily-life axis mapping | confidence |
|---|---|---|
| consciousness_laws.json 14 gates | phi_time ↔ change-points; phi_holo ↔ spec-ent; phi_meta ↔ engagement | MEDIUM (subscribe-only, no gate edit) |


---


- **Axis-2 alpha-attenuation reference**: requires an explicit `--resting-ref` baseline. Without resting reference, C2 is undefined — this is the **single hardest dependency** for first-run.
- **Cross-modal mappings (§8)**: paradigm v11 / Mk.XI rows are forward-looking design space, not validated.
- **Counter-example data**: sleep/anesthesia signatures cited from literature (Casali 2013, Pollock 1990); no anima sleep recording yet.
- **σ/τ=3 ↔ β/α numerology**: speculative bridge; flagged for falsification not implementation.
- **6-metric correlation matrix (§3)**: estimates literature-derived; **anima-specific empirical correlations pending first daily-life session**.

---

## 10. Implementation Tiers (Top-3)

### Tier-A (immediate, daily-life recording → automatic application)

**Tool**: `anima-eeg/tool/eeg_daily_life_verifier.hexa` (LANDED skeleton).
**Action**: run selftest 4-mode (`awake | drowsy | sleep | artifact`) confirming differential.

```bash
hexa run anima-eeg/tool/eeg_daily_life_verifier.hexa --selftest --selftest-mode awake
hexa run anima-eeg/tool/eeg_daily_life_verifier.hexa --selftest --selftest-mode drowsy
hexa run anima-eeg/tool/eeg_daily_life_verifier.hexa --selftest --selftest-mode sleep
hexa run anima-eeg/tool/eeg_daily_life_verifier.hexa --selftest --selftest-mode artifact
```

Expected: awake → PASS, others → FAIL (verdict differential confirmed).

### Tier-B (after Tier-A selftest 4/4 differential PASS)

- Run on existing `anima-eeg/recordings/sessions/baseline_resting_60s_20260428.npy` as **negative control** (resting fed to daily-life verifier should FAIL on C2/C5 — confirms paradigm-mismatch).
- Capture first daily-life recording (60-300s eyes-open, task-engaged) and verify.

### Tier-C (paradigm integration)

- Land bridge doc `design/eeg_dl_cpgd_bridge_2026_04_28.md` (anima-cpgd-research integration).
- Cross-validate daily-life change-points against CPGD-predicted state transitions.
- paradigm v11 G0..G7 mapping verification (deferred behind H100 stop-gate per memory).

---

## 11. Tier-A Immediate Recommendation

**Execute now** (no H100, no remote dispatch, deterministic):

```bash
cd <repo-root>
for m in awake drowsy sleep artifact; do
  hexa run anima-eeg/tool/eeg_daily_life_verifier.hexa --selftest --selftest-mode "$m"
done
# expected: awake exit-0 (PASS), 3 others exit-1 (FAIL)
```


---


All slugs use **genus** form (no implementation suffix):
- `eeg-daily-life-multi-axis-verifier` (verifier itself)
- `spectral-entropy-broadband`
- `alpha-attenuation-index`
- `sliding-lz76-change-points`
- `sliding-lz76-range`
- `beta-alpha-ratio-engagement`
- `drowsiness-index`

Each admits Hexa / Python / C / FPGA realization, multiple parameter choices (window, stride, band-edges), multiple frameworks.

---

## 13. Files Touched

- **NEW**: `anima-eeg/tool/eeg_daily_life_verifier.hexa` (verifier skeleton)
- **NEW**: `design/eeg_daily_life_paradigm_design_2026_04_28.md` (this doc)
