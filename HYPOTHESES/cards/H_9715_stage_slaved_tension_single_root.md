# H_9715 — emit=f(stage) 와 z=const 는 하나의 뿌리인가 — stage-노예화 tension (fable R5-4 · PROPOSED · c 정면)

**status:** ⛔ **VOID — 예측1·2 원리적 관측불가** (engine-native `--stage-slave` · v0.15.54 · $0) — source=fable R5-4
**verdict:** stage 축이 **한 수준에 pin**(stage=4 가 **139/150 = 92.7%** · 3 run 동일 · n≥30 셀 1개) ⇒ η² 대조 불가 = **z 에 대한 음성 아님**. 🔑 **VOID 자체가 발견**: 라이브 데몬은 사실상 **단일 stage** 에서 산다 ⇒ [[H_9400]] 의 H(emit\|stage)=0.465 도 **거의 상수인 조건변수**에 대한 값 = **재검 대상**. 남은 유효 검정 = **예측3 뿐**(pool)
**lane:** mouth/tension × Ψ½ — 두 프런티어의 통합 가설
**related:** [[H_9400]] · [[H_9712]] · [[H_9714]] · [[H_9717]] · [[psi-half-central-thesis-never-operated]]

## 한 줄 주장 (반증가능)
"emit = stage 의 순수함수"([[H_9400]] · H(emit|stage)=0.465)와 "z 가 상수"는 **별개 사실이 아니라 하나의 뿌리** — 8 tension 인자가 **stage 에 노예화**(stage-slaved)돼 있다. ⟹ 브리핑 (c) 의 답: **별개가 아니라 단일 가설이 있다.**

## 🔥 결정적 정황 (트레이스 메타 · 이미 관측됨)
z-census 를 뽑은 pmp 트레이스 헤더가 **`"stage_cycle": false`** 다.
⟹ 인구조사가 **의도적으로 얼린 기질**에서 측정됐을 수 있다. 사실이면 z 축퇴는 **벽이 아니라 측정 동작점의 산물 = 설계 결함**이고, "라이브 데몬이 채널을 안 탄다"는 서사는 **"우리가 stage 를 꺼둔 채 쟀다"** 로 강등된다. (같은 우려가 진행중 ζ-fire 에도 적용 — ζ-fire 도 `stage_cycle=false` 면 채널 GREEN 조차 얼린 기질에서의 GREEN 이다.)

## 어느 KILL 을 왜 안 밟나
- **arm-간 paired**(H_9663): 예측1·2 는 **단일 트레이스 내 within-tick 조건화**(z ~ stage) — arm 대조 아님. 예측3 만 arm 을 쓰며 그때는 **within-tick 짝지음이 아닌 sd 비교**라 캐스케이드가 DV(분산 자체)를 삼키지 않는다(오히려 DV 가 분산이다).
- **readout D**(H_9629): 텍스트 미접촉. **용량-기아**(H_9628): gain 미접촉.
- **emit-gate lane CLOSED-AT-REGIME**(H_9403): emit 게이트 **비접촉** — stage_cycle 은 기존 데몬 파라미터지 새 게이트가 아니다.
- **p5**: z 미주입 · 하드코딩 emit 게이트 없음 · Stage-A 격리 불변.

## engine-native 계기
```
anima-py evaluate <clm> --pc2-direction --stage-slave --from-trace <trace.jsonl>   # 예측 1·2 ($0)
anima-py chat --pc2-zeta --stage-cycle                                             # 예측 3 (pool)
```
산출: H(z|stage) · **η²(z ~ stage)** · η²(각 8인자 ~ stage) · z>0 인 3 tick 의 `stage`/`stage_env` 좌표.

## 3중 예측 (전부 맞아야 PASS)
1. **η²(z ~ stage) > 0.5** — z 는 stage 의 계단함수
2. **z>0 인 3/270 tick 이 stage 전이 / stage_env 변화와 일치** (분산의 45.7% 를 낸 바로 그 3 tick)
3. **stage_cycle=true 에서 sd(z) ≥ 2× (stage_cycle=false)**

