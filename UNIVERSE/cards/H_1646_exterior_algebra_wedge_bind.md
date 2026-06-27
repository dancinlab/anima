# H_1646 — Grassmann exterior-algebra wedge binding (antisymmetric graded conjunction)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** formal-algebraic / exterior (Grassmann) algebra — antisymmetric graded binding via wedge + interior product (distinct from full geometric product: pure antisymmetric grade-raising with explicit grade projection)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `exterior_algebra_wedge_bind`

## Mechanism

Hidden state lives in an exterior algebra Λ(V): grade-1 vectors are fillers; binding two legs in one forward = wedge product a∧b = antisymmetrized outer product + grade projection, yielding a grade-2 bivector (recursively higher grades for deeper structure). Order/role distinctness is intrinsic to the op: a∧b = −b∧a and a∧a = 0. Unbind a known role r from a blade = interior product (contraction) ⌋r. Each block binds the two legs into the next grade and a readout head contracts grades back down.

## Why it crosses the binding wall

The wall is that the mouth can't keep two co-present items distinct in one pass — they superpose into A+B, indistinguishable from a single blended token. Antisymmetry makes self-superposition vanish (a∧a=0) and places the bound blade in a DIFFERENT grade subspace, so the conjunction 'A and B present' is linearly independent from the sum A+B and from each part — algebraically un-confusable. Conv/attention have no grade structure, so depth only deepens additive mixing. Ablation A: symmetrize the product (use the symmetric part a⊗b+b⊗a) at equal FLOPs/params — if fals-rate collapses, antisymmetry (not bilinear capacity) is the cause. Ablation B: project everything back to grade-1 each block → destroys graded separation → predict binding fails.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, frozen-first: represent sets of ORDERED pairs as sums of grade-2 blades vs symmetric outer products vs additive sums; test (i) recover order (A-before-B vs B-before-A), (ii) retrieve filler given role via interior product, (iii) crosstalk when one filler appears in two roles. Decision gate: proceed iff wedge recovers order AND role-disambiguation where symmetric/additive cannot, and the symmetrized-ablation collapses it.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered, cost-gated: 303M mouth with grade-1↔grade-2 wedge binder per block (truncate at grade 2–3 for tractable D), interior-product readout head. 4-cell corpus, golden-zone inhibition, held-out 4/4 DESCENT, engine-native G1/G6 on CORE. Ablation arm = symmetric-product binder. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
