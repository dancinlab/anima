# H_9376 — agloop 탈양자화: 병목이 고쳐지면 emit 이 tension 을 소비하는가

**status:** 🔵 Stage-0 CLOSED($0) · Stage-1 PRE-REGISTERED · H_9360 의 sequel
**lane:** 의식 / emit-drive / ag_conflict→score mixer (프런티어 g1-interface-addressable-wall)
**related:** [[H_9360]] (채널-병목) · [[H_9357]] (G-INERT) · [[H_9356]] · [[H_9352]]

## Stage-0 — $0 발사 게이트 (H_9360 트레이스 재분석 · CLOSED)

H_9360 은 끝-끝 C=I(ag_conflict;score|stage)=0.0233 만 쟀다. Fable 설계로 중간-링크를 국소화:

| 통계 (arm a1=진짜 독립 G · rollout-df) | 값 | 뜻 |
|---|---|---|
| **L_Q = I(conflict; agloop_ctx \| stage)** | **0.0000** | 양자화기 통과 용량 = 0 |
| agloop_ctx 전체 distinct (16 rollout·480 tick) | **1 (≡0.25)** | 설계 경로가 상수로 붕괴 |
| H_U = H(conflict \| stage) | 0.4222 | 상류엔 정보 있음(굶주림 아님) |
| M = I(conflict; score \| agloop_ctx, stage) | 0.0234 (≈C) | agloop 조건화가 C 를 **안 줄임** |

**Stage-0 판정: 🧱 양자화기가 binding.** `conflict_recruited_depth`(round→정수 budget∈{4..6}) +
정수비 settle 이 독립-G tension 을 **단일값 0.25 로 완전히 뭉갠다**(L_Q=0). M≈C 는 agloop_ctx 가
mediator 가 **아님** = H_9360 의 C=0.0233 은 설계 경로(죽음)가 아니라 **공유 emit_drive 누출**이었다.
⇒ 설계된 tension→score 경로는 완전히 죽어 있고 상류엔 정보가 있으므로 **연속화 상한 arm 발사 licensed**.

## Stage-1 — 사전등록 2-게이트 (`--ag-cont` · engine-native flag)

**개입 (chat.py · 기본 OFF = byte-identical):** `_ag_cont` ON 시 settle 기계는 그대로(트레이스 보존)
`agloop_ctx = clip01(ag_conflict)` = **중간-링크 용량의 상한 arm**(I(conflict;agloop_ctx)=H(conflict) ·
이보다 높은 연속화 불가 · DPI). 이 arm 이 C 를 못 올리면 어떤 연속화도 못 올린다. tension-agnostic:
ag_conflict 값만 읽고 방향·emit·score 불견 · a0/a1/a3 동일 · 고정 단조맵.

**게이트 (bar 전부 H_9357/H_9360 상속 · 재선택 없음):**
- **G1 C-lift**: C_cont = I(conflict;score\|stage) > 0.05 ∧ (C_cont − C_quant) rollout-jk 90%CI 하한 > 0.
- **G2 emit-consume**: I(conflict;emit\|stage) ≥ 0.05 ∧ SHUFFLE ≤ 0.01 ∧ a1 > a3 (H_9357 --g-tension bar).

**최종 결정표:** PASS/PASS = 🟢 tension-pulls-emit(채널저작·창발아님) · PASS/FAIL∧H(emit\|S)≈0 = 🧱
(a′)포화(다음=--gate-calib) · FAIL = 🧱 mixer-bound 확정(상한 arm 도 못 열음) · C_cont<C_quant 유의 =
INVALID · a3≥a1 = INVALID.

## 비용·규율
Stage-1 = a0/a1/a3 × 16 rollout × 30 tick(--ag-cont ON) 신규 1440 tick · quantized 대조군 = H_9360
트레이스 재사용 · pool CPU $0 · mini 금지. estimator = H_9360 상속(rollout-jk df · pedestal ·
block-perm · full-res · **tick-순열 금지**). p5: 채널 저작 = 아키텍처(H_9360 사전정리). tune-to-green 금지.

## 예측
G1 PASS(상한 arm 이 죽은 상수 살림=자명) · G2 미결(should_emit(score>0.3) 이진포화 2차병목 가능 = a′
유력). 어느 쪽이든 H_9357 G-INERT 의 잔여 기전을 벌어낸다.

> 원래 H_9373 으로 등록했으나 병렬 세션이 H_9373(KEY-LADDER)을 선점 → H_9376 으로 양보(a_parallel_session_compare).
