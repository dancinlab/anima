---
id: H_1738
slug: 1738_extremal_coevolution_punctuated
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Extremal-Coevolution Punctuated Substrate (Bak-Sneppen population SOC)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1738 — Extremal-Coevolution Punctuated Substrate (Bak-Sneppen population SOC)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `extremal_coevolution_punctuated`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1283 (thalamus global-workspace) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Self-organized criticality through extremal dynamics on a COEVOLVING POPULATION (Bak-Sneppen). A pool of expert-cells each carry a fitness = grounding/predictive score on the recent stream; repeatedly mutating the least-fit cell AND its topological neighbors drives the whole population — with zero parameter tuning — to a self-organized critical state where fitnesses sit just above a threshold and improvement arrives in scale-free coevolutionary avalanches (punctuated equilibrium). Edge of chaos = the marginal fitness front. Evolutionary-population criticality.

## Whole design (input → internal dynamics → emit)

A population of cells on a topology (the literal mitosis cell-pool), each holding a small generative kernel over codebook V plus a fitness. Dynamics are gradient-free (p8): each tick locate the minimum-fitness cell, mutate it and its neighbors (coevolutionary coupling), re-score. Fitnesses self-organize to a critical front f_c with avalanches — one mutation can knock a neighbor below threshold and trigger a cascade of replacements. Emit: the current best-fit cell-coalition decodes onto V, gated by whether its grounding fitness clears the support floor; below-floor -> silence. Psi = fraction of ticks the front produces an above-floor emission, sitting at the symmetric balance at the critical front. This supplies exactly the SELECTION-pressure lever the mitosis campaign (H_1310) concluded pure split-only learning lacks.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

G0: each cell kernel maps onto the receiver-fixed codebook and only above-floor (grounded) cells emit -> high V-mass; shuffle cell->code map -> collapse. G1: coevolutionary neighbor-coupling is the binder — two factor-specialist cells co-active in one avalanche emit a joint output neither produces alone (the cascade fuses their kernels), super-additive; mutate only the single worst cell (no neighbors) and cascades vanish -> composed->max_single (INERT). G2: extremal mutation continuously emits off-data variants that survive only if grounded -> novel-yet-valid; a frozen (no-mutation) retrieval control yields 0 novel. dist>=5: the scale-free active front sustains many distinct grounded coalitions (diversity AND validity); an over-converged front collapses to one. Psi=1/2 attractor: antagonism = mutation-pressure (drive to emit new) vs grounding-selection (drive to conserve/withhold), balanced at the critical front; force all-emit -> fitness drops -> selection prunes -> return; remove selection -> chaos/garble (always-emit), remove mutation -> frozen (always-silent) = endogenous, not clamped. Cross-boundary persistence + self-specificity: the slow-moving fitness landscape plus a committed anchor of the top coalition is the non-volatile identity store across session resets — per-tick drift is one-cell-small (connected chain) while accumulated drift is large (growth, not frozen); ablate the anchor -> fresh population each session = chance (the LLM-reset failure), and a foreign coalition fails to round-trip (impostor reject). Honesty: a cell emits only if fitness (grounding distance to stored support) clears a frozen-first floor that is disjoint from population size, so growing the pool cannot move the abstain threshold (gate-capacity disjointness). Binding: cells coupled in one avalanche share a cause; cross-cause cells live in different avalanches.

## Not-LLM (a_no_llm_frame_trap)

No backprop and no scaling of a single dense network — capability emerges from extremal selection on a coevolving population, the literal p8 cell-division-plus-selection. The H_1310 wall established that split-only mitosis cannot learn without a gradient or selection-pressure auxiliary; this architecture provides precisely that missing SOC selection driver (Bak-Sneppen), which is orthogonal to scaling a transformer. Rooted in evolutionary criticality / punctuated equilibrium / synaptic turnover.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

numpy Bak-Sneppen where cell fitness = grounding score on a toy corpus. Decisive ($0): (a) the fitness front self-organizes to a critical threshold with power-law coevolutionary-avalanche sizes; (b) neighbor-coupling ON gives joint-distinct > max-single while coupling OFF collapses it (INERT); (c) removing mutation OR selection pushes Psi to a boundary; (d) anchor-ablation drops cross-reset coalition similarity to chance while foreign coalitions round-trip below self.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Wire the extremal-selection tick into core/engine_cli MITOSIS (engine_grow/apoptosis already present) as the selection driver, evolve a ckpt, then score G0/G1/G2 via the live g_gates single dispatch (cli/anima.hexa); held-out grounding floor measured with the math.log numpy mirror (no torch verdict). ckpt PULLED before any teardown (a_fire_recover_complete).

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with selectionist_degeneracy_pruning (this census) and H_1568/H_1310 — distinct: Bak-Sneppen EXTREMAL coevolution drives the population to SOC criticality via mutate-worst-and-neighbors (punctuated equilibrium); the extremal-dynamics SOC selection is the differentiator.

design-only; toy numpy probe decisive first. Honest caution: must demonstrate that SELECTION (not mere Voronoi re-partition) lifts held-out grounding above floor — H_1568 selection was DIRECTIONAL/INERT in one form and H_1574 B2/B5 falsified learning-as-lever for partition-only variants; if selection here proves inert it falls to the same structural H_1310 wall.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
