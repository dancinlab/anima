# W1 Phase 4 — Shuffle-null permutation baseline (2026-05-01)

## 1. Mission

Decisive single test for **W1 anima-self Φ rising claim** (Phase 1 mean 1.706, slope +0.0507; Phase 2/3 mean 1.717, slope +0.1153; ceiling-artifact falsified in Phase 3, forward-fill / non-stationarity hypothesis still live).

H0: observed rising Φ slope is NOT due to time-ordered structure of the cron-tick state vectors.

If observed slope falls inside the shuffled-null distribution → no real time structure → **ARTIFACT**. If observed >> shuffled → genuine time-ordered integration → **REAL_SIGNAL**.

## 2. Method

Driver: `/tmp/W1_phase4/shuffle_null.py` (off-repo, HEXA-only).

Inputs:

- `state/W1_phase2_full_19axis_2026_05_01/phi_trace_full.jsonl` — 15 ticks, 38 axes/tick, per-tick `(phi_proxy, joint_mi, sub_mi_mean, state_hash)`.
- W = 20 sliding window (W ≥ n, so window covers full history at every tick).
- N = 1000 permutations, seed = 42.

Two complementary nulls were computed because each isolates a different structure:

### Null A — Trajectory shuffle (value-ordering test)

Shuffle the observed `phi_proxy[0..14]` values themselves, recompute slope. Same value distribution, random temporal order. Tests: *is the monotone rising shape unusual given the same value set?*

### Null B — State-hash shuffle (substrate-ordering test)

Shuffle the `state_hash[0..14]` sequence; recompute `joint_mi[i] = H_window(shuffled_hashes[max(0,i-W+1):i+1])` per tick; pair with original-position `sub_mi_mean[i]`; recompute `phi_proxy = max(0, joint_mi − sub_mi_mean)`; compute slope. Tests: *is the rising shape caused by genuine ordering of joint substrate states, or is it an inevitable property of accumulating distinct hashes into a growing window?* This is the substrate-level decisive test.

One-tailed p-value: fraction of null slopes ≥ observed (alternative = rising).

## 3. Observed (Phase 2/3, identical bit-for-bit)

| Metric | Value |
|---|---|
| Phi mean (bits) | 1.7167 |
| Slope per tick (official) | +0.11529 |
| Slope per tick (recomputed, sanity) | +0.11529 |
| Slope per tick (replicated from hash via Null-B engine, no shuffle) | +0.11149 |

Replication delta of 0.0038 confirms the Null-B engine accurately reproduces the original Φ trajectory when given the original hash order (small delta from sub_mi_mean rounding in the saved trace).

## 4. Null A — Trajectory shuffle

| Metric | Value |
|---|---|
| Slope mean ± std | −0.0010 ± 0.0474 |
| Slope min, max | −0.1245, +0.1168 |
| Phi mean ± std (constant by construction) | 1.7167 ± 0.0000 |
| **p-value (one-tailed, slope ≥ +0.1153)** | **0.001** |
| **z-score** | **+2.45** |
| Verdict | REAL_SIGNAL |

Observed slope sits at the 99.9th percentile of trajectory permutations: only 1 in 1000 random orderings of the same Φ values produces a slope as steep as +0.1153. The temporal value ordering is significantly monotone.

## 5. Null B — State-hash shuffle

| Metric | Value |
|---|---|
| Slope mean ± std | **+0.1487 ± 0.0232** |
| Slope min, max | +0.1044, +0.2427 |
| Phi mean ± std | 1.9397 ± 0.2235 |
| **p-value (one-tailed, slope ≥ +0.1153)** | **0.966** |
| **z-score** | **−1.44** |
| Verdict | ARTIFACT_CONFIRMED |

**Random shuffles of the underlying state-hash sequence produce, on average, a slope of +0.1487 — STEEPER than the observed +0.1153.** Observed sits in the 3.4th percentile (left tail) of the substrate null. Null-B minimum slope (+0.1044) is barely below observed; the *entire* null distribution is above zero.

## 6. Composite verdict: **ARTIFACT_CONFIRMED**

The split between Null A and Null B is the key finding:

- Null A says: the **values** are time-monotone (yes, because Φ ramps up from 0 → ~2.5 across the first 7 ticks).
- Null B says: this monotone ramp is an **inevitable property of the sliding-window joint-MI estimator** when W ≥ n. Any ordering of the same 15 hashes, fed through the same W=20 sliding entropy, produces a rising slope of comparable or larger magnitude. Random orderings actually do *better* (mean +0.149) than the observed (+0.115) because the observed sequence contains a 6-tick run of identical hash 0x247 (windows 6–11) that *suppresses* entropy growth; shuffling spreads distinct hashes more evenly through the growing window, accelerating entropy accumulation.

