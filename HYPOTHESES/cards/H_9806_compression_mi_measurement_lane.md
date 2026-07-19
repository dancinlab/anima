---
id: H_9806
title: COMPRESSION-MI 계측 레인 — 스트림 자체의 경계횡단 상호정보를 모델 forward 없이 $0 로 재는 계기 (조건부-bpb 3-추정기 배터리 + shift-null LOO capture)
tier: PROPOSED · 계기 IMPLEMENTED + TOY e2e 통과 · 자체 인증 PASS (아직 어떤 substrate verdict 도 없음)
frontier: instrument-absorption (lab/v3 → production)
lane: stream-property measurement (NOT a model-reach measurement)
created: 2026-07-20
series: R-absorb
origin: "lab/v3 H_005 (SUPPORTED/ANCHORED) + H_009 (verdict REFUSED · 계기 CERTIFIED)"
related: "[[H_9520]] · [[H_9329]] · [[H_9774]] · [[H_9800]]"
wired: no (계기만 착륙 · production substrate 미측정)
---

# H_9806 — 압축-MI 계측 레인

## ⚠️ 이 카드의 상태 (정직 선언)

**이 세션은 계기(instrument)만 착륙시켰다.** 아래 수치는 전부 **토이 e2e 배관 검증 + 계기
자체인증**이며, **어떤 것도 substrate verdict 가 아니다.** production 코퍼스/ckpt 로는 한 번도
돌리지 않았다. 출처인 `lab/v3` 는 rule-exempt 샌드박스이므로 **랩의 숫자는 영구히 production
verdict 가 될 수 없다** — 여기 착륙한 `anima-py` 코드가 낸 숫자만 cement 대상이다.

## 왜 존재하는가 (한 줄)

production anima 에는 **압축기반 MI 추정기가 0개**였다. 그래서 "이 스트림이 경계를 넘어 정보를
나르는가"는 언제나 모델 forward 로만 물을 수 있었고, 그 답은 **스트림의 성질과 모델의 reach 를
섞어버린다**(`instrument-claim-alignment-before-reading-a-bar` · H_9329 가 정확히 이 혼동).
이 레인은 **스트림 자체의 성질**을 ckpt·GPU·numpy 없이 $0 로 잰다.

## 계기 ① — 경계횡단 조건부-bpb 배터리 (`--stream-mi`)

순서 있는 세그먼트 s_0..s_{n-1} 에 대해

```
ceiling(t) = bpb(P_{t+1} | tail_t) − bpb(P_{t+1} | tail_t + body_t)
```

`tail_t` = 세그먼트 t 의 마지막 W 바이트(= in-context reach 대리), `P_{t+1}` = 다음 세그먼트의
앞 P 바이트, `body_t` = tail 이전 전부(= **어떤 병목 요약의 상한** — 전체 body 도 bpb 를 못
올리면 어떤 k-byte 발췌도 못 올린다 · kill 쪽으로 보수적).

**추정기 3개**(하나짜리 압축기의 맹점은 substrate 사실로 읽힌다):
`gzip`(LZ · 32KB 창 밖 단일 장거리 토큰에 맹목) · `ppm`(1..k 다중차수 적응 · 문맥 reach 무한) ·
`markov6`(희소 order-6 · 고차 PPM 이 불가능한 영역까지 order-aware).

**★ floor 는 DERIVED, 절대 가정 아님.** raw ceiling 은 값이지 신호가 아니다
(`measurement-metalaw-form-tunable-bind-earned`: 신호 = collapse-Δ). floor 는 **동일한 realized
세그먼트**에서 인접성만 결정론적으로 파괴해 재계산한다 — 길이·바이트통계·쌍 개수 전부 동일, **순서만**
파괴. 보고 수치는 `over_floor = ceiling − shuffle_floor`, 추정기별·스트림별.

## 계기 ② — 특징공간 shift-null LOO capture (`--capture-anchor`)

배터리는 **추상 코드에 구조적으로 맹목**이다(gzip/ppm/markov 는 디코더 없는 리터럴 바이트 모델 —
k-float 코드를 렌더링해 붙이면 진실과 무관하게 capture≈0). 그래서 "경계횡단 정보 중 rank-k 연속
요약이 얼마나 살아남나"는 특징공간에서만 물을 수 있다.

```
align_X    = median_δ err_X(δ) − err_X(0)        # δ = 질의의 순환 어긋냄
capture(k) = align_s(k) / align_full
```

shift-null 이 핵심: **K-NN 추정기의 분산 페널티가 정렬/어긋남 양쪽에서 동일**하므로 차분에서
**상쇄**된다. (랩의 1차 시도는 상수-평균 분모를 써서 살아있는 스트림에 음수 capture 를 냈다 —
추정기 분산을 substrate 로 읽은 것. shift-null 은 그 실패양식을 구성으로 해소한다.)

