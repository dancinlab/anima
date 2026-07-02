# H_1609 — Gain-Field Coordinate-Transform Mouth (full outer-product bilinear basis)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** parietal gain fields / basis-function binding (Andersen; Pouget-Sejnowski; Salinas-Abbott) — multiplicative coordinate-transform binding.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `gain_field_basis`

## Mechanism

One leg (context/state, leg-B) multiplicatively GAINS the tuning of the other leg's feature units, yielding an explicit outer-product basis b_{ij} = phi_i(A) * psi_j(B) — a FULL bilinear / tensor-pooling map (not the diagonal Hadamard of dendritic_coincidence) — forming a population of gain-modulated basis-function units. A linear readout over this product space computes arbitrary functions of (A,B), including coordinate transforms. Binding = the full off-diagonal outer-product basis present in one forward (factorized low-rank for feasibility).

## Why it crosses the binding wall

gain-field basis-function theory (Pouget-Sejnowski; Salinas-Abbott): an outer-product basis lets a LINEAR readout approximate any function of two variables — the universal substrate for binding/coordinate transforms. attention value-combination and conv are additive (rank-collapsed). The outer product is full-rank bilinear, strictly more expressive than the diagonal (Hadamard) gate and than additive mixing. Ablation cleanly tiers the cause: (a) restrict the bilinear to its diagonal (= Hadamard) -> loses off-diagonal cross-terms, PARTIAL fail; (b) drop to additive -> FULL fail. The strict gap full-outer < diagonal < additive attributes binding to the OFF-DIAGONAL product terms specifically.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, DIRECTIONAL. coordinate-transform toy: target = readout of f(A,B) needing off-diagonal terms (a rotation/lookup that is NOT diagonal-separable). full outer-product basis vs Hadamard-diagonal vs additive, equal readout, 25% held-out combos. Frozen bar: outer held-out CE < 0.2 nats; Hadamard intermediate; additive >= 0.9x uniform — pre-register the strict ordering outer < diag < additive. (outer is O(d^2): pre-register a low-rank factorization r<<d to keep 303M feasible.)

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M with a factorized low-rank (r~64) bilinear gain-field block at mid-depth (trunk-summary gains token features); CE-trained; engine-native G1/G6; bars frozen. ~$15; ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
