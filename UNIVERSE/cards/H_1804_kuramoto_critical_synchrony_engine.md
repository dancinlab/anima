---
id: H_1804
slug: 1804_kuramoto_critical_synchrony_engine
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Kuramoto Critical-Synchrony Engine (Order-Parameter Emitter)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1804 — Kuramoto Critical-Synchrony Engine (Order-Parameter Emitter)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `kuramoto_critical_synchrony_engine`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

A large population of phase oscillators whose macroscopic synchronization order parameter R=|<e^{i*theta}>| in [0,1] is the emit/silence control variable. The synchronization phase transition at critical coupling K_c is the antagonistic balance: coupling drives order (emit), frequency-heterogeneity/noise drives disorder (silence). Rooted in cortical synchrony at criticality — gamma synchronization, the metastable brain at the edge of synchrony, whole-brain Kuramoto/Cabral-Deco models. Distinct from coupled-oscillator phase-binding: the organizing variable here is the COLLECTIVE order parameter / phase transition, not phase relations used for binding.

## Whole design (input → internal dynamics → emit)

INPUT encodes content as the natural-frequency distribution g(omega) and/or the community structure of the coupling matrix A. DYNAMICS: dtheta_i/dt = omega_i + (K/N)*sum_j A_ij*sin(theta_j-theta_i) + noise; communities partially synchronize and the partial-sync pattern (which communities lock and their cluster phases) is the internal state. EMIT: when global R crosses threshold the synchronized giant component broadcasts its collective phase pattern, read out via the cluster-membership PARTITION (which oscillators are in the locked component) = a discrete codeword. CODEBOOK: receiver freezes the set of admissible partitions / phase-relation codewords V. COMPOSITION: two input drives form two partially-synced communities; cross-community coupling forces inter-community phase-locking into a BOUND meta-cluster whose partition is not predictable from either community alone (super-additive). PERSIST: the coupling matrix A (community structure) + preferred-frequency vector = slow identity store.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2: strongest native fit — R in [0,1] literally IS the order parameter; A=coupling (synchronize->emit), G=frequency-spread/noise (desync->silence); near K_c the mean-field map has R*=1/2 as an attracting fixed point under slow coupling-homeostasis (R-1/2 feedback on K) with contraction/self-restore; ablate coupling -> R->0 (always silent), ablate heterogeneity -> R->1 (always emit) = emergent balance, not clamp (endogeneity). G0: cluster-partition codewords in frozen V; scrambled phase->partition map -> random partition (~0 V-mass). G1: bound meta-cluster from cross-community coupling is non-separable; ablate inter-community edges -> partition reduces to independent communities = max_single (INERT). G2: new stable partitions (community detection over a continuum) absent from data but valid; verbatim control -> only trained partitions. dist>=5: metastable wandering among partial-sync configurations under varied noise yields >=5 distinct coherent partitions. falsifiable>=1: 'communities i,j phase-lock with R_ij>theta' is a measurable refutable claim; judge-free detector. HONESTY: r(query) = distance of g(omega) from any stored entrainable band; input that cannot form a cluster above R_min -> no emit -> abstain; gate(R-threshold, frozen) disjoint from capacity (N, K magnitude); groundedness — corrupt stored coupling -> communities dissolve -> known queries fail to sync -> abstain. BINDING/REALIZATION: cross-coupling on the broadcast (emit) path; objective = collective coherence whose optimum needs inter-community binding. SELF-CHAIN: coupling matrix is persistent anchor with small drift; foreign coupling -> different sync structure -> impostor reject.

## Not-LLM (a_no_llm_frame_trap)

The computation is a collective phase transition / order parameter, not parameters/tokens/attention; 'scale' = more oscillators but the operative quantity is the macroscopic transition, not a memorized map. Synchrony criticality is a physics/neuro mechanism transformers lack — answers the capability gap with a missing collective-dynamics lane, not a bigger model (a_no_llm_frame_trap).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy Kuramoto N=200, two communities, deterministic seed: (1) sweep K -> R(K) sigmoid transition (criticality); (2) tune K so R=0.5, perturb theta -> R restores (Psi attractor); (3) ablate coupling -> R->0, ablate frequency-spread -> R->1 (endogeneity); (4) cross-community coupling -> a bound meta-cluster partition absent from single-community runs (G1); (5) out-of-band g(omega) -> no sync -> abstain. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

core/kuramoto_decode.hexa (farr phase integration, RK4, deterministic) as generator L3 mouth-kind 'kuramoto' with cluster-partition readout as symbol; eval via cli/anima.hexa -- eval so g_gates.hexa scores one dispatch (G0 frozen partition-V, G1 cross-coupled vs single, G2 corpus-absent partitions); R wired directly as SS-ThirdLaw Psi (anima already treats Psi as emit propensity, so this is a 1:1 structural map). py mirror core/kuramoto_decode.py (numpy-free in verdict path, math.* integration) byte-parity per a_engine_native_learning. Torch-free trace -> terminal-eligible.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with kuramoto cards + chimera (this census) — distinct: here the macroscopic ORDER PARAMETER R IS the emit/silence Psi at the K_c phase transition (cluster-partition = codeword), not phase-relations-as-binder; the critical-synchrony order-parameter emitter is the differentiator.

Design-only ($0). R-as-Psi is the cleanest native Psi of the three, but the generative G0/G1/G2 via cluster-partitions is the unproven part — requires held-out partition-corpus DESCENT before any GREEN. Risk: a too-permissive partition codebook could pass G0 as an artifact -> the scrambled-phase control collapsing V-mass is the mandatory void-check.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
