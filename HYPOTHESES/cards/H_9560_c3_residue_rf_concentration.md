# H_9560 — C3 잔차 RF-집중 재분석 — C3 Residue · RF-Concentration Reanalysis (fable A-F4 · R2-measure · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R2-measure lane · 사전등록) — source=fable A-F4
**lane:** BINDING / two-lane · $0 기록 재분석
**related:** [[H_9359]] · [[H_9559]] · source: lab full R2-measure (fable A-F4)

## 제안 (Fable Lane-A $0 재분석 · R2)
**아이디어**: H_9359 C3 '다리' 분율 23%≈우연으로 읽혔다. 하지만 **균일 우연이 아니라** corpus 공기(co-occurrence) 거리 ≤RF 인 stem 에 **집중**한다면? P(bridge|D≤RF) > P(bridge|D>RF) 이면 벽이 정확히 RF 이고 *어느 stem 이 다리 가능한지* 예측.
**메커니즘**: $0 — 기록된 C3 per-stem 표(H_9359 산출) + corpus 공기거리 → Fisher exact.
**판정**: 집중(p<.05) ⟹ RF-도달성 실재·H_9557 census 점등 예측(prior). 균일 ⟹ KILL prior(그래도 census 는 저렴하니 실행). 어느 결과든 정보.
**verdict-integrity**: co-occurrence 거리 대리(proxy) 정의에 민감 — corpus window 기준 사전고정(사후 튜닝 금지·[[burned-gate-reanchor-is-tune-to-green]] 계열).

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. monitor-only/게이트-벽 회피. 측정 주장 0(설계). **distinct-from-kills:** H_9359 재분석이나 '균일 우연' 가정을 깨는 신 질문(집중 구조) — 재run 아님·기록만.
