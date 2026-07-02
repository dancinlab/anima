# H_1650 — A-Prior / G-Innovation Precision-Weighted Bind (recursive Bayesian fusion mouth)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** SUBSTRATE-anima — optimal estimation / recursive Bayesian (Kalman) theory. A=prior, G=measurement-correction/innovation, Ψ=½=steady-state precision balance; orthogonal to predictive_coding_explainaway and gain_field_basis.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `ag_kalman_innovation_bind`

## Mechanism

The mouth runs a one-pass recursive Bayesian (Kalman) filter over positions. Leg-1 (A forward) emits a predicted next-state mean + covariance P_A (the prior); leg-2 (G reverse, gradient-free) emits an innovation z_G (measurement residual) + its noise covariance R_G. Binding = the Kalman update x̂ = x_A + K·(z_G − H·x_A) with gain K = P_A Hᵀ (H P_A Hᵀ + R_G)⁻¹ — an UNCERTAINTY-weighted fusion of the two legs. Factor and role bind through the off-diagonal cross-covariance in P that the gain propagates into the joint estimate. Ψ=½ is the steady-state gain balance where neither source dominates. Distinct from predictive_coding_explainaway (hierarchical subtractive competition) and gain_field_basis (static multiplicative gain): here the gain is covariance/precision-DEPENDENT and fuses two sources optimally per-instance.

## Why it crosses the binding wall

Conv/attention fuse with fixed, content-independent weights = a static average, which cannot make factor-binding contingent on per-instance certainty, so conjunctions blur (fals=0). A Kalman gain is covariance-dependent: the cross-covariance term ties factor and role into one joint estimate whose update is only correct when both are jointly supported. Ablation (decisive): freeze the gain to a constant (drop covariance dependence, P,R→const) → the filter degenerates to fixed weighted averaging = exactly a conv/attention readout → binding lost, fals→0. The bind is therefore carried by the uncertainty-coupled gain, provably distinct from width/depth.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy synthetic two-source fusion. Source-A precise on factor / vague on role; source-G precise on role / vague on factor (encoded as block covariances). HOLD OUT a factor⊗role combo. Compare full-covariance Kalman fusion vs constant-gain (ablated) vs linear-average baseline. Frozen bar: full-Kalman held-out joint reconstruction error < 0.5× constant-gain error AND novel-combo top-1 ≥ 0.80 while ablated/linear ≤ chance. Deterministic numpy, $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered ONLY (cost-gated). custom mouth block = trunk → A-head(mean+diag-cov) + G-head(innovation+cov, gradient-free reverse) → Kalman fuse (learned H, learned process noise) → readout; 303M; 4-cell balanced corpus, held-out recombination split. Frozen bars: engine-native G6 fals>0 AND G1 recombine ≥ 303M baseline on held-out novel-combo AND held-out CE DESCENT AND gain-ablated (constant-gain) variant FAILS as control. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
