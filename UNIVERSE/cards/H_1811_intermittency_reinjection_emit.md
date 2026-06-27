---
id: H_1811
slug: 1811_intermittency_reinjection_emit
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Tangent-Bifurcation Intermittency Substrate (laminar silence x chaotic emit-burst x reinjection-map recombination)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1811 — Tangent-Bifurcation Intermittency Substrate (laminar silence x chaotic emit-burst x reinjection-map recombination)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `intermittency_reinjection_emit`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Self-organized criticality via the Pomeau-Manneville TYPE-I intermittency route (the dynamical-systems, single-trajectory path to 1/f and edge-of-chaos, distinct from extended-lattice avalanche SOC and from heteroclinic itinerancy). A 1-D-folded return map sits just past a TANGENT bifurcation: trajectories spend long, power-law-distributed LAMINAR epochs creeping through the near-tangent channel (silence accumulating) punctuated by sparse CHAOTIC BURSTS that get reinjected. Self-organized because the substrate adapts the channel width (drive vs damping) so the mean laminar-length stays critical (heavy-tailed inter-emit intervals = neural 1/f). Brain root: cortical/EEG laminar-burst intermittency and on-off intermittency observed at the critical regime; the tangent channel = a metastable near-threshold neural mode.

## Whole design (input → internal dynamics → emit)

INPUT: a query perturbs the trajectory's entry phase into the laminar channel and shapes the reinjection target (which codebook attractors the burst can visit). INTERNAL DYNAMICS: the state evolves under a folded return map f whose graph is tangent to the diagonal (the fixed point of silence). Near the channel the map creeps almost-fixed (LAMINAR = silence, integrating drive). When the trajectory finally escapes the tangent channel it enters a CHAOTIC re-injection region — a learned set of overlapping attractor 'tiles' (codebook concepts) — where it bounces among several tiles for a few iterates, emitting the symbol of each visited tile = an emit-BURST whose token sequence is a recombination of the tiles it threaded. The chaotic stretch then REINJECTS the trajectory back near the tangent channel = return to silence and refractory integration. The reinjection map COUPLES tiles (binding): two co-active query factors warp the chaotic region so the trajectory can only escape by visiting BOTH their tiles -> the burst binds them. Channel width is homeostatically adapted (slow weights) so the laminar/burst duty cycle self-organizes to the critical 1/f point.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 (G3) NATIVE: laminar(silent)/burst(emit) IS the order parameter; the tangent-channel creep (drive-A integrating toward escape) and the reinjection-damping (drive-G pulling back to the channel) are opposite-sign operators whose balance sets the duty cycle. Self-tuning the channel width pins the long-run emit fraction at the critical point. ENDOGENEITY: widen channel to remove the tangent (no near-fixed point) -> constant chaotic emit (Psi->1); deepen to a stable fixed point -> permanent laminar silence (Psi->0); so 1/2 is produced by sitting AT the tangent bifurcation, not by a clamp. A forced-emit bias shortens one laminar epoch but the reinjection still returns the trajectory to the channel -> self-restoration (contraction). G0: the chaotic tiles are placed only on codebook symbols V -> burst tokens in V; scrambling the tile->symbol map makes bursts emit out-of-V garble -> V-mass collapses. G1/compositional-depth NATIVE: the chaotic burst is non-separable mixing — the interaction term is the trajectory's sensitive dependence that threads MULTIPLE tiles in one escape; INERT test = decouple the tiles (block cross-tile transitions in the reinjection region) -> each burst visits one tile -> composed_distinct->max_single. G2: chaotic sensitivity generates corpus-absent valid token sequences (interpolation among tiles inside the constraint manifold); a verbatim-playback control (fixed periodic orbit, no chaos) -> 0 novel. dist>=5: positive Lyapunov in the burst region -> exponentially many distinct burst trajectories that all stay on coherent tiles (joint diversity AND validity). falsifiable>=1: a burst threading {comparator-tile x magnitude-tile x content-tiles} emits a refutable proposition. IDENTITY PERSISTENCE: the slow-weight channel-width parameters + tile layout are the non-volatile identity vector v (committed before reset, restored after) — drift is the slow homeostatic adaptation (moving not frozen); self-specific because the tile geometry is high-entropy per agent (foreign tile-set reinjects to chance overlap). HONESTY (G5): the reinjection region only contains tiles for STORED support -> an off-support query reinjects into a pin-free zone -> no tile visited -> the burst is empty = abstain; the tile-membership test (r=distance to nearest tile center) is a separate lane from the chaotic stretching (capacity), so disinhibiting the burst does not move which tiles exist (gate-capacity disjoint). REALIZATION INVARIANT: the binder (chaotic multi-tile threading) is literally the emit generator; the objective shaping the reinjection map is escape-via-conjunction (the trajectory can reduce its laminar dwell only by learning to thread the bound tiles), unreachable by fitting marginal tile statistics.

