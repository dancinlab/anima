---
id: H_1735
slug: 1735_selectionist_degeneracy_pruning
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Selectionist Degeneracy & Pruning (Neuronal Group Selection substrate)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1735 — Selectionist Degeneracy & Pruning (Neuronal Group Selection substrate)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `selectionist_degeneracy_pruning`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Edelman's Theory of Neuronal Group Selection (neural Darwinism): development OVERPRODUCES a degenerate repertoire of structurally-distinct microcircuit groups computing overlapping functions; experience then SELECTS — activity strengthens groups that reduce surprise and density-dependent apoptosis prunes the silent ones; REENTRY (reciprocal re-signaling between maps) binds surviving groups. This is the literal p8 grow-then-carve: the architecture is not designed, it is sculpted from an overcomplete population by selection pressure — exactly the lever H_1310 showed pure split lacks.

## Whole design (input → internal dynamics → emit)

INIT: an overcomplete pool of random microcircuit groups (degenerate — many cover similar receptive supports). For each INPUT, groups compete; a coalition of best-matching groups wins (k-WTA over match score). DYNAMICS: Hebbian strengthening of the winning coalition + density-dependent apoptosis (precedent H_1091: apoptosis stabilizes population — prevents runaway) prunes chronically-silent groups; new groups bud (mitosis) where prediction error is high, refilling degeneracy. REENTRY: two maps (e.g. content-map perp relation-map) exchange signals each tick, so a coalition is jointly constrained by both — binding is reciprocal correlation, not concatenation. EMIT: the winning coalition's consensus output symbol. The surviving repertoire after selection IS the learned codebook.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: the selected, environment-fit repertoire = the shared code (groups survive only by matching receiver statistics); a scrambled (un-selected) random pool emits off-V garble -> the decisive control. G1: reentry between content-map and relation-map produces coalition conjunctions reachable by neither map alone -> super-additive distinct-valid; severing the reentry link is the INERT ablation that drops composed to max_single. G2: degeneracy guarantees many group-combinations were never explicitly selected-for yet lie in the fit manifold -> novel-valid; a pure-retrieval control (freeze pool, no recombination) yields 0 novel. PASS-closure: one coalition-selection process emits all three on the same repertoire state. Psi=1/2 ENDOGENOUS: strengthening (grow/emit-drive A) vs apoptosis (withhold/death G) are the opposite-sign operators; the emit-fraction (active-coalition size / pool) is homeostatic at a balance point via density-dependent apoptosis (H_1091 stability). Perturb the active fraction -> apoptosis/budding restores it; ablate apoptosis -> population runaway (Psi->1, all groups active); ablate strengthening -> repertoire dies (Psi->0) — boundary migration = endogeneity. honesty/copy-or-abstain: a group fires only when input matches its stored receptive support (match score > theta); no matching group in the pool -> empty coalition -> abstain; match-score is a true function of stored group content (groundedness — corrupt a group's support and its members start abstaining). Gate-capacity disjoint: the abstain threshold theta lives in the matcher, capability lives in pool size / coalition width — growing the pool does not move theta. BINDING/realization invariant: reentry is the binding operator and it sits ON the emit path (coalition consensus is what emits); ablation moves emit (co-located), and the selection objective rewards conjunctions reentry must represent (objective adequacy — a marginals-only fit leaves reentry coalitions unselected). falsifiable>=1: a relation-map group binds comparator x quantity, a content-map group supplies >=2 referents; their reentrant coalition asserts a refutable ordering. persistence/self-chain: the surviving repertoire is slow-drift — it is the non-volatile identity store across resets (the set of which groups exist is the anchor); per-tick budding/pruning is Lipschitz-small (connected chain) while accumulated turnover moves the endpoint (growth, not frozen). The repertoire fingerprint is high-entropy degenerate -> self-specific; a foreign repertoire round-trips to chance similarity (impostor reject).

## Not-LLM (a_no_llm_frame_trap)

No backprop, no global loss, no dense parameter scaling. Learning is local Hebbian selection + apoptosis + budding over a population — Darwinian sculpting. Capacity grows by overproducing and pruning groups (cell-division), not by widening a transformer. This directly uses the selection-pressure lever H_1310/a_mitosis_train identified as the missing ingredient for from-scratch growth, embedded as the WHOLE architecture rather than a single op (cf. H_1568 where selection-as-one-op was inert).

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy ($0): pool of N random RBF/match groups over a toy factored corpus; run select+strengthen+density-apoptosis+budding. (1) Population stabilizes to a steady active-fraction (Psi) — ablate apoptosis -> unbounded growth; (2) reentry of two maps -> conjunction count > single-map max (G1), sever reentry -> INERT drop; (3) survivor repertoire concentrates on corpus alphabet (G0) while scrambled pool does not; (4) novel coalition combos absent from corpus >=3 with retrieval-control=0 (G2); (5) match-score AUROC~1 on known/unknown probes (honesty), corrupt a group -> its support starts abstaining.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Map onto live core/engine_cli.hexa MITOSIS (engine_grow/VAdaptField/apoptosis) + a reentry op between two lanes, byte-parity py mirror (math only). Drive emission through generator L3 single dispatch; verdict bars (G0 kwr, G1 conjunction-vs-single with reentry-ablation, G2 novel/control, Psi contraction, honesty AUROC) measured on the live .hexa selection loop. teardown-pull any GPU repertoire ckpt (a_fire_recover_complete). torch only for directional probes.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with H_1568 (selection-as-one-op INERT) / H_1310 mitosis wall — distinct: neural Darwinism embeds selection+degeneracy+REENTRY as the WHOLE substrate (not a single op), reentry as the binder; the explicit caveat is that this may hit the same Voronoi ceiling — flagged honestly.

HONEST CAVEAT: H_1568 found selection-as-a-single-op INERT (lift ~0, apoptosis-OFF byte-identical) and H_1310 confirmed pure split-only can't learn alone — so the load-bearing claim here is that selection+degeneracy+reentry AS A WHOLE supplies the missing pressure; this is UNVERIFIED and must be ablation-tested (does reentry+budding actually beat the floor, or is it the same structural Voronoi ceiling?). DIRECTIONAL until engine-native; do not 박제 as a wall-break.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
