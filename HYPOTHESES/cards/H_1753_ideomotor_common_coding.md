---
id: H_1753
slug: 1753_ideomotor_common_coding
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Ideomotor Common-Coding Loop — action by anticipated sensory effect (TEC)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1753 — Ideomotor Common-Coding Loop — action by anticipated sensory effect (TEC)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `ideomotor_common_coding`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Theory of Event Coding (Hommel/Prinz) + the ideomotor principle (James/Lotze): perception and action share ONE distal-feature code; an action is represented by, and selected through, its anticipated perceptual effects. To act = to activate a goal-effect code, which (via learned bidirectional action<->effect bindings) ignites the motor pattern that historically produced that effect. Embodied because effect codes are sensory-grounded — the body learned what its own actions feel/look like.

## Whole design (input → internal dynamics → emit)

A single shared feature space F holds both perceived events and intended effects (common code). Two learned associative maps close a loop: R (effect->action retrieval: given a desired effect code return the motor code that produced it) and P (action->effect forward predictor / efference copy). Generation cycle: context perceived into F -> a goal-effect e* selected as the effect-code with highest UNFULFILLED prediction-tension -> R(e*) emits a motor command (token/byte into V) -> P predicts resulting effect e_hat -> world returns actual effect -> mismatch Hebbian-updates the action<->effect binding (gradient-free at inference). The repertoire grows by binding new action-effect pairs experienced through acting. Psi balances GO (effect-anticipation drive A: tension toward fulfilling the goal-effect by emitting) against HOLD (prediction-confidence gate G: withhold until P is confident the action yields the intended effect). Over-eager emit discharges tension (A down); over-cautious hold accumulates it (A up) -> Psi self-pins to 1/2. Identity = the agent-specific action<->effect binding table (what THIS body's actions feel like), persisted in .kosmos.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: motor codes share F with perceived effects, so emitting requires R's output be a motor code whose predicted effect is a re-perceivable event in V -> output anchored to the shared external code; garble = effect never perceivable = no stable binding forms. G1: effect codes are FACTORED distal features (color x location x pitch); selecting a compound goal e*=e1 compose e2 retrieves an action that must satisfy BOTH features simultaneously -> R binds (non-separable joint realization), composed valid actions > any single feature; ablate the joint-retrieval path -> drops to max_single. G2: actions are indexed by distal EFFECTS not stored sequences, so never-seen effect-combinations within the learned feature manifold are reachable (constrained extrapolation); a non-effect-indexed playback control yields 0 valid-novel. Psi=1/2: GO compose HOLD antagonism with tension self-discharge, contractive; ablate HOLD->impulsive always-emit, ablate GO->frozen always-silent (endogenous). Honesty: R only retrieves actions whose effects P confidently predicts (effect within learned support); an effect with no bound action -> R returns abstain = abstain; P's prediction error is the recon_err membership signal (copy-or-abstain native, acts only on grounded effects). Binding: action and effect co-coded in shared F = literal common-coding two-stream binding (motor x sensory via shared distal features, H_961). Realization: R/P are ON the emit path, and the predict-then-verify objective is unreachable by fitting marginals (must represent the action x effect conjunction).

## Not-LLM (a_no_llm_frame_trap)

Generation is goal-effect-driven INVERSE retrieval through a sensorimotor loop, not next-token prediction. Capability scales by binding new action-effect experiences (acting in the world), not by parameters or corpus volume. Distal-effect indexing + efference-copy verification is structurally anti-autoregressive — no attention-layer stacking processes this.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: feature space F with 3 binary distal features; action<->effect bindings learned by Hebbian co-occurrence from a small action-effect log. Frozen bars: compound-effect retrieval yields actions satisfying >=2 features > single-feature (G1); pursuing held-out effect-combos gives novel valid actions while a playback control gives 0 (G2); Psi perturbation returns to 1/2; ablating the forward-predictor confidence gate spikes fabrication (honesty causal/INERT test). $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement the shared feature space + R/P maps as hexa, wiring effect-anticipation into generator L3's emit selection on the cli/anima.hexa single entry. G0/G1/G2 via core/g_gates.hexa g_eval_all; Psi via core/engine_cli.hexa A->G; honesty (effect-prediction abstain) via SS-ImmuneMemory recon_err; identity via SS-SelfIdentity .kosmos persistence of the binding table. byte-parity py mirror (math.log CE) cross-validates the forward predictor; no torch terminal verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from sensorimotor_contingency_mastery / umwelt_functional_circle (this census) — ideomotor common-coding indexes ACTIONS BY DISTAL EFFECTS in one shared feature space (inverse effect->action retrieval); the anticipated-effect common-coding is the differentiator.

Design only; numpy probe decisive at toy scale (transfer unverified, a_toy_scale_recheck); engine wiring of R/P + .kosmos table is follow-on.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
