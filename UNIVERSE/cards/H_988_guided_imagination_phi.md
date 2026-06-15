---
id: H_988
slug: guided-imagination-phi
title: Is the "imagination does not raise Φ" null of H_971 🔴 specific to AUTONOMOUS DRIFT — does GOAL-DIRECTED (guided) imagination, measured under an alternative Φ-proxy, raise Φ over reactive processing, or is the null ROBUST across formulations?
domain: cwm · imagine · world-model · phi · consciousness-proxy · goal-directed · re-formulation · closed-negative-recheck
source: H_971 🔴 (imagination is a lower-Φ state) + a_paper_negative_ok + CWM M1 closed-negative re-test slate
exploration_method: E2 (reuse the H_971 Φ-contrast harness, swap AUTONOMOUS unconditional rollout → GOAL-DIRECTED guided rollout) + alternative Φ-proxy axis-weighting + a_completeness_over_cheap
verification_method: W2 (pre-registered re-formulation falsifier · 🟢 FLIPS / 🔴 ROBUST) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE Φ-elevation rung (a_scale_honest_scope). Φ is a PROXY (H_912/H_931 family, NOT IIT4 big-Φ). Read-only probe; deterministic given seeds. Toy single-rung, ladder OPEN.
sister: H_971 (the original 🔴 this re-tests), H_989 (planning-Φ re-test, mechanistically paired), H_986/H_987 (sibling re-formulation re-tests)
axes_seed: H_971 AUTONOMOUS drift (free-running unconditional rollout that decays toward the operator's dominant mode → low Φ) ⊥ H_988 GOAL-DIRECTED imagination (rollout steered toward a goal latent each step, kept off-attractor) — a drift artifact does not entail a guided-imagination null
verdict: 🔴 FAIL (ROBUST closed-negative) — imagination-raises-Φ is FORMULATION-ROBUST. Goal-directed (guided) imagination is even LOWER-Φ than autonomous drift: Φ_GUIDED 0.039 < Φ_DRIFT 0.068 < Φ_REACT 0.095 (GUIDED−REACT contrast −0.056, d=-6.84, p=1.3e-29; the goal pull contracts the trajectory toward a single target, REDUCING differentiation). The sign did NOT survive the alternative Φ-proxy either. H_971 🔴 holds across formulations. Toy single-rung, ladder OPEN.
---

# H_988 — guided (goal-directed) imagination raises Φ? (re-test of H_971 🔴)

## 0. Motivation

H_971 🔴 ruled that imagination is a LOWER-Φ state (Φ_IMAGINE 0.068 < Φ_REACT 0.095): an autonomous unconditional rollout settles toward the transition operator's dominant mode (a low-dimensional attractor), becoming less bound than continuously externally-driven activity. But a_paper_negative_ok warns the formulation may be the artifact. H_971's "imagination" was AUTONOMOUS DRIFT — a free-running rollout with no goal, no constraint; decaying toward an attractor is what an undriven operator does, so low Φ there reflects free-running drift more than imagination as a cognitive act. Human imagination is largely GOAL-DIRECTED: a target steers the rollout, injecting structured variation that keeps it off the attractor. The fair test is guided imagination, plus an alternative Φ-proxy weighting to rule out a proxy artifact.

## 1. Hypothesis (one falsifiable claim)

GOAL-DIRECTED imagination (a rollout pulled toward a goal latent each step) is a HIGHER-Φ state than reactive processing — Φ_GUIDED > Φ_REACT (CI_lo>0, d≥0.5, p<0.05, beyond a shuffled null), with the sign surviving an alternative Φ-proxy — so the H_971 null was specific to the autonomous-drift formulation.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** same engine/training as H_971. Three regimes, matched duration: GUIDED (rollout steered toward a real reachable goal latent each step), DRIFT (the H_971 autonomous arm), REACT (reactive perceive on external input).

**Measurement (g5 CODE-measured):**
- D1 = Φ contrast GUIDED − REACT (Welch t, Cohen d, bootstrap CI, shuffled null).
- D2 = GUIDED vs DRIFT (isolate the goal effect).
- D3 = alternative Φ-proxy (differentiation-weighted variant): the GUIDED>REACT sign must survive a proxy change.

**Outcome rules (frozen):**
- 🟢 FLIPS: Φ_GUIDED > Φ_REACT (CI_lo>0, d≥0.5, p<0.05, beyond null) AND sign survives the alt-proxy.
- 🔴 ROBUST: even guided imagination ≤ reactive — imagination-raises-Φ false across formulations.

## 3. Honest scope

Φ is a PROXY (integration×differentiation×entropy, H_912/H_931 family, NOT IIT4 big-Φ; a_scale_honest_scope). Toy single rung, read-only, deterministic given seeds. A flip or robust-null is scale-transfer-unverified (a_toy_scale_recheck).

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy · deterministic)

