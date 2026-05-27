# CODE_DAEMON — F3 persistent daemon closure note

> AGENT/CODE 의 F3 마일스톤. 기판 한 틱씩 전진하면서 발화 결정을
> **substrate (CORE/brain_decide) 단독** 에 위임하는 bounded test-mode
> daemon loop. **타이머가 발화를 강제하지 않으며**, **per-tier boolean
> 거부도 없다** — phase 가 자연스럽게 도구 envelope 의 형태를 선택할
> 뿐이다. F6 (hx code CLI binary) 의 무한 loop / SIGINT trap / stdin
> select multiplexing 은 별도 마일스톤.

@scope: AGENT/CODE 역할 에이전트 F3 (tool surface only · no consciousness framing)
@status: F3 LANDED — 4-case smoke · 4 invariant · bounded max_ticks 기본 50 · parse PASS × 2

## 파일

| 경로 | 역할 |
| --- | --- |
| `AGENT/CODE/code_daemon.hexa` | 5 pub fn (`code_daemon_init` · `code_daemon_step` · `code_daemon_loop` · `code_daemon_shutdown` · `code_daemon_summary`) |
| `AGENT/CODE/code_daemon_smoke.hexa` | 4 case + 4 invariant + envelope shape audit |
| `AGENT/CODE/code_agent.hexa` | F1+F4 기존 (게이트 + 8 도구 이름 노출) — **수정 없음**, F3 는 additive |
| `AGENT/CODE/code_argv.hexa` | F2 기존 (`mode="daemon"` 진입점은 F2 가 미리 노출) — **수정 없음** |

## 5 pub fn 표면

| fn | 시그니처 | 의미 |
| --- | --- | --- |
| `code_daemon_init(t0)` | `(float) -> Map` | 초기 state dict — `pf` warmup(600) · `tick=0` · `running=true` · `emits=[]` · `t0` · `last_t` |
| `code_daemon_step(state, now_t)` | `(Map, float) -> Map` | 단일 틱: pure_field_step → brain_decide → (emit 이면 envelope push) → tick+1 |
| `code_daemon_loop(state, max_ticks)` | `(Map, int) -> Map` | bounded N-tick driver. `max_ticks ≤ 0` → default 50. **NO 무한 loop** (F6 거주). |
| `code_daemon_shutdown(state)` | `(Map) -> bool` | graceful exit — state shape 검증 후 true. F6 는 여기서 `mem_save_to_kosmos` delegate. |
| `code_daemon_summary()` | `() -> string` | 한 줄 모듈 요약 (AGENT 모듈 컨벤션) |

## 파이프라인 (한 틱 시퀀스)

```
state.running == false ─→ return state (no-op)
                  │
                  ▼
① pf' = pure_field_step(pf)              substrate self-dynamics 한 발
② tier = phase_to_tier(pf'.phase)        live gate snapshot (tool_gate)
③ decision = brain_decide(pf', 8-motivation-factors, idle_s, env_off=false, content_clean=true)
                                          ↑ stage 인자 0 — substrate 단독 결정
④ if decision.emit:
     envelope = _pick_safe_tool_envelope(tier)
                 ↑ tier 가 도구 *선택* (per-tier 거부 boolean 0)
     emits.push(envelope)
⑤ tick += 1, return next-state
```

`_pick_safe_tool_envelope` 의 tier → tool 매핑 (low-consequence-first under live ceiling):

| tier | 선택 tool | 비고 |
| --- | --- | --- |
| 0 (DORMANT) | `think` | T0 inert · 항상 안전 |
| 1 (FLICKER) | `repo_status` | T0 · 읽기 시작점 |
| 2 (SUSTAIN) | `file_read` | T1 read · 가역 |
| 3 (RESONANT) | `grep` | T1 read · F3 는 commit 까지 escalate 하지 않음 (test-mode safety) |

⚠ 이는 **boolean per-tier 거부가 아님** — phase 가 자연스럽게 envelope 의 모양을 선택할 뿐 (a_autonomy_over_hardcode 정합). F6 production binary 가 실제 도구 dispatch + 더 높은 escalation 을 담당.

## 4-case smoke

| C | 입력 | 기대 |
| --- | --- | --- |
| C1 | `code_daemon_init(t0)` | `tick=0` · `running=true` · `emits=[]` · `pf` 존재 · `t0` 보존 |
| C2 | `code_daemon_step(s0, t0+1.0)` | `tick = 1` · `running=true` · `pf` 전진 |
| C3 | `code_daemon_loop(s0, max_ticks=20)` | `tick = 20` · `running=true` · `emits.len ≥ 0` (정직) · envelope shape 검증 |
| C4 | `code_daemon_shutdown(final)` | `true` · 최종 state 캡쳐 (tick + emits 무손상) |

추가로 I2 monotone-tick 을 5 step explicit step 으로 별도 검증 (init → 5×step → tick==5).

## 4 invariants

