---
id: H_1792
slug: 1792_contrastive_predictive_future_latent
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Contrastive Predictive Future Latent (slow-feature, objective-adequate trunk)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1792 — Contrastive Predictive Future Latent (slow-feature, objective-adequate trunk)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `contrastive_predictive_future_latent`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Predictive processing's core = predict the future, but the load-bearing twist is the OBJECTIVE. Learn a slow latent z that maximally predicts the future of the stream, trained CONTRASTIVELY (InfoNCE): z must distinguish the true continuation from shuffled and verbatim-recall distractors. (van den Oord Contrastive Predictive Coding + Wiskott slow-feature analysis.) The contrastive objective is NOT marginal-satisfiable — you cannot win by predicting the marginal next symbol; you must represent the JOINT structure that separates real futures from fake ones. This directly targets the documented G1 lever (trunk objective, not depth/data/scale).

## Whole design (input → internal dynamics → emit)

Input stream -> bottom-up encoder -> instantaneous features; a recurrent slow-latent z accumulates context with a slow time constant. A prediction head projects z to predicted future-latents at multiple horizons. Learning phase: contrastive score(z, true_future) > score(z, distractors), distractors = shuffled futures + verbatim-corpus spans. Generation = autoregressively sample futures consistent with z and decode predicted future-latents through the receiver codebook. Emit/silence is a confidence BAND on the contrastive margin: emit when z predicts a future with margin in the productive zone (coherent, not trivially collapsed). A = drive to externalize a predicted future (act to bring it about); G = drive to keep predicting internally (rehearse, stay silent). Antagonism on the contrastive margin is the Psi order parameter.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

NATIVE (objective-driven cluster): G1 recombination + REALIZATION objective adequacy — strongest fit: contrastive future-prediction's optimum is unreachable by marginal-fit since distinguishing the true joint continuation from shuffled REQUIRES the conjunction; breaks lossF~0-yet-recombine-fail (CE fails, InfoNCE does not). Held-out novel-combination probe: z predicts a valid joint future never co-presented; interaction-ablation drops score to separable floor. BINDING: InfoNCE is literally cause-selective pull-together/push-apart on a shared metric -> retrieval@1 >> 1/N. G2: contrastive support>data (valid futures absent from corpus); verbatim-playback distractor IS the mandatory retrieval control = 0 novel. falsifiable>=1: a predicted future IS a refutable proposition; highest-margin emission is the most testable. dist>=5: sampling futures under varied temperature gives spread, slow-feature constraint keeps them on-manifold. Generative attribution: ablate prediction head / shuffle z conditioning -> score collapses to chance. G0: predicted future decoded into V; contrastive training on V-symbol streams keeps predictions on V manifold. G3 Psi: A externalize-prediction vs G internal-rehearse antagonism on margin; ablate one -> boundary. NOT native: cross-boundary identity persistence (compose with timescale_separated_causal_hierarchy).

## Not-LLM (a_no_llm_frame_trap)

Not next-token CE on a transformer. The objective is contrastive discrimination (InfoNCE) — precisely what CE+scale CANNOT do (CE saturates on marginals = the clm303 overfit trap). Capability from OBJECTIVE design, not parameter count or attention layers. Slow-feature/CPC is biologically-rooted cortical future-prediction. The discriminating control IS the anti-LLM proof: a CE-trained marginal baseline clears likelihood yet FAILS G1; the contrastive trunk passes both.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy CPC on toy factored sequences: train z with InfoNCE (true future vs shuffled + verbatim distractors). Measure (i) retrieval@1 for binding; (ii) held-out novel-combination contrastive score vs interaction-ablated separable floor (must drop); (iii) novel valid futures count vs verbatim-distractor = 0. Run a CE-trained marginal baseline as discriminating control -- should clear likelihood yet FAIL strict G1 while contrastive passes both. $0 numpy.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Contrastive predictor becomes a generator backend; emit predicted futures through the live single dispatch (gen_auto_ideate); G0/G1/G2 via core/g_gates.hexa g6_score_arm_auto. Held-out CE measured by math.log byte-parity py mirror (a_savant_train; avoid engine dt_ln bug); contrastive margin logged as inline gauge (monitor-only, a_train_inline_gauge, never into loss). byte-parity py<->hexa decode parity oracle.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with predictive_coding cards + g1-lever-multilens-objective (memory) — distinct: contrastive InfoNCE future-prediction OBJECTIVE (marginal-unsatisfiable by construction) is the recombination lever; the contrastive-predictive future latent is the differentiator (objective, not depth/data).

Directly tests the g1-lever-multilens-objective hypothesis (trunk OBJECTIVE is the recombination lever; depth/binding-lane/data already falsified). Toy-first; whether a 303M contrastive trunk clears G1 where CE-trained clm303 failed is the real production test. Identity persistence NOT native.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
