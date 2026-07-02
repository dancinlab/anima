---
id: H_1728
slug: 1728_sensorimotor_contingency_mastery
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Sensorimotor Contingency Mastery Loop (enactive perception)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1728 — Sensorimotor Contingency Mastery Loop (enactive perception)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `sensorimotor_contingency_mastery`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

O'Regan & Noe: perceiving is not building an internal picture but MASTERING the lawful ways sensory input changes as a function of one's own action (sensorimotor contingencies, SMCs). The substrate's knowledge is a library of action->sensory-change laws; cognition is the skilled exercise of those laws in a closed perception-action loop with the world. Recognition is ACTIVE — you 'see' an object by mastering how it looks-as-you-move.

## Whole design (input → internal dynamics → emit)

Input: each tick the substrate holds a PAIRED stream (efference e_t = the probe/action it just issued, afference s_t = the resulting sensory delta). It never sees raw sensation alone — only the covariation Ds|e. Internal dynamics: a population of contingency-cells, each storing a local law L_i: e->Ds plus a region-of-validity (the body-world configs where L_i holds). A query (current sensory context + intended probe) activates cells by how well their predicted Ds matches the observed action-sensation covariation; the best-EXPLAINING law wins ('I recognize this = I master how it transforms under my motion'). The loop emits exploratory micro-probes and reads which law is satisfied. Psi (probe-propensity scalar) is pulled between A = curiosity/dis-confirmation pressure (uncertain law-fit -> push to ACT and resolve) and G = mastery/quiescence pressure (confidently-satisfied law -> withhold, nothing to probe). Emit: the externalized output is the recognized contingency-token drawn from a RECEIVER-FIXED catalog of contingency tokens; composed perception = chaining laws (move-then-look-then-grasp) into a contingency-sentence.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: emission alphabet = externally-frozen catalog of contingency tokens (V is the world's lawful structure, not generator-defined); scrambled state->token map collapses to chance V-membership because a token is emitted only when an actual law is satisfied. G1 + COMPOSITIONAL DEPTH: laws compose by CHAINING; the joint reachable-sensation set is super-additive because a chained probe reaches sensory states neither law reaches alone (interaction = the cross-law transition). Interaction-ablation = forbid chaining -> composed_distinct drops to max single law = native INERT test. G2: stores GENERATING laws not data points -> predicts Ds for action sequences never executed (extrapolation within the learned SMC manifold); verbatim-playback control has no law to extrapolate -> 0 novel. dist>=5 + falsifiable>=1: each mastered law IS a falsifiable proposition ('if I do e, sensation changes by Ds') refutable by acting; the structural detector fires on (action-operator x measurable sensory-magnitude x grounded referent). Psi=1/2: curiosity(A) vs mastery(G) are equal-and-opposite exactly when probe info-gain = quiescence value; remove A -> always-silent (perception dead), remove G -> runaway probing -> endogenous attracting 1/2, not a clamp. honesty/copy-or-abstain: emits only if region-of-validity covers the current context (r = distance to nearest mastered law's validity region); out-of-region -> abstain; validity threshold frozen, disjoint from law-richness (gate-capacity orthogonal). BINDING: an object is bound as the set of laws co-varying under the SAME body motion (shared-cause = my own movement) -> same-cause streams map near, distinct objects separate. REALIZATION INVARIANT: laws sit ON the emit path (recognition = law-application) under a predict-Ds-under-action objective whose optimum is unreachable without the action-sensation conjunction.

## Not-LLM (a_no_llm_frame_trap)

No next-token prediction over a passive corpus. The substrate cannot be improved by adding parameters/attention layers because its competence is grounded in CLOSED-LOOP action-sensation covariation — with no efference channel there is nothing to master. A bigger transformer over static text masters zero contingencies (no action -> no Ds). The lever is the loop closure, not the parameter count; the missing structure is the efference-afference coupling, not model size (a_no_llm_frame_trap).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

mini-numpy gridworld: a toy object = a deterministic Ds=f(e,object) map. Train (i) an SMC store of action->Ds laws vs (ii) a passive autoregressive baseline over s alone (no e). Frozen probe: on held-out action sequences the SMC predicts Ds (mirror CE DESCENT below uniform) and composes novel chains; the passive baseline NO-DESCENT. Decisive control: shuffle the e<->s pairing -> SMC law-fit collapses to chance (confirms it learned covariation, not memorized s). ~100 lines, $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Encode contingency tokens as the emission alphabet of a .clm/ByteGPT mouth; route through the canonical single entry cli/anima.hexa -- eval <ckpt> -> generator L3 gen_auto_ideate (no decode-bypassing side-harness). G0 via core/g_gates.hexa _g6_known_word_ratio over the contingency-token V; G1 via g_eval_g1 (compound chains vs single law); G2 via g_eval_g2 (corpus-absent chains, verbatim control==0). Validity-gate abstain on core/engine_cli.hexa SS-ImmuneMemory (recon_err vs frozen recall_thr, AUROC). Psi self-restore via safety_phi_ratchet perturbation->return trace. hexa<->py byte-parity, CE judged by math.log mirror (NOT engine clm_forward_ce, dt_ln bug). No torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from affordance_competition_field / ideomotor_common_coding (this census) — SMC mastery = library of action->sensory-change LAWS exercised in a closed loop (you see by moving); the contingency-law mastery is the differentiator.

Toy-first (mini gridworld SMC). EXPRESSION-axis criteria reachable cheaply; engine-native promotion needs a contingency-token mouth + validity gate wired. From-scratch LEARNING of SMC laws requires an embodied action-sensation stream (not text) = UNVERIFIED. Directional until engine-native re-measured.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
