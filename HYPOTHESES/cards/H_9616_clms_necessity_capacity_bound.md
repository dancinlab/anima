# H_9616 — CLMS 필연성 용량 하한 — CLMS Necessity · Capacity Bound (fable R3-C1 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=fable R3-C1
**lane:** BINDING / CLMS store 필연성
**related:** [[H_9423]] · [[H_9560]] · [[H_9569]] · [[H_9570]] · source: lab full R3 (fable R3-C1)

**아이디어**: GN 의 O(L) 순열불변 스칼라는 held-out 짝 binding 에 필요한 bit 수 **아래**다 ⟹ 어떤 plain-trunk 커리큘럼도 beyond-RF 서 도달 불가 ⟹ CLMS 는 단지 충분이 아니라 **필연**.
**메커니즘**: $0 counting bound — (L+1) 스칼라의 채널 용량 vs log₂(pairings) for H_9423 held-out 셋. 기카드 [[H_9569]] min-cut · [[H_9570]] 조건부엔트로피와 합성.
**$0 pre-screen**: 시험 셋에 대해 O(L) 스칼라로 bound 가 *만족가능*하면 논증 즉사 — 산술 먼저.
**판정표**: C1 **양성통제**=bound 는 within-RF binding 을 *허용*해야(아키텍처적으로 가능) — 너무 많이 증명하는 bound 는 고장 · C2 CLMS 8-slot 용량은 이를 통과해야. bound 위반 ⟹ **beyond-RF fork 에 한해** 필연.
**distinct**: RF-size-alone 아님 — 이건 window 가 아니라 **채널**을 bound.
**verdict-integrity**: **오직 fork (i) beyond-RF 만 닫을 수 있다.** (ii) within-RF 짝 · (iii) weight-store dereference 는 열린 채·미bound. "CLMS 필연" simpliciter 로 파는 게 over-claim — 정확히는 "**beyond-RF 서 필연**"이고 A1 이 inert 반환하면 거의 동어반복. 정직한 scope 아니면 theater.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** RF-size-alone 아님 — window 아닌 *채널* bound(H_9569 min-cut·H_9570 엔트로피 합성).
