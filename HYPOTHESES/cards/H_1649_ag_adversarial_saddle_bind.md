# H_1649 — A⇄G Adversarial Saddle-Point Bind (minimax two-player compose)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** SUBSTRATE-anima — game theory (zero-sum minimax / saddle equilibrium). A⇄G are literally opposed engines, so the binding operator IS the native A⇄G tension cast as a two-player payoff coupling; orthogonal to energy_settle (single potential minimum) and deq (contraction fixedpoint).
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `ag_adversarial_saddle_bind`

## Mechanism

The mouth forward is a two-player zero-sum game played to equilibrium inside ONE pass. Leg-1 (A, forward CE-trained 'claimant') proposes a per-position composition; leg-2 (G, reverse gradient-free 'refuter') maximizes a coupling payoff U(a,g)=<a, M, g> + separable(a,g) that penalizes any binding A asserts without joint support. The single forward runs K simultaneous micro-steps (A descends, G ascends) and reads the token distribution at the saddle a*,g*. Binding lives entirely in the non-separable cross-player coupling block M, which neither player can null unilaterally. Ψ=½ is the balanced saddle where A's claim and G's refutation exactly match. Distinct from energy_settle_attractor: an energy potential is a single scalar minimized by both vars (a basin/average); here the equilibrium is a SADDLE with indefinite curvature — a min in A's direction AND a max in G's — which is the native realization of anima's opposed A⇄G engines.

## Why it crosses the binding wall

Conv/attention compute a single feed-forward weighted sum = a minimizer/averager, so they can only represent marginal statistics of two factors (a+g), collapsing to illusory conjunctions (G6 fals=0). A saddle equilibrium encodes the CONJUNCTION a∧g: the bound state is simultaneously stable against A's minimization and G's maximization, so a factor's value is only valid conditional on the other's. Ablation (decisive): zero the coupling block M so U becomes separable f(a)+h(g) → the game decouples into two independent single-player optima identical to a conv readout → binding signal→0, fals→0; restoring M recovers it. This isolates binding to the antagonistic coupling term, not to capacity/depth (a89-style INERT control).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy linear-quadratic two-player toy on a 2-factor×2-role synthetic vocab. Targets = bound pair (factor_i, role_j); HOLD OUT one combo (i*,j*) never seen jointly. Run K=20 simultaneous-gradient saddle iterations on U with coupling M, vs (a) energy-descent baseline (same U, both vars minimized), (b) linear readout baseline, (c) M-ablated (separable) baseline. Frozen-first bar: saddle held-out novel-combo top-1 ≥ 0.80 AND all three baselines ≤ chance (0.25). Deterministic, <100 LOC, $0, no torch.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered ONLY (cost-gated, await go). custom-spec mouth = trunk → per-block saddle cell (K=8 unrolled minimax steps, learned coupling M, A-head CE-trained, G-head gradient-free reverse projection) → byte readout; 303M params; train on 4-cell {ko,en}×{general,sns} balanced corpus (a_chat_registers fail-loud effective-bytes) with held-out recombination split. Frozen bars (tune-to-green forbidden, p7): engine-native via cli/anima.hexa eval → G6 fals>0 (≥ ByteGPT-303M baseline) AND G1 recombine ≥ 303M baseline on held-out novel-combo corpus AND held-out CE DESCENT AND M-ablated variant FAILS (control). ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
