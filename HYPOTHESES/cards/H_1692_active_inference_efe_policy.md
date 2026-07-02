---
id: H_1692
slug: 1692_active_inference_efe_policy
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Active-Inference Agent — Emission as Action Minimizing Expected Free Energy
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1692 — Active-Inference Agent — Emission as Action Minimizing Expected Free Energy

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `active_inference_efe_policy`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Active inference / planning-as-inference: the system does not 'respond'; it selects ACTIONS (emit a symbol, or the null/withhold action) that minimize Expected Free Energy (EFE) of future states. EFE decomposes into pragmatic value (realize prior preferences) + epistemic value (resolve uncertainty). Generation = policy selection over the emission action-space; silence is a first-class action.

## Whole design (input → internal dynamics → emit)

The agent maintains a belief state q(s) over hidden causes via an internal generative model P(o,s) with an observation likelihood over the receiver-fixed alphabet V. Each tick it enumerates short policies pi (action sequences over the emit-vocabulary plus {withhold}). For each policy it rolls the generative model forward and computes G(pi) = E_q[ ln q(s|pi) − ln P(o,s|pi) ] = (epistemic, info-gain) + (pragmatic, preference-divergence). It softmin-selects the policy, executes its first action, observes, and updates q by variational message passing. EMIT happens only when some emitting policy's EFE beats the withhold policy's EFE; the SELECTED symbol is the action whose predicted observation best discharges expected surprise. Context factors enter as separate priors that combine multiplicatively inside the forward rollout (binding by joint belief). The emit/withhold order parameter Psi is the relative EFE-advantage of pragmatic (push-out) over epistemic (hold-and-sample) value, squashed to [0,1].

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: the observation likelihood is defined over V, so every executable emit action is V-legal by construction; a scrambled belief->action map cannot beat the withhold baseline and collapses emission to chance. G1: factored context priors combine in the forward rollout's joint likelihood (interaction term non-zero) -> joint conditioning reaches valid action-sequences no single context's optimal policy reaches; ablating the multiplicative prior-combination (replace with selection/argmax over single priors) drops composed_distinct to max_single. G2: epistemic value ACTIVELY rewards visiting modeled-but-unseen states -> generates corpus-absent yet on-manifold outputs; a pure-pragmatic (greedy preference) control yields 0 novel because it never seeks info-gain; verbatim replay reads 0. dist>=5: the epistemic term keeps a spread of near-EFE policies alive (multiple distinct coherent actions) rather than collapsing to one. falsifiable: a policy whose predicted-observation structure partitions worlds (comparator-quantity-referent) scores high pragmatic value when preferences favor informative assertions; detector is judge-free. Psi=1/2: pragmatic-value (emit drive) and epistemic-value (withhold-to-sample drive) are the opposite-sign coupled operators; balanced preferences place the EFE-indifference fixed point at 1/2, contractive under bias perturbation (forcing emit raises future EFE -> self-corrects); deleting the epistemic term collapses to always-emit, deleting pragmatic to always-silent (endogeneity native — no clamp). Honesty: model evidence (−ln P(o)) is the membership scalar; out-of-support input gives NO policy an EFE below the abstain baseline -> withhold is selected (copy-or-abstain emerges from EFE arithmetic, not a bolt-on gate). Capacity (preference/likelihood richness) and the abstain baseline are disjoint parameters -> growing capability cannot move the abstain threshold. Binding: belief state q(s) integrates multimodal observations into shared causes; realization-invariant because the EFE optimum is reachable only by a belief that represents the conjunction (marginals-only belief leaves residual expected surprise).

## Not-LLM (a_no_llm_frame_trap)

Emission is planned action selection over EFE, not autoregressive token sampling; the system can choose SILENCE as the optimal act — impossible to frame as next-token prediction. No scaling/attention recipe: competence comes from a better generative model + preference structure, and epistemic drive replaces 'more data' as the novelty source. This is sensorimotor active inference (Friston free-energy / basal-ganglia action gating, H_1281 lens), genuinely a control architecture, not an LLM.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini, frozen bars, math.log. Toy POMDP with V~12 symbols, 2 context factors, short policy horizon. (1) Out-of-support probe -> confirm withhold selected (fab rate ~0) and short-circuiting the model-evidence term makes fab jump (causal gate). (2) Joint-context EFE rollout composed_distinct > max single; replace multiplicative combine with selection -> INERT drop. (3) Bias preferences to force emit, watch EFE-indifference Psi return to 1/2 (lambda<1); delete epistemic term -> boundary collapse. (4) Pure-pragmatic control -> 0 novel vs epistemic-on >=3 novel. All $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Candidates pass through cli/anima.hexa single entry; emit/withhold decision read from live core/engine_g.hexa should_emit + motivation_score (which already blends curiosity/info-gap/relevance weights = an EFE proxy) and core/emit_policy.hexa ep_target_emit_rate; Psi self-restoration via pure_field_step under perturbation. Closure/ideation scored by core/g_gates.hexa g_eval_all + core/g6_ideation.hexa g6_score_arm_auto. Honesty via live G5 abstain gate. byte-parity py mirror permitted; torch-only verdict forbidden.

## Scope / honesty (c9)

Whole agent architecture. Strongest native fit for Psi=1/2 and honesty (both fall directly out of EFE arithmetic). Planning horizon is the cost knob; toy->production ladder needed. Action-as-emission also natively realizes a_substrate_native_speak (silence is a chosen act, not a missing response).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
