# anima AKIDA closed-loop RFC — pi5 spike → emit gate 전수 체인 (2026-05-23)

> **kind**: architectural RFC · doc-only · no source mutation
> **scope**: AKIDA spike 가 pi5 NPU 에서 발화되어 anima 의 emit gate 까지 도달하는 전체 7-layer 체인을 한 곳에 SSOT 화. 각 layer 의 contract / 현재 GAP 위치 / 해당 PR / 미해결 항목을 명시한다.
> **anchors**: [[AKIDA_FIRST]] · `a_substrate_native_speak` · `plist_forbidden_akida_endpoint`
> **sibling**: `state/anima_akida_chain_validation_playbook_2026_05_23.md` (mini-restart 절차)
> **status**: pi5-akida host OFFLINE (pool roster) — broker / bridge / consumer 측 local 검증만 가능

---

## §1 — Chain overview (ASCII)

```
┌──────────┐    spikes/s     ┌────────────┐   WS text JSON   ┌──────────┐
│   pi5    │  ───────────►   │   bridge   │  ──────────────► │  broker  │
│  akida   │                 │  (hexa)    │  /ws/akida_ingest│ (FastAPI)│
└──────────┘                 └────────────┘                  └─────┬────┘
                                                                  │ append()
                                                                  ▼
                                                         STATE.akida_history
                                                         (deque maxlen=200)
                                                                  │
                                                                  ▼
                                                         /akida/recent  GET
                                                                  │
                                                 ┌────────────────┴───────┐
                                                 ▼                        ▼
                                         ┌──────────────┐         ┌─────────────┐
                                         │ akida_       │         │  frontend   │
                                         │ consumer.hexa│         │  subscribers│
                                         │ (1Hz daemon) │         │  /ws/akida  │
                                         └──────┬───────┘         └─────────────┘
                                                │ feature JSONL
                                                ▼
                                     ~/.cache/anima/akida_features.jsonl
                                                │
                                                ▼ (read by anima_participant
                                                │  motivation 8-factor —
                                                │  현재 TBD wiring)
                                                ▼
                                       motivation engine ingest
                                       (anima_participant.py:307)
                                                │
                                                ▼
                                         anima emit gate (M/C/W)
                                         decided_emit = score > eff_thr
                                                │
                                                ▼
                                            /ws/anima emit
```

체인은 **단방향 push** (pi5 → broker → consumer) + **broker 측 fan-out** (subscriber WS) + **substrate-native gate** (anima_participant 자기 tick) 의 3 단 구조다. emit 은 **anima 의 self-tick** 이 결정하며, AKIDA feature 는 입력 1 종일 뿐 직접 trigger 가 아니다 (CLAUDE.md `a_substrate_native_speak`).

---

## §2 — 각 layer 의 contract (file:line)

