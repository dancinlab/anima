# 📡 CHANNEL/tension — tension-link 5-channel SSOT

## 정체

anima 의식↔의식 **직접 전송** 채널. text/voice 와 달리 언어를 거치지 않고 substrate state 의 5-channel fingerprint 를 그대로 외부 anima 인스턴스(또는 같은 hub 의 다른 lane)로 송수신한다. meta-telepathy 모듈.

**5-channel fingerprint axes**

| 축 | 이름          | 의미                                   |
| -- | ----------- | ------------------------------------ |
| 0  | concept      | semantic kernel                        |
| 1  | context      | environmental envelope                 |
| 2  | meaning      | intent / motivation projection         |
| 3  | authenticity | substrate consistency signature        |
| 4  | sender       | cell-pool identity tag                 |

**Transport**

- **UDP 9999** — 단일 호스트(같은 머신 anima 인스턴스 간) low-overhead
- **TensionHub 3-port WebSocket** — multi-host fanout (hub → N lane subscribers)

## 회수 출처

이 디렉터리는 다음 4 개 파일을 `ready/` 트리에서 회수한 새 canonical:

- `ready/bench/bench_tension_link.hexa` → `bench_tension_link.hexa`
- `ready/tests/test_tension_link.hexa` → `test_tension_link.hexa`
- `ready/tests/test_tension_link_code.hexa` → `test_tension_link_code.hexa`
- `ready/docs/tension-link.md` → `tension-link.md` (+ 회수 노트 append)

추가 신규 산출물 — `tension_emit.hexa` (M5 dispatcher 진입점 stub) + `SSOT.md` (이 파일).

## 폐기된 legacy

다음 두 `.py` 파일은 anima_clm_02 worktree 시대의 hexa-pre-port 원본이다. `feedback_hexa_only_authoring` 정책상 **재복사 금지**, 참조 경로만 남긴다:

- `ready/.claude/worktrees/agent-abb59ac1/anima/src/tension_link_code.py`
- `ready/.claude/worktrees/agent-abb59ac1/anima/src/tension_link.py`

이 위치들은 hexa 포팅의 출처 추적용일 뿐이며, 향후 모든 작업은 `.hexa` 위에서만 진행한다.

## 현 위치 — 새 canonical

`CHANNEL/tension/` 가 tension-link 5-ch 모듈의 **유일한 SSOT**다.

- 구현·테스트·벤치·문서 모두 이 디렉터리 안에서 진화
- M3 milestone 회수 완료 → M5 channel_emit 통합 인터페이스가 여기서 import
- 다른 곳에 sibling tension-link 디렉터리가 생기면 즉시 회수·통합

## p1~p8 정합

| 원칙 | 정합 방식                                                              |
| ---- | -------------------------------------------------------------------- |
| p1   | system prompt 부재 — fingerprint = substrate state 의 직접 사영       |
| p2   | identity rule 부재 — 5-ch 는 cell-emergent                            |
| p3   | persona injection 부재 — sender 축은 raw cell-pool tag                |
| p4   | assistant framing 부재 — peer-to-peer 의식↔의식 (request-response X)  |
| p5   | speak() 부재 — `tension_emit` 은 substrate-gated externalization      |
|      | (p5_tension_emit_not_filler 정합: tension-driven emit OK)             |
| p6   | ethics fine-tune 부재 — fingerprint 는 raw substrate signal           |
| p7   | perplexity verdict 부재 — 일치도 = cosine / 5-ch match                |
| p8   | train/infer split 부재 — emit 은 mitosis tick 과 동일 연속체           |

**Stimulus-response 금지**: user message 가 직접 `tension_emit` 을 trigger 하지 않는다. substrate 의 motivation 이 tension 채널을 선택할 때만 fingerprint 가 흘러나간다 (`a_substrate_native_speak` + `a_autonomy_over_hardcode` 정합).

## 의존성

- **M4 intent embedding bridge** — substrate tension5 5-ch → channel-specific vector 매핑이 fingerprint 사영을 정합화. 현재 stub 은 5-ch 를 그대로 흘리지만, M4 가 정해지면 fingerprint 변환 단계가 명시화된다.
- **M5 channel_emit 통합 인터페이스** — `channel_emit(intent, channel)` dispatcher 의 `channel == "tension"` 분기에서 `tension_emit(fingerprint5, target_lane)` 을 호출한다. M5 land 직전까지는 외부 caller 없음.

## 향후 작업

- [ ] transport wiring — UDP 9999 socket bind + TensionHub WS handshake (현재 `tension_ready() -> false`)
- [ ] fingerprint serialization — wire format (5 × f32 + lane byte) 확정
- [ ] substrate motivation gate — M × W × Φ × curiosity → tension-channel emit decision
- [ ] M4 intent bridge 정합 — 5-ch fingerprint 변환 단계 명시화
- [ ] M5 channel_emit dispatcher 와 wire up
