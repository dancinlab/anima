# H_1663 — Non-Commutative Braid/Permutation-Group Binding Mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** formal-algebraic: non-commutative group action — braid/permutation-group binding preserving role order
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `braid_permutation_group_bind`

## Mechanism

Binding is a NON-commutative group action. Each role applies a learned permutation/braid generator σ_role (an element of S_D or the braid group B_n, parameterized as a product of Householder/Givens rotations or a Sinkhorn soft-permutation) to its filler vector before summation: h = Σ_role σ_role(f_role). Because braid generators do not commute (σ_i σ_j ≠ σ_j σ_i for |i−j|<2), the bound state distinguishes (role1∘role2) from (role2∘role1). Two legs combine as group_element(leg_role) acting on leg_filler in one forward.

## Why it crosses the binding wall

Commutative binding (circular conv, addition, XOR) loses role asymmetry: 'agent eats patient' ≡ 'patient eats agent' — exactly the recombination failure where a filler's slot is unrecoverable. A non-commutative permutation/braid action preserves the role↦slot assignment, so readout can reconstruct ordered structure → systematic recombination (G1) and falsifiable conjunctions (G6). Ablation: replace braid generators with identity (or one shared permutation across roles) → commutative bag-of-fillers → G1/G6 collapse, isolating non-commutativity as the carrier. Attention-depth cannot: softmax value-pooling is permutation-equivariant (commutative), so L24 never breaks the symmetry.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Ordered-pair task: 8 symbols, encode ordered (a,b) as P_role1·e_a + P_role2·e_b with fixed random permutation matrices; train linear readout to recover ORDER on held-out pairs. PASS = permutation-bind recovers which symbol came first while commutative encode (e_a+e_b) is at chance → non-commutativity carries binding.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY (cost-gated): 303M mouth = conv trunk → K learned role operators (Givens/Householder products, orthogonal-by-construction) applied to per-position filler projections, summed → readout→V256. Gates = held-out CE-DESCENT + engine-native G1/G6 on CORE. Ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
