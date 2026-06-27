# H_1623 — Multiplicative role-filler mouth (hypernetwork tensor-product binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `hypernet_multiplicative_bind`

## Mechanism

Leg_a is NOT concatenated/added to leg_b — instead leg_a is fed to a hypernetwork that GENERATES the weights θ(a) of the small transform applied to leg_b: out = g_{θ(a)}(b). This realizes a Smolensky role⊗filler tensor-product / bilinear interaction (multiplicative, not additive) inside one forward, with the hypernet factorization avoiding the full outer-product blowup. Binding = the dynamic re-parameterization: leg_a literally changes the FUNCTION that reads leg_b.

## Why it crosses the binding wall

conv/attention mix legs ADDITIVELY (weighted sums, softmax convex combos) — additive superposition cannot represent role⊗filler binding (the canonical 'binding problem'; AND/conjunction needs a product term). A hypernetwork injects a genuine multiplicative interaction: the same filler b produces different outputs under different roles a, which is exactly compositional generalization to UNSEEN role×filler pairs. Ablation logic: freeze the hypernet output to a constant (θ independent of a) → reverts to a static layer with additive leg-mixing → compositional-generalization collapses to memorization. The gap on the unseen-combination split is attributable solely to the multiplicative path. (Orthogonal to attention_block: attention is additive convex mixing; this is multiplicative weight-generation.)

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy ($0) — the cleanest binding probe: role-filler retrieval ('what attribute does the object selected by role-A have, per filler-B?') with a TRAIN/TEST split on UNSEEN role×filler combinations. hypernet (a→θ→applied to b) vs concat-MLP (additive baseline) vs frozen-θ ablation. PRE-REG: hypernet held-out-combo acc ≥0.95, concat-MLP ≤0.60, frozen-θ ≤0.60. Decisive = compositional split (zero overlap of train/test pairs) separates multiplicative from additive.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

(pre-reg only) 303M mouth: insert a hypernet-gated block where trunk-state a generates a low-rank weight delta applied to register/second-leg b (rank-r factorized to stay ~303M). 4-cell corpus, held-out CE, forge own-GEMM. Engine-native G6/G1 via `anima eval`; ablation arm = θ frozen to mean. Pre-reg success = hypernet arm G6 fals>0 ∧ G1≥baseline, frozen-θ arm FAIL — the cleanest causal isolation of binding to the multiplicative path. ~0.5–1 H100-day; explicit-go.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
