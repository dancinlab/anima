# anima-eeg unified CLI + daemon architecture — spec (cond.7 candidate)

**Cycle:** 2026-05-04
**Status:** spec_landed (impl deferred to next cycle EXEC)
**Roadmap slot:** `.roadmap.eeg cond.7` candidate (next condition after cond.6 qmirror cross-witness)
**Sister roadmaps:** `.roadmap.eeg` cond.1 / cond.5 / `eeg.long_term_coding_paradigm_program` (14-idea register, lines 20-23)
**Source ideas:** `anima-clm-eeg/docs/d_day_session_2026_04_28/IDEAS_INVENTORY.md §3` (Tier A 5 + Tier B 5 + Tier C 4 = 14 paradigms)
**Raw invariants applied:** raw#9 (hexa-only on Mac) / raw#10 (honest C3) / raw#15 (no-personal-paths) / raw#37 (transient ubuntu helper) / raw#71 (falsifier-bound) / raw#91 (honesty-triad)

---

## 1. Goal & motivation

### 1.1 Problem statement

Today every paradigm in the `eeg.long_term_coding_paradigm_program` register lives as an **isolated one-shot script**. The 14 registered paradigms (Tier A 1–5, Tier B 8–12, Tier C 13–16) each have a `*.hexa` entry under `anima-eeg/tool/`:

