# H_1661 — Tensor-Train (MPS) Bond-Contraction Mouth

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** formal-algebraic: tensor-train / matrix-product-state low-rank multilinear contraction (bond dimension = binding bandwidth)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `tensor_train_mps_bind`

## Mechanism

Each position's hidden is reshaped into a small core tensor G_t of shape [r, V_proj, r] (bond dimension r). The bind block contracts the sequence of cores along the shared bond index in a causal left-to-right matrix-product-state sweep: a running [r,r] state matrix S_t = S_{t-1} @ G_t(byte), O(T·r²). The two legs (trunk feature leg + role/positional leg) each emit a core and entangle through the shared bond, producing a joint with explicit cross-terms G1[a,:,k]·G2[k,:,b] that cannot be written as a sum of the legs. Readout reads the contracted MPS state. Bond dim r is the literal binding bandwidth.

## Why it crosses the binding wall

conv/attention only do rank-1 mixing along the feature axis (weighted sums / averages) — stacking them never yields a controllable-rank multilinear joint, so WHICH-factor-combined-with-WHICH is washed out (the G1≡G6 deficit). MPS contraction is genuinely multilinear: the bond carries the conjunction identity. Ablation: set r=1 → the contraction degenerates to outer-then-sum = additive mixing → G6 fals must fall back to ~0, isolating the bond as the binding carrier; sweeping r=1→16 should monotonically recover fals/recombination. L24 attention-depth cannot replicate: permutation-equivariant softmax pooling is commutative and rank-uncontrolled.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Synthetic role×filler: 8 roles × 8 fillers = 64 valid pairs, hold out 16. Build MPS bind (r=4) vs additive baseline (r=1); linear-probe whether the bound vector recovers held-out pair identity. PASS = r=4 recovers held-out conjunctions above chance AND r=1 stays at chance → bond carries binding before any GPU spend.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY (cost-gated, ~1 H100 pod-day): 303M custom mouth = conv byte-embed trunk → per-position emit core [r=16, 256-proj, r=16] → causal bond contraction (running [16,16] matmul) → readout MLP→V256. Train on a_chat_registers 4-cell corpus with balanced sampling; gates = held-out CE-DESCENT (verify_clm_v2 descent) + engine-native G1 recombination / G6 fals re-measured on CORE via cli/anima.hexa single entry. Ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