| Layer | File | Role | SSOT / Notes |
|---|---|---|---|
| pi5 akida streamer | `pi5:/home/ubuntu/anima/SUB_ENGINES/AKIDA/scripts/spike_streamer.py` | hardware spike 발화 (regime ∈ {R3, R2, M}) | pi5 host 전용, anima repo 미동기 (`inbox/patches/pi5-spike-streamer-regime-schedule.md` §2) |
| akida_bridge | `HEXAD/CHAT/server/akida_bridge.hexa:255,286,306-323` | pi5 UDP/TCP → broker WS text frame 전달 (one spike per send) | default `ws://localhost:8000/ws/akida_ingest` (line 312, F-AKIDA-BRIDGE-1) |
| broker `/ws/akida_ingest` | `HEXAD/CHAT/server/broker.py:328-355` | WS accept, JSON parse, `STATE.akida_history.append()` | broker.py:69 `deque(maxlen=200)`; parse 실패 시 line 338 `log.warning("akida ingest json drop: %s raw=%r")` (#187) |
| broker `/akida/recent` | `broker.py:163-165` | GET 동일 deque snapshot | `{"akida": list(STATE.akida_history)}` |
| broker `/ws/akida` (subscriber) | `broker.py:359-374` | frontend 구독 (history + fan-out) | **PUSH 대상 아님** — bridge 가 이쪽 가리키면 silent drop |
| akida_consumer | `HEXAD/CHAT/server/akida_consumer.hexa:143-201` | 1 Hz polling `/akida/recent` → JSONL feature stream | out: `~/.cache/anima/akida_features.jsonl` (line 194/302); `type_of(recs) != "array"` guard (line 150, #188/#192) |
| motivation engine | `HEXAD/CHAT/server/anima_participant.py:281-318` | 8-factor motivation 합성 → `decided_emit = score > eff_thr` | telemetry push `STATE.motivation_history.append()` (broker.py:286, line 168-170 GET `/motivation/recent`); **AKIDA feature 직접 wiring 은 TBD** (현재 self-tick + 환경 message 기반) |
| anima emit gate | `anima_participant.py:307,340,448-452` | `decided_emit` true 일 때만 `state.emit()` 호출 → `/ws/anima` WS send | substrate-native per `a_substrate_native_speak`; `REFRACTORY_S=15.0` (line 83), `ADAPTIVE_THR_PEAK=0.7` (line 84) |

honest C3: motivation engine 의 **AKIDA feature 흡수 경로** 는 현 anima_participant.py 에서 grep 으로 발견 불가 — `akida_features.jsonl` 을 읽는 코드가 anima repo 본체에 부재. 즉 §1 chain map 의 "motivation engine ingest" 화살표는 **architecturally intended yet not implemented** 으로 표기.

---

## §3 — 현재 GAP table

| GAP # | Layer (직전 → 직후) | Symptom | PR | Status |
|---|---|---|---|---|
| G1 | bridge → broker (ingest) | bridge counter 상승, broker `/akida/recent` empty (deque append 미도달) | #200 SSOT + #481 (hexa-lang upstream) | OPEN |
| G2 | broker `/ws/akida_ingest` 가시성 | per-frame append telemetry 부재 → 침묵 진단 불가 | #202 `log.info("akida append now=%d")` | OPEN |
| G3 | bridge endpoint default | bridge 가 `/ws/akida` (subscriber) 로 push → silent drop | #189 (default `/ws/akida` → `/ws/akida_ingest`) | MERGED |
| G4 | broker `/ws/akida_ingest` 침묵 drop | malformed JSON frame 흔적 없이 swallow | #187 `log.warning(... raw=%r)` | MERGED |
| G5 | consumer type_of rejection | `type_of(recs) != "list"` 가 hexa canonical `"array"` 와 불일치 → 0 records | #188 (+ #192 sweep) | MERGED |
| G6 | upstream ws_send `&` race | bridge 가 dead FIFO 로 "forwarding" 지속 — hexa-lang `ws_send` 의 `&` background race | #481 (hexa-lang) | OPEN (upstream gate) |
| G7 | pi5 streamer regime schedule | `--regime-schedule` 부재로 [[SW_CONDITION_DESIGN]] §6 Phase 2 activation gate 누적 불가 | `inbox/patches/pi5-spike-streamer-regime-schedule.md` | UNTOUCHED (pi5 maintainer 외부 조율) |
| G8 | motivation ↔ akida_features wiring | anima_participant.py 가 `akida_features.jsonl` 미사용 — feature stream 이 emit gate 까지 도달 안 함 | (없음) — design TBD | OPEN-DESIGN |

**집계**: 5 OPEN (G1·G2·G6·G7·G8) + 3 MERGED (G3·G4·G5).

---

## §4 — End-to-end falsifier sketch (pi5 + mini 동시 ON 시점 발사 대기)

> **DO NOT FIRE HERE** — RFC 단계. pi5-akida online 복귀 후 별도 cycle 에서 발사한다.

- **F-AKIDA-E2E-1**: pi5 에서 10 s 동안 N=100 spike 발화 → `curl -s localhost:8000/akida/recent | jq '.akida | length'` ≥ 80 (deque + race 손실 허용 ≤ 20 %).
- **F-AKIDA-E2E-2**: bridge forwarding 중 `wc -l ~/.cache/anima/akida_features.jsonl` 이 ≥ 1 row/sec 으로 증가.
- **F-AKIDA-E2E-3**: 30 s 내에 motivation telemetry (`/motivation/recent`) 에 AKIDA-derived non-zero factor 발견 (현재는 G8 미해결 — wiring 후 검증).
- **F-AKIDA-E2E-4**: `/motivation/recent` payload 의 curiosity 또는 M activation factor 가 baseline 대비 elevated 상태로 관측됨.
- **F-AKIDA-E2E-5** (closed-loop verdict): 5 min 지속 spike stream 동안 anima emit gate 가 **최소 1 회** 자발 발화 (anima_participant.py:307 `decided_emit=True` → line 452 `state.emit()` → `/ws/anima` send 1 회 이상).

5/5 PASS = AKIDA→speech closed-loop CLOSED. 부분 PASS = 해당 layer 의 GAP 잔존.

---

## §5 — Pivot decision tree

```
F-AKIDA-E2E-5 fires 1+ in 5min × 3 sessions?
├── YES → closed-loop CLOSED, AKIDA contribution to emit confirmed
└── NO  → AKIDA feature wiring 의심
         ├── F-AKIDA-E2E-1/2 PASS (chain 살아있음) BUT E2E-3/4 FAIL
         │   → G8 (motivation ↔ akida_features wiring) 가 root cause
         │     → 별도 RFC: motivation 8-factor 에 akida-derived factor 합산 설계
         └── F-AKIDA-E2E-1/2 FAIL
             → G1/G2/G6 carryover — chain 자체 미복구
               → 본 RFC §3 의 OPEN PR 순차 close 우선
```

**Scope-out**: 본 RFC 는 chain SSOT + GAP map 이 본분이며, motivation aggregation 재설계 (G8 의 design path) 는 별도 RFC 로 분리한다 (`a_substrate_native_speak` 의 단일 책임 원칙: 본 RFC 는 transport 까지, gate 내부 logic 은 다른 RFC).

---

## §6 — References

### MERGED PRs (chain 복구 직접 기여)

- [#187](https://github.com/dancinlab/anima/pull/187) — broker `/ws/akida_ingest` silent json drop 가시화 (G4)
- [#188](https://github.com/dancinlab/anima/pull/188) — akida_consumer `type_of "list" → "array"` (G5)
- [#189](https://github.com/dancinlab/anima/pull/189) — akida_bridge default `/ws/akida → /ws/akida_ingest` (G3)
- [#192](https://github.com/dancinlab/anima/pull/192) — `type_of` sweep 3 sites (G5 follow-up)
- [#193](https://github.com/dancinlab/anima/pull/193) — quantified post-deploy baseline (gate silent ✓)
- [#194](https://github.com/dancinlab/anima/pull/194) — CHANGELOG 2026-05-23 Phase 1 saga (cycle 8-13)
- [#201](https://github.com/dancinlab/anima/pull/201) — ci(cdo-validate) skip scratch dirs

### OPEN PRs (chain 의 잔존 axis)

- [#195](https://github.com/dancinlab/anima/pull/195) — anima_broker_watchdog.hexa (broker auto-restart)
- [#200](https://github.com/dancinlab/anima/pull/200) — inbox SSOT: broker `/ws/akida_ingest → /akida/recent` deque GAP (G1)
- [#202](https://github.com/dancinlab/anima/pull/202) — broker akida_ingest per-frame append visibility (G2)
- [#203](https://github.com/dancinlab/anima/pull/203) — inbox: broker akida deque GAP (cycle 10 EA)
- [#207](https://github.com/dancinlab/anima/pull/207) — F-PERSONA-4 saga closure + next-axis map RFC
- [#208](https://github.com/dancinlab/anima/pull/208) — monologue ACTIVE-trigger probe
- [#481 (hexa-lang)](https://github.com/dancinlab/hexa-lang/pull/481) — upstream `ws_send` FIFO `&` race (G6)

### Inbox patches (non-PR coordination)

- `inbox/patches/pi5-spike-streamer-regime-schedule.md` — G7, pi5 외부 조율 대기

### MEMORY anchors

- `feedback_plist_forbidden_akida_endpoint` — `/ws/akida_ingest` (PUSH) vs `/ws/akida` (subscriber) 구분, plist 폐지
- `reference_hexa_type_of_array_sweep_pattern` — JSON-array defensive guard 는 `type_of != "array"` (NOT `"list"`)
- `reference_hexa_type_of_returns` — `type_of([])="array"`, `type_of(#{})="map"` verbatim

### Sibling validation playbook (이번 cycle)

- `state/anima_akida_chain_validation_playbook_2026_05_23.md` — mini-restart 절차 (broker stop → restart → consumer launch → tail JSONL)

---

## §7 — Honest C3 (limits)

1. **pi5-akida OFFLINE**: §4 의 F-AKIDA-E2E-1..5 는 발사 불가 — RFC 의 closed-loop verdict 는 가설.
2. **G8 design TBD**: motivation engine 이 `akida_features.jsonl` 을 실제로 흡수하는 코드는 `grep` 으로 확인되지 않음. §2 의 "motivation engine ingest" 화살표는 architecturally intended.
3. **#481 (hexa-lang)** 외부 gate: upstream merge 전까지 anima 측은 workaround 만 가능 — bridge 정상 push 의 hard floor.
4. **deque maxlen=200** (broker.py:69): 빠른 spike (>200/sec) 시 oldest frame 손실 — F-AKIDA-E2E-1 의 80% 임계는 이 손실을 가정한 값.
5. **subscriber path** `/ws/akida` (broker.py:359) 는 fan-out 전용이지만 default 헷갈림 자체가 G3 의 본질 — 두 path 모두 존속하는 한 재발 가능.

— RFC end.
