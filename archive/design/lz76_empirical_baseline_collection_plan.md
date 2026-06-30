# LZ76 Empirical Baseline Collection Plan — anima resting EEG

**Created**: 2026-04-28
**Trigger**: Schartner-validation agent recommendation in commit 98d61133
**Goal**: replace operational placeholder `HUMAN_BASELINE_LZ76_X1000=850`
(raw#12 frozen 2026-04-26) with empirical mean − 2·SD computed from
`N ≥ 10` anima resting-EEG runs once homogeneity gate is met.
**Out of scope**: changing C1 (650) or C2 (200) — both remain operational
pre-commitments per raw#12 until separate falsifier transition is defined.

---

## 1. Current state (N counter)

Source of truth: `state/clm_eeg_lz76_audit/2026-04-28_lz76.jsonl`
(append-only ledger emitted by `anima-clm-eeg/tool/clm_eeg_lz76_real.hexa`).

| Mode | Row count | Notes |
|---|---|---|
| selftest (random / structured fnv synthetic) | 7 | 4× random, 3× structured — sanity, not real |
| **real** | **8** | first 60s baseline_resting captures; not all ICA-cleaned |
| **real ∧ ICA-cleaned ∧ ≥60s ∧ resting-eyes-closed** | TBD (≤ 8) | needs per-row inspection of `input` field + recordings/sessions/ filtered status |

**Headline N (real, all-mode)**: **8**
**Required N before transition**: ≥ 10
**Additional runs needed**: ≥ 2 (eyes-closed resting), ideally ≥ 5 to allow
homogeneity gate (std/mean < 0.5) without leverage from outliers.

---

## 2. Measurement protocol (per-run)

Identical to `state/recording_protocol_baseline_resting_v1.json` (D-day SOP):

| Step | Spec |
|---|---|
| Hardware | OpenBCI Cyton + Daisy 16-ch, 125 Hz native sample-rate |
| Montage | 10-20, references A1+A2 (linked-mastoid), GND Fpz |
| Subject state | seated, eyes-closed, awake, ambient quiet, no caffeine 4h prior |
| Duration | 60 s minimum (n ≥ 7500 samples/ch → concatenated 16-ch ≥ 120 000 bits, asymptote-stable per Aboy/Hu 2006) |
| Filtering | 1–45 Hz band-pass (CYTON_DAISY 125 Hz Nyquist 60 Hz limited) |
| Artifact rejection | ICA via MNE-Python (`anima-eeg/scripts/eeg_ica_clean.hexa`); reject components with EOG correlation > 0.6 or EMG-band power > 50% total |
| Binarisation | per-channel median-threshold (above=1, else 0); 16-channel sequential concatenation → 1-D binary stream (matches `clm_eeg_lz76_real.hexa`) |
| LZ76 | Kaspar-Schuster 1987 production-count; `b_n = c(n)·log2(n) / n` |
| Audit | append row to `state/clm_eeg_lz76_audit/<YYYY-MM-DD>_lz76.jsonl` with mode=real, full SHA-256, `b_n_x1000`, ICA flags, session metadata |

---

## 3. Mean − 2·SD calculation (placeholder script)

Pseudo-spec for future hexa tool `tool/lz76_empirical_baseline_compute.hexa`:

```
1. Load all rows from state/clm_eeg_lz76_audit/*.jsonl where:
     mode == "real"
     classification != "FAILED"
     binarized_length >= 120000
     ica_cleaned == true     (new field; emit from clm_eeg_lz76_real.hexa next bump)
2. Extract b_n_x1000 list → b_array (length = N)
3. Compute:
     mean_x1000  = sum(b_array) / N
     var_x1000sq = sum((b_i - mean)^2) / (N - 1)         // sample variance
     sd_x1000    = isqrt(var_x1000sq)                    // integer sqrt
     std_over_mean_permille = (sd_x1000 * 1000) / mean_x1000
4. Homogeneity gate (raw#71 falsifier transition condition):
     PROCEED if (N >= 10) AND (std_over_mean_permille < 500)
     ELSE     report "INSUFFICIENT_DATA" and HALT
5. Compute new HUMAN_BASELINE_LZ76_X1000:
     new_baseline = mean_x1000 - 2 * sd_x1000
6. Witness emit:
     state/raw71_falsifier_transitions/2026-MM-DD_lz76_baseline_empirical.jsonl
     {ts, action: "TRANSITION", N, mean_x1000, sd_x1000,
      std_over_mean_permille, old_baseline: 850, new_baseline,
      raw12_v2_bump_required: true, ...}
7. raw#12 v2 bump:
     a) chflags nouchg clm_eeg_lz76_real.hexa + clm_eeg_p1_lz_pre_register.hexa
     b) update HUMAN_BASELINE_LZ76_X1000 = new_baseline (both files, both must match)
     c) increment version v1 → v2 in cert string
     d) chflags uchg + emit raw#1+raw#85 audit
```

---

## 4. raw#71 falsifier transition condition (formal)

Transition `HUMAN_BASELINE_LZ76_X1000`: 850 (operational) → empirical mean − 2·SD

**PRE-conditions (ALL required)**:
- (a) `N ≥ 10` real-mode rows with `binarized_length ≥ 120000`
- (b) `std/mean < 0.5` (homogeneity — coefficient of variation under 50 %)
- (c) all rows `ICA-cleaned == true` (no raw EMI residue contaminating sample)
- (d) all rows from same hardware (Cyton+Daisy 125 Hz) — cross-hardware
  transfer is a separate question (raw#117)

**Condition (b) is the key falsifier**: if std/mean ≥ 0.5, the resting state
itself is not stationary across sessions — replacing the operational baseline
with a high-variance empirical mean would be premature; instead the workflow
should investigate state-stratification (eyes-open vs eyes-closed,
morning vs evening, etc.) before transition.

**POST-conditions (all witnessed)**:
- (a) raw#12 v1 → v2 bump in BOTH `clm_eeg_lz76_real.hexa` AND
      `clm_eeg_p1_lz_pre_register.hexa` (SSOT mirror parity)
- (b) raw#1 + raw#85 audit ledgers emitted for both unlock cycles
- (c) cert JSON outputs regenerated (deterministic, idempotent re-run)
- (d) all design / docs forward-pointers updated (separate own4 cycle)

---

## 5. Open items / not-this-cycle

- C1 0.65 floor empirical replacement: separate calculation, requires
  prior literature replication on anima hardware (Schartner 2015 Fig 7
  visual-estimate is not directly comparable to Cyton 125 Hz median path)
- C2 20% tolerance: defined as relative deviation, not directly affected
  by baseline change but the absolute |Δ| target shifts with new baseline
- Cross-substrate path (CLM hidden-state LZ76): independent of this plan

---

## 6. References

- Lempel-Ziv 1976: IEEE Trans Inform Theory 22(1):75-81 — LZ76 definition
- Kaspar-Schuster 1987: Phys Rev A 36:842, DOI 10.1103/PhysRevA.36.842 —
  production-count algorithm + random-asymptote b → 1.0
- Bódizs et al. 2024: eNeuro 11(3):ENEURO.0259-23 — median-binarisation
  method matching anima pipeline
- Aboy/Hu 2006-era simulation: finite-length LZ76 bias ~20–30 % below
  asymptote at n=256 bits, asymptote-stable at n ≥ 100 000 bits
- raw#12 frozen criteria registry (anima/.own/freeze.json or equivalent)
- raw#71 falsifier transition rules
- commit 98d61133 — Schartner reference accuracy retraction (this plan's
  ancestor)
