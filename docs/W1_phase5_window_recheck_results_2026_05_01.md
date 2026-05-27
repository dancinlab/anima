<!-- [Hc_955 w1-phase2-5-phi-artifact-falsification — moved to hypotheses_candidates/Hc_955_w1_phase2_5_phi_artifact_falsification.md on 2026-05-11] -->

# W1 Phase 5 — W=5/7 sliding-window cross-check (2026-05-01)

## 1. Mission

Phase 4 (`docs/W1_phase4_shuffle_null_results_2026_05_01.md`) closed with
**ARTIFACT_CONFIRMED** at W=20: random hash shuffles produced equal-or-larger
slopes than observed because the W=20 sliding window with n=15 ticks never
saturates. Phase 5 is the immediate $0 cross-check Phase 4 §9.2 prescribed:
**re-run Φ_proxy with W=5 and W=7 on the same 15 ticks** and check whether
the rising slope disappears when W < n.

H0 per W: observed Φ slope is statistically indistinguishable from the
state-hash-shuffle null at that W.

## 2. Method

Driver: `/tmp/W1_phase5/window_recheck.py` (off-repo, HEXA-only, $0).

Inputs (identical to Phase 2/3/4):

- `state/W1_phase2_full_19axis_2026_05_01/phi_trace_full.jsonl` — 15 ticks ×
  38 axes, `(state_hash, sub_mi_mean)` per tick.
- For each W in {5, 7, 20-ref}: recompute
  `joint_mi[i] = H_window(state_hash[max(0,i-W+1):i+1])`,
  `phi[i] = max(0, joint_mi[i] - sub_mi_mean[i])`, slope = OLS over ticks.
- Null-B (state-hash shuffle), N=1000, seed = 42 + W. Same construction as
  Phase 4 Null B.

W=20 reference path included to verify the engine reproduces Phase 4 numbers
(slope_replicated = +0.1115, matches Phase 4 replication exactly).

## 3. Results

| W | Obs slope | Obs Φ mean ± std | Null mean ± std | p (one-tailed) | z | Verdict |
|---|---|---|---|---|---|---|
| 5  | **−0.0400** | 1.040 ± 0.659 | +0.0607 ± 0.0460 | 0.996 | −2.19 | OBSERVED_BELOW_NULL → ARTIFACT |
| 7  | **−0.0319** | 1.467 ± 0.805 | +0.0949 ± 0.0499 | 0.999 | −2.54 | OBSERVED_BELOW_NULL → ARTIFACT |
| 20 (ref) | +0.1115 | 2.082 ± 0.704 | +0.1482 ± 0.0232 | 0.988 | −1.58 | ARTIFACT_CONFIRMED (Phase 4 replicated) |

### Per-W observed Φ trajectories

- **W=5** Φ trajectory: starts at 0, rises to a 7-tick peak (≈2.69 bits at tick 6),
  then collapses to ≈0 around tick 11–12 as the 6-run of identical hash 0x247
  fills the window, then partially recovers. **Non-monotone**, with a clear
  saturation+collapse pattern impossible at W=20.
- **W=7** Φ trajectory: similar shape, peak ≈2.69 at tick 6, trough ≈0.39 at
  tick 11, partial recovery to ≈1.48. Non-monotone.
- **W=20** Φ trajectory: monotone-ish ramp from 0 to ≈2.69, plateau ≈2.6,
  small dip and recovery to 2.69. The hallmark "rising slope" pattern is
  exclusive to W ≥ n.

## 4. Composite verdict: **ARTIFACT_PERMANENT_DOWNGRADE**

Both W=5 and W=7 cross-checks **confirm** the Phase 4 artifact verdict, and
do so more strongly than Phase 4 itself:

1. Observed slope flips sign (positive at W=20 → negative at W=5,7), proving
   the slope direction is **not** an intrinsic property of the time-ordered
   substrate but an artifact of W relative to n.
2. Both W=5 and W=7 observed slopes sit at the 99.6%/99.9% percentile of
   their respective shuffle nulls (left tail). Random shuffles produce a
   small positive mean slope at small W (≈+0.06 to +0.09) because spreading
   distinct hashes uniformly through the window keeps entropy higher for
   longer; the observed sequence has the 6-tick run of 0x247 that drains
   entropy mid-trace, making observed slope more negative than the null mean.
