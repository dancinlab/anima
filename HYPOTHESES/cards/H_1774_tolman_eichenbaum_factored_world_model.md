---
id: H_1774
slug: 1774_tolman_eichenbaum_factored_world_model
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Factored Structure-x-Content World-Model (TEM-CLS)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1774 — Factored Structure-x-Content World-Model (TEM-CLS)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `tolman_eichenbaum_factored_world_model`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Tolman-Eichenbaum Machine (Whittington 2020) as a CLS-unifying generative model. Slow medial-entorhinal system learns ENVIRONMENT-INVARIANT relational STRUCTURE (an abstract transition/group-action graph reusable across worlds = the generating grammar); fast hippocampal system binds current sensory CONTENT to current structural position via conjunctive cells; lateral-entorhinal supplies grounded content. Knowledge is factorized structure-x-content, enabling zero-shot inference of unobserved content at known structural positions — the explicit unification of hippocampal-entorhinal coding with CLS, NOT a spatial-metric operator.

## Whole design (input → internal dynamics → emit)

Slow system maintains abstract state g and a learned transition operator T_a(g) (action a moves through structure), identical across episodes/worlds. Fast system holds memory M binding (g-x-x): conjunctive cells = position x content. Inference loop: from g predict g'=T_a(g); query M for content bound at g' (pattern-completion); if bound -> emit retrieved content (grounded); if a NEW world -> one-shot bind observed x to g. Emission = traverse the structural graph and compose the content expected there. Because structure is shared and content swappable, the system infers content combinations never observed (apply known relational scaffold to new sensory set). The factorization is the binding operator; recombination = same structure x new content; novelty = valid positions whose content is inferred, not stored.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G1/binding/compositional-depth NATIVELY: structure-x-content is a non-separable conjunction (conjunctive cells), joint image positions x contents >> either factor (super-additive); held-out novel combo = known position + content seen elsewhere -> systematic (Fodor-Pylyshyn) generalization; interaction-ablation (force structure+content additive) collapses conjunction to separable floor. G2/dist: zero-shot content inference at unvisited positions = valid corpus-absent outputs; verbatim-recall control=0. G0: content emitted in the shared sensory/lateral-EC codebook. Honesty/support: position with NO bound conjunctive cell -> no completion -> abstain; r = completion confidence (distance to bound cell); gate params in M (fast) disjoint from structural-grammar params (slow), disinhibiting structure doesn't move theta; groundedness because completion reads actual bound content. Psi=1/2: antagonism between structure-driven prediction (generalize forward = G, withhold raw obs) and content-driven grounding (commit to observed = A); ablate either -> boundary. Identity: agent's structural graph + trajectory anchor (g-trace) persists across sessions as the self-index; self-specific because learned structure+trajectory is high-entropy individuating; ablate the g-store -> fresh self each episode.

## Not-LLM (a_no_llm_frame_trap)

An explicit factored generative world-model with a separate REUSABLE structural grammar — not a monolithic sequence predictor. Transformers entangle structure and content in shared weights and must re-learn relations per distribution; TEM's zero-shot transfer comes from FACTORIZATION + conjunctive binding, a structural choice no amount of scale gives a non-factored net. Compositional generalization is architectural, not emergent-from-data-volume.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: learn transition structure on graph-world A (slow T) + bind content X_A; deploy on graph-world B with same structure, new content X_B; measure zero-shot content prediction at unvisited (position,content) pairs vs a non-factored lookup baseline (must be 0 zero-shot). Ablate conjunctive binding (replace g-x-x with g+x) -> novel-combo accuracy -> chance. Probe Psi: bias predict-vs-observe and check return to balance. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire structural-T as a slow lane, conjunctive M as a fast lane; entry via cli/anima.hexa generator L3. G1 via g_eval_g1 (composed_distinct>max_single on novel structure-x-content), G2 via g_eval_g2 (zero-shot positions corpus-absent, control=0), honesty via SS-ImmuneMemory completion-confidence AUROC; byte-parity py mirror for the transition operator. No torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with grid/entorhinal cards + cls (this census) — distinct: TEM factorizes STRUCTURE (reusable transition grammar) x CONTENT (conjunctive cells) for zero-shot recombination; the factored structure-x-content world-model is the differentiator (not a spatial-metric operator).

Full substrate; strongest on binding/composition/novelty. Toy-decisive at numpy; engine-native G1/G2 closure needs the two lanes wired. Caveat: structural grammar must be LEARNED (slow); inherited/fixed structure is weaker and risks scale collapse (a_toy_scale_recheck — cf. H_1569 inherited-repr collapse at 12000B).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
