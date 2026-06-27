# H_1621 — Deep-equilibrium implicit-coupling mouth (root-of-equation binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `deq_implicit_equilibrium`

## Mechanism

A single weight-tied layer f defines an IMPLICIT equation z = f(z, a, b) where f contains a bilinear coupling term between the two legs (e.g. f = σ(Wz + U_a a + U_b b + a⊙(V z) routed by b)). The mouth output is the root z* solved by Anderson/Picard iteration to convergence (not a stack of distinct layers). The two legs are bound because z* is the simultaneous solution of a coupled nonlinear system — neither leg's contribution is resolvable independently; the fixed point is the algebraic intersection of both constraints.

## Why it crosses the binding wall

This is distinct from the (excluded) 'depth' family in principle: depth = stacking N DISTINCT learned layers (finite expressivity, additive residual mixing); DEQ = solving for the ROOT of one coupling operator (effectively unbounded, adaptive iterations; binding = implicit-function-theorem solution, not a transform chain). A finite feedforward stack cannot represent the fixed point of an arbitrary coupled system, but the equilibrium solver can. Ablation logic: cap solver iterations to 1 → reduces to one feedforward layer (NOT a deep net) → binding collapses; the gap between 1-iter and converged isolates binding to the implicit coupling, and a SECOND ablation (drop the bilinear cross-term, keep iterations) shows additive-only equilibria also fail — proving the cross-term, not mere iteration, is load-bearing.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy ($0): solve z=tanh(Wz + U_a a + U_b b + (a⊙Vz)) by 50 Picard iters vs 1 iter vs (50 iters, cross-term zeroed). Task = held-out conjunction retrieval over two legs. PRE-REG bars: converged DESCENT (CE < shuffle); 1-iter NO-DESCENT; cross-term-off NO-DESCENT even at 50 iters. Decisive = only the (converged ∧ cross-term-on) cell descends — double dissociation pins binding to implicit coupling.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

(pre-reg only) 303M mouth: last 4 conv/attn blocks → 1 DEQ block (Anderson solver, ≤12 iters, bilinear leg-coupling), param-matched. Same 4-cell corpus, held-out CE, forge own-GEMM. Engine-native G6/G1 via `anima eval`. Ablation arms at eval: iters=1, and cross-term masked. Pre-reg success = converged arm G6 fals>0 ∧ G1≥baseline, both ablation arms FAIL. Backward = implicit-grad (1-step Neumann) to keep memory flat. ~1 H100-day; explicit-go gated.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
