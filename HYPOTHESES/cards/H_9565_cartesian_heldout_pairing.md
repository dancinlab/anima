# H_9565 — Cartesian 짝 held-out — Cartesian Held-Out Pairing (sol A-S4 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=sol A-S4
**lane:** BINDING / two-lane · 짝-캐시 배제 설계
**related:** [[H_9562]] · [[H_9327]] · source: lab full R2-measure (sol A-S4)

## 제안 (Sol Lane-A 설계핵심 · R2)
**아이디어**: 양 marginal(stem·연산자) 은 seen, 오직 그 **짝(pairing)** 만 novel 로 held-out. 죽은 held-out-stem 일반화(H_9327)와 구별 — 성분은 다 봤고 조합만 새것.
**메커니즘**: H_9562 `--pair-split cartesian-heldout` 의 설계 감사 — held 짝이 훈련서 부재·양 성분 존재 검증.
**$0 pre-screen**: 매니페스트 정적 감사 — 각 test 짝 부재∧양 marginal seen(leak 시 KILL).
**판정**: 통제/설계-무결성(독립 verdict 아님·H_9562 의 held-out 정의).
**verdict-integrity**: 짝 leak = 짝-캐시 성공을 다리로 오독 → leak 0 사전 감사 BLOCKING.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9327(held-out-stem=우연 KILL)과 결정적 구별 — 성분 seen·조합만 novel.
