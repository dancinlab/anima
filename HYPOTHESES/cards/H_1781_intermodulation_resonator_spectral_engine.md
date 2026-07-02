---
id: H_1781
slug: 1781_intermodulation_resonator_spectral_engine
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Intermodulation Resonator Spectral Engine
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1781 — Intermodulation Resonator Spectral Engine

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `intermodulation_resonator_spectral_engine`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Spectral/resonance computation via a bank of nonlinearly-coupled damped resonators (Izhikevich resonate-and-fire / subthreshold oscillation neurons). Composition is the COMBINATION-TONE (intermodulation) cross product — the cochlear/auditory principle that two tones generate sum/difference frequencies. Calculation = a spectral trajectory through resonance and the edge-of-self-oscillation Hopf balance, not feedforward summation.

## Whole design (input → internal dynamics → emit)

SUBSTRATE: a bank of damped harmonic oscillators, each with a complex eigenfrequency omega_k + i gamma_k; learned eigenfrequencies = the content alphabet, learned NONLINEAR (quadratic) coupling = combination-tone rules. INPUT: a temporal trajectory drives the bank; each resonator integrates with its oscillatory kernel = online spectral decomposition (which resonators ring). DYNAMICS: when two resonators ring together the quadratic coupling pumps energy into combination-tone resonators at omega1 +/- omega2 — these fire although no single input excited them (a literal product term present only when BOTH factors are co-active). EMIT/SILENCE: A = regenerative resonance gain (raises Q, ringing sustains -> emit), G = damping gamma (ringing decays -> silence); Psi = sustained-ring probability, equal-and-opposite at marginal Q (gain=damping = edge of self-oscillation) -> Psi*=1/2 is the Hopf-bifurcation-balance attractor. EMIT: a resonator that crosses the sustained-ring threshold AND whose phase aligns with a fixed readout-phase lattice (codebook) emits its symbol; sub-threshold or off-lattice -> abstain. HONESTY: a resonator exists only for stored-support frequencies; an input frequency with no matching resonator excites nothing -> abstain; r = spectral distance to nearest resonator eigenfrequency.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: ringing resonator -> fixed frequency/phase codebook, only resonators tuned to legal symbols emit; scramble input->drive map -> random ringing off-lattice -> V-mass->chance. G1: combination-tone resonators are the binder — two feature freqs drive a combination tone unreachable by either alone -> composed_distinct > max_single, multiplicative; linearize the coupling (ablation) -> combination tones vanish -> composed->max_single (decisive INERT). G2: intermodulation produces corpus-absent valid frequencies inside the generative constraint (harmonic structure); linear playback control -> 0 novel. dist>=5: multiple simultaneous ringing modes + combination tones give distinct coherent spectra. falsifiable>=1: a combination tone binds a measurable magnitude (frequency/amplitude) relation -> structural detector fires; resonators assert magnitude not stance/question. Psi=1/2: Hopf onset (gain=damping) is the bifurcation, emit/silence balance is marginal-Q, self-tune restores; ablate damping -> runaway self-oscillation (Psi->1), ablate gain -> all decay (Psi->0). HONESTY: spectral-distance membership AUROC; copy-or-abstain (no resonator -> no emit); resonator-existence/Q-threshold gate disjoint from coupling-strength (composition capacity); faithful (r reads eigenfrequency set; remove a resonator -> that input abstains). BINDING: same-cause inputs phase-coherent -> resonators ring in-phase -> constructive combination tones; different-cause -> tones cancel = paired-vs-shuffled on combination-tone amplitude. COMPOSITIONAL DEPTH: intermodulation non-separable (product), defined for every novel resonator pair, ablate mixing -> separable floor. REALIZATION INVARIANT: combination-tone resonators ARE read out (on path); predict-next-spectrum objective optimum requires the intermodulation product (a linear-marginal fit cannot predict combination tones — the clm303 lossF~0-yet-recombine-fail trap is structurally excluded).

## Not-LLM (a_no_llm_frame_trap)

Computation is continuous-time resonance physics (Q, eigenfrequencies, quadratic mixing), not discrete-token attention; emission is a Hopf-threshold crossing, not a softmax. Combinatorial productivity comes FREE from nonlinear physics (combination tones are intrinsic), not from scaling parameters or corpus volume; you grow capacity by adding resonators and mixing rules, never by transformer depth. The recombination wall is dissolved at the substrate level, not via a bigger objective.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy bank of damped oscillators with quadratic coupling: drive f1 alone, f2 alone, f1+f2; FFT the output and assert peaks at f1 +/- f2 appear ONLY in the joint case (composed>max_single). Linearize the coupling -> assert combination tones vanish (INERT). Sweep gain vs damping -> locate marginal Q, perturb, confirm return to balance. <100 lines, $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire core/resonator_bank.hexa <-> core/resonator_bank.py (byte-parity); ringing->phase-lattice symbol via cli/anima.hexa single entry -> core/g_gates.hexa g_eval_g0/g1/g2 + _g6_is_falsifiable (combination-tone magnitude relation) + _g6_jaccard dist via core/g6_ideation.hexa. Psi via safety_phi_ratchet perturbation-restore, honesty via SS-ImmuneMemory AUROC (self-tune sweep OFF/ON fab byte-identical), identity via SS-SelfIdentity tuning vector. numpy Hopf byte-parity mirror (torch verdict 금지).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with coupled_oscillator_phase_binding / self_tuned_hopf_critical_resonator (this census) — distinct: intermodulation engine makes COMBINATION TONES (omega1 +/- omega2 sum/difference) the native binder; the spectral intermodulation resonator is the differentiator.

Vibration(Hopf) criticality — orthogonal to absorbing-state SOC; sensory front-end + combination-tone ideation. toy decisive but combination-tone codebook covering language register (frequency->language token mapping) needs scale/mapping recheck.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