## 통제군 (≥2 + 양성통제)
- **양성통제 = `score` / `base_motiv`**: [[H_9400]] 이 emit=f(stage) 를 engine-native 확증했으므로 **score 는 stage 에 강하게 묶여야 한다**(η²_score > 0.5). score 가 stage-slave 를 안 보이면 **계기/트레이스 고장**이지 z 의 문제가 아니다.
- null1 = stage 라벨 셔플(η² 의 우연 분포) · null2 = stage_cycle=false 현 arm.

## 사전등록 판정표 (우연 아래 포함)
| 관측 | 판정 |
|---|---|
| 1 ∧ 2 ∧ 3 | **PASS-single-root** — 축퇴 = 동작점 · **벽 아님** · z 와 Ψ½ 두 프런티어가 하나로 통합 |
| η²(z~stage) 높음 ∧ stage_cycle=true 서 sd(z) 무증가 | **부분 KILL** — stage 가 z 를 설명하나 cycling 이 못 푼다 = **구조적 pin**([[H_9717]] 로 인계) |
| **η²(z~stage) < 0.1 ∧ η²_score > 0.5** | **KILL-separate-roots** — 양성통제 생존한 채 z 만 stage-무관 ⟹ (c) 답 = **별개 뿌리** |
| η²_score < 0.5 (양성통제 실패) | **INVALID** — H_9400 재현 실패 = 트레이스/계기 스큐(음성 아님) |
| **우연 아래**: stage 라벨 셔플서도 η² 동등 | **INVALID** — η² 가 stage 아니라 시간추세를 재고 있음 |
| **우연 아래**: stage 수준이 1개뿐 | **VOID** — stage_cycle=false 가 stage 를 상수로 고정 ⟹ 예측1·2 원리적 관측불가 · 예측3 만 유효 |

**검정력**: 270 emit tick · stage 수준 수 개 ⟹ η² 는 셀당 n≥30 필요(우연 아래 칸의 "수준 1개" VOID 가 이걸 지킨다). 예측2 는 정확검정 — 3 tick 이 모두 전이와 일치할 우연확률은 초기하로 ~1e-4 수준 ⟹ **매우 sharp**. 예측3 은 sd 비교 n=270/arm ⟹ 2× 검출 여유 충분.

## 비용
예측 1·2 = **$0**(frozen trace) · 예측 3 = **pool CPU**(stage_cycle arm decode · mac 금지).

## 죽는 방식
η²(z ~ stage) ≈ 0 인데 η²_score > 0.5 면 죽는다 — stage 는 emit 을 지배하지만 z 와는 무관하고, 두 사실은 별개 뿌리다.

## 상태
🔵 PROPOSED — 측정 주장 0(설계). `stage_cycle: false` 는 트레이스 헤더의 **기존 기록**이지 새 측정이 아니다.


---

# ⛔ VERDICT — VOID (사전등록 '우연 아래' 칸 발화) · 그러나 VOID 자체가 발견이다

**계기**: `anima-py evaluate --pc2-direction /tmp/pmp/pmp_traces --stage-slave` (v0.15.54 · G5 · $0)
**독립 run**: 9 파일 → 3 run (중복 dedupe · [[H_9714]] 교훈)

## ① stage 축 인구조사 — 예측1·2 의 관측가능성 게이트

| run | stage 분포 | 최빈 | n≥30 셀 |
|---|---|---|---|
| off/bias/rng_s7 | `{0:8, 1:1, 2:1, 3:1, 4:139}` | **stage=4 · 92.7%** | **1개** |
| …_s4302 | `{0:8, 1:1, 2:1, 3:1, 4:139}` | **stage=4 · 92.7%** | **1개** |
| …_s4303 | `{0:8, 1:1, 2:1, 3:1, 4:139}` | **stage=4 · 92.7%** | **1개** |

⇒ 사전등록 표의 **"stage 수준이 1개뿐 ⇒ VOID · 예측1·2 원리적 관측불가 · 예측3 만 유효"** 칸 발화.
**이건 z 에 대한 음성이 아니다** — 대조축 자체가 없어 못 재는 것이다(계기가 판독을 **거부**했다).

