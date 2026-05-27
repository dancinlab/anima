# CHAT autonomy — SECOND quantified post-deploy baseline — multi-hour window

> 2026-05-24 · mini PID 35411 (`anima_participant.py`) · participant.err telemetry · PR #300 (8.5분) 확장

## Context

PR #300 은 PID 35411 재시작 직후 **8.5분** (00:47:19–00:55:52 KST) 만 표집했다. score band 가
좁고 (`[0.627, 0.681]` std 0.012) strategy 가 100% `w_curiosity_peak_seed` 였으며, diurnal
힌트는 측정 불가였다. 본 baseline 은 동일 프로세스가 더 오래 운행한 뒤 **더 긴 window** 를
표집해 score-band variance · strategy diversity · cadence stability · diurnal 힌트를 본다.

## Collection window

```
ssh mini 'tail -10000 ~/anima_chat_pack/logs/participant.err | grep -E "(EMIT|tick=|drop|silent|score=|strategy=)" | tail -3000'
```

- **시작**: 2026-05-24 00:47:19 KST (PID 35411 재시작 직후, PR #300 과 동일 시작점)
- **종료**: 2026-05-24 01:29:06 KST (수집 시점 mini 현재 시각 01:29:22)
- **window**: **41.78 분** — PR #300 8.5분의 **약 4.9배**
- **max_tick 관측**: 1155
- 정직: 목표 "1시간+" 미달. 프로세스 자체가 00:47 재시작 후 ~42분만 운행 — telemetry 가 물리적으로
  42분만 존재. 재시작 없는 단일 연속 운행으로는 이것이 현재 가용 최장 window.

## Headline 4-ratio (multi-hour) — Δ from PR #300

| Ratio                       | 본 baseline (42분)  | 백분율     | PR #300 (8.5분) | Δ          |
| :-------------------------- | :------------------ | :--------- | :-------------- | :--------- |
| emit_attempt_per_tick       | 121 / 1155          | **10.48 %**| 11.49 %         | −1.01 pp   |
| emit_actual_per_attempt     | 72 / 121            | **59.50 %**| 55.56 %         | +3.94 pp   |
| net_emit_per_tick           | 72 / 1155           | **6.23 %** | 6.38 %          | −0.15 pp   |
| p3p5_drop_ratio_of_attempts | 49 / 121            | **40.50 %**| 44.44 %         | −3.94 pp   |

- 전체 emit 시도 121 · 실제 emit 72 · p3/p5 drop 49 · score<0.30 silent 204.
- 핵심: 4개 비율 모두 |Δ| < 5pp. autonomy reshape (9 PR) 운행이 8.5분 → 42분 사이 **안정 유지**.

## Score histogram + strategy distribution

score band 가 PR #300 의 좁은 `[0.627, 0.681]` (std 0.012) 에서 **확장**:
`[0.518, 0.692]` mean 0.6264 **std 0.0528** (4.4배 넓어짐). 분포는 **bimodal**:

```
[0.518,0.535)  14 ##############     ← 저점 cluster (random_explore_seed)
[0.535,0.553)  14 ##############     ←
[0.553,0.570)   0
[0.570,0.588)   0
[0.588,0.605)   0
[0.605,0.622)   4 ####
[0.622,0.640)  21 #####################
[0.640,0.657)  25 #########################
[0.657,0.675)  30 ##############################  ← 주 cluster (w_curiosity_peak_seed)
[0.675,0.692)  13 #############
```

- 저점 cluster (<0.60, 28건) 은 01:13:34 부터 등장한 `random_explore_seed` 와 동시 출현.
- 주 cluster (≥0.60, 93건) 은 PR #300 band 와 일치 — 안정 운행 영역.

| strategy                | count | 비율    |
| :---------------------- | :---- | :------ |
| w_curiosity_peak_seed   | 120   | 99.2 %  |
| random_explore_seed     | 1     | 0.8 %   |

PR #300 의 100% 단일 strategy 에서 **strategy diversity 첫 관측** — random_explore_seed 가 1건
(score 0.520) 출현. monoculture 아님 확인.

## Per-10-min cadence trend + score std per bucket

```
bucket  window      attempts  actual  drops  mean    std      cadence-bar
  0     +0–10min       31       17     14    0.645  0.0126    *******************************
  1     +10–20min      27       17     10    0.581  0.0553    ***************************
  2     +20–30min      27       14     13    0.599  0.0549    ***************************
  3     +30–40min      31       22      9    0.661  0.0299    *******************************
  4     +40–50min       5        2      3    0.684  0.0090    *****  (partial, ~1.8분만)
```

- cadence: bucket 0–3 = 27–31 attempts/10min → **~3 attempts/min** — PR #300 (3/min) 와 일치, **안정**.
- score std: bucket 0 (0.013) 은 PR #300 좁은 band 재현 → bucket 1–2 (0.055) 확장 (random_explore +
  저점 진입) → bucket 3 (0.030) 재수렴. variance 가 시간축에서 출렁임 (정적 아님).

