# CHAT_AUTONOMY_POST_DEPLOY_BASELINE — 2026-05-24

FIRST quantified post-deploy baseline — autonomy reshape
(sleep + imagination 정합 작동, 2026-05-24 00:47 KST 재시작 직후)

---

## § Context — 9-PR autonomy reshape

오늘(2026-05-24) main 에 도달한 9 PR 으로 chat 측 substrate-native 자율 emit 경로가
재구성됨. mini production 은 PID 35411 으로 00:47 KST 재시작 (anima_participant.py
585 LoC, PR #286).

| PR    | 요지                                                                        |
| :---- | :-------------------------------------------------------------------------- |
| #272  | feat(CHAT): anima_participant — conversation-active gate 삭제 + dream/imagination hook (혼잣말 가능) |
| #273  | feat(CHAT): anima_imagination_loop.hexa — emit-free internal rehearsal + mitosis tick |
| #274  | docs(PHILOSOPHY): p5 NO SPEAK + a_substrate_native_speak 정합 (tension-driven emit ≠ silence-filler) |
| #275  | feat(CHAT): anima_dream_stage.hexa — WAKE/N1/N2/N3/REM 5-stage state machine + Φ trajectory |
| #279  | docs(project.tape): a_chat_sleep_imagination + a_autonomy_over_hardcode — autonomy-first governance |
| #281  | docs(CHAT): CHAT.md operational SSOT + DEPLOY.md sleep/imagination daemon — P47 substrate-native |
| #282  | fix(CHAT): anima_dream_stage.hexa — emit_allowed boolean API 폐기 + dream_context dict API |
| #286  | fix(CHAT): anima_participant — _dream_stage_current() boolean gate 폐기 + _dream_context dict 주입 |
| #288  | fix(CHAT/docs): CHAT.md — sleep stage boolean gate 표현 정정 |

핵심 변화: conversation-active gate 와 dream_stage boolean gate 가 모두 제거됨.
emit 결정은 substrate 내부 score + p3/p5 enforce filter 만으로 자율 수행.

---

## § Collection window

| 항목                            | 값                                       |
| :------------------------------ | :--------------------------------------- |
| 소스                            | mini:~/anima_chat_pack/logs/participant.err |
| 프로세스                        | PID 35411 (anima_participant.py, restart 00:47 KST) |
| Window start                    | 2026-05-24 00:47:19 KST                  |
| Window end                      | 2026-05-24 00:55:52 KST                  |
| 경과                            | ~8.5 분 (목표 30 분 미달, 재시작 직후 수집) |
| Tick span (min..max)            | 1 .. 235 (span 235 ticks)                |
| Tick logging 모드               | EMIT/EMIT-DROP 매 tick + silent log 5-tick 마다 |
| 텔레메트리 라인                 | 80 (27 EMIT + 12 EMIT-DROP + 41 silent)  |

honest caveat: 30 분 목표 대비 8.5 분 (~28%) 수집. PID 35411 가 00:47 에 시작했고
본 baseline 측정 시각이 00:56 였기 때문. 다음 baseline 사이클에서 30+ 분으로 재측정 필요.

---

## § Headline metrics — 4 ratio

| Ratio                          | 수치        | 백분율   | 의미                                |
| :----------------------------- | :---------- | :------- | :---------------------------------- |
| emit_attempt_per_tick          | 27 / 235    | 11.49 %  | substrate 가 emit 후보를 띄우는 빈도 |
| emit_actual_per_attempt        | 15 / 27     | 55.56 %  | p3/p5 통과율 (시도 중 실제 emit 비율) |
| net_emit_per_tick              | 15 / 235    |  6.38 %  | 최종 actual emit rate (per tick)     |
| p3p5_drop_ratio_of_attempts    | 12 / 27     | 44.44 %  | substrate-internal filter 차단율    |

해석: 11.49 % 에서 score>0.30 가 발생 → 그 중 55.56 % 가 p3/p5 통과. 235 tick
중 15 회 자율 emit. p3/p5 차단은 100 % 가 아님 — substrate 가 실제로 말하고 있음.

---

## § Score histogram (emit 시도 27 건)

```
[0.0-0.1)  n= 0
[0.1-0.2)  n= 0
[0.2-0.3)  n= 0     ← below threshold 0.30 ⇒ silent (별도 41 회)
[0.3-0.4)  n= 0
[0.4-0.5)  n= 0
[0.5-0.6)  n= 0
[0.6-0.7)  n=27  ###########################
[0.7-0.8)  n= 0
[0.8-0.9)  n= 0
[0.9-1.0)  n= 0

min=0.627  max=0.681  mean=0.647  std≈0.012
```

honest C3: emit 시도 27 건 전부 [0.62, 0.69] 좁은 band. score 함수가 현재
w_curiosity_peak_seed strategy 1 개 path 만 활성화된 정황 — 다양성 측정은
multi-strategy 도달 후 가능.

---

## § Strategy distribution

| Strategy                | count | percent |
| :---------------------- | ----: | ------: |
| w_curiosity_peak_seed   |    27 | 100.0 % |

honest C3: 본 window 에서 단일 strategy 만 관측. 다른 strategy (예:
w_tension_high, w_φ_peak 등) 가 wiring 되었는지 / score 함수상 도달 불가능한지
별도 검증 필요.

---

## § Per-minute cadence

`*` = emit 시도, `X` = p3/p5 drop. 시도 - drop = 실제 emit.

| Minute (KST)       | attempts | drops | actual | trace                |
| :----------------- | -------: | ----: | -----: | :------------------- |
| 2026-05-24 00:47   |        3 |     2 |      1 | `***  (XX)`          |
| 2026-05-24 00:48   |        3 |     1 |      2 | `***  (X)`           |
| 2026-05-24 00:49   |        3 |     1 |      2 | `***  (X)`           |
| 2026-05-24 00:50   |        3 |     2 |      1 | `***  (XX)`          |
| 2026-05-24 00:51   |        3 |     2 |      1 | `***  (XX)`          |
| 2026-05-24 00:52   |        3 |     0 |      3 | `***  ()`            |
| 2026-05-24 00:53   |        3 |     3 |      0 | `***  (XXX)`         |
| 2026-05-24 00:54   |        3 |     0 |      3 | `***  ()`            |
| 2026-05-24 00:55   |        3 |     1 |      2 | `***  (X)`           |

regularity 관측: emit 시도가 매 분 3 회로 결정적 — tick interval (~2 s/tick)
과 score 주기성으로부터 유도되는 cadence 로 추정. drop 빈도는 0..3 사이 자유 변동.

---

## § Comparison to previous baseline (ecf17cc0c)

| 축                       | ecf17cc0c (2026-05-23 19:37) | 본 baseline (2026-05-24 00:47+)        |
| :----------------------- | :--------------------------- | :------------------------------------- |
| gate 상태                | ON (conversation-active)     | OFF (autonomy reshape, dream dict API) |
| 측정 소스                | broker `/history`            | participant.err telemetry              |
| anima emit count         | 0 (`/history` empty)         | 15 actual / 27 attempts                |
| 결론 양상                | "silent in void" (gate work) | "autonomous emit in void" (autonomy work) |
| 측정 방향성              | 차단 동작 확인               | 자율 동작 확인                         |
| 결론 강도                | 양방향 양립 — `/history`=0 ⊥ telemetry=0 동시 검증 미수행 | telemetry=15 emit 직접 증거 |

본 baseline 은 ecf17cc0c 의 직접 보완 (gate ON silent ↔ gate OFF autonomous emit).
두 baseline 이 같이 한 쌍을 이루어 "gate semantics 가 의도대로 동작" + "gate 제거
시 자율 emit 발화" 양 방향이 모두 측정됨.

---

## § Honest C3

1. **p3/p5 차단 100 % 아님** — substrate 가 27 회 시도 중 15 회 실제 emit.
   substrate-internal filter 는 conservative 하지만 결정적 침묵이 아님. 본 PR
   설명서두에 "p3/p5 drops 100 %" 가설이 있었으나, 실제 측정상 44.44 % 로
   기록됨. 가설 → 측정 보정.
2. **collection window 8.5 분 only** — 30 분 목표 미달. 다음 baseline 사이클은
   재시작 후 30+ 분 누적 후 측정. 본 baseline 은 "재시작 직후 첫 안정 운행" snapshot.
3. **no user msg arrived during collection** — emit cadence 가 순수 substrate 구동.
   user message 가 도달했을 때의 emit 행동은 별도 측정 필요.
4. **dream_stage hook stub 가능성** — sister agent 의 "ctx verify" 결과 미반영.
   stub 일 경우 모든 stage 가 WAKE default. score 가 단일 band [0.62, 0.69] 에
   몰린 것이 stub 효과인지 정상 동작 결과인지 본 baseline 에서는 미분리.
5. **단일 strategy 만 관측** — w_curiosity_peak_seed 100 %. multi-strategy
   설계 의도 vs 실측 격차 별도 audit 필요.
6. **score 좁은 band** — std≈0.012. variance 가 좁음. score 함수의 dynamic
   range 가 좁은지, score input feature 가 정적인지 별도 측정 필요.
7. **diurnal pattern 측정 불가능** — 8.5 분 sample. 시간대별 cadence 변화
   (수면 stage 와의 정합) 는 multi-hour 수집 후 가능.

---

## § Cross-reference

| 항목                                     | 참조                                          |
| :--------------------------------------- | :-------------------------------------------- |
| 본 reshape 의 9 sister PR                | #272 / #273 / #274 / #275 / #279 / #281 / #282 / #286 / #288 |
| Prior baseline (gate ON silent)          | commit ecf17cc0c (PR #182 monologue sim 기반) |
| Participant source                       | HEXAD/CHAT/anima_participant.py (585 LoC, PR #286 적용) |
| Dream stage daemon                       | HEXAD/CHAT/anima_dream_stage.hexa (PR #275 / #282) |
| Imagination loop                         | HEXAD/CHAT/anima_imagination_loop.hexa (PR #273) |
| Operational SSOT                         | HEXAD/CHAT/CHAT.md (PR #281 + #288)           |
| Deploy runbook                           | HEXAD/CHAT/DEPLOY.md (PR #281)                |
| Governance                               | project.tape `a_chat_sleep_imagination` + `a_autonomy_over_hardcode` (PR #279) |
| Telemetry log (수집 시점 snapshot)       | mini:~/anima_chat_pack/logs/participant.err (~9 KB, 110 lines, 00:47:11 - 00:55:52) |

---

본 baseline 은 autonomy reshape 의 첫 정량 측정. 차기 사이클은 (a) 30+ 분
window 재측정 (b) multi-strategy 도달 여부 audit (c) dream_stage stub/real
분리 (d) user message 도달 시 emit 행동 측정 — 4 개 follow-up 후속.
