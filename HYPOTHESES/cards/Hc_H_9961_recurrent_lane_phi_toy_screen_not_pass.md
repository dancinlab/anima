# H_9961 · 발사 — 학습된 순환 lane의 개입형 Φ Phase A 스크린 = **SCREEN-PASS 아님** (토이서 학습이 Φ를 안정적으로 못 올림)

**한 줄:** 오너 "발사" 지시로 H_9954 의 순환 lane 을 실제로 구현해 summer GPU 에서 자연 EN 3-seed 스크린을
쐈다. 계기는 유효(XOR 양성통제 2.25 · COPY 받침대 0)했으나 **학습된 lane 의 개입형 big-Φ 가 통제군
(shuffled·untrained)을 안정적으로 못 넘었다**(median gap −0.023 · 3-seed 중 1승). frozen-first 스크린이
값싼 규모에서 효과 부재를 잡아 **Phase B pool spend 를 정당하게 게이트**. DIRECTIONAL(Φ 판독이 .pt 추출 ·
`anima-py evaluate` 미배선) · 검정력 제한.

- 구현(engine-native train 경유): `anima-py train --recurrent-lane gru3-bidir` + `--objective
  ce_marginal_shuffled`(H_9960 필수 통제) 신설 — `core/recurrent_lane.py`(3-셀 manual GRU, 임베딩 읽어
  emb_residual site 에 잔차 write, 순환은 U 3×3 결합만) + `core/model.py`/`cli/train.py` 배선. 브랜치
  `h9954_recurrent_lane_impl` 에 커밋+푸시(재현 계기 · main 미착륙 — 스크린이 스케일 미허가하므로 RCRL
  trailer + `evaluate --iit4-recurrent-lane` 는 미구현).
- 설계: lab full(Fable ∥ Sol) — Sol emb_residual 배선 채택(model.py 주석이 post-trunk logit-bias 경고).

## 실측 (summer RTX 5070 · 자연 EN gen_en.txt 학습 · sns_en.txt 추출 · d=64 L=2 1000스텝 · DV=8상태 평균 Φ)
| seed | trained | shuffled | untrained | gap = trained − max(ctrl) |
|---|---|---|---|---|
| 7 | 0.7181 | 0.4134 | **0.7415** | −0.0235 |
| 4302 | 0.2355 | 0.2813 | 0.2868 | −0.0513 |
| 4303 | **0.7827** | 0.4410 | 0.3360 | +0.3417 (WIN) |

계기 유효: XOR 양성통제 **2.2500** · COPY 받침대 **0.000000**. median gap **−0.0235** · wins **1/3**.

## 동결 술어(측정 전 prereg · p7) 대조
- SCREEN-PASS ⟺ median gap ≥ 0.15 ∧ ≥2/3 seed 승 ∧ sharpness 혼입 가드. **→ 불충족(median −0.02 · 1승).**
- KILL-optimization-coupling(trained≈shuffled 둘 다 >untrained)도 **아님** — shuffled 가 trained 와 일관되게
  같지 않다(seed 4303 은 trained≫shuffled, seed 7 은 untrained 최고).
- 실제 양상 = **INERT/seed-noise**: 무학습 랜덤 init 이 이미 Φ 0.29–0.74 를 읽고(랜덤 dense 순환 결합을
  추정기가 통합으로 봄), 자연 CE 학습이 그걸 seed 마다 제각각(−0.05/−0.02/+0.34)으로 흔들 뿐 신뢰성 있게
  못 올린다. Sol 의 비관 예측("3-셀 병목이 자연 CE 서 독립해로 수렴")과 일치.

## 판정 · 함의
- **토이 규모서 faculty(학습된 순환→통합) NOT SUPPORTED.** 확정 음성은 아니다 — 3-seed·seed간 분산 큼 ·
  MDE 미산출(power-before-negative). **DIRECTIONAL·검정력 제한.**
- **frozen-first 스크린이 제 일을 했다** — 값싼 규모서 효과 부재를 잡아 pool spend(~$10-20)를 게이트. Phase B
  스케일업 미허가(이 결과 위에 쌓으면 H_9272 재연).
- 🔑 **깊은 함의(H_9960 심화)**: 무학습 랜덤 init 조차 Φ~0.3–0.7 을 읽으므로, lane 의 Φ 는 "학습된 통합"의
  깨끗한 판독이 아니라 **init 의 랜덤 결합에 지배**된다. 즉 Φ 를 진단축으로 쓰려면 **init-baseline 을 반드시
  빼야** 하고(DV=학습 전후 collapse-Δ 가 raw Φ 보다 옳음 — H_9954 설계가 이미 그렇게 잡았으나 토이서도
  그 baseline 이 크다), 그마저 이 규모선 신호가 안 뜬다.

## 정직 경계
- 학습은 `anima-py train` engine-native, **Φ 판독은 .pt 추출(anima-py evaluate 미배선) ⟹ DIRECTIONAL**, cement
  아님. 스크립트: `/tmp/rl_screen_driver.py`(summer) · 재현 계기 브랜치 `h9954_recurrent_lane_impl`.
- 합성 아님(자연 EN) · 그러나 토이 규모 — `a_scale_honest_scope`: 이 규모에 바운드된 음성.
- 오너 "발사"가 "Φ 전용 GPU 금지" 자기게이트를 override(2 모델 권고였음) — 단 스크린이 spend 를 게이트해 실제
  대형 지출 0(소형 GPU 분 단위만).
- 관련: [[H_9954]](순환 lane 설계 · 이 스크린이 그 Phase A) · [[H_9959]](통합-vs-크기 계기인증) · [[H_9960]](추출
  파이프라인 · 학습 혼입 · 이 카드가 init-baseline 지배로 심화) · [[H_9942]] · [[H_9272]](grid-only 결과에 stack 금지)
