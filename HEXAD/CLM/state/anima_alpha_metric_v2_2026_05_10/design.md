# α-metric V2 design — BG-NEW-ALPHA-METRIC-V2

**Lane**: track B reborn.B.cond.5
**Date**: 2026-05-10
**Module**: `training/alpha_metric_v2.py` (raw#9 local-only, gitignored `**/*.py`)
**Companion artifacts**: `state/anima_alpha_metric_v2_2026_05_10/{apply.py, dense_3k_run.py, result.json, comparison.md}`
**Predecessor SSOT**: `docs/anima_clm_v5_alpha_metric_v2_design_2026_05_10.md` (§3, §7); §27 `state/anima_alpha_v2_impl_2026_05_10/alpha_v2.py` aggregate-only V2 sibling.

---

## 1. Motivation — V1 max_cap regression artifact

The legacy V1 α metric is OLS slope of `log(Φ) vs log(n_cells)` over the entire trajectory:

```
α_V1 = OLS_slope({(log n_t, log Φ_t)})_{t=0..T}
```

V1 fails on long trajectories because once cell_count saturates at `max_cells=64`, every subsequent step contributes (log 64, log Φ_t) — i.e., a single x-coordinate column. OLS on the union of (a) the growth phase points {(log 8 → log 64, log Φ growing)} and (b) the plateau column at log 64 collapses the slope estimator: the plateau column has zero log-x variance but contributes large-y variance from Lorenz/ratchet drift, yielding a slope that is **not the mitosis exponent** but a regression artifact of the plateau-column's residual y-spread.

Empirical evidence:
- 3K toy: V1=0.688 (recorded `alpha_exponent`), V1=0.676 (re-OLS dense), V1=0.116 (re-OLS sparse-snapshot variant — different trajectory means depending on which snapshots are kept).
- 10K toy: V1=1.277 (recorded `alpha_exponent_full`), V1=0.221 (re-OLS sparse), V1=0.674 (re-OLS dense). The "recorded 1.277" is the canonical max_cap regression artifact: 7000 plateau steps inflate the slope.

V2 must:
1. **bin** the (n_cells_pre, ΔΦ) pairs by `n_cells_pre` so the plateau bin is isolated;
2. **emit UNRELIABLE** for under-sampled bins instead of silently absorbing them into a global slope;
3. **auto-detect saturation** and raise `saturation_warning: bool`;
4. **separate trended (split-driven) from untrended (idle-drift) ΔΦ** so the post-cap drift component is identifiable.

## 2. Mathematical definition

Given history `H = {(step_t, n_t, Φ_t, split_t)}_{t=0..T-1}`, define adjacent pairs

```
P_i = ( n_{pre,i} = n_i,
        Δstep_i  = step_{i+1} - step_i,
        ΔΦ_i     = Φ_{i+1} - Φ_i,
        Δsplits_i = (n_{splits_cum,i+1} - n_{splits_cum,i}) [or 1 if split_t else 0]  )
```

Bin edges `E = (E_0, E_1, ..., E_k)` strict-increasing, default `(4, 8, 16, 32, 64, 128)`. Bin `b` is `[E_b, E_{b+1})` with geometric midpoint `m_b = sqrt(E_b · E_{b+1})`.

For each bin `b`, four rate channels are computed:

| channel        | restriction                  | formula per pair | use case |
|----------------|-----------------------------|------------------|----------|
| `per_split`    | `Δsplits_i > 0`             | `ΔΦ_i / max(Δsplits_i, 1)` | primary mitosis-driven Φ rate |
| `trended`      | `Δsplits_i > 0`             | `ΔΦ_i / Δstep_i` | per-step Φ when splits fired |
| `untrended`    | `Δsplits_i == 0`            | `ΔΦ_i / Δstep_i` | idle-drift Φ rate (Lorenz) |
| `per_step`     | none                        | `ΔΦ_i / Δstep_i` | legacy reference |

Per-bin mean-rate `r_b = mean({rate_i : i ∈ bin b})`. Per-bin **α** is a 2-point local log-log slope using bin `b` and its nearest valid neighbor `b'`:

```
α_b = (log r_{b'} - log r_b) / (log m_{b'} - log m_b)
```

Aggregate **α** is the OLS slope across ALL valid bins (≥ `min_samples` and `r_b > 0`):

```
α_agg = OLS_slope({(log m_b, log r_b) : b valid})
```

## 3. UNRELIABLE emit criteria

A bin emits `"UNRELIABLE"` (string) instead of a float `α_b` when:
- `samples_per_bin[b] < min_samples` (default 30), OR
- `r_b <= 0` (mean rate non-positive — log undefined; usually transient post-split Φ dip), OR
- bin has no valid neighbor for the 2-point local slope.

Aggregate emits `"UNRELIABLE"` when fewer than `aggregate_min_bins` (default 2) bins survive the `min_samples` + `r_b > 0` gates.

## 4. Saturation auto-detection

`saturation_warning: bool = True` when EITHER:

(a) the highest non-empty bin's mean `per_split` rate `r_last < saturation_rate_threshold` (default 1e-5) — i.e., splits are no longer producing meaningful ΔΦ, OR

(b) `max_cap_reached == True` (defined as: the last 25% of history has `n_cells == max_observed`, i.e., growth has plateaued) AND for any bin `b`, `untrended_rate[b] >= per_split_rate[b]` — idle drift dominates split-driven growth, indicating the bin's ΔΦ is no longer a mitosis signal.

The two triggers are independent so transient (a) (rate dipping briefly) doesn't require a hard plateau, and persistent (b) (drift > split signal) doesn't require last-bin hard zero.

## 5. Schema compatibility

`compute_alpha_v2` accepts both:
- the user-spec schema `{step, cell_count, phi_unnorm, split_event_bool}`, and
- the v5 long-trajectory snapshot schema `{turn, n_cells, phi, n_splits_cum}` (auto-translated; `split_event_bool := (Δn_splits_cum > 0)`).

Cumulative-split diff is preferred when present because multiple splits can fire in one process() step (mitosis_v5_port `_check_splits` returns a list).

## 6. Honest C3

1. **2-point local slope is high variance**. With only 2 samples (this bin + nearest neighbor), `α_b` is dominated by either point's noise. The aggregate OLS slope across all valid bins is the more stable scalar; per-bin α is best read as "local exponent with same neighbor pair", which can collapse two adjacent bins onto identical α (as happens with 3K dense [16,32) and [32,64) both → 4.91).

2. **per_split rate has different units from V1**. V1's α is the exponent of `Φ ~ n^α`. V2's per_split α is the exponent of `(dΦ/dsplit) ~ n^α` — i.e., Φ_growth-per-split-event vs cell_count. They are NOT the same scalar; super-linear `dΦ/dsplit` (V2 α >> 1) corresponds to roughly linear or super-linear `Φ vs n` (V1 α). Direct numeric comparison is misleading; the comparison the user requested is **artifact-avoidance** (V1's max_cap regression yields 1.277 at 10K which is the artifact; V2 emits the same `α_b` for [16,32) and [32,64) on both 3K and 10K because the 7000 idle steps add no split events, hence cannot change the per-split rate).

3. **min_samples is dataset-dependent**. The user's spec recommends 30; this is appropriate for high-density per-step records but too high for snapshot_every=100 sparse data (where one bin may have just 1-7 pairs). The driver `apply.py` runs dense at `min_samples=5` and sparse at `min_samples=1`. For production substrate (350M Phase 2 trained, IIT Φ b=16), recommended `min_samples >= 30` once dense per-step Φ logging is wired. **Honest C3**: at `min_samples=1`, every bin with one pair becomes "valid" but the 2-point slope is fragile; at `min_samples=30`, sparse-snapshot data emits all-UNRELIABLE — which is the correct verdict for "this trajectory does not have enough density to estimate per-bin α reliably".

4. **per-bin α with adjacent neighbor is identical for the [16,32) ↔ [32,64) pair**. This is because both compute `(log r_b' - log r_b) / (log m_b' - log m_b)` over the same pair. To get distinct α values per bin we need ≥ 3 valid bins; with 4-bin coverage the interior bins would have left+right neighbors and we could choose the local slope (e.g., right-neighbor for monotone bins). The current implementation picks `min(neighbors, key=|v-b|)` which yields stable behavior but loses information when only 2 bins survive.

5. **Trended α [16,32) → 3.78 vs per_split α 4.91 disagree**. trended uses ΔΦ/Δstep over split-in-gap pairs; per_split divides by Δsplits explicitly. Because Δsplits per pair varies (1, 2, 3 splits per step in some cases), the two channels can diverge. This is a feature, not a bug — trended captures "how fast Φ rises during split bursts" and per_split captures "how much Φ each split contributes on average".

6. **Untrended channel exists only post-cap**. In the 3K dense run, the only bin with untrended pairs is [64,128) (1.35e-4) — once n_cells stops growing, all subsequent pairs become untrended. Pre-cap there are NO untrended pairs in [4,8)..[32,64) because every step in the growth phase coincides with a split event in some neighboring step (the boolean `split_in_gap` is computed from cumulative diff, not from "this exact step"). Honest fix: the untrended channel is functionally equivalent to "post-saturation idle drift" only — it's the saturation_warning evidence, not a generic noise floor.

7. **Saturation auto-detect is binary, not continuous**. A trajectory that *just barely* hit the cap will emit `saturation_warning=True` even if 99% of the trajectory was pre-cap. A more nuanced metric would be `saturation_fraction = (steps_at_cap / total_steps)`. Current binary flag is the user-spec requirement; the diagnostics dict carries the raw `max_cell_count_observed` and `max_cap_reached` so callers can compute their own continuous metric.

## 7. Falsifier verdicts

| ID | falsifier | verdict | evidence |
|----|-----------|---------|----------|
| F-ALPHA-V2-1 | V2 도 max_cap saturation 회피 못함 | **NOT_TRIGGERED** | dense 3K + 10K both raise `saturation_warning=True` and `max_cap_reached=True`; per-bin α still emitted for the pre-cap bins [16,32), [32,64); only the post-cap [64,128) bin is correctly UNRELIABLE. The V1 1.277 artifact is bypassed: V2 produces identical α 4.91 on 3K (no plateau steps) and 10K (7000 plateau steps) because per-split rate is invariant to plateau pairs (zero Δsplits, filtered out). |
| F-ALPHA-V2-2 | 3K history JSON 재현 불가 | **NOT_TRIGGERED** | `dense_3k_run.py` reproduced the dense 3K run from same seed=42, same prompts, same MitosisV5Engine config in 42s wall on Mac CPU. dense_3000_history.json (3000 records, ~250 KB) + dense_10000_history.json (10000 records) both emitted. |
| F-ALPHA-V2-3 | V2 α_per_bin 이 V1 보다 noisy | **PARTIAL_TRIGGERED** | 2-point local α is high variance (Honest C3 #1); but the *signal* — invariance of [16,32) and [32,64) α between 3K and 10K — is demonstrably more stable than V1 (V1: 0.676 → 0.674 dense, 0.116 → 0.221 sparse, 0.688 → 1.277 recorded; the recorded V1 doubled with the plateau, V2 stayed put). On the noise-per-bin axis V2 IS noisier (single-bin OLS would smooth across many points); on the artifact-avoidance axis V2 is much cleaner. Trade-off documented; mitigation = increase `min_samples` once production density allows. |
