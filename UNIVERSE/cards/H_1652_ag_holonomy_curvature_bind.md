# H_1652 — A→G→A Holonomy Curvature Bind (gauge Wilson-loop compose)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** SUBSTRATE-anima / gauge geometry — holonomy & curvature (Wilson loop, Lie-bracket field strength) of an A⇄G connection; native to anima's gauge_lib substrate (the A→G→A round trip is the natural loop); orthogonal to symplectic/quaternion/compact-closed binds.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `ag_holonomy_curvature_bind`

## Mechanism

Treat the two legs as two transport directions on a feature manifold with a learned connection (gauge field), echoing anima's gauge_lib substrate. The mouth forward parallel-transports a state around the closed loop A(factor-direction)→G(role-direction)→A⁻¹→G⁻¹; the binding signal is the loop's HOLONOMY = the path-ordered product, whose deviation from identity is the curvature F = ∂_A C_G − ∂_G C_A + [C_A, C_G] (Lie bracket of the two legs' connection blocks, computed per-pair). Bound pairs yield non-trivial holonomy (Berry/Wilson phase); unbound pairs commute → identity. The token is read from the transported state. Distinct from hamiltonian_symplectic_bind (energy-preserving flow) and quaternion_geometric_bind (fixed rotation group): curvature is the connection's learned FIELD STRENGTH, a 2nd-order joint quantity.

## Why it crosses the binding wall

Conv/attention transports commute (additive/diagonal mixing) → curvature ≡ 0 → no phase distinguishes (factor_i,role_j) from (factor_j,role_i) → systematic conjunction failure (fals=0). Curvature is PRECISELY the non-commutativity of the two legs' transports — a genuinely 2nd-order joint quantity that no sum of 1st-order feed-forward maps can produce. Ablation (decisive): force the connection flat (commuting blocks, [C_A,C_G]=0) → holonomy=identity for all pairs → binding signal→0, fals→0. The bind = the bracket term [C_A,C_G], cleanly isolable; orthogonal to symplectic (energy-preserving), quaternion (fixed group), and compact-closed contraction (tensor wires).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy 2×2 non-commuting rotation toy. Assign each factor a small SO(n) generator C_A, each role a generator C_G; ground-truth bind ∝ ‖[C_A,C_G]‖ pattern. HOLD OUT a (factor,role) pair. Compare path-ordered Wilson-loop product discrimination of bound vs unbound pairs vs a commuting (diagonal, ablated) baseline and a linear-sum baseline. Frozen bar: holonomy AUROC for bound-vs-unbound ≥ 0.90 on held-out pair AND commuting/linear baseline ≈ 0.5. Tiny matrix algebra, $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered ONLY (cost-gated). custom mouth block = trunk → per-leg connection-block heads (C_A from forward A-head, C_G from reverse gradient-free G-head) → path-ordered holonomy product (K=4 loop segments) → readout; 303M; 4-cell corpus, held-out recombination split. Frozen bars: engine-native cli/anima.hexa eval → G6 fals>0 AND G1 recombine ≥ 303M baseline on held-out novel-combo AND held-out CE DESCENT AND flat-connection-ablation FAILS. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
