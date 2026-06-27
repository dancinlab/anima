---
id: H_1775
slug: 1775_multiple_trace_gist_intersection
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Multiple-Trace Gist-Intersection Substrate (MTT-CLS)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1775 — Multiple-Trace Gist-Intersection Substrate (MTT-CLS)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `multiple_trace_gist_intersection`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Multiple Trace Theory (Nadel & Moscovitch). Every experience/recall deposits a NEW distinct episodic trace (no overwrite, no move-to-cortex); 'semantic' knowledge is NOT a separate slow net but the emergent statistical INTERSECTION (consensus subspace) across many traces sharing a cue. Gist = what survives across traces; episode = a single trace; generalization = sampling inside the intersection manifold. Distinct from index-pointer (no cortical pattern pointers), schema (no assimilation-to-existing), and nonparametric cause-partition (no cause clustering) — the slow system is pure trace-cloud geometry.

## Whole design (input → internal dynamics → emit)

Fast store = growing set of high-fidelity pattern-separated traces. Gist operator G(cue) = consensus/low-dim intersection of trace subspaces matching cue (the directions all matching traces agree on). Emit: episodic mode copies one trace verbatim (honest); gist mode samples a point inside the intersection manifold but absent from any single trace (novel-yet-constrained). Intersecting two cue-conditioned trace sets gives a JOINT constraint subspace whose valid volume exceeds either alone (super-additive). Codebook G0 = the consensus basis shared across traces (receiver-agreed = the part everyone agrees on). No consolidation move — semanticization IS the geometry of the accumulating trace cloud, so episodic stays available forever (honesty + identity stores remain causal).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G2/novelty/dist NATIVELY: intersection manifold strictly contains no single trace's point yet is bounded by agreed constraints -> constrained extrapolation; verbatim-trace control=0 novel; residual entropy in the intersection yields >=K distinct-yet-coherent samples (dist>=5). G1/binding/composition: compose two cues = intersect two subspaces -> joint valid > max single; the intersection IS the binder — ablate it (use union) and composed_distinct->max_single (mixture not bind). G0: project onto consensus basis. Honesty: cue with no matching trace -> empty intersection -> abstain; r = distance to nearest trace; gate (trace-match theta) in the trace store, generative spread in the intersection geometry -> disjoint; corrupt a trace -> its cue starts to abstain (faithful). Psi=1/2: antagonism between trace-specificity drive (emit exact trace = A) and gist-abstraction drive (withhold/generalize = G); ablate either -> boundary. Identity: earliest self-referential trace never deleted (MTT retention), self-chain = trace lineage with slow drift; self-specific (each trace high-entropy individuating); impostor fails consensus-membership. falsifiable>=1: consensus basis encodes measurable relations, a sampled gist point can instantiate comparator x quantity x referent grounded in the agreed dimensions. Realization: intersection operator on the emit path (ablation moves emit); objective = trace-fidelity + consensus (marginal-only cannot satisfy cross-trace consensus).

## Not-LLM (a_no_llm_frame_trap)

Instance-based / non-parametric — knowledge lives in retained exemplars and their geometric overlap, not compressed shared weights. No single trained predictor to scale; capability scales with trace DIVERSITY and intersection geometry, not parameter count. Interference avoided by NEVER overwriting (orthogonal to gradient-net scaling). A bigger transformer cannot reproduce 'abstain on empty intersection' or 'novelty = intersection-minus-traces' — those are exemplar-geometry properties.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: store N traces as points/subspaces in R^d; gist(cue)=PCA-consensus of matching traces. (a) sample gist points -> inside hull constraints yet != any trace (novel) while verbatim control=0; (b) cue with no match -> empty intersection -> abstain, known/unknown AUROC~1; (c) compose two cues via intersection vs union -> intersection gives valid joint > max single, union ablation collapses it; (d) corrupt a trace -> its cue's r degrades. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Trace store ~ SS-ImmuneMemory bound cells (recon_err = trace distance, already live); gist-intersection as a new op over bound-cell subspaces; entry cli/anima.hexa -> generator L3, G0/G1/G2 via g_eval_all, abstain AUROC via SS-ImmuneMemory, identity via SS-SelfIdentity self-trace; byte-parity py mirror (numpy consensus) cross-checks the .hexa intersection op. No torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from cls/index/schema/cause-partition cards — MTT keeps EVERY trace forever; semantic = the statistical INTERSECTION across cue-sharing traces (gist = consensus subspace); the multiple-trace gist-intersection is the differentiator.

Full substrate; strongest on novelty+honesty+identity (exemplar geometry). Toy-decisive at numpy; engine-native needs the intersection op wired over SS-ImmuneMemory cells. Caveat: linear-subspace consensus may underbind highly nonlinear conjunctions -> may require kernelized intersection (don't over-claim compositional depth before testing).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