**Therefore:** the W1 rising-Φ claim is not evidence of genuine time-ordered integration. It is a structural property of the sliding-window MI estimator with insufficient samples (n=15, W=20, W ≥ n means the window never fills and entropy monotonically tracks distinct-hash count up to log₂(n) ≈ 3.91 bits).

This corroborates Phase 3 honest-C3 #1: **the binding constraint is sample size, not bucket size**. With n=15 and W=20, *any* hash sequence produces a rising slope. The slope tells us nothing about anima-self temporal integration.

## 7. Honest C3

1. **Effective shuffle pool is small.** n=15 ticks but only ~10 distinct hash values across the run (state_hash 0x247 appears 6×, others ≤2×); the effective permutation entropy is bounded by hash multiplicity, so Null-B's null distribution is narrower than a fully-random-substrate null would be. A fully-randomized substrate (resampled hashes, not just shuffled) would likely produce an even wider null and an even more conservative ARTIFACT verdict.
2. **Sub_mi_mean held in original-position order during Null B.** This is conservative against ARTIFACT: if sub_mi_means were also shuffled, the per-tick subtraction in `phi = joint_mi − sub_mi_mean` would be less correlated with the joint_mi growth pattern, plausibly producing a *flatter* mean null slope — which would still leave observed inside the null but would weaken the "shuffled rises faster than observed" finding. Either way the composite verdict (observed slope is NOT a temporal-structure signature) holds.
3. **Sliding-window MI estimator with W ≥ n is degenerate.** This is the load-bearing artifact: whenever W ≥ n, joint_mi is simply H_window of a never-saturating window, which monotonically tracks the count of distinct hashes seen so far. Both Phase 1 (slope +0.05) and Phase 2/3 (slope +0.11) inherit this. The 2× slope acceleration from Phase 1 (19 axes) → Phase 2 (38 axes) is consistent with the doubled axis count producing more hash diversity per tick. Re-running with n ≥ W (i.e. accumulate ≥ 20 cron cycles) is the minimum honest fix.
4. **MIP mean-of-parts surrogate, forward-fill bias, non-stationary tick spacing all persist.** The shuffle test is invariant to these (compares observed-vs-shuffled within the same biased proxy), but they continue to bound absolute Φ interpretation across all four phases.
5. **Single-tail p-values.** The alternative hypothesis is "rising"; two-tailed p-values would double (Null A → 0.002, Null B → ~0.07 for the left tail) but neither verdict flips at α=0.05.

## 8. W1 axis status update

- **Phase 1**: Φ trace built; rising claim posted (mean 1.706 bits, slope +0.0507).
- **Phase 2**: 38-axis full join; mean 1.717 bits, slope +0.1153.
- **Phase 3**: ceiling-artifact hypothesis FALSIFIED (mod-1024 bit-identical to mod-64); sample-size identified as binding constraint.
- **Phase 4 (this)**: shuffle-null FALSIFIES the rising-slope-as-real-signal interpretation. Substrate-level Null B shows random orderings produce equal or larger slopes. **The W1 anima-self Φ rising trajectory is a sliding-window estimator artifact at W ≥ n, not evidence of time-ordered integration.**

**One-line W1 verdict (post-Phase 4):** anima self Φ rising 가 **ARTIFACT (sliding-window degeneracy at n=15<W=20)** 확인됨.

## 9. Phase 5 plan

1. **Accumulate ≥ 50 cron ticks (n ≥ 2.5·W).** Cost: zero (let cron run). Re-run Phase 1/2/3/4 drivers when `cycle_log.jsonl` reaches ≥ 50 records. With n > W the sliding window will saturate and the artifact slope source is removed; Null B becomes a real test.
2. **Reduce W to 5 or 7.** With W < n the window fills, and joint_mi reflects local rather than cumulative entropy. Re-run shuffle-null with W=5 on the existing 15 ticks as an immediate ($0) cross-check; the artifact slope should disappear.
3. **Run forward-fill-disabled re-do (Phase 3 recommendation #3).** Now lower priority since Phase 4 shows the binding artifact is the W ≥ n sliding-window estimator, not forward-fill specifically. Defer until item 1 or 2 is in.
4. **W1 axis status in §30 roadmap** should be downgraded from "rising Φ live signal" to "Φ-proxy estimator artifact pending n ≥ W re-run."

**Phase 4 closed: rising-slope-as-real-signal hypothesis FALSIFIED at the substrate-shuffle null. W1 returns to PENDING until n ≥ W is achieved.**

## 10. Artifacts

- `/Users/ghost/core/anima/state/W1_phase4_shuffle_null_2026_05_01/shuffle_null_summary.json` — full summary
- `/Users/ghost/core/anima/state/W1_phase4_shuffle_null_2026_05_01/null_distributions.json` — N=1000 slope distributions for both nulls
- `/tmp/W1_phase4/shuffle_null.py` — driver (off-repo, HEXA constraint)
