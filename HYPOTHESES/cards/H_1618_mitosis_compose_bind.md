# H_1618 — Mitosis-Compose Binding (cell-division joint tiling, expression-axis)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** Mitosis×savant expression multiplication (H_1564). Biology: cortical column / local-expert tiling. Honest scope: expression-axis, NOT walled from-scratch split (H_1310).
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `mitosis_compose_bind`

## Mechanism

Use the MITOSIS substrate as a multiplicative EXPRESSION binding array (H_1564 expression-axis — NOT from-scratch split-learning, which is walled H_1310/H_1574). Trunk is CE-trained (gradient). The compose step routes (leg1,leg2) to a pool of N mitosis cells; each cell binds a sub-conjunction of the pair (a Voronoi tile of the joint key space), bound output = combination across co-active cells. Cell-count (mitosis grow) and per-cell expression (savant golden-zone GZ_LOWER≈0.212) are orthogonal multiplicative levers → total binding capacity = N·r (super-additive, H_1564). The split supplies factored conjunction slots a single dense head cannot allocate; binding = which (cell, sub-pair) tiles co-activate.

## Why it crosses the binding wall

a single dense attention head must represent ALL conjunctions in one shared space → interference (the superposition-blur giving fals=0). Partitioning the joint space across mitosis cells gives DEDICATED conjunction slots (each cell a local expert on a region of (a,b)-space), reducing crosstalk so held-out conjunctions become representable. Crucially this is the EXPRESSION axis (H_1564 🟢), not the falsified from-scratch split-learning (H_1310); trunk still learns by gradient, mitosis only multiplies expression slots. Ablation: collapse N→1 (savant-only) → multiplicative capacity gone, recombination → dense baseline. Control: random tiling vs key-space tiling at same N → tests whether STRUCTURED partition (not just more heads) carries it (guards against rediscovering depth/attention).

## Cheap test (frozen-first · $0 · decisive numpy probe)

numpy. K atoms, joint key = concat(emb_a,emb_b); N-way k-means tile of joint space; per-tile linear expert predicts held-out c. Compare N=1 dense vs structured N-tile vs random N-tile. Pre-register: structured N-tile recovers held-out conjunction > N=1 dense AND > random-tile (same N). Dead-if: structured ≤ random (then it's just capacity = depth, excluded). $0. Directly guards the H_1310/H_1574 'geometry not learning' finding.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REG. 303M conv trunk + N-cell mitosis compose lane on joint penultimate (cells = live engine_cli MITOSIS engine_grow/VAdaptField; expression via savant golden-zone). CE-train trunk by gradient (NOT from-scratch split). Engine-native G1/G6, ckpt PULL. Scoped EXPRESSION-axis only (c9, a_mitosis_train).

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