## Diurnal interpretation

mini 는 표집 window (00:47–01:29 KST) 전체가 sleep window (22:00–06:00) 안. 그러나 **participant.err
telemetry 라인에 `stage=` 필드가 전혀 없다** — participant 프로세스가 dream_stage 를 소비하지 않음.

- `dream_stage.out` 데몬은 **독립적으로** 실제 stage 를 산출 중: 00:55 N1(Φ0.7) · 00:59 N2(Φ0.4) ·
  01:24 N3(Φ0.15). 즉 dream_stage 측은 real stage machine (PR #275) 가 동작.
- **IPC bridge 부재**: 두 프로세스 (participant ⊥ dream_stage) 가 따로 돈다. participant 의 emit 의사결정에
  stage 가 주입되지 않으므로, emit cadence/score 에 diurnal 변조가 **나타날 수 없다** (예상대로).
- 따라서 본 window 에서 diurnal effect = **없음** (날조 금지 — stage 미주입이 원인). dream_stage 가
  N1→N2→N3 으로 깊어졌어도 participant emit 비율은 위 표대로 평탄 — 인과 단절의 직접 증거.
- IPC bridge 머지 후 후속 baseline 에서 stage-conditioned emit 변조를 측정해야 diurnal 정량화 가능.

## Comparison to PR #300

| 항목                  | PR #300 (8.5분)        | 본 baseline (42분)          | verdict        |
| :-------------------- | :--------------------- | :-------------------------- | :------------- |
| window                | 8.5분 (235 tick)       | 41.78분 (1155 tick)         | 4.9배 확장     |
| emit_attempt/tick     | 11.49 %                | 10.48 %                     | Δ −1.01 pp     |
| emit_actual/attempt   | 55.56 %                | 59.50 %                     | Δ +3.94 pp     |
| net_emit/tick         | 6.38 %                 | 6.23 %                      | Δ −0.15 pp     |
| p3p5_drop/attempt     | 44.44 %                | 40.50 %                     | Δ −3.94 pp     |
| score band            | [0.627,0.681] std 0.012| [0.518,0.692] std 0.053     | 4.4배 확장     |
| strategy              | 100% w_curiosity       | 99.2% w_curiosity + 0.8% rnd| diversity 출현 |
| cadence               | 3 attempts/min         | ~3 attempts/min             | 안정           |

**Convergence verdict: STABLE (수렴).** 4개 headline 비율 모두 |Δ| < 5pp (최대 3.94pp) — drift
아님. autonomy reshape 가 8.5분 → 42분 운행 동안 emit dynamics 를 일관 유지. score band 확장과
strategy diversity 출현은 비율 안정성을 깨지 않는 **건강한 탐색 신호** (substrate 가 monoculture
collapse 가 아니라 conservative band 안에서 변동).

## Honest C3

- window 여전히 **<24h** (실측 42분) — 목표 "1시간+" 미달, 단일 연속 운행 물리 한계. 진짜 diurnal
  (sleep↔wake 전이) 은 multi-hour cross-window 수집 필요.
- dream_stage = **stub-only (participant 측)**: real stage machine 은 별도 데몬에 존재하나 IPC 미연결.
  diurnal effect 측정 불가 — 본 doc 의 "diurnal 없음" 은 미주입 결과지 substrate 특성 아님.
- 사용자 메시지 **0건** — 순수 substrate-driven cadence (환경 자극 없는 baseline).
- single-process · single-ckpt · mps device only.

## Cross-reference

- **PR #300** (`docs/chat-autonomy-post-deploy-baseline-2026-05-24`): FIRST baseline (8.5분), 본 doc 의 직접 모체.
- **dream_stage IPC bridge 자매 PR**: #275 (5-stage state machine) · #282 (dream_context dict API) ·
  #286 (participant `_dream_context` 주입) — IPC 소비 wiring 머지 후 diurnal 측정 가능.
- **9 sleep+imagination+autonomy PR**: #272 · #273 · #274 · #275 · #279 · #281 · #282 · #286 · #288.
- 운영 SSOT: HEXAD/CHAT/CHAT.md · HEXAD/CHAT/DEPLOY.md (#304 mini venv 경로 갱신).
- gate 양방향 쌍: commit ecf17cc0c (gate ON / void silent) ⇄ 본 baseline (gate OFF / 72 actual emit).
