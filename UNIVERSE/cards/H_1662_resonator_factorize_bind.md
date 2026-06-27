# H_1662 — Resonator-Network Factorization Mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** formal-algebraic: resonator-network factorization / VSA unbinding as an in-forward alternating fixed point
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `resonator_factorize_bind`

## Mechanism

The bind block holds a bound state s = bind(a,b) (elementwise/circular product of two factor estimates) and runs a few resonator iterations INSIDE the forward pass: â ← cleanup_A(s ⊘ b̂); b̂ ← cleanup_B(s ⊘ â), where ⊘ is the exact algebraic unbind and cleanup_X = softmax projection onto a learned factor codebook (256 entries). The mutually-constraining fixed point disentangles the conjunction; readout conditions on (â, b̂, s). The two legs are the two factor estimates coupled through the shared bound product.

## Why it crosses the binding wall

The core generation-binding problem is INVERTING a bound conjunction to recover its parts — attention never inverts a product, it only mixes. Resonator exploits the exact invertibility of the binding operator plus a discrete codebook constraint to factor the conjunction within one forward, letting the mouth emit conditioned on the actual (role,filler) pair rather than their blur. Ablation: replace codebook cleanup with identity (no discrete constraint) → iterations diverge/collapse to mean → fals→0; freeze to 0 iterations → equals the plain product = the already-FAIL bytegpt baseline, so any lift is attributable to the factorization dynamics. Distinct from energy_settle/deq: it is NOT scalar-energy gradient descent but per-factor algebraic unbind + codebook projection (alternating Gauss-Seidel), which is precisely what makes the factorization tractable in O(few steps).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. D=512 bipolar HRR; bind 3 factors from codebooks of size 16 each (4096 combos), hold out 25%. Run resonator decode on held-out bound vectors; measure factor-recovery accuracy vs single-shot (0-iter) decode. PASS = resonator recovers held-out conjunctions while 0-iter stays at chance → factorization is the crosser.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY (cost-gated): 303M mouth = trunk emits two factor heads a,b (D=512 bipolar/phasor) → circular-conv bind → 3 resonator steps with learned 256-entry codebooks → concat(â,b̂,s) → readout→V256. Gates = held-out CE-DESCENT + engine-native G1/G6 on CORE. Ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
