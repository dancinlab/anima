---
id: H_1807
slug: 1807_trophic_overproduction_apoptosis_sculpt
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Trophic-Overproduction & Apoptotic Sculpting Substrate
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1807 — Trophic-Overproduction & Apoptotic Sculpting Substrate

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `trophic_overproduction_apoptosis_sculpt`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Neurotrophic competition and programmed cell death sculpting (Oppenheim; Levi-Montalcini NGF; target-derived LIMITED trophic factor). The system overproduces candidate units, then ~half die — survival is awarded only to units that made FUNCTIONALLY USED, decodable connections to a fixed target that secretes a finite trophic budget. The final architecture is SCULPTED by actual usage, not authored; capability is reached by removal, not addition.

## Whole design (input → internal dynamics → emit)

Begin with an overproduced pool of candidate emission units, each proposing a state->symbol map. A fixed external TARGET (the receiver = frozen codebook + a demand profile) secretes a limited trophic budget B per cycle. Each unit's trophic uptake = how much its proposed output is actually decodable by the target AND meets unmet demand. Units compete for the finite B; uptake below a survival threshold theta -> apoptosis (prune). Survivors sprout into freed space (overproduction continues), so the population cycles toward a sculpted set whose every member is grounded in real target demand. Emission = the surviving units' outputs through the single dispatch. Honesty is structural: a unit emitting content the target cannot decode / does not demand draws zero trophic uptake -> dies -> there is no surviving path that fabricates off-support. Population sits at carrying capacity Psi-half as overproduction (sprout/emit) balances apoptosis (prune/withhold). The sculpted survivor set is the persistent identity regrown from the same seeds after reset.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

honesty (copy-or-abstain): trophic uptake r = decodability x demand against the FIXED target support, theta = survival threshold; off-support emitters starve -> apoptosis -> structurally no fabrication path survives. Gate-capacity disjointness: enlarging the overproduced pool does not move theta (separable coordinates). Faithfulness: corrupting the target support drops uptake for the units it grounded -> they die (gate tracks actual content, not a proxy). AUROC separation is the uptake distribution of demanded vs undemanded. G0: trophic reward only for V-decodable outputs -> survivors concentrate on V by selection; non-V starves to chance. Psi=1/2: overproduction A vs apoptosis G are equal-and-opposite at carrying capacity -> density-dependent stable attractor (anima precedent H_1091 apoptosis density-stabilization); remove apoptosis -> runaway to boundary, remove overproduction -> extinction = endogeneity, not clamp. self-chain: sculpted survivor set persists across reset (committed seeds); a foreign survivor set fails to take up budget here = impostor reject. G1/G2/dist: because the target DEMANDS conjunctions, units that bind multiple factors out-compete single-factor units -> recombinant survivors dominate (composed>max_single), novel-but-demanded combos survive while verbatim-only units lose budget margin. binding/realization: only survivors ON the emit path whose output reduces unmet-demand (objective unreachable by marginal single-factor uptake) persist.

## Not-LLM (a_no_llm_frame_trap)

Inverts 'bigger is better': capacity is PRUNED (apoptosis) not scaled; the sculpt is by usage/death, not gradient descent over more parameters. No attention, no corpus growth. Rooted in literal PCD/neurotrophic biology. Distinct from Edelman selectionist degeneracy (group VALUE selection) — here it is target-derived LIMITED trophic factor competition with literal cell death as the sculptor.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy mini: N overproduced linear emitters; fixed target demand vector over V; trophic budget B; uptake = match(output,demand) normalized to B; prune below theta; resprout into freed slots. Frozen-first theta. Decisive probes — (i) off-support fabrication rate -> ~0 after sculpt vs a gate-OFF control (force-survive) where fab jumps (causal honesty); (ii) population returns to carrying capacity under perturbation with lambda<1 (Psi); (iii) AUROC of uptake separating demanded vs undemanded; (iv) ablate apoptosis -> fab spike + population runaway (INERT/coupled test). $0.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement SS-TrophicSculpt over core/engine_cli.hexa MITOSIS/apoptosis ops (engine_grow + apoptosis already live) with the fixed target = the frozen receiver codebook + demand; hexa + byte-parity py. Verdict honesty via the live SS-ImmuneMemory abstain bar (fab=0, AUROC) on the sculpted survivor set; G0/G1/G2 via core/g_gates.hexa on survivor outputs through cli/anima.hexa single dispatch; Psi via the population order-parameter restore trace. Parity oracle = single-cycle uptake/prune hexa<->py byte-identical. No torch in verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with selectionist_degeneracy_pruning (this census) / H_1091 apoptosis — distinct: trophic sculpting uses TARGET-DERIVED LIMITED trophic factor competition + literal apoptosis (usage-decodability = survival), not group-value selection; the trophic-overproduction sculpt is the differentiator (honesty by structural starvation).

TOY (abstract demand vector). Whether 'trophic uptake = real decode demand' transfers to 303M byte emission is unverified. Leans on anima-proven apoptosis density-stability (H_1091) and abstain (H_1576); the novel claim is fusing them into a usage-sculpted honest emission population.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
