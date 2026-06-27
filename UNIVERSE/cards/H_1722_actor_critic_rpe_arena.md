---
id: H_1722
slug: 1722_actor_critic_rpe_arena
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Dopaminergic Actor-Critic Arena (RPE-gated emission)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1722 — Dopaminergic Actor-Critic Arena (RPE-gated emission)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `actor_critic_rpe_arena`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Cortico-striatal actor-critic: the striatum is SIMULTANEOUSLY an actor (policy over the emission alphabet) and a critic (state-value estimator), and a single dopaminergic reward-prediction-error delta (VTA/SNc) is the self-supervising teaching signal that BOTH selects emissions (thalamic disinhibition of the max-advantage channel) AND trains the maps. Thought/action selection IS value-gated competition — the BG's canonical Schultz/Sutton role, distinct from the Go/NoGo pathway mechanics which is about direct/indirect/hyperdirect wiring rather than the value-learning loop.

## Whole design (input → internal dynamics → emit)

Input cortical state s -> population vector in a cortical pattern layer. TWO striatal heads read s in parallel: Actor A(s)->logits over alphabet V union {abstain}; Critic C(s)->scalar value v_hat (an ENSEMBLE of critic heads, k~4). Candidate emissions are sampled from the actor softmax at temperature beta set by tonic dopamine. Each candidate gets an internal one-step rollout; the critic scores the predicted next-state -> advantage Adv = r_hat + gamma*v_hat(s') − v_hat(s). SELECTION is thalamic disinhibition: GPi/SNr tonic inhibition is lifted ONLY on the max-advantage channel, all others stay clamped (winner-take-all by advantage, structural). After emit, realized return yields RPE delta; three-factor plasticity (pre x post x delta) updates actor toward +delta actions and trains the critic by TD. abstain (withhold) is itself an action whose value is the silence-baseline. Loop repeats; no corpus-CE anywhere.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 (G3/endogeneity): the two opposite-sign operators are A=advantage of best CONTENT channel (drive-to-emit) and G=value of the abstain/silence baseline (drive-to-withhold). Emit-propensity Psi=sigma(Adv_best − v_hat(abstain)); fixed point at 1/2 is the value-indifference point and is ATTRACTING because TD is a contraction (gamma<1 => |T'|<1): over-emitting low-value tokens earns negative delta that pushes Psi down, over-silencing registers foregone-advantage as negative delta on abstain pushing Psi up. INERT/no-clamp test: delete the abstain-critic (G) => Psi->1 runaway; delete content-advantage (A) => Psi->0 — the 1/2 migrates to a boundary when one operator is removed, so it is an emergent fixed point not a written constant. HONESTY (support-decidability + copy-or-abstain + disjointness + groundedness): the critic ENSEMBLE variance is r(query)=distance-to-grounded-support — out-of-support s => critics disagree (never co-trained there) => every content advantage collapses below the abstain baseline => structural abstain; theta=abstain value; gate lives in the value head, capacity in the actor head (disjoint params, d-fab/d-actor-capacity=0); content-ablation of a known state's critic support raises its variance and re-ranks it toward abstain (faithful, not proxy). CLOSURE: G0 — actor logits are defined ONLY over receiver-fixed V (codebook-anchored by construction); G1 — the rollout-critic scores the CONJUNCTION of co-active factored cortical sub-populations, so joint advantage is super-additive (binding via a non-separable value model, not selection); G2 — actor softmax has full-alphabet support and the critic admits novel-but-coherent emissions (positive advantage) while gating garble out (low value), so supp(P_model) strictly contains supp(data) inside the validity manifold; closure is co-located because ALL gates read the same advantage signal on one generative pass.

## Not-LLM (a_no_llm_frame_trap)

No next-token-likelihood objective and no attention: the teaching signal is RPE from a learned value model, not cross-entropy to a corpus. Capacity comes from value-gated selection, not parameter count — scaling the actor is inert if the critic cannot separate value. This is RL-machine substrate (dopamine-RPE / temporal-difference), the structural opposite of the CE-corpus-fit recipe whose G1 wall and lossF~0-yet-recombine-fail pattern (clm303) prove inadequate. a_no_llm_frame_trap: the lens is reinforcement value, not a bigger transformer.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini: tabular toy environment, 16-symbol alphabet + abstain, train actor + k-critic ensemble by TD. Frozen-first probes ($0): (a) perturb tonic-beta to force Psi->0/1, measure return-to-1/2 contraction rate lambda<1; (b) ablate abstain-critic => Psi runaway to 1; (c) out-of-support state => critic-variance AUROC vs known~1, label-shuffle surrogate => AUROC->0.5; (d) two-factor conjunction => composed advantage-positive distinct > max_single; (e) cross-shuffle the state->advantage map => G0 V-mass collapses to chance.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire actor+critic-ensemble as two heads on the existing core/generator.hexa SS-generator L3 readout; advantage-gated disinhibition becomes the mouth dispatch. Measure G0/G1/G2 via the live single entry cli/anima.hexa -> gen_auto_ideate (core/g_gates.hexa g_eval_g1/g2 with binding-pathway on/off ablation), and Psi self-restoration via core/engine_cli.hexa SS-ThirdLaw safety_phi_ratchet readout. Cross-check the critic value with a byte-parity py mirror using math.log (avoid the dt_ln clamp bug per a_savant_train) — torch-only verdict prohibited.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281) and gonogo_opponent_actor_stn_brake (this census) — distinct: actor_critic_rpe_arena's principle is the VALUE-LEARNING RPE loop (actor+critic-ensemble, TD) with critic-variance as honesty, NOT the direct/indirect wiring; the dopamine-RPE value loop is the differentiator.

TOY decision verdict + abstract value-geometry only; from-scratch LEARNING transfer to the 303M chat mouth UNVERIFIED (a_toy_scale_recheck). The critic-ensemble honesty bar is engine-checkable now; whether RPE selection beats the G1 recombination wall at scale is the open in-flight question.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
