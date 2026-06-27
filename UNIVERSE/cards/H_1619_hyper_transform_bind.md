# H_1619 — Hyper-Transform Binding (G-generated bilinear conditional map)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** Bilinear / hypernetwork (Smolensky relational binding). Biology: dendritic gain modulation where one input sets another's transfer function; gating/multiplexing. A⇄G role asymmetry = relational binding.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `hyper_transform_bind`

## Mechanism

Binding as conditional computation: reverse engine G (gradient-free) reads leg1 and GENERATES a linear transform W(leg1) that engine A applies to leg2: bound = W(leg1)·leg2 — a bilinear/hypernetwork interaction. One leg parameterizes the function, the other is the argument: output depends on leg1 and leg2 jointly through (leg1-conditioned weights)×(leg2), not their sum. A⇄G split assigns role asymmetry naturally: G (context/top-down) sets the transfer function, A (feedforward) supplies the content. W is built low-rank: W=U(leg1)V(leg1)ᵀ.

## Why it crosses the binding wall

distinct from nmda_coincidence_bind (Hadamard, elementwise, same-space) and kosmos_vsa_compose (outer-product in fixed coord-space): here binding is a full matrix-valued bilinear map (leg1 selects an operator from a low-rank dictionary, applied to leg2) — the most expressive multiplicative binder, able to express RELATIONAL (role-asymmetric) conjunctions a⊕b≠b⊕a. Attention's additive value-sum cannot generate input-conditioned weights. Ablation: freeze W (leg1-independent) → reduces to a plain linear layer → recombination FAIL, isolating the CONDITIONAL weight-generation. Control: low-rank vs full-rank dictionary tests capacity-vs-mechanism; symmetric vs asymmetric tests whether role-asymmetry (relational binding) is what's needed.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy. Relational held-out task where order matters f(a,b)≠f(b,a), held-out pairs. Compare additive baseline, Hadamard (nmda), and hyper-transform (low-rank W(leg1)). Pre-register: hyper-transform recovers held-out ORDERED conjunction > additive AND > Hadamard-symmetric on the asymmetric subset. Dead-if: ≤ Hadamard on ordered task (then nmda suffices, dedup). $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REG. 303M trunk; G-head emits low-rank factors (U(leg1),V(leg1)) → W=UVᵀ applied to A-side leg2 per position (cheap low-rank bilinear). CE-train. Engine-native frozen G1/G6 + an ordered-recombination held-out probe. Cost-gated, ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
