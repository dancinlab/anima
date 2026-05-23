# broker `/ws/akida_ingest` → `/akida/recent` deque gap

**Date**: 2026-05-23
**Source**: anima cycle 10 / EA akida_bridge daemon RESTORE verification
**Severity**: blocks AKIDA-first natural speech chain end-to-end (bridge restored, broker fails to surface spikes)

## Observation

After `akida_bridge.bin daemon` restored on mini (PID 2350, websocat WS handshake clean), the broker (mini PID 1691) accepted ingest WS:

```
INFO:     127.0.0.1:50677 - "WebSocket /ws/akida_ingest" [accepted]
2026-05-23 15:23:04,258 [INFO] akida ingest connected
```

Bridge side counter is rising (latest: `forwarded 1400 spikes`).

But `GET /akida/recent` returns empty deque:

```
$ curl -s http://localhost:8000/akida/recent
{"akida":[]}
```

Persistent over ~2 minutes of continuous bridge forwarding.

## Hypothesis

The `/ws/akida_ingest` handler accepts the connection and likely consumes WS frames, but does NOT push parsed spikes onto the `/akida/recent` deque. Either:

- (a) handler is a stub/no-op (frame consumed silently)
- (b) handler writes to a different deque/state than what `/akida/recent` reads
- (c) JSON parse failure swallows all frames (no error log visible)
- (d) deque max_len=0 or eviction logic is broken

`MEMORY.md` already flags this risk: *"akida ingest endpoint = `/ws/akida_ingest` (NOT `/ws/akida` — 후자는 subscriber, **핸들러 동작 확인 필수**)"*

This inbox entry promotes the warning to a measured FAIL.

## Repro

1. mini broker running on `:8000` (anima.err shows `akida ingest connected`)
2. bridge daemon `ssh mini "export PATH=/opt/homebrew/bin:\$PATH && cd ~/anima_chat_pack && nohup ./akida_bridge.bin daemon > logs/akida_bridge.out 2> logs/akida_bridge.err < /dev/null & disown"`
3. wait 30s
4. `ssh mini -- 'curl -s http://localhost:8000/akida/recent'` → `{"akida":[]}`

## Suggested fix

Look at the broker's WS handler for `/ws/akida_ingest` (likely in `anima_chat_pack/broker.*` or similar). Confirm it:

- parses incoming WS text frames as JSON
- appends `{"ts": ..., "spike_ids": [...], "regime": "..."}` to the same `deque` that `/akida/recent` reads from
- has a non-zero `maxlen`

Cross-check against pi5 spike_streamer JSON format (lines like `{"t_rel": 20511.83, "step": 204741, "n_spikes": 8, "spike_ids": [...], "regime": "R3_tonic_zero_input", "thr": [...]}`).

## Side findings (not blockers, observe)

- **websocat PATH**: mini's non-interactive ssh PATH does NOT include `/opt/homebrew/bin`. `akida_bridge.bin daemon` exits FATAL on `which websocat`. Workaround `export PATH=/opt/homebrew/bin:$PATH` before nohup. Permanent fix candidate: patch `akida_bridge.hexa` to probe `/opt/homebrew/bin/websocat` + `/usr/local/bin/websocat` before falling back to `$PATH`.
- **nc connection state**: `netstat -an | grep 192.168.50.155.9512` shows only FIN_WAIT_2 even while bridge counter rises (likely buffered FIFO data after pi5 close). Pi5 itself confirmed still streaming via manual `nc -w 2`. Separate observation; not blocking the broker gap above.

## Verdict on bridge restoration

Bridge daemon: RESTORED + ALIVE.
End-to-end ingest visible at `/akida/recent`: FAIL — broker handler gap.

## Status — main-HEAD review (post-PR-#187/#188/#189)

After this entry was drafted, three relevant PRs landed:

| PR | Title | Effect on hypotheses |
|---|---|---|
| #187 | broker silent json drop visibility | (c) — `except: continue` now `log.warning(... raw=%r ...)` |
| #188 | akida_consumer type_of "list" → "array" | sibling fix, downstream of `/akida/recent` |
| #189 | akida_bridge default `/ws/akida` → `/ws/akida_ingest` | bridge-side endpoint correctness |

Source review of `HEXAD/CHAT/server/broker.py` at main HEAD:

- (a) **DISPROVED** — handler line 340 `STATE.akida_history.append(msg)` IS present
- (b) **DISPROVED** — `/akida/recent` (line 165) reads same `STATE.akida_history`
- (c) **VISIBILITY ADDED, not yet observed** — PR #187 promoted silent drop to `log.warning`; logs will surface the actual JSON failure mode once a frame fails
- (d) **UNTESTED** — `STATE.akida_history` `maxlen` not yet inspected, but defaults in repo SSOT are non-zero

