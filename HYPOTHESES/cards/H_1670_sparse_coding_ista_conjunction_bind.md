# H_1670 — Unrolled-ISTA shared-code conjunction binding

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** sparse coding / compressed-sensing proximal-gradient inference dynamics
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `sparse_coding_ista_conjunction_bind`

## Mechanism

Mouth forward = iterative sparse inference (proximal soft-thresholding / ISTA) for ONE shared latent code z that must reconstruct BOTH legs through two decoders: minimize ||legA - D_A z||^2 + ||legB - D_B z||^2 + lambda||z||_1. T unrolled prox steps: z <- softthreshold(z - eta(D_A^T(D_A z - legA) + D_B^T(D_B z - legB)), lambda*eta). Output head reads z (or D_bind z). Because z is sparse and must explain both legs at once, the surviving active atoms are necessarily CONJUNCTIVE — a coincidence-coding dictionary where an atom fires only when its legA-part and legB-part are jointly present.

## Why it crosses the binding wall

Attention mixes additively (weighted value sum): it can hold legA+legB in superposition but nothing forces a MINIMAL JOINT explanation, so the mix stays linear/unbindable. ISTA's L1 prox actively suppresses single-leg atoms — they pay the sparsity cost without halving both residuals — so the optimizer SELECTS atoms that co-explain = a competitive binding operator. Ablation: lambda=0 -> least-squares additive code = no conjunction (back to attention-like FAIL); restore lambda -> conjunctive atoms emerge. Second ablation: drop the legB reconstruction term -> atoms become legA-only, binding lost. Distinct from generic energy_settle attractor: this is convex sparse inference whose binding logic is sparsity-induced conjunction, not Hopfield pattern completion.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Plant a dictionary where low-L1 reconstruction of paired inputs is only achievable with conjunctive atoms; data = sparse combos of bound pairs. Dual-decoder ISTA vs (i) lambda=0 least-squares (ii) single-leg ISTA. Pre-register: dual-ISTA support-recovery F1>=0.9 on planted conjunctive atoms + lower joint reconstruction at matched sparsity; lambda=0 and single-leg fail recovery. Binding-selectivity metric (atom fires for pair(a,b) but not a-alone/b-alone) high only for dual-ISTA.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTERED ONLY (cost-gated, user-go). 303M custom mouth: unrolled-ISTA block (T=4 prox steps, D_A=conv-trunk readout, D_B=attention role readout, per-atom learned lambda) replaces top transformer blocks; output reads sparse code. Loss = next-byte + joint-reconstruction aux. Clean 4-cell corpus, held-out CE-descent gate + engine-native G1/G6 on CORE conv; ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
