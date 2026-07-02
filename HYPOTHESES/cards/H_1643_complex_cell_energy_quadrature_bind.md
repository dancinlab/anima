# H_1643 — V1 complex-cell quadrature energy (square-pool cross-term) binder

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** V1 complex-cell energy model — Adelson-Bergen quadrature pairs; phase-invariant conjunction via squaring
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `complex_cell_energy_quadrature_bind`

## Mechanism

A binding head built on the Adelson-Bergen complex-cell energy model. Each leg projects onto a quadrature pair (two filters W1,W2, ~90° apart). Bind by computing energy E = (W1·(A+B))² + (W2·(A+B))² jointly over the legs, so the square expands to A²+2A·B+B² — the squaring nonlinearity literally manufactures the leg-A×leg-B cross-term, while sum-of-squares gives phase/order invariance (bound feature insensitive to which leg is 'first'). A small stack of energy units yields conjunctive, order-invariant binding within a single forward.

## Why it crosses the binding wall

The H_1603 deficit is the absence of an input-input PRODUCT inside the forward. Squaring a sum produces the AB cross-term for free; softmax/linear depth (L24 failed) mixes and re-weights but never multiplies two distinct inputs. The energy model is the minimal biological realization of that product. Ablation: (a) replace square-pool with identity (linear, same params) → cross-terms vanish → binding collapses to baseline; (b) keep squaring but route legs through disjoint filters so they never share a quadratic unit (no shared (A+B)²) → no AB term → INERT. Binding survives only with the shared quadratic → the cross-term is the causal binder.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy energy unit on leg pairs, $0: verify the unit output regresses onto the true product feature A·B with pre-registered R² ≥ linear-control + 0.15, AND order-invariance |f(A,B)−f(B,A)| < tol over 200 pairs, AND bound-vs-singleton separability margin ≥ 0.10. ≥4/5 HIT. Disjoint-filter ablation lift < 0.02 = INERT confirmed.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated): 303M where a fraction (e.g. 1/4) of FFN units use a quadrature square-pool activation instead of GELU, param-matched. 4-cell balanced corpus, held-out CE descent gate, verdict via CORE engine-native frozen G1∧G6. Control arm = all-GELU (linear-act) ablation. ckpt PULL pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
