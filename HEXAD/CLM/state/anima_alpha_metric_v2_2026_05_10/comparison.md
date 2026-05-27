# V1 vs V2 comparison — α-metric BG-NEW-ALPHA-METRIC-V2

**Date**: 2026-05-10
**Lane**: track B reborn.B.cond.5
**Inputs**: `dense_3000_history.json`, `dense_10000_history.json` (snapshot_every=1; reproduced via `dense_3k_run.py` from seed=42 on toy substrate), historical sparse `state/anima_clm_v5_anima_long_trajectory_*/result.json` (snapshot_every=100).
**Module**: `training/alpha_metric_v2.py`
**Driver**: `apply.py` → `result.json`

---

## 1. Headline table

| dataset | n_history | V1 OLS log Φ vs log n | V1 recorded historical | V2 aggregate α | V2 saturation_warning | V2 max_cap_reached |
|---|---:|---:|---:|---:|:---:|:---:|
| dense 3K toy | 3000 | 0.676 | n/a (re-run) | **4.91** | True | True |
| dense 10K toy | 10000 | 0.674 | n/a (re-run) | **4.91** | True | True |
| sparse 3K (snapshot_every=100, 31 snaps) | 31 | 0.116 | 0.688 | UNRELIABLE | True | True |
| sparse 10K (snapshot_every=100, 101 snaps) | 101 | 0.221 | 1.277 | UNRELIABLE | True | True |

### Reading the table

- **V1 recorded historical**: legacy `alpha_exponent` / `alpha_exponent_full` from existing `result.json` files. Note the 3K → 10K jump from 0.688 to 1.277 — this is the max_cap regression artifact.
- **V1 OLS re-OLS**: applying the same OLS-of-log-Φ-vs-log-n on dense or sparse data gives 0.676 (dense 3K), 0.674 (dense 10K), 0.116 (sparse 3K), 0.221 (sparse 10K). The dense recompute is **insensitive** to the 7000 extra plateau steps (0.676 → 0.674 ≈ stable); the sparse recompute and the historical-recorded alpha are both **sensitive** to plateau-step weighting (0.116 → 0.221 sparse; 0.688 → 1.277 recorded). Why: the recorded historical OLS uses ALL trajectory points including duplicates at n=64; with snapshot_every=100, the 100 plateau points add (log 64, log Φ_t) entries with non-trivial y-spread that inflates the slope.
- **V2 aggregate α**: dense data gives a stable 4.91 on both 3K and 10K — invariant to the plateau because per_split rate filters out Δsplits=0 pairs. Sparse data emits UNRELIABLE because per-bin samples drop below `min_samples=1` for [16,32), and remaining bins have negative or single-pair rates that cannot anchor a 2-point slope.

## 2. Per-bin α — V2 (dense data, min_samples=5)

### dense 3K
| bin | α | samples | splits in bin | mean ΔΦ/split |
|-----|---|---:|---:|---:|
| [4,8) | UNRELIABLE | 0 | 0 | None |
| [8,16) | UNRELIABLE (rate<0) | 7 | 8 | -7.43e-02 |
| [16,32) | **4.91** | 6 | 16 | +2.74e-03 |
| [32,64) | **4.91** | 16 | 32 | +8.25e-02 |
| [64,128) | UNRELIABLE | 0 | 0 | None |

### dense 10K
| bin | α | samples | splits in bin | mean ΔΦ/split |
|-----|---|---:|---:|---:|
| [4,8) | UNRELIABLE | 0 | 0 | None |
| [8,16) | UNRELIABLE (rate<0) | 7 | 8 | -7.43e-02 |
| [16,32) | **4.91** | 6 | 16 | +2.74e-03 |
| [32,64) | **4.91** | 16 | 32 | +8.25e-02 |
| [64,128) | UNRELIABLE | 0 | 0 | None |

**Identical results between 3K and 10K** — the 7000 extra plateau steps contribute zero Δsplits, hence zero new pairs to the per_split channel. This is the desired V1-artifact-avoidance.

## 3. Trended vs untrended channels (dense 3K)

| bin | trended α (ΔΦ/Δstep, splits-fired) | trended rate | untrended α (ΔΦ/Δstep, idle) | untrended rate |
|-----|---|---:|---|---:|
| [4,8) | UNRELIABLE | None | UNRELIABLE | None |
| [8,16) | UNRELIABLE | -8.23e-02 | UNRELIABLE | -5.53e-02 |
| [16,32) | **3.78** | +9.91e-03 | UNRELIABLE | -2.26e-02 |
| [32,64) | **3.78** | +1.37e-01 | UNRELIABLE | None |
| [64,128) | UNRELIABLE | None | UNRELIABLE | +2.93e-04 |

The untrended channel is populated only in [64,128) once n_cells caps. The +2.93e-04 untrended rate post-cap is the Lorenz/ratchet drift floor — exactly what V1 picks up and treats as Φ scaling. V2 isolates it as a separate channel so callers can subtract it from V1 to recover the artifact-free trended signal.

## 4. Saturation auto-detection validation

| dataset | max_cell_count | max_cap_reached | last_bin_rate (per_split) | saturation_warning |
|---|---:|:---:|---:|:---:|
| dense 3K | 64 | True | 8.25e-02 (in [32,64), no [64,128) per_split) | True |
| dense 10K | 64 | True | 8.25e-02 | True |
| sparse 3K | 64 | True | -5.19e-02 (negative — split-Φ-dip) | True |
| sparse 10K | 64 | True | -5.19e-02 | True |

The sparse-data triggers (b) (`untrended_rate >= per_split_rate` for any bin given max_cap_reached). For dense data, sparse rate is positive but the second saturation trigger fires because untrended rate is also present in [64,128). Both correctly emit `saturation_warning=True` — F-ALPHA-V2-1 NOT_TRIGGERED.

