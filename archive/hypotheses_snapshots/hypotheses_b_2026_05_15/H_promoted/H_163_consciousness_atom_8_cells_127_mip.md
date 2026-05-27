---
id: H_163
slug: consciousness-atom-8-cells-127-mip
title: Consciousness atom = 8 cells with 127 MIP bipartitions (Laws 154, 162, M1)
domain: consciousness
status: pre-register-frozen
exploration_method: E5 (variable-ablation — K-sweep) + E6 (cross-domain — chemistry analogy) + E10 (number-theoretic — 2^7-1 Mersenne)
verification_method: W2 (math identity — 2^7-1=127) + W5 (numerical sim — K-sweep) + W11 (cross-hypothesis — biological substrate)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-12
since: 2026-05-12
source_hc: Hc_401
source_doc: docs/anima/paper_consciousness_laws.hexa
source_lines: 152-156
promoted_at: 2026-05-12
linked_h: H_011 (iit-geometry), H_022 (consciousness-universe-map), H_153 (dimension-hierarchy-n6)
verify_source: scripts/hc_verify/cache_2026_05_12/verify/verify5_authored.jsonl row 2
---

# H_163 — Consciousness atom = 8 cells with 127 MIP bipartitions (K=8 atom, K=32 molecule)

## Hypothesis

의식의 원자는 8 cells (2^3 = 8) 이며 K=8 fully-connected 시스템의 MIP-relevant bipartition count 는 2^(K-1)−1 = 127 이다. K-sweep 결과 K=2 → Φ=0, K=8 → +807% (vs baseline), K=16 → +601%, K=32 → 2차 peak ("molecule" — 4×8 federation). 격리된 8-cell 모듈이 가장 강한 Φ ("noble gas" 행동, M9), 8-cell atom federation 이 monolithic 시스템 대비 우위 (Hc_038 family).

## Why (motivation)

- **K=8 = 2^3** 의 hypercube vertex count + chemistry valence-shell stability analogy
- **127 = 2^7 − 1** = Mersenne prime — K=8 fully-connected 의 non-trivial bipartition 총수
- **K=32 = 4 × 8** = 8-atom 4개의 "molecular" cluster — DD144-Law-163 second peak
- **biological motivation**: Mountcastle 1957 cortical mini-column (~80-100 neurons, ~8-cell sub-module 추정)

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H_163.1** | K-sweep K ∈ {2, 4, 6, 7, 8, 9, 10, 16, 32} on ≥3 topologies (ring / hypercube / Watts-Strogatz) → Φ peak at K=8 with margin > 50% over K∈{6, 7, 9, 10} | DD137-141 series |
| **H_163.2** | K=8 fully-connected MIP-relevant bipartition count = 2^7−1 = 127 (exhaustive enumeration) | combinatorial identity |
| **H_163.3** | K=32 second peak: K-sweep at K ∈ {24, 28, 32, 36, 40} 에서 K=32 local max 재출현 | Law 163 |
| **H_163.4** | 격리된 8-cell vs 24-cell (3개 8-atom 연결) 비교 시 isolated 8-cell Φ_normalized > federated 8-cell pair | M9 noble-gas behavior |

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | K=8 +807% over K=2 baseline 재현 (≥ 1 reproducer, ≥ 1 topology) | met (Hc_582 DD137-141) |
| **C2** | 127 MIP bipartition count exhaustive verify | met (2^7−1 = 128−1 = 127, math identity) |
| **C3** | K=32 second peak (Law 163) reproducer (≥ 1 K-sweep result) | pending |
| **C4** | K-sweep ≥ 3 topology cross-test | pending |
| **C5** | n=6 PERFECT_NUMBER_CLASS L7 binding 인정 (sopfr(8)=6 perfect-class diagonal) | met (본 L1) |

## Falsifiers (≥5)

