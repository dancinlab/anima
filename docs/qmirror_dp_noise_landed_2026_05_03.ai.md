# qmirror QRNG vs classical Laplace DP noise — F-QDP-1 landed (2026-05-03)

## TL;DR

**F-QDP-1 verdict: FALSIFIED** (technically, by a marginal 1-SE band — see "Honest reading" below).

| metric | classical Laplace | qmirror QRNG | non-private ref | qm − cl (paired, 1 SE) |
|---|---|---|---|---|
| test acc | 0.9090 ± 0.0176 | 0.9080 ± 0.0176 | 0.9085 | **−0.0010 ± 0.0007** |
| MIA advantage | 0.0376 ± 0.0065 | 0.0376 ± 0.0065 | 0.0376 | −0.00005 ± 0.00004 |

The hypothesis was that qmirror QRNG noise yields **both** higher utility **and** lower empirical privacy bound than `torch.distributions.Laplace`. At ε=1.0 per step, on a 1000-row synthetic logistic-regression task with 10 seeds, the data show:

- **Utility:** qmirror is paired-worse by 0.001 ± 0.0007 — falsified at 1 SE on the strict reading. Effect size ~0.1% absolute, which is below practical floor.
- **Privacy:** essentially identical (paired difference 5×10⁻⁵ ± 4×10⁻⁵, both noise paths are within noise of each other and of the non-private reference).

The non-private reference also achieves test_acc=0.9085 and MIA advantage=0.0376 — i.e., DP noise at this ε/scale was **too small to perturb the model meaningfully**. The experiment is in a "noise-dominated" regime where neither path moves the needle, and the verdict is essentially measuring numerical reproducibility of two Laplace samplers.

## Method (one paragraph)

Synthetic 1000-row binary classification (`sklearn.make_classification`, 20 features, 2 informative, 80/20 split). DP-SGD on logistic regression: per-sample L2 clip C=1.0, sum, add Laplace(0, 2C/(B·ε)) noise to the **summed** (D+1)-dim gradient, then average by batch size B=64. 30 epochs, lr=0.05, ε=1.0 per step. **Path A:** `torch.distributions.Laplace.sample()`. **Path B:** uniform U(0,1) drawn from qmirror MOCK LCG bytes (4-byte→uint32→/2³² packing) then mapped through standard Laplace inverse CDF `−b·sgn(u−0.5)·log(1−2|u−0.5|)`. Identical seeds for data, init, and batch order — only the noise source differs. Empirical privacy: Yeom-style loss-threshold MIA AUC over (member=train, non-member=test); advantage = 2·|AUC−0.5|. 10 paired seeds, paired-difference SE.

## Files

- `/Users/ghost/core/anima/state/qmirror_dp_noise_2026_05_03/run_dp_compare.py`
- `/Users/ghost/core/anima/state/qmirror_dp_noise_2026_05_03/verdict.json`
- `/Users/ghost/core/anima/state/qmirror_dp_noise_2026_05_03/utility_privacy_curve.json`
- `/Users/ghost/core/anima/state/qmirror_dp_noise_2026_05_03/run.log`
- `/Users/ghost/core/anima/state/markers/qmirror_dp_noise_landed.marker`

## Three honest caveats

1. **qmirror source is MOCK (Park-Miller LCG seed=12345), NOT true quantum entropy.** The "QRNG" stream in this run is the same statistically-uniform but cryptographically-trivial LCG validated in `state/qmirror_qrng_regression_2026_05_03/regression_summary.txt` (PARTIAL: PASS at n=1024, n=8192 fails lag-1 autocorr at α=0.01). Therefore the F-QDP-1 verdict actually tests "*does the inverse-CDF transform pipeline match torch.distributions.Laplace*" — and the answer is "yes, to within 0.1%". A live ANU substitution is one line (`anu_fetch_bytes` from `qmirror_qrng_nist_tier1plus_2026_05_03/run_tier1plus.py`) but requires `NEXUS_QMIRROR_ANU_KEY` and ~10s of rate-limited HTTPS per 8KB. This is the **single biggest gap** between this run and the falsifier as written.

2. **No formal (ε,δ)-DP accountant.** "ε=1.0 per step" composed over 30·12=360 steps is ε_total≈360 under sequential composition — there is **no meaningful end-to-end DP guarantee** in this run. The privacy_bound metric is empirical MIA advantage, not a formal bound. The non-private reference matching both paths' MIA confirms we're in "noise too small to matter" territory; a deployable DP comparison needs RDP/PRV accounting + amplification-by-subsampling to set scale at a target ε_total (e.g., 1.0 or 8.0).

3. **n=10 seeds is small; small-sample SE gives the verdict its sharp edge.** The −0.001 utility delta is 1.5 SE wide; with 100 seeds the same effect could become non-significant or could solidify. The MIA delta is ~1 SE, dominated by the Yeom estimator's noise (loss-threshold AUC has high variance; shadow-model MIA per Shokri 2017 is the proper reference). Treat the FALSIFIED label as **strict 1-SE reading**, not as physical evidence that LCG noise hurts logistic regression — the practical conclusion is "indistinguishable at this scale."

## Reproduction

```
cd /Users/ghost/core/anima
KMP_DUPLICATE_LIB_OK=TRUE python3 state/qmirror_dp_noise_2026_05_03/run_dp_compare.py
# ~5 seconds on Mac local, deterministic given seeds [0..9]
```

## Next-step handoff (if pursued)

- **Tier-1 upgrade:** swap `QmirrorByteStream` for `anu_fetch_bytes` (live ANU vacuum-fluctuation QRNG). 360 noise-draws · (D+1)·4 bytes ≈ 30KB total → ~30s rate-limited fetch.
- **Tier-2 upgrade:** add `prv_accountant` or `opacus.accountants.RDPAccountant`, set noise to hit ε_total=8.0; run with subsampling probability q=B/N=0.064. Expect noise to become large enough to actually depress utility — *then* the F-QDP-1 comparison becomes physically meaningful.
- **Tier-3 upgrade:** shadow-model MIA (5 shadow models, train attack classifier on shadow outputs); 100 seeds; report 95% CI not 1-SE.
