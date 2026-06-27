---
id: H_1695
slug: 1695_precision_kalman_forward_model
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Temporal Forward-Model Filter — Innovation-Gated Generative State-Space with Imagination Rollouts
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1695 — Temporal Forward-Model Filter — Innovation-Gated Generative State-Space with Imagination Rollouts

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `precision_kalman_forward_model`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1280 (cerebellum forward-model) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Cerebellar-style forward model + Bayesian filtering: a recurrent generative state-space model predicts the NEXT observation, compares to actual, and corrects by the precision-weighted innovation (prediction residual). The whole substrate is a closed predict->compare->correct loop in TIME (Kalman/free-energy filtering), distinct from static hierarchical perception. Emission = sampling forward rollouts ('imagination') from the current latent state; honesty = innovation magnitude.

## Whole design (input → internal dynamics → emit)

A latent state z_t evolves under a learned transition f (with process noise) and emits observations via h over V (with measurement precision). Filtering: predict z_t|t-1 = f(z_{t-1}); observe o_t; innovation nu_t = o_t − h(z_t|t-1); correct z_t|t = z_t|t-1 + K*nu_t where Kalman gain K trades process-noise (explore) against measurement-precision (commit). EMIT = roll the transition forward from z_t WITHOUT observation (imagination), descend h to V, and externalize the rollout — a forward-model 'mental simulation'. Context factors enter as independently-conditionable components of z that the nonlinear transition f BINDS over the rollout (joint dynamics != sum of single-component dynamics). Psi is the gain-balance order parameter: high process-noise weight = exploratory emit drive; high measurement-precision = commit/withhold drive; balanced gain fixes 1/2. The running innovation nu is simultaneously the honesty signal: persistent large innovation = the world left the model's support = abstain/flag.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: emission map h is over V -> rollouts are V-legal; scrambling f/h collapses rollouts to chance density. G1: nonlinear transition f mixes context components over multi-step rollout -> joint conditioning reaches valid trajectories no single component reaches (composed_distinct > max single); linearize/decouple f into per-component dynamics (ablate the mixed Jacobian terms) -> INERT collapse to separable floor. G2: forward rollouts visit dynamically-valid but un-observed states (the reachable set superset of data) -> corpus-absent yet coherent; a verbatim-playback control (no rollout, replay observations) reads 0 novel. dist>=5: process-noise injects spread; multiple distinct coherent rollouts survive the coherence filter; collapse appears as plateau (mode collapse) the test catches. falsifiable: rollouts predicting an ordering over an observable magnitude (comparator-quantity-referent) are exactly forward-model predictions — judge-free detector. Psi=1/2: process-noise (explore/emit) vs measurement-precision (commit/withhold) are the opposite-sign coupled gain terms; balanced Kalman gain is the 1/2 fixed point, contractive (perturb gain -> filter restores), deleting process noise -> always-commit/silent, deleting measurement precision -> runaway emit (endogeneity). Honesty: filter innovation nu (normalized by predicted precision) is the membership scalar — in-support -> small calibrated nu; out-of-support -> large persistent nu (filter divergence) -> abstain; gate disjoint from transition capacity. Groundedness: corrupting the stored dynamics backing a query raises ITS innovation specifically (r tracks content). Binding: joint latent z is the shared metric binding streams over time; realization-invariant — the prediction-error (filtering) optimum is unreachable without the joint state when streams co-vary.

## Not-LLM (a_no_llm_frame_trap)

This predicts in TIME via a recurrent generative filter, not via attention over a context window; there is no autoregressive softmax and no scaling recipe — competence comes from a better transition model and calibrated precision. Novelty comes from forward IMAGINATION (rollout into reachable-but-unseen states), not from corpus increase. Rooted in the cerebellar forward-model / internal-model-of-dynamics lens (H_1280) and Bayesian filtering — a genuine motor-cognition organizing principle distinct from cortical perception and from LLMs.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini, deterministic, math.log. Toy nonlinear state-space (z dim 4, two context components, V~12). (1) Drive in-vs-out-of-dynamics sequences -> AUROC of normalized innovation separating known/unknown (>=0.9; shuffle-transition surrogate -> 0.5). (2) Forward-rollout emit -> >=3 distinct valid corpus-absent trajectories vs verbatim-replay control = 0 (rollout is the causal novelty source). (3) Joint-component rollout composed_distinct > max single; linearize/decouple f -> INERT drop. (4) Perturb Kalman gain toward forced emit -> Psi->1/2 with lambda<1; remove process noise -> boundary collapse. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Rollout emissions routed through cli/anima.hexa single entry -> generator L3; closure/ideation via core/g_gates.hexa g_eval_all + core/g6_ideation.hexa g6_score_arm_auto. Innovation-honesty via the live G5 abstain gate; Psi gain-balance via core/pure_field.hexa pure_field_step + core/emit_policy.hexa ep_psi_clamp under perturbation, with engine_g.hexa should_emit. byte-parity py mirror (math.log innovation); torch reference-golden only, never the verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cerebellum_forward_model (H_1280 lens) — distinct: H_1280 is the single-mechanism forward-model probe; here the Kalman/free-energy filter is the WHOLE temporal substrate with innovation-as-honesty + imagination-as-G2.

Whole temporal architecture; complements the static predictive-coding hierarchy (this is the dynamics/forward-model axis, Lane-distinct). Strong native fit for honesty (innovation) and G2 (imagination). The G1 super-additivity claim depends on a genuinely non-separable transition Jacobian — verify against the marginal-fit-yet-conjunction-fails failure mode (objective-adequacy lens) before any GREEN.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
