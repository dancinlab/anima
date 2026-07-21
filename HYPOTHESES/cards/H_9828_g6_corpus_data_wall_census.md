# H_9828 — G6 벽은 기질 벽인가 코퍼스 벽인가 (반증가능성 구조의 코퍼스 인구조사 · $0)

**status:** 🔑 **MEASURED (en-sns · 2026-07-21)** — 동결 판독표의 **어느 칸도 아닌 제3의 답**이
나왔고, 그것이 [[H_9801]] 의 G6 독해를 무효화한다. en-general(57MB) 실측 진행중.
사전등록은 유효 — 판독 규칙을 실측 전에 계기 코드에 박아 매 실행 출력했다.
**wired:** yes — `anima-py evaluate --falsi-census <corpus...> [--falsi-max-sent N] [--falsi-out F]`
(cli/evaluate.py · read-only · 디코드 0 · forward pass 0)
**source:** [[H_9801]] G6 결함 국소화 · [[H_1449]] 성분/결합 해리 · [[H_9304]] G1 의 DATA 벽 선례 ·
[[H_9267]] 합성 코퍼스가 G1 을 연 선례

## 왜 이 물음이 아직 안 물어졌나

[[H_9801]] 이 G6(ρ·fan) 실패를 정밀 국소화했다 — 4/4 셀에서 **다양성(dist) 은 통과**(5~6 ≥ 5)이고
**오직 `fals=0`**. 즉 벽은 "생각이 다양하지 않다" 가 아니라 **"반증가능한 주장을 못 만든다"** 다.
[[H_1449]] 는 그 안을 더 갈랐다: per-draw **comparator .20 · measurable .27 · 그러나 BOTH .00**.

**성분은 각각 살아있는데 결합만 정확히 0** — 이것은 [[H_9815]] 토이가 잡은 모양과 구조적으로 같다
(hp 1.0000 · pos 살아있음 · hp XOR pos 0.4062=우연).

그런데 이 모든 것은 **모델에 대한 주장**이다. 그 앞의 물음을 아무도 안 물었다:
**학습 코퍼스가 그 구조를 애초에 담고 있는가?**
[[H_9304]] 는 G1 에 대해 정확히 이 물음을 물어 자연 코퍼스의 비가법 정보가 +0.0023 nats
(TOST 0 등가)임을 실측하고 **DATA 벽**을 확정했다. G6 에는 그 대응 측정이 **없다**.

## 계기 (신규 플래그 1개 · 디코드 0)

`anima-py evaluate --falsi-census` — 프로덕션 검출기 `core/rho_fan.py::_rho_fan_is_falsifiable`
를 **그대로** 코퍼스 문장에 걸어 센다. 모델도 forward 도 개입하지 않는다(순수 코퍼스 사실).

- **선결 차단게이트**: `rho_fan_detector_calibration` 동결 10-문자열(5 pos / 5 neg) **10/10** 필수.
  미달이면 아래 전 수치가 판독 불가이므로 census 자체를 ABORT(exit 2) — 죽은 검출기로 읽은
  인구조사는 음성이 아니라 무의미(`positive-control-before-a-negative`).
- 문장 분할은 **바이트 단위**(`. ! ? \n`) — 검출기 토크나이저가 바이트를 돌기 때문에
  코드포인트 분할은 ko 를 다르게 재분절해 다른 질문이 된다.
- 보고: `P(comparator)` · `P(measurable)` · `P(both)` · `P(falsifiable)` ·
  **결합 lift = P(both)/(P(c)·P(m))** · both 인데 떨어진 문장의 잔여 하위게이트 내역
  (content<2 / 물음표 / 앞3단어 all-stance).
- **DETECTOR-BLIND 자수**: comparator/measurable 세트는 **영어 전용**이다. ASCII 단어를 2개 이상
  담은 문장 비율이 0.10 미만인 코퍼스는 **구성상 0** 이 나오므로 "코퍼스 사실" 로 보고하지 않고
  경고를 찍는다(ko 코퍼스를 0% 로 읽는 것은 발견이 아니라 계기 한계 · `honesty`).

