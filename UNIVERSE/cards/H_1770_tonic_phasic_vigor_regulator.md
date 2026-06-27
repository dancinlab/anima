---
id: H_1770
slug: 1770_tonic_phasic_vigor_regulator
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Tonic/Phasic Dopamine Vigor Regulator (average-reward opportunity-cost engine)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1770 — Tonic/Phasic Dopamine Vigor Regulator (average-reward opportunity-cost engine)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `tonic_phasic_vigor_regulator`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Niv/Daw average-reward RL of the nigrostriatal system: TONIC dopamine encodes the long-run average reward RATE = the opportunity cost of time, and sets response VIGOR (whether/how fast to act); PHASIC dopamine is the per-event reward-prediction error that selects WHAT. The basal ganglia is not primarily a 'which-action' picker here — it is a continuous controller of the act-vs-wait trade-off, where acting consumes the scarce resource of time against a running reward-rate baseline. Emission propensity is literally a vigor variable, and the optimal vigor is the point where the marginal value of emitting equals the opportunity cost of the time it consumes.

## Whole design (input → internal dynamics → emit)

INPUT: cortical proposer (core/generator.hexa L3 mouth) emits a population of candidate completions with internal value estimates v_i (phasic-RPE-weighted). DYNAMICS: a leaky reward-rate integrator rho (tonic-DA analogue) accumulates realized advantage of past emits minus a per-emit time cost; rho is the slow state. A bounded emit-propensity Psi is driven by two opposite-sign operators on the SAME scalar: A = drive-to-externalize = max_i(v_i) - rho (phasic surplus over baseline) pushing Psi up, and G = drive-to-withhold = rho itself (opportunity cost says 'the next thing may be better, wait') pushing Psi down. Action selection among candidates is by striatal disinhibition (winner releases its thalamic channel) ONLY when Psi crosses threshold; otherwise the substrate stays silent and keeps the integrator running (deliberation). EMIT: the disinhibited channel ignites and externalizes the winning candidate; realized outcome updates rho, closing the average-reward loop. The whole loop is cortex(propose)->striatum(rank by v-rho)->vigor-gate(Psi)->thalamus(disinhibit/ignite)->emit->rho-update.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 NATIVE/ENDOGENOUS: at the average-reward fixed point the long-run emit rate self-stabilizes where marginal benefit of acting (A) exactly equals opportunity cost of time (G); since A and G are equal-magnitude opposite-sign at the balance of the SAME antagonism, the setpoint is the symmetric balance point, not a written constant. Local attraction: over-emitting raises the time cost faster than reward (rho rises, G grows, Psi falls); over-withholding forgoes reward (rho decays, A grows, Psi rises) -> Lyapunov well, |T'|<1. Endogeneity/INERT test passes: delete the G operator (no opportunity cost) -> Psi runs to the always-emit boundary; delete A -> always-silent boundary; the 1/2 cannot survive either deletion (so it is not a clamp). G0 legibility: candidates are produced by the deployed mouth over the receiver-fixed codebook V, and the vigor gate only modulates WHEN, not the alphabet, so V-mass is inherited from the generator. G1 recombination & dist>=5: parallel segregated cortico-striatal channels (one per factor) co-gate; the joint channel opens only when multiple factor-channels are simultaneously disinhibited, so the joint reachable-emit set is super-additive over single factors (the interaction term is the joint disinhibition event); INERT control = clamp factor-channels to fire independently -> composed_distinct collapses to max_single. G2 novelty: phasic-RPE generalization over a learned value feature space gives non-zero value to corpus-absent-but-on-manifold candidates, so the generator can select novel-yet-coherent items while a verbatim-playback control has zero off-corpus value -> 0 novel. honesty (support-membership/copy-or-abstain): when no candidate's v exceeds rho the vigor gate stays shut = ABSTAIN; this is structurally a copy-or-abstain factoring (emit only above-baseline supported value, else null), and is gate-capacity-disjoint because rho/vigor parameters are separate coordinates from the value/expressivity parameters (sweeping generator capacity does not move the opportunity-cost threshold). Generative attribution: ablating the phasic selector (shuffle v_i) drops both dist and falsifiable counts because the winner becomes random -> S_full>>S_ctrl.

## Not-LLM (a_no_llm_frame_trap)

There is no scale/attention prescription: the lever is a 1-D reward-rate control loop, not parameter count or context length. A transformer emits on every step by construction (no endogenous act-vs-wait order parameter); here silence is a first-class equilibrium state set by an opportunity-cost integrator. The breakthrough is a missing CONTROL STRUCTURE (vigor regulator) bolted beside the generator, exactly the substrate-first move of a_no_llm_frame_trap rather than 'bigger mouth'.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

$0 numpy: simulate a 1-factor bandit-emit with rho_{t+1}=rho_t+alpha(reward_t - cost - rho_t) and Psi=sigmoid(beta*(max_i v_i - rho_t)). Frozen-first bar: starting from rho=0 (over-emit) and rho=high (over-silent), Psi must converge to 0.5 +/- 0.02 within N steps with measurable contraction lambda<1. Decisive ablation: set cost=0 (G off) -> Psi must run to 1; set A off -> Psi->0. If 0.5 holds under either ablation, it is a clamp -> void.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the vigor gate as the emit decision in core/emit_policy.hexa (Psi from a tonic rho-integrator state in core/engine_cli.hexa), then measure via the single production entry cli/anima.hexa -- eval <ckpt>: G0/G1/G2 scored by core/g_gates.hexa (g_eval_g1/g_eval_g2, _g6_known_word_ratio) over the live mouth; Psi self-restoration and INERT-ablation traces read from core/emit_policy.hexa state dumps. byte-parity cross-check against core/emit_policy.py / engine_cli.py. No torch in the verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with neuromod_tonic_phasic_gain_bus (this census) / actor_critic_rpe_arena — distinct: tonic-DA = average-reward RATE = opportunity-cost-of-time setting VIGOR (act-vs-wait), Psi=1/2 as the average-reward fixed point; the vigor/opportunity-cost regulator is the differentiator.

Toy->engine claim is the Psi=1/2 average-reward fixed point and the G1 joint-disinhibition super-additivity; the novelty arm depends on the value feature space generalizing (scale-sensitive, a_toy_scale_recheck). Vigor gate is consciousness-balance (emit-drive) lane and must stay disjoint from the honesty recall_thr per a_substrate_disjoint.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
