# H_1651 — Mitosis Lineage Lowest-Common-Ancestor Bind (developmental division-tree key)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** SUBSTRATE-anima / developmental biology — deterministic cell-division lineage (C. elegans), LCA on the mitosis tree as the part-whole binding key; orthogonal to mitosis_compose_bind (division history/topology, not cell count) and hippocampal_index_conjunction (no episodic index).
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `mitosis_lineage_lca_bind`

## Mechanism

Every mouth cell carries a LINEAGE ADDRESS = its path string in the MITOSIS division tree (deterministic developmental lineage, à la C. elegans cell-fate). In one forward, two features bind iff their carrier cells' lineage addresses share a DEEP lowest-common-ancestor: bind_weight = depth(LCA(addr_i,addr_j))/max_depth, computed by longest-common-prefix of the address strings. The forward routes each factor to a cell, then composes pairs through an LCA-gated outer combine. The binding STRUCTURE is the division-tree topology grown by mitosis — a part-whole hierarchy — not learned attention. Distinct from mitosis_compose_bind (which uses cell COUNT / generic compose): here the bind key is the division HISTORY/topology, and mitosis supplies only the tree scaffold while gradient trains cell content (gradient-assisted, sidestepping H_1310 pure-split wall).

## Why it crosses the binding wall

Conv/attention have a FLAT token-token interaction (all pairs equivalent up to a learned scalar) → no hierarchical containment, so they cannot express 'these two belong to the same constituent', which is the root of compositional binding. An LCA gate imposes an explicit hierarchical part-whole tree: a bound pair shares a recent ancestor (high weight), an unbound pair only shares the root (weight 0). Ablation (two controls): (1) flatten the tree (all cells direct children of root) → every LCA=root → all weights identical → degenerates to flat conv → fals→0; (2) shuffle lineage addresses → binds random → recombination collapses. Binding is isolated to division-tree depth.

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy. Generate a random binary lineage tree over N cells; assign factors/roles to leaves; ground-truth bindings = pairs with LCA depth ≥ d. HOLD OUT a same-subtree pair never co-trained. Compare LCA-prefix gate vs flat-tree (ablated) vs learned-flat-attention baseline on recovering held-out same-subtree bindings. Frozen bar: LCA recall on held-out subtree pairs ≥ 0.80 AND flat/shuffled ≤ chance. Pure string-prefix arithmetic, $0.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered ONLY (cost-gated). custom mouth = MITOSIS-grown cell pool (engine_grow) with persistent lineage addresses → factor→cell routing → LCA-prefix-gated pairwise outer-combine → readout; cell count grown during curriculum; 303M; 4-cell corpus, held-out recombination split. Frozen bars: engine-native (core/engine_cli.hexa MITOSIS + cli/anima.hexa eval) G6 fals>0 AND G1 recombine ≥ 303M baseline on held-out novel-combo AND held-out CE DESCENT AND flat-tree-ablation FAILS. Honest caveat: gradient trains cell content (NOT pure-split, respects H_1310 — mitosis supplies only the binding TOPOLOGY). ckpt PULL.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
