---
id: H_1780
slug: 1780_chimera_metastable_coherence_split
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Chimera Metastable Coherence-Split Substrate
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1780 — Chimera Metastable Coherence-Split Substrate

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `chimera_metastable_coherence_split`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Metastable coordination dynamics (Kelso/Tognoli; Abrams-Strogatz chimera): a population of coupled phase oscillators spontaneously and reversibly splits into a SYNCHRONIZED coherent cluster and a DESYNCHRONIZED incoherent sea. The coherence fraction is the order parameter; computation = which oscillators join coherence and when. Distinct from operator-level phase-binding: the organizing principle is the order+disorder COEXISTENCE as the emit/silence dynamics itself.

## Whole design (input → internal dynamics → emit)

SUBSTRATE: N Kuramoto-Sakaguchi phase oscillators with phase-lag alpha, heterogeneous natural frequencies omega_i set by stored content, nonlocal learned coupling K_ij (= memory). INPUT: a stimulus biases the frequency/coupling of a subset, seeding a coherent cluster around the matching attractor frequency. DYNAMICS: synchronizing coupling (drive A) competes with frequency heterogeneity + phase-lag (drive G); at intermediate coupling the system lives in a CHIMERA — a coherent cluster (the currently bound/thought content) coexisting with an incoherent sea (withheld). EMIT/SILENCE: Psi = coherence fraction R (Kuramoto order-parameter magnitude). A pulls toward full sync (R->1, always-emit), G pulls toward incoherence (R->0, always-silent); equal-and-opposite at the chimera balance -> Psi*=1/2 (half the population coherent), locally attracting via Ott-Antonsen self-consistency contraction. EMIT: the coherent cluster's collective phase pattern is quantized onto a fixed receiver phase-codebook; incoherent oscillators emit abstain. COMPOSITION: two co-active stimuli recruit two frequency clusters; if commensurate they m:n phase-lock into a joint collective rhythm neither produces alone (super-additive). HONESTY: an oscillator joins coherence only if its natural frequency is within Delta of a stored attractor frequency; off-support stimulus finds no match -> oscillators stay incoherent -> abstain; r = frequency-distance to nearest stored attractor.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2: strongest native fit — R in [0,1] literally IS the order parameter; A=coupling (synchronize->emit), G=frequency-spread/noise (desync->silence); near K_c the mean-field map has R*=1/2 as an attracting fixed point under slow coupling-homeostasis (R-1/2 feedback on K) with contraction/self-restore; ablate coupling -> R->0 (always silent), ablate heterogeneity -> R->1 (always emit) = emergent balance, not clamp (endogeneity). G0: cluster-partition codewords in frozen V; scrambled phase->partition map -> random partition (~0 V-mass). G1: bound meta-cluster from cross-community coupling is non-separable; ablate inter-community edges -> partition reduces to independent communities = max_single (INERT). G2: new stable partitions (community detection over a continuum) absent from data but valid; verbatim control -> only trained partitions. dist>=5: metastable wandering among partial-sync configurations under varied noise yields >=5 distinct coherent partitions. falsifiable>=1: 'communities i,j phase-lock with R_ij>theta' is a measurable refutable claim; judge-free detector. Psi=1/2: chimera coherence-fraction fixed point, Lyapunov via the Ott-Antonsen reduced map; remove G (heterogeneity) -> R->1, remove A (coupling) -> R->0; perturb R -> returns to balance. HONESTY: frequency-distance membership AUROC; copy-or-abstain (off-frequency stays incoherent); frequency-match-threshold gate disjoint from coupling-strength (capacity); faithful (r reads stored omega attractors; corrupt one -> that stimulus can't recruit coherence). BINDING: same-cause oscillators frequency-lock -> coherent together, cross-cause -> separate clusters = paired-vs-shuffled phase proximity. COMPOSITIONAL DEPTH: m:n locking non-separable, generalizes to novel commensurate pairs, ablate cross-locking -> separable floor. REALIZATION INVARIANT: the coherent cluster IS read out (on path); predict-collective-rhythm objective optimum requires the cross-locking interaction term.

## Not-LLM (a_no_llm_frame_trap)

Emission emerges from a population SYNCHRONIZATION order parameter — a collective dynamical variable with no analog in token attention or a softmax gate. Capacity = number of distinguishable stable chimera configurations, grown by coupling TOPOLOGY not parameter count; the emit/silence balance is intrinsic to chimera coexistence, not a learned binary gate. You cannot scale your way to it with more data — you tune coupling/heterogeneity onto the chimera regime.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy Kuramoto-Sakaguchi, N=100, two-population nonlocal coupling at known chimera params (Abrams 2008): measure R, confirm the coherent/incoherent split (R~0.5). Seed two commensurate clusters -> assert a joint locked mode appears (composed>max_single); kill cross-population coupling -> assert the joint mode vanishes (INERT). Force R->1 then release -> confirm return to chimera. <120 lines, $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire core/oscillator_field.hexa <-> core/oscillator_field.py (byte-parity); coherent-cluster phase -> codebook through cli/anima.hexa single dispatch -> core/g_gates.hexa g_eval_g0/g1/g2; R-perturbation Psi trace via core/engine_cli.hexa safety_phi_ratchet analog. Byte-parity on the order-parameter R and emitted phase symbols vs numpy mirror — no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with kuramoto / coupled_oscillator_phase_binding (this census) — distinct: chimera substrate uses the ORDER+DISORDER COEXISTENCE (coherent cluster + incoherent sea) coherence-fraction R as the emit/silence Psi; the metastable chimera split is the differentiator.

Toy N=100 design; whether the count of stable chimera configurations scales to a legible production vocabulary, and chimera stability against finite-size fluctuations at scale, are UNVERIFIED.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
