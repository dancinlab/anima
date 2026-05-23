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