구성으로 배제한 두 결함:
- **VALID-k ONLY** — k ≥ n_train−1 이면 top-k 축이 학습 부분공간 전체를 span 하고, 테스트 질의의
  직교 잔차가 per-query 상수가 되어 k-NN argmin 에서 상쇄 ⟹ **capture ≡ 1.0 이 기계적으로** 나온다.
  `k > (n_train−1)//2` 또는 `2k > numeric rank` 인 k 는 거부한다. 이건 보수성이 아니라 **측정과
  동어반복의 차이**다.
- **LEAKAGE** — 후보에서 `|i−j| < 2` 제외(세그먼트를 공유하는 이웃이 예측자가 될 수 없음).

**topic floor**: 어느 topic 인지만 식별해도 점수가 나오므로, topic-최근접 **다른** 세그먼트
(t−1,t,t+1 제외)의 요약으로 질의하는 arm 을 둔다. 진짜 시험은 총계 margin 이 아니라 **쌍별 부호
카운트**이고, **그 임계값은 realized 쌍 개수에서 정확 이항 꼬리로 유도**한다(랩의 28/43 을 복사하지
않는다 · `chance-level-must-be-derived-per-metric`).

## 인증은 계기와 분리되지 않는다 (하드 규칙)

**null 통제만으로는 계기가 무언가를 볼 수 있음을 절대 증명 못 한다** — 헛것을 안 본다는 것뿐이다
(`positive-control-before-reading-a-negative`). 두 진입점 모두 substrate 숫자를 보고하기 **전에**
양성 plant 와 음성 통제를 돌리고, plant 가 안 터지면 verdict 자체를 거부한다. plant 를 별도
스크립트로 두면 `rm` 하나 거리의 같은 결함이므로 **플래그 안에 실어 보낸다**.

| 계기 | 양성 plant | 음성 통제 |
|---|---|---|
| `--stream-mi` | `plant_crossboundary` — 세그먼트 t 의 고엔트로피 블록이 **tail 밖 body** 에 놓이고 t+1 의 prefix 가 바로 그 블록. body 에서만 읽히는 정보 = ceiling 이 잰다고 주장하는 바로 그 양. | `plant_null_stream` — **동일 구성에서 carry-over 만 제거**. 길이·알파벳·주변분포 동일, 경계횡단 정보만 0. floor 를 넘으면 안 됨. |
| `--capture-anchor` | **HIGH** `plant_weak` — top-k 축이 실제로 span 하는 약한 진짜 ceiling → capture ≥ 0.8 | **FAIL** `plant_iid` — 순수 잡음 → ceiling gate 가 **반드시 실패**해야 함 · **LOW** `plant_buried` — 아래 |

**LOW = buried delay-line** (계기가 capture 를 부풀릴 수 없음을 증명하는 arm): 단일 로지스틱
스칼라 x_{i+1}=4x(1−x) 의 **20개 지연 탭**(탭 공분산이 정확히 1·I — 평탄 스펙트럼, PCA 가 집을
돌출 방향 없음) 을 분산 4.0 의 iid decoy 8개 **아래에 묻는다**. full k-NN 은 신호블록의 거리지분
20/(20+8·4)=38.5% 를 보므로 **gate PASS**, 그러나 top-8 표본축은 decoy 지배라 rank-k 코드는
놓친다 ⟹ **capture(k≤8) 이 구성상 낮아야 한다**.
**해상도 한계(측정·은폐 않고 보고)**: LOW arm 은 n ≳ 100 에서만 gating. 그 아래에선 작은 학습셋의
decoy 표본고유값 산포가 신호 조합을 top-8 로 새게 하므로 **INFORMATIONAL** 이고 등급은
PRIMARY 가 아니라 **REPLICATION** 으로 표기된다. (power 에 대한 진술이지 substrate 에 대한 진술이 아니다.)

## 새 플래그 (정확한 문법 · 설치된 CLI 표면)

```
anima-py evaluate --stream-mi [<path>] [--shuffle-floor derived|off]
                              [--win 4096] [--span 2048] [--n-segments 30] [--out f.json]
anima-py evaluate --capture-anchor [<path>] [--k 8] [--win 4096] [--span 2048]
                                   [--n-segments N] [--out f.json]
```

- `<path>` **생략 가능** ⟹ plant 만 도는 **순수 인증 패스**(substrate 에 대해 아무것도 주장 않음).
- `<path>` 가 디렉토리면 파일당 1 세그먼트(파일명 정렬), 파일이면 빈줄 구분자로 분할.
  `win+span` 미만 세그먼트는 **버린다**(패딩하면 답을 제조하게 된다).
- `--shuffle-floor off` = 통제 arm 생략 fast raw 패스 ⟹ **verdict 를 거부**하고 `RAW-NO-CONTROL`
  을 낸다. 원리를 문법에 박은 것.
