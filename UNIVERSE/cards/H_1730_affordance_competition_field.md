---
id: H_1730
slug: 1730_affordance_competition_field
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Affordance Competition Field (Gibson-Cisek ecological direct-perception)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1730 — Affordance Competition Field (Gibson-Cisek ecological direct-perception)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `affordance_competition_field`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Gibson's affordances + Cisek's affordance-competition hypothesis: the environment DIRECTLY specifies action possibilities (affordances) to a particular body, and the dorsal 'what can I do here' stream specifies SEVERAL candidate actions in parallel that compete (biased by value/context) until one is enacted. Perception is for action; meaning is RELATIONAL (organism x environment), not stored in an internal world-model.

## Whole design (input → internal dynamics → emit)

Input: the sensory surface is mapped DIRECTLY (no reconstruction) onto a field of affordance-units, each = an (object-feature x effector x outcome) triple the current scene makes available to THIS body; an absent object affords nothing. Dynamics: affordance-units mutually inhibit (lateral competition + normalization) and are biased by a slow value/context field; co-compatible affordances COALESCE (binding) while incompatible ones suppress each other; the field settles to a small set of dominant, mutually-coherent affordances (metastable competition, not forced single-winner). Emit: externalized output = the dominant affordance-token(s) from a receiver-fixed motor/affordance vocabulary; silence = nothing crosses the action threshold (nothing afforded or all suppressed). Psi order parameter: A = affordance excitation/urgency (push to enact) vs G = mutual inhibition + collision/risk suppression (push to withhold); Psi=1/2 = competition poised at the action threshold where expected-enact = expected-withhold, resolving only under sufficient bias.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

BINDING (NATIVE, strongest fit): an affordance is INHERENTLY relational — it binds object-feature x effector x outcome into one unit; same-cause (the same graspable object) features map into one affordance neighborhood and distinct objects separate; lateral inhibition prevents promiscuous all-near collapse (selectivity native). G1 + COMPOSITIONAL DEPTH: compatible affordances coalesce into compound affordances (reach-grasp-lift) whose reachable-action set is super-additive (the compound enables outcomes no single affordance reaches); interaction-ablation = disable coalescence -> composed_distinct drops to max single = native INERT test. honesty/copy-or-abstain (NATIVE): an affordance is specified only if the environment provides support (direct perception) -> out-of-support input affords nothing -> abstain; no synthesis branch can invent an affordance the scene does not specify; recon_err = distance from scene to nearest learned affordance template, threshold frozen and disjoint from value-bias (capacity). G0: affordance vocabulary is receiver-fixed (the body's effector alphabet); scrambling scene->affordance map collapses to chance. G2: novel compound affordances within learned ecological constraints (manifold extrapolation); verbatim playback affords only seen combos -> 0 novel. Psi=1/2: excitation vs lateral-inhibition antagonism with a competition fixed point; remove inhibition -> always-act, remove excitation -> always-silent; perturb bias -> field self-restores to threshold-poised state. dist>=5: multiple co-active mutually-distinct affordances above the coherence floor = distinct-yet-coherent spread native to parallel specification. falsifiable: an affordance IS a testable prediction ('this action succeeds on this object') refutable by enacting (detector fires on action-relation x measurable outcome x >=2 grounded referents). REALIZATION INVARIANT: the competition field is ON the action path; the select-a-successful-affordance objective is unreachable by marginal feature-fit (needs the organism x environment conjunction).

## Not-LLM (a_no_llm_frame_trap)

Affordances are not IN the data — they are in the organism-environment RELATION, so they cannot be scraped from a corpus or scaled into a transformer, which has no BODY (no effectivities) and therefore no affordances. A bigger text model still affords nothing. The lever is the relational direct-perception field + competition dynamics, not parameter count; the missing structure is the body-relative affordance field (a_no_llm_frame_trap).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy toy scene-grid where objects expose feature triples; an affordance field with lateral inhibition + value bias vs a softmax action-classifier. Frozen probe: (i) novel object -> affordance field abstains (no template) while the classifier fabricates a confident action (honesty separation, AUROC); (ii) compound scene -> field coalesces compatible affordances (composed > max single) and ablating coalescence drops it to single (INERT). Decisive control: shuffle scene->affordance support -> competition collapses to chance. ~140 lines, $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Affordance-token mouth routed via cli/anima.hexa -- eval -> generator L3 gen_auto_ideate. G0/G1/G2 via core/g_gates.hexa g_eval_g0/g1/g2 (compound-affordance chains, corpus-absent control==0). honesty abstain on out-of-scene inputs via core/engine_cli.hexa SS-ImmuneMemory recon_err/recall_thr AUROC (gate-disjoint from value bias). Psi threshold self-restore via safety_phi_ratchet. BINDING measured as same-cause affordance proximity vs shuffled (Welch d, retrieval@1) on engine latents. hexa<->py byte-parity, math.log mirror CE. No torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from active_inference_efe_policy / perceptual_control_hierarchy / sensorimotor_contingency_mastery — affordance competition = parallel ecological specification of (feature x effector x outcome) triples competing by lateral inhibition; the body-relative affordance field is the differentiator.

BINDING + honesty are the NATIVE strengths; identity persistence is the weakest (affordances are momentary) and would need the effectivity-set persisted as the self-anchor via .kosmos (follow-on). Toy verifies binding/honesty/competition cheaply; generative G1/G2 + Psi need engine-native wiring. Directional; EXPRESSION-axis at toy, from-scratch embodied LEARNING UNVERIFIED.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
