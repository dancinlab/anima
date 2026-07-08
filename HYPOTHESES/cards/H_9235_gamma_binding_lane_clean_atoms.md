# H_9235 — ⚗️ γ binding-lane on clean atoms — G1 operator 유일 잔여 engine 레버 (사전등록·GPU spend-gated)

**tier**: ⏳ PRE-REGISTERED (frozen-first · 발사=오너 spend-go 대기) · 부모 [[H_9234]] (operator=readout-arch 국한 확증) · [[H_9211]] (#3135 blind-atom 붕괴)

## 왜 이게 유일 잔여 레버인가
H_9234가 operator 필요조건 **2개**를 격리: **① interaction readout**(attention/MLP=1.00) ∧ **② clean/separable atom**.
- ①은 clean atom 위에서 증명됨(토이 1.00).
- ②는 #3135 kill-shot이 실 byte-LM **learned atom=blind → 붕괴** 확인.
- ⟹ 남은 단 하나의 미검 질문: **학습으로 atom을 interaction lane이 쓸 만큼 clean하게 만들 수 있나** (= γ trained-constructive-bind, #3108 재프레임). 이건 GPU 학습이라 $0 아님 → spend-gate.

## 사전등록 스펙 (frozen-first · a_no_tune_to_green)
**H1 (atom-cleanness probe · 선행 $0-이지만-heavy pool)**: 실 303M `clm303.clm` concept-atom hidden에 **linear probe**로 atom-identity 복원 가능한가.
- FROZEN: linear-probe held-out atom acc ≥0.80 (clean) → γ 발사 정당 / <0.55 (blind, #3135 재확인) → γ도 terminal, 발사 NO-GO.
- 경로: `anima evaluate --py <clm> --probe` 계열 hidden 추출 → numpy linear probe. pool(summer/aiden), mini 금지(303M OOM).

**H2 (γ binding-lane 학습 · GPU spend-gated · H1 PASS 후만)**: additive nearest-basin readout → **trained bilinear/tensor-product bind operator** 교체 후 303M engine-native G1 재측정.
- FROZEN: engine-native G1 held-out recombination ≥ frozen a303m_pass bar ∧ shuffle-control 붕괴 ∧ seen≈held gap 축소. tune-to-green 금지(frozen bar 선동결).
- 통제: additive-baseline(현 .clm) · blind-atom ablation(#3135 재현) · attention positive control.
- scope: 성공해도 a_scale_honest_scope(측정 rung 한정). 실패=결과(negative 박제).

## 비용/발사 게이트
GPU 학습 fire = rent=spend → **오너 go 필요**(a_fire_autonomous fleet/spend caveat). H1(cleanness probe)은 pool decode라 상대적 저비용 — 오너 go 시 H1부터.

## 예측 (modal)
#3135(blind atom)·#3108(γ DUP-WALLED)로 보아 **H1이 blind(<0.55)로 나와 γ도 terminal**일 공산. 그러나 H_9234가 "clean atom이면 interaction이 operator를 완벽히 짓는다"를 새로 확증했으므로, atom-cleanness가 **학습 curriculum으로 개선 가능**하다면(mitosis/savant lane [[mitosis-substrate-lane-wired]]) 유일한 real crack 후보. H1이 그 갈림을 $0-heavy로 결정.

## 맥락
[[H_9234]] operator-vs-association 종결(#3166): fuel≠operator·벽=additive-readout 국한. 싼 레버 전수 소진 후 유일 잔여 engine 경로=이 γ lane. 발사 전 [[check-ledger-before-lever-fire]] 준수(#3135·#3108 이미 검토).
