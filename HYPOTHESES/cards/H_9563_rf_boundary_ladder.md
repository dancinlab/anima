# H_9563 — RF±δ 경계 사다리 — RF Boundary Ladder (D=RF±δ breakpoint) (sol A-S2 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=sol A-S2
**lane:** BINDING / two-lane · 국소성 경계 진단
**related:** [[H_9562]] · [[H_9559]] · source: lab full R2-measure (sol A-S2)

## 제안 (Sol Lane-A 발산 · R2)
**아이디어**: D=RF±δ 사다리 — 계산된 RF 근처 **breakpoint** 는 벽을 '국소성-속박'으로 재특성화(일반 '문맥 더=도움' 효과와 구별되는 날카로운 도달성 경계).
**메커니즘**: H_9562 corpus 의 `--rf-distance` 를 RF−2δ..RF+2δ 미세 배열로. inside/outside 이진 대비보다 경계 위치를 측정.
**$0 pre-screen**: 각 δ 계단의 인과 의존구간 분류(H_9562 게이트 상속).
**판정**: RF 근처 급강하(sigmoid breakpoint CI 가 계산 RF 포함) ⟹ 국소성-벽 확증. 완만/무경계 ⟹ RF 모형 약화.
**verdict-integrity**: 다중 δ = 다중 비교 → 사전등록 breakpoint 위치, 사후 이동 금지.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9562 의 이진 inside/outside 를 연속 경계로 정밀화 — 벽=arch-class 아닌 거리-국소성 직접 측정.
