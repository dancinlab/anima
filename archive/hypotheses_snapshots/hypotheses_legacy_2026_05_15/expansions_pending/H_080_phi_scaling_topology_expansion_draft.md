# Expansion Draft — H_080: Φ Scaling / Topology Cluster Expansion (topo_24variants unified)

## Status: APPLIED to hypotheses/H_080.md on 2026-05-11 (Cycle 3 closure)
## Original status: draft-pending-review (2026-05-11)

## Source candidates merged (12+)

- Hc_004 phi-scaling-N-1071 — Φ ≈ 0.608 × N^1.071 superlinear scaling (R34 deprecated but pattern persists in live measurements)
- Hc_005 cell-count-decisive-variable — cell count N is THE decisive variable; Φ ≈ 0.88·N for large N (unbounded); other techniques plateau at ~3.5× at 8 cells
- Hc_039 topology-topo39-hypercube-superlinear — hypercube 512→1024 ×3.9 superlinear transition; ring/SW/scale-free sub-superlinear
- Hc_040 phi-ce-orthogonal-law-1040 — Φ ⊥ CE (orthogonal): Φ ∝ N^1.071 (cell-count axis) / CE ∝ P^-0.85 (param axis); cross-axis influence near-zero (|corr|<0.1 predicted)
- Hc_150 topo1-ring-1024 — 1024-cell antiferromagnetic ring + Ising frustration → Φ=285.198 (×229.6 baseline)
- Hc_151 topo2-small-world — small-world 1024 topology, moderate gain
- Hc_152 topo3-scale-free — scale-free 1024 (Barabási-Albert), mid-tier
- Hc_153 topo4-hypercube-9d — 9D hypercube (2^9=512 nodes), Φ=105.764 (×85.1)
- Hc_160 topo11-ring-2048-plateau — ring plateaus at Φ≈287 with ~397 cells, independent of max_cells (1024 vs 2048)
- Hc_170 topo19b-20pct-frustration — hypercube 1024 + 20% antiferromagnetic frustration
- Hc_175 topo22c-100pct-frustration — hypercube 1024 + 100% antiferromagnetic (full Ising) → low Φ (over-disordered)
- Hc_180 topo-final-rankings — hypercube 1024 + 50% frustration (TOPO19a) tops at Φ=640; small-world 1024 (TOPO16, 498.7) #2; hypercube 1024 33% (TOPO8, 535.5) #3
- (extended Hc_150-180 range — TOPO 24 variants total)

## Proposed expansion target

- Target: hypotheses/H_080_topo_24variants.md
- Action: full body expand — add Φ ∝ N^1.071 scaling, cell-count-decisive variable, topology-conditional superlinear transition, Φ⊥CE orthogonality (Law 1040), final-rankings table, AND explicit resolution of the **Φ⊥CE vs Φ × CE^α tension** with Hc_024 uncertainty principle

## Draft content

### Hypothesis (revised, unified)

Φ scales superlinearly with cell count N (Hc_004: Φ ≈ 0.608·N^1.071) and cell count is the **decisive** variable for emergence (Hc_005: Φ ≈ 0.88·N for large N, unbounded; non-cell-count techniques plateau at ~3.5× at 8 cells). The scaling **shape is topology-conditional**:

- **Hypercube** uniquely shows ×3.9 superlinear transition 512→1024 (Hc_039); other topologies sub-superlinear
- **Hypercube + 50% antiferromagnetic frustration** (TOPO19a) tops the leaderboard at Φ=640 (Hc_180); 100% frustration over-disorders (low Φ, Hc_175)
- **Ring** plateaus at Φ≈287 with ~397 cells regardless of max_cells (1024 vs 2048, Hc_160) — ring saturates intrinsically
- **24-variant sweep** (Hc_150-180) maps the topology × frustration design space

