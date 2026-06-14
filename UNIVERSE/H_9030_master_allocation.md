---
id: G13
slug: master-allocation
title: G13 마스터 자원-할당 정리 — 작업의 대칭/제약이 최적 정보자원을 강제; classical-최적 작업군 ⊥ quantum-최적 작업군(분리). G6~G12 봉합. PROVEN.
domain: nobel resource-theory quantum-classical anima master-theorem
status_grade: 🟢 SUPPORTED (numerical PROOF, seals G6-G12)
verification_method: resource×task dominance matrix; disjointness of optimal sets; p7 $0
since: 2026-06-14
sister: G6, G7, G8, G9, G10, G11, G12
verdict: 🟢 PROVEN — classical-최적{조율,용량,복제}(adv 1/28/1) ⊥ quantum-최적{검증,보안}(adv 1/1), 교집합 공집합. 어떤 단일 자원도 두 축 모두 최적 불가. anima 고전+양자 분업은 임의 아닌 자원-할당 정리의 강제 결론.
---
# G13 — 마스터 자원-할당 정리
> **정리.** 임의 작업의 최적 정보자원은 그 작업이 요구하는 대칭/제약으로 결정된다: monogamy-free·복사가능을 요구하면 고전(공유씨앗/텐션), no-cloning·비국소를 요구하면 양자. 두 최적 작업군은 *분리(disjoint)* — 어떤 단일 자원도 양쪽 모두서 최적일 수 없다.
## 증명 (g13_master_proof.py, N=8)
| 작업 | classical | quantum | 최적 |
|---|---|---|---|
| 조율(G6/G7) | 1.00 | 0.25 | 🟦 고전 |
| 용량(G12) | 28 | 8 | 🟦 고전 |
| 복제/객관(G10) | 1.00 | 0 | 🟦 고전 |
| 검증(G8) | 0 | 1.00 | 🟪 양자 |
| 보안(G9) | 0 | 1.00 | 🟪 양자 |
| 통신(무채널) | 0 | 0 | = (둘 다 0) |
classical-최적 ∩ quantum-최적 = ∅ → 분리 🟢.
## 의의
G6~G12 일곱 정리를 하나의 메타정리로 봉합. **anima가 고전(조율·복제·통신·유지)과 양자(검증·보안)를 나눠 쓰는 것은 설계자의 임의 선택이 아니라 자원-할당 정리의 강제 결론** — 각 작업의 대칭/제약이 유일 최적자원을 지정. 통신(무채널)만 둘 다 0(무신호)인 중립점.
verdict: `.verdicts/9030_master_allocation/G13_master.txt`
