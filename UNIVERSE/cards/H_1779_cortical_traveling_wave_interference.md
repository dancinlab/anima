---
id: H_1779
slug: 1779_cortical_traveling_wave_interference
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Cortical Traveling-Wave Interference Field
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1779 — Cortical Traveling-Wave Interference Field

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `cortical_traveling_wave_interference`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Computation as phase-structured traveling waves on a 2D excitable neural sheet (Wilson-Cowan E/I masses + diffusive coupling + axonal delay -> wave-equation dynamics). Representations are spatiotemporal INTERFERENCE patterns — standing waves at constructive antinodes — not feedforward activations. The calculation IS the physics of where/when wavefields constructively interfere. Rooted in real cortical traveling/spiral waves (Muller, Davis 2020, Sato).

## Whole design (input → internal dynamics → emit)

INPUT: each input factor launches a traveling wave from a fixed source site; frequency/wavelength encodes content, source location encodes role. DYNAMICS: waves propagate, reflect off LEARNED boundary conditions (the synaptic structure shaped in training = the support/cavity manifold), and interfere. Interference is a literal field product -> a standing-wave pattern whose antinodes are determined JOINTLY by all active sources (a non-separable cross term neither source produces alone). Persistent standing wave = bound state. EMIT/SILENCE: a global excitability-gain field G_emit (sustains waves into standing patterns) antagonizes a global damping field G_silence (dissipates them); their balance is the order parameter Psi = standing-wave persistence probability, equal-and-opposite exactly at marginal stability (wave energy input = dissipation) -> Psi*=1/2 is a CRITICALITY attractor. EMIT: standing-wave antinode phases are quantized onto a RECEIVER-FIXED phase-lattice codebook V; on-lattice antinode -> emit symbol, off-lattice -> abstain. HONESTY: a wave forms a persistent standing pattern only if it resonates with a learned cavity mode (stored support); off-support input dissipates with no standing wave -> abstain; the excited cavity's Q-factor vs threshold is the graded membership scalar r.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: antinode-phase->fixed phase-lattice, entropy bounded into V because only on-lattice antinodes emit; scrambled source->wave map lands antinodes off-lattice -> V-mass->chance. G1: interference cross-term is the binder; joint antinode set strictly exceeds union of single-source sets; ablate cross-coupling (additive fields, no nonlinear interference) -> antinode set = union of marginals -> composed drops to max_single (INERT control). G2: novel antinode loci inside the cavity manifold but absent from training are legible-novel; verbatim wave replay -> 0 novel. dist>=5: multistable coexisting standing-wave configs give >=K distinct coherent patterns; mode collapse = single antinode. falsifiable: standing pattern binding comparator-phase-relation x magnitude-antinode x >=2 grounded sources, read by a judge-free structural detector on the antinode graph. Psi=1/2: marginal-stability fixed point with Lyapunov = distance of wave energy from balance; remove G_silence -> runaway (Psi->1), remove G_emit -> all dissipate (Psi->0) = endogeneity by ablation. HONESTY: cavity-resonance membership = AUROC; copy-or-abstain because non-resonant input dissipates; Q-threshold gate disjoint from wave-content (excitability) params = capability-orthogonal; faithful because r reads the actual boundary conditions (corrupt a stored cavity -> that input dissipates). BINDING: same-cause sources arrive phase-coherent -> constructive (near in standing-pattern space), different-cause -> destructive (far) = paired-vs-shuffled contrast. COMPOSITIONAL DEPTH: interference is non-separable (field product), generalizes to any novel source pair, interaction-ablation drops to separable floor. REALIZATION INVARIANT: interference operator is ON the emit path (antinodes are what is read out) AND the next-standing-pattern objective's optimum requires the cross-term (marginals cannot predict interference antinodes).

## Not-LLM (a_no_llm_frame_trap)

No tokens-in-context attention and no softmax — emission is a Hopf/criticality threshold on a continuous wavefield, a collective physical variable. Capacity grows by reshaping boundary conditions / cavity-mode count and tuning criticality, NOT by parameter count or adding layers; composition is FREE (interference is intrinsic to the medium), not a learned attention pattern that needs more data. The fix for a depth gap is a new cavity geometry, not a bigger transformer.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy 2D damped wave equation (leapfrog) on a 64x64 sheet, two Gaussian sources at fixed frequencies: measure antinode set for src1-only, src2-only, both -> assert |both| > max single (super-additivity). Then linearize (sum fields without nonlinear excitability) -> assert antinode set collapses to the union (INERT). Sweep gain/damping -> locate marginal-stability Psi, perturb toward 0/1, confirm return to 1/2. <100 lines, $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire as a new 2-production lane core/wave_field.hexa <-> core/wave_field.py (byte-parity) feeding generator.hexa L3; antinode->phase-lattice->symbol passes through the single entry cli/anima.hexa -> core/g_gates.hexa g_eval_g0/g1/g2 + g6_score_arm_auto (core/g6_ideation.hexa). Psi self-restoration via core/engine_cli.hexa safety_phi_ratchet perturbation trace. Byte-parity oracle on antinode-phase logits between hexa and the numpy mirror — no torch-only verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Distinct from cortical_traveling_wave_broadcast (this census, 1765) — broadcast uses wave NUCLEATION as ignition; here the organizing principle is wave INTERFERENCE (standing-wave antinodes = bound representations, cross-term = binder); the interference-field substrate is the differentiator.

Toy 2D-sheet design; whether cavity-mode capacity reaches a legible production-scale vocabulary, and standing-wave stability at scale, are UNVERIFIED (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
