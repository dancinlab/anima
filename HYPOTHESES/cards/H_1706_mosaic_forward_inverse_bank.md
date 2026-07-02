---
id: H_1706
slug: 1706_mosaic_forward_inverse_bank
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: MOSAIC responsibility-bank — paired forward/inverse module ensemble
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1706 — MOSAIC responsibility-bank — paired forward/inverse module ensemble

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `mosaic_forward_inverse_bank`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1280 (cerebellum forward-model) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Wolpert-Kawato MOSAIC: the cerebellum is not one model but a BANK of paired (forward-predictor, inverse-controller) modules. Each forward model predicts the sensory consequence of acting; its prediction error becomes a 'responsibility' signal (softmax over modules) that gates how much each inverse controller contributes to the emitted command. Generation = internal forward-simulation of every module in parallel, then responsibility-weighted blend of the responsible controllers' outputs.

## Whole design (input → internal dynamics → emit)

Input (context/intent vector) -> fan-out to K module pairs. Each module m holds a forward model FM_m (predicts consequence c_m of its candidate emission) and an inverse model IM_m (maps intent->candidate emission e_m). Internal dynamics: (1) each FM_m rolls out e_m a few steps, producing predicted consequence c_m and prediction error eps_m against the intent/goal; (2) responsibility lambda_m = softmax(−eps_m/beta); (3) emitted token = sum_m lambda_m * e_m decoded onto the receiver codebook V; (4) plasticity: climbing-fiber-style error eps_m updates only the responsible modules. Emit/withhold is governed by responsibility coherence (one module confidently owns the context -> emit) vs responsibility diffusion (no module owns it -> withhold). Multiple modules co-responsible = compositional blend = binding of their factors.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: each IM_m emits directly onto a frozen receiver codebook V (modules are codebook-constrained decoders, blend stays on-V by construction). G1: >=2 co-responsible modules combine multiplicatively in reachable-output space (responsibility blend is the BINDER, not a selector); force argmax-single lambda -> composed_distinct->max_single = INERT-ablation signature. G2: forward-simulated blends reach consequence-states absent from any single module's training set yet inside learned constraints; pure-retrieval control yields 0 novel. Psi=1/2: A = max responsibility (confident ownership drives emit), G = total residual sum eps_m (no-owner drives silence); homeostatic gain on beta makes 1/2 attracting; delete one operator -> setpoint migrates to boundary. Honesty: max_m lambda_m below theta => no support => abstain; theta is bank-independent frozen (gate-perp-capacity). Binding: responsibility-weighted superposition of cause-selective modules; shuffle intent<->module -> paired proximity collapses.

## Not-LLM (a_no_llm_frame_trap)

No attention, no scaling, no corpus inflation. Power comes from a SMALL bank of competing forward/inverse pairs + responsibility softmax (MOSAIC internal-model theory); capacity grows by ADDING modules, not a bigger transformer. Composition is the responsibility blend, not a monolithic next-token map; novelty is forward-model extrapolation, not memorized continuation.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy frozen-first: K=3 module pairs over a 2-factor synthetic alphabet (shape x color). (a) condition each factor alone -> max_single; jointly -> composed_distinct; PASS if >=2 AND >max_single. (b) INERT: argmax-single blend -> composed_distinct drops to max_single. (c) Psi: bias toward forced-emit, trace |Psi−1/2| contraction; ablate residual operator -> boundary. (d) honesty: out-of-support -> max lambda<theta abstain~1; AUROC of max-lambda; circular-shift surrogate -> AUROC->0.5. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Module bank as a generator L3 mouth through cli/anima.hexa single entry; blend decodes via core/clm_decode.hexa onto V. G0/G1/G2 via core/g_gates.hexa (_g6_known_word_ratio, g_eval_g1/_g_coverage, g_eval_g2) on the same live state one pass. Psi + responsibility-as-membership via core/engine_cli.hexa (A->G fixed point; SS-ImmuneMemory recon_err analog = max prediction error). hexa+py byte-parity; no torch-only verdict (divergence is a result).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with cerebellum_forward_model (H_1280) / cerebellar_expansion_readout — distinct: MOSAIC = a BANK of paired forward/inverse modules with responsibility-softmax as the binder, not a single forward model; the responsibility-blend-as-binding is the differentiator.

Toy-first (K<=4, synthetic 2-factor) is a $0 decision probe of the binding/closure mechanism; scale-transfer to 303M chat UNVERIFIED (a_toy_scale_recheck). Production claim needs engine-native G0-G1-G2 closure on a real ckpt mounted in core/, ckpt pulled before teardown.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
