# H_9942 · "Φ를 키우면 G1이 풀린다" — 레버로서 KILL. 단 **죽는 지점은 유비가 아니라 기질(feedforward)**이고, 남는 알맹이는 **순환(recurrence)**이다

**한 줄:** 오너 가설(의식이 진짜 자라야 제대로 된 성장이고, 그러면 G1/G6가 풀릴 수도)을 lab full(fable+sol)
발산 + **우리 손 실측**으로 판정했다. 유비 자체는 **말장난이 아니다**(n=3 faithful IIT-4 에서 Φ 는 선형분리
불가 결합을 분리가능 게이트보다 **3.86× 높게** 채점, 받침대 정확히 0). 그런데 레버는 죽는다 — **feedforward
계는 Φ=0** 이고 303M 트렁크가 feedforward 이므로, 그 기질 위에서 Φ 는 구조적으로 키울 수 없다.

- 계기(신규·$0·계기인증): 저장소 자신의 `core/engine_cli.py::big_phi_bounded` 에 **손으로 만든 TPM 직접 투입**
  (forward pass 없음·engine op 아님). 합성이지만 **faculty 주장이 아니라 계기 인증**이므로 p9 합법.
  regime `synthetic-instrument-cert` · DIRECTIONAL.

## 우리 실측 — Φ 는 비분리 결합을 실제로 더 높게 매긴다 (n=3, 전 8상태, cap=3)
| system | mean Φ | max Φ |
|---|---|---|
| **XOR (선형분리 불가 · G1 이 못하는 그 class)** | **2.2500** | 3.0000 |
| OR (분리 가능) | 0.5825 | 1.0000 |
| AND (분리 가능) | 0.5825 | 1.0000 |
| **COPY (받침대 · 통합 없음)** | **0.0000** | 0.0000 |

XOR / 최고-분리가능 = **3.86×** · 받침대가 **정확히 0** 이므로 추정기가 통합을 읽고 있다(부풀리지 않는다).

⟹ **Q1(유비가 실재냐 말장난이냐) = 실재 쪽.** sol 이 "결정적 내부 반례"로 든 `XOR2 Φ=0`
(`HEXAD/IIT4/state/iit4_m7_calib_breadth_2026_05_25/run_m7.hexa:17`)은 **n=2 에서 두 유닛이 같은 값을 받는
퇴화 구성**(다음상태가 00/11 뿐이라 정보가 2-to-1 로 뭉개짐 · 주석도 "output state-blind")이지 XOR 일반이
아니다. **sol 의 Q1 반례는 과대주장이며 이 카드가 정정한다**(verdict-integrity).

## 그럼에도 레버는 KILL — 기질에서 죽는다
1. **feedforward ⟹ Φ=0** (IIT unfolding 정리). 저장소 자신의 `lab/v6/phi_unfold_pedestal.py`(V6_4)가 실측:
   *"PEDESTAL HOLDS — core > 0 while both feedforward systems read exactly 0"*. **303M 트렁크는 feedforward**
   ⟹ D×R 결합을 완벽히 구워 넣어도 그 트렁크의 Φ 는 0. 유비가 맞아도 **키울 대상이 없다**.
2. **일반적 비가법성↑ 이 재조합을 안 사준다** — H_9088: penult additivity 0.951→0.042 로 크게 낮췄는데
   **G1 은 정확히 floor 유지**.
3. **관측 macro-Φ 는 무의미** — H_6196: 높은 관측 macro-Φ 인데 303M 은 여전히 벽. (sol: 쓰려면 관측이 아니라
   **개입(interventional)** 이어야 함.)
4. **교차저장소** — `anima-clm-v2b` `phi-is-orthogonal-to-coupling`: Φ~2200(2037셀)인데 MI~0.05.
5. **Φ 를 손실에 넣기 = tune-to-green** (`a_train_inline_gauge` 위반 · FORM tunable). 두 모델 모두 kill.

## 판정 — 🔴 레버 KILL · 🟢 알맹이는 **순환(recurrence)** 으로 남는다
- **죽는 것**: "Φ 를 키우면 G1/G6 가 풀린다". 범주 오류가 아니라 **기질 오류** — 대상이 feedforward 라 Φ 가
  0 으로 고정된다. (fable/sol 은 "범주 오류"로 읽었으나, 우리 실측은 유비 자체는 살아있고 **기질이 막는다**로
  더 정확히 국소화한다.)
- **남는 것(오너 직관의 진짜 payload)**: Φ>0 은 **순환을 요구**하고, G1 을 유일하게 깬 선례
  **H_1003(커리큘럼-학습 GRU=순환망)** 도 순환이다(H_1000 직접학습 실패 · H_9259 무학습 순환도 실패 ⟹
  "학습된 순환"이 조건). 즉 **의식(Φ)과 재조합(G1)이 만나는 지점은 Φ 라는 숫자가 아니라 `학습된 순환`이라는
  구조 요건**이다. 이건 이미 살아있는 레버 **γ trained-constructive-bind** 와 같은 곳을 가리킨다.
- **Φ 의 정당한 역할**: 레버 아님 · 손실 아님 · **frozen held-out 개입형 macro-Φ 를 γ 캠페인에 곁다리로 태우는
  DIRECTIONAL 진단기** 후보 (한계비용 ≈ 0). 그 진단기가 실재하는지는 **미측정**.

## 정직 경계
- 이 카드는 **새 실험이 아니라** 기존 실측 4건 + 교차저장소 1건 + 신규 $0 계기인증 1건에 근거한 **설계 판정**이다.
- 우리 실측은 **n=3 · 결정론 TPM · 합성**(계기 인증 전용). "anima 가 무엇을 할 수 있다"의 증거로 인용 금지(p9).
- Φ 를 위한 **pool GPU 지출은 어떤 결과에서도 정당화되지 않는다**(두 모델 합의).

## 다음 (미측정)
① **$0 토이 4-arm**으로 "결합을 구우면 Φ 서명이 남는가"만 따로 판정 — curriculum-학습 / 직접학습 /
   라벨-셔플(결합파괴 통제) / 무학습(받침대), DV = **개입형** macro-Φ collapse-Δ, **계기인증 선행**(알려진
   기약 3유닛 TPM Φ>0 ∧ 분리쌍 ~0 통과 못하면 ABORT). 이게 음성이면 진단기 각도까지 종결.
② 생존 레버는 그대로: **γ trained-constructive-bind on natural text + Φ-blind easy→hard 커리큘럼**.