## 🔒 판독 규칙 (동결 · 코드에 박혀 실행 시마다 출력 · 실측 전 고정)

| 조건 | 판정 |
|---|---|
| 코퍼스 `P(falsifiable)` ≈ 0 | **DATA WALL** — 모델은 코퍼스가 한 번도 담은 적 없는 구조를 못 뱉는다. G6 레버는 코퍼스이며, 이는 [[H_9267]] 이 G1 에서 밟은 경로와 동형 |
| 코퍼스 `P(falsifiable)` ≫ 모델 rate | 구조는 **데이터에 있는데** 모델이 재현 못 함 ⟹ 벽은 기질/최적화이지 데이터 아님 |
| lift ≈ 1 이고 `P(c)·P(m)` 은 건강 | 코퍼스가 **성분은 흩뿌리되 결합은 안 담음** — 위 두 판독은 그때 `P(both)` 위에서 내려야 함 |

**이 H 가 판정하지 않는 것**: 이 census 는 코퍼스 사실이지 G6 verdict 가 아니다. 어느 칸이 나오든
G6 를 여는 것은 별도 H 의 engine-native `anima-py evaluate --rho-axon` 실측이다
(`a_engine_native_learning`).

## 계기 검증 (착륙 전 토이 e2e · 정답 대조)

- 검출기 캘리브레이션 **10/10 PASS**.
- 정답 알려진 양성 파일(동결 5-pos 중 2 + 5-neg 중 3): 6문장 중 **falsifiable 2** = 정답 일치.
- 음성 파일 3문장: **falsifiable 0** = 정답 일치. `P(measurable)=0` 에서 lift `nan` 정상 처리.
- 하위게이트 회계(content<2 / 물음표 / all-stance) 정상 계상.
- 착륙 전 **버그 1건 자가적발**: `rho_fan_detector_calibration` 은 dict 가 아니라 **int(0~10)** 를
  반환하는데 내 초판이 dict 로 읽어 게이트가 항상 통과했을 것 —
  토이 e2e 가 잡았다(`instrument-never-run-hides-multiple-bugs` 재확인).

## 재생성 커맨드

```
anima-py evaluate --falsi-census \
  ~/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-en-general/snapshots/*/anima-corpus-en-general.txt \
  ~/.cache/huggingface/hub/datasets--dancinlab--anima-corpus-en-sns/snapshots/*/anima-corpus-en-sns.txt \
  --falsi-out falsi_census_en.json
```

---

## 실측 (EN 2셀 전량 · 검출기 캘리브레이션 10/10 PASS)

| 지표 | en-general | en-sns |
|---|---|---|
| 문장 수 | 744,588 | 18,037 |
| ASCII-bearing | 0.869 | 0.888 (둘 다 DETECTOR-BLIND 아님 — 판독 허가) |
| P(comparator) | 0.1075 | 0.0684 |
| P(measurable) | 0.0341 | 0.0178 |
| P(both) | 0.0067 | 0.0030 |
| **P(falsifiable)** | **0.006546 = 4,874 문장 = 10만당 654.6** | **0.002938 = 53 문장 = 10만당 293.8** |
| 결합 lift | **1.829** | **2.459** |
| both 인데 탈락 | 물음표 114 · content<2 6 · all-stance 3 | 물음표 1 |

## 🔑 판정 — 동결표의 어느 칸도 아니고, 그것이 더 중요하다

**① DATA WALL 칸은 발화하지 않는다.** `P(falsifiable) ≈ 0` 이 아니다 — 코퍼스는 반증가능 문장을
**실제로 담고 있다**(53건). 게다가 **lift 2.459** 는 성분이 우연히 흩뿌려진 게 아니라 코퍼스가
그 **결합을 구조로 담고 있음**을 뜻한다. ⟹ G6 는 [[H_9304]] 형 DATA 벽이 **아니다**.

