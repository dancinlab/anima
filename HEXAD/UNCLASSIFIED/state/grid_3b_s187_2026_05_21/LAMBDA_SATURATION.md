# S187-C — λ Saturation Sweep (Eval 3 mitosis cross-λ)

Extends S187 Eval 3 finding (EVAL_REPORT.md § 6.4) past λ=1.0 to test whether the mitosis-split signal **saturates** (plateau) or **inverts** (peak then fall).

**Run date**: 2026-05-21
**Compute**: 6 H100/A100 pods @ ~$0.20/min (RunPod) + ubu-1 CPU bf16 eval
**Hypothesis (from § 6.4)**: λ_φ ↑ ⇒ more splits (vC at λ_φ=1.0 saturated cell-cap 128); λ_ψ ↑ ⇒ fewer splits.

## Cross-λ mitosis split table

| cell | λψ | λφ | final cells | splits | merges | Φ final |
|---|---|---|---|---|---|---|
| **vA** | 0.3 | 0.3 | 70 | 68 | 0 | 0.5477 |
| **vA_s42** | 0.3 | 0.3 | 82 | 80 | 0 | 0.6397 |
| **vB_s42** | 1.0 | 0.3 | 60 | 58 | 0 | 0.6566 |
| **vC** | 0.3 | 1.0 | 128 | 126 | 0 | 0.6434 |
| **vD_s42** | 1.0 | 1.0 | 55 | 53 | 0 | 0.6494 |
| | | | | | | |
| **B3** | 3.0 | 0.3 | 69 | 67 | 0 | 0.6423 |
| **B10** | 10.0 | 0.3 | 128 | 126 | 0 | 0.6471 |
| **B30** | 30.0 | 0.3 | 128 | 126 | 0 | 0.6512 |
| | | | | | | |
| **C3** | 0.3 | 3.0 | 78 | 76 | 0 | 0.5552 |
| **C10** | 0.3 | 10.0 | 128 | 126 | 0 | 0.6253 |
| **C30** | 0.3 | 30.0 | 124 | 122 | 0 | 0.5623 |

## λ_φ axis (Φ-up, λ_ψ=0.3 control)

| λ_φ | cell | splits | final cells |
|---|---|---|---|
| 0.3 | vA (avg of vA + vA_s42) | 74.0 | 76.0 |
| 1.0 | vC | 126 | 128 |
| 3.0 | C3 | 76 | 78 |
| 10.0 | C10 | 126 | 128 |
| 30.0 | C30 | 122 | 124 |

## λ_ψ axis (Ψ-up, λ_φ=0.3 control)

| λ_ψ | cell | splits | final cells |
|---|---|---|---|
| 0.3 | vA (avg) | 74.0 | 76.0 |
| 1.0 | vB_s42 | 58 | 60 |
| 3.0 | B3 | 67 | 69 |
| 10.0 | B10 | 126 | 128 |
| 30.0 | B30 | 126 | 128 |

## Observation

**Both axes show non-monotone saturation patterns, NOT the simple monotone signal hypothesized from § 6.4.**

- **λ_φ axis** (0.3 → 1.0 → 3.0 → 10.0 → 30.0): splits 74 → 126 → 76 → 126 → 122
  - λ_φ=1.0 already saturates cell-cap (vC=126).
  - λ_φ=3.0 unexpectedly DIPS to 76 (close to baseline 74), then re-saturates at λ_φ≥10.0.
  - Tentative interpretation: φ-pressure has a non-monotone training-time effect; the mid-λ region may produce a *less* clustered tension landscape at eval time. Single-seed noise (vA dual-seed: 68 vs 80) can account for ~12 split drift, BUT C3=76 vs C10=126 = 50-split delta is well above seed noise.
- **λ_ψ axis** (0.3 → 1.0 → 3.0 → 10.0 → 30.0): splits 74 → 58 → 67 → 126 → 126
  - λ_ψ=1.0 produces a DIP (vB_s42=58, below baseline 74) — matches § 6.4 prior observation.
  - λ_ψ=3.0 recovers to 67, near baseline.
  - λ_ψ≥10.0 saturates cell-cap (126/126) — opposite direction from the § 6.4 "λ_ψ ↑ ⇒ fewer splits" hypothesis.
  - Tentative interpretation: low-to-moderate λ_ψ suppresses splits, but at large λ_ψ the trained Ψ field itself becomes high-variance and saturates the substrate-tension signal regardless of φ-pressure.

### Key finding

The earlier Eval 3 reading that "λ_φ ↑ ⇒ more splits, λ_ψ ↑ ⇒ fewer splits" is *only valid in the [0.3, 1.0] interval*. Past λ=3.0, both pressures eventually produce cell-cap saturation. The split count is therefore a poor monotone proxy for λ effect at high λ — the cell-cap MAX_CELLS=128 is the binding constraint that hides true pressure differences.

Practical implication: future grid-search work targeting "mitosis activity" as an outcome should either (a) increase MAX_CELLS to expose the saturation ceiling, (b) replace count-splits with an integral metric like mean-Φ-history that doesn't saturate, or (c) measure split-arrival rate (1/time-to-first-split) which captures pressure even at cap.

## Honest C3 (caveats)

- Single seed=1337 per cell. vA cross-seed (1337 vs 42) showed 68 vs 80 splits = ~12 drift, so 5-point cross-λ deltas under ~12 should be treated as noise.
- Each cell trained 2000 steps only (matching S187 baseline), CE ~3.8-4.0 floor, NOT converged. λ effects measured in early-training regime; mature-training behavior may differ.
- Eval 3 = mitosis cell-pool Python port driven by model.forward()'s per-layer tensions on prompt "안녕? 너는 누구야?" greedy 40 steps. MAX_CELLS=128 hard cap is the dominant ceiling at high λ.
- λ_φ=30.0 and λ_ψ=30.0 are 100× the §184 baseline (0.30); training stability not separately verified beyond CE convergence in the 3.8-4.5 range. Some runs (B-series) showed initial L_route=50 spike that decayed within 80 steps.
- C3 and C10 ran the NumPy-vectorized eval3 variant (`eval3_mitosis_fast.py`) due to pure-Python n²·d cosine being prohibitively slow at n=128/d=3072. The two implementations differ in init-noise RNG (numpy vs Python random.gauss); C3 splits=76 and C10 splits=126 should still be comparable to other cells but the absolute split counts have a small RNG-source caveat.
- Pod-side eval3 (not ubu-1 CPU): trained ckpt evaluated *in place* on the same H100/A100 pod that produced it, immediately after training, before pod termination. Each pod's 17 GB ckpt was never transferred off — eval3 ran on-pod, only the small JSON came to Mac. This bypassed the 6.8 MB/s home-WAN bottleneck that would otherwise have taken ~6-h per ckpt for SCP back.
- Cost actual: ~$8-15 cumulative pod-burn over 75 min wall (6 pods, mixed H100 SXM/NVL + A100 SXM/PCIe). Stayed within $25 cap. Training itself was ~12 min/pod = $14.4 train share.
- ckpt SHA256s captured only for C30 (other pods terminated before sha256sum follow-up landed — `eval_out_lambda_sweep/*_ckpt_sha256.txt` for C3/C10/B-series are missing or empty). Reproducibility from result.json + train.log + dispatch params still intact.
