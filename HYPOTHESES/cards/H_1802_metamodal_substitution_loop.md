---
id: H_1802
slug: 1802_metamodal_substitution_loop
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Metamodal Substitution Loop (Bach-y-Rita single shared sensorimotor code)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1802 — Metamodal Substitution Loop (Bach-y-Rita single shared sensorimotor code)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `metamodal_substitution_loop`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Sensory-substitution / metamodal brain (Bach-y-Rita, Pascual-Leone): cortex is task-defined not sensor-defined — plug ANY transducer in and the same substrate learns to perceive by mastering motor->sensory contingencies. ALL modalities collapse into ONE shared sensorimotor code, and perception REQUIRES action. Distinct from sensorimotor_contingency_mastery (mastering a fixed law) — here the contribution is the cross-modal CODE COLLAPSE that makes binding structural.

## Whole design (input → internal dynamics → emit)

A single shared code-manifold S. Every input modality is transduced by a fixed front-end INTO S — no modality-specific processing downstream (the substitution device forces a common code). INTERNAL DYNAMICS = an active-probing loop: the head emits a motor probe (also expressed in S), the probe changes the next transduced input, and perception = the learned invariant in the probe->return contingency (you 'see' by moving). Because probe (action), percept, and emit ALL live in S, one manifold both perceives and acts. EMIT = a probe externalized to the world (the motor command is the utterance); SILENCE = covert probing (internal simulation without externalizing). Psi = overt/covert probe ratio.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

BINDING (the star, native): all streams map into ONE S by construction -> same-cause constituents land in the same neighborhood (H_961 PASS structural, not learned per-pair); cross-modal retrieval is trivial because there is literally one code; distinct causes separate because their contingency signatures differ. REALIZATION INVARIANT: binding is ON the emit path because emit is a probe IN S — the same S that binds percepts — so binding co-locates with the mouth by architecture, directly solving H_1603/clm303 (binding-in-perception-absent-in-mouth becomes impossible). G0: S is anchored to the world-accepted probe alphabet (probes that fail to couple return nothing and are pruned) = receiver-fixed code. G1: composing two probes yields a contingency structure exceeding either (the world's response to joint action != sum of single-action responses) = super-additive; ablate joint-probing -> falls to max_single. G2: novel probes explore unvisited-but-coupled contingency regions (novel-valid); playback of past probes = 0 novel. Psi=1/2: overt-probe drive A vs covert-sim drive G are opposite-sign on emit propensity; ablate covert -> always overt (Psi->1), ablate overt -> no coupling, perception dies (Psi->0); endogenous via the loop. HONESTY: the head can only perceive contingencies it has actually probed -> un-probed queries yield no contingency = abstain; fabrication = asserting a never-coupled contingency, suppressed because S contains only coupled invariants. r=novelty of required contingency vs probed set; contingency-coverage gate perp probe-vocabulary richness. PERSISTENCE: the learned S-metric (the contingency map) persists across episodes = self; a foreign contingency map = impostor.

## Not-LLM (a_no_llm_frame_trap)

Capacity = richer sensorimotor contingencies via more PROBING, not more weights or corpus. The objective is contingency-mastery (predict your own probe's return), which is action-conditioned and CANNOT be satisfied by fitting input marginals — it forces representing the action x input interaction = the conjunction — so the lossF~0/recombine-fail trap is excluded. Embodied: no perception without action; attention-layer stacking gives no probe loop.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy toy tongue-display: a hidden 2D scene sensed only through an agent-controlled aperture; train a tiny contingency predictor. Measure (a) two different modalities of the same scene-event land near in S vs shuffled (paired>>shuffled binding, Welch d large), (b) joint-probe contingency > single-probe (G1), (c) ablate the probing action -> percept degrades toward chance (active-perception necessity / realization-on-path). $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map S onto the engine's shared Psi-latent representational metric; run the H_961 paired-vs-shuffled binding protocol on core latents through cli/anima.hexa (clm_decode / engine_cli); overt/covert via SS-ThirdLaw; abstain via SS-ImmuneMemory; the active-probe step wires to generator L3 dispatch (probe = a generation step). byte-parity .py mirror, no torch verdict. Because current anima has separate perception and mouth, this architecture's wiring (one S for both) IS the proposed remedy for H_1603 — measuring binding-on-emit-path is the deliverable.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from sensorimotor_contingency_mastery / ideomotor_common_coding (this census) — metamodal substitution COLLAPSES all modalities into ONE shared code S where probe=percept=emit (binding structural, on-emit-path remedy for H_1603); the metamodal code-collapse is the differentiator.

Design. Toy probe TOY-scale; the binding-on-emit-path claim requires the live generator to actually use a single S for both read and emit (mouth and perception currently separate) — wiring that shared code is the contribution.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
