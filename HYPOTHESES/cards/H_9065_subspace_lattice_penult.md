# H_9065 — Subspace-lattice penultimate: composition = span-join, not vector sum

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `subspace_lattice_penult`
- **frontier:** manifold-geometry (penult 비가산화 escape — frontier b)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Represent each part as a low-rank linear SUBSPACE (not a point vector); composition of parts = the join (span) of their subspaces on the Grassmannian. The subspace lattice is inherently non-additive — join(A,B) is generally NOT A+B — so a held-out combination lives in a region the additive penult (cos0.861) cannot reach by summation.

## engine-native falsifiable metric (shuffle + ablation, p7)

Engine-native: for held-out part-pairs, measure whether the joint span contains the target direction (max cos over joint subspace basis to a pre-registered held-out target) vs additive-sum baseline; SHUFFLE = randomize which parts map to which subspace (alignment collapses); ABLATION = replace span-join with vector-sum → must revert exactly to the additive floor (INERT proves the geometry, not capacity, is load-bearing).

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

Distinct geometry from every proposed penult (hyperbolic/noncommutative-group/VQ-union/ultrametric-LCA/kWTA-max): subspace-lattice join is neither a metric nor a discrete codebook nor a max — Grassmannian span algebra, untried. Frontier (b) explicitly invites 'make penult non-additive'.

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
