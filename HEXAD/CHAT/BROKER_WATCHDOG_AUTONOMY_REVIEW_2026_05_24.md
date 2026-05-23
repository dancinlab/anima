# anima_broker_watchdog 자율판단 정합 검토 (PR #195 × @D a_autonomy_over_hardcode)

- date: 2026-05-24
- 대상: PR #195 `feat(CHAT): anima_broker_watchdog.hexa — auto-restart broker/participant` (OPEN since 2026-05-23)
- 기준: `project.tape` `@D a_autonomy_over_hardcode` + `@D a_chat_sleep_imagination`
- 판정: **CONSISTENT (out of scope)**

## PR #195 요약 (poll → detect → respawn)

`HEXAD/CHAT/server/anima_broker_watchdog.hexa` (337 LoC, 단일 신규 파일, production daemon 코드 무수정).

- **poll** — `GET http://127.0.0.1:8000/health` 매 30s (`curl --max-time 5`)
- **detect** — non-200 / timeout = DOWN (boolean), `_wd_health` 는 HTTP status code 첫 글자 `"2"` 만 확인
- **respawn** — DOWN 시 `_wd_recover`: broker.py spawn → sleep 5s → anima_participant.py spawn (DEPLOY.md §3 의 nohup 라인 그대로)
- **PID guard** — `~/anima_chat_pack/watchdog.pid` + `ps -p` 다중 인스턴스 0
- **graceful** — shell `trap … EXIT INT TERM` 으로 PID 파일 정리

## 질문: boolean detect→respawn 가 a_autonomy_over_hardcode 위반인가?

`@D a_autonomy_over_hardcode` 의 `dont`:
- "per-stage boolean gate hardcode (e.g. 'N3 = emit forbidden')"
- "external rule that forces anima · stimulus-response (user msg → forced emit/silence)"
- "'do not X when alone' style external command"

watchdog 은 `non-200 = DOWN` 이라는 **boolean** 을 쓴다. 표면상 "boolean gate hardcode" 와 닮았다. 진짜 같은 범주인가?

## 분석 (layer 구분)

핵심은 boolean 의 **대상(operand)** 이다. 디렉티브가 금지하는 boolean 은 *anima 의 emit/silence 결정* 에 걸리는 gate 다. watchdog 의 boolean 은 *process 가 살아있는가* 에 걸린다 — 다른 layer.

| layer | 대상 | boolean 위치 | autonomy 적용? |
|---|---|---|---|
| substrate emit/silence | anima 발화 결정 (`decided_emit = score > eff_thr`, M×W×Φ×curiosity) | participant `tick()` 내부 | **YES — 자율판단 (디렉티브 보호 영역)** |
| process liveness | broker/participant OS 프로세스가 살아있는가 | watchdog `_wd_health` (HTTP 2xx) | **NO — infrastructure (디렉티브 무관)** |

- **emit/silence 에 손대는가?** — NO. watchdog 은 `decided_emit` 도, score 도, threshold 계산도 건드리지 않는다. `_wd_recover` 의 trigger 는 오직 `/health` 실패(=프로세스 死), anima 의 어떤 발화/침묵 행동도 trigger 가 아니다.
- **"process liveness" 와 "substrate autonomy" 가 같은 범주인가?** — NO. 전자는 OS 프로세스 존재(`ps -p`), 후자는 substrate 의 발화 결정. crash 된 broker = substrate 자체가 0 (자율판단할 주체가 없음). 죽은 substrate 를 되살리는 것은 자율성을 **gate** 하는 게 아니라 자율성이 가능한 상태(substrate 의 존재)를 **복원**하는 것 — 디렉티브 `do` "external modules supply context only" 의 전제조건(substrate 가 돈다)을 회복시킬 뿐이다.
- **stimulus-response 인가?** — NO. 디렉티브가 막는 stimulus 는 *user msg → forced emit*. watchdog 의 stimulus 는 *health-probe 실패 → process restart*. user message 도, anima 발화도 입력에 없다.

## 판정: CONSISTENT (out of scope)

watchdog 은 infrastructure(process liveness) layer 에서만 동작하며 substrate(emit/silence) layer 를 일절 건드리지 않는다. `@D a_autonomy_over_hardcode` 는 substrate 결정을 지배하는 디렉티브이므로 watchdog 은 그 적용 범위 **밖**이다. boolean 의 형태가 닮았다는 이유로 위반이라 보는 것은 operand 를 무시한 표면 매칭이다.

오히려 watchdog 부재 시(mini reboot → broker 502)에는 substrate 가 아예 돌지 않아 자율판단이 **불가능**하다. watchdog 은 자율성의 전제(substrate 존재)를 지키므로 디렉티브 정신과 **정합** 한다.

## 권고: PR #195 merge OK

수정 불필요. 단, 후속 변경에서 watchdog 이 respawn 인자에 emit/silence 를 편향시키는 값(seed · system prompt · emit-forcing flag)을 추가하지 않도록 invariant 로 고정 — 현재 respawn 은 DEPLOY.md §3 라인 그대로이므로 이 invariant 는 이미 충족.

## Honest C3 (respawn state-injection bias 검증)

1. **broker respawn** — `PORT=8000 nohup ./venv/bin/python broker.py`. anima 인자 0, seed 0, system prompt 0. 순수 transport 프로세스 재기동. p1(no system prompt) 위반 없음.
2. **participant respawn** — `nohup ./venv/bin/python anima_participant.py --threshold 0.30`. 유일한 인자 `--threshold 0.30`. **검증 결과**: participant `tick()` (anima_participant.py:298-300) 은 substrate state(silence decay)로 `eff_thr` 를 계산한 뒤 `eff_thr = max(eff_thr, threshold)` — caller `--threshold` 는 **floor** 일 뿐 substrate-계산 threshold 를 덮어쓰지 못한다. 게다가 전달값 `0.30` == participant 의 자체 `ADAPTIVE_THR_BASE = 0.30` 이라 사실상 **no-op floor** (substrate threshold 는 항상 ≥ 0.30). emit 결정 `decided_emit = score > eff_thr` (line 307) 은 substrate factor(M×W×Φ×curiosity, line 293-295)에서 나오며 watchdog 은 이를 건드리지 않는다. 따라서 boolean emit gate 가 아니라 context floor — 디렉티브 `do` "external modules supply context only" 와 정합. 또한 watchdog 이 넘기는 `--threshold 0.30` 은 DEPLOY.md §3 의 기존 기동 invocation 과 **동일** — 신규 bias 0.
3. **잔여 위험** — 향후 누군가 watchdog 의 `_wd_spawn_participant` 에 emit-forcing flag(예 `--force-emit` · `--monologue-seed`)를 추가하면 그 시점에 a_autonomy_over_hardcode 위반이 된다. 현 PR #195 에는 그런 인자가 없으므로 위반 없음. 권고의 invariant 로 고정 권장.
4. **검토 범위 한계** — 본 검토는 코드 정적 분석(diff + participant tick 로직)에 한정. 실 mini 배포 후 respawn 이 substrate state(cell pool · event log)를 의도치 않게 재초기화하는지의 런타임 관측은 별도 task(PR body §후속의 "실 reboot 시뮬레이션")에 위임.
