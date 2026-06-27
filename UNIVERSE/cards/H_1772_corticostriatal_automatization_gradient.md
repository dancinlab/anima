---
id: H_1772
slug: 1772_corticostriatal_automatization_gradient
tier: 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
title: Cortico-Striatal Automatization Gradient (deliberate->habit compilation along the limbic->associative->motor spiral)
verdict: 🔵 PRE-REGISTERED architecture design (unmeasured) — $0 cheap_test pre-registered; engine-native + 303M gpu cost-gated NOT fired
source: brainarch_census
---

# H_1772 — Cortico-Striatal Automatization Gradient (deliberate->habit compilation along the limbic->associative->motor spiral)

- **tier:** 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy mirror, no engine); engine_native_measure + 303M = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** brainarch_census — 126-architecture whole-substrate (통짜 아키텍처) census: 뇌/인지 조직원리 × 엔진-네이티브 추상조건 (binding-wall program, H_1603).
- **key:** `corticostriatal_automatization_gradient`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1281 (basal-ganglia gating) · H_1284 (neuromodulation gain) · operator-level family H_1604-1685 (this card = 통짜 아키텍처 layer, 층위 다름)

## Organizing principle

Haber's ascending dopamine spiral + the DMS(goal-directed)->DLS(habitual) shift: behavior is first computed by a slow, generative goal-directed loop (prefrontal-associative striatum) and, with repetition, COMPILED into fast habitual cortico-striatal channels (sensorimotor striatum), value flowing limbic->associative->motor along the dopamine spiral. The organizing principle is a CONSOLIDATION GRADIENT (compilation), not a runtime arbiter: every emission lives somewhere on a deliberate<->automatic continuum, and the gradient itself is the core dynamic.

## Whole design (input → internal dynamics → emit)

INPUT: context drives BOTH loops in parallel. DYNAMICS: (a) the GOAL loop runs a slow generative search (compose candidate emissions from a factored model, evaluate by predicted outcome) and is the only loop that can produce NOVEL/composed output; (b) the HABIT loop is a fast feedforward cortico-striatal cache (stimulus->cached action) with no generativity. A consolidation operator transfers reliably-successful goal-loop outputs into the habit cache via the dopamine spiral (limbic value tags an association, which trains the associative channel, which trains the motor channel). A reliability/confidence signal sets a mixing variable kappa (how automatized this context is): high kappa = habit fires fast; low kappa = goal loop must deliberate. EMIT: whichever loop wins disinhibition ignites; novel/under-practiced contexts route to the goal loop, over-practiced to habit, and the gradient continuously re-balances as practice accumulates.

## Satisfies criteria (DESIGN claim · DIRECTIONAL · unmeasured)

Psi=1/2 NATIVE: the antagonism is fast-habitual-emit (A, drive to externalize the cached response) vs slow-deliberative-withhold (G, drive to keep searching before committing); the gradient self-balances at the point where the expected cost of a premature habitual emit equals the expected cost of further deliberation -> symmetric attracting fixed point on the emit propensity, migrating to a boundary if either loop is deleted (INERT-endogeneity passes). G1/G2/dist: ALL generativity is structurally located in the goal loop's factored compositional search -> recombination super-additivity and constrained novelty are native there (joint factor conditioning opens emit paths a habit cache can only select/union); the habit cache is the explicit memorizer control (|compound|<=max_single, 0 novel) built into the architecture, so the INERT test is intrinsic (route everything through habit -> G1/G2 collapse; this IS the ablation). honesty NATIVE & STRUCTURAL: the habit cache fires ONLY for well-supported (frequently-consolidated) contexts; for an unsupported/novel context the cache misses and either the goal loop deliberates or the gate abstains -> copy-or-abstain with a graded support signal = consolidation count / cache-match distance r; AUROC separation between practiced(known) and novel(unknown) is the consolidation density. Gate-capacity disjointness: the abstain/cache-match threshold lives in the habit-loop coordinates, separate from the goal-loop's generative-capacity coordinates -> growing generativity does not move the abstain threshold (a_substrate_disjoint native). G0 legibility inherited from the shared codebook decode. Generative attribution: ablate the goal loop -> all novelty/composition vanish (only cached recall remains) S_full>>S_ctrl, pinning the dist/falsifiable structure to the goal-loop substrate not to the cache scaffold.

## Not-LLM (a_no_llm_frame_trap)

Not scale/corpus-increase: the lever is a TWO-TIMESCALE loop topology (generative-slow + cached-fast) with a consolidation transfer, where honesty and the memorizer-baseline are STRUCTURAL parts of the architecture rather than properties hoped-for from a single bigger network. A monolithic transformer fuses memorization and generation in one weight set (so memorized combos and novel combos are indistinguishable); separating them into two loops is the substrate-first fix.

## Cheap test (frozen-first · $0 · numpy mirror · DIRECTIONAL)

$0 numpy: two controllers over a toy task -- goal=compositional generator, habit=lookup cache filled by consolidation count. Frozen bars: (i) novel context -> goal loop yields >=3 corpus-absent valid while routing-through-habit yields 0; (ii) G1 composed_distinct>max_single only via goal loop, drops to max_single when forced through cache; (iii) abstain AUROC(known vs novel) from cache-match ~1.0 and INVARIANT when goal-loop capacity is scaled (disjointness); (iv) emit-propensity converges to 0.5 and migrates to a boundary when either loop is deleted.

## Engine-native measure (cost-gated · PRE-REGISTER ONLY · NOT fired)

Implement the two loops as a goal-channel (core/generator.hexa compositional search) and a habit-cache (core/engine_cli.hexa associative store) with a consolidation transfer op, gated in core/emit_policy.hexa; route via cli/anima.hexa -- eval and score G0/G1/G2 + closure with core/g_gates.hexa (a7b_pass), honesty/abstain via the ImmuneMemory recall_thr in core/engine_cli.hexa. byte-parity vs the .py mirrors. Habit-route = the engine-native memorizer control arm. No torch in verdict.

## Scope / honesty (c9)

## Distinction (near-overlap kept, not a dup)

Near-overlap with dual_controller_arbiter (this census) — distinct: this is a LEARNING-TIME consolidation gradient (goal-loop output COMPILED into habit cache via the dopamine spiral), not a runtime uncertainty arbiter; the automatization gradient is the differentiator.

Closure (G0&G1&G2 co-located in the goal loop) and the structural honesty/disjointness are the claims; the consolidation transfer's effect on real-corpus capacity is scale-sensitive (a_toy_scale_recheck). Overlaps but is distinct from a runtime arbiter: this is a learning-time compilation gradient, not single-step controller selection.

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED ARCHITECTURE (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). engine_native_measure 는 단일 진입점 cli/anima.hexa → generator L3 → g_gates/g6 경유 byte-parity 채점만 terminal; torch-only/side-harness 결과는 DIRECTIONAL. numpy cheap_test 결과도 DIRECTIONAL(엔진-네이티브 아님). gpu/engine 발사 시 held-out mirror-DESCENT(a_clm_gen_pipeline) + CORE mount frozen-bar engine-native 재측정 + ckpt PULL(a_fire_recover_complete).
