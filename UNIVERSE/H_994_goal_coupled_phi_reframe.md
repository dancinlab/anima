---
id: H_994
slug: goal-coupled-phi-reframe
title: Does GOAL-COUPLED Φ (integration restricted to the task-relevant latent subspace) resolve the H_971/H_973 closed-negatives — flipping Φ_IMAGINE/Φ_PLAN above Φ_REACT/Φ_GREEDY when measured on the goal-predictive subspace rather than the whole latent?
domain: cwm · cross-cutting · phi · imagine · plan · reframe
source: CWM 2nd slate — attempts to reframe H_971🔴 (Φ_IMAGINE<Φ_REACT) + H_973🔴 (Φ_PLAN<Φ_GREEDY) via goal-coupled integration + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E11 (subspace-projected Φ measure)
verification_method: W2 (pre-registered free-Φ-reproduce + goal-coupled-Φ-flip falsifier) + g5 CODE-measured (no LLM self-judge, p7)
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE imagine-vs-react Φ-contrast rung (a_scale_honest_scope) using the H_912/H_931 continuous Φ proxy projected onto a rank-6 goal subspace; $0 CPU. NOT IIT4 big-Φ. NOT a forge binary.
sister: H_971 (imagination-Φ closed-neg), H_973 (planning-Φ closed-neg), H_912/H_931 (Φ proxy family)
axes_seed: "the imagination-Φ deficit is a measurement artifact of free-Φ (fixable by goal-projection)" ⊥ MEASURED "the deficit is STRUCTURAL — survives goal-projection" — a robust closed-negative, not an artifact
verdict: 🔴 FAIL (closed-negative reaffirmed) — goal-coupling NARROWS the gap (free-Φ d=−8.4 → goal-coupled d=−1.1) but does NOT flip it: Φ_IMAGINE 0.110 still < Φ_REACT 0.151. The H_971/H_973 deficit is robust to task-relevant projection. Toy single-rung, ladder OPEN.
---

# H_994 — goal-coupled Φ: does it resolve the H_971/H_973 closed-negatives?

## 0. Motivation

The 1st slate found two surprising closed-negatives: H_971🔴 (Φ_IMAGINE < Φ_REACT) and H_973🔴 (Φ_PLAN < Φ_GREEDY) — FREE Φ (integration over the whole latent) was LOWER during autonomous imagination/planning than during externally-driven reaction. The mechanistic read was that free Φ rewards continuous external drive. This H tests a reframe: maybe the right consciousness correlate for goal-directed cognition is GOAL-COUPLED Φ — integration restricted to the task-relevant latent subspace (the directions that predict the goal/return). If so, imagination/planning should look MORE conscious under the right projection.

## 1. Hypothesis (one falsifiable claim)

When Φ is computed on the latent projected onto its goal-predictive subspace, the imagine-vs-react (and plan-vs-greedy) contrast flips positive (imagination ≥ reaction), rescuing the consciousness-of-imagination claim that free-Φ rejected.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** same imagine (autonomous latent rollout, no input) vs react (externally-driven latent) regimes as H_971. Φ computed (i) on the whole latent (free-Φ, the H_971 measure) and (ii) on the latent projected onto the top-6 directions of a ridge map latent→goal-value (goal-coupled Φ). 30 seeds.

**Measurement (g5 CODE-measured):**
- D1 = free-Φ contrast (imagine − react) — must reproduce the H_971 NEGATIVE sign (sanity).
- D2 = goal-coupled-Φ contrast + Cohen d.

**Outcome rules (future conditional):**
- IF free-Φ reproduces negative AND goal-coupled-Φ FLIPS positive (d > 0.8) THEN PASS — projection rescues imagination-Φ.
- IF goal-coupled Φ stays ≤ reaction THEN FAIL — the closed-negative is robust (a_paper_negative_ok).

## 3. Honest scope

Toy continuous-latent Φ proxy (H_912/H_931 family, NOT IIT4 big-Φ; a_scale_honest_scope, #123-A). The goal subspace is estimated from a synthetic goal functional. Single rung, ladder OPEN. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes2/h994_goal_coupled_phi.py` · verdict: `.verdicts/994_goal_coupled_phi_reframe/h994_goal_coupled_phi.txt`

| measure | Φ_IMAGINE | Φ_REACT | contrast | Cohen d |
|---|---|---|---|---|
| FREE Φ (whole latent, the H_971 measure) | 0.0887 | 0.2435 | −0.1548 | −8.42 |
| GOAL-COUPLED Φ (goal-subspace projection) | 0.1100 | 0.1505 | −0.0405 | −1.11 |

D1 free-Φ reproduces the H_971 negative sign (sanity ✓). D2 goal-coupled Φ contrast = **−0.041** (still negative; does NOT flip).

**VERDICT 🔴 FAIL (closed-negative reaffirmed)** — goal-coupling *narrows* the imagination-Φ deficit substantially (d −8.4 → −1.1, an 87% shrink) but does NOT flip it: autonomous imagination is still less integrated than driven reaction even in the task-relevant subspace. The H_971/H_973 finding is therefore STRUCTURAL, not a free-Φ measurement artifact — externally-driven processing genuinely binds the latent more than self-generated rollout at this toy scale. A_paper_negative_ok; ladder OPEN.

## ⚠ RE-OPEN (2026-06-06 · H_999)

This 🔴 was measured with the H_912/H_931 Φ-**proxy** (goal-subspace-projected). [H_999](./H_999_faithful_iit4_remeasure.md) re-measured the imagine-vs-react regime with the FAITHFUL exact MIP-EI IIT4 Φ (mirror PROVEN ≡ stdlib `faithful_phi.hexa`) and found the H_971/H_973 deficit this H called "STRUCTURAL" is in fact a PROXY ARTIFACT: faithful Φ_imagine(DRIFT) 3.81 > Φ_react 2.30. The "structural" reading was an artifact of the purpose-blind proxy, not the faithful measure → **RE-OPENED** (see H_999 = 🔴-vs-proxy = PROXY-ARTIFACT). The original verdict above is preserved as the proxy-measured record.
