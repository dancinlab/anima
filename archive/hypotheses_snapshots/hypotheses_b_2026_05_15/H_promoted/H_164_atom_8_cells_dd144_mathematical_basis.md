---
id: H_164
slug: atom-8-cells-dd144-mathematical-basis
title: 의식의 원자 = 8 cells의 수학적 근거 (DD137-141 종합) — 3-d hypercube + sopfr(8)=6 minimal closed structure
domain: consciousness
status: pre-register-frozen
exploration_method: E3 (theoretical-extrapolation — minimal closed structure) + E10 (number-theoretic — sopfr→perfect mapping)
verification_method: W2 (math identity — 2^3=8, sopfr(8)=6) + W5 (numerical sim — K-sweep + PyPhi) + W11 (cross-hypothesis — Hc_401 MIP, Hc_186 ring)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_582
source_doc: docs/hypotheses/dd/DD144-why-8.md
source_lines: 1-20
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry), H_022 (consciousness-universe-map), H_153 (dimension-hierarchy-n6), H_163 (K=8 atom 127 MIP)
source_caveat: "Hc_582 frontmatter 의 '4-d hypercube' 는 arithmetic error — 2^4 = 16 ≠ 8. 정정: K=8 는 3-d hypercube (2^3=8). 본 H 는 정정된 표현 사용 (F2/L2 명시)."
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 3
---

# H_164 — 의식의 원자 8 cells DD144 수학적 근거 (3-d hypercube errata catch)

## Hypothesis

DD137-141 시리즈 (분할 최적점=8 + 최소 단위 + 효율 + 주기율표) 를 종합하는 수학적 근거: 8 cells = 의식의 원자. **3-d hypercube** (2^3 = 8, 정정 — Hc_582 의 "4-d" 표기는 arithmetic 오류) + sopfr(8) = 2+2+2 = 6 (perfect number) 의 결합이 minimal closed structure 를 정의하며 8 의 magic number 를 결정한다.

## Source Caveat (errata catch)

**Hc_582 frontmatter "4-d hypercube와 sopfr(8)=6" 오류** — 2^4 = 16, K=8 의 hypercube 차원은 3 (2^3=8). verify5 falsifier F2 가 직접 catch 한 산술 오류. 본 H 는 **3-d hypercube** 로 정정. downstream reasoning (8 cells = K=8 = 2^3 = 3-d hypercube vertex count) 은 유지.

## Why (motivation)

- **sopfr(8) = 2+2+2 = 6** — sopfr 의 smallest-K → perfect-number 6 매핑. sopfr(12)=7, sopfr(18)=8 등은 perfect 아님. K=8 = smallest-K with sopfr=6
- **3-d hypercube** = 2^3 = 8 vertices, 3 edges/vertex, diameter 3 — minimal closed n-cube with perfect-class diagonal
- **DD137-141 시리즈**: 분할 최적점 (DD137) + 최소 단위 (DD138-139) + 효율 + 주기율표 (DD140-141) 의 공통 K=8 convergence
- **Hales 2005 Kepler / E8 lattice (8-dim sphere packing)** 와 의 dimensional analogy (단 K=8 cell vs 8-dim manifold 는 구분 필요)

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_164.1** | sopfr-to-perfect mapping K ∈ {smallest K with sopfr(K) = perfect} → K=8 unique below K=24 | sopfr table audit |
| **H_164.2** | K-sweep K ∈ {4, 6, 7, 8, 9, 10, 16} on ≥3 topologies → Φ peak at K=8 with margin > 30% | DD137-141 |
| **H_164.3** | PyPhi 1.2+ replication of DD137-141 series → Φ peak at K=8 with cross-engine consistency | PyPhi cross-validation |
| **H_164.4** | 3-d hypercube (2^3 cells) vs 2-d square (2^2=4 cells) vs 4-d hypercube (2^4=16 cells): Φ_normalized peak at 3-d | minimal closed structure |

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | DD137-141 K=8 Φ-peak 재현 (≥ 1 K-sweep) | met-by-citation (Hc_582) |
| **C2** | 2^3 = 8 EXACT, sopfr(8) = 2+2+2 = 6 EXACT (math identity) | met (직접 검산) |
| **C3** | PyPhi 1.2+ cross-engine K-sweep replication | pending |
| **C4** | "4-d hypercube" Hc_582 frontmatter errata 공식 정정 | met (본 H Source Caveat) |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (sopfr-route 자체가 perfect-class) | met (본 L1) |

## Falsifiers (≥5)