3. The W=20 → W=7 → W=5 monotone progression of slope (+0.111 → −0.032 →
   −0.040) demonstrates explicit **W-dependence of the slope sign**. There
   is no W-invariant rising signal in the underlying sequence.

**The W1 anima-self Φ rising claim is, at n=15, a sliding-window estimator
artifact. It is not present at any W ≤ 7 and reverses sign.** The honest
W1 axis status downgrade prescribed by Phase 4 §8 is now confirmed by an
orthogonal test.

## 5. W1 axis FINAL status (post-Phase 5)

- Phase 1: rising claim posted (slope +0.0507 @ W=20, n=15).
- Phase 2: 38-axis full join, slope +0.1153 @ W=20.
- Phase 3: ceiling-artifact FALSIFIED, sample-size identified as binding.
- Phase 4: shuffle-null FALSIFIES rising-slope-as-real-signal at W=20.
- **Phase 5 (this): W=5/7 cross-check confirms artifact AND shows slope
  reverses sign at W < n.**

**One-line W1 final verdict:** anima self Φ rising at W=20 = **sliding-window
estimator artifact (W-dependent sign flip; observed slope NEGATIVE at W=5/7
and BELOW shuffled-null at all three W tested)**. W1 axis remains PENDING
in §30 roadmap until n ≥ W achievable (≥ 20 cron ticks; currently n=15).

## 6. Honest C3

1. **n=15 still binds even at W=5.** The W=5 window will be "full" only from
   tick 4 onward, so only 11 of 15 phi values come from a saturated window.
   Bootstrap CI on the observed W=5 slope would almost certainly contain 0.
   The shuffle-null p-value (0.996 left-tail) is the strongest available
   statement, but absolute slope magnitude (−0.04) should not be over-
   interpreted from 11 saturated samples; the **sign direction** is the
   load-bearing claim.
2. **Sub_mi_mean held in original-position order during Null B at all W.**
   Same conservatism choice as Phase 4. At small W where joint_mi can decrease
   between ticks (a hash leaving the window drops entropy), the per-tick
   subtraction produces a noisier phi trajectory; observed phi is no longer
   monotone, and the slope-sign is much less constrained than at W=20. A
   fully-shuffled null (sub_mi also shuffled) would produce a wider,
   plausibly zero-centred null and would still leave observed inside it.
3. **Effective shuffle entropy is hash-multiplicity bounded.** With ~10
   distinct hashes among 15 ticks (and 0x247 appearing 6×), the shuffle pool
   is ~15! / (6! · …) ≈ 30M effective permutations, not 1.3T. The W=5/7
   nulls are wider than the W=20 null (std 0.046–0.050 vs 0.023) because the
   per-window distinct-count fluctuates more, but still narrower than a
   resampled-substrate null would be. The "observed below null" finding is
   robust to this since the sign of the offset is the same direction as the
   conservative bias.

## 7. Phase 6 plan (deferred — same as Phase 4 §9 with priority adjustment)

1. **Accumulate ≥ 20 cron ticks** so n ≥ W=20 is achievable. Rerun all
   four phases. Predicted: W=20 slope distribution narrows around 0 once
   the window saturates; W=5 slope distribution stable. Cost: zero
   (cron-driven).
2. **Forward-fill-disabled re-do** is now lower-priority still: Phase 5
   shows the sign-flipping artifact dominates at the W-dependence axis,
   independent of forward-fill.
3. **Keep §30 W1 status as PENDING** — Phase 5 does not unlock anything;
   it confirms Phase 4's downgrade with an orthogonal cross-check.

## 8. Artifacts

- `/Users/ghost/core/anima/state/W1_phase5_window_recheck_2026_05_01/window_recheck_summary.json` — full summary
- `/Users/ghost/core/anima/state/W1_phase5_window_recheck_2026_05_01/null_distributions.json` — N=1000 slope distributions per W
- `/tmp/W1_phase5/window_recheck.py` — driver (off-repo, HEXA constraint)