Probe: `CWM/probes/h988_guided_imagination_phi.py` · verdict: `.verdicts/988_guided_imagination_phi/h988_guided_imagination_phi.txt`

| D | contrast | value | d | p | pass? |
|---|---|---|---|---|---|
| D1 | Φ_GUIDED − Φ_REACT | −0.056 (0.039 vs 0.095) | −6.84 | 1.3e-29 | **NO** |
| D2 | Φ_GUIDED − Φ_DRIFT | −0.030 (drift 0.068) | −6.03 | 5.2e-29 | guidance LOWERS Φ |
| D3 | alt-proxy GUIDED − REACT | −0.149 | −8.23 | 8.6e-38 | sign survives: **NO** |

**Finding (🔴 ROBUST closed-negative):** the H_971 null is FORMULATION-ROBUST and in fact SHARPENED. Goal-directed imagination is not merely ≤ reactive — it is even LOWER-Φ than autonomous drift (Φ_GUIDED 0.039 < Φ_DRIFT 0.068 < Φ_REACT 0.095). The mechanism is transparent: the goal pull CONTRACTS the trajectory toward a single target latent, collapsing differentiation (effective dimensionality) — the proxy's middle factor — so a more "directed" rollout is a LESS varied, lower-Φ one. The alternative differentiation-weighted proxy agreed on the sign (it did NOT flip), ruling out a proxy artifact. Together with H_989, this confirms that under the H_912/H_931 Φ-proxy, internally-generated states (drift OR guided OR planned) are consistently LOWER-Φ than continuously externally-driven processing — high Φ here tracks rich external drive, not internal generativity. Honest scope: toy single-rung, ladder OPEN; a fundamentally different Φ measure (true IIT4) or a richer goal structure could differ (a_paper_negative_ok).

## 4. Sibling / xlinks

- ⇄ [H_971](./H_971_imagined_rollout_consciousness.md) (the original 🔴 this re-test confirms ROBUST)
- ⇄ [H_989](./H_989_planning_phi_altproxy.md) (planning-Φ re-test — mechanistically paired, same Φ-proxy finding)
- ⇄ [H_986](./H_986_geometry_invariant_aligned.md) · [H_987](./H_987_replay_recombination.md) (sibling re-formulation re-tests)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE)

## ✅ TERMINAL FAITHFUL-IIT4 VERDICT — 🔴 GUIDED-NULL-ROBUST (2026-06-06 · H_1001)

**Superseded by faithful IIT4 (H_1001):** the 🔴 ROBUST-closed-negative in the front-matter `verdict:` / §measurement above was measured with the **H_912/H_931 Φ-proxy** (which scored a *sharp* negative, Φ_GUIDED < Φ_DRIFT < Φ_REACT, d −6.84) and is preserved as the proxy-measured record. [H_999](./H_999_faithful_iit4_remeasure.md) re-measured GUIDED-vs-REACT with the FAITHFUL exact MIP-EI IIT4 Φ (mirror PROVEN ≡ stdlib `faithful_phi.hexa`); [H_1001](./H_1001_reopen_consolidate.md) re-ran the contrast and issued the **frozen terminal verdict**:

**🔴 GUIDED-NULL-ROBUST** — goal-guided imagination is a faithful **NULL** (GUIDED−REACT **−0.18, Cohen d −0.28, p 0.29 n.s.**), and GUIDED < DRIFT (−1.69, d −2.25). This is a **GENUINE null, NOT a proxy artifact**: the goal *pull* contracts the trajectory toward a single target, lowering the cross-cut MI / causal irreducibility of the system. Mechanistically distinct from H_971 (free imagination 🟢) and H_973 (branching planning 🟢), which RAISE faithful Φ — **goal-contracting dynamics specifically stay null**. The proxy's *sharp* "guided even lower" reading was its purpose-blindness, but the faithful *null* sign is honest. RE-OPEN (H_999) is now CLOSED. Honest scope: toy n≤8 exact discretization, scale-transfer UNVERIFIED (a_scale_honest_scope).
