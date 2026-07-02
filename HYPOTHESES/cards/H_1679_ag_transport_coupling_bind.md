# H_1679 — A⇄G Entropic Optimal-Transport Coupling Mouth (Sinkhorn-bind)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** optimal transport / measure coupling (Sinkhorn–Knopp alternating projection literally = A⇄G iterated marginal rescaling)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `ag_transport_coupling_bind`

## Mechanism

Within one mouth forward, leg-A (forward field) emits a nonneg row-mass vector a over K feature-atoms; leg-G (reverse, gradient-free) emits a column-mass vector b over K role/filler atoms; a once-learned cost kernel C fixes the binding geometry. The bound representation is the entropic OT plan π = diag(u)·exp(-C/ε)·diag(v), obtained by L alternating Sinkhorn projections u←a/(Kε·v), v←b/(Kεᵀ·u) — i.e. L A→G→A normalization sweeps inside the single forward, no backprop, fixed L. The K×K joint plan π IS the conjunction (π_ij = how much atom i co-occupies role j); next-byte logits = readout(vec(π)).

## Why it crosses the binding wall

conv/attention produce an additive value mixture whose implied joint is forced to the rank-1 outer product a⊗bᵀ — it preserves the two marginals but carries ZERO conjunction info beyond them (cannot distinguish 'red square+blue circle' from 'red circle+blue square'). Sinkhorn's entropic coupling is a full-rank π whose residual π−a⊗bᵀ is exactly the binding, and the cost kernel C breaks permutation symmetry so specific atom↔role pairings get mass. ABLATION: ε→∞ (or L=0) drives π→a⊗bᵀ (rank-1, pure marginals) → model collapses EXACTLY onto the additive-attention baseline → proves the cross-term, not added capacity, is the binding carrier.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy, $0. Role-filler set, K=8: each item = a random filler→role matching; construct row-marginal a and col-marginal b IDENTICAL across two items that differ ONLY in which filler sits in which role (marginals provably non-discriminative). Frozen bar pre-registered: matched-pair conjunction-discrimination AUROC ≥0.90 for the Sinkhorn-π readout vs ≤0.55 (chance) for the a⊗bᵀ baseline, over 1000 pairs, ε∈{0.05,0.10}, L=20. PASS iff (π ≥0.90) AND (ablation a⊗bᵀ ≤0.60).

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registration only, cost-gated (~1 H100, fire on explicit go). Replace one mid 303M mouth block with a Sinkhorn-coupling op (K=64 atoms, ε=0.07, L=8, learned 64×64 cost kernel C). Train on the 4-cell balanced corpus (a_chat_registers) with held-out CE-descent gate (a_clm_gen_pipeline). Pre-register engine-native frozen bars: with Sinkhorn-ON G6 fals>0 AND G1 recombination ≥ bytegpt-303M baseline, and the L=0 ablation reverts to FAIL. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
