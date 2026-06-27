---
id: H_1792
slug: 1792_contrastive_predictive_future_latent
tier: 🔵 PRE-REGISTERED ARCHITECTURE · cheap_test measured (DIRECTIONAL toy)
title: Contrastive Predictive Future Latent (slow-feature, objective-adequate trunk)
verdict: 🔵 PRE-REGISTERED · cheap_test measured (DIRECTIONAL toy) = NOT (under-powered caveat) — InfoNCE shows zero held-out composition advantage over CE-marginal (Δ=-0.022, all bars FAIL), but binding-required toy cannot grok for ANY objective (modular-addition control at chance) → recombination axis UNDER-POWERED (a_break_the_wall type-a). No cheap InfoNCE win; deferred to cost-gated 303M engine-native (H_1602, NOT fired).
source: brainarch_census
---

# H_1792 — Contrastive Predictive Future Latent (slow-feature, objective-adequate trunk)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE · cheap_test measured (DIRECTIONAL toy — NOT terminal)
- **wired:** DIRECTIONAL-mirror — $0 numpy cheap_test MEASURED (see §Probe result), verdict NOT (under-powered). NOT engine-native; engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
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

## Probe result (cheap_test · $0 numpy · DIRECTIONAL toy · NOT terminal)

- **verdict:** **NOT (DIRECTIONAL) — with explicit under-powered caveat.** Per frozen bars BAR-2 FAILS (InfoNCE held-out 0.000, no advantage over CE-marginal, Δ=-0.022) → NOT.
- **frozen_bar** (pre-registered in probe BEFORE running, verbatim, no tune-to-green; chance=1/42=0.0238): BAR-1 binding/retrieval@1 M3(InfoNCE) held-out compositional acc ≥0.50. BAR-2 objective=G1 lever: (M3_held − M1_CE-marginal_held) ≥0.20 AND M3_held ≥0.50. BAR-3 interaction-ablation: (M3_held − M4_additive-floor_held) ≥0.30. BAR-4 verbatim control: M3 prefers true compositional future over verbatim-recall distractor on ≥0.80 held-out. DISCRIM-CTRL: M1 train≥0.95 AND M1 held<0.50. SUPPORT = BAR-1&2&3&4 all pass; NOT = BAR-2 fails; MIXED otherwise. Mean/5 seeds, bars on BEST held-out over run (generous, anti false-negative).
- **numbers:** Means/5 seeds (best held-out over 40k AdamW steps): M1 CE-marginal train=0.800 held=0.022 | M2 CE-joint held=0.000 | M3 InfoNCE held=0.000 verbatim_win=0.000 | M4 additive-floor held=0.067. BARS: BAR-1 M3_held=0.000 FAIL · BAR-2 Δ(M3−M1)=-0.022 FAIL · BAR-3 Δ(M3−M4)=-0.067 FAIL · BAR-4 vb_win=0.000 FAIL · DISCRIM-CTRL tr=0.80/he=0.02 FAIL. GROKKABILITY CONTROL (single-head modular ADDITION, canonical grokkable task, AdamW 40k, 50% held): best held-out=0.050 ≈ chance(1/11=0.091) ⇒ toy CANNOT grok for ANY objective. Diagnostics: SGD+momentum 30k AND AdamW wd∈{0.01,0.05,0.1} all train→1.0 held→0.0 (one-hot MLP lacks shared-embedding bias).
- **honest scope:** the grokkability control shows the $0 numpy toy cannot induce held-out compositional generalization for ANY objective (incl. the grokkable modular-addition control at chance), so the recombination axis is UNDER-POWERED (a_break_the_wall type-a: measurement limit, NOT science ceiling). Within the test's power, InfoNCE gives NO cheap recombination win over CE — symmetric failure. Neither cheaply supported nor strongly falsified.
- **probe_path:** `state/brainarch_census/probes/H_1792.py`
- **NOT terminal:** DIRECTIONAL numpy toy only (a_engine_native_learning); the real test is the cost-gated 303M engine-native run (H_1602 / engine_native_measure, NOT fired).

## Distinction (near-overlap kept, not a dup)

Near-overlap with predictive_coding cards + g1-lever-multilens-objective (memory) — distinct: contrastive InfoNCE future-prediction OBJECTIVE (marginal-unsatisfiable by construction) is the recombination lever; the contrastive-predictive future latent is the differentiator (objective, not depth/data).

Directly tests the g1-lever-multilens-objective hypothesis (trunk OBJECTIVE is the recombination lever; depth/binding-lane/data already falsified). Toy-first; whether a 303M contrastive trunk clears G1 where CE-trained clm303 failed is the real production test. Identity persistence NOT native.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
