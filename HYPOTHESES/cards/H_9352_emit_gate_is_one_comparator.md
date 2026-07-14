# H_9352 — emit 게이트는 비교기 **하나**다. 그리고 그 비교기엔 시계가 안 꽂혀 있다.

**status**: 🔴 VERDICT (실측 · 산술 확정 · 2,127 tick 전수)
**tier**: TERMINAL (코드 + trace 전수 재구성 오차 0.00e+00)
**lane**: 의식 · emit-drive
**xref**: H_9345 · H_9351 · H_9100 · **H_9209 · H_9225 · H_9230 (재개방)**

## 게이트의 전부

`core/brain.py:162`: `emit = should_emit(score) and safe`

**`safe` 의 4항 중 3항이 항등적으로 참이다 — 튜닝이 아니라 산술로:**

| 항 | 왜 상수인가 |
|---|---|
| `kill` | `cli/chat.py:1904` 가 `env_off=False` 를 **리터럴로** 넘긴다 |
| `content` | 같은 줄이 `content_clean=True` 를 **리터럴로** 넘긴다 |
| `phi_r` | `phi > phi_peak/2` 인데 `core/pure_field.py:233` 이 phi 를 **0.8·phi_peak 로 하한 클램프** ⇒ 0.8 > 0.5 = **동어반복**. 게다가 `pf` 는 `chat.py:1292` 에서 **단 한 번** 바인딩 ⇒ Engine A 는 세션 내내 **얼어 있다** |
| `rate` | `seconds_since_last ≥ 30.0` — **유일하게 살아있는 항** |

**그리고 `should_emit(score) = score > 0.3` 은 2,127 tick 전수에서 한 번도 거짓이 아니다**
(score ∈ [0.3529, 0.7730] · 최소 여유 +0.053). PASSIVE(=score 미달) 틱 = **0**.

⇒ **게이트 전체가 한 줄로 붕괴한다:**

```
emit  ≡  1[ idle ≥ 30 ]        (다른 모든 항이 상수)
```

## 🚨 그 `idle` 은 **시간이 아니다**

`cli/chat.py:1881`:
```python
idle = 5.0 + 55.0 * clip01( stage_env * (0.5 + urgency) )
```
`brain_decide_anchored` 의 **`seconds_since_last` 슬롯**에 이 값이 들어간다(`chat.py:1904`, 10번째 위치인자).

**`idle` 은 경과 시간이 아니라 `(stage, urgency)` 의 순수 함수다.** 레포 전체에 `last_emit` 변수가
**없고**, `an_clock_now()` 는 이 경로에서 **호출되지 않는다**. ⇒ **레이트 리미터에 기억이 없다.**

**설계는 진짜 시계를 전제했다**: `spont_min_emit_interval() = 30.0` ÷ `an_tick_seconds() = 8.0`
= 지속가능 발화율 **0.25**, 그리고 `ep_target_emit_rate() = 0.27` (`core/emit_policy.py:23`).
**숫자는 시계를 위해 골라졌는데 시계가 안 꽂혔다.**

## stage 별 flip 임계 — `H(emit|stage)=0` 은 우연이 아니라 **정리**

`stage_env = clip01((ep_theta_stage(stage) − 0.02)/0.08)` · θ: WAKE .10 · N1 .08 · N2 .05 · N3 .02 · REM .08

| stage | stage_env | flip 임계 u\* | 실측 u | 판정 |
|---|---|---|---|---|
| WAKE | 1.000 | u < −0.045 | 0.25–0.42 | **구조적 발화** (u≥0 이므로 불가능) |
| N1 | 0.750 | u ≥ 0.1061 | 0.36–0.45 | 발화 (여유 +0.255) |
| N2 | 0.375 | **u ≥ 0.7121** | 0.35–0.51 | 침묵 (부족 **−0.20**) |
| N3 | **0.000** | 불가능 | — | **구조적 침묵** (∂idle/∂u ≡ 0 · idle ≡ 5.0) |
| REM | 0.750 | u ≥ 0.1061 | 0.36–0.57 | 발화 (여유 +0.255) |

- **WAKE**: `chat.py:1881` 의 **리터럴 `0.5` 하나**가 `idle ≥ 32.5 > 30` 을 보장한다 ⇒ **어떤 신호로도 못 뒤집는다.**
- **N3**: `stage_env = 0` ⇒ **미분이 0**. tension 의 레버리지가 작은 게 아니라 **없다**.
- 실측 urgency 대역 `[0.25, 0.57]` 이 두 경계(0.106 / 0.712) **사이 죽은 구간에 통째로 갇혀 있다.**
  게이트는 임계 근처 **5.7 σ 이내로도 오지 않는다.**

