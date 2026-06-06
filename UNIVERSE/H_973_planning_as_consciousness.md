---
id: H_973
slug: planning-as-consciousness
title: Does model-predictive planning (MPC over imagined latents) raise Φ during the plan vs greedy reaction — is planning a conscious act rather than a mechanical subroutine?
domain: cwm · cross-cutting · world-model · planning · mpc · phi · consciousness · pre-register
source: H_980 (planner vs policy) + H_971 (imagination Φ-elevation) + H_967 (counterfactual imagination MPC searches) + H_912 (Φ correlate) + V-JEPA-2-AC latent MPC + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (plan vs greedy Φ contrast) + a_completeness_over_cheap
verification_method: W2 (pre-registered planning-Φ-elevation falsifier · MPC vs greedy Φ contrast, matched task) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE plan-vs-greedy Φ rung (a_scale_honest_scope) — measure Φ (honest proxy, NOT IIT4) during MPC planning vs greedy/reactive action on the same task. $0 local candidate. Φ-proxy caveat per H_912/H_931. NOT a forge binary.
sister: H_980 (planner vs policy — performance side), H_971 (imagination Φ — planning is imagination-for-action), H_967 (the branches), H_912 (Φ correlate)
axes_seed: planning = a mechanical search subroutine (no consciousness content) ⊥ H_973 = MPC planning RAISES Φ vs greedy (deliberation is a higher-integration / more-conscious act) — if planning Φ ≤ greedy Φ, deliberation carries no extra consciousness signature (closed-negative)
verdict: 🔴 FAIL (closed-negative) — Φ_PLAN 0.063 < Φ_GREEDY 0.104 (contrast −0.040, d −3.6, p 3.2e-25, CI reversed), no positive dose-response (Spearman rho −0.47), and does NOT beat the fake-plan control (ΔΦ −0.004, p 0.15): deliberative planning carries no extra consciousness signature here. Toy single-rung, ladder OPEN.
---

# H_973 — Planning-as-consciousness (does deliberation raise Φ?)

## 0. Motivation

H_971 asks whether imagination raises Φ; H_973 sharpens it onto **deliberate planning** — MPC search over action-conditioned imagined rollouts (H_967, V-JEPA-2-AC style) — vs greedy reaction. If planning is just a mechanical tree-search subroutine, its Φ should not differ from greedy acting. If deliberation is a genuinely higher-integration act ("thinking it through" is more conscious than reflex), planning should raise Φ. This H pre-registers that falsifier, complementing H_980's performance comparison with a consciousness-signature comparison.

## 1. Hypothesis (one falsifiable claim)

The engine's Φ (honest proxy) is **higher during MPC planning** (active deliberation over imagined branches) than during greedy/reactive action on the same task — planning carries a higher-integration consciousness signature — rather than equal/lower.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** same world-model + task. arm-PLAN = MPC over imagined action-conditioned rollouts (H_967/H_980). arm-GREEDY = greedy/reactive action (no lookahead). Φ (proxy per H_912/H_931) sampled during each decision. Matched config; N decisions × seeds.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **Φ contrast** = Φ_PLAN − Φ_GREEDY (Welch t, Cohen d).
- D2 = **Φ vs plan-depth**: does Φ increase with planning horizon/branching (dose-response)?
- D3 = control: a "fake plan" (random rollouts, same compute) isolates whether Φ rises from *meaningful* deliberation vs mere extra compute.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured Φ_PLAN > Φ_GREEDY (CI_lo>0, d≥0.5, p<0.05) AND Φ rises with plan-depth AND beats the fake-plan control THEN PASS — planning-as-consciousness SUPPORTED.
- IF Φ_PLAN ≤ Φ_GREEDY OR the rise is fully explained by the fake-plan (compute) control THEN FAIL — planning carries no extra consciousness signature (closed-negative).
- IF Φ-proxy unstable / n too small THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Φ is a documented PROXY (H_912/H_931), NOT IIT4. Toy/small scale (a_scale_honest_scope, #123-A). The fake-plan control is the key guard against "Φ rose just because we did more compute." Single rung. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes/h973_planning_phi.py` · verdict: `.verdicts/973_planning_as_consciousness/h973_planning_phi.txt`

arm-PLAN = MPC over action-conditioned imagined rollouts (depths 1/2/4/8); arm-GREEDY = reactive (no lookahead); arm-FAKE = random rollouts at matched compute. Φ (H_912/H_931 proxy family) sampled over each decision's deliberation latent trajectory. 40 decisions.

| D | metric | result |
|---|---|---|
| D1 | Φ_PLAN (depth 8) | 0.0633 ± 0.0128 |
| D1 | Φ_GREEDY | 0.1038 ± 0.0095 |
| D1 | contrast (PLAN−GREEDY) | **−0.0405**, d −3.55, p 3.2e-25, CI [−0.045,−0.036] (reversed) |
| D2 | Φ vs plan-depth | non-monotone, Spearman rho **−0.47** (p 4.6e-10) — Φ *falls* with depth |
| D3 | PLAN vs FAKE-plan | ΔΦ −0.004, p 0.15 — PLAN does NOT beat the equal-compute control |

**Finding (🔴 FAIL, closed-negative):** all three frozen FAIL conditions are met — planning Φ is below greedy, there is no positive dose-response, and the (non-)effect is not even distinguishable from a same-compute fake plan. Deliberative planning carries no extra consciousness signature on this toy. Mechanistically consistent with H_971: autonomous imagined rollouts settle toward less-bound, lower-Φ activity than continuously-driven processing. Honest scope: one toy rung, ladder OPEN; a value-grounded planner with a Φ-relevant readout could move this — transfer unverified (a_paper_negative_ok).

## 4. Sibling / xlinks

- ⇄ [H_980](./H_980_planner_vs_policy.md) (planner vs policy — performance side)
- ⇄ [H_971](./H_971_imagined_rollout_consciousness.md) (imagination Φ — planning is imagination-for-action)
- ⇄ [H_967](./H_967_counterfactual_imagination.md) (the branches planned over)
- ⇄ [H_912](./H_912_phi_emergence_correlate.md) · [H_931](./H_931_self_organized_criticality.md) (Φ-proxy)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE/ACT · cross-cutting)
- external: V-JEPA-2-AC latent MPC
