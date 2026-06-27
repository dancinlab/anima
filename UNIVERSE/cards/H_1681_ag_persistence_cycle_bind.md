# H_1681 — Persistent-Homology Cycle Mouth (A-grow / G-shrink filtration bind)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** algebraic topology / persistent homology (relational H1 1-cycle as a basis-free conjunction certificate; distinct from sheaf cohomology gluing)
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `ag_persistence_cycle_bind`

## Mechanism

The two legs place points in a shared feature metric space. The binding op builds a Vietoris–Rips filtration where leg-A monotonically GROWS the connectivity radius (forward) and leg-G (reverse) monotonically SHRINKS/kills it (a co-filtration). A conjunction is encoded as a persistent 1-cycle (a loop) BORN only when both legs' points are present and DYING under G's shrink — its persistence (death−birth) is the binding strength. Readout = the H1 persistence diagram (a few (birth,death) pairs) computed by union-find/boundary reduction in one forward. Two features bound ⇒ long-lived 1-cycle; either feature alone ⇒ no loop (only H0 components).

## Why it crosses the binding wall

H0 (connected components) is the additive 'which features are present' content conv/attention already capture. An H1 1-cycle is an intrinsically RELATIONAL, coordinate-free invariant: it exists iff features sit in a closed relation no single feature creates, and it cannot be recovered from per-feature marginals or pairwise sums. ABLATION: read H0 only (zero the H1 channel) → reverts to clustering baseline; if conjunction accuracy collapses to H0-only, binding provably lives in H1 = relational structure, not parameter count.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy + tiny union-find, $0. 4 feature-atoms placed so the BOUND class forms a 4-point loop (long H1 persistence) and the UNBOUND class is the same 4 points as a tree/star (H1≈0), with IDENTICAL H0 component count AND identical pairwise-distance histogram (provably H0/marginal-blind). Frozen bar: H1-persistence readout AUROC ≥0.90; H0-only baseline ≤0.55. PASS iff H1 ≥0.90 AND H0-only ≤0.60 over 1000 configs.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registration only (~1 H100, explicit go). Mid mouth block emits ~16 feature points; binding op = mini Rips H1 (grow radius from leg-A norms, kill from leg-G), feed top-3 (birth,death,centroid) of H1 to readout. 4-cell corpus, held-out CE-descent gate. Pre-register engine-native: H1-ON → G6 fals>0 AND G1≥baseline; H0-only ablation → FAIL. ckpt PULL before teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
