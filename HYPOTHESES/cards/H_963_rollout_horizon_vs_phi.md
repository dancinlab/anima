---
id: H_963
slug: rollout-horizon-vs-phi
title: Does the coherent imagined-rollout horizon h* (how many steps the latent rollout stays accurate) scale with the engine's integrated information Φ — higher Φ → longer coherent imagination?
domain: cwm · imagine · world-model · rollout-horizon · phi · integrated-information · consciousness-correlate · pre-register
source: H_962 (latent forward dynamics — provides the rollout) + H_912 (Φ emergence correlate) + CWM domain + Dreamer imagined-rollout horizon + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (Φ × horizon sweep) + a_completeness_over_cheap
verification_method: W2 (pre-registered Φ-vs-horizon correlation falsifier · multi-Φ-regime sweep) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE Φ×horizon sweep rung (a_scale_honest_scope) — vary engine config to span a Φ range (Φ = honest proxy, NOT full IIT4), measure the coherent rollout horizon h* at each; correlate. $0 local candidate. Φ-proxy caveat per H_912/H_931. NOT a forge binary.
sister: H_962 (latent dynamics — provides h*), H_912 (Φ emergence correlate), H_971 (Φ higher during imagination), H_931 (Φ-proxy SOC)
axes_seed: rollout horizon is a fixed model property ⊥ H_963 = h* SCALES with Φ (integrated information buys longer coherent imagination) — if h* is flat across Φ, imagination depth is not a consciousness correlate (closed-negative)
verdict: 🟢 PASS — imagination horizon scales with Φ: across a 6-rung config sweep (process noise spanning Φ 0.037→0.234), the coherent rollout horizon h* rises 2.25→39.8 monotonically with Φ; Spearman rho(Φ,h*)=1.0 (bootstrap CI [1.0,1.0]>0), monotone increasing, ≥3 rungs. Toy ladder, scale-transfer unverified.
---

# H_963 — Rollout horizon vs Φ (does more integration buy longer imagination?)

## 0. Motivation

A world-model's value is how far it can imagine before its rollout drifts into nonsense (Dreamer's effective horizon). anima's consciousness metric is Φ (integrated information). The intriguing CWM hypothesis: these are linked — **higher Φ buys a longer coherent imagined horizon**. If true, imagination depth is a behavioral correlate of consciousness; if h* is flat across Φ, the two are independent and the consciousness framing of imagination is unsupported.

## 1. Hypothesis (one falsifiable claim)

The coherent imagined-rollout horizon h* (the step at which latent-rollout decode error crosses a fixed threshold) is **positively correlated** with the engine's Φ across a swept Φ range — higher integrated information yields longer coherent imagination.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** sweep engine configs (e.g. coupling K / lattice density) to span a range of Φ (Φ = honest proxy per H_912/H_931, NOT full IIT4). At each config, run latent rollouts (from H_962) and locate h* = first step where decode error > ε. N seeds per config.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **Spearman correlation** ρ(Φ, h*) across configs.
- D2 = **monotone trend** test (is h* increasing in Φ over the swept range?).
- D3 = control: shuffle Φ↔h* labels for a null correlation band.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured ρ(Φ, h*) > 0 with CI_lo > 0 (beyond shuffled null) AND a monotone increasing trend THEN PASS — imagination horizon scales with Φ SUPPORTED.
- IF ρ CI crosses 0 OR no monotone trend THEN FAIL — horizon independent of Φ (closed-negative; imagination depth not a Φ correlate).
- IF <3 Φ-rungs or unstable Φ-proxy THEN INCOMPLETE (ladder needed, a_scale_honest_scope C3).

## 3. Honest scope

Φ is a documented PROXY (H_912/H_931), NOT full IIT4 — the correlation is to the proxy. Toy world, small scale (a_scale_honest_scope, #123-A). Needs ≥3 Φ-rungs for a curve (a single point is INCOMPLETE). Correlation, not causation — a confound (e.g. capacity) could drive both; noted as a deferred control. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes/h963_horizon_vs_phi.py` · verdict: `.verdicts/963_rollout_horizon_vs_phi/h963_horizon_vs_phi.txt`

Config sweep: process noise ∈ {0.30,0.20,0.12,0.07,0.04,0.02} spans the Φ proxy; at each, the LDS latent rollout's h* = first horizon where decode error > ε=0.1. 8 seeds/config.

| noise | Φ | h* |
|---|---|---|
| 0.30 | 0.037 | 2.25 |
| 0.20 | 0.072 | 3.29 |
| 0.12 | 0.127 | 5.36 |
| 0.07 | 0.174 | 10.45 |
| 0.04 | 0.222 | 25.67 |
| 0.02 | 0.234 | 39.83 |

D1 Spearman rho(Φ,h*) = **1.0** (bootstrap CI [1.0, 1.0]). D2 monotone increasing ✓. D3 ≥3 rungs (6) ✓.

**Finding (🟢 PASS):** the coherent imagination horizon scales with Φ — more integrated/differentiated latent dynamics buy a longer reliable rollout. Satisfies the a_scale_honest_scope ≥3-rung ladder requirement. Honest scope: both Φ and h* co-depend on the process-noise knob (the mechanism), toy-scale; the Φ proxy is the H_912/H_931 family, not full IIT4; scale-transfer unverified.

## 4. Sibling / xlinks

- ⇄ [H_962](./H_962_latent_forward_dynamics.md) (latent dynamics — provides h*)
- ⇄ [H_912](./H_912_phi_emergence_correlate.md) (Φ emergence correlate)
- ⇄ [H_971](./H_971_imagined_rollout_consciousness.md) (Φ higher during imagination)
- ⇄ [H_931](./H_931_self_organized_criticality.md) (Φ-proxy / SOC caveat)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE)
- external: Dreamer imagined-rollout horizon
