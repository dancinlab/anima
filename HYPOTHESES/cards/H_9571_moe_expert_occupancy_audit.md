# H_9571 — MoE 전문가 점유 감사 — MoE Expert-Occupancy Audit (conditional-novel) (sol A-S10 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=sol A-S10
**lane:** BINDING / two-lane · $0 재분석(조건부 실행가능)
**related:** [[H_9359]] · [[H_1583]] · source: lab full R2-measure (sol A-S10)

## 제안 (Sol Lane-A 조건부 $0 · R2)
**아이디어**: 연산자 vs 선언에 대한 MoE 전문가 점유 — 물리적으로 다른 experts 면 두-lane 이 라우팅으로 분리됐다는 직접 증거. **단, production 303M 은 plain CONV(experts 없음)** — ConvMoE 는 sandbox/training 경로(#42492882·owner-gated).
**메커니즘**: $0 재분석 — **expert id/gate 가 trace 에 기록됐을 때만**. 없으면 INVALID/UNANSWERABLE(신 forward 금지).
**판정**: 상호배타 점유 = 진단(통신부재 증명은 아님·experts 가 trunk feature 공유 가능). 짝 예제서 공활성 = 통신 예측이나 현 trace 필드 불충분 가능.
**한계**: production 대상 없음(plain CONV) → ConvMoE 산출물 위서만·그건 DIRECTIONAL ceiling.
**verdict-integrity**: sandbox 숫자를 production verdict 로 승격 금지(영구 DIRECTIONAL). trace 에 expert 필드 없으면 KILL 아닌 INVALID.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_1583(expert-routing top2)의 $0 감사 판 — 단 plain-CONV production 엔 experts 부재라 sandbox 한정 DIRECTIONAL.
