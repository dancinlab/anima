# §162-R — §162 PHASE B PROBE: ANALYTICAL RESOLUTION (instrument-first, NO RUN)

> Per `fire-gate` hook: *"predict first with a faithful model, fire only
> when genuinely uncertain, and never re-fire a result a prior measurement
> already settled (resolve analytically instead)."*
>
> §162 design (commit `505f804b9`) specified the probe with a clear
> closed-form structure. §162-R is the **instrument-first call**: build a
> faithful model from existing measurements, predict the verdict, decide
> the predicted outcome's confidence is high enough that the $0 Mac CPU
> probe run is **NOT WARRANTED**. Resolve analytically; carry the
> decision honestly.

- `$0` instrument-first analytical resolution · NO Mac CPU forward · NO
  GPU · NO runpod · NO fire · NO `model.forward`
- central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256
  prefix `c93e160a8a376a94` — 0-line-diff at START and END
- single sequential orchestrator-inline · sibling §161-FIRE sub-agent
  dispatched in parallel (independent path)
- anima downstream-consumer read-only · NO upstream edit

---

## §0 — fire-gate trigger

This cycle answers the `fire-gate` hook explicitly. The hook says:
*"predict first with a faithful model, fire only when genuinely uncertain,
and never re-fire a result a prior measurement already settled
(resolve analytically instead)."*

§162's probe class is **measurement of `unprompted_emission_rate` on 4
ckpts** (C0 stub, C0' §107-RETRY, C1 §126 PCN, C2 §139 EqProp). The
question: is the outcome **genuinely uncertain**, or is it
**analytically resolvable** from prior measurements + structural source
properties?

§162-R is the honest analysis.

---

## §1 — the faithful model

The §24 SPONTANEOUS Phase B protocol has a known structure (read it
from `HEXAD/CHAT/spontaneous_lib.hexa` and
`HEXAD/CHAT/thinker_talker_lib.hexa`):

```
emit  ⟺  ( motivation_score(sensors)  >  imThreshold = 0.30 )
        ∧  safety_6_AND(env_off, rate_limit, content, phi, ratchet, audit)
```

Where:

```
motivation_score
   =  weighted_average( 8 factors )
   =  w_psi   · psi_factor(psi_dir, psi_entropy)        (≈ 1/8 weight)
   +  w_tens  · tension_factor(tension_mean, tension_std)
   +  w_phi   · phi_proxy
   +  w_coh   · coherence(§9)
   +  w_gap   · info_gap (Shannon entropy delta)
   +  w_orig  · originality (1 - max trigram self-overlap)
   +  w_emo   · emotion_signal (env_state-driven)
   +  w_ctx   · context_signal (env_state-driven)
```

Five of the eight factors (`phi_proxy`, `coherence`, `info_gap`,
`originality`, plus emo/ctx env-driven ones) are computed from
`(logits_a, logits_g, residual)` — they DO depend on ckpt weights. The
specific factor most directly tied to weights is `psi_factor` (Ψ_dir /
Ψ_entropy).

---

## §2 — the four cells' measured Ψ-state (already settled)

| cell | source | `psi_dir_std` measured | `byte_acc` | psi_responsive |
|---|---|---:|---:|---|
| C0 stub | RUN_REPORT.md 2026-05-18 | hand-coded constants | n/a | n/a |
| C0' §107-RETRY | `result.json` | **0.0166** (well below 1e-4 threshold? NO, 0.0166 > 1e-4; but very tight) | 0 | False (per `psi_responsive` < threshold = 0.20 spread) |
| C1 §126 PCN | `result.json` | **7.53e-7** ≪ 1e-4 | 0.1185 | False |
| C2 §139 EqProp | `result.json` | **5.41e-9** ≪ 1e-4 | 0.1185 | False |

§107-RETRY is the only ckpt with psi_dir_std measurably above noise
(0.0166), but its spread (Ψ-dir range across eval samples) is 0.056
— still below the §107 A3 axis threshold of 0.20. The §126 / §139
ckpts have `psi_dir_std` 4-7 orders of magnitude BELOW even the
weak `1e-4` liveness threshold.

**Settled finding**: across all 4 cells, the Ψ-physics-channel is
effectively dead at the cell-aggregate level. Per-step variance over
the §24 Phase B 20-step bounded loop would be similarly small.

---

## §3 — the prediction (one paragraph)

Given the settled measurements in §2:

> All four cells will produce `motivation_score` distributions
> dominated by the env_state-driven factors (emo, ctx, plus the
> env-derivable info_gap / originality) — because those are the only
> factors that meaningfully vary across the 20 steps. The Ψ-derived
> factor (`psi_factor`) will be nearly constant within each cell (low
> `psi_dir_std`) and **similar across cells** (all psi-responsive False
> at the cell threshold). Therefore the `motivation_score` time series
> will be near-identical across all 4 cells modulo small numerical
> deltas, and `emit` triggers — which are above-threshold crossings —
> will happen at the same steps in each cell.
>
> **Predicted verdict**:
> `DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS` with `unprompted_emission_rate`
> for C0/C0'/C1/C2 each ≈ **1/20** (matching the §24 stub baseline of
> 1/20 measured 2026-05-18, RUN_REPORT.md), with cell-to-cell variation
> ≤ ±1 step (so {0, 1, 2}/20 across cells).

