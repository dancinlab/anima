# H_9762 — R8-2 · TWO-HISTORIES-COMMON-FUTURE exact-relock — interior-부재 SUFFICIENT 의 동역학 다리 (fading-memory 검정)

**status:** 🔵 PROPOSED (lab full Fable 5 심화 · R8 · pool CPU/GPU chat · 사전등록 · H_9761 상수 유도 후 발사)
**lane:** theta-alive-sigma-rebase (H_9749 STATE-QUOTIENT STRONG-DIRECTIONAL → 충분조건 승격 · Sol 경고 봉인 주다리)
**related:** [[H_9749]] · [[H_9761]] · [[H_9763]] · [[H_9738]] · [[H_9728]] · [[H_9760]]

## ① 한 줄 주장 (반증가능)

상이 public prefix H_A≠H_B (각 L tick) 로 분화시킨 두 동일-init 데몬을 **동일 공통 future percept** N tick 으로
구동하면 decision-trace 가 **exact relock**(TIER-1 d≡0 도달 후 W 유지)한다 = fading memory(echo-state property)
= **persistent private residue 0**. 표준 형식 프레임: Boyd–Chua fading-memory / echo-state property — 표준적이며 명명된 검정.

## ② Sol-gap ("public fading ≠ private state 부재") 봉인 논증 — 통제로 닫는다

3단 삼단논법: (1) C0 결정성([[H_9749]]② sha b13443a4) ⟹ state = f(init, public afferent history) — private **SOURCE** 없음.
(2) fading 실측 ⟹ state = f(최근 bounded window). (3) window 는 관측된 public record ⟹ state 재구성 가능 ⟹ private residue 0.
잔여 leak 2개를 통제로 봉인: **same-init**(ckpt+빌드 sha 사전 고정·기록) · **미분화 confound**(아래 evaluability 통제 — prefix 가 state 를 실제로 갈랐음을 요구).
자기발화 루프(emit→lane 재주입)는 p5 상 mouth 문맥 미재진입 + 발화 자체가 public record ⟹ 자기유지 발산도 public-매개 = private 아님(판정식 분기 ④-c 로 분류).

## ③ 계기 (engine-native · 신규 조작 = anima-py 플래그 1개)

- `anima-py chat --percept-script <jsonl>` — 기존 `percept_source` 콜러블(`cli/chat.py:395` · anima study 계보)의 CLI 승격.
  tick→percept 결정론 스크립트. **p5 합법**(percept = 타자 afferent · self-seed 아님).
- trace = `ANIMA_DECISION_TRACE=<path>` (기존 · stdout 금지). 비교기 = trace JSONL 오프라인 diff(포워드 재실행 없음 — probe 아님).
- tick 정렬: 두 prefix **등길이 L** ⟹ 공통 phase 절대 tick 일치(tick-의존 상수 confound 제거).

## ④ 사전등록 판정식 (bar 에 tunable 0개)

**metric:** TIER-1 `d1(t)` = [emit-bit ⊕ emit bytes] exact 불일치 지시자 · TIER-2 `d2(t)` = canonical trace-line byte 불일치
(whitelist = timestamp 제외 전 필드). **ε 없음 — 기질이 byte-det(C0 sha 확증)이므로 bar = exact 0.** 상수 L·W·N 은 [[H_9761]] 코드 유도(§④).

**battery:** 4 register cell(ko/en × general/SNS · a_chat_registers) 교차 6 pair + 동일-cell 내용대비 2 pair.
**validity(pair):** prefix 당 emit ≥10 (lane write 는 emit-gated — emit 0 prefix 는 state 를 안 씀 ⟹ INVALID pair, 미집계).

**통제 (≥2 · collapse-Δ 프레임):**
- ⓐ **C0 floor**: 동일 prefix 2-run → d≡0 (계기 유효성 · 이미 sha 확증, 본 세팅 재확인)
- ⓑ **ceiling**: 공통 future 없이 상이 percept 지속 → d 높게 유지 (metric 동적범위 생존)
- ⓒ **positive persistence detector**: [[H_9763]] kosmos-swap arm 이 발산을 만들 수 있어야 함 (지속상태 검출능력 증명 · positive-control-before-reading-a-negative)

**evaluability:** pair 는 공통 phase 초기창 t<W 에서 max d2>0 이어야 판독가능. tick0 부터 d≡0 인 pair → 디스크 lane file-diff 로
{state-equal | behaviorally-silent} 분류. **전 pair d≡0 = INSTRUMENT-DEAD**(prefix 분화 실패 → 배터리 강화 재발사, 판정 금지).

**verdict:**
- (a) **NO-INTERIOR-SUFFICIENT(within-session)** ⟺ ⓐⓑⓒ 성립 ∧ 모든 evaluable pair 가 t≤N−W 에서 TIER-1 0 도달 후 W 유지 ∧ 비-evaluable pair 전부 state-equal 분류.
- (b) 1 pair 라도 지평 N 에서 TIER-1 발산 유지 = **INTERIOR-CANDIDATE** (음성이 결과 — 프런티어 재개봉 · 다음 H = 잔류의 내용구조 분석: structured vs 카오스 증폭).
- (c) 발산이 자기발화-매개로만 지속(발산 tick 이 항상 선행 자기 emit 차이에 후속·percept 동일) = **PUBLIC-LOOP residue** — private 아님(별도 흥미 발견으로 기록).
- (d) TIER-1 relock ∧ TIER-2 미relock (N_fp 이후에도) = sub-decisional fp 잔류 — 진단 기록·판정 불변.

## ⑤ falsify
(b)가 곧 반증이고, 그게 발견이다. tune-to-green 불가: bar=exact0·상수=코드유도·battery=사전등록.

## kill-list 비충돌
- H_9729(own-ness⊥context-continuity probe)와 다름 — probe 가 아니라 history-조작 수렴검정(do on public history).
- H_9739 KEY-LADDER(트리거 키 탐색)와 다름 — 키 탐색 없음; content-∀ 봉인은 [[H_9763]] transplant 가 담당.
- ½-인식 렌즈·quantile·타이밍 계열 무관. relock 개념은 H_9728 계보 재사용이나 대상이 다름(½-schedule 아닌 state washout).
