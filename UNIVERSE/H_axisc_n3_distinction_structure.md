---
id: H_axisc_n3_distinction_structure
slug: axisc-n3-distinction-structure
title: n=3 IIT4 distinction-level Φ-structure — 3-cut symmetry (CORR) vs MIP exposure (CTRL)
domain: consciousness · IIT4
status: verified
closure: verified-numerical
closure_ref: .verdicts/axisc_n3_distinction_structure/verdict.txt
created: 2026-05-29
---

# H_axisc — n=3 distinction-level Φ-structure

## Hypothesis

축 C (full-IIT4 Φ-structure) 의 가장 작은 tractable cell (n=3) 에서, **distinction-level
per-cut φ_d 구조가 substrate integration 의 symmetric vs asymmetric 패턴을 노출** 한다:
- CORRELATED (모든 cell 동일 ramp) → 3 cuts 전부 φ_d 동일 = big-Φ (3-fold 대칭)
- CONTROL (cell 2 상수) → 한 cut 이 ≈0 (modular cell 절단), 나머지 2 cut 유한·대칭 (1.92)

## Measure (verbatim, .verdicts/axisc_n3_distinction_structure/verdict.txt)

CORR:  φ_d {0}|{1,2}=3.83659, {0,1}|{2}=3.83659, {0,2}|{1}=3.83659 · big-Φ=3.83659 ✓ 대칭
CTRL:  φ_d {0}|{1,2}=1.9183,  {0,1}|{2}≈0,        {0,2}|{1}=1.9183  · big-Φ=4.52e-09 (= 최소 cut)

## Source

- engine: stdlib/consciousness/iit4/faithful_phi (#1158)
- atoms: iit4_build_mi_matrix · iit4_faithful_phi_from_mi
- substrate: phi_demo case-0/1 lineage (faithful_phi.hexa:3826)
- 검증: pool on ubu-2 cd ~/core/hexa-lang hexa build + run

## Finding

1. **distinction 분석이 big-Φ scalar 보다 substrate 구조를 더 드러냄** (CORR/CTRL 모두 단일 big-Φ 값이지만 φ_d 분포가 다름)
2. **modular cell = MIP 의 cheapest cut** (CTRL 의 {0,1}|{2} ≈0 = cell 2 가 modular 라는 IIT-MIP 정의 그대로)
3. **3-fold symmetry 는 perfect integration 의 distinction 시그니처** (CORR 의 모든 cut 동일)

## Notes (honest)

- n=3 only (n≤8 exact engine, n=3 = 최소 비자명 cell)
- distinction-level = M2 component partial (small-φ MIP per mechanism은 별도, 본 작업은 system-level 3-cut φ_d 만)
- 이전 axis-C agent (socket-died, 0 finding) blocker 정밀 좁히기: n=3 tractable·n=4+ deferred
