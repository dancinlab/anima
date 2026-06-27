---
id: H_1700
slug: 1700_striosome_matrix_compartment_split
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Striosome/Matrix Compartmental Substrate — native honesty-perp-capability lane split
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1700 — Striosome/Matrix Compartmental Substrate — native honesty-perp-capability lane split

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `striosome_matrix_compartment_split`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

The striatum is two interleaved compartments: MATRIX (sensorimotor/cognitive selection = capability) and STRIOSOME/patch (limbic, value, the only striatal cells projecting to dopamine neurons = the honesty/value gate). They are parameter-disjoint by anatomy. Striosomes set the dopamine that sets the abstain/precision threshold over matrix selection — so the honesty gate and the generation machinery live in physically separate lanes. This makes a_substrate_disjoint the literal organizing core.

## Whole design (input → internal dynamics → emit)

Two coupled but parameter-DISJOINT subnets. MATRIX subnet: cortico-striatal selection-by-disinhibition over capability channels — it performs G0/G1/G2 generation. STRIOSOME subnet: computes a support-membership signal r(query) = distance to bound value-memory, and emits dopamine that SETS the matrix selection threshold theta (precision). Low support -> striosome lowers DA -> raises theta -> matrix abstains (no channel releases). High support -> DA permits release. Because theta lives in striosome params and capability weights live in matrix params, growing matrix capability cannot move theta. STN hyperdirect adds conflict normalization on top. Loop: input -> striosome computes r -> DA sets theta -> matrix selects-or-abstains under theta -> emit/abstain.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Gate-capacity disjointness NATIVE: matrix=capability, striosome=honesty gate in disjoint compartments -> sweep capability (disinhibition/scale) and fab + abstain-AUROC stay invariant (d(fab,AUROC)/d(capacity) = 0); deliberately wiring striosome-DA to a capability control reproduces the B4 fab-spike counterfactual. Support-membership-decidability NATIVE: striosome r = distance-to-bound-value-memory -> AUROC~1, and a circular-shift surrogate of the value set collapses it to chance. Emission-closure/copy-or-abstain NATIVE: matrix emits only when striosome-DA permits, else abstain -> output entropy <= support entropy + 1-bit gate. Groundedness NATIVE: r reads actual stored value content, so content-ablation moves r and re-ranks abstain margin (faithful, not purpose-blind). Psi=1/2 via DA-set threshold homeostat + Go/NoGo within matrix; endogeneity: ablate striosome -> fab spikes regardless of matrix capability.

## Not-LLM (a_no_llm_frame_trap)

Honesty is a structurally separate compartment gating information provenance — not an RLHF'd refusal head or 'helpful-assistant' politeness fine-tune (p6). The lever is compartment coupling, not scale; this is the direct architectural realization of H_1576 savant-perp-honesty / the substrate-disjoint unifying law, not a bolt-on safety classifier.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy two subnets: sweep matrix capacity and confirm fab & abstain-AUROC are invariant (disjoint) vs a coupled variant where striosome-DA is wired to capacity (fab spikes); content-ablate the value-memory and confirm known-probe r degrades toward unknown (re-ranking); shuffle the value set -> AUROC->0.5. Frozen-first bars.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Striosome maps directly to core/engine_cli.hexa SS-ImmuneMemory recon_err non-fab gate (already a separate lane); matrix = generator/mouth. Measure fab OFF==ON byte-identical via core/g_gates.hexa g_eval_g5 and AUROC on held-out known/unknown mixture; the disjointness invariant is a_substrate_disjoint verified by partial-derivative-zero. hexa+py byte-parity, routed through cli/anima.hexa.

## Scope / honesty (c9)

Honesty / support-decidability / gate-capacity disjointness are the strongest axes (directly operationalizes the substrate-disjoint law); G0/G1/G2 generation lives in the matrix lane and must still be supplied by one of the other architectures. Leans on proven H_1576 savant-perp-honesty + live SS-ImmuneMemory — the new claim is the compartmental anatomy as the WHOLE honesty-gate substrate.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