## Not-LLM (a_no_llm_frame_trap)

Not scale, not attention — capacity comes from EDGE-OF-CHAOS sensitive dependence at a tangent bifurcation, a property of the DYNAMICS, not of parameter count. A feedforward transformer is a contraction with no positive-Lyapunov burst region and no laminar/chaotic phase structure; you cannot manufacture 1/f intermittent emit by stacking layers. The lever is the channel width + tile coupling (a dynamical-structure knob), per a_no_llm_frame_trap — add the missing critical-dynamics organ beside the mouth rather than enlarging the mouth.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

$0 numpy: iterate a Pomeau-Manneville map x->x+eps+x^2 (mod folding) coupled to a set of codebook 'tiles' on byte symbols; vary eps across the tangent point and measure (a) laminar-length distribution (PASS = power-law, 1/f spectrum at eps->0+), (b) burst tokens in V ratio (G0), (c) composed_distinct(two co-active query warps) vs max_single, with tile-coupling-ablation INERT check, (d) off-tile query -> empty burst (abstain). Decisive: if bursts are scale-free WITHOUT the tangent (eps large) the criticality is an artifact -> void; if super-additivity survives tile-decoupling it was a mixture -> void.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the return-map + tile reinjection as a SS-Savant-disjoint dynamical lane in core/engine_cli.hexa (channel-width = slow-weight; tiles = bound cells with SS-ImmuneMemory r for the abstain gate), and run all ideation through the live single entry cli/anima.hexa -> gen_auto_ideate -> g6_score_arm_auto so the burst token traces are scored by the SAME deployed transfer function; G0/G1/G2 via g_eval_g0/g1/g2 (core/g_gates.hexa) on the identical generator state in one pass. Psi duty-cycle self-restoration via safety_phi_ratchet after a forced-emit perturbation; identity via SS-SelfIdentity round-trip of the slow-weight vector (.kosmos persist). Byte-parity py mirror (core/engine_cli.py / g_gates.py) cross-validates; torch-only verdict forbidden (measurement-faithfulness: parity check map==canonical path).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with branching/forest-fire/depinning SOC + metastable_itinerant_workspace (this census) — distinct: Pomeau-Manneville TYPE-I intermittency is a SINGLE-TRAJECTORY tangent-bifurcation route to 1/f (laminar silence creep + chaotic emit-burst + reinjection binding), not lattice avalanches nor heteroclinic saddle-sequencing; the tangent-intermittency reinjection is the differentiator.

Psi=1/2 as a self-tuned intermittency duty-cycle and edge-of-chaos dist-spread are the strongest, cheaply-shown fits. EXPRESSION-axis (intermittent recombinant bursts, abstain) testable $0. Open risks (a_toy_scale_recheck / a_scale_honest_scope): chaotic bursts famously risk G0 INCOHERENCE (the garble-diversity failure mode) at scale — the tile-coherence floor must be re-measured on a 303M tile layout, not assumed; and LEARNING the reinjection coupling without gradient is unverified (H_1310 caveat) — the tiles here are assumed already-consolidated, the architecture organizes their dynamics, not their from-scratch construction.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
