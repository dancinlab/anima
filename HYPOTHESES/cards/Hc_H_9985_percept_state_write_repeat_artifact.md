# H_9985 · 사전등록 — 40턴의 `REPEAT` 는 **동결된 디코드 씨앗**의 산물인가?

**상태: PROPOSED · 판정표 동결 · 측정 0 · 계기 배선 완료 · cement 는 engine-native `anima-py` 로만**
**계열: H_9984 의 다음 수 ② (거의 $0) · 선행 = H_9984 설계 · 40턴 study**

## 왜 이게 ① 결합 사다리보다 먼저인가

H_9984 의 1순위는 결합 사다리이고 그 DV 는 `COMPOSE` 다. 그런데 COMPOSE 는 "발화가 **상대의 말**과
**자기 상태** 둘 다의 함수인가"를 묻는데, **자기 상태가 상수면 어떤 함수든 구조적으로 퇴화**한다.
따라서 상태가 실제로 움직이는지 먼저 정하지 않으면, 사다리에서 나올 `COMPOSE=0` 이 **결합 사망**인지
**상태 동결 artifact** 인지 갈리지 않는다. 이 카드는 그 전제를 산다.

## 배경 — 가정이 아니라 **원본 재분석으로 실측**했다

원본 40턴 산출물(`~/anima-weights/study_long/study_long_transcript.jsonl` · 120 tick · 교사 40발화 ·
60 emit)을 다시 읽었다. 카드가 인용하던 수가 그대로 재현되고, **조작이 가해질 층으로 조건화하면 더 극단**이다:

| 층 | 최빈 byte-identical 발화 비중 |
|---|---|
| 전체 emit 풀 (H_9984 가 인용한 수) | **40/60 = 0.667** |
| **percept-SILENT tick (= 이 do() 가 닿는 유일한 층)** | **40/40 = 1.000** |
| percept-seeded tick | 0/20 = (반복 0) |

⟹ 침묵 tick 에서는 **예외 없이 같은 바이트열**이 나왔다. 이건 "가끔 반복한다"가 아니라 **상수 함수**다.

## 기전 — 왜 상수여야만 했는가 (코드로 확인)

`cli/chat.py` 의 실제 소비 씨앗은 `phase + " " + _gen_anchor_field(live_anchors[-1])` 이다.
percept 가 있는 tick 은 percept 가 `[-1]` 로 붙지만, **없는 tick 의 `[-1]` 은 `live_seed` = `session_seed`
= 세션 상수**다. argmax 입에 상수 씨앗을 주면 같은 바이트가 나오는 게 당연하다.
⟹ 침묵 tick 의 1.000 은 **기질 사실이기 전에 배선 사실일 수 있다.** 이 카드가 그 둘을 가른다.

## 조작 — `anima-py chat --percept-write` (engine-native · 새 플래그 · 기본 off = byte-identical)

교사 percept 만으로 세션-로컬 상태를 쓰고, **침묵 tick 의 `[-1]` 씨앗**으로 소비한다.
- **p5/자기루프**: 상태에 기질 자신의 발화는 **절대** 들어가지 않는다(쓰기 지점이 percept 분기 뿐).
  되돌아온 제 말을 외생 도달로 계상하는 세탁([[teacher-prompted-with-own-output-launders-self-loop]])도 구조적으로 불가.
- **발화 게이트 불변**: 상태는 `live_anchors`(디코드 씨앗)만 타고, 게이트는 그걸 읽지 않는다.
  H_9984 가 "게이트에 percept 항 넣기 = p5 오염"으로 못 박은 것을 그대로 지킨다.
- **percept 있는 tick 은 byte-untouched** ⟹ do() 가 정확히 동결 tick 에만 가해진다.

| arm | 상태 | 역할 |
|---|---|---|
| `off` | 없음 | 기준선 재현 (byte-identical) |
| `last` | 최신 percept | 처치 |
| `ring` | 최근 N=3 percept 결합 | 처치 (역사 민감) |
| `frozen` | **최초 percept 고정, 갱신 없음** | 🧱 **받침대** — 상태가 *있으나 안 움직임* (DV1 의 통제) |
| `shuffle` | ring 을 byte-정렬 | 🧪 **내용-절단 이동 arm** — 바이트 multiset·길이·feat8 동일, 순서(=내용)만 절단 (DV2 의 통제) |

