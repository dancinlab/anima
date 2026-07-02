# H_1675 — Fractional-Power-Encoding mouth (Spatial-Semantic-Pointer binding)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** FORMAL-algebraic -- continuous unitary group action / fractional convolution power (SSP/FPE VSA, Komer-Eliasmith-Frady)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `fractional_power_encoding_bind`

## Mechanism

Trunk emits per-position a unit-modulus phase vector (components are phases of a fixed base unitary's eigendecomposition). Binding two legs A (role/context) and B (filler/token) is ELEMENTWISE COMPLEX EXPONENTIATION: z = exp(i*(s_A*theta_A + s_B*theta_B)) -- raise a base vector to continuous fractional powers given by the two legs and multiply (fused FFT -> phase-add -> iFFT, or direct complex elementwise). Unbind = exponentiate by negative power. One fused forward op; binding is associative and unitary-invertible (lives on the torus).

## Why it crosses the binding wall

Conv-trunk/L24 attention superpose features ADDITIVELY (A+B), so the pair is not recoverable as a factorizable product -- novel role-filler recombination is impossible because no forward operator maps (A,B)->a deconvolvable single vector. FPE binding is a CONTINUOUS unitary group action: the bound state is one point on the torus, the exact pair recovers by inverse power in one step, and unseen combinations are valid points on the SAME manifold (compositional generalization built into the group, not learned from co-occurrence). Distinct from HRR (integer circular conv): the fractional/continuous power gives a kernel over combinations. ABLATION: replace fractional exponentiation with additive superposition (s->0) -> reverts to bag-of-features, G6 fals->0 returns; replace continuous power with integer power -> loses novel-combination smoothness (degrades toward discrete HRR), recombination of unseen pairs falls.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy $0, <1min CPU. V=64 symbols as random unit base vectors (d=256). Encode 200 role-filler pairs by FPE; store superposition (sum) of bound vectors. Query: unbind by a role, nearest-neighbor recover filler. FROZEN bar: recovery accuracy on HELD-OUT pairs (role x filler combos never co-bound in stored set) >= 0.8 AND additive-superposition control = chance (1/64). FPE held-out >=0.8 while additive control ~chance => mechanism provides novel-pair binding the additive baseline cannot.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY, cost-gated ~1 H100-day. 303M custom mouth: replace ConvMoE expert mix with FPE-binding block -- per layer split hidden into (phase, magnitude); learned linear maps token+context to fractional powers s; binding via batched FFT phase-add. Train on 4-cell balanced corpus (a_chat_registers, fail-loud effective bytes). Frozen acceptance = engine-native (cli/anima.hexa eval) G6 fals>0 AND G1 recombination >= ConvMoE baseline on held-out. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
