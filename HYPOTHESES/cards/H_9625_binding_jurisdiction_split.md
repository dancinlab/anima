# H_9625 — binding 관할 분할 — Binding Jurisdiction Split (reframe) (sol R3-S8 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=sol R3-S8
**lane:** BINDING / frontier 재프레임 (관할 분할)
**related:** [[H_9562]] · [[H_9423]] · [[H_9560]] · source: lab full R3 (sol R3-S8)

**아이디어(재프레임)**: 최전선을 **plain trunk = 국소 조합 파싱** vs **CLMS = 주소가능 작업기억**으로 **관할 분할**하고, 한 메커니즘이 둘 다 풀길 요구하지 말자.
**메커니즘**: 신규 아키텍처 0 — `anima-py evaluate --xbind` 로 **2축 engine-native 벤치마크** 등록: D≤20 국소 held-out 짝 · D≫35/슬롯수 주소 조회, 각 성분 **개별 채점**.
**$0 pre-screen**: 기존 재조합 항목 전부를 거리 × 주소-cardinality 로 매핑 · 라벨이 **어느 한 marginal 만으로 복원되면** 벤치마크 기각.
**판정표**: **PASS-reframe** = plain 이 [[H_9562]] 후 국소 짝은 이기나 원거리 무작위 주소서 우연 유지 ∧ CLMS 가 원거리 주소를 이김. **KILL-reframe** = 어느 native arm 이 둘 다 이김. 통제: seen-pair 양성 · exact-copy 양성 · wrong-key 음성 · 거리매칭 비-binding 문맥.
**distinct**: capability-budget 이나 "그냥 메모리 추가" 아님 — **매핑된 통신 그래프 기반**으로 경험적 분리가능한 관할 배정.
**verdict-integrity**: 벤치마크 분리는 **공학적 분해**지 재조합이 의식에 필요/충분하다는 증거 아님.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** capability-budget/'메모리 추가' 아님 — 매핑된 통신그래프 기반 경험적 관할 배정.
