# H_9568 — 교차저장소 MI + 순열 null — Cross-Store MI + Permutation Null (sol A-S7 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=sol A-S7
**lane:** BINDING / two-lane · $0 측정 + 위조통제
**related:** [[H_9561]] · [[H_9359]] · source: lab full R2-measure (sol A-S7)

## 제안 (Sol Lane-A $0 측정 · R2)
**아이디어**: 기존 trace 서 교차저장소 MI 측정 + **선언-값 순열 null**(stem 내 선언값 뒤섞기) = cross-store MI 의 위조통제. 연산자-템플릿 순열은 공동-binding vs 템플릿-캐시 학습 구별.
**메커니즘**: $0 — 기록 trace 통계 MI + 순열 null. 결합확인, 런타임 읽기 증명은 아님(association≠causation).
**판정**: MI>null(p<.01) ∧ 조건부(stem·클래스) 유지 ⟹ 결합 존재(다리 후보). 순열서 사라짐 = 위조 배제. **한계**: 측정은 결합만, 런타임 읽기는 H_9562/H_9566 이 인과 시험.
**verdict-integrity**: MI 를 '다리'로 승격 금지(association) — 인과는 개입(이식)만. 참값0 pedestal.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9561(≤RF MI 하한)의 자매지만 *순열 null* 로 위조통제 추가 — association 을 causation 으로 오독 방지.
