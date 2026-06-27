---
id: H_1744
slug: 1744_mixed_discrete_continuous_generative
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Mixed Discrete-Continuous Generative Substrate (categorical-top, continuous-bottom active inference with drift-diffusion emit)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1744 — Mixed Discrete-Continuous Generative Substrate (categorical-top, continuous-bottom active inference with drift-diffusion emit)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `mixed_discrete_continuous_generative`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Friston's hybrid (mixed) generative models — a discrete categorical/HMM layer governs a continuous predictive-coding layer. Discreteness at the top supplies symbolic structure (the shared code); continuity at the bottom supplies graded sensory prediction. The emit/withhold decision is Bogacz-optimal sequential evidence accumulation (drift-diffusion / SPRT to a bound) — the brain's evidence-to-bound dynamics, not a thresholded logit.

## Whole design (input → internal dynamics → emit)

Two coupled regimes. Discrete top: a learned categorical generative model whose states ARE symbols/morphemes over V, with a learned transition tensor = grammar/constraint manifold, plus an explicit NULL/abstain state with its own likelihood. Continuous bottom: predictive coding that, conditioned on the active discrete state, predicts continuous sensory features and sends precision-weighted prediction errors upward. (1) Input clamps the continuous bottom; errors drive Bayesian model-selection at the discrete top. (2) A drift-diffusion accumulator integrates the log-likelihood ratio (evidence-for-winning-symbol minus prior-to-withhold); drift = net evidence, the two bounds = emit-symbol vs reset-to-silence. (3) Emit when the accumulator crosses the emit bound: externalize the MAP discrete symbol, then the transition tensor conditions the next state (sequential generation = traversing the discrete model). (4) Silence while the accumulator is below bound. (5) Psi = normalized accumulator position between the two symmetric bounds; unbiased start = 1/2, opponent drift terms (evidence-for-emit vs cost/prior-to-withhold) balance there. (6) The discrete state-prior vector (initial distribution + a 'self' latent conditioning the transition tensor) persists across episodes; fast accumulator state is wiped.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: discrete states = V (receiver-fixed codebook) so output is on-code by construction; legibility = posterior concentrated on a V-state. G1: the discrete state factors into independently-conditionable slots (e.g. tense x person x root); cross-slot terms in the transition/emission tensor bind them so reachable joint strings > max single-slot; zeroing the cross-slot coupling (diagonal-only) collapses composed_distinct to max_single. G2: the learned transition tensor generates grammatical symbol sequences absent from the corpus (extrapolation within grammar) — supp(model) strictly contains data; clamp-to-data verbatim playback = 0 novel. dist>=5: temperature on the categorical samples distinct sequences whose coherence is guaranteed by transition constraints. falsifiable>=1: a discrete structure binding comparator-state x quantity-state x >=2 content-states emits a refutable proposition. Psi=1/2: drift-diffusion with symmetric unbiased start + opponent drift is literally Bogacz's optimal balanced accumulator — contractive return to 1/2 under perturbation; remove one drift term -> bound-collapse (endogeneity). Honesty: the NULL-state likelihood is the abstain branch — out-of-support input gives NULL highest likelihood -> no symbol emitted; copy-or-abstain is structural (a symbol requires a supported discrete state to win). Gate-capacity disjoint: the NULL threshold is frozen in the discrete layer while expressivity lives in the transition tensor (d-fab/d-capacity = 0). Binding (H_961): the discrete state is the shared latent binding continuous modalities. Realization invariant: the discrete model sits ON the emit path, and a next-discrete-state objective is minimizable only by representing the transition interaction terms (marginal-fit cannot reach the optimum) — objective adequacy is native.

## Not-LLM (a_no_llm_frame_trap)

Symbolic structure is an EXPLICIT discrete generative model (HMM/PCFG-class), not structure-implicit-in-weights from scale. Composition is the transition tensor's interaction terms; novelty is grammar-extrapolation, not interpolation in a large net. You improve it by enriching the discrete state factorization (adding a slot = structure), not by adding layers/params/corpus. The emit decision is a dynamical drift-to-bound, not a softmax over a vocabulary — a closed-loop accumulator, not a feedforward classifier.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

mini-numpy: factored HMM (2 slots x 3 values) over a 6-symbol V + a NULL state, with a drift-diffusion emit accumulator. (a) G1: distinct valid emissions with cross-slot transition coupling ON vs diagonal-only — must collapse to max_single. (b) honesty: feed out-of-support obs -> NULL must win (fab=0) vs force NULL-likelihood->0 (gate-off) -> fab must jump (causal gate). (c) Psi: perturb accumulator start -> must return to 1/2; delete one drift term -> runs to a bound. $0, decisive on G1-binding, honesty-causality, and Psi-endogeneity.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the discrete top as a core/*.hexa categorical generative op feeding generator L3; reuse core/clm_decode.hexa / bytegpt_decode.hexa as the continuous sensory predictor. Score G0/G1/G2 via core/g_gates.hexa g_eval_all through cli/anima.hexa single entry (gen_auto_ideate). Psi via SS-ThirdLaw; honesty via SS-ImmuneMemory with the NULL-state likelihood as the recon_err/recall_thr analog (parity check). byte-parity py mirror computes the HMM forward/transition math (no torch in the verdict path).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with variational_factor_graph_substrate / mixed-model cards — distinct: this is a MIXED discrete-categorical-top + continuous-PC-bottom with a Bogacz drift-diffusion emit; the discrete-grammar-over-continuous-PC + drift-to-bound is the differentiator.

Discrete-state count and slot factorization are toy-scale first; the drift-diffusion emit is parameter-light and robust. NULL-abstain calibration transfer to a 303M corpus UNVERIFIED. The G1 lever (cross-slot interaction in the transition tensor) is the structural claim to measure — a diagonal tensor would fail, matching the clm303 lossF~0-yet-recombine-fail pattern (objective adequacy is the real test).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
