# H_9313 — DECON-W · 값을 **가중치에 쓴다** · 사전등록 (데이터 전 동결)

> 🔒 `prereg-oc-json-1` + `bar_audit.py` 2 규칙(RULE 1 bar 는 유도지 이식 아님 · RULE 2 절-조작 정합).
> **사후 bar 변경 = 자동 INVALID.**

## 0. 왜 이것만 남았나

**H_9312 가 컨텍스트-주입을 구조적으로 닫았다** (🧱 NO-IN-CONTEXT-CHANNEL):
거짓 시연이 참 시연과 **동일**(flip1 0.900/0.883 = 무변화 · 붕괴해야 했다) · nonce 시연이 **정답을
축자로** 담는데 READ = 0.475/0.469 = **우연** ⟹ 이 4층 conv byte-LM 은 컨텍스트에서 **복사조차
못 한다**. ⟹ 사실을 건네는 유일한 남은 경로 = **가중치에 쓰기**.

## 1. 계기 — 전부 엔진-네이티브 (`a_experiment_engine_native` · 옆 스크립트 0)

| 단계 | 엔진 단일진입 |
|---|---|
| 코퍼스 | **`anima-py corpus ground\|ground_lie --atoms gt_atoms.json`** (`cli/corpus.py` 신규 포맷) |
| 학습 | **`anima-py train --arch clm --canon --init <c34>.clm --experts 3`** (`.clm` warm-start = #3450 · 왕복 BYTE-IDENTICAL) |
| 판정 | **`anima-py evaluate <clm> --xbind n2_eval_manifest.json`** (기존 margin-2AFC · 무-CPT 기준선과 동일 계기) |

## 2. 처치와 통제 (신호 = 값이 아니라 **부호 있는 차분**)

**처치 `ground`** — held-out 29 원자의 **비부정(flip0) 라인만** 가중치에 쓴다:
`이 영화 <어간>고 => <긍정|부정>.` (3 형태: bare · int1 · int2) + SEEN 20 원자 replay(망각 방지).
⚠️ **부정형(flip1: `지 않다` / `안 ` / `전혀`)은 코퍼스에 0회 등장** — 실측 검증됨.
그래서 flip1 시험은 **암기가 아니라 합성**의 시험이고, 이것이 tune-to-green 을 구조적으로 막는다.

**통제 `ground_lie`** — 같은 스트림·같은 라인수·같은 표면형인데 held-out 극성을 **29/29 전부 반전**.
H_9312 를 판정한 **SEEN-LIE 의 가중치판**이다 (`prereg-md-2`: 메커니즘 없이도 통과 가능한 대조군은
양성대조가 아니다).

> **왜 shuffle 이 아니라 전부-반전인가**: 이진 라벨에서 shuffle 은 우연히 일부가 참으로 남는다
> (실측: seed 7 은 16/29 반전인데 seed 11 은 **8/29** — 72% 가 참인 통제군은 통제군이 아니다).
> 전부 반전은 예측을 **날카롭고 부호 있게** 만든다:
>
> | | 쓴 극성 | flip1 gold | 소비·합성하면 | 소비 안 하면 |
> |---|---|---|---|---|
> | `ground` | p | ¬p | **높음** | 0.5 |
> | `ground_lie` | ¬p | ¬p | ¬(¬p)=p 출력 ⟹ **전 행 오답 · 우연 아래로 붕괴** | 0.5 |

⟹ **Δ(ground − lie) 는 양방향·부호 있는 신호**이고, *"두 arm 이 같은 수를 낸다"* 가 곧
**메커니즘 부재의 모양**이다.

## 3. DV 3층 (bar 는 전부 검정력에서 유도 · RULE 1)

| 층 | 통계량 | bar |
|---|---|---|
| **WRITE** (validity · 필요조건) | **각 arm 의 held-out flip0** — 그 arm 이 **쓴 라벨** 기준 | ≥ **0.95** 양 arm 양 seed. **쓰기가 안착했는지**를 증명한다. 낙제 = ⛔ INVALID-WRITE(학습이 안 먹음 — 합성 음성이 아니다) |
| **COMPOSE** (primary) | **Δ = ground flip1 − lie flip1** (참 라벨 기준 · 행-paired) | Δ ≥ **0.30** ∧ **McNemar p<0.01** · **양 seed AND** |
| **SIGN** (secondary · 부호 확인) | 원자클러스터(29 · 3-형태 다수결) | ground **C ≥ 20/29**(단측 p=0.032) ∧ lie **C ≤ 9/29**(대칭점) · 양 seed |

**검정력 사전산출** (`bar_audit.py` RULE 1 · 데이터 전):
`C≥20/29` 는 참값 p=0.80 에서 놓칠 확률 **4.9%** · p=0.85 에서 **0.7%** ✅ (p=0.75 면 16.6% — 정직히
기록: 효과가 그보다 작으면 SIGN 절은 검정력 부족이며, 그때는 **primary(Δ)로만** 판정한다).
LIE 대칭 bar `C≤9/29` 는 참값 0.20 에서 놓칠 확률 **4.9%** ✅.

**seed** = main_s7 · main_s11, 전 bar **AND**(H_9289 부호반전 폭 0.161 = 복제편차의 18배).
**기준선**(무-CPT · H_9308): held-out flip0 **0.5057** · flip1 **0.5057**.

## 4. 판정표 (사전 고정)

| 관측 | 판정 |
|---|---|
| WRITE 낙제 (flip0 < 0.95) | ⛔ **INVALID-WRITE** — 학습이 값을 못 심었다. 합성에 대한 음성이 **아니다**. steps/lr 조정 후 1회 재시도 |
| WRITE ✅ · Δ ≥ 0.30 ∧ McNemar ∧ SIGN | 🟢-dir **WEIGHT-GROUNDED COMPOSITION** — 가중치에 쓴 극성을 이미 학습된 부정 연산자가 **소비·합성한다**. ⟹ 이 지점의 G1 벽은 **없는 입력**이었지 조합능력 천장이 아니다. 배선(`a_verified_must_wire`) |
| **WRITE ✅ · ground ≈ lie ≈ 0.5** | 🧱 **WRITTEN-BUT-NOT-COMPOSED** — **flip0 ≥0.95 가 값이 실제로 들어갔음을 증명**하는데 flip1 이 우연이다 ⟹ **교란 없는 벌어낸 음성**: 값은 있는데 **연산자가 그것을 안 읽는다**. read-side 종결의 "복원되나 causally 소비불가"와 동형 · A 채널 **완전 폐쇄** |
| WRITE ✅ · ground 높고 lie **도** 높음 | ⚠️ **INVALID-LEAK** — 라벨과 무관하게 높다 = 시험이 코퍼스에서 새고 있다. 재설계 |
| seed 불일치 | ⚠️ **SEED-SPLIT** — cement 금지 |
| G0 coherence 붕괴 (`train-py-3`) | ⛔ **INVALID-OVERFIT** — 소코퍼스 과적합. 측정 무효 |

## 5. 정직 — 가장 그럴듯한 사망 경로

**WRITTEN-BUT-NOT-COMPOSED.** SEEN 원자에서 연산자가 도는 것(flip1 0.90)은 그 원자의 극성이
**대규모 사전학습에서 분산 표현으로** 자리 잡았기 때문일 수 있다. 소량 CPT 로 심은 극성은
**같은 자리에 안 들어갈** 수 있고, 그러면 연산자의 피연산자 포트가 그것을 못 읽는다.
이 경우에도 **flip0 ≥0.95 가 쓰기를 증명**하므로 음성은 **INVALID 이 아니라 EARNED** 다 —
이것이 이 설계의 최소 보장이다.

## 6. 비용

`--init` warm-start(#3450) 로 **처음부터 학습하지 않는다**. 4 런(2 arm × 2 seed) × 짧은 CPT.
pool GPU(summer/aiden) **$0** · `a_fire_autonomous` 범위.