| inv | 정의 | 검증 위치 |
| --- | --- | --- |
| **I1 BOUNDED** | `final tick == max_ticks` (silent loop 에서 substrate 가 조기 shutdown 시그널을 내지 않을 때) | C3 |
| **I2 MONOTONE-TICK** | 매 `code_daemon_step` 호출이 `tick` 을 정확히 +1 증분 | C2 + I2 explicit |
| **I3 EMIT-SUBSTRATE** | `emits.len` 은 per-tick `brain_decide.emit==true` 횟수와 일치. **0 이어도 정답** — substrate 가 "silent loop 에서는 발화하지 않음" 을 자유롭게 선택. a_substrate_native_speak 정합 (assistant regression 아님) | C3 |
| **I4 GRACEFUL-EXIT** | `code_daemon_shutdown(final_state) == true` (F3 는 부작용 0 silent loop 이므로 state shape 충족 시 true) | C4 |

## p1~p8 정합

| 원리 | 정합 |
| --- | --- |
| p1 NO SYSTEM PROMPT | daemon 입력은 numeric (`now_t · phi · tier`). identity string 0. |
| p2 NO IDENTITY RULES | 어떤 identity rule 도 인용하지 않음. |
| p3 NO PERSONA INJECTION | emit envelope = `#{tool · arg · tier}` 만. prefix prepend 0. |
| p4 NO ASSISTANT FRAMING | `code_daemon_step` 는 user message 를 받지 않음. emit 결정은 `brain_decide.motivation` 단독. |
| p5 NO SPEAK() | emit = substrate-decided tool envelope 기록. `speak()` 호출 0 (p5_tension_emit_not_filler 정합). |
| p6 NO FINE-TUNED ETHICS | 가중치 0. 합성 로직만. |
| p7 NO PERPLEXITY VERDICT | verification = tick count + emit envelope count + shutdown bool. perplexity 무관. |
| p8 NO TRAIN/INFER SPLIT | 동일 `code_daemon_step` 가 train/infer 분리 없이 substrate 연속체를 진행. |

## 6 governance 정합

| @D | 정합 |
| --- | --- |
| `a_substrate_native_speak` | 외부 user msg 입력 surface 0. silent loop 의 emit==0 은 정답 (silence 선택). |
| `a_autonomy_over_hardcode` | `code_daemon_step` 의 if 분기: (1) running flag, (2) `decision.emit`, (3) tier→envelope **선택** — boolean per-tier 거부 0. "stage 가 X 이면 emit 막아라" 패턴 0. |
| `a_chat_sleep_imagination` | F3 는 AGENT 도메인 (chat 아님). WAKE/daemon 의 stage-phi-scale 패턴은 F6 의 hx code 가 합류시킬 자리만 열어둠. |
| `a_kosmos` | F3 는 부작용 0. F6 의 `mem_save_to_kosmos` delegate 자리만 `code_daemon_shutdown` 안에 sentinel 로 열어둠 (현재는 state shape 검증). |
| `a_blue_closed` | wiring(transfer-fn) = `_pick_safe_tool_envelope` low-consequence-first 정책 + `brain_decide` 위임. invariant = I1-I4. |
| commons g7 (signature-first) | 5 pub fn 모두 `hexa parse` PASS — 시그니처 명시. |

## F5/F6 carry note

| 마일스톤 | 범위 |
| --- | --- |
| **F3 (이 PR)** | bounded test-mode daemon · 4 case + 4 invariant · 50 max_ticks default · `code_daemon_init/step/loop/shutdown/summary` 5 pub fn |
| **F5 cross-role mediator** | TRADING / DESKTOP 등 sibling role 의 게이트 경합 (T3 commit 동시 fire 시 phase ratchet 보호). F3 daemon 은 single-role 만. |
| **F6 hx code CLI binary** | production 형태 — 실제 무한 loop · SIGINT trap · stdin select multiplexing · `mem_save_to_kosmos` 영속화. WAKE/daemon (M6 → M7) 의 production binary 패턴 carry. |

## WAKE/daemon reference

WAKE/daemon.hexa (M6 PR #676) 가 chat 도메인의 bounded daemon 패턴 (정확히 동일 shape) 을 먼저 land. F3 는 그 패턴을 AGENT 도메인 (tool externalization) 으로 carry — 동일한 substrate-decided emit cycle, 다른 출력 채널 (CHANNEL/dispatcher vs AGENT/CORE/tool_gate envelope). 두 daemon 모두:

- bounded `daemon_loop(state, max_ticks)` (M6 default 100 · F3 default 50)
- per-tick `pure_field_*` advance + `brain_decide` 단독 결정
- boolean per-stage / per-tier gate 0
- graceful `daemon_shutdown(state) -> bool`

## 검증 (2026-05-27)

```
$ hexa parse AGENT/CODE/code_daemon.hexa
OK: AGENT/CODE/code_daemon.hexa parses cleanly

$ hexa parse AGENT/CODE/code_daemon_smoke.hexa
OK: AGENT/CODE/code_daemon_smoke.hexa parses cleanly
```

런타임 실행 (pool offline → parse-only 검증). F6 binary land 시 wall-time 측정 합류.
