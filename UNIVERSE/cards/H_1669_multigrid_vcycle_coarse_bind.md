# H_1669 — Multigrid V-cycle coarse-grid binding solver

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** numerical multigrid / multiscale PDE-relaxation dynamics
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `multigrid_vcycle_coarse_bind`

## Mechanism

Replace the stacked-layer trunk with a multiscale V-cycle relaxation. The two legs (e.g. conv-trunk content stream + attention-derived role stream) live on a fine grid of positions/features. One forward = (a) a few cheap local smoothing iterations on the fine grid; (b) RESTRICTION: pool the residual of the binding equation r = bind(legA,legB) - out down to a coarse grid (few, broad units whose receptive field is the whole sequence); (c) recursively SOLVE the coarse problem where the two legs interact GLOBALLY in one shot; (d) PROLONGATE the coarse correction back up and add; (e) post-smooth. The quantity being relaxed to zero is explicitly the cross-leg consistency residual, so the conjunction is carried across scales rather than hop-by-hop.

## Why it crosses the binding wall

L24 attention propagates one hop per layer and still must learn to route a specific conjunction through generic softmax mixing — it doesn't (H_1394/1590/1598). Multigrid carries the binding-equation RESIDUAL across scales: the coarse-grid solve satisfies the global component of the conjunction in O(1) cycles instead of waiting for it to emerge from depth, decoupling binding-range from layer count. Ablation: set restriction depth=0 (pure fine smoothing = plain recurrent conv) → residual plateaus at the depth-only FAIL level; restore coarse levels → residual→0. Second ablation: drop the cross-leg term from the residual (relax only legA) → coarse solve degenerates to a smoother, no binding — isolates that the coarse global coupling, not the extra compute, is causal.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Synthetic 1-D binding task: random factor vectors a,b at random positions; target recoverable only by combining both. Tiny linear V-cycle (Jacobi smoother + fixed restriction/prolongation, 3 levels) vs matched-flop single-scale relaxation of equal total iterations. Pre-register: V-cycle binding-residual < single-scale by >=10x at equal flops AND single-scale plateaus above zero. Falsified if single-scale matches.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY (cost-gated, user-go). 303M custom mouth: 24-block trunk -> 8-block x 3-level V-cycle (restriction = strided pool x4, prolongation = learned upsample); loss = next-byte + auxiliary cross-leg consistency between conv-content and attention-role streams. Train on clean 4-cell corpus; held-out CE-descent gate (verify_clm_v2 descent) + engine-native G1/G6 re-measure on CORE --engine conv; ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
