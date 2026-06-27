---
id: H_1748
slug: 1748_divisive_normalization_value_select
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Divisive-Normalization Shunting Selection Field
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1748 — Divisive-Normalization Shunting Selection Field

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `divisive_normalization_value_select`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Striatal/BG value coding uses DIVISIVE NORMALIZATION (Louie & Glimcher; Carandini-Heeger canonical computation): each candidate's selection weight = its drive divided by a pooled sum of all drives, via recurrent shunting (FSI/GPe) inhibition. Selection is context-dependent, conserved (weights sum toward a constant), gain-controlled — winners emerge without explicit argmax, and the gate is intrinsically scale-invariant (capacity-orthogonal).

## Whole design (input → internal dynamics → emit)

INPUT: context -> cortex emits raw drives x_i per codebook channel. DYNAMICS: a recurrent shunting pool computes w_i=x_i^beta/(sigma+sum_j x_j^beta); the denominator is a shared FSI/GPe inhibition field coupling all channels. SELECTION-BY-EMERGENCE: channels whose w_i clear an emit floor open; the shared pool means raising one suppresses others (competition), yet under high total drive several COMPATIBLE channels co-clear (recombination via multiplicative numerator x_a^beta*x_b^beta for compatible pairs). CONSERVATION->Psi: sum w_i=total^beta/(sigma+total^beta) saturates; Psi=sum_open w_i is pinned near the half-saturation point set by sigma (total drive=sigma -> half-saturated -> Psi=1/2). Opponent operators: numerator drive (A, emit) vs denominator pool-inhibition (G, withhold); adding drive grows the denominator too (gain control) -> Psi self-restores (contraction, not clamp). EMIT: open channel-set read out. PERSIST: learned drive weights + .kosmos self-anchor survive boundary; transient pool activation wiped.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2: sigma is the STRUCTURAL symmetric point and divisive gain-control is the contraction — perturbing total drive moves Psi then it RETURNS (responds-then-contracts = real attractor, not a pinned clamp); ablate denominator -> runaway to boundary (no fixed point); ablate numerator -> silence (endogeneity by INERT). Gate-capacity DISJOINTNESS (standout): divisive normalization is scale-invariant in ranking, so multiplying ALL drives (capacity) leaves the open-set and abstain floor unchanged -> d(fab,AUROC)/d(capacity)=0 BY CONSTRUCTION (the H_1576 savant-OFF==ON invariant, here structural). G0/G1/G2: channels=V; recombination via multiplicative numerator coupling (interaction term native), ablate cross-coupling (independent denominators) -> marginal mixture -> composed=max_single; novelty via combinations of supported channels absent from corpus, control 0. PASS-closure: one normalization field yields all three. Honesty: channel with no learned drive (x_i=0) -> w_i=0 -> never opens -> abstain; r=1−w_i grounded (content-ablate a channel's drive -> w->0 -> it abstains, re-ranking by margin); sigma gate frozen + capability-independent -> disjointness. Binding/realization: denominator coupling = non-separable conjunction on emit path (interaction-ablation drops conjunction to separable floor = path-co-location); legible compound unreachable by independent per-channel normalization (objective-adequacy). Faithfulness: the shunting field IS the deployed emit gate.

## Not-LLM (a_no_llm_frame_trap)

Softmax is a degenerate special case of normalization used as READOUT; here normalization is the WHOLE recurrent selection substrate (a shunting inhibition field), the emit decision is floor-crossing on normalized weights (not sampling a vocab distribution), and the signature property — a capacity-DISJOINT scale-invariant honesty gate — is explicitly anti-LLM (LLMs entangle capacity and behavior so scaling moves everything). No attention, no scale/corpus prescription; capacity grows by adding channels. Rooted in canonical divisive normalization + its BG value-coding instantiation.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy, frozen-first: drives x_i, w=x^beta/(sigma+sum x^beta). Check: (1) perturb total drive -> Psi=sum_open w returns toward sigma-set half-saturation (contraction lambda<1, attractor not clamp); (2) scale ALL x by 10x -> ranking, open-set, abstain floor UNCHANGED (capacity-disjointness, d~0 — headline test); (3) multiplicative compatible pair -> distinct-valid > max single; ablate cross-coupling -> equal (INERT); (4) x_i=0 channel -> w=0 abstain, content-ablate a known channel re-ranks its r-margin (grounded); (5) remove denominator -> runaway, no fixed point. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement the normalization pool as a shunting emit-gate over generator L3 channel logits in core/ (divisive op on the single dispatch); score G0/G1/G2 via core/g_gates.hexa (_g6_known_word_ratio, g_eval_g1, g_eval_g2) on identical generator state; measure capacity-disjointness directly by the H_1576 protocol — savant golden-zone disinhibition OFF->ON must leave unknown-input fab byte-identical (0.0==0.0) and abstain-AUROC invariant via engine_cli. Byte-parity py mirror of the normalization field; no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with basal_ganglia_gating (H_1281) / gonogo — distinct: divisive normalization is the WHOLE selection substrate (shunting pool, scale-invariant ranking) whose capacity-disjoint honesty gate is structural; the divisive-normalization-as-selection is the differentiator.

Design + $0 normalization probe only. Engine wiring follow-on (a_verified_must_wire). Capacity-disjoint honesty claim structurally argued + toy-confirmable but TOY until measured on trained channels through CORE; recombination/novelty lift over H_1129/H_1140 bars UNVERIFIED at scale — do not promote toy green to production closure (a_scale_honest_scope).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
