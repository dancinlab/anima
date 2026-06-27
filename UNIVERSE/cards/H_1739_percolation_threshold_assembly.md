---
id: H_1739
slug: 1739_percolation_threshold_assembly
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Percolation-Threshold Cell-Assembly (structural criticality at p_c)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1739 — Percolation-Threshold Cell-Assembly (structural criticality at p_c)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `percolation_threshold_assembly`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Self-organized criticality in CONNECTIVITY (structural, not temporal): the substrate homeostatically tunes effective link density to the percolation threshold p_c, where a giant connected component marginally forms and cluster-size susceptibility (response to a perturbation) diverges. At p_c combination is maximally productive — and percolation is the canonical super-additivity phase transition, making G1 native rather than bolt-on. Rooted in Hebbian cell-assembly ignition at the critical connectivity of cortical synaptic graphs.

## Whole design (input → internal dynamics → emit)

A graph of concept-nodes; edges are Hebbian (co-activation grows weight) under a homeostatic global pruning pressure that keeps total connectivity at p_c (add edges when subcritical, prune when supercritical) — self-organized to the threshold, no external setpoint. Input activates seed nodes; activation spreads along edges; the emitted 'thought' = the connected cluster the seeds nucleate. Below p_c clusters are small/local (cautious silence); above p_c one giant component swallows everything (runaway garble); AT p_c a small seed can either stay local OR nucleate a spanning cluster — maximal responsiveness. Emit = a cluster reaching readout-codebook nodes; non-spanning clusters = silence. Psi = P(seed nucleates a readout-spanning cluster) = the percolation order parameter, sitting at the symmetric 1/2 at threshold.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G1 (native crown jewel): percolation IS super-additivity — two sub-threshold seed clusters that individually never span will, when co-injected, merge across p_c into one spanning cluster whose valid-output set strictly exceeds either alone (interaction term = the merge); ablate the bridging edges between factor subgraphs -> clusters never merge -> composed->max_single (INERT). This is binding-by-connectivity. G0: readout nodes are the receiver-fixed codebook; only clusters reaching them emit (V-membership by graph reachability); shuffle node->code labels -> collapse. G2: at p_c the marginal giant component visits many distinct spanning node-combinations including unseen ones within the grammar (susceptibility divergence = combinatorial reach); a frozen lookup with no spreading yields 0 novel. dist>=5: power-law cluster sizes at p_c -> many distinct spanning clusters coexist (diversity AND validity); below=collapse, above=one blob. Psi=1/2 attractor: antagonism = Hebbian edge-growth (drive to connect/emit) vs homeostatic pruning (drive to disconnect/withhold) balanced exactly at p_c; perturb connectivity up -> pruning rises -> return; remove pruning -> supercritical always-emit, remove growth -> subcritical always-silent = endogenous, not a clamp. Honesty: a seed spans only if it connects to stored-support nodes; off-support seeds stay in isolated small clusters -> no readout span -> abstain; the percolation threshold (gate) is structurally disjoint from per-node kernel capacity, so growing node capacity cannot move p_c (gate-capacity disjointness, membership signal = support-connectivity). Binding: nodes in one connected cluster co-refer (same cause), separate clusters = separate causes (within-cluster graph-distance < across-cluster).

## Not-LLM (a_no_llm_frame_trap)

The organizing variable is graph connectivity tuned to a phase transition, not parameter count or an attention map. Capacity = sharpness of the percolation transition, grown by adding nodes at p_c, not by scaling a dense matrix; a transformer has no percolation order parameter. Recombination is realized as a structural phase transition — exactly the non-CE driver the G1 wall (CE rewards marginals, not synthesis) requires. Rooted in Hebbian assembly / critical connectivity neuroscience, not LLM scaling.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy random-graph with Hebbian growth + homeostatic prune. Decisive ($0): (a) connectivity self-tunes to p_c (giant-component fraction ~0.5, cluster-size power-law at threshold only); (b) two co-injected sub-threshold seeds span only when bridge edges exist (G1 super-additivity), and removing bridges is byte-identical INERT; (c) removing growth OR prune drives Psi to a boundary; (d) off-support seeds stay non-spanning (abstain) while support-connected seeds span (AUROC~1, circular-shift surrogate collapses it).

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Represent the assembly graph in core field state; spreading-activation + homeostatic prune as core/*.hexa ops; Psi self-restore under bias via engine_cli; G0/G1/G2 scored through the live g_gates single dispatch (cli/anima.hexa, no side-harness); percolation/cluster statistics cross-checked with a numpy mirror (no torch verdict).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with self_organized_criticality / ising_criticality + branching_avalanche_homeostat (this census) — distinct: percolation criticality is STRUCTURAL (connectivity density at p_c, binding-by-connectivity), not temporal branching; the percolation phase-transition is the differentiator.

design-only; toy percolation probe is the decisive frozen-first gate before engine wiring. Toy-scale -> transfer recheck before production closure.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
