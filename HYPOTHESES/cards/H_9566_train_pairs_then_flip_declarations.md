# H_9566 — 짝 훈련 후 선언-만 뒤집기 — Train-Pairs-Then-Flip-Declarations (sol A-S5 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=sol A-S5
**lane:** BINDING / two-lane · 최강 인과 판독
**related:** [[H_9562]] · [[H_9359]] · source: lab full R2-measure (sol A-S5)

## 제안 (Sol Lane-A 최강 판독 · R2)
**아이디어**: 짝 예제 먼저 훈련(다리 reader 생성 시도) → 그 뒤 **선언-만** 극성 뒤집기. 학습된 다리가 있으면 사후 선언 flip 이 연산자 짝 재훈련 없이 연산자 답을 이동. 연산자 저장소는 test 시 **무접촉** = 최강 다리 기준.
**메커니즘**: H_9562 파이프의 순서 arm — CPT1(짝)→CPT2(선언-만 flip)→연산자 재채점.
**판정**: 연산자 이동(≥10/12·≥2seed·p≤.01) = 런타임 다리 획득. 무이동 = H_9359 재현(다리 없음·per-stem 캐시).
**verdict-integrity**: H_9359 는 *짝 커리큘럼 없이* 이걸 했고 무이동(다리 없음). 이 카드는 *짝 커리큘럼 후* 재시험 — 짝이 reader 를 만들었나. 연산자-포함 라인이 CPT2 진입 시 INVALID.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9359(짝 없이 무이동)의 직접 후속 — 짝 커리큘럼이 reader 를 벌었는지 인과 검정.
