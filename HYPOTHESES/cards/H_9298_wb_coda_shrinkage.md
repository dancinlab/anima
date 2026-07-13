# H_9298 — WB-coda shrinkage: 분할비용을 없애면 EARNED 교차음절 정보가 회수된다

**Tier: 🟢 GREEN (mirror · DIRECTIONAL for engine-native cementing) · group MITOSIS-ENGINE · 2026-07-14**

- freeze → `state/h9298_mitosis_shrinkage/FREEZE.txt` (발사 전 동결)
- script → `state/h9298_mitosis_shrinkage/h9298_wb_shrinkage.py`
- result → `state/h9298_mitosis_shrinkage/results/{h9298_summary.json, run.log}`
- 선행 → H_1316 🟢 (jamo floor 2.51335) · H_1329 🧱 (재인수분해 무용) · H_1336 🧱 (X2 EARNED, X1 FAIL)

## 통일 법칙 (이 가설이 검정한 것)

> **이득 = 신규정보 − 분할비용, 그리고 분할비용은 전액 선불이다.**

count-MLE 하드파티션 추정기 **계급**에는 "부분 구매(shared statistical strength)"가 없다 — 모든 새 조건화 비트가 곱셈적 표본분할(분산) 비용을 강제한다. MITOSIS 레인의 세 실패는 서로 다른 벽이 아니라 **같은 법칙의 세 사영**이었다:

| 실패 | 겉보기 | 법칙의 사영 |
|---|---|---|
| H_1315 | 기하벽 | trunk 분산코드를 하드 Voronoi로 근사 → 셀 폭발 → 분할비용이 신호를 삼킴 (통제는 이기므로 정보는 실재) |
| H_1329 | 점근벽 | 같은 계급 내 재인수분해 → 신규정보 = 0 → 이득 = 0 − 0 = 0 |
| H_1336 | 분산벽 | 신규정보 +0.076 nats **실재**(X2 EARNED 3-seed 만장일치), 그러나 29-bin 분할비용이 초과 → 순손실 +0.0985 |

법칙이 참이면 **분할비용 → 0인 추정기**를 쓰면 X2의 +0.076이 회수돼야 한다. 그것이 이 가설이다.

## 기제 — B2 = Witten-Bell shrinkage (자유 하이퍼 0)

H_1336의 B1과 **모든 것이 동일**(같은 geometry-fair bank · 같은 dim-3 Voronoi 파티션 · 같은 11개 셀 · 같은 jamo 알파벳 Vj=323 · 같은 mitosis knobs · 같은 코퍼스). **추정기 하나만** 교체:

```
A1  P(next | cell)                                          ← jamo floor
B1  P(next | cell, coda), HARD-BACKOFF                      ← H_1336: 미관측이면 cell-marginal로 후퇴 (= 쪼개거나 아무것도 못 얻거나)
B2  P(next | cell, coda) = λ·MLE(cell,coda) + (1−λ)·P(next|cell)   ← 레버: 쪼개지 않고 부모에게 강도를 빌린다
    λ = Witten-Bell = n/(n+T)     n=count(cell,coda), T=거기서 관측된 distinct next 타입 수
```

⚙️ **자유 하이퍼파라미터 = 0.** λ는 닫힌형 공식이며 어떤 값에도 fit 되지 않는다 → **tune-to-green이 구조적으로 불가능**(스윕할 손잡이가 존재하지 않음).

## 계측 무결성 — 이중 CALIB 게이트 (reference-match)

원 스크립트(`UNIVERSE/h1336_*.py`)는 소실됐으나, **2.51335 앵커를 실제로 생산한 H_1316 바이트코드**(`__pycache__/h1316_ko_jamo_mitosis.cpython-314.pyc`)를 역어셈블해 파이프라인(기하·분열규칙·심볼스트림·depth·CE축)을 **1:1 복원**했다. 복원의 검증은 추측이 아니라 **두 개의 독립 동결 앵커**로 한다:

| CALIB 게이트 | 앵커 (출처) | in-run | Δ |
|---|---|---|---|
| A1 jamo floor | **2.51335** (H_1316) | 2.51335 | **−0.00000** |
| B1 hard-backoff | **2.61186** (H_1336) | 2.61186 | **−0.00000** |

