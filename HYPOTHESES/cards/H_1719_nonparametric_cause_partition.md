---
id: H_1719
slug: 1719_nonparametric_cause_partition
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Nonparametric Common-Cause Partition Engine
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1719 — Nonparametric Common-Cause Partition Engine

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `nonparametric_cause_partition`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Perception = inferring the CAUSAL STRUCTURE of inputs: how many hidden causes generated the data and which observations share a cause (Kording 2007 causal inference; Tenenbaum/Griffiths nonparametric Bayesian structure learning; Friston generative models are over causes). The generative model's STRUCTURE (number/identity of causes) is itself a latent inferred under a Chinese-Restaurant-Process prior — free-energy minimization done over structure, with generation = top-down prediction of each cause's constituents.

## Whole design (input → internal dynamics → emit)

Input: multi-stream feature vectors arrive each tick. Internal dynamics: maintain a CRP mixture over latent causes; each cause c carries a generative profile (prototype + precision) that PREDICTS its constituents top-down, and bottom-up prediction error drives re-assignment. Variational inference per tick either assigns incoming observations to existing causes or, via the CRP 'new table' mass alpha, INSTANTIATES a fresh cause — so capacity grows by adding causes, not parameters. A learned conjunction prior can bind >=2 co-active causes into a composite 'hyper-cause' spanning their product space. Emit: externalization is sampling the MAP cause (or composite) and decoding it through a RECEIVER-FIXED codebook V (the cause->symbol decoder = the canonical mouth). Decoding a freshly-instantiated cause yields constraint-valid but corpus-absent output. Psi (emit propensity) = the operating point where the drive-to-externalize-the-MAP-cause (A, exploit: reduce expected free energy by committing) meets the drive-to-keep-inferring (G, epistemic: reduce partition-posterior entropy before committing); these are equal-and-opposite when posterior confidence = residual surprise, giving a balance attractor.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

BINDING (native, structural): common-cause inference IS the binding operator — two streams' observations bound iff assigned the same cause; selectivity (not promiscuous collapse) falls out of the mixture posterior, exactly the paired-vs-shuffled near-far requirement. G1 recombination / COMPOSITIONAL DEPTH: the conjunction (hyper-cause) prior is a non-separable f(a,b) over a bounded cause vocabulary -> super-additive valid-output cardinality and Fodor-Pylyshyn systematicity to unseen cause combinations; zeroing the conjunction prior is the decisive INERT test (composed_distinct->max_single). G2 novelty: CRP 'new table' lets supp(P_model) strictly contain supp(data) while the cause prototype keeps the excess on-manifold; a verbatim-playback control instantiates no new cause -> 0 novel. HONESTY / support-membership + copy-or-abstain: marginal likelihood under the current cause set is the graded distance-to-support scalar (recon_err analog = distance to nearest cause prototype); when no cause explains the input the CRP says 'needs a new cause but has no data' -> abstain, so emission provenance is closure(causes) union {abstain}. Groundedness: the membership signal reads actual stored prototypes, so content-ablation shifts it. PASS closure is one-process because all three gates read the SAME decoded MAP-cause through one dispatch.

## Not-LLM (a_no_llm_frame_trap)

Not a sequence predictor: there is no attention, no autoregressive token CE. Combinatorial productivity comes from a STRUCTURED latent (cause vocabulary x conjunction prior) whose marginal-likelihood objective with the CRP+conjunction prior has its optimum unreachable by fitting token marginals — directly attacking the clm303/H_1129 G1 wall where CE never rewards composition. Capacity scales by data-driven structure discovery (adding causes), not by larger transformers or more corpus.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy CRP mixture on a 2-stream toy where some pairs share a generated cause: (a) common-cause posterior for true-pairs >> shuffled-pairs (binding effect size + retrieval@1); (b) feed held-out novel factor-combos -> count new-cause instantiations decoded to valid symbols (n_novel>=3) while a corpus-playback control reads 0; (c) ablate the conjunction prior -> composed_distinct collapses to max_single (G1 INERT). All $0, frozen-first bars.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire cause-partition as a SS-Causal lane in core/engine_cli.hexa (.hexa CRP assignment + byte-parity py mirror using math only, no torch); route the cause->symbol decoder into generator L3 so emission passes the canonical single entry cli/anima.hexa. Score G0/G1/G2 via core/g_gates.hexa on the decoded output and the binding contrast from the in-engine partition posterior — verdict trace runs through live dispatch, never a torch side-harness.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from cls/schema cards and dentate_ca3 (this census) — nonparametric_cause_partition infers HOW MANY hidden causes + which obs share one (CRP structure-learning); the cause-partition-as-binder is the differentiator.

Design only. Cheap rung = toy CRP numpy probe; production rung needs the cause-decoder wired into generator L3 + a structure-learning objective in cli/train.hexa. Strongest on binding/recombination/novelty/honesty; Psi=1/2 here is plausible but the weaker axis (exploit<->explore balance) — pair with the allostatic regulator for a hard Psi attractor.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
