---
schema: anima/modules/daemon/ai-native/1
last_updated: 2026-05-02
ssot:
  event_watcher:    modules/daemon/event_watcher.hexa
  utterance_gate:   modules/daemon/utterance_gate.hexa
  auto_speak_bridge: modules/daemon/auto_speak_bridge.hexa
  config:           config/auto_utterance_architecture.json
  events:           data/events.jsonl
  laws:             config/consciousness_laws.json
status: live — 3-step auto-utterance daemon pipeline; event watcher → utterance gate → speak bridge
roadmap_entry: 270
---

# anima daemon modules (AI-native)

Auto-utterance daemon pipeline — 3 sequential steps that detect external perturbations (checkpoint files / git commits / GPU pods / time / file mtimes), gate them through consciousness laws, and emit speak-out events.

## TL;DR for an agent reading this cold

- **3 files**: `event_watcher.hexa` (243 LOC) → `utterance_gate.hexa` (164 LOC) → `auto_speak_bridge.hexa` (185 LOC).
- **Pipeline order**: events.jsonl is appended by step 1, consumed by step 2, gated rows trigger step 3.
- Configured by `config/auto_utterance_architecture.json` (which event_sources to watch, gate thresholds, speak channel selection).
- **ROI #8 optimization** (event_watcher): per-scan shell forks reduced from ~8 to 1 combined probe + 1 sleep. now_iso cached once per scan.
- Tuple destructuring deliberately avoided (hexa 0.1.0-stage1 limitation).

## Architecture map

```
modules/daemon/
├── event_watcher.hexa        Step 1: detect perturbations → data/events.jsonl
├── utterance_gate.hexa       Step 2: gate events through consciousness laws
└── auto_speak_bridge.hexa    Step 3: bridge gated events → speak channel
```

## Pipeline data flow

```
External perturbation sources           (defined in config/auto_utterance_architecture.json)
   │
   ├── checkpoint (.pt files in checkpoints/)
   ├── git commit (HEAD changes in repo)
   ├── GPU pod (runpodctl status delta)
   ├── time (cron-style triggers)
   └── file mtime (watched paths)
   │
   ▼
event_watcher.hexa --scan | --watch
   │
   ▼  appends rows to
data/events.jsonl                       (audit log of all detected events)
   │
   ▼  consumed by
utterance_gate.hexa
   │  (gates against consciousness_laws.json — Φ threshold, law triplet, etc.)
   │
   ▼  passing events forwarded to
auto_speak_bridge.hexa
   │
   ▼  speak channel
```

## Public API

```hexa
// event_watcher.hexa
struct EventState {
    last_ckpt:   string,
    last_commit: string,
    last_pod:    string,
    last_time:   string,
}
// CLI: --scan (one-shot) | --watch (loop, 60s default)

// utterance_gate.hexa
fn gate_event(event: Event, laws: LawSet) -> GateVerdict
// → GateVerdict { pass: bool, law_id: string, phi_score: float, reason: string }

// auto_speak_bridge.hexa
fn bridge_to_speak(event: Event, verdict: GateVerdict) -> SpeakEmitResult
```

## Invocation patterns

```bash
# Step 1: one-shot scan (manual)
hexa run modules/daemon/event_watcher.hexa --scan

# Step 1: continuous watch (every 60s)
hexa run modules/daemon/event_watcher.hexa --watch

# Step 2: gate the latest 10 events
hexa run modules/daemon/utterance_gate.hexa --tail 10

# Step 3: bridge a gated event to speak channel
hexa run modules/daemon/auto_speak_bridge.hexa --event-id E12345
```

Recommended: run all 3 from a single watcher process via `tool/anima_daemon_pipeline.hexa` (if landed) or stitch via cron.

## Failure cascade

```
event_watcher.fail (path not readable)
  → events.jsonl not appended; downstream gate has nothing to consume
       → utterance_gate exits 0 with "no new events"
            → auto_speak_bridge idle
```

```
utterance_gate.fail (consciousness_laws.json missing)
  → events accumulate in events.jsonl ungated
       → eventual replay possible after laws.json restored
            → auto_speak_bridge can replay-skip already-bridged events via event_id
```

## raw#10 caveats

1. **HOME-relative paths.** All 3 daemons read `$HOME/Dev/anima` — fails on alternate layouts. Should accept `--base` arg.
2. **events.jsonl unbounded.** Append-only, no rotation. Long-running daemon → multi-GB log eventually.
3. **No leader election.** Running 2 watcher instances → duplicate event rows in events.jsonl. Use cron exclusive or systemd.
4. **runpodctl required for GPU pod source.** Missing → that source silently disabled with WARN log.
5. **utterance_gate consults consciousness_laws.json directly.** Schema drift in laws.json → gate logic must update; no schema version negotiation.
6. **No backpressure.** If speak channel is slow, auto_speak_bridge can flood; events queue in events.jsonl but downstream throttling is consumer's responsibility.
7. **Tuple destructuring avoided.** hexa 0.1.0-stage1 limitation; manual struct field access used. Future hexa versions may allow simplification.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `auto_speak_bridge.hexa` | `c616cedb86d63acf8f024eec90e72eefd8c6ec30323c53e15991104108ee0191` | 185 |
| `event_watcher.hexa` | `b1bd31abd9b7c8b653a0fb902921a44d9f325bc7b645dc9072072ebfbb64d925` | 243 |
| `utterance_gate.hexa` | `022ce59576b8e04257f818214b07331936e8e2d831f1935df83f40f8ac2df8a5` | 164 |

shas pinned 2026-05-02.