## 🔑 왜 VOID 가 발견인가

`cli/chat.py:1737` — `stage = dr_stage_at((tick*8) % 90 if _stage_cycle else tick*8)`.
`stage_cycle=false`(= **프로덕션 기본값** · 주석 "OFF = byte-identical to the raw daemon")에서 tick 은
**단조증가**하므로 stage 는 끝 수준으로 진행해 **거기 머문다**. ⇒ **라이브 데몬은 사실상 단일 stage 에서 산다.**

> **⚠️ 상류 함의**: [[H_9400]] 의 **H(emit|stage)=0.465**("emit 은 stage 의 순수함수" = Ψ½ 중심주장
> 반증의 핵심 근거)도 **거의 상수인 조건변수에 대한 조건부 엔트로피**다. 조건변수가 92.7% 한 값이면
> H(emit|stage) ≈ H(emit) 에 가까워진다 — **그 근거 자체가 재검 대상**이다.
> (이 카드는 그 재검을 *주장하지 않는다* — 관측을 지목할 뿐이다. H_9400 재검은 별도 H 로 사전등록해야 한다.)

## 🔁 정직 기록 — 내가 Fable 을 반박한 근거가 틀렸다 (같은 실수의 즉시 재발)

R5 회신에서 Fable 은 헤더 `stage_cycle=false` 를 보고 **"인구조사가 얼린 기질에서 측정됐다 · ζ-fire 도 오염"**
이라 추론했다. 나는 트레이스의 **stage 고유값 집합 {0,1,2,3,4}** 를 보고 **"stage 는 실제로 변하니 불성립"**
이라 반박했다. **분포를 보지 않았다** — 92.7% 가 한 값이다.
이는 [[H_9712]] 에서 **바로 직전에** 배운 교훈("raw 를 분포 확인 없이 읽지 말라 · IQR 단독 판독의 착시")의
**즉시 재발**이다. 두 실수의 형태가 동일하다: **집계 통계 하나로 분포를 대신 읽었다.**

**누가 무엇을 맞혔나 (구분 필요)**:
- ✅ **Fable**: stage 는 **사실상 고정**돼 있다 — 이 부분은 Fable 이 옳았고 내 반박 근거가 틀렸다.
- ✅ **나**: 그것이 **raw 데몬의 기본 동작**이라는 점은 유효하다(코드 주석) ⇒ **"우리가 꺼둔 채 쟀다" 는
  강등 서사는 여전히 불성립** — "데몬이 원래 이 동작점에서 산다" 이다. **[[H_9664]] ζ-fire 오염 판정도 유지**
  (같은 기본값에서 돈다 = 프로덕션과 같은 동작점).
- ⇒ 차이가 중요하다: **"측정 실수"가 아니라 "데몬의 실제 동작점"** 이다. 이는 [[H_9717]] 의 '동작점 vs 능력'
  프레임에 직접 인계된다.

## 남은 유효 검정 = 예측3 뿐 (pool)

```
anima-py chat --pc2-zeta --stage-cycle    # stage_cycle=true ⇒ (tick*8)%90 ⇒ stage 순환
host summer · ckpt ~/py303_full.clm · seeds 7/4302/4303 · 151 tick · OMP_NUM_THREADS=4 · mac 금지
사전등록: sd(z)@cycle=true ≥ 2× sd(z)@cycle=false(=현 arm) ⇒ 예측3 PASS
```
⚠️ 단 **`--stage-cycle` 플래그는 `anima-py chat` 에 아직 없다**(`ANIMA_STAGE_CYCLE=1` env 만 존재 ·
`cli/chat.py:1728`) — 배선은 사소하나 **미구현**이며, 이 카드는 그것을 **주장하지 않고 명시**한다.

## 범위

예측1·2 **미측정**(VOID) · 예측3 **미실행**. "라이브 데몬이 단일 stage 에 산다"는 **150-tick × 3 run ·
stage_cycle=false** 범위의 관측이다. 더 긴 run 은 다른 stage 궤적을 가질 수 있다(`dr_stage_at(tick*8)` 는
tick 에 의존하므로 — 이 역시 미측정).