Per PR #187 commit caveat:

> Production caveat: mini PID 1691 runs the OLD broker; this PR lands on main only. User-gated restart required for the new log surface to fire on chat.dancinlab.org.

## Next step — gated on mini broker restart

1. User restart mini broker → new code path live (PRs #187/#188/#189 effective)
2. Re-run bridge ingest → observe `anima.err` for either:
   - **(c) confirmed** — `log.warning("akida ingest json drop: ... raw=...")` lines accumulate → fix JSON format mismatch between bridge frames and broker parser
   - **silence** — drop hypothesis falsified, deque populates → end-to-end CLOSED 🟢
3. If still empty AND no warning logs → inspect `STATE.akida_history` maxlen (hypothesis (d))

This patch document remains the SSOT measurement record; status will be updated when the restart-driven verification fires.

## Local repro verdict (2026-05-23T20:15 · pre-mini-restart)

mini broker 재시작 전, anima 측 worktree 에서 진행한 source-level 검증 결과 (b)/(c)/(d) 3 가설 모두 falsified 되었으며 실 root cause 는 bridge ↔ websocat 채널 race 로 옮겨졌다.

- (b) **FALSIFIED** — `STATE.akida_history` 는 `maxlen=200` 으로 정의되어 있다 (citation: `HEXAD/CHAT/server/broker.py:69` — `self.akida_history: deque[dict[str, Any]] = deque(maxlen=200)`). `/akida/recent` 는 같은 deque 를 `broker.py:163-165` 에서 읽는다. handler append target ↔ endpoint read target 일치 확인.
- (c) **FALSIFIED** — bridge frame 은 유효한 JSON 이다. `stamp_spike()` (`HEXAD/CHAT/server/akida_bridge.hexa:162-176`) 가 생성하는 frame 예시는 `{"step": 42, "n_spikes": 7, "regime": "R3_tonic_zero_input", "_bridge_ts": 1779534874.0217}`. Python `json.loads(<that>)` 는 dict 로 정상 round-trip 한다. broker `json.loads()` 가 이 형식에서 실패할 이유 없음.
- (d) **FALSIFIED** — maxlen 은 0 이 아닌 200 이다 (위 (b) citation 동일).
- (a) 는 main-HEAD review 단계에서 이미 DISPROVED (handler line 340 append 존재).

Bridge send mode 는 **TEXT** 로 일관 확인되어 `broker.py:334` `receive_text` 와 호환:
  - websocat backend (`hexa-lang/stdlib/websocket.hexa:408-422`) — default line-oriented text mode
  - native backend (`hexa-lang/stdlib/net/websocket_native.hexa:337-345`) — `_ws_encode_frame(1, message)` (opcode 1 = TEXT)

**Most-likely root cause (hypothesis e / upstream)** — `ws_send` (`hexa-lang/stdlib/websocket.hexa:419-420`) 는 FIFO 에 `printf %s <escaped> > $fifo &` 로 write 한다. 후행 `&` 가 write 를 background 로 돌리며, FIFO reader (websocat stdin) 가 이미 죽어 있으면 write 가 silently no-op 되더라도 `ws_send` 는 `exec()` 호출 성공 여부만 보고 `true` 를 return 한다. 즉 bridge 측 counter 상승 ≠ 실제로 frame 이 host 밖으로 나간다는 보장이 아니다.

**Mini-side check on restart** — `pgrep websocat` 와 `ss -tnp | grep :8000` 로 bridge 의 TCP peer 가 현재 broker PID 와 매칭하는지 확인한다. websocat process 가 사라져 있거나 peer 가 stale PID 면 위 race 가 confirm.

**Broker-side disambiguation (separate PR, parallel)** — `broker.py:340` 다음에 `log.info("akida append now=%d", len(STATE.akida_history))` 를 추가한다. 이 라인이 live 인 상태에서 차후 incident 가 발생하면 "append 호출 자체가 없음" (websocat dead / broker stuck) 과 "append 는 발화하지만 `/akida/recent` 가 empty" (deque write clobbered) 두 모드를 명확히 분리할 수 있다.

**Upstream filing** — `hexa-lang/inbox/patches/<slug>.md` (parallel agent 가 동시 작성 중) 에 `ws_send` 의 `&` race 를 hexa-lang 측 inbox 로 escalate.

요약: 4-가설 트리는 closed (a/b/c/d 모두 FALSIFIED), 잔여 가설은 anima repo 가 아닌 hexa-lang stdlib 의 `ws_send` FIFO background-write race 로 이동했다. mini broker 재시작 후 logs/process snapshot 으로 최종 확정 예정.
