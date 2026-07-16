# H_9613 — GN 순열불변 falsifier — GN Permutation-Invariance Falsifier (fable R3-A3 · R3 · PROPOSED)

**status:** 🔵 PROPOSED (미실행 · lab full 고갈-발산 R3 post-GroupNorm · 사전등록) — source=fable R3-A3
**lane:** BINDING / GroupNorm 전역 bus 채널 (R3 신규 whitespace)
**related:** [[H_9560]] · [[H_9564]] · [[H_9611]] · source: lab full R3 (fable R3-A3)

**아이디어(R3 지도 자체를 반증할 유일한 싼 테스트)**: GN 의 beyond-RF 기여는 **순열불변**이므로 beyond-RF 판독은 far-context **multiset 엔 민감**·**순서엔 불변**이어야 한다 — binding 이면 위반할 강한 아키텍처 예측.
**메커니즘**: `--dump-hidden`; 동일 근접문맥(≤RF) + far-context 를 순열(순서만) vs 재구성(multiset 변경) 비교.
**$0 pre-screen**: byte 거리 ≥RF 를 [[H_9564]] 정확-RF 로 단언 — arm 이 RF 안으로 새면 무효.
**판정표**: C1 **양성통제**=RF 내 순열은 h 를 **움직여야**(probe 가 순서를 볼 수 있음 증명) · C2 항등순열→byte-identical. 순서불변 ∧ multiset민감 = GN-bus 서명 확증. **beyond-RF 서 순서민감 ⟹ R3 지도가 틀림 = 미지의 채널 존재**(최고정보 결과).
**distinct**: 死한 margin/2AFC RF probe(미훈련 association confound) 아님 — 순열은 학습연관 불요한 **model-내 불변성** 시험.
**verdict-integrity**: 순서불변은 아키텍처가 *예측*하므로 확증은 near-vacuous — **가치는 오직 반증 가지**에 있다. 확증을 discovery 로 카드화 금지.

## 상태
🔵 PROPOSED — 미실행 사전등록. run 시 위 판정표로. 측정 주장 0(설계). **distinct-from-kills:** margin/2AFC RF probe kill 아님 — 학습연관 불요한 model-내 불변성 시험.
