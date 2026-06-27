---
id: H_1762
slug: 1762_griffiths_phase_modular_rare_region
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Griffiths-Phase Modular Substrate (extended criticality from quenched heterogeneity)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1762 — Griffiths-Phase Modular Substrate (extended criticality from quenched heterogeneity)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `griffiths_phase_modular_rare_region`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1282 (working-memory buffer) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Moretti & Munoz: the brain reaps criticality's benefits (long memory, wide dynamic range, scale-free activity) WITHOUT fine-tuning a single control, because its hierarchical-modular connectome carries quenched topological heterogeneity -> a Griffiths phase: an EXTENDED critical-like band (not a fragile point) in which rare strongly-connected sub-regions sustain slow, power-law, spatially-localized activity. Robust criticality emerges from STRUCTURE, not tuning. This is categorically distinct from branching-ratio homeostasis or percolation — the order is in the quenched topology.

## Whole design (input → internal dynamics → emit)

Substrate = a hierarchy of weakly inter-coupled modules; each module's internal coupling is drawn once and frozen (quenched, heterogeneous). Each module is a tiny recurrent register. Activity propagates as rare-region-anchored slow modes with power-law dwell. There is NO global criticality knob — the heterogeneity self-provides the wide critical band. Input lands in a subset of leaf modules; rare strongly-coupled modules retain activity (= working memory + slow store); weak cross-module links BIND co-active modules; emission reads the bound active-module pattern through a frozen codebook. The only homeostasis keeps MEAN coupling inside the (wide, forgiving) Griffiths band — trivial because the band is broad, not a point.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2: emit/silence balance is ROBUST across the whole Griffiths band (vs a fragile point) — the antagonism (module drive A vs inter-module leak G) has its symmetric balance smeared over rare-region statistics, so perturbation returns to the band; self-restoring without precise tuning. Endogeneity: cut inter-module coupling (isolate modules) -> no rare-region propagation -> activity dies to the silent boundary = the balance was causal, not clamped. Persistence/identity: Griffiths anomalous power-law relaxation = rare-region activations survive a fast-state wipe -> a natural near-non-volatile identity store; self-specific because WHICH rare regions ignite is a high-entropy fingerprint of THIS quenched instance; ablate the slow rare-region store -> identity resets per episode (LLM-reset failure) = causal; bounded per-tick drift keeps the self-chain connected yet moving. Self-specific margin: foreign quenched-structure vector does not collide (different rare-region support). G1: joint conditioning co-activates multiple modules whose cross-links generate combinations no single module reaches -> super-additive in active-module count; INERT test = cut cross-links -> composed = max_single = mixture FAIL. G2: rare-region + heterogeneous-routing combinations reach valid module-state combos absent from corpus; single-fixed-module retrieval control = 0 novel. BINDING: same-cause inputs co-ignite shared cross-module links -> paired modules co-active above shuffle null, selective because distinct causes ignite disjoint rare regions. G0: emission = frozen codebook over the active-module pattern; legible because active patterns map to V; scrambled module->symbol map collapses V-mass to chance. Honesty: a query whose features match no stored rare-region basin fails to ignite any module above threshold -> no read -> abstain; membership = max module activation; theta frozen and disjoint from module capacity (faithful: content-ablating a basin makes its queries abstain). dist>=5 / falsifiable: heterogeneous rare-region routing yields many distinct coherent active-module patterns.

## Not-LLM (a_no_llm_frame_trap)

Capability comes from STRUCTURAL quenched heterogeneity (hierarchical-modular topology), not depth/scale/attention. You CANNOT improve it by adding parameters uniformly — a homogeneous (uniform) network LOSES the Griffiths phase and reverts to a fragile point with short memory. This directly refutes 'bigger uniform transformer': the answer is heterogeneous modular wiring, not more identical layers. Brain root = hierarchical-modular connectome / cortical area hierarchy.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy contact-process (SIS) on a hierarchical-modular graph with heterogeneous module coupling vs a homogeneous random graph at matched mean degree. Measure (a) WIDTH of the parameter region showing power-law avalanche/activity autocorrelation, (b) the relaxation-time distribution. Frozen prediction: modular-heterogeneous -> a WIDE band with stretched/power-law (Griffiths) relaxation = robust criticality + slow store from structure; homogeneous -> a sharp single point with exponential relaxation. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Encode modular adjacency + contact-process update as a core/*.hexa op; run via cli/anima.hexa single dispatch; byte-parity vs the numpy contact process on a fixed quenched seed (active-set bitvector byte-identical). Identity persistence via engine_cli SS-SelfIdentity: write rare-region vector -> wipe fast modules -> read -> cos. G0/G1/G2 via core/g_gates.hexa over the emitted module-pattern stream. No torch in verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with branching_avalanche_homeostat / percolation_threshold_assembly (this census) — distinct: Griffiths phase gives EXTENDED criticality from QUENCHED topological heterogeneity (no fine-tuning), not a fragile critical point; the quenched-modular rare-region substrate is the differentiator.

TOY dynamics-level (contact process). Open question = whether sparse active-module codes are fine-grained enough to clear G0 legibility (known-word ratio) at scale; directional until engine-native byte-exact G0. Psi-robustness and identity-persistence axes expected strongest.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