- ckpt 를 받지 않는다(스트림의 성질을 재므로) · $0 · stdlib only · GPU/numpy/torch 0.

## 반증조건 (계기 수준)

- plant 가 안 터지거나 null 이 floor 를 넘으면 → `INSTRUMENT-DEAD`, rc=2, substrate 숫자 판독 금지.
- `--capture-anchor` 에서 FAIL arm 의 gate 가 통과하면 → 그 gate 는 추정기 분산을 읽는 것 ⟹
  그 계기로 낸 모든 capture 는 void.
- `rank_full > RANK_GATE` → `NO-FEATURE-CEILING`: **계기의 power 를 반증**하는 것이지 substrate 를
  반증하는 것이 아니다(둘을 섞으면 H_9520 의 오독을 반복).
- capture 가 k 에 대해 비단조(> 0.05 하락) → `PENDING(instrument)`, 크기 판독 금지.

## 토이 e2e (실측 · exit 0 · 전부 $0 CPU 로컬)

`anima-py evaluate --capture-anchor --n-segments 102` — **3-arm 인증 전부 통과**:

```
HIGH (plant_weak)     gate=True capture(8)=1.1792 → PASS
LOW  (buried delay)   full_rank=0 capture(k<=8)={'2': -0.2520, '4': 0.1228, '8': 0.1517} → PASS
FAIL (iid noise)      gate=False → PASS
certified=True · grade=PRIMARY
```

`--stream-mi` plant vs null (n=12 · W=512 · P=256) — **plant 발화 · null 거부**:

```
gzip     plant over_floor +7.1250 | null over_floor -0.0312
ppm      plant over_floor +0.8660 | null over_floor -0.0016
markov6  plant over_floor +0.4791 | null over_floor -0.0126
plant_fires=True · null_refuses=True → certified=True
```

디스크의 실제 스트림 왕복(carry-over 있는 24 세그먼트 파일) → `🟢 ANCHORED`
(gzip +7.1562 · ppm +0.8367 · markov6 +0.4672 over floor, 23 쌍).

**derived floor 가 왜 필요한지의 실증** — `core/*.py` 30 파일 스트림:
raw gzip ceiling **+1.1875** 는 커 보이지만 derived floor 가 **+0.8125**, over_floor 는 +0.3750 이고
order-aware 쌍(ppm +0.0234 · markov6 −0.0080)은 확인해주지 않는다 ⟹ `🔴 AT-FLOOR`.
raw 값 하나만 읽었으면 정반대 결론이 나왔을 자리다.

`--capture-anchor` 를 문서 청크 스트림(44 세그먼트)에 → `🔴 TOPIC-DECORATION`
(capture(8)=1.0449 로 anchor 는 넘지만 topic 1.1676 에 지고, 쌍별 부호 19/43 < **유도된 바 28**).
랩 H_009 가 본 것과 같은 양상이 production 코드에서 재현됐다 — 다만 이건 **토이 스트림**이지
production substrate 가 아니다.

## 정직한 한계

- **L1 계기만이다.** production 코퍼스·데몬 스트림·303M 어느 것도 이 세션에서 측정 안 함. wired: no.
- **L2 랩 숫자는 승격 불가.** `lab/v3` 의 H_005 ANCHORED / H_009 REFUSED 는 여기서 **재현되지 않았고
  재현될 수도 없다**(다른 스트림·다른 코드). 이 카드가 상속한 것은 **설계와 인증 구조**뿐이다.
- **L3 bag-of-n-gram 은 순서를 파괴**하고 해싱은 수만 trigram 을 256 버킷으로 뭉갠다. 둘 다 **거짓
  음성 쪽으로 보수적** — 여기 capture 는 순서를 아는 학습 코드의 하한이지 상한이 아니다.
- **L4 K-NN 은 학습된 encoder/decoder 보다 약하다.** 절대 capture 는 하한. 다만 align_s 와
  align_full 이 추정기를 공유하므로 **비율**은 대체로 predictor-불변이다.
- **L5 gzip 의 32KB LZ 창**은 단일 장거리 토큰에 맹목 — `ORDER-AWARE-ONLY` 판정은 strict 보다
  약한 판독이며 그렇게 표기된다.
- **L6 scope.** `AT-FLOOR` 는 **그 스트림·그 W** 에 대한 진술이다. 다른 W 는 ceiling 을 움직인다
  (긴 W 는 "일기"를 더 흡수해 측정된 lift 를 줄인다).
- **L7 세그먼트 정의가 결과를 움직인다.** 빈줄 분할과 파일당-1-세그먼트는 서로 다른 경계를 만들고,
  경계가 곧 측정 대상이다. 판독할 때 세그먼트 규칙을 함께 인용해야 한다.

## 2 표면

`HYPOTHESES/HYPOTHESES.jsonl` 한 줄 + 이 카드. 그 외 없음.
