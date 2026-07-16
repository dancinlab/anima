# H_9567 — 역순 방향성-RF 통제 — Reverse-Order Directional-RF Control (sol A-S6 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=sol A-S6
**lane:** BINDING / two-lane · CONV 방향성 통제
**related:** [[H_9562]] · source: lab full R2-measure (sol A-S6)

## 제안 (Sol Lane-A 통제 · R2)
**아이디어**: CONV reach 는 방향성 — 선언→연산자 vs 연산자→선언 은 별개 arm 으로 사전등록. 텍스트 역순은 방향성 RF reach 통제.
**메커니즘**: H_9562 corpus 의 순서 뒤집은 arm(선언 후치=postquery 와 다름: 여긴 전 텍스트 역순).
**판정**: 통제 — 한 방향만 PASS 면 방향성 결과(숨기지 말고 별도 보고). 양방향 대칭이면 비방향.
**verdict-integrity**: 양방향 짝 템플릿은 방향성 결과 은폐 위험 → 방향 사전등록 분리.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9562 의 방향성 통제 — CONV 국소 reach 의 비대칭 노출.
