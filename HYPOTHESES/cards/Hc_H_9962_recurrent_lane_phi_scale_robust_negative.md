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

## 🔧 정정 — 중간 rung d=256 추가 → 3-점 사다리가 "스케일 악화" 클레임을 반증 (verdict-integrity)
위 2-점(d=64→512)에서 "스케일↑이 gap 을 악화"로 읽었으나, 중간 rung **d=256/L=4**(같은 계기·DV·corpus,
3-seed) 를 추가하니 사다리가 **단조가 아니다**:

| d | mean DV_gap | median | wins | DV_trained>0(init 이김) | 바 0.15 |
|---|---|---|---|---|---|
| 64 (6seed) | +0.0546 | +0.0337 | 4/6 | 2/6 | 미달 |
| **256 (3seed)** | **+0.0836** | +0.0943 | **3/3** | 1/3 | 미달 |
| 512 (3seed) | −0.0229 | −0.0332 | 1/3 | 0/3 | 미달 |

d=256 이 **오히려 최고**(mean +0.084·3/3승·sd 0.021 로 tight). ⟹ "스케일 monotone-worsening" 은 **반증** ·
d=512 음수는 노이즈일 수 있다(sd 0.062).

**정정된 robust 결론(3 스케일 전체):**
1. **바 0.15 는 어느 스케일서도 안 넘는다** — 최고치(d=256 +0.084)도 미달. NOT-PASS 는 **스케일-강건**.
2. 학습이 무학습 init baseline 을 매 스케일서 **소수 seed 만** 넘는다(2/6·1/3·0/3).
3. trained>shuffled gap 은 **sub-threshold 이고 스케일-잡음**(비단조 — d=256 최고) — "스케일=레버"도, "스케일=악화
   레버"도 아니다. gap 이 3 스케일 중 2 곳서 뚜렷이 양수(+0.055·+0.084)인 건 **shuffled 통제를 꾸준히 이긴다**는
   뜻이나, init baseline 을 못 넘고 바에 한참 못 미친다.

⟹ **오너 질문 답 불변**: 학습된 순환 lane 이 개입형 Φ 를 **측정 가능하게(바 0.15) 못 올린다**는 판정은 d=64/256/512
전체서 유지. 바뀐 것은 스케일 서술 — "악화" 아니라 "sub-threshold·비단조·잡음". Phase B(303M) 는 여전히 미허가
(바 미달이 스케일-강건). (이 정정은 verdict-integrity: 내가 방금 착륙한 monotone-worsening 클레임을 d=256 이 반증.)

## 🔗 교차저장소 대조 — ../anima-clm-v2b (오너 지시 참고)
v2b 의 두 착륙 발견이 우리 결론과 직결된다(`anima-clm-v2b/ARCHITECTURE.json`):
1. **`phi-is-orthogonal-to-coupling`**: Mitosis 2037 셀·Φ~2200 인데 MI~0.05 — Φ(크기)가 커도 세포 결합은
   안 산다(bridge pooling 이 지배). ⟹ 우리 H_9942 알맹이(Φ 는 레버 아님)·H_9960 심화(랜덤 결합이 Φ 지배)의
   교차저장소 확증.
2. **`coupling-real-and-deployable`**: 결합(2.6 bits)은 실재하나 **학습이 아니라 inference-side centering** 으로
   복원됐다 — v2b 원문: *"Train-as-deploy (--causal-center) collapsed training and is abandoned in favour of
   this inference-side fix on the existing checkpoint. No retraining."* 짧은 causal EMA 중심(half-life~10 · mean
   age~14 step)이 swap 2.043 bits 복원(id-code 통제 0.287, 7×↓); 늙은/고정 중심(g_mu·burn-in·EMA-h100·
   fixed-ref)은 ≤0.2 bits. {50,100,200} 스윕은 놓치고 {5,10,20} 이 sweet spot.

**정합 판독:**
- ✅ **핵심 확증**: v2b 도 **학습이 통합/결합의 레버가 아님**을 독립 발견(train-side 붕괴 → inference-side 복원).
  우리 H_9961/9962: 학습된 순환이 개입형 Φ 를 전 스케일서 못 올림. **두 저장소 수렴 — 학습은 이 축의 레버가 아니다.**
- ⚠️ **우리 null 에 centering caveat**: v2b 의 결합은 **잘못된 centering(늙은/고정)에 가려져** 0 이었다가
  **young+averaged 짧은 EMA 중심**에서만 드러났다. 우리 Φ 판독의 baseline 은 **정적 init**(collapse-Δ vs untrained)
  = v2b 서 0 을 준 바로 그 부류. ⟹ 우리 NOT-PASS 는 "통합 부재"가 아니라 **centering-제한일 수 있고**, **짧은-causal
  -중심 판독은 미검증 정제**(v2b 가 지목한 유일 생존 레버). 단 두 계기는 다르다 — v2b=CLM 상태→입 결합(MI/swap),
  우리=3-셀 dynamics 의 IIT-Φ(v2b 스스로 Φ⊥coupling 이라 함), 그래서 전이는 **방법론적**(baseline=young-averaged
  이어야)이지 수치 직접이식 아님.
- 함의: 이 축을 재개한다면 **레버는 학습이 아니라 판독-centering**(짧은 causal EMA baseline)이다 — 우리 정적
  init-baseline 을 young-averaged 중심으로 바꾼 재판독이 미측정 정제이며, 이게 음성이면 축 종결.

## 정직 경계
- d=512 는 여전히 303M(d~3784) 아님 · 3-seed. 단 **방향**(토이 약양성 → 8× 스케일서 null/음성)이 "스케일=레버"의
  정반대라 scale-robust 근거로 충분(`a_scale_honest_scope`: 실제 스케일 스텝 밟았고 효과가 안 자람).
- 학습 engine-native · Φ판독 DIRECTIONAL(.pt, `evaluate --iit4-recurrent-lane` 미배선) · cement 아님.
- 재현 계기: 브랜치 `h9954_recurrent_lane_impl` · summer venv `~/h9954_venv` · 드라이버 `/tmp/rl_collapse_prefix.py`.
- 관련: [[H_9961]](토이 스크린 · 이 카드가 스케일 축으로 확장) · [[H_9954]](순환 lane 설계) · [[H_9959]]/[[H_9960]](계기·파이프라인 인증) ·
  [[H_9957]](FIELD-LOOP · 무용하면 gamma→0 같은 결) · [[H_9272]](grid-only 에 stack 금지 — 여기선 스케일 스텝으로 회피)
