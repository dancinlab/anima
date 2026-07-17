# H_9715 — emit=f(stage) 와 z=const 는 하나의 뿌리인가 — stage-노예화 tension (fable R5-4 · PROPOSED · c 정면)

**status:** 🔵 PROPOSED (미실행 · lab full R5 · 사전등록 · 예측1·2 는 $0) — source=fable R5-4
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
