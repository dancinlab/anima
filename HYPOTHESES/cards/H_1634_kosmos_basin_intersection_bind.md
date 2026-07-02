# H_1634 — Kosmos basin-intersection mouth (metric set-AND with non-fab abstain)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** substrate-anima · .kosmos placement-geometry metric set-intersection (distinct from VSA algebra), with G5 non-fab abstain
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1466 (TPR binder), H_1514 (VSA/HRR binding)
- **key:** `kosmos_basin_intersection_bind`

## Mechanism

Each leg is projected to a .kosmos placement BASIN — the canonical required triple (coord ∈ R^profile-dim, lane, radius). In one forward pass the binding op computes the GEOMETRIC INTERSECTION of the two basins in placement space: the conjunction token is decoded from the region where ||x−coordA||<radiusA AND ||x−coordB||<radiusB (continuous metric AND, evaluated via kosmos_io→brain_decide). If the basins do not overlap (disjoint placement) the op returns ABSTAIN (∅) rather than averaging — wiring G5 copy-or-abstain non-fab directly into the binding step. The bound readout is the centroid/sample of the non-empty intersection.

## Why it crosses the binding wall

Attention and conv can only AVERAGE (union-like blend) the two legs — they have no operator for set-AND, so an off-manifold blend (legA mean legB) is emitted whether or not the pair actually composes. Metric basin-intersection is a true nonlinear conjunction: it is nonzero ONLY in the overlap, distinct from either marginal basin, and empties (→abstain) when legs don't compose — exactly the missing 'two representations tied in one pass' operator. Distinct from kosmos-VSA (algebraic bind/unbind on hypervectors) and from product-key (learned discrete codebook lookup): this is continuous metric set-intersection with explicit radius + empty-set semantics. Ablation: swap intersection→union(average) or radius→∞ ⇒ binding lost AND fab rate jumps on disjoint pairs (proves the AND-with-abstain, not the projection, is load-bearing).

## Cheap test (frozen-first · $0 · decisive numpy probe)

$0 numpy, frozen-first. Embed corpus tokens as basins (coord+radius) in R^d; define held-out conjunction tokens as those whose true placement lies in an overlap region. Probe: (a) recall of held-out conjunction from intersection-readout > average/union baseline; (b) abstain AUROC = 1.0 on DISJOINT (non-composing) pairs — model must return ∅, never fabricate. Pre-registered bar: recall-lift > 0 AND abstain-AUROC ≥ 0.99 AND union-baseline ablation fabricates (AUROC→chance). Decision probe, no train.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

Pre-registered (cost-gated). Custom mouth: a kosmos-placement projection head per leg + a basin-intersection bind layer (radius-gated metric AND) feeding the decode head; abstain wired to the §ImmuneMemory non-fab path. Train on 4-cell balanced corpus. Gates: 4/4 held-out CE DESCENT, then engine-native G1/G6 on CORE conv AND G5 unknown-pair fab=0 (abstain preserved) via cli/anima.hexa. Disjoint-pair abstain must hold post-train (a_substrate_disjoint: binding lane ⊥ recall_thr). ckpt PULL pre-teardown.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