## ⚠️ 발사 전 정정 — `shuffle` 을 DV1 의 CARRIER 통제로 둔 건 내 설계 오류였다

토이 배선 스모크(`lab/v6/pedestal.clm` · 3 emit · **DIRECTIONAL, 판정 아님**)가 이걸 먼저 잡았다:

| arm | writes/seeded | 씨앗 distinct(침묵) | modal(침묵) |
|---|---|---|---|
| `off` | — | 1/3 | 1.000 |
| `last` | 3/3 | 3/3 | 0.333 |
| `ring` | 3/3 | 3/3 | 0.333 |
| `frozen` | 3/3 | **1/3** | **1.000** |
| `shuffle` | 3/3 | 3/3 | 0.333 |

`frozen` 이 `off` 를 정확히 재현한 것(상태가 있어도 **안 움직이면** 반복이 남는다)은 arm 의미가 옳다는
증거다. 그런데 `shuffle` 도 떨어졌고, 이건 반증이 아니라 **DV 배치 오류**다: 씨앗이 조금이라도 달라지면
byte-identity 는 깨지므로 **`modal_emit_share` 위에서는 CARRIER 통제가 원리상 항상 발화**한다. 즉 원안대로
동결했으면 이 카드는 무엇을 재든 `CARRIER` 로 떨어지는, **결과가 미리 정해진 표**였다.

⟹ 정정: `shuffle` 은 **DV1(반복)의 통제가 아니라 DV2(내용)의 통제**다. 반복이 씨앗 상수성의 산물인지는
`frozen` 이 가르고, 상태의 *내용*이 입에 닿는지는 `shuffle` 이 가른다.
**이 정정은 303M 을 한 번도 돌리지 않은 상태에서 이뤄졌다** — 소각된 게이트의 재동결이 아니다
([[burned-gate-no-refreeze-sequential-gating]]). 토이 수치는 배선 증거일 뿐 어떤 바도 움직이지 않는다.

## DV (동결) 와 타당성 증인

- **DV1 (반복) = `modal_emit_share` (percept-SILENT 층)** — 최빈 byte-identical emit / 그 층의 emit 수.
  분모를 조작 적용 층으로 조건화하는 것은 이 파일이 이미 한 번 저지른 결함의 재발방지 규칙이다
  (`study-py-1`(e)). 전체 풀 값도 카드의 0.667 과의 연속성을 위해 **별도 층으로** 병기한다.
- **움직임 증인 = `seed_distinct_silent / seed_rows_silent`** — chat 이 기록하는 `seed_sha8`(입이 **실제로
  읽은** 앵커의 지문). 씨앗이 안 움직였으면 그 런은 **음성이 아니라 INVALID** 다
  ([[flat-across-manipulations-means-the-lane-is-dead]]).
- **배선 영수증** — 런 끝의 `percept-write: writes=… silent-ticks-seeded=…`. `seeded=0` 이면 플래그가
  파싱만 되고 기질에 닿지 않은 것(H_9853 형) ⟹ 자동 INVALID.

## 판정표 (사전 동결 · 발사 전)

**V. 타당성 게이트 (먼저 통과해야 아래를 읽는다)**
- V1 `off` arm 의 침묵층 DV ≥ 0.50 **그리고** `seed_distinct_silent(off) == 1`.
  → 안 그러면 **전제 파기**: 침묵 tick 씨앗이 애초에 상수가 아니었다는 뜻이고, 40턴 REPEAT 의 원인은
  다른 데 있다. 카드는 INVALID 로 닫고 원인을 다시 찾는다(tune-to-green 금지).
- V2 처치 arm(`last`·`ring`)의 `seed_distinct_silent ≥ 2` 그리고 `silent-ticks-seeded > 0`.
  → 안 그러면 **INVALID**(배선 미도달), 음성으로 읽지 않는다.