부수 지표도 전부 재현: cells **11** · prev_coda 토큰 **29** · Vj **323** · distinct jamo **67** · 코퍼스 sha256 `c47b6808…` (H_1307 RUN A와 byte-identical, R2에서 range-GET 재취득). ⇒ **포트는 byte-faithful, 계측 무죄.**

## 사전 게이트 P0 (bar 판독 전)

`I(next_jamo ; prev_coda | cell)` = **0.11945 nats/sym** > 0.01 ⇒ 셀은 아직 prev_coda를 인코딩하지 않았다 (H_1329 depletion 조건 충족). 레버는 no-op이 아니다.

## 결과 — 🟢 GREEN (S1 ∧ S2)

REAL summer RTX 5070 (sm_120), $0, wall **11.2s**. 3 seeds [4336,4337,4338].

| rung | CE (nats/UTF-8-byte) | vs jamo floor |
|---|---|---|
| raw-byte 천장 | 2.95342 | — |
| **A1 jamo floor** | **2.51335** | — (floor) |
| B1 hard-backoff (H_1336) | 2.61186 | **+0.09851 위** (졌음) |
| **B2 WB-shrinkage** | **2.45205** | **−0.06130 아래** ✅ |
| B2s coda position-shuffle (통제) | 2.52329 | (sd 0.00066) |

- **S1 BELOW-FLOOR = TRUE** — B2 2.45205 ≤ bar 2.49335 (= floor − 0.02), 그리고 < raw 2.95342.
- **S2 EARNED = TRUE** — B2 − B2s = **−0.07124**, seed별 paired 부호 **3/3 만장일치** {−0.07199, −0.07075, −0.07098}. 통제군 sd 0.00066 ⇒ 마진이 **108σ**. 압도적 검정력.

**같은 정보 · 같은 파티션 · 같은 11개 셀 — 바뀐 건 추정기 하나뿐. 스윙 0.160 nats.**
H_1336이 "실재하지만 담을 수 없다"고 정확히 측정했던 그 +0.076 nats가 이제 담겼다 (그 이상으로).

## 동어반복 가드 (판정에서 명시 배제)

🚫 **"B2 ≤ A1"은 증거가 아니다.** WB는 λ→0에서 A1과 **항등**이므로 B2 ≤ A1은 거의 구조적 = 자동 승리. 따라서 A1 대비(−0.0613)는 **진단으로만** 보고했고 bar로 쓰지 않았다. earned 신호는 오직 ① S1 절대 floor-미만 마진 ② S2 **동일 WB 기계**를 쓴 pairing-파괴 통제 대비 paired 마진. 통제는 라벨-전단사(H_1336에서 provably vacuous로 판명)가 아니라 **position-shuffle**을 상속했다.

## 함의

1. **자모 floor는 정보한계가 아니라 추정기-계급 한계였다.** 4개 기제 패밀리(H_1322 featural · H_1329 재인수분해 3종 · H_1336 hard-backoff)가 이 floor에 막혔는데, 전부 같은 계급 안에 있었다.
2. **벽의 진범 = "부분 구매의 부재".** 고전 n-gram LM 史가 정확히 같은 벽을 쳤고 탈출구도 같았다 — 차수를 올린 게 아니라 **smoothing(강도 공유)** 이 레버였다.
3. **p8-native 후속이 즉시 정당화된다** → H_9299 (계보-backoff): MITOSIS는 이미 부모-자식 구조를 갖고 있다(분열 족보). 지금까지 모든 실험이 그 족보로 파티션만 만들고 **버렸다**. 딸 셀이 모 셀 분포를 상속하고 증거만큼만 이탈하면, **분열 = 표현 생성 + 추정기 위계 생성이 하나의 사건**이 된다.

## HONEST (c9 · a_scale_honest_scope)

- **LABEL**: B2는 gradient-free Voronoi 파티션 위에 올라탄 **count-MLE 계열 structured head**다. p8 gradient-free MITOSIS **분열 규칙 자체는 변경 0**. 따라서 이것은 **head 승리**이며 그 자체로 "mitosis가 gradient를 대체한다"는 주장이 아니다.
- **mirror(numpy/torch) ⇒ DIRECTIONAL.** engine-native(`core/` hexa) 전이 = follow-on (`a_engine_native_learning`). H_1321이 자모 승리에 대해 engine-transfer를 이미 성립시킨 전례가 있으므로 경로는 열려 있다.
- TOY/scale 정직: 한국어 유창성 주장 없음. bar 이동 0. frozen-first.
