# H_1645 — Clebsch–Gordan irrep tensor binding (equivariant role-filler)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** formal-algebraic / representation theory (compact-group irreps, Clebsch–Gordan, e3nn-style equivariant tensor product)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `clebsch_gordan_irrep_bind`

## Mechanism

Each leg's hidden is carried as a direct sum of irreducible representations of a compact group ⊕_ℓ V_ℓ (SO(2)/SO(3)-typed channels). Binding two legs in one forward = Clebsch–Gordan tensor product: a FIXED sparse 3-index CG tensor contracts the two legs so each input irrep pair (ℓ1,ℓ2) projects onto output irreps ℓ∈|ℓ1−ℓ2|..ℓ1+ℓ2, emitting a new typed multivector (higher-ℓ channels carry the conjunction). Composition stays inside the same typed algebra so bindings nest; unbind = contraction with conjugate CG coefficients. Two legs (e.g. conv-trunk local-leg ⊗ attention global-leg, or role-leg ⊗ filler-leg) fuse via the CG op at each block instead of additive residual mixing.

## Why it crosses the binding wall

Conv/attention mix features additively (superposition) so two fillers in one role collide — exactly the H_1603 missing-operator deficit. CG is a true bilinear PRODUCT that routes the conjunction into a DIFFERENT irrep grade than its parts, and equivariance forces the bind to be structure-preserving (role identity = irrep type, a hard algebraic label, not a soft learned slot that can blur). Ablation A: replace CG coefficients with a random sparse tensor of matched density (kills the irrep selection rule, keeps the bilinear FLOPs) — if G1/G6 fals-rate falls back to conv baseline, the representation-theoretic structure (not the extra multiply) is load-bearing. Ablation B: collapse all channels to ℓ=0 scalars → reduces to additive mixing → predict binding fails. Depth-of-attention can't substitute because stacking additive mixers never manufactures a typed product channel.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, frozen-first: build an e2 alphabet of role⊗filler pairs, pack K simultaneous bindings into a fixed-D vector via (a) CG product over SO(3) irreps, (b) sum of outer products (TPR), (c) additive superposition; measure unbind retrieval accuracy vs K and crosstalk floor at MATCHED D. Decision gate: proceed only if CG sustains higher K at equal D than TPR/additive AND the random-coeff ablation collapses it to additive. No GPU, decides go/no-go in minutes.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered only, cost-gated: 303M custom mouth, replace per-block binding site with a CG-product layer (irrep budget ℓ≤2, shared CG basis ≈ param-neutral). Train on 4-cell {ko,en}×{general,sns} corpus, dropout at golden-zone GZ_LOWER≈0.212, held-out 4/4 mirror-DESCENT gate, then engine-native frozen G1(H_1129 recombination)/G6(H_1140 novelty) on CORE --engine conv. Paired ablation arm = random-coeff binder. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