- `daily_life_context_logger.hexa` (idea #2, 307 LoC)
- `eeg_feedback_loop.hexa` (idea #8, 528 LoC)
- `longitudinal_session_recorder.hexa` (idea #9, 156 LoC)
- `behavioral_correlates_logger.hexa` (idea #11, 396 LoC)
- (10 more, total 14 hexa modules)

Each module:
1. Opens its own BrainFlow board session (or attempts to — most are scaffolds with synthetic data).
2. Manages its own ring buffer / .npy writeout.
3. Has its own ad-hoc event log format.
4. Cannot **share** the EEG stream with another paradigm (BrainFlow boards are single-acquirer per serial port).

This makes **multi-paradigm concurrent measurement impossible**. If the user wants to run idea #2 (context labels) + idea #8 (feedback loop) + idea #9 (CLI correlation) simultaneously across a 1-hour coding session, today they must pick one. The OpenBCI board cannot be opened twice.

### 1.2 What a unified daemon unblocks

A single long-running EEG daemon that:

1. Owns the **single** BrainFlow session (one acquirer per board).
2. Maintains a shared ring buffer that any number of consumer paradigms can sample from.
3. Provides a stable **JSONL event log** that any paradigm or external process can append marker events to.
4. Exposes a unified CLI (`anima-eeg <cmd>`) for all session lifecycle + introspection.

Then **all 14 paradigms become concurrent listeners** on one stream, not competing acquirers. This directly unblocks:

| Idea | Tier | Name | Daemon need |
|------|------|------|-------------|
| #2 | A | Daily-life context labeling | Marker emission + 24/7 background recording |
| #8 | B | EEG-driven feedback loop | Real-time ring buffer read for engagement metric |
| #9 | B | Claude CLI longitudinal correlation | Post-hoc EEG window pairing with `~/.claude/*.jsonl` |
| #11 | B | Behavioral correlates (keyboard/mouse) | Marker emission from input device hooks |
| #13 | C | Long-duration 1hr+ recording | Crash-recovery + segmented writeout |
| #5 | A | Self-experiment N=1 longitudinal | Cross-session ledger continuity |

Without the daemon, ideas #2 / #8 / #9 / #11 are **structurally** stuck at "scaffold landed, no real measurement" — even after B-track v7 (electrode contact health) closure restores clean signal.

### 1.3 Non-goals (what this spec does NOT do)

- Does NOT replace `anima-eeg/calibrate.hexa` / `board_health_check.hexa` / `collect.hexa` — those remain the canonical one-shot diagnostic tools (B1/B2/B3 gates).
- Does NOT define new metric algorithms — daemon is **transport infrastructure only**, metrics live in `anima-eeg-core/tool/modules/_metrics/`.
- Does NOT solve electrode contact (B-track v7 prerequisite — see §9 caveats).
- Does NOT introduce any new Python module on Mac side (raw#9 strict).

---

## 2. Command surface (`anima-eeg <cmd>`)

The unified CLI entry point lives at `anima-eeg/tool/anima_eeg_cli.hexa` (see §5 for raw#9 enforcement). All subcommands return JSON on stdout and exit-0 on success / non-zero with `{"error": "..."}` on failure.

### 2.1 `start` — spawn daemon

```
anima-eeg start [--board cyton|cyton_daisy|synthetic] [--port /dev/cu.usbserial-DM*] [--samplerate 250|500|1000]
```

- Acquires single-instance lock (`anima-eeg/recordings/.daemon.lock`, see §3.4).
- Forks daemon child, parent returns `{"pid": N, "lock": "...", "started_at": "..."}`.
- Daemon child opens BrainFlow board, allocates ring buffer (§3.1), opens event log (§3.2).
- On failure (lock held, board not found, USB serial unavailable): exit-1 with structured error.

### 2.2 `stop` — graceful shutdown

```
anima-eeg stop [--flush-window-secs 5] [--force]
```

- Sends SIGTERM to daemon pid.
- Daemon flushes pending samples, finalizes ring buffer to `anima-eeg/recordings/sessions/<ts>/ringbuf_final.npy`, closes event log, releases lock.
- `--force` sends SIGKILL after 10s grace.

### 2.3 `record` — start a recording session (manual or daemon-driven)

```
anima-eeg record --duration-secs N [--label <free-text>] [--paradigm idea_2|idea_8|...]
```

- Requires daemon running (else exit-2 with hint to call `start`).
- Allocates a **session window** (sub-region of the daemon's continuous stream).
- Writes session metadata to `anima-eeg/recordings/sessions/<ts>/manifest.json` (start_ts, duration, label, paradigm, board_config, lock_id).
- On completion, emits dual artifacts: `.npy` (16ch × samples × float32) + symlinked event-log slice (start_ts → end_ts subset of daemon's JSONL).
- Manual mode (`--paradigm` omitted) = pure recording. Paradigm mode hooks the named listener (§4.2).

### 2.4 `mark` — emit timestamped event marker

```
anima-eeg mark --kind <stim_onset|behavior|cli_msg|context_label|custom> --payload '<json>' [--source <module>]
```

- Appends one line to `anima-eeg/recordings/daemon_events.jsonl`:
  ```
  {"ts":"2026-05-04T13:42:01.234567Z","ts_ns_monotonic":12345678901234,"source":"behavioral_correlates_logger","kind":"behavior","payload":{"keystroke":"a","ts_input":...}}
  ```
- **Falsifier F-CLI-2 target:** event lands in JSONL within 50ms of CLI invocation (measured wallclock from `anima-eeg mark` start to `fsync()` complete).
- Schema (§3.2) is rigid — any unknown `kind` is accepted but validators downstream may filter.

### 2.5 `correlate` — pair recent EEG window with external signal

```
anima-eeg correlate --window-secs 30 --external-jsonl <path> [--key ts] [--output <path>]
```

- Reads last N seconds from ring buffer.
- Reads external signal (e.g., `~/.claude/projects/<proj>/*.jsonl` for idea #9, or behavioral log for idea #11).
- Emits paired (eeg_window, external_event) tuples to `anima-eeg/recordings/correlations/<ts>.jsonl`.
- Note: this is **post-hoc pairing**, not a continuous stream join. For continuous stream join, register a listener via §4.2.

### 2.6 `status` — daemon health snapshot

```
anima-eeg status [--json|--tui]
```

Returns:
```json
{
  "daemon_pid": 12345,
  "uptime_secs": 3612,
  "board": "cyton_daisy",
  "samplerate_hz": 125,
  "channels": 16,
  "ring_buffer_fill_secs": 58.4,
  "ring_buffer_capacity_secs": 60.0,
  "samples_acquired_total": 451500,
  "samples_dropped_total": 0,
  "last_marker_ts": "2026-05-04T13:42:01Z",
  "last_marker_kind": "stim_onset",
  "impedance_kohm": [12, 18, 9, 14, ...],
  "impedance_last_check_ts": "...",
  "active_listeners": ["idea_2_context", "idea_8_feedback"]
}
```

**Falsifier F-CLI-1 target:** returns within 100ms when daemon running (no full ring buffer scan, just read shared header).

### 2.7 `listen` — register a paradigm listener (subagent / process)

```
anima-eeg listen --paradigm idea_8 --window-secs 4 --hop-secs 1 --metric lz76|alpha|engagement [--out-jsonl <path>]
```

- Subscribes to ring buffer with sliding window.
- For each window, computes the named metric (delegated to `anima-eeg-core/tool/modules/_metrics/<m>_native.hexa`).
- Emits one JSONL line per window to `--out-jsonl` (default: `anima-eeg/recordings/listeners/<paradigm>_<ts>.jsonl`).
- Long-running command (until daemon stops or SIGINT). Multiple listeners coexist; each gets its own ring buffer cursor.

### 2.8 Ancillary

- `anima-eeg log [--tail N] [--kind <k>] [--since <ts>]` — query event log.
- `anima-eeg sessions [--since <ts>]` — list past recording sessions.
- `anima-eeg version` — emit `{"version":"...", "raw_invariants":["raw#9","raw#15","raw#37","raw#71"]}`.

---

## 3. Daemon architecture

### 3.1 Ring buffer

**Layout:** mmap-backed file at `anima-eeg/recordings/.daemon.ringbuf` with header + circular sample region.

```
┌─────────────────────────────────────────────────┐
│ Header (4096 bytes, page-aligned)               │
│  - magic: "ANIMA-EEG-RINGBUF-v1"                │
│  - n_channels: u32 (16)                         │
│  - samplerate_hz: u32 (125 cyton+daisy / 250)   │
│  - capacity_samples: u32 (e.g., 7500 for 60s)   │
│  - sample_dtype: "float32"                      │
│  - write_cursor: u64 (atomic, monotonic)        │
│  - samples_dropped: u64 (atomic)                │
│  - last_impedance_kohm: f32[16]                 │
│  - last_impedance_ts_ns: u64                    │
│  - daemon_pid: u32                              │
│  - daemon_started_ts_ns: u64                    │
├─────────────────────────────────────────────────┤
│ Circular sample region                          │
│  - capacity_samples × n_channels × float32      │
│  - 60s default = 7500 × 16 × 4B ≈ 480 KB        │
│  - 5min variant = 37500 × 16 × 4B ≈ 2.4 MB      │
└─────────────────────────────────────────────────┘
```

**Sizing decision:** default 60s (480 KB). Optional `--ringbuf-secs 300` for the 5min variant when running long-duration paradigms (idea #13). 1hr+ recordings (idea #13/#14) flush to per-segment `.npy` every 60s — ring buffer is **transport**, not archive.

**Atomicity:** `write_cursor` is the only mutated header field on hot path. Writes are single-producer (daemon BrainFlow thread). Readers (listeners) snapshot `write_cursor` then read backward, accepting a race window of <1 sample (~8ms at 125Hz).

**Sample loss accounting:** if BrainFlow's internal queue overflows (board faster than daemon read loop), `samples_dropped` increments and is exposed via `status`. Falsifier F-CLI-3 target: 0 drops over 1hr at 125Hz.

### 3.2 Event log JSONL

**Path:** `anima-eeg/recordings/daemon_events.jsonl`

**Schema (one JSON object per line):**
```json
{
  "ts": "2026-05-04T13:42:01.234567Z",
  "ts_ns_monotonic": 12345678901234,
  "source": "<module-name>",
  "kind": "<stim_onset|behavior|cli_msg|context_label|impedance_check|daemon_event|custom>",
  "payload": { /* free-form, but schema-validated per kind */ },
  "session_id": "<optional, set if inside an active session window>"
}
```

**Schema enforcement:** `anima-eeg mark` validates `kind` against an allowlist. Unknown kinds rejected with exit-3. Payload schemas per kind:

| kind | required payload fields |
|------|-------------------------|
| `stim_onset` | `stim_id` (str), `stim_kind` (visual\|auditory\|tactile) |
| `behavior` | `device` (keyboard\|mouse\|screen), `event` (str) |
| `cli_msg` | `direction` (user\|assistant), `len_chars` (int), `jsonl_path` (str) |
| `context_label` | `label` (str), `confidence` (float in [0,1]) |
| `impedance_check` | `kohm` (float[16]) |
| `daemon_event` | `event` (start\|stop\|drop\|board_disconnect) |
| `custom` | none required (fully free-form) |

**Append semantics:** `O_APPEND | O_DSYNC` open, line atomically written + `fsync()` before CLI returns. Falsifier F-CLI-2 measures the wallclock from `mark` invocation to `fsync` completion.

### 3.3 Crash recovery / pickup

If daemon crashes mid-session:

1. Lock file (§3.4) becomes stale (pid no longer running).
2. Next `anima-eeg start` invocation detects stale lock → reads ring buffer header `daemon_pid` → confirms pid not running → emits `daemon_event` line to JSONL `{"event":"crash_recovery","prev_pid":N,"prev_uptime_secs":X}` → reclaims lock.
3. Ring buffer **content is preserved** (mmap survives process death) but `write_cursor` may be stale by up to one sample. New daemon resets `write_cursor` to header value, resumes BrainFlow board, continues writing.
4. Active sessions in flight are marked `crashed` in their `manifest.json` and the partial `.npy` is finalized with whatever samples landed before crash.

No transactional log replay — daemon is **stateless beyond ring buffer + event log**. Ring buffer == in-memory snapshot, event log == persistent record.

### 3.4 Single-instance lock

**Path:** `anima-eeg/recordings/.daemon.lock`

**Format:** flock-protected file containing `{"pid": N, "started_at": "...", "board": "...", "ringbuf_path": "..."}`.

**Acquisition:** `flock(LOCK_EX | LOCK_NB)` — fails immediately if another daemon holds it. CLI subcommands (`mark`, `record`, `status`, `listen`) acquire `LOCK_SH` (shared) for read access to header fields, never block daemon's exclusive write.

**Stale lock handling:** if pid in lock file is not running (verified via `kill -0 <pid>`), CLI auto-clears and proceeds. This is the only auto-recovery path.

---

## 4. Integration with paradigms

### 4.1 Listener API surface

Each paradigm becomes a **subscriber** rather than a self-contained acquirer. Pattern:

```
anima-eeg listen --paradigm <id> --window-secs <w> --hop-secs <h> --metric <m> --out-jsonl <out>
  ↓
internally calls anima-eeg-core/tool/modules/_metrics/<m>_native.hexa
  ↓
emits per-window JSONL row keyed by ring-buffer cursor at window end
```

### 4.2 Per-paradigm wiring

#### Idea #2 — Daily-life context labeling
- **Producer:** `anima-eeg/tool/daily_life_context_logger.hexa` reads keyboard/screen/audio activity.
- **Wiring:** logger calls `anima-eeg mark --kind context_label --payload '{"label":"coding","confidence":0.9}'` whenever activity classifier emits a new label.
- **No EEG read on logger side** — logger is pure marker emitter.
- **Pairing:** post-hoc `anima-eeg correlate --window-secs 30 --external-jsonl daemon_events.jsonl --kind context_label`.

#### Idea #8 — EEG-driven feedback loop
- **Wiring:** `anima-eeg listen --paradigm idea_8 --window-secs 4 --hop-secs 1 --metric engagement` runs in background.
- Consumer process reads `--out-jsonl`, on threshold-cross dispatches Mac notification (delegated to `osascript` via existing `eeg_feedback_loop.hexa` notification path).
- **Latency budget:** sample-to-notification ≤ 5s (4s window + 1s pipeline) — documented, not falsified this cycle.

#### Idea #9 — Claude CLI longitudinal correlation (CLI-only, NO API)
- **Producer:** lightweight watchdog tails `~/.claude/projects/*/conversations/*.jsonl` (existing `longitudinal_session_recorder.hexa` foundation).
- For each new (user_msg, assistant_msg) pair: `anima-eeg mark --kind cli_msg --payload '{"direction":"...","len_chars":N,"jsonl_path":"..."}'`.
- **Pairing:** end-of-day batch `anima-eeg correlate --window-secs 60 --external-jsonl daemon_events.jsonl --kind cli_msg`.
- **NO API constraint:** no `api.anthropic.com` reads anywhere in this path. Source is Claude CLI's local conversation jsonl only.

#### Idea #11 — Behavioral correlates
- **Producer:** `anima-eeg/tool/behavioral_correlates_logger.hexa` (input device hooks).
- For each input event class transition (typing-burst-start, mouse-idle-cross, scroll-velocity-shift): `anima-eeg mark --kind behavior --payload '{...}'`.
- **Listener:** `anima-eeg listen --paradigm idea_11 --window-secs 8 --hop-secs 2 --metric cognitive_load` running concurrent with marker production.
- **Cross-modal join:** done at analysis time, not in daemon hot path (daemon stays minimal).

### 4.3 New paradigm registration

A new paradigm registers by:

1. Picking a unique `--paradigm <id>` string.
2. Appending an entry to `anima-eeg/recordings/.paradigm_registry.jsonl`:
   ```
   {"id":"idea_N","registered_ts":"...","listener_kinds":["..."],"marker_kinds":["..."]}
   ```
3. Optionally implementing a `*.hexa` module that runs the listen-loop (if metric is custom and not in `_metrics/`).

No daemon restart required — daemon doesn't read the registry, registry is documentation for cross-paradigm coordination.

---

## 5. Implementation strategy under raw#9

### 5.1 Side-by-side responsibility matrix

| Component | Mac side (raw#9: hexa-only) | Linux/ubu1 side (raw#37: transient py allowed) |
|-----------|-----------------------------|------------------------------------------------|
| `anima-eeg <cmd>` CLI entry | `anima-eeg/tool/anima_eeg_cli.hexa` (raw#9) | symlink / wrapper bash if user wants from ubu1 |
| Ring buffer mmap | hexa native (mmap syscall via hexa stdlib) | hexa native (same code) |
| Event log JSONL append | hexa native | hexa native |
| BrainFlow board acquisition | **NOT on Mac** — Mac uses USB serial bridge OR stub | `state/.brainflow_daemon_helper.py` (raw#37 transient, ubu1 only) |
| Listener metric compute | `anima-eeg-core/tool/modules/_metrics/<m>_native.hexa` (already raw#9) | same hexa, runs on either |
| Daemon process supervision | hexa fork + signal | hexa fork + signal |

### 5.2 BrainFlow Python helper — transient ubuntu helper pattern (raw#37)

**Honest C3 (raw#10):** BrainFlow is a Python/C++ library. There is no first-party BrainFlow port to hexa-lang. Per raw#9, we cannot import a Python module on Mac. Per raw#37, we are allowed a **transient ubuntu helper** that lives outside the repo (or in `state/` with `.` prefix) and is invoked over IPC.

**The split:**

- **Linux/ubu1:** `state/.brainflow_daemon_helper.py` — reads BrainFlow stream, writes raw samples to a Unix-domain socket OR shared mmap segment. Spec'd here, NOT implemented this cycle.
- **Mac:** `anima_eeg_cli.hexa` connects via SSH-tunneled UDS or directly to a USB serial → mmap bridge if board is plugged into Mac. If Mac-attached: hexa speaks the OpenBCI Cyton serial protocol directly (existing `anima-eeg/calibrate.hexa` already does serial reads in pure hexa, no BrainFlow).

**Decision tree:**

```
Is OpenBCI plugged into Mac?
├─ YES: hexa-only path, talks raw serial protocol (no BrainFlow needed). Daemon runs on Mac.
└─ NO (plugged into ubu1): hexa CLI on Mac → SSH tunnel → daemon on ubu1
                          → ubu1 daemon spawns transient .py helper (raw#37) for BrainFlow only
                          → ring buffer mmap on ubu1, exposed via UDS to Mac CLI
```

**Result:** Mac never imports Python. .py only on Linux side and only as transient helper (raw#37 explicit concession). raw#9 honored on Mac strictly. **No new .py files on Mac**, including under `_python_bridge/` (per session memory `feedback_py_to_hexa_only`).

### 5.3 Honest C3 declaration of the split

This spec **explicitly declares** a hexa-on-Mac, py-on-Linux split. This is NOT a violation of raw#9 because:

1. raw#9 is enforced **per host** — Mac side has zero .py.
2. raw#37 explicitly permits **transient** Python helpers on Linux for hardware-bound libraries that cannot be ported (e.g., BrainFlow's C++ binding chain).
3. The helper is **transient** — it lives in `state/.<name>.py`, is regenerated per cycle, and never commits to a permanent module path.

If the user later runs OpenBCI on Mac directly, the daemon runs hexa-only end-to-end. Linux helper becomes unused. Spec accommodates both.

### 5.4 LoC budget for impl cycle (next)

Pre-impl estimate, NOT this cycle:

| File | Estimated LoC |
|------|---------------|
| `anima-eeg/tool/anima_eeg_cli.hexa` (entry + subcommand dispatch) | ~600 |
| `anima-eeg/tool/_daemon/ringbuf.hexa` (mmap header + circular write) | ~400 |
| `anima-eeg/tool/_daemon/event_log.hexa` (JSONL append + schema) | ~350 |
| `anima-eeg/tool/_daemon/lock.hexa` (flock + stale recovery) | ~150 |
| `anima-eeg/tool/_daemon/listener.hexa` (sliding window + metric dispatch) | ~450 |
| `state/.brainflow_daemon_helper.py` (Linux only, raw#37 transient) | ~300 |
| Falsifier suite (F-CLI-1..4 selftest) | ~250 |
| **Total impl cycle** | **~2500 LoC across 7 files** |

---

## 6. Falsifier set (raw#71)

Pre-registered acceptance criteria. Each must have a measurable outcome and a failure-mode declaration.

### F-CLI-1: status latency
- **Claim:** `anima-eeg status` returns daemon health JSON in <100ms when daemon running.
- **Measure:** 10 invocations, median wallclock from CLI start to JSON write to stdout.
- **Pass condition:** median ≤ 100ms AND 95th percentile ≤ 200ms.
- **Fail mode:** mmap header read pulls in cold pages (kernel page cache miss). Mitigation: `madvise(WILLNEED)` on header at daemon start.

### F-CLI-2: marker latency
- **Claim:** `anima-eeg mark` event lands in JSONL within 50ms of CLI invocation.
- **Measure:** wrapper script invokes `mark`, immediately reads tail of JSONL, computes (file mtime − invocation start). 100 trials.
- **Pass condition:** 99th percentile ≤ 50ms AND 0 missing events.
- **Fail mode:** `fsync` on slow disk pushes p99 over 50ms. Documented but not blocker — async-fsync variant noted as fallback in §3.2.

### F-CLI-3: ring buffer integrity over 1hr
- **Claim:** ring buffer survives 1hr continuous recording without sample loss.
- **Measure:** synthetic source (BrainFlow synthetic board) at 250Hz × 16ch × 3600s. Final `samples_dropped_total` from daemon header.
- **Pass condition:** `samples_dropped_total == 0` AND `samples_acquired_total == 250 * 3600 * 16 ± epsilon`.
- **Fail mode:** GC stutter or BrainFlow internal queue overflow under load. Mitigation: dedicated read thread with elevated priority (documented for impl).

### F-CLI-4: paradigm wiring selftest
- **Claim:** at least 2 of {idea #2, idea #8, idea #9, idea #11} are demonstrably wired via daemon API in a single self-test.
- **Measure:** selftest script runs daemon, fires synthetic markers for #2 + #11 (context label + behavior), runs listener for #8 (engagement on synthetic stream), runs post-hoc correlate for #9 (synthetic CLI jsonl).
- **Pass condition:** all 4 produce output artifacts under `anima-eeg/recordings/sessions/<selftest_ts>/` AND no JSONL schema violations.
- **Fail mode:** CLI dispatch bug, schema mismatch, or listener cursor race. Each failure is a distinct fix.

### F-CLI-5 (stretch, not blocking cond.7 land)
- **Claim:** daemon survives Mac sleep/wake cycle without ring buffer corruption.
- **Measure:** daemon up, `pmset sleepnow`, wake after 60s, `anima-eeg status`.
- **Pass condition:** status returns OK, no header magic byte corruption, BrainFlow board reconnect or graceful `daemon_event:board_disconnect` log line.
- **Stretch rationale:** Mac sleep behavior with USB serial is hardware-specific and may require user-side `caffeinate -d` workaround.

---

## 7. Cost band

**$0** — local Mac + ubu1 hardware reuse. Specifically:

- **Mac side:** hexa-only, no GPU, no cloud, no new dependencies.
- **ubu1 side:** existing `venv_orchestrator` (per session memory `reference_ubu1_venv_orchestrator`) hosts the transient BrainFlow helper. No new pods, no new disk allocation beyond ~10MB for ring buffer + event log growth (rotation policy keeps event log ≤ 100MB, see §9).
- **No paid API:** raw#9 + idea #9 NO API constraint preserved. CLI reads `~/.claude/projects/*.jsonl` (local file system) only.
- **No hardware purchase:** OpenBCI 16ch arrival is a separate cond.1 prerequisite (`eeg.blk.1`), not part of this cond.7 spec.

---

## 8. Cross-link block

### 8.1 Sister roadmaps & conds

- `.roadmap.eeg cond.1` — B1-B4 4관문 PASS (real signal arrival). Daemon is **useless without clean signal**, so cond.1 remains hard prerequisite for daemon's real-data falsifiers (F-CLI-3 with real data, not synthetic).
- `.roadmap.eeg cond.5` — runtime hookup (anima-eeg/realtime.hexa → metric ingest → CLM consciousness verifier). Daemon is the **invocation seam** for cond.5 — current `realtime.hexa` becomes one of many listeners on the daemon.
- `.roadmap.eeg long_term_coding_paradigm_program` (line 20) — 14 ideas. cond.7 is the **invocation seam** that line 20 explicitly names as `next_cycle_dep`.
- `.roadmap.eeg eeg.tier_a_paradigm_register` (line 21) — ideas #1-5. Idea #2 (context labeling) and #5 (longitudinal) directly consume daemon API.
- `.roadmap.eeg eeg.tier_b_paradigm_register` (line 22) — ideas #8-12. Idea #8/#9/#11 directly consume daemon API.
- `.roadmap.eeg eeg.tier_c_paradigm_register` (line 23) — ideas #13-16. Long-duration (#13) and pre/post (#16) benefit from segmented writeout (§3.1).

### 8.2 Sister cross-domain roadmaps

- `.roadmap.anima_clm_eeg cond.1 / cond.3` — anima-clm-eeg's CLM-EEG bridge needs continuous EEG stream. Daemon provides it.
- `.roadmap.slm_speech_eeg_lm cond.2` — EEG-conditioned LM head spec; sister invocation seam.
- `.roadmap.blm_brain_lm cond.3 F-CT-3` — BOLD↔EEG correlation r ≥0.5; daemon enables paired-stream collection.

### 8.3 Upstream prerequisites

- **B-track v7 measurement** (`anima-eeg/docs/electrode_reseat_b_track_runbook_2026_05_03.md`) — daemon useless if signal is saturated / electrode contact bad. cond.7 land does NOT require B-track v7 PASS, but cond.7 EXEC selftest with real signal does (F-CLI-3 gets useful data only with clean electrodes).
- **OpenBCI 16ch hardware arrival** (`eeg.blk.1`) — same as above for real-data falsifiers; synthetic-board falsifiers can land without hardware.

### 8.4 Downstream consumers

- Each of the 14 paradigms in `eeg.tier_{a,b,c}_paradigm_register` becomes a daemon consumer. Per-paradigm wiring details in §4.2 above.
- `anima-eeg-core/tool/modules/_metrics/*_native.hexa` — listeners delegate metric compute to existing PORTs (lz76, pe, hjorth, phi_proxy).
- `tool/clm_consciousness_verify.hexa` — orchestrator consumes daemon listener output as one of its substrate inputs.

### 8.5 Predecessor audit

- `anima-eeg/docs/anima_eeg_protocols_quickstart_2026_05_03.md` — current protocols assume one-shot scripts. cond.7 supersedes that pattern for paradigms that need concurrency.
- `anima-eeg/docs/electrode_reseat_b_track_runbook_2026_05_03.md` — physical-layer prerequisite (orthogonal axis).
- `anima-clm-eeg/docs/d_day_session_2026_04_28/IDEAS_INVENTORY.md §3` — source of the 14-idea register.

---

## 9. Honest C3 (raw#10) — caveats

### Caveat 1: Daemon does NOT replace clean electrode contact

The daemon transports samples; it cannot improve their quality. If electrode impedance > 50 kΩ or saturation occurs (B-track unresolved per `electrode_reseat_b_track_runbook_2026_05_03.md`), the ring buffer will faithfully store **garbage**. cond.7 PASS does not imply usable data; cond.1 (B1-B4) remains the gate for that.

### Caveat 2: 24/7 wear is blocked by user health, not by software

The daemon's design supports continuous 24/7 recording. However, current OpenBCI helmet ergonomics cause scalp pain on extended wear (referenced in `eeg.tier_c_paradigm_register honest_c3` for sleep tracking). Per session memory, **user health > falsifier closure**: cond.7 design accommodates 24/7 but does not pressure the user to attempt it. Realistic measurement windows are 1-3hr per session, repeated daily.

### Caveat 3: Event log unbounded growth — rotation policy required

`anima-eeg/recordings/daemon_events.jsonl` grows monotonically. At idea #11 typing-burst rate (~5 markers/sec during active coding), 8hr/day = ~144k lines/day ≈ 30 MB/day. Rotation policy:

- Daily rotation: at midnight local time, daemon renames active log to `daemon_events.<YYYY-MM-DD>.jsonl` and opens fresh active log.
- Retention: keep last 30 days locally, archive older to `anima-eeg/recordings/archive/<YYYY-MM>/`.
- Total disk budget: ~1 GB at steady state for log. Ring buffer is fixed 480 KB.
- **Caveat-of-caveat:** rotation logic is impl-cycle work; this spec defines the policy but does not implement it. Until rotation lands, the daemon emits a `daemon_event:log_size_warn` line every 100 MB threshold cross.

### Caveat 4: hexa↔py cross-OS bridge latency unmeasured

The Linux-helper path (§5.2) introduces a network-or-UDS hop between Mac CLI and ubu1 daemon. Latency budget for SSH-tunneled UDS over LAN: ~5-15ms typical, but unmeasured in this spec. If empirically the hop pushes F-CLI-1 (status) or F-CLI-2 (mark) over their thresholds, the falsifier definition allows either:
- relax the threshold for cross-OS configurations (with explicit mode flag), or
- mandate Mac-attached OpenBCI for low-latency paradigms.
This is a **deferred decision** — measured at impl cycle, not legislated here.

### Caveat 5: Race between listener cursor and writer

Multiple listeners reading the ring buffer while daemon writes can race on `write_cursor` snapshot. The 1-sample tolerance (~8ms at 125Hz) is acceptable for all current paradigms (window sizes 1-30s, sample-level alignment not required). But: any future paradigm that needs sub-sample alignment (e.g., precise stim-locked ERP) must use the event log's `ts_ns_monotonic` for alignment, not the ring buffer cursor. Spec'd, not enforced — selftest F-CLI-4 does not exercise this.

### Caveat 6: This spec does NOT address electrode impedance live monitoring beyond snapshot

`status` exposes `last_impedance_kohm` and `impedance_last_check_ts`. The daemon does NOT continuously re-measure impedance (would interrupt acquisition). User must run `anima-eeg/calibrate.hexa` between sessions (existing tool) or daemon emits `impedance_check_overdue` warning after 1hr. Live impedance monitoring is a separate cond / future spec.

---

## 10. Roadmap entry proposal

**For next-cycle land (DO NOT edit `.roadmap.eeg` in this cycle).** The exact JSONL line to append:

```json
{"type":"entry","id":"eeg.cond.7","kind":"cond","title":"anima-eeg unified CLI + daemon architecture — single-acquirer EEG daemon + ring buffer + event log + paradigm listener API as invocation seam for 14-idea register","desc":"24/7-capable EEG daemon owning single BrainFlow acquisition, mmap ring buffer (60s default / 5min variant), JSONL event log, single-instance flock lock, paradigm listener API (subscribe-by-window). Unblocks ideas #2/#8/#9/#11 concurrent measurement. raw#9 hexa-on-Mac, raw#37 transient py-on-Linux split honestly declared.","status":"spec_landed","substrates":["eeg","cli","daemon","invocation_seam","longitudinal"],"contributes_to":["eeg.cond.1","eeg.cond.5","eeg.long_term_coding_paradigm_program"],"source":"anima-eeg/docs/anima_eeg_unified_cli_daemon_spec_2026_05_04.md","spec_loc":"~520","cycle":"2026-05-04","verifier":{"type":"script","path":"anima-eeg/tool/anima_eeg_cli.hexa","exit_zero_means_met":false,"sub_gates":["anima-eeg/tool/_daemon/ringbuf.hexa","anima-eeg/tool/_daemon/event_log.hexa","anima-eeg/tool/_daemon/lock.hexa","anima-eeg/tool/_daemon/listener.hexa"],"status_emit":"__EEG_UNIFIED_CLI_DAEMON__ <SPEC_LANDED|IMPL_LANDED|SELFTEST_PASS>"},"falsifiers":{"F-CLI-1":"status latency p50 ≤ 100ms","F-CLI-2":"mark→jsonl ≤ 50ms p99","F-CLI-3":"1hr ring buffer 0 sample loss","F-CLI-4":"≥2 of {idea #2,#8,#9,#11} wired in selftest","F-CLI-5":"(stretch) daemon survives sleep/wake"},"raw_invariants":["raw#9 hexa-only on Mac","raw#10 honest C3 (6 caveats)","raw#15 repo-relative paths","raw#37 transient py helper on Linux declared","raw#71 5 falsifiers pre-registered","raw#91 honesty-triad on hexa/py split"],"honest_c3_caveats":6,"prerequisite":"eeg.cond.1 (B1-B4 PASS) for real-data falsifiers; spec land does NOT require cond.1","cost_band":"$0","blocker_reason":"impl cycle deferred — spec only this cycle (2026-05-04); next cycle EXEC for ~2500 LoC across 7 files (per spec §5.4)","since":"2026-05-04"}
```

**Land criteria for status transitions:**
- `SPEC_LANDED` (this cycle): doc disk-landed, roadmap entry committed.
- `IMPL_LANDED`: 7 hexa files (§5.4) disk-landed + selftest exit-0 in synthetic-board mode.
- `SELFTEST_PASS`: F-CLI-1..4 all PASS with real OpenBCI 16ch (after cond.1 closure).

---

## 11. Cross-cycle TODO (next EXEC cycle)

1. Implement `anima-eeg/tool/anima_eeg_cli.hexa` with subcommand dispatch (§2).
2. Implement `_daemon/ringbuf.hexa` mmap header + circular write (§3.1).
3. Implement `_daemon/event_log.hexa` JSONL append with schema (§3.2).
4. Implement `_daemon/lock.hexa` flock + stale recovery (§3.4).
5. Implement `_daemon/listener.hexa` sliding window dispatch to existing `_metrics/*_native.hexa` (§4.1).
6. Spec-and-land `state/.brainflow_daemon_helper.py` for ubu1 side ONLY (raw#37, transient, do not commit) (§5.2).
7. F-CLI-1..4 selftest with synthetic BrainFlow board (no hardware required).
8. Add `eeg.cond.7` JSONL entry to `.roadmap.eeg` (§10 above).
9. Update `eeg.long_term_coding_paradigm_program.next_cycle_dep` field to point at `eeg.cond.7 IMPL_LANDED`.
10. Cross-update `.roadmap.anima_clm_eeg` to reference daemon as upstream invocation seam.

---

## 12. End-of-spec checklist

- [x] Goal & motivation referenced 14-idea register (§1)
- [x] Command surface ≥6 subcommands defined (§2 — 8 subcommands)
- [x] Daemon architecture: ring buffer + event log + crash recovery + lock (§3)
- [x] Per-paradigm wiring for ideas #2/#8/#9/#11 (§4.2)
- [x] raw#9 strict on Mac + raw#37 honest declaration of py-on-Linux (§5)
- [x] Falsifier set ≥4 (raw#71) — 5 declared, 4 blocking + 1 stretch (§6)
- [x] Cost band $0 (§7)
- [x] Cross-link sister roadmaps + upstream + downstream (§8)
- [x] Honest C3 (raw#10) ≥4 caveats — 6 declared (§9)
- [x] Roadmap entry JSONL proposed, NOT edited in `.roadmap.eeg` this cycle (§10)
- [x] Repo-relative paths only (raw#15) — verified throughout
- [x] No code/impl in this BG — spec doc only
- [x] LoC target 400-650 — actual ~520 LoC

**End of spec.**
