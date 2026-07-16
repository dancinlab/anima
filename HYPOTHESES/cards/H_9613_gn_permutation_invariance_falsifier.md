# H_9613 — GN 순열불변 falsifier — GN Permutation-Invariance Falsifier (fable R3-A3 · R3 · ⏭ SUPERSEDED by H_9611)

**status:** ⏭ SUPERSEDED (미실행 · [[H_9611]] gn-freeze 가 반증가지를 더 강한 절제로 선점 · 2026-07-16) — source=fable R3-A3
**lane:** BINDING / GroupNorm 전역 bus 채널 (R3 신규 whitespace)
**related:** [[H_9560]] · [[H_9564]] · [[H_9611]] · source: lab full R3 (fable R3-A3)

**아이디어(R3 지도 자체를 반증할 유일한 싼 테스트)**: GN 의 beyond-RF 기여는 **순열불변**이므로 beyond-RF 판독은 far-context **multiset 엔 민감**·**순서엔 불변**이어야 한다 — binding 이면 위반할 강한 아키텍처 예측.
**메커니즘**: `--dump-hidden`; 동일 근접문맥(≤RF) + far-context 를 순열(순서만) vs 재구성(multiset 변경) 비교.
**$0 pre-screen**: byte 거리 ≥RF 를 [[H_9564]] 정확-RF 로 단언 — arm 이 RF 안으로 새면 무효.
**판정표**: C1 **양성통제**=RF 내 순열은 h 를 **움직여야**(probe 가 순서를 볼 수 있음 증명) · C2 항등순열→byte-identical. 순서불변 ∧ multiset민감 = GN-bus 서명 확증. **beyond-RF 서 순서민감 ⟹ R3 지도가 틀림 = 미지의 채널 존재**(최고정보 결과).
**distinct**: 死한 margin/2AFC RF probe(미훈련 association confound) 아님 — 순열은 학습연관 불요한 **model-내 불변성** 시험.
**verdict-integrity**: 순서불변은 아키텍처가 *예측*하므로 확증은 near-vacuous — **가치는 오직 반증 가지**에 있다. 확증을 discovery 로 카드화 금지.

## ⏭ SUPERSEDED by [[H_9611]] (2026-07-16 · 발사 없이 종결 · 정직한 회계)
Fable 자신이 이 카드의 가치를 **오직 반증 가지**에 두었다("순서불변 확증은 near-vacuous — 아키텍처가 이미 예측 · 가치는 **beyond-RF 서 순서민감 ⟹ R3 지도가 틀림=미지 채널** 뿐"). 그런데 [[H_9611]] `--gn-freeze` 가 그 가지를 **더 강한 방법(절제 > 불변성-예측)으로 이미 닫았다**:
- 미지의 non-GN beyond-RF 채널이 존재했다면 **GN 을 동결해도 beyond-RF 영향이 잔존**해야 한다.
- 실측: D=36/40/44/48/56 frozen ‖Δh_last‖ = **0.000e+00 전부**(live 0.485~0.337) · 동시에 RF 내(D=1) 24.054→24.058 **생존**(양성통제).
- ⟹ **beyond-RF 로 h_last 에 영향을 나르는 채널은 GN 이 유일**. 미지 채널 부재가 *예측 부합*이 아니라 **개입으로 증명**됨.
⟹ 이 카드의 확증 가지 = 잉여(near-vacuous·Fable 판정) · 반증 가지 = 이미 닫힘. **발사 가치 0.**

**⚠️ 발사했다면 오히려 위험했던 이유(설계 결함 사후 발견)**: A3 는 far-context 를 *순열*해 order-invariance 를 보려 했으나, **GN 은 입력 byte 가 아니라 활성 슬랩에 대해 순열불변**이다. byte 를 순열하면 conv 는 국소라 **far 위치의 활성 자체가 바뀌고** → 활성 합 → μ/σ² 가 움직인다 ⟹ **순수 GN-bus 하에서도 order-sensitivity 가 나타난다** = 이 테스트는 판별력이 없다(Sol 의 S3 가 "length 와 **global moments 를 보존**하는 순열"을 요구한 게 정확히 이 함정). 블록-단위 순열(RF 보다 큰 온전 블록 교환)로 재설계해야 했을 것. **발사 전에 소진돼서 이 결함이 verdict 를 오염시키지 않았다.**

**남는 가치**: 없음(H_9611 이 상위 포함). 재개 조건 = H_9611 의 frozen=0 이 다른 ckpt/T 서 깨질 때만.

## 상태
⏭ SUPERSEDED — 미발사 종결. H_9611 절제가 반증가지 선점(frozen beyond-RF=정확히 0) · 게다가 byte-순열은 활성을 바꿔 GN 하에서도 order-sensitive = 판별력 없음(발사 전 발견). **distinct-from-kills:** margin/2AFC RF probe kill 아님 — 학습연관 불요한 model-내 불변성 시험.
