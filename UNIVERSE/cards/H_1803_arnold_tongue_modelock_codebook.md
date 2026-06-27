---
id: H_1803
slug: 1803_arnold_tongue_modelock_codebook
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Arnold-Tongue Mode-Locking Codebook (Devil's-Staircase Emitter)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1803 — Arnold-Tongue Mode-Locking Codebook (Devil's-Staircase Emitter)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `arnold_tongue_modelock_codebook`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

A nonlinear oscillator (or bank) driven by input entrains into rational frequency-lock ratios p:q (Arnold tongues / devil's staircase); the structurally-stable set of rationals (a Farey sequence) is a receiver-fixed discrete alphabet. Computation = which tongue the driven system settles into, and the rotation-number map IS the state->symbol emission. Rooted in mode-locking that is ubiquitous in neural systems: auditory phase-locking, respiratory-cardiac coupling, locomotor gait ratios, theta-gamma n:m locking. Not LLM scale-up — the alphabet is a geometric property of resonance, not a learned softmax.

## Whole design (input → internal dynamics → emit)

INPUT: a query maps to drive parameters (forcing frequency Omega, amplitude K), possibly a vector of drives to coupled oscillators. DYNAMICS: each unit follows a forced limit cycle / sine-circle map; under sustained drive it relaxes onto a phase-locked orbit with winding (rotation) number rho=p/q. The lock has finite tongue width so small input perturbation preserves the symbol (robust quantization). CODEBOOK: receiver freezes a Farey set F (all p/q, q<=Q) before measurement = V; the settled rotation number is read out as the emitted symbol. COMPOSITION: M coupled oscillators each lock; cross-coupling forces a JOINT torus resonance n:m:k that is NOT the product of independent locks (higher-order Arnold tongue) — a non-separable interaction term, so the joint reachable-symbol set is super-additive. EMIT/SILENCE: drive inside a tongue -> stable lock -> emit rational; drive in a quasiperiodic gap (irrational rotation number, no lock) -> no stable symbol -> silence/abstain. PERSIST: the intrinsic-frequency vector + coupling matrix (the tongue STRUCTURE) is the slow, addressable identity store that defines which symbols are reachable = the self.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0 legibility: NATIVE — emitted symbol = rotation number in the frozen Farey set; scrambling the drive->phase map yields irrational/quasiperiodic rotation not in F, V-mass ->~0 (decisive control passes). G1 recombination: NATIVE — coupled-tongue torus resonance is a non-separable joint lock; ablate cross-coupling -> joint collapses to product of single ratios = max_single (INERT mixture-detector). G2 novelty: NATIVE — Farey set is infinite, so valid p:q unseen in training are constrained-extrapolation; verbatim-playback control reproduces only trained ratios (0 novel), noise->irrational (0 valid-novel). dist>=5: many tongues coexist under jittered drive, each a distinct coherent rational. falsifiable>=1: a lock p:q asserts 'output period = q drive cycles' = measurable/refutable; judge-free detector fires on (ratio AND bounded-q AND stable-across-resamples). PSI=1/2: NATIVE — order parameter = lock-probability L in [0,1]; antagonists are forcing K (drive-to-lock=A) vs detuning/phase-noise D (drive-to-unlock=G); at the tongue boundary (SNIC bifurcation) L=1/2 is an attracting fixed point of slow K-homeostasis (contraction, self-restore). Ablate A (K->0) -> no tongues -> L->0 always silent; ablate G (D->0) -> tongues fill -> L->1 always lock = endogeneity proven, not a clamp. HONESTY copy-or-abstain: NATIVE — r(query)=detuning to nearest tongue center; inside->lock->emit stored ratio, outside all tongues->quasiperiodic->abstain; AUROC from lock/no-lock separation; gate(tongue membership, frozen) disjoint from capacity (drive amplitude widens tongues but membership decision unchanged); groundedness — corrupt stored intrinsic frequencies -> tongues move -> known queries fall into gaps -> abstain. BINDING/COMPOSITIONAL-DEPTH/REALIZATION: cross-coupling operator is ON the joint readout (emit) path; objective = lock-error minimization whose optimum requires the joint resonance (unreachable by marginal single locks). SELF-CHAIN: intrinsic-frequency vector is the persisted anchor with small consecutive drift; a foreign frequency vector reproduces a different tongue map -> impostor reject.

## Not-LLM (a_no_llm_frame_trap)

No tokens, attention, or vocab-softmax; the discrete alphabet emerges from nonlinear resonance geometry (tongues are structurally privileged rationals), not from corpus size. 'More capacity' = more oscillators/coupling, but legibility and novelty come from the rational-lock manifold, not scale. A larger transformer does not create Arnold tongues — this is a resonance substrate, satisfying a_no_llm_frame_trap (motor/auditory entrainment lens, not scale lens).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy sine-circle map theta_{n+1}=theta_n+Omega-(K/2pi)sin(2pi theta_n), deterministic seed, <100 lines: (1) sweep Omega at fixed K>0, compute rotation number -> devil's-staircase plateaus at rationals = legible alphabet; (2) 2-coupled oscillators -> a joint n:m lock absent from either single staircase (G1); (3) ablate K->0 -> staircase becomes identity line (continuum, no plateaus) -> G0 collapses; (4) tune K so half a random Omega-batch locks -> L~0.5, perturb and show restoration (Psi attractor); (5) Omega in a gap -> irrational rho (no plateau) -> abstain. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement sine-circle/coupled-tongue dynamics as core/modelock_decode.hexa (farr phase arrays, deterministic iteration) exposed via generator L3 as mouth-kind 'modelock' with gen_modelock_chat dispatch; rotation-number readout = emitted symbol stream fed through cli/anima.hexa -- eval so core/g_gates.hexa g_eval_g0/g1/g2 score the SAME single dispatch (G0 via frozen Farey V, G1 coupled-vs-single distinct, G2 corpus-absent rationals); lock-probability wired as the SS-ThirdLaw Psi order parameter. byte-parity py mirror core/modelock_decode.py (math.* only, no torch/numpy in verdict path) cross-validates per a_engine_native_learning. Torch absent from the trace -> terminal-eligible.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with kuramoto / oscillator cards — distinct: Arnold-tongue mode-locking makes the FAREY set of rational lock-ratios (devil's staircase) the receiver-fixed codebook + lock-probability as Psi; the mode-lock codebook is the differentiator (alphabet from resonance geometry).

New substrate, design-only ($0). Decisive probe is numpy; any GREEN requires the hexa mouth + held-out ratio-corpus mirror-DESCENT gate (a_clm_gen_pipeline) first. Open risk (a_toy_scale_recheck): whether a learned drive-encoder can place real linguistic content into (Omega,K) so Farey symbols carry semantics is unverified and scale-sensitive.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