**판정 A — DV1(반복). 통제 = `frozen`**
| 결과 | 조건 | 읽기 |
|---|---|---|
| 🟢 **ARTIFACT-CONFIRMED** | `ring` 또는 `last` 의 침묵층 DV1 **< 0.50** 그리고 `frozen` **≥ 0.50** | 40턴 REPEAT 는 **동결 씨앗의 산물**. 결합 사다리는 이 배선을 켠 상태에서만 COMPOSE 를 읽을 수 있다 |
| 🔴 **KILL (카드의 kill 조건)** | 처치 arm 의 DV1 **≥ 0.50** 유지 (V 통과 = 씨앗은 실제로 움직였음) | 반복은 씨앗 탓이 아니다 ⟹ **결손은 전부 G1**. WRITE 로는 살 수 없다 |
| ⚪ **PEDESTAL-CONFOUND** | `frozen` 도 < 0.50 | 하락이 **움직임**이 아니라 "`live_seed` 가 아닌 아무 앵커"로 산 것 ⟹ 움직임 주장 불가 |
| 🟠 **REVERSED** | 처치 arm 의 DV1 > `off` | 우연 아래쪽까지 판정표가 덮는다([[prereg-table-must-cover-below-chance]]) — 쓰기가 반복을 **악화**시킴, 그 자체가 결과 |

**판정 B — DV2(내용). 통제 = `shuffle`**
DV2 = 침묵층의 `borrow_content` (교사 CONTENT 어휘가 입에 닿은 비율 · 받침대 있는 지표) + regime 계수.
DV1 이 떨어져도 그건 "반복이 죽었다"까지이므로, 상태의 **내용**이 실제로 실렸는지는 따로 물어야 한다.
| 결과 | 조건 | 읽기 |
|---|---|---|
| 🟢 **CONTENT-REACHES** | `ring` 의 DV2 > `off`, 그리고 `shuffle` 은 `off` 수준 | 순서(=내용)를 보존해야만 오르므로 **내용이 실렸다** |
| ⚪ **CARRIER** | `shuffle` 도 같이 오름 | 상승이 **바이트 다발·길이**로 산 것 ⟹ 내용 주장 불가 |
| 🔴 **NO-UPTAKE** | `ring` 의 DV2 ≈ `off` (침묵층 borrow_content 가 바닥) | 씨앗은 움직였는데 교사 어휘는 입에 안 닿는다 — 반복만 죽고 흡수는 없음 |

⚠️ **이 카드가 살 수 없는 것**: DV 가 떨어져도 그건 **반복이 죽었다**는 뜻이지 **COMPOSE 가 생겼다**는
뜻이 아니다. H_9984 가 미리 못 박은 대로 WRITE 는 REPEAT 는 죽이나 COMPOSE 는 못 산다. COMPOSE 는
G1(결합기)이 공급해야 하며 그건 ① 결합 사다리의 몫이다. 이 카드의 어떤 결과도 대화 능력 주장이 아니다.

## 검정력

침묵층 n=40, 기준선 1.000(40/40). 이항 SE 는 p=0.5 에서 0.079 이므로 1.000 → <0.50 판별은 여유가 크다
(관측 가능한 최소 하락 1/40 = 0.025). 즉 이 판정은 **검정력 부족으로 음성이 날 설계가 아니다**
([[power-before-negative-verdict]]).

## 교사 통제 — 5 arm 이 **byte-identical percept** 를 받아야 한다

LLM 교사는 런마다 발화가 달라져 arm 간 비교 자체가 성립하지 않는다. 그래서 원본 40턴에서 교사가 실제로
한 **40 발화를 그대로 추출해 고정 스크립트**로 쓰고(`--teacher script`), 5 arm 전부 같은 바이트를 먹인다.
합성 드릴이 아니라 **실제 자연 교사 발화의 재생**이므로 p9 상 corpus regime = `natural`(재생).
확인용 2차: 승리 arm 1개를 라이브 교사로 한 번 더 돌려 반응형 교사에서도 사는지 본다.

## 실행

```
anima-py study ~/anima-weights/py303_full.clm --teacher script --script percepts40.txt \
  --rounds 40 --window 3 --chat-flag --percept-write --chat-flag <arm> --out <arm>.jsonl --report <arm>.json
```
303M 은 **pool 에서만**(mini 금지 · [[heavy-anima-eval-pool-not-mini]]). 5 arm × 120 tick.

regime: `natural`(교사 발화 재생) · tier-ceiling: 이 카드는 **계기/배선 판정**이며 대화 능력 주장 아님.
