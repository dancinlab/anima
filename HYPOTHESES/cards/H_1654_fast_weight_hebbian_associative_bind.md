# H_1654 — Fast-Weight Hebbian Associative Binding (write-then-settle)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** DYNAMICS — synaptic fast-plasticity (Hebbian write + inner relaxation)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `fast_weight_hebbian_associative_bind`

## Mechanism

Within ONE forward: leg A is written into a transient per-sequence fast-weight matrix S by a Hebbian outer-product rule S = Σ_i η · a_i k_i^T (no learned generator — S is created on the fly). Then leg B is injected as a query and the hidden state is iterated for S-steps under h ← LayerNorm(h_slow + S h) (Ba et al. inner relaxation), so B retrieves and RECOMBINES whatever A deposited. The fast weights ARE the binding substrate; the settle loop resolves the conjunction.

## Why it crosses the binding wall

the binding is held in a QUADRATIC (rank-accumulated) per-sequence memory and resolved by a MULTI-STEP settle — neither expressible by a fixed-weight conv/attention layer (attention's QK is a single softmax read: one Hebbian read, zero relaxation). Distinct from hypernet_multiplicative_bind (weights are produced by a LEARNED feedforward net, a deterministic function of input, with no online Hebbian accumulation and no inner settle) and from tpr_outer_bind (keeps the outer product AS the representation; here the outer product becomes a TRANSFORM applied iteratively). ABLATION: settle steps=0 (read S once) → reduces to linear-attention assoc read, binding weak; η=0 (no Hebbian write) → no memory, fals collapses. Both-off = baseline, both-on = pass → isolates write+settle jointly.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy associative-recall toy: write K random (key,value) pairs as leg A via Hebbian outer products, then probe with leg B. (1) recovered-value MSE after 0 vs S=3 settle iterations; (2) COMPOSITIONAL probe — query with a novel composed key (sum of two written keys) and check retrieved value equals the corresponding value composition. Pre-registered bar: S=3 settle cuts compositional-probe error ≥ 40% vs S=0 AND beats additive baseline. $0 numpy.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated 303M): insert a fast-weight associative layer after the trunk — per-frag Hebbian write of the first-leg span, then S=2-3 settle iterations over second-leg positions. Train 4-cell corpus, held-out CE monitor. Verdict = ckpt PULL → CORE --engine conv engine-native G1/G6; bar fals>0 ∧ recombine ≥ baseline.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
