# H_9962 · 스케일 축 — 학습된 순환 lane의 Φ 이득은 스케일에 안 자란다(오히려 약해진다): 음성이 scale-robust

**한 줄:** H_9961(토이 d=64/L=2)이 "학습된 순환 → Φ 증가"를 약한·유의하지-않은 양성(6-seed mean +0.055)으로
남겼고, 그게 스케일-한정인지 실재인지 가르려 오너 "발사" 하에 **d=512/L=8**(폭 8×·깊이 4×)로 같은 from-scratch
자연 EN 레짐을 발사했다. **스케일을 올리니 gap이 자라기는커녕 음수로 갔고(mean −0.023), 학습이 무학습 init
baseline 을 단 한 seed 도 못 넘었다(0/3).** ⟹ 음성이 **scale-robust** — 스케일은 이 lane 의 Φ 레버가 아니다.
오너의 "303M 학습시" 질문에 대한 강한 실측 답: **감당 가능한 스케일 범위(d=64→512)서 학습이 Φ를 못 올리고,
스케일↑ 일수록 약해진다.**

- 계기: `anima-py train --recurrent-lane gru3-bidir`(+`ce_marginal_shuffled` 통제) · summer RTX5070 · 자연 EN
  gen_en.txt 학습·sns_en.txt 추출 · DV=collapse-Δ − untrained baseline · Φ판독 .pt 추출 = DIRECTIONAL.

## 스케일 대조 (같은 계기·같은 DV·같은 corpus, d 만 변화)
| | 토이 d=64 L=2 (6-seed) | **스케일 d=512 L=8 (3-seed)** |
|---|---|---|
| mean DV_gap (trained−shuffled) | +0.0546 | **−0.0229** |
| median DV_gap | +0.0337 | −0.0332 |
| wins (trained>shuffled) | 4/6 | **1/3** |
| DV_trained>0 (학습이 init 이김) | 2/6 | **0/3** |
| 바 0.15 | 미달 | 미달 |

d=512 per-seed: seed7 gap +0.043 W · seed11 −0.079 · seed4303 −0.033. 계기 유효성은 d-불변(추정기는 3-셀
TPM 위에서 돌지 트렁크 d 에 무관 — XOR 2.25·COPY 0 로 확인, H_9959/H_9960 동일 계기).

## 판정 · 함의
- **음성 scale-robust.** 8× 넓히고 4× 깊게 해도 토이의 약한 양성이 **사라지고 반전**했다. 스케일이 레버였다면
  gap 이 커졌어야 하나 정반대. ⟹ 학습된 3-셀 순환은 스케일이 커져도 통합(개입형 Φ)을 안정적으로 못 키운다.
- **오너 질문 종합 답**("303M 학습시 Φ 늘리는 방법"): 유일 메커니즘(함께 학습된 순환 lane)이 값싼~중간 스케일서
  Φ를 못 올리고 **스케일↑ 이 추세를 악화**시키므로, 303M 외삽도 부정적. Phase B(303M) 대형 지출은 이 스케일
  기울기가 **더욱 강하게 게이트**한다(frozen-first + scale-trend 둘 다).
- 🔑 왜인가(구조): lane 은 트렁크 d 와 무관하게 **항상 3 셀**이고 Φ는 그 3×3 순환 결합에서 나온다. 트렁크가
  커져도 CE 가 그 3 셀을 통합(비-모듈)해로 미는 압력은 안 커지고, 오히려 큰 트렁크가 스스로 예측을 더 잘 해
  lane 잔차를 덜 쓰는(gamma↓) 쪽으로 갈 수 있다 — H_9957 FIELD-LOOP 의 "무용하면 gamma→0" 과 같은 결.

## 정직 경계
- d=512 는 여전히 303M(d~3784) 아님 · 3-seed. 단 **방향**(토이 약양성 → 8× 스케일서 null/음성)이 "스케일=레버"의
  정반대라 scale-robust 근거로 충분(`a_scale_honest_scope`: 실제 스케일 스텝 밟았고 효과가 안 자람).
- 학습 engine-native · Φ판독 DIRECTIONAL(.pt, `evaluate --iit4-recurrent-lane` 미배선) · cement 아님.
- 재현 계기: 브랜치 `h9954_recurrent_lane_impl` · summer venv `~/h9954_venv` · 드라이버 `/tmp/rl_collapse_prefix.py`.
- 관련: [[H_9961]](토이 스크린 · 이 카드가 스케일 축으로 확장) · [[H_9954]](순환 lane 설계) · [[H_9959]]/[[H_9960]](계기·파이프라인 인증) ·
  [[H_9957]](FIELD-LOOP · 무용하면 gamma→0 같은 결) · [[H_9272]](grid-only 에 stack 금지 — 여기선 스케일 스텝으로 회피)
