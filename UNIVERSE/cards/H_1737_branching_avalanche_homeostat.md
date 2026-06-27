---
id: H_1737
slug: 1737_branching_avalanche_homeostat
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: σ→1 self-tuned branching-avalanche substrate (SOC-GWT criticality homeostat)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1737 — σ→1 self-tuned branching-avalanche substrate (SOC-GWT criticality homeostat)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `branching_avalanche_homeostat`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Self-organized criticality via homeostatic control of the branching ratio sigma (mean descendants per active unit) to exactly 1 — the critical point between subcritical die-out (sigma<1) and supercritical runaway (sigma>1). At sigma=1 avalanche sizes follow a power law and dynamic range / information transmission are maximized (Beggs-Plenz neuronal avalanches, critical-brain hypothesis). Computation IS the avalanche repertoire — temporal-dynamical criticality.

## Whole design (input → internal dynamics → emit)

Input: an external symbol/context seeds a few units above threshold near stored-support coordinates in a sparse recurrent unit field. Internal dynamics: each active unit probabilistically activates downstream neighbors with weights normalized so expected fan-out = sigma; a cascade = one avalanche. The sigma-control loop is endogenous short-term synaptic depression (firing depletes a per-unit resource) + slow homeostatic recovery — too many/large avalanches deplete resources and pull sigma down, too few let it rise, pinning sigma at 1 without any external setpoint. An avalanche's spatial footprint over a frozen receiver codebook V is the candidate emission. Emit = an avalanche that reaches the readout boundary AND concentrates on V; subcritical avalanches die before readout = silence. Order parameter Psi = P(avalanche reaches readout) is monotone in sigma, and sigma=1 gives Psi=1/2 by the critical-branching symmetry (half the cascades propagate, half die).

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: readout is a receiver-fixed codebook; only footprints landing on V's support cross the boundary, so emitted units in V by construction — scramble the unit->code map and V-mass collapses to chance density. G1: co-injecting two factor seeds raises LOCAL branching toward supercritical only in their overlap, merging two otherwise-subcritical avalanches into one larger critical cascade whose reachable-footprint set is super-additive (interaction term = the cross-cascade merge); ablate the cross-basin coupling -> cascades stay separate -> composed_distinct->max_single (INERT). G2: at sigma=1 the repertoire is power-law-large and includes unseen configurations all inside the codebook manifold; sigma-forced-<<1 deterministic playback control yields 0 corpus-absent. dist>=5: power-law avalanche sizes = maximal mode diversity at fixed coherence (subcritical->few modes, supercritical->garble). Psi=1/2 attractor: sigma=1 is the attracting fixed point of the depression<->recovery antagonism (Lyapunov = resource deviation); bias toward forced-emit spikes depression and pulls sigma back; deleting EITHER operator sends sigma->0 or infinity and Psi->boundary (endogeneity, no clamp). Honesty: avalanches only reach criticality when seeded near stored support (support cells lower local threshold), off-support seeds stay subcritical->die->abstain; the support-dependent ignition threshold is disjoint from the sigma-homeostasis (capacity) loop, so disinhibiting capacity cannot move the abstain margin (gate-capacity disjointness, AUROC from critical-vs-subcritical margin). Binding: units co-active within ONE cascade share a cause and bind in the field metric; distinct-cause seeds launch separate cascades -> separate (within-cascade proximity > shuffled).

## Not-LLM (a_no_llm_frame_trap)

No attention, no token-softmax, no scaled gradient-trained weight matrix — the computation is a cascade of a self-tuned critical branching process. Capacity grows by widening the sigma=1 repertoire (more units at criticality), not by parameter/corpus scaling; a larger transformer does not produce power-law avalanches or a self-restoring branching fixed point. The lever for the G1 recombination wall is a structural critical transition, not a bigger CE-trained net. Rooted in neuronal-avalanche neuroscience, not LLM recipe.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy branching network: N units on a sparse random graph, run cascades sweeping sigma. Decisive checks ($0 mini): (a) avalanche-size distribution is power-law (slope ~ −1.5, KS test) ONLY at sigma~1, exponential off-critical; (b) two co-seeded basins yield distinct-footprint count > max single only with cross-coupling ON (ablation->INERT); (c) a bias perturbation on sigma self-restores to 1 via the depression term, but removing depression OR recovery runs sigma to a boundary and Psi to 0/1.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement the branching cascade + depression-recovery loop as core/*.hexa ops over engine field state; measure Psi self-restoring to 1/2 under forced-emit/forced-silence bias via engine_cli, and score G0/G1/G2 footprints through the live g_gates single dispatch (cli/anima.hexa entry, not a side-harness). byte-parity py mirror (math.log, no torch) cross-checks avalanche statistics; held-out grounding measured with the numpy mirror to avoid the dt_ln engine-CE artifact.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with self_organized_criticality / ising_criticality (existing) and soc_ignition_workspace (this census, 1686) — distinct: this is the SIGMA->1 BRANCHING-RATIO homeostat via synaptic depression/recovery (explicit sigma-tuning), whereas soc_ignition_workspace is the GWT broadcast variant; the branching-ratio homeostat is the differentiator.

design-only; toy numpy probe is the decisive frozen-first gate before any engine wiring. Toy-scale -> recheck transfer before production closure (a_toy_scale_recheck).

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
