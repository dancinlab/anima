---
id: Hc_958
slug: qmirror-2-5-conds-cluster
title: qmirror 2.0 — 5 cond cluster (cond.10 GHZ-3 Mermin M=+4.0 / cond.11 Stabilizer 1.0 / cond.12 Surface code / cond.13 CSCS / others). Aer state-vector local $0 noiseless validation
domain: quantum-computing, validation
status: candidate-unverified
source_doc: docs/qmirror_2_cond10*.ai.md + docs/qmirror_2_cond11*.ai.md + docs/qmirror_2_cond12*.ai.md + docs/qmirror_2_cond13*.ai.md
source_lines: cluster
promoted_at: 2026-05-11
linked_h: Hc_914, Hc_944
notes: "qmirror 2.0 closure series. Each cond self-contained axis. $0 Aer state-vector local. Each cond F-QM-2-<NAME>-N falsifier."
---

## Hypothesis

qmirror 2.0 closure 의 5 cond 가 Aer state-vector local 에서 $0 노이즈없는 검증 통과: cond.10 GHZ-3 Mermin witness M=+4.0 (analytic max, classical bound 2.0 violated by 2.0 units), cond.11 Stabilizer-measurement (syndrome+ ratio 1.0, post_fidelity 1.0, ⟨ZZ⟩=+1, ⟨XX⟩=+1, ⟨YY⟩=-1), cond.12 Surface code, cond.13 CSCS, etc.

## Sub-claims

- cond.10 GHZ-3 Mermin: M=+4.0 analytic max, 30 trials × 1024 shots/basis PASS F-QM-2-GHZ-10
- cond.11 Stabilizer: syndrome_+ ratio 1.0 (all 4 axes), post_fidelity 1.0, 1792 shots PASS F-QM-2-STAB-11
- cond.12 Surface code: read source for details
- cond.13 CSCS: read source for details
- Aer-LOCAL: state-vector $0 noiseless
- SELF-CONTAINED: each cond independent axis

## Migration TODO

- [ ] cond.12 + cond.13 + remaining cond detail extract
- [ ] Aer state-vector regime 한계 (qubit count)
- [ ] noise model injection 후 결과 비교
- [ ] qmirror 2.0 full closure verdict
