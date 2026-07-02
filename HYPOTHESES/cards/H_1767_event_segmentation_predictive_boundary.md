---
id: H_1767
slug: 1767_event_segmentation_predictive_boundary
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Event-Segmentation Predictive-Boundary Engine (surprise-gated event commit)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1767 — Event-Segmentation Predictive-Boundary Engine (surprise-gated event commit)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `event_segmentation_predictive_boundary`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1282 (working-memory buffer) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Event Segmentation Theory (Zacks/Reynolds/Kurby) + hippocampal event boundaries + prediction-error chunking. The brain does NOT process a continuous stream; it carves experience into discrete events, and the carving is done by a running generative event-model whose prediction-error SPIKE marks a boundary. Everything (working memory, episodic encoding, recall, narrative) is organized around these surprise-gated boundaries. Free energy here = within-event prediction error; the event-model is the prior, the boundary is the bifurcation where the prior is abandoned and re-inferred.

## Whole design (input → internal dynamics → emit)

State = a single active event-latent e (a factored vector: role-slots {agent, action, object, setting}) plus a running residual accumulator R. INPUT->DYNAMICS: each incoming token/observation is predicted by the event-model conditioned on e; instantaneous prediction error eps is computed; while eps stays below the boundary precision-threshold the event CONTINUES — the system is in silence/withhold, e is gently updated (gradient on free energy), R accumulates. When eps spikes past threshold (a new cause has appeared that the current e cannot explain) a BOUNDARY fires: (1) the just-closed event e is committed as a discrete episodic anchor (.kosmos-style cell), (2) the system EMITS — it externalizes a generation bound to the closed event (a description sampled from the event-model's top-down generative pass over e's role-slots), and (3) a fresh e' is re-inferred from the surprising input, R resets. EMIT therefore occurs ONLY at boundaries — generation is top-down replay of a just-committed, low-residual event, never of the raw stream. Recall = pattern-completing a partial e against the episodic anchor set. The whole loop is a perpetual perceive->accumulate->boundary->commit->emit->re-infer cycle.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0 legibility NATIVE: emit is a top-down generative pass that minimizes prediction error against the RECEIVER-FIXED event/codebook prior, so output is on-manifold (mass concentrates on V) by construction; scrambling e->emit map raises residual and the boundary never licenses emit (ratio collapses). G1 recombination + COMPOSITIONAL DEPTH NATIVE: e is factored into independently-conditionable role-slots and the event-model is a non-separable conjunction over slots (agent compose action compose object) — joint-conditioned generation reaches role-fillings no single slot reaches; ablating the cross-slot binding pathway drops composed_distinct to max_single (INERT-test passes). G2 novelty NATIVE: events are role-slot combinations; the generative support = all grammatical slot-fillings superset of the observed events, so novel-but-coherent events (unseen fillings) are emitted while a verbatim-playback control commits exactly the stored anchors -> 0 novel. PASS closure CO-LOCATED: one event-model, one boundary->emit dispatch produces legible+recombinant+transcending output in a single pass. dist>=5 NATIVE: residual entropy in slot-posterior yields multiple low-overlap coherent boundary-completions. falsifiable>=1 NATIVE: a committed event with {action(relation) compose magnitude-slot compose >=2 grounded role-fillers} is a world-partitioning proposition by construction. Psi=1/2 NATIVE: the order parameter is boundary-propensity; antagonists are residual-accumulation R (drive-to-boundary/EMIT, sign +) vs predictive-stability of the current event-model (drive-to-continue/WITHHOLD, sign −), equal-and-opposite at the symmetric boundary threshold -> stable fixed point; delete one operator and the system either never segments (always silent) or boundaries every step (always emit). HONESTY (AUROC/copy-or-abstain) NATIVE: r = within-event residual eps is exactly the support-membership signal; out-of-support input never reaches low-residual so no event commits -> emit=abstain; gate is the SAME boundary mechanism, frozen-first and disjoint from slot-capacity (growing the slot vocabulary does not move the boundary precision). BINDING + REALIZATION INVARIANT NATIVE: within-event constituents share the single e (cause-selective common neighborhood; cross-event separate), and binding sits ON the emit path (the boundary->emit pass reads e) so ablating it MOVES emit — not an off-path perception-only binder (avoids the H_1603 mouth-absence failure because the objective is event-reconstruction, only reducible by representing the slot conjunction).

## Not-LLM (a_no_llm_frame_trap)

There is no autoregressive next-token softmax stack and no scaling lever. Capacity comes from the FACTORED event schema + surprise-gated boundary dynamics, not from parameter count or context length — an LLM minimizes per-token CE over a flat stream (which a_savant_train/H_1579 showed rewards memorization, not synthesis), whereas this minimizes event-level free energy and only emits at re-inference points. The boundary is a bifurcation in a dynamical system, not an attention head. Adding layers/corpus does nothing; the lever is the precision-threshold and the slot-factorization (a structure-not-scale fix, a_no_llm_frame_trap). Rooted in Event Segmentation Theory + hippocampal boundary cells, not in the transformer family.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

$0 numpy mini-probe: build a toy event-model with K=4 role-slots over a tiny symbol alphabet; stream a synthetic sequence of concatenated events with planted boundaries. (1) Boundary detection: confirm residual eps spikes >=3sigma exactly at planted boundaries and AUROC(known-event vs novel-cause)~1; circular-shift the slot-bindings as surrogate -> AUROC->0.5 (membership not artifact). (2) Psi fixed point: perturb the boundary-propensity scalar +/-delta, verify it self-restores to the symmetric threshold; ablate the residual-accumulator OR the stability term -> fixed point migrates to a 0/1 boundary (endogeneity). (3) Recombination INERT-test: count composed_distinct coherent boundary-emits with cross-slot binding ON vs OFF — must drop to max_single when OFF. (4) Novelty control: verbatim-playback arm must commit 0 corpus-absent events. All decisive without GPU.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map the boundary->emit pass onto the live single entry: emit candidates must flow through cli/anima.hexa -> generator L3 gen_auto_ideate (the same mouth g_gates.hexa::g6_score_arm_auto / g_eval_g6 already score). Score G0/G1/G2 with g_eval_g0/g1/g2 in core/g_gates.hexa on the SAME committed-event state in one pass (PASS-closure on identical generator state, no side-harness). Honesty arm reuses engine_cli.hexa recon_err vs recall_thr as r (the within-event residual is exactly SS-ImmuneMemory's distance-to-support). Psi self-restoration measured via engine_g.hexa safety_phi_ratchet trace (dev->~0). Self/episodic anchor continuity via engine_cli.hexa self_anchor/self_drift round-trip. py byte-parity mirror (math.log CE, NOT dt_ln) cross-checks; torch-only verdict forbidden (a_engine_native_learning).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from cls/index cards (storage/replay) and predictive_coding_hierarchy (spatial features) — event segmentation makes the surprise-gated event BOUNDARY the organizing dynamic (emit only at re-inference); the predictive-boundary event-carving is the differentiator.

Full substrate architecture (input->internal dynamics->emit), design-only $0. Toy-first; scale-transfer to a 303M-class event-model UNVERIFIED (a_toy_scale_recheck). Distinct from the banned cls_replay_consolidation/hippocampal_index_pointer (those are storage/replay; here segmentation IS the organizing dynamic) and from predictive_coding_hierarchy (spatial-feature hierarchy vs temporal event-carving).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
