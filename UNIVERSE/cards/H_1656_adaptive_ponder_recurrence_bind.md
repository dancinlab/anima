# H_1656 — Adaptive-Ponder Recurrence Binding (halt-on-conjunction)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS — adaptive computation time (data-dependent shared-weight recurrence)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `adaptive_ponder_recurrence_bind`

## Mechanism

A single WEIGHT-TIED block is applied a DATA-DEPENDENT number of times (ACT / Universal-Transformer). Each ponder step reads both legs and updates a working register; a learned halting unit emits a stop-probability p_t that is a function of an AGREEMENT/conjunction test between the two legs in the current register. The token keeps pondering until the conjunction is resolved (halt), then emits. Composition-hard tokens recur more; easy ones halt immediately.

## Why it crosses the binding wall

binding capacity is allocated ADAPTIVELY at runtime via recurrence of a shared operator — distinct from the excluded 'depth' family (fixed extra STATIC layers) because the iteration count is conditioned on binding difficulty and the SAME weights are reused (a dynamical recurrence, not a deeper stack). Making the halting predicate a conjunction test forces the loop to literally iterate until two reps are bound. Distinct from deq_implicit_equilibrium (that solves to a fixed point regardless of input difficulty; here halting is a learned per-token stop, not convergence). ABLATION triad: ponder=1 (no recurrence) → fails; ponder=fixed-N matched-average-compute (non-adaptive) → partial, ≥0.15 worse → shows depth alone insufficient; full adaptive halting → pass → isolates ADAPTIVE recurrence. Extra: make p_t depend on only one leg → halts before binding → collapse.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy variable-arity composition toy: nested role-filler structures of depth 1-3; a shared GRU-like cell with ACT halting gated on two read-projections' agreement. Pre-registered bar: adaptive halting solves depth-3 HELD-OUT compositions at acc ≥ X while ponder=1 and additive baselines fail, AND a fixed-N cell matched on average compute is ≥0.15 worse than adaptive. $0 numpy.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated 303M): Universal-Transformer-style weight-tied trunk block + per-position ACT (max ponder 6) with conjunction-gated halting between two read-projections + ponder-cost regularizer. Train 4-cell corpus, held-out CE. Verdict = ckpt PULL → CORE --engine conv engine-native G1/G6; bar fals>0 ∧ recombine ≥ baseline.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