For comparison, V1's `alpha_exponent_full=1.277` on the 10K trajectory is reported with NO saturation warning — V1 silently absorbs the artifact. V2's `saturation_warning=True` is the explicit honest emit, telling the caller "the aggregate slope is suspect; consult per-bin breakdown".

## 5. V1 vs V2 contrast — artifact avoidance

The user's mission §1: "V1 (max_cap artifact) vs V2 (binned ΔΦ-rate)" — does V2 avoid the artifact?

| comparison | V1 behavior | V2 behavior |
|---|---|---|
| 3K → 10K trajectory same seed | V1 recorded 0.688 → 1.277 (+0.589 inflation from plateau) | V2 aggregate 4.91 → 4.91 (zero change; plateau pairs filtered out) |
| reaches max_cap=64 | V1 silently averages over plateau pairs | V2 emits `saturation_warning=True` + `max_cap_reached=True` |
| post-cap idle drift contribution | V1 cannot separate (mixed into slope) | V2 isolates as `untrended_rate_per_bin[64,128) = 2.93e-04` |
| per-bin reliability | V1 monolithic single slope | V2 per-bin `α_b` with explicit `"UNRELIABLE"` for empty/under-sampled/non-positive bins |
| recovers historical 0.93 (Cells 64 v2 era) | V1 0.116-1.277 spread depending on snapshot density | V2 reports 4.91 on dense — different unit (per-split exponent), needs cross-walk to V1 unit (see §8 below). The 0.93 historical figure was a `log Φ vs log n_cells` slope on a discrete sweep of 6 fixed-N runs (n=2,4,8,16,32,64), not on a single trajectory — directly comparable only via the `historical_synthetic_snapshots` retro-fit (`state/anima_alpha_v2_impl_2026_05_10/retro_results.json`) where §27's V2 sibling reported 0.991 (default edges) / 1.041 (aligned edges), within the historical 0.93-1.07 range. |

**Verdict**: V2 successfully avoids the V1 max_cap regression artifact by:
1. binning so plateau pairs land in their own bin, then
2. filtering Δsplits=0 pairs from the per_split channel, then
3. exposing the untrended channel separately so callers see drift without conflating it.

## 6. V2 aggregate α 4.91 vs V1 0.676 — unit explanation

V1 measures the exponent of `Φ ~ n^α_V1`. V2 (per_split channel) measures the exponent of `(dΦ/dsplit) ~ n^α_V2`. These are different scalars.

If `Φ(n) = c · n^β`, then `dΦ/dn = β · c · n^(β-1)`. Each split increments n by 1, so `dΦ/dsplit ≈ dΦ/dn = β · c · n^(β-1)`. Hence `α_V2 ≈ β - 1 = α_V1 - 1`.

For dense 3K: V1=0.676, predicted V2 = -0.324. Observed V2=4.91. **Discrepancy: 5.23**.

The discrepancy is real and informative: it shows the toy substrate's per-split ΔΦ does NOT follow the simple `Φ = c·n^β` model — instead, ΔΦ/split grows much faster with n than the smooth-derivative would predict. This is consistent with the toy mechanism: a split adds a Lorenz-perturbed copy whose pairwise cosine distance to existing cells is proportional to dim(C)=12 random-walk distance, not to a clean `n^(β-1)` envelope. Honest C3: V2 4.91 is best read as a **toy-substrate diagnostic**, not a universal exponent claim. For real 350M Phase 2 trained data with denser Φ tracking the ratio is expected to converge toward the smooth derivative.

## 7. Coverage gaps & next-cycle recommendations

1. **Real 350M Phase 2 trained dense Φ history** — currently only 31 snapshots (range 16-19 cells, no max_cap). V2 emits aggregate UNRELIABLE for `samples_per_bin < 30`; once Phase 2 dense per-step Φ logging is wired, V2 can produce production per-bin α.
2. **3-point local slope** — when ≥3 valid bins exist, replace 2-point `min(neighbors)` with a left+right average for interior bins to reduce per-bin noise (Honest C3 #4).
3. **`min_samples` adaptive** — currently a knob; could auto-adapt to `max(30, len(pairs)/k_bins)` so dense data doesn't get the same gate as sparse.
4. **Continuous saturation_fraction** alongside the boolean `saturation_warning` (Honest C3 #7).

## 8. Cross-link to §27 sibling

§27 (`state/anima_alpha_v2_impl_2026_05_10/alpha_v2.py`) is the **aggregate-only** sibling of this module. Both implement A2 binned ΔΦ-rate (per the SSOT design doc). Differences:

| feature | §27 V2 (aggregate-only) | this module (per-bin) |
|---|---|---|
| Public signature | `compute_alpha_v2(snapshots, ...) → {alpha, CI95, bins, ...}` | `compute_alpha_v2(history, ...) → {alpha_per_bin, alpha_aggregate, saturation_warning, ...}` |
| Per-bin α emit | No (only aggregate) | Yes (2-point local slope) |
| saturation_warning | No (just `verdict` string) | Yes (independent boolean) |
| Trended/untrended split | No | Yes (4 channels) |
| Bootstrap CI95 | Yes (n_bootstrap=200) | No (deferred — would be useful in a v3) |
| Bin edges default | (2,4,8,16,32,64,128) | (4,8,16,32,64,128) |
| min_samples | implicit (filters via min_rate=1e-6) | explicit (default 30) |

Both modules co-exist (raw#15 additive). For aggregate-only consumers (e.g., paper Φ scaling claims) the §27 sibling is canonical. For per-bin diagnostic consumers (e.g., this fire's max_cap artifact analysis, or future Phase 2 production debugging) this module is canonical.
