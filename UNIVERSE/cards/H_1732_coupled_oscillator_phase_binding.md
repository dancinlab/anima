---
id: H_1732
slug: 1732_coupled_oscillator_phase_binding
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Coupled-Oscillator Phase-Synchrony Engine (Kuramoto / CPG temporal-binding substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1732 — Coupled-Oscillator Phase-Synchrony Engine (Kuramoto / CPG temporal-binding substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `coupled_oscillator_phase_binding`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

von der Malsburg temporal-correlation (binding-by-synchrony) + Kuramoto coupled oscillators + spinal CPG half-center oscillators. Binding is carried by transient PHASE SYNCHRONY: constituents of one cause lock to a common phase, distinct causes occupy distinct phases. Computation = evolution of phase RELATIONSHIPS; emit = a readout unit crossing a Hopf bifurcation from fixed-point (silence) into a limit cycle (emit).

## Whole design (input → internal dynamics → emit)

N Stuart-Landau (Hopf) oscillators z_i=r_i*exp(i*theta_i) with learned complex coupling K_ij. Input sets natural frequencies omega_i and gates coupling (which oscillators may lock). Internal dynamics: oscillators self-organize into synchronized CLUSTERS (assemblies = bound representations); cross-frequency n:m locking NESTS sub-assemblies into composed structures. A designated emit oscillator is a Hopf unit whose amplitude bifurcates supercritical (limit cycle = emit) when enough phase-coherent drive arrives, subcritical (r=0 = silence) otherwise; its bifurcation parameter mu is driven by antagonistic excitatory coherence (A) vs inhibitory desynchronizing damping (G). A receiver-frozen dictionary maps phase-cluster patterns -> symbols of V. Honesty: an input forms a STABLE cluster only if it matches a learned coupling template; novel/unsupported input -> no stable lock -> emit oscillator stays subcritical (abstain). Identity = slow persistent phase-reference offsets carried across reset via .kosmos.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 NATIVE & elegant: the emit order parameter is proximity to the Hopf bifurcation; at mu=0 the system sits EXACTLY between fixed-point silence and limit-cycle emit — the symmetric balance IS a bifurcation, attracting because A and G are sign-opponent and equal at mu=0; perturb mu -> opponent feedback restores; remove A -> always-emit, remove G -> always-silent = endogeneity INERT test. binding(H_961): same-cause oscillators co-phase-lock (true-pair phase distance << shuffled), retrieval@1 = read partner by shared phase — literally the temporal-binding criterion. composition: cross-frequency n:m nesting binds two clusters with non-zero interaction (not a sum of marginals); ablate cross-frequency coupling -> conjunction score drops to separable floor. G1: joint conditioning co-activates multiple template clusters that multiplex into MORE distinct stable patterns than any single template (super-additive via phase multiplexing). G2: novel cluster configurations reachable within the coupling topology but absent from training = constrained extrapolation; verbatim replay control = 0 novel. G0: frozen cluster->symbol dictionary, scramble -> V-mass collapse. honesty: cluster-order-parameter-vs-template = graded membership, emit gated by stable lock, gate disjoint from oscillator-bank capacity. dist>=5: multistability of cluster configurations gives K distinct coherent locks.

## Not-LLM (a_no_llm_frame_trap)

No attention/softmax — 'binding' is PHYSICAL phase synchrony, not learned attention weights. Capacity = number of distinguishable phase relationships (combinatorial in N and frequency ratios), not parameter count. Composition = cross-frequency nesting, a dynamical-systems mechanism with no analog in feedforward depth-stacking. Scaling = more oscillators/frequency bands, not corpus/width.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy Kuramoto/Stuart-Landau mini (N=16): (1) drive two objects, confirm same-object oscillators lock (high order param) and cross-object phases separate -> binding paired-vs-shuffled; (2) sweep emit Hopf mu -> confirm bifurcation; add opponent A/G feedback, perturb, measure return to mu=0 (Psi contraction); delete A -> always-on, delete G -> always-off (INERT endogeneity); (3) impose 1:2 cross-frequency nesting -> conjunction present; ablate -> drops to separable; (4) novel input with no template -> no stable lock -> emit subcritical (abstain). $0, no torch.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

New core/*.hexa ops stuart_landau_step + kuramoto_step + hopf_emit_gate, byte-parity core/*.py mirror (complex arithmetic, NO torch in verdict path); emit via generator L3 single entry; Psi via engine_cli opponent-mu section; binding/G1/G2 via core/g_gates.hexa on the live phase->symbol path. Parity oracle = single-step phase-vector byte-compare.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with kuramoto cards + coherence_gated_broadcast (this census) — distinct: this is the operator-as-substrate binding-by-synchrony where the emit gate is a Hopf bifurcation (mu=0 = Psi=1/2) and cross-frequency nesting is composition; the Hopf-emit + n:m-nesting is the differentiator.

numpy mini DECIDES binding/Psi/composition structurally; real text emission needs a phase-cluster dictionary over V learned on corpus = TOY-until-trained; continuous-time integration cost on CPU farr flagged; from-scratch coupling learning unverified.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