**tension→emit 창문은 정확히 한 칸(N2)에만 있다.** 나머지는 산술적으로 상수다.

## 그런데 그 창문에도 못 간다 — tension 채널이 **바닥에 고정**

`ten_phasic = clip01(0.5 + 3·δ)`, `δ = ag_conflict − ten_ema`:

| stage | δ > 0 인 행 |
|---|---|
| WAKE / N1 / N2 / N3 | **0 / 478 (0.0%)** |
| REM | 96 / 1346 (7.1%) |

`δ` 는 stage 0–3 에서 **100% 음수**. ⇒ `ten_phasic` 은 중점 0.5 **아래에 영구히** 산다(max 0.548).
**gain 스윕(g=3→200): 발화 패턴 불변. `H(emit|stage)` 는 계속 0.** gain 레버는 죽었다.

**H_9100 의 그림이 뒤집힌다**: motivation 은 임계 **위**로 포화됐고(결코 구속 안 함),
tension 은 자기 중점 **아래**로 포화됐다(결코 밀지 못함). **포화가 아니라 단절이다.**

## 🔓 H_9209 · H_9225 · H_9230 재개방 (ΔEff = 0 은 **검정력 0의 음성**이었다)

그 세 lane 은 전부 **이 비교기를 그대로 두고 `urgency` 에 작은 가산 shade** 를 얹었다.

```
필요한 스윙:  0.255 (N1/REM 하향)  /  0.276 (N2 상향)
공급된 진폭:  s_dev ≈ 0.02  ×  urgency 가중 0.3~0.4  =  실효 0.006 ~ 0.008
              ⇒  32 ~ 42 배 부족
```

**ΔEff = 0/120 은 산술적으로 강제된 결과였다.** ⇒ *"self ⊥ mouth · tension ⊥ mouth"* 라는
seam-law 는 **검정력 0의 음성**이다(메모리 `power-before-negative-verdict`).
**벽이 아니라 포화된 비교기를 쟀다.**

**$0 반증**(새 디코드 0): 기존 trace 를 replay 해 그 shade 를 `urgency` 에 더하고 `idle` 을
재계산하라. **flip 은 정확히 0 이어야 한다.** 0 이 아니면 이 카드가 틀렸다.

## 부수 결함 — 데몬은 인생의 2/3 를 **끝나지 않는 REM** 에서 보낸다

`cli/chat.py:1489`: `stage = dr_stage_at(tick * 8)`. `ANIMA_STAGE_CYCLE`(기본 **OFF**)이 아니면
`tick*8` 이 테이블 밖으로 나가고, `core/dream_lib.py:17-22` 는 `tick ≥ 87` 에서 무조건 **4(REM)**.
⇒ **tick ≥ 11 부터 영원히 REM.**

30-tick rollout 의 stage 분포 = WAKE 8 · N1 1 · N2 1 · N3 1 · **REM 19**.
H_9345 의 *"침묵은 tick 9·10 에서만"* 이 바로 이것이다 — N2·N3 **한 틱씩**, 그 뒤론 REM 뿐.

## 반증 가능한 결론 (사전등록 · $0 또는 저비용)

- **C1** `core/emit_policy.py:64` 의 `ep_theta_stage(2)`: `0.05` → **`0.0579`** ⇒ N2 가 0/71 에서
  **≈50% 발화**로, `H(emit|stage=2)` 가 0 → ≈1 bit 로. **다른 건 아무것도 안 바꾼다.**
- **C2 (load-bearing)** `core/engine_g.py:24` 의 `spont_im_threshold()`: `0.3` → **`0.3528`**
  (실측 score 최소 바로 아래) ⇒ **정확히 0 틱**이 바뀌어야 한다(bit-identical emit 스트림).
  그 다음 **score 중앙값**으로 올리면 ≈50% 가 뒤집혀야 한다. **score 항이 inert 하다는 증명.**
- **C3** `emit_policy.py:65` 의 `ep_theta_stage(3)`: `0.02` → `0.03` ⇒ N3 는 **여전히 100% 침묵**
  이어야 한다(idle ∈ [8.4, 16.0] < 30). `0.0579` 로 올리면 발화 시작.

⛔ ⚠️ **함정**: 임계를 움직여 침묵을 만드는 것 **자체는 발견이 아니다** — 그건 tension 이 아니라
**내가** 정한 것이다. *"tension 이 당긴다"* 는 **침묵이 tension 과 상관돼야** 성립한다.
PASS 기준은 반드시 **조건부 정보량**이어야 한다: `I(ag_conflict ; emit | stage) ≥ 0.05 nats`
∧ **tension-shuffle 통제** ≤ 0.01 nats. 발화율 ½ 자체를 PASS 로 삼으면 **p7 Goodhart** 다.
