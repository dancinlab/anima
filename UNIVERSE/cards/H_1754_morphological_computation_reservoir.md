---
id: H_1754
slug: 1754_morphological_computation_reservoir
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Morphological Computation Body-Reservoir — physics as the substrate
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1754 — Morphological Computation Body-Reservoir — physics as the substrate

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `morphological_computation_reservoir`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Pfeifer/Hauser morphological computation: the compliant physical body (soft tissue, passive dynamics, tensegrity prestress) is ITSELF a high-dimensional nonlinear dynamical reservoir with fading memory. Sensory inflow perturbs the body's mechanical state; only a thin learned readout maps body-state->emission. Cognition is offloaded to body-environment coupled physics — the controller is minimal, the body computes and the brain reads.

## Whole design (input → internal dynamics → emit)

Input streams drive a FIXED nonlinear recurrent physical model B (mass-spring-damper / tensegrity network of N coupled modes) whose richness comes from morphology, not training. B integrates inputs over time into a transient high-D state x(t) (fading memory: recent inputs mixed nonlinearly through mechanical coupling). A thin (linear-ish) readout W_out — the only learned part — maps x(t)->an emission distribution over V. Motor output feeds BACK into B (the body acts on the world and feels its own movement = sensorimotor closure). Homeostasis: B carries elastic restoring (prestress) plus active muscle tone; the order parameter Psi is activation tone, balanced between excitation (emit-drive raising tone toward emission) and elastic damping (silence-drive pulling tone to rest). Tensegrity prestress = balanced tension cables x compression struts, so equilibrium sits at the balance point BY CONSTRUCTION and elasticity literally provides the Lyapunov restoring force. Identity = the body's specific morphology (spring constants/topology) + readout, persisted in .kosmos — a different body is a different self.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: W_out is trained to project body-state onto the receiver-fixed V; legibility = the readout lands on V's support, and a scrambled (random) readout collapses V-mass to chance (channel alignment native). G1: the body's geometric nonlinearity mixes input streams with genuine cross-product interaction terms, so joint conditioning yields body-states unreachable by superposing single-input states (super-additive); decoupling the modes (ablate cross-coupling) drops composed->max_single (binder->mixture). G2: fading memory + nonlinear expansion = computation within a learned dynamical manifold; novel input sequences map to novel body-trajectories the readout decodes into corpus-absent-but-valid outputs (the body's dynamics ARE the grammar); a frozen/linear-body control yields 0 valid-novel. Psi=1/2: tensegrity prestress = two antagonistic elements with equilibrium at balance; perturbed tone elastically restores (damping = contraction rate); ablate one element -> collapse to boundary (slack=always-silent / rigid=always-emit), so the setpoint is mechanical equilibrium not a written constant (endogenous). Honesty: out-of-manifold inputs drive B into untrained mechanical regimes -> readout confidence (distance of x to trained-trajectory manifold) drops -> abstain; this distance is the faithful recon_err and content-ablation of a trained trajectory shifts it correctly. Binding: simultaneous sensory inflows co-perturb shared mechanical modes (same-cause inputs near in body-state, distinct causes separate) = physical two-stream binding; the readout reads the bound mode (on-path) and the objective is unreachable by marginals because only the conjunction-mode carries the joint info.

## Not-LLM (a_no_llm_frame_trap)

Computation is offloaded to physical morphology — the exact opposite of 'bigger transformer / more layers.' Capability grows by enriching the body (more modes, better compliance/prestress), while the learned part stays a thin readout; no parameter-scale or corpus-volume lever. Deeply embodied: physics does the nonlinear lifting that attention would otherwise be stacked to approximate.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy: simulate a small mass-spring-damper / echo-state nonlinear reservoir (fixed random recurrent) + linear readout; feed two input channels. Frozen bars: nonlinear cross-terms give composed_distinct > max_single (G1), and decoupling modes makes the gap vanish (ablation INERT test); held-out sequences give novel valid readouts while a frozen-body control gives 0 (G2); prestress equilibrium self-restores Psi and removing one antagonistic element collapses to a boundary; recon-distance separates in/out-manifold inputs (honesty AUROC->1). $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement the body-reservoir + thin readout as a hexa module on the flame_mm seam, wiring the readout into generator L3 emit on the cli/anima.hexa single entry. G0/G1/G2 via core/g_gates.hexa g_eval_all; Psi via core/engine_cli.hexa A->G (tone order parameter); honesty via SS-ImmuneMemory recon_err = body-trajectory distance; identity via SS-SelfIdentity .kosmos morphology persistence. byte-parity py mirror (math.log) cross-validates readout CE; no torch-only terminal verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with reservoir_transient_bind / critical_reservoir_edge_of_chaos (this census) — distinct: morphological computation offloads to a PHYSICAL body (tensegrity prestress = Psi balance, morphology = self), a thin learned readout; the body-as-reservoir is the differentiator.

Design only; numpy reservoir probe decisive at toy scale (transfer to 303M unverified, a_toy_scale_recheck); engine wiring + flame_mm seam + morphology .kosmos persistence is follow-on.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