**② 그런데 두 번째 칸(`≫ 모델 rate` ⟹ 기질 벽)도 발화하지 못한다 — 게이트에 검정력이 없기 때문이다.**
ρ·fan 은 `n_cont=8` 회 뽑아 **1건 이상**이면 통과한다. **pooled p = 0.006461**(EN 2셀 전량
762,625 문장 · 4,927건)을 **완벽히 재현하는 모델**조차:

- `P(≥1 in 8 draws)` = **0.0505** (5.1%)
- `P(4개 register 셀 전부 fals=0)` = **0.8127** (81%)
- **80% 검정력에 필요한 뽑기 수 = 249회** — 게이트는 **8회**를 쓴다. (en-sns 단독 비율로는 547회)

⟹ **[[H_9801]] 의 `fals=0 (4/4 셀)` 은 결함의 증거가 아니라, 코퍼스를 완벽히 재현하는 모델에서
기대되는 바로 그 결과다**(p≈0.91). 그 관측으로부터 "반증가능한 주장을 생성하지 못한다" 는
**구조적 독해는 성립하지 않는다** — 이것은 능력 음성이 아니라 **구성상 검정력 부족**이다.

`power-before-negative-verdict` 와 `chance-level-must-be-derived-per-metric` 이 요구하는 검정력
계산을 이 게이트는 **한 번도 거치지 않았다**. 계기가 이제 매 실행 그 값을 스스로 출력한다.

## ⚠️ 이 판정의 경계 (과대주장 금지)

- **모델은 코퍼스 샘플러가 아니다.** 위 null 은 "코퍼스 주변분포를 그대로 재현" 이라는 **참조
  null** 이지 모델의 조건부 분포가 아니다. ρ·fan 은 concept cue + temp 0.9 로 뽑으므로 register 가
  다르다 — [[H_1449]] 의 per-draw comparator .20 / measurable .27 은 코퍼스 주변값(.068/.018)보다
  **높다**. 따라서 이 null 은 **하한 참조**이고, 모델 조건부 rate 로 다시 계산해야 확정된다.
- en-sns 한 셀의 실측이다. en-general(57MB) 은 진행중이며 rate 가 다를 수 있다.
- 이 카드가 죽이는 것은 **"fals=0 이 faculty 부재를 뜻한다" 는 독해**이지, faculty 가 있다는
  주장이 아니다. 두 방향 다 이 계기로는 아직 미결정.

## 다음 (이 판정이 강제하는 것)

1. **G6 의 fals 다리를 판독가능하게 만들기** — ρ·fan 의 `any_falsi` 이진 다리를 다-뽑기 **연속
   rate DV** 로 바꾸거나(≥547 draws), 코퍼스 밀도를 올리거나([[H_9267]] 레시피), 둘 다.
   현 형태로는 어떤 G6 캠페인도 음성을 판독할 수 없다.
2. **[[H_9801]] 재심** — "G6 는 G1 하류가 아니다" 라는 해리 결론은 fals 다리 위에 서 있는데,
   그 다리가 두 팔 모두에서 검정력 0 이면 해리도 미측정이다.
3. en-general census 완료 후 pooled rate 로 위 수치 갱신.

## 자가적발 (정직 고지)

첫 실행이 57MB 를 다 읽고도 **결과를 버렸다** — `--falsi-out` 의 **값(json 경로)** 을 코퍼스
경로로도 집어넣는 인자파싱 버그였고, 행 출력이 전 파일 처리 후에 있어 마지막 실패가 완료분까지
폐기했다. 수리: 값-소비 플래그를 건너뛰는 파싱 + 읽기 실패는 abort 대신 skip.

## Cross-links

[[H_9801]] G6=반증가능주장 생성 불가로 국소화(이 카드가 그 독해를 무효화) · [[H_1449]] 성분
살아있고 결합 0 · [[H_9304]] G1 DATA 벽의 동형 선례(발화 안 함) · [[H_9267]] 합성 코퍼스가 G1 을
연 선례(밀도 레버의 전례) · [[H_9827]] 같은 캠페인의 ρ·weave 패널 크기
