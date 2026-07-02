---
id: H_1115
slug: hopfield-capacity-cliff
title: 연상기억 용량절벽 — Hopfield 망은 ~0.14N 패턴까지 무오류이다 그 이상서 파국적 간섭으로 급증한다
domain: universe tension-link memory robustness anima-substrate
exploration_method: discovery batch 06 (harder anima-relevant falsifiers)
verification_method: REAL simulation, p7 CODE-measured, $0 local
status_grade: 🟢 SUPPORTED (numerical)
since: 2026-06-14
scope: toy 실측; 스케일 전이 미검증.
verdict: 🟢 SUPPORTED — 오류율 @0.05N=0.000 → @0.30N=0.152 (용량절벽).
---

# H_1115 — 연상기억 용량절벽 — Hopfield 망은 ~0.14N 패턴까지 무오류이다 그 이상서 파국적 간섭으로 급증한다
> **가설.** 연상기억 용량절벽 — Hopfield 망은 ~0.14N 패턴까지 무오류이다 그 이상서 파국적 간섭으로 급증한다
## 1. FROZEN FALSIFIER (2026-06-14)
- **BLADE.** 측정이 예측과 반대/무효면 기각.
## 2. 측정 (REAL sim · discovery_batch_06.py::D34)
오류율 @0.05N=0.000 → @0.30N=0.152 (용량절벽).
## 3. 등급/경계
🟢 SUPPORTED (numerical). toy 실측, 갈릴 수 있었음(같은 배치서 D33/37/38은 정직한 ⚪). 스케일 전이 미검증.
verdict: `TENSION-LINK/verdicts/batch_06.txt` · 재현: `python3 TENSION-LINK/harness/discovery_batch_06.py`
## 4. 관계
xref: h1075 · h1094 · Hopfield