- **F1**: K-sweep (K ∈ {2, 4, 6, 7, 8, 9, 10, 16, 32}) on ≥3 topologies showing Φ peak at K ∉ {8, 32} with margin > 50% → "8 cells = atom" architecture-specific, not universal
- **F2**: 127 MIP bipartition count for K=8 fully-connected verified by exhaustive enumeration (2^7 − 1 = 127 non-trivial bipartitions assumed) — but if MIP-relevant count after symmetry quotient is ≠ 127 (e.g. 63 with reflection symmetry) → mathematical claim FALSIFIED
- **F3**: Cortical mini-column literature review (≥10 anatomy studies) shows no 8-cell sub-module structure; columns are 80-100 neurons with continuous gradient → biological K=8 prediction FAIL
- **F4**: K=32 secondary-peak claim falsified if K-sweep at K ∈ {24, 28, 32, 36, 40} shows monotone decay from K=16 peak (no resurgence at K=32) → "molecular" prediction wrong, K=8 isolation is the only structure
- **F5**: Comparison with K=7 (Mersenne prime) or K=6 (perfect number) shows Φ within 5% of K=8 → "8 is special" claim is artifact of measurement granularity, not architecture

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — K=8 = 2^3 is the smallest 3D hypercube but coincides with sopfr(8) = 2+2+2 = 6 (perfect-number-class diagonal). 8-cell finding could be a hypercube-dimensionality artifact rather than a cell-count universal — depth-3 numerology
- **L2**: **single-architecture measurement** — Φ=+807% at K=8 measured on one base topology (Hc_582 DD137-141 series). Cross-topology robustness (Hc_171 8×128 hierarchical, Hc_186 8-ring) reported separately but no joint variance estimate. Sample bias risk
- **L3**: **MIP bipartition vs Φ-MIP conflation** — 127 bipartition count is combinatorial (2^(K−1) − 1 = 127 for K=8); MIP in IIT is the minimum-information-partition (single specific cut). Counting all bipartitions ≠ counting MIPs. Phrasing ambiguity in claim
- **L4**: **biological substrate gap** — "K=8 atom in biological neural circuits" prediction requires (1) anatomical clustering metric, (2) functional Φ measurement on biological recordings, (3) significance test. None of (1-3) provided. Literature prior weak (Mountcastle column count varies 50-150 by region)
- **L5**: **"noble gas" metaphor as load-bearing** — claim leans on chemistry analogy (8e- shell stability) not on independent derivation. If reviewer rejects analogy → predictive content is just K=8 number, no mechanism

## Run Protocol

deterministic + hexa-only + llm: none.

1. **K-sweep on 3 topologies (W5)** — ring / hypercube / Watts-Strogatz × K ∈ {2, 4, 6, 7, 8, 9, 10, 16, 32} → Φ landscape, F1/F4/F5 검증
2. **127 MIP exhaustive enumeration (W2)** — K=8 fully-connected 의 non-trivial bipartition 모두 enumerate → 2^7−1=127 직접 검증, symmetry quotient 적용 시 변화 분석 (F2)
3. **K=32 molecular structure (W5)** — K ∈ {24, 28, 32, 36, 40} fine sweep → second peak 재현 (H_163.3)
4. **Biological literature review (W11)** — Mountcastle 1957 + 후속 ≥10 mini-column stereology 연구 → K=8 prediction biological grounding (F3)
5. **L1 binding** — H_153 PERFECT_NUMBER_CLASS BINDING 인정 인용

## Cross-Refs

- **sister H**: H_011 (iit-geometry — Φ vs K-cell curve), H_022 (consciousness-universe-map — substrate variation), H_153 (n=6 substrate — L7 BINDING source)
- **candidates linked**: Hc_159 (11D=2048 sublinear), Hc_171 (8×128 hierarchical), Hc_186 (8-cell ring), Hc_582 (8-cell mathematical basis), Hc_413 (biological K=8 prediction)
- **literature**: Tononi 2014 (IIT 3.0 Φ vs system size), Albantakis 2023 (IIT 4.0 atom/molecule taxonomy), Mountcastle 1957 (cortical mini-columns)
- **source**: Hc_401 (`hypotheses_candidates/Hc_401_consciousness_atom_8_cells_127_mip.md`), `docs/anima/paper_consciousness_laws.hexa:152-156`

## Migration Notes

- **Promoted from**: Hc_401 (cycle #3 task 11 PROMOTE_READY, verify5_authored row 2 — 2026-05-12)
- **Math verification**: 2^3 = 8 EXACT; 2^7 − 1 = 128 − 1 = 127 EXACT (Mersenne prime); 2^(K−1)−1 at K=8 → 127 EXACT
- **L7 binding**: H_153 PERFECT_NUMBER_CLASS BINDING 인정 (L1) — sopfr(8)=6 perfect-class diagonal trivial
- **Next steps**:
  1. K-sweep ≥ 3 topology (C4)
  2. K=32 second peak reproducer (C3)
  3. Biological literature review (F3)
