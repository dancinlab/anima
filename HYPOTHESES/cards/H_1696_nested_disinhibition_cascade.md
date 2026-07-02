---
id: H_1696
slug: 1696_nested_disinhibition_cascade
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Nested Disinhibition Cascade (NDC) — computation by chained sign-inversion gating
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1696 — Nested Disinhibition Cascade (NDC) — computation by chained sign-inversion gating

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `nested_disinhibition_cascade`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The literal BG signature is multi-stage inhibition: cortex->striatum -| GPi -| thalamus (direct = 2-link disinhibition) and striatum -| GPe -| GPi -| thalamus (indirect = 3-link re-inhibition). Computation is the PARITY of an inhibition chain; 'release' = an even number of active brakes removing a default-on tonic clamp. Default-OFF is the organizing axiom — the opposite of LLM default-emit.

## Whole design (input → internal dynamics → emit)

The substrate is a stack of tonically-ACTIVE inhibitory fields, each suppressing the next. Output channels are clamped OFF by default. Input perturbs the bottom striatal field; an active striatal unit silences its GPi target, which un-silences (disinhibits) the corresponding thalamic channel -> that one symbol releases. An emit requires a clean even-parity disinhibition path from input to a channel; no matched path => the channel stays clamped (abstain). Direct (2-link) paths push global disinhibition Psi up; indirect (3-link) paths re-inhibit, pushing Psi down. STN hyperdirect = a global re-inhibition pulse that broadly raises the clamp when many channels start lifting (contraction). Emit = parity-clean release; the whole input->dynamics->emit loop is sign-arithmetic over brakes, never additive activation.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0/legibility: each thalamic channel is exactly one receiver-fixed codebook symbol; clean disinhibition lifts one legal symbol, byte-garble = no clean parity so nothing legal lifts (random source -> 0 V-mass). Honesty (support-membership + copy-or-abstain + endogeneity): default-on inhibition IS abstain; content can only escape via a supported disinhibition path, so fabrication is structurally impossible without a path — r = path disinhibition strength, theta = tonic clamp; ablating the indirect re-inhibition collapses the gate (INERT test passes). Psi=1/2: direct(2-link) up vs indirect(3-link) down opponent parity gives a symmetric fixed point; STN global re-inhibition supplies the contraction toward 1/2. G1/binding is the weak axis (handled only via co-lifted channels).

## Not-LLM (a_no_llm_frame_trap)

No softmax/attention over tokens and no scale lever — computation is the sign-parity of an inhibition chain, and the substrate is default-OFF (must EARN emission) rather than default-emit. Adding layers != help; only chain parity/coupling matters. This is a_no_llm_frame_trap-compliant: missing capability is added as a brake-chain stage, not a bigger transformer.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: N channels each with a direct(2-link) and indirect(3-link) gain; perturb a supported subset and measure released-channel fraction vs an unsupported/random input (must collapse to ~0 V-membership); then ablate the indirect stage and confirm Psi runs to all-ON (gate INERT). Frozen-first bar: supported-release ratio >=0.5 AND unsupported ~0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Released-symbol legibility via core/g_gates.hexa _g6_known_word_ratio on the disinhibition-field output; abstain via core/engine_cli.hexa SS-ImmuneMemory recon_err threshold reinterpreted as the tonic clamp theta; Psi self-restoration via SS-ThirdLaw safety_phi_ratchet. Author the disinhibition-field op as a hexa+py byte-parity pair (a_engine_native_learning), no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281 lens) and tonic_disinhibition_release_gate (this census) — distinct: NDC's organizing principle is inhibition-chain PARITY (even/odd brakes), not value-gating nor a single SNr clamp; default-OFF parity is the differentiator.

TOY-first; selection + abstain + Psi are native, recombination/compositional-depth is the open risk to be measured, not assumed.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
