---
id: H_1714
slug: 1714_neuromod_tonic_phasic_gain_bus
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Tonic/phasic dual-timescale gain bus (adaptive-gain regime)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1714 — Tonic/phasic dual-timescale gain bus (adaptive-gain regime)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `neuromod_tonic_phasic_gain_bus`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Aston-Jones/Cohen adaptive-gain theory: one broadcast 'gain bus' runs in two modes -- TONIC (baseline, broad/exploratory, high-entropy) vs PHASIC (event-locked, sharp/exploitative, low-entropy). The architecture's selectivity is set by where on the tonic<->phasic continuum the bus sits; breadth (dist) and legibility (G0) come from the two ENDS of ONE knob operated at two TIMESCALES rather than traded within one distribution.

## Whole design (input → internal dynamics → emit)

A pool of feature cells feeds a shared output decoder. A global gain bus g(t) multiplies all cell activations before a competition. NE sets tonic baseline of g (slow) AND emits phasic pulses (fast) locked to detected task-relevant events; DA biases which dims get the phasic boost (value-gating); ACh sets the SNR floor (suppresses cells below a familiarity threshold); 5HT sets the tonic floor (patience/withhold). Cycle: low-tonic + no-phasic -> broad sampling of many distinct on-manifold candidates (dist); then a phasic pulse selects and sharpens one winner -> legible emit (G0) through frozen codebook V.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

dist>=5 AND G0 CO-LOCATED: tonic mode yields >=K pairwise-distinct coherent candidates (breadth without garble because ACh-SNR floor keeps each on-manifold), phasic mode sharpens to one legible emit -- TIME-SEPARATED, not traded in one distribution, so not anti-correlated (defeats garble-diversity by construction). Psi=1/2: NE-phasic emit drive vs 5HT-tonic withhold floor; homeostat on phasic-rate -> 1/2; remove NE-phasic -> never sharpens (silence), remove 5HT-floor -> constant phasic (always emit). Honesty: ACh-SNR floor suppresses low-familiarity cells; no cell clears floor -> no winner -> abstain; r = max familiarity-weighted activation, theta in ACh, capacity in NE-gain -> disjoint. G2/falsifiable: tonic breadth samples off-data on-manifold (novel-valid); phasic selector can prefer high-information complement-bearing candidates, read by a judge-free structural detector. G1/binding: phasic pulse co-selects a DA-value-bound COALITION of cells firing together (shared-pulse coupling) whose joint output is super-additive over any single cell; independent-gain ablation -> joint=union (INERT).

## Not-LLM (a_no_llm_frame_trap)

Capability from a 2-timescale gain control over a fixed cell pool -- the breadth-vs-sharpness conflict is solved by TIME-MULTIPLEXING one knob, not a larger sampler or more parameters. Rooted in LC-NE adaptive gain + DA value-gating, an explicit neuro mechanism.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy feature pool + global gain with tonic baseline and phasic pulses: (a) tonic mode -> >=5 distinct-coherent candidates, phasic mode -> single legible winner, both above floors (joint region exists); (b) phasic-rate homeostat -> 1/2; (c) ACh-floor ablation -> fab jumps (gate causal); (d) coalition-coupling ablation -> composition collapses to union. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Gain bus = a section modulating generator L3 logits gain (temperature as tonic/phasic) inside cli/anima.hexa; tonic spread via best-of-K dist>=5 through g6_ideation gen_auto_ideate (engine-native, NOT g6_common torch mirror), phasic G0 via _g6_known_word_ratio; Psi via A<->G; honesty via ImmuneMemory floor; byte-parity py temperature-schedule mirror.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with neuromodulation_gain (H_1284) and neuromod_regime_attractor_field (this census) — distinct: Aston-Jones adaptive-gain solves breadth-vs-sharpness by TIME-MULTIPLEXING tonic/phasic on ONE gain bus; the dual-timescale gain bus is the differentiator.

Maps cleanly onto existing temperature/gain knobs so engine-native is near-term -- but precisely because of that, the load-bearing test is the coalition-coupling ablation separating genuine G1 binding from mere diverse sampling (dist-without-binding / garble-diversity risk). 'Tonic breadth = real recombination' is the unverified rung.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