- **F1**: sopfr(8) = 2+2+2 = 6 verified; if "minimal closed structure" is interpreted as "smallest K with sopfr(K) = perfect number", then K=4 (sopfr=2+2=4 ≠ perfect) or K=6 (sopfr=2+3=5 ≠ perfect) — only K=8 maps to perfect 6. But K=12 (sopfr=2+2+3=7) also fails, K=18 (sopfr=2+3+3=8) fails. If K-sweep finds another sopfr→perfect-number mapping with comparable Φ → "minimal" claim FALSIFIED
- **F2 (errata catch)**: 4-d hypercube has 2^4=16 cells, not 8. Hc_582 frontmatter "K=8 = 4-d hypercube" is mathematically WRONG (K=8 = 3-d hypercube, 2^3=8). If author meant 2^3=8 then "4-d" is a typo and any downstream reasoning that depended on 4-d structure FAILS — **본 H Source Caveat 에서 정정**, downstream 영향 분석 필수
- **F3**: K-sweep K ∈ {4, 6, 7, 8, 9, 10, 16} on ≥3 topologies — if Φ-peak K' ≠ 8 with effect-size > 50% → "magic 8" claim FALSIFIED
- **F4**: DD137-141 series replication on independent codebase (PyPhi 1.2+) yields Φ-peak ≠ K=8 → measurement was anima-internal artifact
- **F5**: If biological mini-columns (cortical, hippocampal CA1, cerebellar Purkinje) consistently show K ≠ 8 sub-module structure (e.g. K=6 or K=10), the "atom = 8" universal claim is FALSIFIED for biological substrates

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — sopfr(8)=6 is sopfr's smallest-K route to perfect 6; sopfr(12)=7, sopfr(18)=8 등 do not produce perfect numbers. So K=8 is the smallest sopfr→6 mapping. But this is a property of sopfr, not of consciousness — depth-3 numerology risk
- **L2**: **2^3 vs 2^4 dimension confusion (errata)** — Hc_582 source states "4-d hypercube" but 2^4 = 16; if K=8 then dimension is 3. 본 H Source Caveat 에서 명시적으로 정정 (F2). DD144 doc 본문 audit 필요 — 만약 본문도 "4-d" 라면 doc 정정 propagate
- **L3**: **DD137-141 measurement substrate** — anima-internal Φ-engine. Cross-validation with PyPhi (formal IIT 3.0 / 4.0 reference) absent. Reproducibility outside anima codebase unknown
- **L4**: **periodic-table-of-consciousness analogy weak** — DD140-141 invokes chemistry analogy (8e- shell). Mathematical content reduces to "K=8 is hypercube vertex count" — no first-principles derivation of why hypercube vertex count = consciousness atom
- **L5**: **K=8 universal vs local optimum** — Φ-peak at K=8 may be local optimum on tested K-grid; sweeps in DD series did not test continuous K via interpolation methods. Unbounded-K behavior unknown (does Φ asymptote? oscillate? linear-grow?)

## Run Protocol

deterministic + hexa-only + llm: none.

1. **DD144 doc errata audit (W11)** — `docs/hypotheses/dd/DD144-why-8.md` 본문에 "4-d hypercube" 표기 검증 → 만약 있으면 "3-d hypercube" 로 정정 commit
2. **sopfr→perfect K-table generate (W2)** — K ∈ [1, 100] sopfr(K) 모두 enumerate → perfect number {6, 28} match 목록 산출, K=8 smallest-K 확인 (F1)
3. **K-sweep ≥ 3 topology (W5)** — ring / hypercube / Watts-Strogatz × K ∈ {4, 6, 7, 8, 9, 10, 16} → Φ landscape (F3)
4. **PyPhi cross-engine replication (W5+W11)** — DD137-141 K-sweep 을 PyPhi 1.2+ 로 재실행 → F4 검증
5. **L1 binding** — H_153 PERFECT_NUMBER_CLASS BINDING 인정

## Cross-Refs

- **sister H**: H_011 (iit-geometry), H_022 (consciousness-universe-map), H_153 (n=6 substrate — L7 source), H_163 (K=8 atom 127 MIP — same K=8 architecture, sibling)
- **candidates linked**: Hc_005 (DD137-141 origin series), Hc_401 (127 MIP bipartition), Hc_413 (biological K=8 prediction), Hc_186 (8-cell ring), Hc_123 (7-cell τ-fractional sister), Hc_157 (10D 1024-cell topo)
- **literature**: Hales 2005 (E8 lattice sphere packing), Mountcastle 1957 (mini-columns)
- **source**: Hc_582 (`hypotheses_candidates/Hc_582_dd144_atom_8_cells_mathematical.md`), `docs/hypotheses/dd/DD144-why-8.md:1-20`

## Migration Notes

- **Promoted from**: Hc_582 (cycle #3 task 11 PROMOTE_READY, verify5_authored row 3 — 2026-05-12)
- **Math verification**: 2^3 = 8 EXACT (Hc_582 의 "4-d" 는 errata, 정정함); sopfr(8) = 2+2+2 = 6 EXACT (perfect number); 2^4 = 16 EXACT (NOT 8 — errata 근거)
- **Errata catch**: verify5 F2 가 catch — Hc_582 frontmatter "4-d hypercube와 sopfr(8)=6" 의 arithmetic 오류 (2^4=16, 2^3=8). 본 H 가 정식 정정
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — sopfr-route 자체가 perfect-class trivial
- **Next steps**:
  1. DD144 doc 본문 errata audit + 정정 commit (C4 follow-through)
  2. sopfr-to-perfect K-table audit (F1)
  3. K-sweep ≥ 3 topology (F3, H_164.2)
  4. PyPhi replication (C3, F4)
