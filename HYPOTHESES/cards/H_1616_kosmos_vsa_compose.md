# H_1616 — Kosmos Placement-Space VSA Binding (tensor / circular-conv role-filler)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** Algebra-first: VSA/HRR (Plate), tensor-product variable binding (Smolensky). Substrate: kosmos placement-coord field as binding+cleanup space. a_no_llm_frame_trap — algebraic, not scale.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `kosmos_vsa_compose`

## Mechanism

Each leg maps to a high-dim vector in the existing kosmos placement coord-space. Binding uses an ALGEBRAIC vector-symbolic operator: bind(a,b)=a⊛b (circular convolution / HRR) or role⊗filler tensor product — invertible, producing a vector dissimilar to both operands yet from which either is recovered by unbinding (a⊛b⁻¹≈b). The mouth composes constituents by ⊛ in coord-space, accumulates a bundle (superposition) for multi-pair context, and decodes the next byte by cleanup-memory nearest-anchor lookup over the .kosmos field. Unbinding at read-out gives compositional recall.

## Why it crosses the binding wall

this is the canonical algebraic solution to the binding problem (Plate HRR / Smolensky tensor-product variable binding). Attention's additive weighted sum cannot represent role-filler conjunctions invertibly (a+b loses which-role); circular convolution can — bind then unbind recovers constituents, exactly the operation conv/attention lack. Distinct from corpus_register (training-data buckets) and binding_lane (side lane): here the operator is the in-forward compose op over kosmos coords, decoded via existing anchor cleanup. Ablation: replace ⊛ with + (bundle without bind) → role info lost, held-out recombination → chance, isolating the binding operator (not the high-dim space). Control: random fixed permutation vs structured ⊛ → tests whether invertibility (not just nonlinearity) carries it.

## Cheap test (frozen-first · $0 · decisive numpy probe)

pure numpy HRR — cheapest, most decisive. d=512 random anchors for K atoms; encode pairs by circular conv (FFT); bundle; query held-out (a,b)→c via unbind+cleanup. Frozen bar: top-1 cleanup of held-out conjunction > additive-bundle baseline AND > random-permutation control. Dead-if: ⊛ ≤ additive. Deterministic, $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REG. 303M mouth where trunk penultimate projects to d≈2048 HRR coord; compose = FFT circular conv; cleanup = learned anchor codebook (kosmos field). CE-train projector+codebook. Engine-native: serialize codebook into .kosmos, decode via kosmos_io→brain_decide. Frozen G1/G6. Cost-gated, ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
