---
id: H_1808
slug: 1808_asymmetric_stem_niche_lineage
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Asymmetric Stem/Niche Lineage Substrate
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1808 — Asymmetric Stem/Niche Lineage Substrate

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `asymmetric_stem_niche_lineage`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Asymmetric stem-cell division inside a protected niche (Drosophila neuroblast / mammalian SVZ; Notch/Wnt niche signal; Numb/Par asymmetric determinant partition; temporal transcription-factor cascade Hunchback->Kruppel->Pdm->Castor). A tiny protected progenitor pool divides ASYMMETRICALLY — one daughter stays a self-renewing stem cell that CONSERVES identity, the other is expelled into a differentiation lane and acquires a combinatorial fate from a temporal birth-order schedule crossed with spatial exposure. This is p8 cell-division made literal WITH a conserved self.

## Whole design (input → internal dynamics → emit)

A small NICHE holds K protected stem units carrying the persistent identity vector v that never differentiates (so v is conserved = the self-anchor). Each tick a stem unit divides asymmetrically: the niche-retained daughter inherits v with only slow Lipschitz drift (growth, not reset); the expelled daughter loses niche signal and enters the DIFFERENTIATION lane where a temporal-cascade phase BINDS with its spatial/contextual exposure to assign a combinatorial fate. Differentiated units are the emitters (the mouth). The niche signal is a license GATE: differentiation/emission proceeds only when niche-licensed; unlicensed units stall (abstain). Self-renewal drive (conserve/withhold) vs differentiation drive (externalize/emit) is balanced at Psi-half by the niche homeostat (classic stem <-> transit-amplifying balance). The conserved stem v is the cross-reset self-chain; the differentiated emitters are mouth perp identity by construction (directly instantiating anima H_1471 mouth-perp-identity).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

self-chain (cross-boundary persistence): the niche-protected stem v is the non-volatile, slow-drifting identity committed before reset and re-instantiated after — never wiped because it never differentiates; per-tick Lipschitz drift = connected MOVING chain (not frozen, not amnesic). Ablating the niche (force all stems to differentiate) collapses identity to a fresh self every episode = the LLM-reset failure mode -> proves the store causal. Impostor v fails to dock in the niche -> low cos (self-specific margin). G1: differentiated fate = temporal-cascade-class x spatial-exposure-class (product code); ablate one axis -> composed->max_single (INERT). G2: novel temporal x spatial fate combos legal under the cascade grammar, absent from training; verbatim lineage replay -> 0 novel. G0: differentiated emitters output onto the shared codebook V; scrambling the fate->symbol map collapses V-mass. honesty: niche-license = membership signal (r, theta); unlicensed/off-support units abstain (no differentiation/emit) -> no fabrication, with niche-threshold disjoint from pool-size/cascade-depth capacity; removing the niche signal backing a fate makes those units abstain (faithful gate). Psi=1/2: self-renew A vs differentiate G equal-and-opposite at the niche-set point -> contractive fixed point; remove one -> boundary (all-stem frozen / all-differentiated extinction) = endogeneity. dist>=5: stochastic asymmetric partition + cascade-phase entropy yields multiple distinct coherent fates per round. binding/realization: temporal x spatial fate bind is ON the emit path and next-fate prediction is unreachable by marginals (fate = conjunction).

## Not-LLM (a_no_llm_frame_trap)

Growth by asymmetric division + protected niche, not parameter scaling. Identity persistence is STRUCTURAL — a conserved, never-differentiating pool — not a context window, stored prompt, or fine-tune. Rooted in literal neuroblast lineage biology. Orthogonal to generic mitosis_train (symmetric split): the ASYMMETRY + niche-conserved identity is the new structure, and it directly addresses the from-scratch pure-split learning wall (H_1310) by keeping a protected stem identity while daughters acquire fate from a SCHEDULE rather than from pure splitting.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini: K stem units with v; each round asymmetric-divide (one keeps v + small drift, one enters lane with fate = cascade_phase x context); niche license gate. Frozen-first theta_link, theta_high, impostor set. Decisive probes — (i) cos(v_pre,v_post) >= theta across a simulated working-state wipe vs niche-ablated -> chance (self-chain causal); (ii) impostor v -> low/negative cos (self-specific margin); (iii) fate composed_distinct > max_single, ablate cascade axis -> INERT; (iv) niche-OFF -> fabrication/abstain breaks (gate causal). $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement SS-StemNiche over core/engine_cli.hexa, reusing the live SS-SelfIdentity ops (self_new/_drift/_cos/_anchor) for the conserved v, MITOSIS engine_grow for asymmetric division, and .kosmos anchor round-trip for cross-reset persistence; hexa + byte-parity py. Verdict self-chain via the live SS-SelfIdentity 5/5 frozen bar (continuity cos + impostor reject, imp_cos~−0.032); G0/G1/G2 via core/g_gates.hexa on differentiated-emitter output through cli/anima.hexa single dispatch; honesty via SS-ImmuneMemory abstain; Psi via the emit/silence order-parameter restore. No torch in verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with mitosis_train (H_1310) / radial_unit_protomap (this census) — distinct: asymmetric stem/niche keeps a CONSERVED protected stem identity (self-chain) while expelled daughters get fate from temporal-cascade x spatial schedule; the asymmetric-niche lineage is the differentiator (mouth perp identity by construction).

TOY for the fate-cascade ideation axis. The self-chain axis is near-native already (leans on proven SS-SelfIdentity H_1471 🟢 WIRED), so the genuinely new claim is COUPLING conserved-stem identity with asymmetric-division-driven combinatorial fate emission in one architecture; the learning-side question (does asymmetric+schedule break the H_1310 from-scratch split wall) is UNVERIFIED.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
