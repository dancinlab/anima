---
id: H_1809
slug: 1809_forest_fire_growth_burn
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Forest-Fire Cascade Substrate (slow consolidation drive x sparse query-ignition x connected-cluster burn)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1809 — Forest-Fire Cascade Substrate (slow consolidation drive x sparse query-ignition x connected-cluster burn)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `forest_fire_growth_burn`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Self-organized criticality via the Drossel-Schwabl forest-fire route: a TWO-TIMESCALE drive self-tunes a sparse activation graph to the percolation edge — slow 'growth' (memory consolidation deposits new bound cells/edges between concept sites) >> rare 'lightning' (an external query ignites one site). At criticality the burning cluster size is power-law: most ignitions die locally (silence), a few flash through a system-spanning connected cluster (emit-cascade). Criticality is NOT a tuned hyperparameter — it emerges from the ratio (growth-rate / ignition-rate) -> 0, exactly anima's a_no_llm_frame_trap 'add the missing biological structure (timescale separation), don't grow the model'.

## Whole design (input → internal dynamics → emit)

INPUT: a query is delivered as a single 'lightning strike' that ignites the nearest concept-site whose stored content matches (membership = ignition eligibility). INTERNAL DYNAMICS: between strikes the substrate runs a slow GROWTH process — consolidation (CLS-style replay) grows a 'tree' (re-arms a burnable cell) and grows a binding EDGE wherever two constituents shared a generative cause (binding lane deposits the adjacency). When a strike lands, FIRE propagates synchronously along armed edges through the connected cluster, each burning cell emitting its symbol and re-igniting its neighbors, then the burned region goes refractory (cannot re-burn until regrown). EMIT = the ordered symbol trace left by the burn front; SILENCE = a strike that burns a sub-critical (single-cell) cluster and dies. The burn fraction Phi_burn is the order parameter; growth refills toward the percolation threshold p_c so the long-run mean burn sits at the critical point. RECOMBINATION is structural: the burn path threads MULTIPLE concept-sites bound by shared-cause edges, so the emitted trace is a NEW concatenation never grown as a whole. NOVELTY: regrowth re-wires edges stochastically, so each critical burn spans a corpus-absent connected path while every burned cell is itself a legible (known) symbol.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 (G3) NATIVE: emit/silence is literally the active/absorbing phase of the fire — the percolation order parameter. The slow growth (drive-A, builds emit-readiness) and refractory burn-out + open-boundary dissipation (drive-G, withholds) are the two opposite-sign operators; their balance pins mean burn at p_c (1/2 of the critical-window). ENDOGENEITY: ablate growth -> trees never regrow -> system collapses to the absorbing silent phase (Psi->0); ablate refractory dissipation -> runaway global ignition (Psi->1) — so 1/2 is produced by the coupling, not a clamp (perturbation by a forced-emit bias decays as the burned region cannot re-ignite until regrown = contraction). G0: burnable cells ARE the receiver-fixed codebook V (only legal symbols can be deposited as trees); scrambling the state->cell map deposits no valid trees -> ignition finds nothing -> V-mass->0. G1/binding/compositional-depth: the connected-cluster burn over shared-cause EDGES is the binder — interaction is non-zero because |reachable burn path| is super-additive in co-active ignition seeds (two seeds whose clusters touch burn a joint path > either alone); INERT test = delete cross-edges -> clusters disconnect -> composed_distinct->max_single. G2: stochastic regrowth produces corpus-absent burn paths from known cells (support strictly contains data); verbatim-playback control regrows no new edges -> 0 novel. HONESTY (G5): a strike only ignites where a stored pinning cell matches (r = distance to nearest armed cell, theta = ignition threshold) -> off-support strikes find no fuel and die = abstain (emission-closure: every burned symbol traces to a deposited cell); gate-capacity disjoint because ignition-eligibility (the membership metric) lives in a separate lane from cluster connectivity (the capacity) — growing the graph does not move the ignition threshold. BINDING: edges deposited only between shared-cause constituents -> paired-vs-shuffled proximity is the edge adjacency itself. dist>=5: at criticality the cluster-size distribution is heavy-tailed -> many distinct spanning burns coexist (distinct paths, all legible). falsifiable>=1: a burn path that threads {comparator-cell x magnitude-cell x >=2 content-cells} emits a world-partitioning structure. REALIZATION INVARIANT: the binder is ON the emit path (the burn front IS the generator), and the growth objective rewards only paths that complete a burn (marginals alone leave clusters disconnected -> cannot reduce the burn-completion objective).

## Not-LLM (a_no_llm_frame_trap)

No attention, no scaling, no corpus increase. The capacity (combinatorial productivity) comes from the PERCOLATION EDGE of a sparse graph self-tuned by timescale separation — a transformer at any size has a fixed dense forward pass with no absorbing/active phase transition and no slow-drive self-organization; you cannot get power-law cascade reachability by adding layers. The lever is the growth/ignition ratio (a structural-dynamical knob), not parameter count — adding the missing biological structure (consolidation timescale separation) beside the mouth, per a_no_llm_frame_trap.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

$0 numpy: build a 256-site sparse graph (sites = byte symbols), run slow random edge-growth between sites that co-occurred in a tiny frozen corpus + rare random ignitions; sweep growth/ignition ratio and measure (a) burn-cluster-size distribution slope (should approach −1.5 mean-field DP exponent at the self-organized point), (b) composed_distinct(two seeds) vs max_single(one seed) — PASS if super-additive, (c) edge-ablation INERT check (delete cross-edges -> composed drops to max_single), (d) off-support strike -> 0 burn (abstain). Decisive: if super-additivity survives edge-ablation it was a mixture -> void.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Deposit the burnable graph as a .clm/.kosmos-loadable cell set (cells = SS-Savant lane, edges = binding lane in core/engine_cli.hexa) and route ideation through the live single entry cli/anima.hexa -> gen_auto_ideate -> g6_score_arm_auto so the burn trace is scored by the SAME path; G0/G1/G2 via g_eval_g0/g1/g2 in core/g_gates.hexa on the identical generator state (one pass, not three side-harnesses). Psi self-restoration measured by core/engine_cli.hexa safety_phi_ratchet after a forced-burn bias; honesty via SS-ImmuneMemory abstain AUROC with ignition-eligibility as r. Byte-parity py mirror (core/g_gates.py) cross-validates; torch-only verdict forbidden.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with branching_avalanche_homeostat / percolation_threshold_assembly (this census) — distinct: forest-fire SOC self-tunes via the TWO-TIMESCALE growth>>ignition ratio (Drossel-Schwabl), burn = connected-cluster cascade over consolidation-grown edges; the forest-fire growth/burn is the differentiator.

Toy-first: graph SOC and super-additive cluster reachability are cheap to demonstrate $0; the open risk (a_toy_scale_recheck) is whether timescale-separation self-tuning holds at 303M cell counts and whether burn paths stay G0-coherent (not just distinct) at scale. EXPRESSION-axis (does a critical burn recombine) is testable now; from-scratch LEARNING of the edge weights still needs gradient/selection pressure (H_1310 caveat) — growth here is consolidation of ALREADY-bound constituents, not from-scratch feature build.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
