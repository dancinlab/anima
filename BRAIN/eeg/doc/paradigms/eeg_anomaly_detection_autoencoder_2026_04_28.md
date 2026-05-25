# anima-clm-eeg B10 — Anomaly Detection (Autoencoder Reconstruction-Error) — Design

**Date**: 2026-04-28
**Tool**: `anima-clm-eeg/tool/eeg_anomaly_autoencoder.hexa`
**Status**: synthetic-only landing; real-baseline collection deferred to user action (N≥50 segments)

---

## 0. Problem

Resting-EEG verifiers (LZ76, PE, Hjorth, GCG, TLR — anima-clm-eeg/tool/) verify a *single
hypothesis* per segment. They cannot detect **state-shift / motion-artifact / drowsy onset**
within an otherwise-passing recording. The B10 axis adds an unsupervised, **per-segment
anomaly score**: train an autoencoder on the user's own resting-eyes-closed baseline manifold,
then any segment whose reconstruction error exceeds the learned baseline distribution by
z-score > 2 is flagged.

Why autoencoder (vs PCA / Mahalanobis):
- F4 falsifier explicitly compares against PCA(8) — if AE does not beat PCA on injected anomalies,
  the architecture is over-parameterized for an 80-d feature space and we honestly fall back.

---

## 1. Architecture

```
EEG segment (16 ch × N samples, default N = 5 s × 125 Hz = 625)
        │
        ▼  scipy.signal.welch (Hann, nperseg=125, no overlap)
PSD per channel × 5 bands (delta 1-4 / theta 4-8 / alpha 8-13 / beta 13-30 / gamma 30-45 Hz)
        │  log10(power + eps) per (ch, band)
        ▼
80-d feature vector  (16 ch × 5 bands)
        │  per-feature z-score using TRAIN-set μ, σ (saved with model)
        ▼
   80 ─[W1 80×40 + b1, tanh]─ 40 ─[W2 40×20 + b2, tanh]─ 20 ─[W3 20×8 + b3, linear]─ 8
                                                                                      │
   80 ─[W6 16×80 + b6, linear]─ 16←[W5 …, tanh]─ 20 ←[W4 8×20 + b4, tanh]── 8 ◄───────┘
        │
        ▼
reconstruction_error = mean_squared_error(input, output)  (per segment)
```


| key | value | reason |
|---|---|---|
| sample_rate_hz | 125 | OpenBCI Cyton default |
| segment_seconds | 5.0 | matches LZ76 / Hjorth window |
| n_channels | 16 | OpenBCI Cyton + Daisy |
| n_bands | 5 | δ θ α β γ |
| feature_dim | 80 | 16×5 |
| bottleneck_dim | 8 | 의식 상태 manifold 가정 (state ≈ 8 latent dims) |
| epochs_min | 100 | overfitting 방지 lower bound |
| epochs_max | 300 | early-stop safety |
| learning_rate | 0.01 | seeded SGD |
| batch_size | 16 | small-N (N≥50 baseline) friendly |
| z_threshold | 2.0 | 95% CI, anomaly above |
| min_baseline_n | 50 | frozen lower bound |

---


| ID | Criterion | Pass condition |
|---|---|---|
| C1 | training converges | final_train_loss < 0.5 × initial_train_loss |
| C2 | not catastrophically overfit | val_loss ≤ 3.0 × train_loss (Bishop PRML ch 12 small-N AE; honest threshold for 80-d feature on N≈120 train) |
| C3 | reconstruction calibrated | on held-out *baseline* segments, ≥80% have z-score ≤ 2 |
| C4 | injected anomaly detected | synthetic anomaly segments have median z-score ≥ 2 |
| C5 | not all-anomaly | < 50% of baseline segments flagged on re-run (F5 guard) |

- **PASS** = C1∧C2∧C3∧C4∧C5
- **PARTIAL** = C1∧C2 hold but exactly one of C3/C4/C5 fails (model trained but calibration off)
- **FAIL** = C1 or C2 fails (model did not learn)

- synthetic mode → `NOT_VERIFIED_SYNTHETIC` always (training data = synthetic)
- real mode → `REAL_HW_PASS_AE` / `REAL_HW_PARTIAL_AE` / `REAL_HW_FAIL_AE`

---


| ID | Falsifier | How exercised |
|---|---|---|
| F1 | train loss not decreasing → FAIL | `--selftest-mode flat-loss` (frozen weights, no SGD) |
| F2 | re-running on same baseline produces z>2 (over-anomalous) → triggers C5 fail | implicit in C5 (≥50% flagged on re-run = self-anomaly) |
| F3 | val_loss > train_loss × 2 (overfitting) → FAIL via C2 | exercised when N small (<20) — selftest reports |
| F4 | bottleneck=8 underperforms PCA(8) on injected anomaly detection | `--ablation-pca` flag computes PCA(8) reconstruction-error AUC vs AE AUC |
| F5 | every segment flagged → C5 fail | re-evaluation pass on training set; if >50% flagged the threshold is mis-calibrated |

Selftest-modes:
- `baseline-only`: synthetic 1/f resting-EEG (16 ch, 60 segments, 5 s @ 125 Hz). Expect **PASS**.
- `inject-anomaly`: 50 baseline + 10 injected (high-amplitude beta burst, simulated motion artifact) → expect baseline z-mean ≈ 0, injected z-mean > 2 (C4 PASS).
- `flat-loss`: forces 1 epoch, no convergence → C1 FAIL → verdict FAIL (F1).
- `tiny-n`: N=10 baseline → val_loss explodes → C2 FAIL (F3).

---

## 4. Implementation notes

- **No torch dependency** — pure numpy autoencoder (forward + manual back-prop). The user's
  `.venv-eeg` does not include torch and B10 is supposed to be lightweight; numpy is sufficient
- **3-way split**: 60% train / 20% val (early-stop) / 20% calibration (z-score anchoring).
  μ_e, σ_e of reconstruction error are anchored on the **val** pool (not train) to avoid
  optimistic bias; C3 is measured on the held-out **calibration** pool.
- **L2 weight decay = 0.01** on weight matrices (not biases) to regularize the over-parameterized
  re-deterministic-trainability from same seed; we save seed + hyperparams instead).
- Audit JSONL: one row per invocation with full metric set, frozen hyperparams, seed,
  input sha256, and verdict. Append-only, BSD `uchg`-eligible.

---

## 5. Why this is honest

  reconstruction error to floating-point precision. The verdict is deterministic.
  collect ≥50 real eyes-closed baseline segments before `--mode real` produces a `REAL_HW_*`
  classification.
  per-segment hypothesis tests; it complements them with a per-segment unsupervised score.
  honestly rather than forcing a binary PASS/FAIL.

---

## 6. User action plan (real-data path)

1. Collect ≥50 eyes-closed resting baseline segments (5 s each, 16 ch, 125 Hz) using
   `anima-eeg/eeg_recorder.hexa` or existing `collect.hexa`. Save as a single
   `(n_segments, 16, 625)` `.npy` array.
2. Run training:
   ```
   hexa run anima-clm-eeg/tool/eeg_anomaly_autoencoder.hexa \
       --train --input <baseline.npy> \
       --out state/anima_eeg_b10_baseline_v1.json
   ```
3. Run inference on a new recording:
   ```
   hexa run anima-clm-eeg/tool/eeg_anomaly_autoencoder.hexa \
       --infer --input <new_session.npy> \
       --baseline state/anima_eeg_b10_baseline_v1.json
   ```
4. Inspect `state/eeg_anomaly_audit/<UTC-date>_anomaly.jsonl` for per-segment z-scores
   and flagged-segment indices.