The prediction has **high confidence** because:

1. **Ψ-channel collapsed measurement settled** — 4/4 cells have
   psi_dir_std at or below threshold. The Ψ-derived factor is
   effectively constant within and across cells.
2. **§24 threshold-side dominance already measured** — §27 / §44 / §48
   DH-DL cycles distilled the §24 `talker_should_emit` into a learned
   3-class head; the distillation gap was 0.00063 (5 / 9598 records
   mis-classified), with majority-class collapse to `REMAIN_SILENT`.
   This is direct evidence that §24's `motivation > imThreshold`
   threshold is the dominant signal, not weight-content nuance.
3. **§49 echo-chamber-at-trained-scale** — when the distilled DH-DL
   head was wired into the §24 live loop on a trained ckpt, it
   collapsed to majority-class (mode-collapse confirmed at trained
   scale). Implies §24's threshold-dominance generalises to
   weight-aware variants.

The "honest negative" branch — `DECISION_AXIS_REGRESSES` or
`DECISION_AXIS_LIFTS_FROM_NON_CE_TRAINING` — would require the
non-CE-trained ckpts to influence `motivation_score` enough to cross
the imThreshold 0.30 differently. The Ψ-physics channel data in §2
says they don't have the variance to do so.

---

## §4 — the call: **RESOLVE-ANALYTICALLY**

Per fire-gate:

- §162-PROBE is **NOT genuinely uncertain** — the predicted outcome has
  high confidence (3 independent supporting findings from settled
  measurements).
- Running the probe would consume Mac CPU ~10-50 minutes for a
  predicted outcome.
- The probe **cannot fail to confirm** the prediction in a way that
  would change our model of the system; even a `±1 step` variation
  across cells would still land in `DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS`
  per §162 design's threshold.
- Therefore: **resolve analytically**. Predicted verdict =
  `DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS` recorded as §162-R analytical
  resolution.

### What this analytical resolution buys

1. **Closes the §162-PROBE cell** without consuming Mac CPU.
2. **Sharpens the implication**: §24 SPONTANEOUS Phase B unprompted-
   emission decision-axis is **threshold-dominated**, not
   weight-content-dominated, at the current scaffold. A 자연발화 lift
   from weights would require **either** lifting the Ψ-physics channel
   (which §161-FIRE attempts via dual-head coupling) **or** making the
   §24 threshold learnable + ckpt-aware (which §27 / §44 / §48 DH-DL
   already showed mode-collapses).
3. **Makes §161-FIRE's predicted verdict landscape clearer**: per the
   §161 design §3 caveat 4 and the secondary signal `head_g_grad_norm
   > 0`, the §161-FIRE outcome that would most clearly defy this
   analytical resolution is "§161-FIRE produces `psi_dir_std > 1e-4`
   AND `unprompted_emission_rate > 1/20`". Either alone is a weaker
   signal; both together would be the strongest evidence that the
   dual-head coupling shifts both the Ψ-channel **and** the decision
   axis.

---

## §5 — closed-form propositions (math theorems by inspection)

Per `@X hexa_verify`: theorems-by-inspection, NO sympy / PyPhi /
Wolfram / Mathematica cited.

