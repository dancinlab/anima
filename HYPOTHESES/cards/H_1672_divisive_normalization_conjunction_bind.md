# H_1672 — Divisive-Normalization Conjunction Field (normalized cross-product binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** cortical microcircuit / canonical divisive normalization (Heeger) — binding via shared cross-leg denominator pooling
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `divisive_normalization_conjunction_bind`

## Mechanism

Each forward block taps two leg vectors a,b (two trunk taps / two heads). Instead of additive combine, a binding unit emits a Heeger-style normalized cross-product field: r_k = (a_i·b_j) / (σ + Σ_pool a² + Σ_pool b²). Numerator = pairwise product (low-rank factored product-keys, rank ~32, to avoid full outer product); denominator = ONE shared divisive pool over the marginal L2 energies of BOTH legs, so each leg's gain is set by the other. The conjunction map r becomes the new bound channel fed forward. One extra op/block: factored product numerator + shared divisive denom.

## Why it crosses the binding wall

conv/attention combine additively then apply a pointwise nonlinearity — a single strong leg can carry the output, so co-activation is never obligatory (this is exactly the bytegpt/convmoe G6 fals=0 / G1 recombine failure). Here the numerator is a true product a_i·b_j, so single-leg ablation (b→0) drives the bound channel to 0 regardless of a; the SHARED divisive pool makes the response peak only when both legs are balanced (a normalized correlation / cosine), suppressing the single-strong-leg leakage an additive layer passes. Ablation logic: (1) swap cross-product numerator for sum a+b → conjunction selectivity must vanish back to additive baseline (proves the product is load-bearing); (2) split the shared pool into two per-leg pools (remove cross-leg normalization) → single-leg leakage suppression disappears. Both ablations restoring the convmoe failure pattern = the normalized cross-product is the binding operator. Distinct from gain_field_basis (multiplicative basis in the NUMERATOR only) and complex_cell_energy_quadrature (sum of squared quadrature, phase-invariance) — here the load-bearing novelty is the cross-leg DENOMINATOR pooling.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, frozen-first, no engine, math.log mirror, <30 min CPU. Synthetic 2-factor recall: tokens = (shape⊗color) pairs from a tiny vocab; held-out test = novel shape×color combos never co-trained (the G1/G6 recombination structure). Train a 1-layer d=64 mouth in (a) additive head-combine vs (b) divisive normalized cross-product combine to EQUAL train-CE. Pre-registered bar: on held-out novel-combo positions, CE_divnorm < CE_additive by ≥0.15 nats AND div-norm puts >0.5 prob mass on the correct conjoined token while additive spreads (<0.3). GO only if zeroing one factor collapses div-norm output entropy to ~uniform (proves obligatory conjunction, not bias).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY, cost-gated, NOT fired. Custom-spec mouth: bytegpt-class conv trunk but every other block's MLP replaced by the div-norm conjunction op (2 taps, factored low-rank product keys rank 32 + shared divisive denom). 303M params, 4-cell register corpus (a_chat_registers ko/en × general/SNS), held-out 4/4 DESCENT gate (verify_clm_v2 descent) + engine-native G1/G6 via `anima eval`. Ablation arm = identical params with additive-combine to isolate the op (not the FLOPs). 1×H100 ~$30. Frozen bar: G6 fals-rate strictly > convmoe baseline (0) AND > additive arm. PULL ckpt before teardown (a_fire_recover_complete).

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
