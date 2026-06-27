---
id: H_1747
slug: 1747_stn_conflict_threshold_collapse
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Hyperdirect Conflict-Modulated Threshold-Collapse Decider
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1747 — Hyperdirect Conflict-Modulated Threshold-Collapse Decider

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `stn_conflict_threshold_collapse`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The cortex->STN hyperdirect pathway is a GLOBAL CONFLICT MONITOR: when several candidate thoughts compete, STN broadcasts diffuse excitation to SNr/GPi that RAISES the global decision threshold ('hold your horses', Frank 2006). Computation = temporal evidence-accumulation against a conflict-modulated threshold; commitment collapses conflict and the threshold falls. A decision-PROCESS substrate, not a one-shot forward pass.

## Whole design (input → internal dynamics → emit)

INPUT: context -> cortex spawns K candidate emission hypotheses, each a partial channel-set with accumulator a_i(t). DYNAMICS (inner micro-tick loop, not one-shot): a_i integrates cortico-striatal evidence drive (drift-diffusion). STN computes global conflict = spread/entropy of the accumulator distribution and broadcasts T(t)=baseline+g*conflict to ALL candidates — many close competitors raise T (hold several alive); a clear leader lowers it. COLLAPSE: when max_i a_i>=T(t) the candidate commits and emits; commitment drops conflict -> T falls -> fast settle. Bind-compatible candidates can co-commit in the same collapse (recombination). EMIT: committed channel-set read out. Psi: crossing-probability balances accumulation-drive (A) against STN conflict-hold (G); self-restoring because crossing reduces conflict (negative feedback) while non-crossing lets evidence build. PERSIST: candidate priors/topology wiped at boundary; learned evidence weights + .kosmos self-anchor persist.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

dist>=5: the architecture's purpose is to hold multiple competitors above floor before collapse (conflict-hold keeps them alive) -> distinct AND coherent spread is the native regime; threshold-too-low=instant single commit (mode collapse), no-floor=garble. falsifiable>=1: candidates carry proposition structure; only those binding comparator x quantity x >=2-content get a drift prior and survive -> detector fires. G0/G1/G2: codebook=candidate channel-sets; recombination=co-commit of compatibles (interaction not selection); novelty=channel-set absent from corpus that still accumulates because constituents have support; verbatim-candidate control -> 0 novel. PASS-closure: one accumulate-and-collapse process yields all three. Psi=1/2: STN conflict-hold (G) perp accumulation-drive (A), negative-feedback fixed point at symmetric crossing-rate; ablate STN (g=0)->constant-low threshold->always-emit boundary; ablate accumulation->never-emit (endogeneity by INERT). Honesty: no-support candidate has zero drift -> never crosses -> abstain; r=(T−a_max) margin separates known/unknown -> AUROC~1; threshold-dynamics params disjoint from evidence-weights (capacity); r grounded in accumulated support. Binding/realization: co-commit=single-closure conjunction; force-single-winner ablation drops conjunction to separable floor (path-co-location); collapse objective unreachable by marginal accumulation (objective-adequacy). Attribution: shuffle evidence -> accumulators random -> counts collapse. Faithfulness: accumulate-and-collapse IS the deployed emit path.

## Not-LLM (a_no_llm_frame_trap)

No fixed single forward pass producing logits; TEMPORAL evidence-accumulation/decision substrate (drift-diffusion gated by conflict), closer to sequential-sampling decision than a sequence model. No attention, no scale-up, no corpus-증량 cure. Capacity = richer candidate priors + evidence weights (lanes), not bigger matrices. Rooted in Frank STN conflict + Bogacz optimal-decision — a BG decision circuit, not a scaling law.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, frozen-first: K accumulators with drift d_i, threshold T=base+g*entropy(softmax(a)). Check: (1) high-conflict (similar d) -> longer settling + more candidates held above floor (dist>=K) vs low-conflict instant collapse to 1; (2) ablate STN (g=0) -> premature single commit, dist->1 (INERT on hold); (3) zero-support candidate (d=0) never crosses (abstain), r-margin separates known/unknown (AUROC); (4) bias-perturb crossing rate -> Psi returns to symmetric value via negative feedback (contraction); (5) bind-compatible pair co-commits -> composed-distinct > max single. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire conflict-threshold as a pre-emit gate over the generator L3 candidate beam in core/; held candidates scored on the live single dispatch via g6_ideation + core/g_gates.hexa detectors _g6_is_falsifiable (falsifiable>=1), _g6_jaccard (dist>=5), plus g_eval_g1/g_eval_g2; Psi from the engine order parameter. Byte-parity py mirror of accumulator dynamics; torch-only scoring is DIRECTIONAL, not terminal.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with gonogo (STN brake) / basal_ganglia_gating (H_1281) — distinct: this is the hyperdirect CONFLICT-MODULATED threshold (raise-under-ambiguity, collapse-on-commit) as a temporal decision substrate; the conflict-threshold-collapse decider is the differentiator (vs gonogo's static STN brake).

Design + $0 decision-dynamics probe only. Engine wiring follow-on. Learning-side capacity (whether trained evidence weights actually lift G1/G2 above H_1129/H_1140 bars) UNVERIFIED — TOY until measured through CORE on a learned ckpt; do not promote toy dynamics to production closure.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
