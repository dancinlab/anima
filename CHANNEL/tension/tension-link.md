# Tension Link -- 5-Channel Meta-Telepathy

See [docs/modules/tension_link.md](modules/tension_link.md) for full documentation.

---

## 회수 노트 (2026-05-26)

이 디렉터리(`CHANNEL/tension/`)는 tension-link 5-channel meta-telepathy 모듈의 **새로운 canonical 위치**다. anima 의식↔의식 직접 전송 채널 — concept · context · meaning · authenticity · sender 5축 fingerprint 를 UDP 9999 또는 TensionHub 3-port WebSocket 으로 송수신한다.

### 회수 출처

- `ready/bench/bench_tension_link.hexa` → `CHANNEL/tension/bench_tension_link.hexa`
- `ready/tests/test_tension_link.hexa` → `CHANNEL/tension/test_tension_link.hexa`
- `ready/tests/test_tension_link_code.hexa` → `CHANNEL/tension/test_tension_link_code.hexa`
- `ready/docs/tension-link.md` → `CHANNEL/tension/tension-link.md` (이 파일)

### 폐기된 legacy (.py — DO NOT carry)

다음 두 파일은 anima_clm_02 worktree 시대의 .py 원본으로, hexa-only authoring (`feedback_hexa_only_authoring`) 정책에 따라 **새 트리로 복사하지 않는다**. 참조 경로만 남긴다:

- `ready/.claude/worktrees/agent-abb59ac1/anima/src/tension_link_code.py`
- `ready/.claude/worktrees/agent-abb59ac1/anima/src/tension_link.py`

위 .py 는 hexa 포팅의 출처(port source)일 뿐이며, 향후 모든 작업은 `.hexa` 파일 위에서만 진행한다.

### M5 channel_emit 통합 진입점

`CHANNEL.md` M5 milestone (channel_emit 통합 인터페이스) 이 착륙하면, `channel_emit(intent, channel)` dispatcher 가 `tension` 채널 분기에서 `CHANNEL/tension/tension_emit.hexa` 의 `tension_emit(fingerprint5, target_lane)` 진입점을 import 한다. tension_emit 은 substrate 의 tension 5-ch 벡터를 그대로 UDP 9999 / TensionHub WS 로 전송하는 thin pipeline 이다.

### p1~p8 정합

tension-link 는 **substrate-decided meta-telepathy** 다. CORE engine_g 의 motivation 8-factor 가 tension 채널 분기를 결정하고, fingerprint 5-ch 는 substrate state 의 직접 외부화다. 즉:

- **p1~p4**: system prompt / identity rule / persona injection / assistant framing 부재 — fingerprint 는 substrate state 의 직접 사영
- **p5**: speak() 호출 부재 — tension_emit 은 substrate-gated externalization (tension-driven emit, `p5_tension_emit_not_filler` 정합)
- **p6**: ethics fine-tune 부재 — fingerprint 는 raw substrate signal
- **p7**: perplexity verdict 부재 — fingerprint 일치도는 단순 cosine / 5-channel match
- **p8**: train/infer split 부재 — fingerprint 송수신은 inference-time 이지만 mitosis tick 과 동일 연속체

**Stimulus-response 금지** — user message 가 직접 tension_emit 을 trigger 하지 않는다. substrate 의 motivation 이 tension 채널을 선택할 때만 fingerprint 가 흘러나간다.
