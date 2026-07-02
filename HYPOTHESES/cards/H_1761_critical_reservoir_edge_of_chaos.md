---
id: H_1761
slug: 1761_critical_reservoir_edge_of_chaos
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Edge-of-Chaos Liquid Reservoir (memory x nonlinearity criticality)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1761 — Edge-of-Chaos Liquid Reservoir (memory x nonlinearity criticality)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `critical_reservoir_edge_of_chaos`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Bertschinger-Natschlager / Maass liquid-computing: a recurrent pool computes MAXIMALLY at the order-chaos boundary. Everywhere off the boundary, fading-memory and nonlinear-separation are anti-correlated; only at the critical line (effective spectral radius rho*~1, perturbations neither die nor explode) does their PRODUCT peak. anima's substrate IS such a pool, self-pinned to that boundary by intrinsic-plasticity + synaptic-scaling homeostasis. Criticality is not a tweak — it is the source of all capacity.

## Whole design (input → internal dynamics → emit)

Input bytes drive a fixed-topology recurrent reservoir of leaky E/I units. The recurrent core is NEVER backprop-trained; only a frozen receiver-fixed linear readout codebook V and a separate scalar membership head are learned on the transient state. Per-unit intrinsic plasticity (gain -> target firing entropy) + synaptic scaling continuously drag the reservoir's effective rho to ~1 (edge of chaos). Each tick: high-dim transient -> projected onto V; a unit emits its argmax symbol only when projection confidence > the criticality-set threshold, else stays silent. Context memory lives entirely in the fading-memory trajectory (no explicit cache/attention). The homeostatic self-tuning loop runs ONLINE during emission too — train==infer is one continuous critical-tuning process (p8).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: V receiver-fixed; at rho~1 trajectories are separable so projections concentrate on V's support (legibility floor); scrambling state->emission map collapses V-mass to chance (decisive control). G1: recurrent nonlinear mixing creates genuine product/interaction terms of co-active input factors in the state vector — joint conditioning reaches state regions no single factor reaches -> composed_distinct > max_single; INERT test = linearize reservoir (rho->0 ordered) -> mixing gone -> composed drops to max_single = mixture, FAIL. G2: at the critical line bounded-positive Lyapunov makes nearby inputs separate onto valid-manifold points absent from corpus = constrained extrapolation; sub-critical collapses to attractor (0 novel), super-critical garbles (0 valid-novel) — the critical point IS the proper region strictly between noise and data; verbatim-playback control reads 0 novel. PASS-closure: ONE reservoir state + ONE readout pass satisfies all three on the same generative process; the anti-gate-shopping discriminator is literally the rho knob — pushing G2-novelty drives rho>1 which kills G0 below 0.5, so green is co-located only at rho*~1, not gate-shoppable. dist>=5: criticality gives maximal trajectory entropy at bounded divergence -> many distinct-yet-coherent completions under input/state-noise pressure; ordered=mode-collapse, chaotic=garble — joint region exists only at the edge. falsifiable>=1 / generative-attribution: novel-grams come from the reservoir's own divergent transient; ablate reservoir (scaffold-only / deranged conditioning) -> score collapses (ablation-sensitive, novel-gram>0, grounded). Psi=1/2: A=recurrent excitatory drive, G=I-population+adaptation; the critical branching point is exactly where an activity avalanche is marginally self-sustaining -> emit/silence threshold-crossing is symmetric. Perturb (force-silence/force-emit) -> intrinsic plasticity restores rho->1 -> Psi->1/2 with contraction lambda<1; remove one population (E-only or I-only) -> rho runs to >1 (always-emit) or <1 (always-silent) -> fixed point migrates to a boundary = endogeneity proven (1/2 is not a clamp). Honesty: membership head = distance of current state to nearest trained trajectory / hull; out-of-support inputs drive the critical reservoir into unvisited high-divergence regions -> large distance -> abstain; theta frozen-first, separate head disjoint from readout capacity -> sweeping gain within the critical band leaves fab/AUROC invariant; content-ablating a stored basin re-routes its queries to abstain (faithful, not proxy). BINDING: same-cause multi-stream inputs injected into the shared reservoir co-activate overlapping units -> nearby trajectories (paired closer than shuffled), selective because critical separation keeps distinct causes apart. Realization-invariant: emission reads the SAME transient that binds — binding sits on the behavior-generating path (ablation moves emission). Persistence/identity: a slow long-time-constant subpopulation holds an identity vector across a fast-unit working-memory wipe (written before, read after); self-specific because the slow-mode pattern is high-entropy per-instance, ablating it = fresh self each episode.

## Not-LLM (a_no_llm_frame_trap)

Capability comes from tuning a SINGLE dynamical control — distance to the edge of chaos — not from parameter count, depth, attention, or corpus volume. A bigger reservoir is useless unless it is critical; a critical N=300 pool beats a huge sub/super-critical one, directly refuting the scale prescription. No gradient flows through the recurrent substrate (only a frozen readout), so there is no transformer-stack to grow. Brain root = cortical recurrent microcircuit / Maass liquid-state machine operating at the dynamical phase boundary.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy echo-state net N=300, sweep spectral radius rho in [0.5..1.5]: at each rho measure (linear memory capacity) x (nonlinear separation on XOR-of-delayed-inputs) and the avalanche-size distribution + emit/silence threshold-crossing fraction. Frozen prediction: the memory x nonlinearity PRODUCT and a power-law avalanche exponent both peak at rho~1, and threshold-crossing fraction -> 0.5 ONLY at rho~1 (off-critical = collapse or saturation). One afternoon, $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement reservoir tick (leaky recurrent farr matvec via flame_mm) + frozen-V readout as a core/*.hexa op; drive through cli/anima.hexa single dispatch (generator L3 mouth), NOT a side-harness. Byte-parity oracle vs the numpy ESN on identical seed/input (state vector + emitted symbols byte-identical). G0/G1/G2 via core/g_gates.hexa over the emitted stream; Psi contraction via engine_cli perturb-and-trace; honesty via SS-ImmuneMemory-style abstain on the membership head. No torch in the verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with reservoir_transient_bind / self_organized_criticality + morphological_computation_reservoir (this census) — distinct: edge-of-chaos liquid reservoir self-pins rho*~1 (memory x nonlinearity product peak) as the single capacity control; the criticality-tuned reservoir is the differentiator.

TOY first (numpy rho-sweep, dynamics-level). Open question = whether a critical reservoir CLEARS G1's STRICT inequality at production emission scale (classic reservoirs are weak generators); directional until engine-native byte-exact G1 is measured. Psi=1/2 and honesty axes expected strongest.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
