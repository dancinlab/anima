# H_9624 — 매칭 커리큘럼 아키텍처 레이스 — Matched-Curriculum Architecture Race (sol R3-S7 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=sol R3-S7
**lane:** BINDING / CLMS store 필연성
**related:** [[H_9623]] · [[H_9562]] · [[H_1584]] · [[H_9423]] · source: lab full R3 (sol R3-S7)

**아이디어**: **동일 데이터·최적화 예산·파라미터 기회** 하에서 CLMS 가 plain trunk 대비 held-out 짝 우위를 **커리큘럼 풍부화에도 사라지지 않게** 유지하나.
**메커니즘**: `anima-py corpus --rf-paired-bridge` 요인 커리큘럼 사다리 + `anima-py train --binding-architecture {plain,clms,param-matched-null}` (동결 seed/예산) → Cartesian-held-out 짝을 inside·outside RF 양쪽서 평가.
**$0 pre-screen**: H_9423/H_9562 파일럿 산출물서 **학습곡선 검정력 분석** · arm 이 예제수·스텝·optimizer 노출·유효 학습파라미터서 다르면 기각.
**판정표**: **PASS-relative-necessity** = CLMS 가 고정 target 을 전 seed 서 통과 ∧ plain 과 **param-matched-null 둘 다** 전 사전등록 예산서 TOST-미달 ∧ plain 은 seen-pair readback·local-copy 양성엔 성공. **KILL-necessity** = plain 이 **어느 동결 arm 서든** held-out inside-RF binding 통과. 통제: param-matched 비-주소 모듈 · seen-pair readback · local-copy 양성 · label-shuffled 음성 · outside-RF arm.
**distinct**: H_1584 는 깊이 변경 — 이건 **매칭 아키텍처 통제 하 커리큘럼 풍부화**를 변화 · H_9562 와 달리 명시 store 와 **직접 레이스**.
**verdict-integrity**: **유한 스윕은 "아무리 풍부한 커리큘럼도 불가"를 증명 못함.** 합법 최강 verdict = **예산·커리큘럼-가족 한정 필연**. 보편적인 건 아키텍처적 D>RF 결과뿐.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** H_1584(깊이) 아님 — 매칭 통제 하 커리큘럼 풍부화 변화 · 명시 store 와 직접 레이스.