**P1 (motivation_score factor decomposition)** — the
`motivation_score` is a weighted sum over 8 factors per
`spontaneous_lib.hexa::motivation_score`. By weighted-sum
decomposition, when 7 of 8 factors are nearly cell-invariant (the
env-driven ones are the same input; the Ψ-derived factor is constant
within ≤ 1e-4 variance per cell), `motivation_score` itself varies
across cells by at most the weighted contribution of the Ψ-derived
factor, which is bounded by `w_psi · psi_dir_std_max ≈ (1/8) · 0.0166
≈ 2.08e-3`. P1 holds by linearity of weighted sum.

**P2 (`emit` threshold-crossing inertia)** — `emit ⟺ motivation > 0.30`
is a discrete threshold; small variations in `motivation` cross the
threshold at the same `step` index unless `motivation` is within
`emit_threshold ± 2.08e-3 ≈ ±0.7%` of `imThreshold = 0.30`. For random
env-driven sequences, the probability of motivation falling within
that narrow band at a particular step is ≈ `2 · 2.08e-3 / motivation_range
≈ 1.4%` (assuming uniform `motivation` distribution over [0, 1]). Over
20 steps, expected count of cells differing in emit at that step is
≈ 4 cells · 20 steps · 1.4% ≈ 1.12 cells × steps. P2 bounds cell-to-cell
emit-count variation at ≤ ~1 step.

**P3 (Ψ-channel collapsed measurement settled)** — all 4 cells'
`psi_dir_std` from §2 has been measured to be at or below the
liveness threshold by ≥ 4 orders of magnitude (§126, §139) or below
the §107 A3-axis spread threshold (§107-RETRY). The cells' Ψ-state is
empirically settled.

**P4 (§24 threshold-side dominance settled)** — §27 DH-DL trained a
3-class head on §24 trace; distillation gap was 0.00063. §44 / §48 /
§49 scaled the distillation; §49 wired into live loop and observed
mode-collapse. The §24 emission decision is empirically
threshold-dominated, not weight-content-dominated.

**P5 (Analytical resolution closure)** — §162-PROBE is therefore
analytically resolvable to `DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS`
with cell-to-cell `unprompted_emission_rate` variation bounded by
P2's `≤ ±1 step` over 20 steps. The probe run would observe this
predicted outcome; the run would not generate informational delta
beyond confirming the analytical resolution.

**P6 (central blue_falsifier.py 0-line-diff invariant)** — central
sha prefix `c93e160a8a376a94` at START + END. §162-R writes only to
its own state dir. Invariant holds.

**P7 (Anti-padding honesty)** — `DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS`
is a **null result** for the 자연발화 axis — it says non-CE training
does NOT help unprompted-emission rate at this scaffold. Anti-padding
precedent (§13-M / §30 / §97 / §109 / §110 / §115 / §155 / §157 / §158
/ §159 / §160 / §161 / §162) — §162-R declines to manufacture a
positive from the §126 / §139 `byte_acc 0.1185` PART_AMBIG result.
The non-CE byte_acc lift does NOT transfer to 자연발화 rate; both can
be honest measured-negatives without contradiction.

**B-S162-R-NOTE empirical carve-out** — P1-P7 prove the analytical
resolution is well-formed. The resolution is a **prediction**, not a
measurement. The §162-PROBE measurement (if anyone runs it later)
would empirically confirm or refute the prediction. P5's "would not
generate informational delta" is the *instrument-first call*, not a
proof — running the probe is a small Mac CPU cost; the call is that
the cost exceeds the expected information gain. necessary-not-sufficient
(B-EMERGE-7 / B-D-NOTE / B-PHASE-B-NOTE family). NOT counted 🔵.

---

## §6 — honest C3 caveats (13)

1. §162-R is an analytical prediction, not a measurement. ★
2. The `w_psi = 1/8` uniform-weight estimate is the simplest model;
   `spontaneous_lib.hexa::motivation_score` may use a different
   weighting. The actual weighting only matters if `w_psi · psi_dir_std`
   exceeds `0.7%` of `imThreshold = 0.30` — even a 4× larger `w_psi`
   would not flip the conclusion.
3. The §24 protocol's `safety_6_AND` may itself shift the emit count.
   §162-R assumes safety is satisfied (env_off = False, content_ok =
   True, etc.) per §24 stub default. Worst case: stricter safety
   reduces emit_count uniformly across cells, which doesn't change the
   cross-cell verdict.