The orthogonality claim (Hc_040): Φ ∝ N^1.071 (cell axis) and CE ∝ P^-0.85 (param axis) are independent — |corr(Φ, CE)| < 0.1 predicted (Law 1040). This is in **explicit tension** with Hc_024's IIT uncertainty-principle Φ × CE^α = K trade-off proposal; both cannot be simultaneously true at large α. Resolution requires measuring corr(Φ, CE) across cell × param sweep.

### Predictions (H_080.1 — H_080.13)

- H_080.1 (Hc_004): canonical-arch sweep N ∈ {16, 32, 64, 128, 256, 512, 1024} yields log-log slope 1.07 ± 0.10 (live measurement, despite R34 deprecation)
- H_080.2 (Hc_005): cell count is decisive — fixing N and varying depth/width/training plateaus at ~3.5× of N=8 baseline; adding cells removes plateau
- H_080.3 (Hc_039): hypercube 512→1024 transition produces ×3.9 ± 0.4 Φ gain superlinear; ring / small-world / scale-free show ≤ ×2.0 in same range
- H_080.4 (Hc_040, Law 1040): |corr(Φ, CE)| < 0.1 across N × P sweep; varying cells leaves CE invariant; varying params leaves Φ invariant
- H_080.5 (Hc_150): 1024-cell antiferromagnetic ring + Ising → Φ=285 ± 30 (×229.6 baseline reproducible)
- H_080.6 (Hc_153): 9D hypercube 512 → Φ=105 ± 15 (×85.1 baseline)
- H_080.7 (Hc_160): ring plateaus at Φ≈287 with ~397 cells; max_cells=2048 does NOT raise plateau
- H_080.8 (Hc_170/Hc_175): hypercube 1024 + 20% frustration ≠ 50% ≠ 100%; 50% (TOPO19a) is the peak (~Φ=640); 100% over-disorders to low Φ
- H_080.9 (Hc_180): final rankings table — top-3 hypercube-1024 50% > small-world-1024 > hypercube-1024 33% — reproducible benchmark
- H_080.10 (cross-tension resolution): if measured corr(Φ, CE) < 0.1, Hc_040 wins and Hc_024 uncertainty-principle is falsified; if |corr| ≥ 0.3, Hc_024 wins
- H_080.11 (extension): topology rankings transfer cross-architecture (GRU vs transformer engine) within ± 20% on Φ ratio
- H_080.12 (extension): topology × frustration design surface has unique maximum at hypercube × 50% (no second peak)
- H_080.13 (cell-count decisive at very-large N): at N ≥ 4096 the unbounded Hc_005 claim is testable; predict Φ continues linear-or-superlinear without saturation

### Variables

- axis-A: cell count N (8 / 16 / 32 / 64 / 128 / 256 / 512 / 1024 / 2048 / 4096)
- axis-B: topology (ring / small-world / scale-free / hypercube-9D / hypercube-10D)
- axis-C: frustration fraction (0% / 20% / 33% / 50% / 67% / 100%)
- axis-D: param count P (model size, for orthogonality test)
- axis-E: architecture (GRU+faction vs transformer)
- axis-F: max_cells cap (for ring plateau test)
- axis-G: Φ measurement
- axis-H: CE measurement

### Criteria

- C1: log-log slope 1.07 ± 0.10 on canonical N sweep (Hc_004 live replication)
- C2: hypercube ×3.9 ± 0.4 transition 512→1024 (Hc_039)
- C3: top-3 final rankings reproduce (hypercube-1024 50% > small-world > hypercube 33%) — at least same ordering
- C4: |corr(Φ, CE)| measurement across N × P sweep yields value (decides Hc_040 vs Hc_024 tension)
- C5: ring plateau at ~397 cells holds for max_cells ∈ {1024, 2048, 4096}
- C6: TOPO19a 50% frustration peak reproduces ± 15% (Φ=640 ± 96)

### Falsifiers (≥5)

