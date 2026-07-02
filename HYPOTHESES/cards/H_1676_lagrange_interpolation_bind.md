# H_1676 — Lagrange-Interpolation (evaluation<->interpolation duality) mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** FORMAL-algebraic -- polynomial evaluation<->interpolation duality / Reed-Solomon-Shamir Vandermonde isomorphism
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `lagrange_interpolation_bind`

## Mechanism

Two legs play dual roles via the Vandermonde transform. Leg-1 (role/position) selects an evaluation node x_k from a fixed node set; leg-2 (filler/token feature) is the value y_k. Forward 'bind' computes the coefficient vector of the unique degree-<n polynomial through all current (x_k,y_k) pairs (single matmul by inverse Vandermonde = interpolation operator). The composed object is the COEFFICIENT vector -- it holds ALL role-filler pairs simultaneously. 'Unbind'/read at role x_j = evaluate the polynomial at x_j (one dot with the Vandermonde row). Both directions are single fused linear ops baked into the layer.

## Why it crosses the binding wall

Realizes binding as the evaluation<->interpolation ISOMORPHISM (algebraic core of Reed-Solomon / Shamir secret-sharing): n pairs are losslessly packed into n coefficients and any pair is exactly recoverable, INCLUDING combinations never trained together (the polynomial through an unseen value at a node is well-defined). Generic attention routes but cannot guarantee exact-recovery -- it averages overlapping keys. Distinct from parity_check_syndrome (decoding) and from all product-binders: this is functional packing, not a product. ABLATION: replace inverse-Vandermonde with a learned dense matrix (no Vandermonde structure) -> exact unbinding breaks, recombination collapses to baseline; replace polynomial eval read with softmax attention -> overlapping nodes blur, fals->0 returns. The Vandermonde structure is load-bearing.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy $0, <1min. n=32 random nodes; embed V symbols as scalar values. Interpolate 32 role->value pairs into coeffs, read every node; also read a HELD-OUT reassignment (swap two fillers across roles). FROZEN bar: read-back exact (MSE<1e-6) for interpolation operator AND for novel swaps, while a learned-dense control trained on the training assignments fails (>10x MSE) on swapped held-out. Structured-exact & dense-control-fails-on-novel => interpolation gives compositional binding, dense routing does not.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY, cost-gated ~1 H100-day. Custom 303M mouth: each block has a FIXED Vandermonde interp/eval pair around a learned value/node projection (roles = learned node embeddings, snapped to a fixed node grid via straight-through). Train 4-cell corpus. Accept iff engine-native (cli/anima.hexa eval) G6 fals>0 AND G1 recombination >= baseline on held-out. ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
