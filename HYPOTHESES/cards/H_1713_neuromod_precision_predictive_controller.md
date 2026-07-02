---
id: H_1713
slug: 1713_neuromod_precision_predictive_controller
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Neuromodulatory precision controller (expected/unexpected uncertainty)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1713 — Neuromodulatory precision controller (expected/unexpected uncertainty)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `neuromod_precision_predictive_controller`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

ACh estimates EXPECTED uncertainty and NE UNEXPECTED uncertainty (Yu & Dayan 2005); together they set relative PRECISION (gain) on top-down prior vs bottom-up likelihood in a predictive-coding loop. The whole architecture is a hierarchical self-predictor whose belief-updating is reconfigured by neuromod-estimated uncertainties -- high uncertainty -> trust data/explore, low -> trust model/exploit.

## Whole design (input → internal dynamics → emit)

A generative model predicts its own next input; prediction error drives belief update with precision (effective learning-rate/gain) set by m. ACh down-weights reliable-but-noisy channels (expected noise); NE detects context CHANGE and triggers a network RESET -- flush priors, raise likelihood gain; DA sets precision on value/action-relevant dims; 5HT sets temporal discount + the evidence-accumulation bound (patience before commitment). Emit = a committed prediction decoded through frozen codebook V when precision-weighted accumulated evidence crosses the 5HT-bound; else the loop keeps predicting silently. Learning IS error-minimization on the generative model -- one continuous loop.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2: NE/DA raise drift toward commit (emit), 5HT raises bound + discounts (withhold); balance of drift-vs-bound sets commit-rate, homeostat -> 1/2; remove bound (5HT) -> commits instantly always, remove drift (NE/DA) -> never commits = endogeneity. Honesty (native groundedness): r = precision-weighted prediction ERROR against the actual generative model -- out-of-support -> persistent high error -> low model-precision -> won't commit low-precision belief -> abstain; r reads real model reconstruction, not a proxy (passes H_988/989 purpose-blind test); theta (commit-precision floor) in 5HT, capacity (model richness) elsewhere -> disjoint. G1/binding via EXPLAINING-AWAY: predictive coding's inference of a joint cause from multiple streams is inherently a non-separable conjunction; ablate cross-stream generative coupling -> explaining-away gone -> composed=union (INERT). G2/novelty: NE-reset/explore lowers prior precision -> samples off-prior on-likelihood-manifold = valid-novel; max-prior-precision control = 0 novel. Objective-adequacy (REALIZATION INVARIANT): minimizing prediction error on a generative model whose optimum requires the joint cause is a binding-REQUIRING objective, unlike marginal-satisfiable CE.

## Not-LLM (a_no_llm_frame_trap)

Precision-weighted Bayesian inference controlled by neuromod scalars, not next-token CE on a wide transformer. The lever is uncertainty-estimation + an objective whose optimum is unreachable by fitting marginals -- directly attacking the G1-wall finding that CE rewards parts, not synthesis. Rooted in Yu-Dayan + Friston predictive coding.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy 2-level predictive-coding model with ACh/NE precision scalars: (a) NE-reset on context switch raises valid-novel count while max-prior control yields 0; (b) out-of-support probe -> high error -> abstain (AUROC~1), shuffle-support surrogate -> AUROC->0.5; (c) evidence-bound homeostat pins commit-rate->1/2; (d) cross-stream coupling ablation collapses explaining-away (composed->union). $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

A<->G as drift(NE/DA)<->bound(5HT); generative model = .clm mouth via core/clm_decode (prediction = next-byte dist), precision-weighted CE as r; measure via cli/anima.hexa eval (G0/G1/G2) + held-out mirror-DESCENT (math.log per a_savant_train/a_clm_gen_pipeline -- NOT engine dt_ln which clamps CE) as faithful precision oracle; honesty via ImmuneMemory.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with predictive_coding cards + neuromodulation_gain (H_1284) — distinct: ACh/NE estimate expected/unexpected UNCERTAINTY to set precision in a predictive-coding loop (Yu-Dayan), with explaining-away as the binder; the uncertainty-precision-controller is the differentiator.

Predictive-controller toy; binding-via-explaining-away at real corpus scale is the unverified rung and is exactly the H_1310/G1 frontier -- must show the generative objective is genuinely binding-requiring (interaction-ablation drops held-out novel-combo score to the marginal floor), else falls to the same wall.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