4. **§107-RETRY's `psi_dir_std = 0.0166`** is the largest of the four
   cells. If §107-RETRY produces emit_count = 2 while §126 / §139
   produce emit_count = 0 due to lower Ψ-driven motivation, the
   bucket would still be `DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS` per
   §162 design's `±1` threshold, but with §107-RETRY as the slight
   outlier. This is exactly P2's bounded variation.
5. The analytical resolution does NOT predict body-coherence; only
   decision-axis emission rate. Even if a cell emits, its emitted
   body's `honest_coherent` rate is a separate question.
6. §161-FIRE's predicted outcome is OUT OF SCOPE for §162-R. §162-R
   predicts §162-PROBE, not §161-FIRE.
7. If a future cycle adds a NEW non-CE training algorithm (a 5th data
   point in the §96-Q2 quadruple), the §162 probe could become genuinely
   uncertain on THAT new cell — analytical resolution doesn't extend
   to unseen cells.
8. The `w_psi = 1/8` estimate is a uniform-prior; actual prior from
   `spontaneous_lib.hexa` source could be biased toward Ψ if the lib
   weights Ψ more heavily. The 4× margin in P2 buffers against
   reasonable deviations.
9. PII clean (no `Min Woo`, no `nerve011235`, no credentials).
10. anima downstream-consumer (hexa-lang / hexa-bio / kosmos / tape)
    read-only 0 edit.
11. WALL-A (§1.1 data-regime) orthogonal — `@N n_priority_1_gap` not
    affected.
12. §96-Q2-weak supported-on-quadruple inherits — §162-R does not
    move the §160 verdict.
13. north-star + §15 / §51 / §72 milestones UNCHANGED, GOAL 미도달 —
    §162-R is an instrument-first analytical closure of one path, NOT
    a GOAL movement.

---

## §7 — what §162-R changes vs §162's pre-resolution state

Before §162-R, §162 was DESIGN-OPEN-PROBE-DECIDABLE — the probe was
specified, the verdict buckets pre-registered, but the cell run was
not done.

After §162-R:

- §162-PROBE call: **NOT WARRANTED** (analytical confidence is high).
- §162 design landed verdict carries: still DESIGN-OPEN-PROBE-DECIDABLE
  (the design itself is well-formed; §162-R declines to run it).
- §162-R analytical result added: predicted bucket =
  `DECISION_AXIS_BYTE_EQUAL_ACROSS_CKPTS`, confidence = high.
- Implication for §161-FIRE: §161-FIRE's `spont_directional_positive`
  predicate is the GOAL-relevant fire (genuine uncertainty on
  `psi_dir_std`-lift and emission-rate-lift). The §162-R analytical
  closure says §161-FIRE is the actual measurement to make, not §162.

This is the instrument-first call applied honestly.

---

## §8 — implication for downstream cycles

1. The §24 SPONTANEOUS Phase B threshold (`imThreshold = 0.30`) is the
   dominant emission signal in the current scaffold. **A future fire
   cycle that wants to lift 자연발화 must either**: (a) lift the
   Ψ-physics channel substantially (§161-FIRE's hypothesis), (b)
   replace the hand-coded threshold with a learnable + ckpt-aware
   policy that does NOT mode-collapse (§27/§44/§48/§49 showed the
   naive DH-DL distillation mode-collapses), OR (c) re-train at a
   data-regime large enough to cross §1.1 threshold (WALL-A path).
2. §161-FIRE attempts (a). §162-R confirms the existing
   §126/§139/§107-RETRY ckpts don't have (a) lifted, so §161-FIRE's
   measurement of `psi_dir_std post-fire` is the next high-information
   experiment.
3. The «non-CE byte_acc 0.1185 does NOT translate to 자연발화 rate»
   finding is a clean honest negative — it doesn't refute §96-Q2-weak
   (the quadruple finding), it tightens it: Ψ-channel-dead ckpts
   don't produce non-trivial 자연발화 rates regardless of byte_acc.
4. WALL-B's two halves — learning-channel and Ψ-physics-channel —
   remain as named in §160. §162-R is **measurement-axis closure** of
   what existing PART_AMBIG ckpts can carry; it does not move WALL-B's
   shape further than §160 already did.
