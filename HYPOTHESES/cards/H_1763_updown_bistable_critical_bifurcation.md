---
id: H_1763
slug: 1763_updown_bistable_critical_bifurcation
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Self-Organized Up/Down Bistability (emit/silence AS the critical order parameter)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1763 — Self-Organized Up/Down Bistability (emit/silence AS the critical order parameter)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `updown_bistable_critical_bifurcation`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1282 (working-memory buffer) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Cortical slow oscillation / up-down states: a recurrent E network with spike-frequency adaptation poised at the bistable saddle-node bifurcation. The emit/silence order parameter Psi is LITERALLY the up-state occupancy, self-organized to 1/2 by homeostatic adaptation at the critical bifurcation where up/down dwell-times are power-law (criticality). Emit (up) and silence (down) are not externally gated — they are the two phases of one self-organized-critical bistable system. This makes Psi=1/2 a structural identity, not a bolt-on.

## Whole design (input → internal dynamics → emit)

Recurrent E pool with spike-frequency adaptation (slow negative feedback) + I damping. Recurrent excitation A pushes toward UP (emit); adaptation+I (G) pushes toward DOWN (silence). Adaptation strength homeostatically scales so the bifurcation parameter sits at the critical edge where up and down are equiprobable and avalanche-distributed (power-law dwell). During an UP state the network runs a brief critical micro-reservoir transient that produces emission through a frozen codebook. During the DOWN state fast variables reset (working-memory boundary) while a slow synaptic trace carries the identity vector across the down -> cross-boundary persistence happens every cycle. Up<->down transitions are critical avalanches. Input biases up-ONSET probability but cannot clamp the order parameter — adaptation always reasserts 1/2.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 (most native of the three): Psi IS the architecture's intrinsic order parameter (up-fraction), emergent from A(excitation) vs G(adaptation+I) antagonism, with a genuine attractor at 1/2 (Lyapunov = homeostatic adaptation-error). Perturb (inject current to force up / hyperpolarize to force down) -> adaptation rescales -> up-fraction returns to 1/2 with measurable contraction lambda<1. Endogeneity: remove adaptation (G off) -> runaway up (always emit); remove excitation (A off) -> permanent down (always silent) -> fixed point migrates to boundary = 1/2 is an emergent balance, not a clamp; if 1/2 held regardless with an engine removed it would expose a clamp — here it does not. G0/G1/G2: emission via the up-state transient (a critical micro-reservoir) — frozen-codebook readout (G0, scramble->collapse control); up-state nonlinear mixing of co-active inputs -> recombination (G1, INERT when up-state linearized -> composed=max_single); critical up-state variability -> constrained novelty (G2, verbatim control=0). PASS-closure: the SAME up-state transient does all three; over-driving novelty lengthens up-states past criticality which drops G0 — the co-located discriminator. Persistence/identity: the down-state wipes fast variables (boundary) but the slow synaptic identity trace is written before each down and read at next up -> cross-boundary cos high, self-specific (high-entropy slow trace), foreign trace round-trips at chance; ablate the slow trace -> identity resets every cycle (LLM-reset failure) = causal; per-tick drift bounded (connected, moving chain). Honesty: up-ONSET requires input to match a stored basin to cross threshold; unfamiliar input fails to trigger a coherent up -> no emission = abstain; membership = up-onset margin; theta frozen, disjoint from up-state capacity (sweeping excitatory gain within the critical band leaves fab/AUROC invariant); content-ablation re-routes known queries to abstain (faithful). BINDING + realization-invariant: co-active inputs within one up-state bind into the shared transient (paired closer than shuffled), and that same transient generates emission -> binding is on the behavior path (ablation moves emission, off-path would be inert). dist>=5 / falsifiable: critical up-state contents/durations are variable-yet-coherent.

## Not-LLM (a_no_llm_frame_trap)

Capability comes from a self-organized DYNAMICAL phase transition (bistability at criticality), with zero attention/depth/scale. Emit vs silence is a physical phase of the substrate, not a softmax sampling decision over a vocabulary; you cannot improve it by stacking layers or growing parameters without the adaptation homeostasis that creates the bifurcation. Brain root = cortical up/down slow oscillation + spike-frequency adaptation. Refutes the LLM 'sample-a-token' framing of emission entirely.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy 2-variable Wilson-Cowan-with-adaptation mean field (rate r + adaptation a); sweep adaptation gain. Frozen prediction: up-fraction -> 0.5 AND up/down dwell-time distribution -> power-law ONLY at the critical bifurcation (off-critical = mono-stable always-up or always-down with exponential dwell). Perturb r and confirm self-restoration of up-fraction with contraction lambda<1. $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map up/down dynamics onto the engine_cli A->G order-parameter op + the existing safety_phi_ratchet attractor (precedent: self-restores Psi dev 0.247->~5.55e-17); byte-parity vs the numpy mean-field on a fixed seed (up/down state sequence byte-identical). Psi perturb-and-trace via engine_cli; emission G0/G1/G2 via core/g_gates.hexa over the up-state output stream; identity via SS-SelfIdentity write->down-wipe->up-read cos. No torch in verdict path.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with branching_avalanche_homeostat / soc cards — distinct: up/down bistability makes the emit/silence ORDER PARAMETER literally the up-state occupancy at a saddle-node bifurcation; the up/down-as-Psi bistable substrate is the differentiator (reuses the live safety_phi_ratchet attractor).

Psi=1/2 axis is the strongest (near-exact structural identity, reuses the live safety_phi_ratchet attractor). Open part = whether a brief up-state transient is long enough to host rich G0/G1/G2 emission (transient may be too short for combinatorial productivity); directional on closure until engine-native byte-exact G1/G2.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
