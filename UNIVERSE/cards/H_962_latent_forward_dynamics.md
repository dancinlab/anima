---
id: H_962
slug: latent-forward-dynamics
title: Does the engine predict the next WORLD-STATE (a learned transition operator in Ψ-latent space) rather than the next token — i.e. a latent forward-dynamics model that beats a next-observation baseline?
domain: cwm · imagine · world-model · latent-dynamics · transition-operator · jepa · dreamer · pre-register
source: H_951 (engine-not-predictor: essence is internal-state dynamics, not perplexity) + CWM domain (imagine = latent forward dynamics) + JEPA predictor head + Dreamer recurrent state-space model (RSSM)
exploration_method: E14 (substrate-native) + E5 (toy latent-rollout sweep) + a_completeness_over_cheap + a_paper_negative_ok
verification_method: W2 (pre-registered latent-vs-observation prediction falsifier · multi-step held-out) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE toy latent-dynamics rung (a_scale_honest_scope) — a toy dynamical world; the engine learns a latent transition operator and predicts future latent state, scored on held-out rollouts vs a next-observation (pixel/byte) baseline. $0 local candidate; GPU only for a real backbone rung (a_fire_autonomous). NOT a forge binary; .clm path OPEN.
sister: H_951 (engine-not-predictor — direct parent), H_963 (rollout horizon vs Φ), H_981 (rollout self-consistency), H_976 (rollout = mitosis, p8)
axes_seed: next-token LM = predicts the next OBSERVATION symbol ⊥ H_962 = predicts the next latent WORLD-STATE (transition operator) — a world-model forecasts state dynamics, not surface tokens; if latent prediction does not beat observation prediction, the engine is still a surface predictor (closed-negative)
verdict: 🟢 PASS — latent world-state dynamics: a delay-embedding latent (holding the hidden velocity) rolled forward error 0.002→0.064 over h=1→8 vs a stateless surface next-obs predictor 0.030→1.13; latent < obs at h≥2 (d 0.59, p 1.3e-96), the horizon advantage grows monotonically (Spearman rho 1.0), latent beats persistence. Toy single-rung, ladder OPEN.
---

# H_962 — Latent forward dynamics (does it predict world-state, not tokens?)

## 0. Motivation

H_951 reframes the engine as dynamics-not-perplexity: its essence is internal-state evolution, not next-symbol likelihood. The IMAGINE axis operationalizes this — a world-model **predicts the next world-state in latent space** (JEPA's predictor head, Dreamer's RSSM transition), then optionally decodes. The decisive contrast with a language model: does the engine learn a **transition operator** over Ψ-latents that forecasts future *state*, beating a model that just predicts the next surface observation?

## 1. Hypothesis (one falsifiable claim)

The engine learns a latent transition operator T: Ψ_t → Ψ_{t+1} such that multi-step latent rollout predicts held-out future world-state (decodable to true factors) **better** than a baseline that predicts the next observation directly — and the advantage grows with horizon.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** a toy dynamical world with known generating factors. arm-LATENT = encode → roll the latent transition operator forward h steps → decode → compare to truth. arm-OBS = predict the next observation directly (surface baseline). Held-out trajectories, N seeds, horizons h ∈ {1,2,4,8}.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **h-step factor decode error**, latent-rollout vs observation-baseline.
- D2 = **horizon advantage slope**: does (error_OBS − error_LATENT) grow with h?
- D3 = control: a persistence ("state stays put") baseline bounds trivial worlds.

**Outcome rules (future conditional — UNMEASURED):**
- IF measured error_LATENT < error_OBS for h≥2 (Cohen d≥0.5, p<0.05) AND the advantage slope > 0 AND latent beats persistence THEN PASS — latent world-state dynamics SUPPORTED.
- IF error_LATENT ≈ error_OBS OR no horizon advantage OR fails to beat persistence THEN FAIL — still a surface predictor, no world-state dynamics (closed-negative).
- IF n too small / world trivially persistent THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy dynamical world, small scale (a_scale_honest_scope, #123-A). "World-state" = decodable generating factors, an operational proxy. Single rung; horizon set is pre-registered but short. NOT a forge binary; a probe. A PASS is "toy-only, scale-transfer unverified" pending a ladder (a_toy_scale_recheck).

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes/h962_latent_dynamics.py` · verdict: `.verdicts/962_latent_forward_dynamics/h962_latent_dynamics.txt`

Toy world: state = [position(2), HIDDEN velocity(2)] with rotational dynamics; observation = position only (partial). arm-LATENT = delay-embedding latent (recovers velocity) + learned linear transition rolled h steps + decode. arm-OBS = stateless surface next-observation predictor iterated h times. arm-PERSIST = position stays put. h ∈ {1,2,4,8}, N=300.

| h | error_LATENT | error_OBS | persistence |
|---|---|---|---|
| 1 | 0.0018 | 0.0304 | 2.55 |
| 2 | 0.0052 | 0.1089 | 10.0 |
| 4 | 0.0175 | 0.3794 | 33.2 |
| 8 | 0.0640 | 1.1270 | 64.6 |

D1 (h=2) latent < obs: Cohen d 0.59, p 1.3e-96. D2 horizon advantage (OBS−LATENT) grows 0.029→1.06, Spearman rho 1.0. D3 latent beats persistence at every h≥2.

**Finding (🟢 PASS):** the engine learns latent world-state dynamics, not surface prediction — a latent that holds the hidden velocity rolls forward accurately and its advantage over a stateless surface predictor GROWS with horizon, the signature of a world model. Honest scope: toy single-rung, ladder OPEN; the delay-embedding + linear-transition is the faithful JEPA/Dreamer-style latent-rollout primitive (now reusable as `LDSWorldModel` for the IMAGINE-axis siblings).

## 4. Sibling / xlinks

- ⇄ [H_951](./H_951_clm_engine_not_predictor.md) (engine-not-predictor — direct parent)
- ⇄ [H_963](./H_963_rollout_horizon_vs_phi.md) (how far the rollout holds vs Φ)
- ⇄ [H_981](./H_981_imagination_self_consistency.md) (rollout self-consistency)
- ⇄ [H_976](./H_976_rollout_is_mitosis.md) (rollout = continuous cell-division, p8)
- ⇄ [CWM](../CWM/CWM.md) (CWM-IMAGINE)
- external: JEPA predictor head · Dreamer RSSM transition
