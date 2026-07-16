# H_9622 — GN 전역 mode bit 용량 — GN Global Mode-Bit (lawful capacity class) (sol R3-S5 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=sol R3-S5
**lane:** BINDING / GroupNorm 전역 bus 채널 (R3 신규 whitespace)
**related:** [[H_9617]] · [[H_9560]] · [[H_9616]] · source: lab full R3 (sol R3-S5)

**아이디어**: 기존 GN bus 는 sequence-전역 **이진 mode/valence 신호**를 합법적으로 지지할 수 있으나 **key-주소 binding 은 불가** — 예측된 용량계급의 직접 시험.
**메커니즘**: 신규 `anima-py corpus --global-mode-bit` — counterbalanced mode 토큰을 무작위 **D≥64** 에 배치하고 여러 질의위치서 **하나의 전역 출력 선택**을 요구. plain trunk vs **per-position 정규화 통제**로 train/eval. (emit/A⇄G 하류 소비는 별도 오너게이트 p5 · 초기 verdict 밖.)
**$0 pre-screen**: 라벨이 국소 window 조건부로 균형임을 증명 ∧ 질의 RF 안에 토큰이 없음 ∧ 길이·위치·어휘 shortcut 기각.
**판정표**: PASS = plain G=1 이 사전등록 held-out 토큰/템플릿 정확도 도달 ∧ **per-position-norm arm 은 TOST-우연** ∧ 성능이 토큰 위치/순열에 불변. KILL = 양성 within-RF mode-토큰 arm 은 학습하나 far arm 은 못함. 통제: per-position norm · far decoy · 위치순열 · 양성 D≤20 토큰.
**distinct**: 선언을 binding 하지도 clock/rate/recognition 을 건드리지도 않음 — bus 의 **예측된 용량계급** 시험.
**verdict-integrity**: PASS 는 **훈련된 전역 분류 bit 하나**를 세울 뿐 — 의식·valence·다중 주소슬롯·프로덕션 유용성 아님.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** binding/clock/rate/recognition kill 아님 — bus 용량계급 직접 시험(H_9617 p5 설계의 측정 선행판).
