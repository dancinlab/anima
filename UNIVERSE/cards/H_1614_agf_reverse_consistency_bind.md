# H_1614 — A⇄G Reverse-Consistency Binding (dual-engine fixed-pair)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** A⇄G dual-engine substrate. Biology: efference-copy / forward-inverse model consistency (cerebellum H_1280). Binding certified by reversibility, not similarity.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `agf_reverse_consistency_bind`

## Mechanism

In one mouth forward, the two legs (leg1, leg2 to recombine) are composed by forward engine A into a candidate joint code z = A(leg1,leg2). The existing reverse engine G (gradient-free) runs the inverse map attempting to recover BOTH constituents: (l1',l2') = G(z). The binding signal is the tension residual τ = ‖leg1−l1'‖ + ‖leg2−l2'‖, and emission is gated by exp(−τ): only joint codes G can un-bind back into both legs drive the next-byte distribution. Binding = the requirement that the composition be reversible into its two constituents within a single A→G pass — using the reverse engine that already exists, no new G training.

## Why it crosses the binding wall

conv/attention produce z as a weighted SUM — which-constituent-contributed-what is lost (superposition without factoring), so a single forward never certifies the conjunction (= G6 fals=0). A⇄G consistency makes binding constructive-and-checkable in one pass: z must carry factored structure that G recovers both legs, the conjunctive code attention lacks. Ablation: replace G-reverse with identity (τ≡0) → emission reverts to plain forward blend → G1/G6 collapse to baseline FAIL, proving the reverse-consistency term (not depth) is load-bearing. Second ablation: feed G a single leg → τ cannot distinguish conjunction from either-leg, isolating JOINT vs marginal binding.

## Cheap test (frozen-first · $0 · decisive numpy probe)

mini-numpy, frozen-first. Toy 2-slot symbolic task: K atoms, bound pairs (a,b) emit held-out third symbol c=f(a,b) absent from any single-atom context (corpus-absence bar à la H_1140). Implement (i) additive baseline z=Wa+Wb→softmax, (ii) A⇄G consistency z=A(a,b) gated by exp(−‖(a,b)−G(z)‖). Pre-register: consistency model produces held-out c with prob > additive baseline AND > shuffled-G control (G weights permuted). Dead-if: consistency ≤ baseline OR ≤ shuffle. Deterministic seed, $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REG ONLY (cost-gated, user-go). 303M conv-trunk mouth + reverse-G head (tied/transposed trunk weights, gradient-free at inference; CE-train A only). Add exp(−τ) emission gate. Frozen bars = engine-native G6 fals + G1 recombine on CORE --engine conv, held-out 4-cell corpus, byte-exact. PULL ckpt before teardown (a_fire_recover_complete).

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