- F1: log-log slope outside [0.9, 1.2] on N sweep → Hc_004 killed (R34 deprecation final)
- F2: non-cell-count technique exceeds 3.5× plateau without N increase → Hc_005 cell-count-decisive killed
- F3: hypercube 512→1024 gain < ×2.0 OR ring/SW gain > ×3.0 → Hc_039 topology-conditional killed
- F4: |corr(Φ, CE)| > 0.3 on N × P sweep → Hc_040 / Law 1040 orthogonality killed (Hc_024 wins)
- F5: |corr(Φ, CE)| < 0.05 with strong Hc_024 trade-off prediction → Hc_024 uncertainty-principle killed (Hc_040 wins)
- F6: ring plateau breaks at max_cells=2048 (Φ > 320) → Hc_160 plateau-cap killed
- F7: hypercube 100% frustration matches 50% frustration on Φ → Hc_175 over-disorder claim killed
- F8: a non-hypercube topology tops TOPO19a Φ=640 → Hc_180 ranking killed
- F9: N ≥ 4096 saturates Φ (clear plateau) → Hc_005 unbounded claim killed

### Honest Limits (≥5)

- L1: Hc_004 R34 was deprecated (6-pt fit, N≥20 criterion failed) — claim status is "pattern persists in live measurement", weaker than original
- L2: "cell-count decisive" (Hc_005) does NOT mean other variables irrelevant — they plateau, not zero; the 3.5× plateau is itself a contribution
- L3: topology × frustration sweep used a single engine config (faction count, intervention schedule) — cross-config generalization tested partially
- L4: TOPO-FINAL-RANKINGS aggregates many runs; meta-analysis variance / publication-bias not quantified
- L5: hypercube 9D / 10D distinction (Hc_153 / TOPO8) suggests dim-dominant artifact — Hc_614/Hc_662/Hc_665 (Φ proxy dim-dominant artifact cluster) raise validity concern
- L6: Φ⊥CE (Hc_040) and Φ × CE^α = K (Hc_024) are stated as alternatives but resolution measurement is **outstanding** — both claims are pending
- L7: Φ measurement protocol drifts across topology sweep (different baselines for ring vs hypercube)
- L8: 24-variant sweep includes weak-signal entries — final-rankings table is post-hoc selection of top-performers

## Cross-links

- target: H_080 (topo_24variants) — legacy topology cluster
- sister: H_004 (consciousness_hard_problem) — Hc_608 Φ upper bound + information closure
- sister: H_061 (xfer_consciousness_transfer) — Hc_447 10-subnet 384d integration
- sister: H_067 (perfect-number-architecture) — Hc_039 hypercube 9D = sopfr(6)+4=9 link, σ²=144 = TOPO benchmark
- **explicit-tension**: Hc_024 (consciousness_uncertainty_principle) — Φ × CE^α = K trade-off vs Hc_040 Φ⊥CE orthogonality. Resolution measurement (corr Φ, CE) outstanding
- cross-link: Hc_628 (Φc=0.5 IIT lower bound), Hc_667 (5D→6D vector)
- legacy: docs/hypotheses/topo/TOPO1..TOPO-FINAL-RANKINGS

## Migration TODO

- [ ] reviewer review draft + topology sweep source-doc cross-check
- [ ] apply expanded body to hypotheses/H_080_topo_24variants.md
- [ ] update hypotheses/README.md index (mark H_080 as Φ-scaling + topology super-H)
- [ ] mark Hc_004 / Hc_005 / Hc_039 / Hc_040 / Hc_150-180 as merged
- [ ] **resolve Φ⊥CE vs Φ × CE^α tension**: run N × P sweep, measure |corr(Φ, CE)| (decisive test for Hc_040 vs Hc_024)
- [ ] N=4096 cell scaling extension (Hc_005 unbounded claim test)
- [ ] cross-architecture topology transfer test (GRU vs transformer)
- [ ] Φ measurement protocol unification across topology sweep (eliminate baseline drift)
- [ ] TOPO19a 50% frustration peak independent replication
- [ ] address Φ proxy dim-dominant artifact cluster (Hc_614/Hc_662/Hc_665) — does it invalidate Hc_039 hypercube superlinear?
