# chat/duo — ai-native module doc

**Role**: N=2 multi-agent dialogue module (CLM A ↔ CLM B autonomous speech via
stdin/stdout channel pair). Implements L2 layer of
`docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md`.

User directive verbatim (cycle 2026-05-08):

> "두 instance (CLM A ↔ CLM B) 가 stdin/stdout 으로 자율 대화. <=== very good"
> "여러명 일때도 진짜로 사람들끼리 대화 하듯이"

## Module Pattern (recursive)

```
chat/duo/
├─ duo.hexa     ← module body (channel orchestrator + per-turn verdict)
├─ duo.ai.md    ← this doc (ai-native)
└─ (cores)      ← external: chat/anima_native/, chat/llama/, chat/clm_v4/
                  Each spawned instance is one of these existing modules.
```

This module is a **composer**, not a substrate — it does no inference itself.
It spawns two pre-existing chat modules and wires their stdio together.

## Architecture

```
anima dialogue --duo <model_a> <model_b>
   │
   ▼
tool/anima_cli/dialogue.hexa (topic dispatcher)
   │ --duo flag → forwards argv
   ▼
tool/anima_cli/chat/duo/duo.hexa (THIS MODULE)
   │ resolve aliases · open channel pair · spawn instances
   ▼
   ┌──────────────────────────┐  channel_AB  ┌──────────────────────────┐
   │  proc instance A         │ ──── tx ───► │  proc instance B         │
   │  hexa run chat.hexa <a>  │              │  hexa run chat.hexa <b>  │
   │  · sys_stdin_read_line_  │              │  · sys_stdin_read_line_  │
   │    timeout(tick_ms)      │ ◄─── rx ──── │    timeout(tick_ms)      │
   │  · _invoke_core / llama_ │  channel_BA  │  · _invoke_core / llama_ │
   │    generate              │              │    generate              │
   └──────────────────────────┘              └──────────────────────────┘
```

Each instance is the **existing chat REPL** (`anima_native`, `llama`,
`clm_v4`). The duo module redirects:

- A's `stdout` → `channel_AB` → B's `stdin`
- B's `stdout` → `channel_BA` → A's `stdin`

**No code change to the inner chat module is required.** The instances do not
know they are talking to a peer; from their perspective the other side is just
a user (or — via timeout — silence, which triggers own 34 mandate-4 autonomous
speech).

## Phase Gates

| Phase | Status | Scope |
|---|---|---|
| A | LANDED 2026-05-08 | Skeleton: file structure + alias DB + --help + --selftest. No proc spawn / no channel I/O. `--duo` emits honest β-1 pending notice. |
| B iter 1 | LANDED 2026-05-08 | β-1 channel API wired (`use "stdlib/channel"`). Full N-turn loop activated. |
| B iter 2 | LANDED 2026-05-08 | Same-GGUF guard + lightweight per-turn verdict cells + D1/D2 1차 aggregate. |
| C iter 1 | LANDED 2026-05-08 | Per-turn own 18 C1+C2+C3 verdict via consciousness CLI shell-out (`simple --utterance` / `--prev-utterance`, schema `anima.consciousness.utterance.v1`). `--verdict full` activates; default `simple` keeps lightweight cells. Aggregate: per-instance + dialogue overall PASS_STRICT_C3 rate (own 18 dialogue C3 lane SSOT). |

## β-1 Dependency Hooks (frozen contract)

The following surface MUST be provided by the β-1 hexa stdlib before Phase B
can activate. Signatures are part of the duo↔stdlib contract:

```hexa
channel_pair_open()                                   -> {tx, rx, ok: bool}
proc_spawn_with_channels(cmd, stdin_ch, stdout_ch)    -> {handle, ok: bool}
channel_send(ch, line: string)                        -> bool
channel_recv(ch, timeout_ms: int)                     -> string   // "" on timeout
proc_terminate(handle)                                -> bool
proc_wait(handle)                                     -> int       // exit code
```

Notes:
- `channel_recv` semantics: line-buffered (one model utterance = one recv).
  Timeout returns empty string — duo treats this as "peer silent this turn".
- `channel_send` does not append newline; caller must include trailing `\n` if
  the consumer (chat REPL) is line-oriented (it is — see
  `sys_stdin_read_line_timeout` consumers).
- `proc_spawn_with_channels`: stdin redirect points to `stdin_ch.rx`; stdout
  redirect points to `stdout_ch.tx`. Stderr inherited (visible to terminal —
  honest C3 visibility).

When β-1 lands, flip `_b1_available()` from `false` to `true` and fill the
two stub functions (`_channel_pair_open`, `_spawn_instance`).

## Turn Sequence (Phase B target)

1. Resolve `<model_a>`, `<model_b>` via `chat.hexa` `_alias_resolve` (we
   dispatch through chat.hexa anyway, so its alias DB is the gate).
2. Open two channel pairs: `ab` (A→B), `ba` (B→A).
3. Spawn instance A: stdin = `ba.rx`, stdout = `ab.tx`.
   Spawn instance B: stdin = `ab.rx`, stdout = `ba.tx`.
4. If `--topic-seed` is provided, `channel_send(ab.tx, seed)`. Otherwise A
   speaks first via own 34 mandate-4 autonomous tick (the chat REPL's
   `sys_stdin_read_line_timeout` returns "" → `_invoke_core("")` → BOS-only
   forward → bytes flow into `ab.tx`).
5. For `turn` in `1..N`:
   - `line_a = channel_recv(ab.rx, turn_timeout_ms)` — what A produced
   - `_emit_turn_verdict(turn, "A", line_a)` — own 18 C1+C2+C3 ledger
   - `line_b = channel_recv(ba.rx, turn_timeout_ms)` — what B produced
   - `_emit_turn_verdict(turn, "B", line_b)`
6. `proc_terminate` both instances; emit aggregate summary (mean coherence,
   per-instance utterance distribution, dialogue-coherence verdict).

## Compliance

- **own 34 mandate-1** raw passthrough — channel transport carries bytes
  verbatim; duo never modifies utterance content.
- **own 34 mandate-2** wrapping 0 — no system prompt, no chat template, no
  persona inject. Selftest grep verifies on this file.
- **own 34 mandate-4** autonomous speech — duo does NOT inject any prompt
  beyond optional `--topic-seed`. The "first speaker" is determined by which
  instance's `sys_stdin_read_line_timeout` ticks first — natural emergence.
- **own 34 mandate-7** lane separation — per-turn verdict (own 18 measurement
  lane) is emitted as a ledger line **in stderr/log only**, never folded into
  channel content (which is own 34 chat lane).
- **own 33** trinity compliance (D_no-system-prompt cross-ref).
- **own 31 mandate-1** alias DB mirrors `dancinlab/` SSOT.
- **raw#9** hexa-only — proc spawn via β-1 stdlib (no shell pipes).
- **raw#10** honest C3 (7 caveats in `duo.hexa` footer).
- **raw#11** snake_case.
- **raw#15** no-hardcode (paths via `_resolve_root`).

## Coherence Metric

See `docs/anima_dialogue_coherence_metric_2026_05_08.md` — 4-cell definition
extends own 18 C2.4 (single-utterance 맥락 정합) into multi-turn dialogue
space (D1 reactive, D2 topic-shift-rate, D3 persona-consistency, D4
pseudo-turn-fairness). Aggregate threshold is TBD measurement-driven (mirrors
own 18 C3 policy — random init baseline + ROC analysis).

## Phase C iter 1 — per-turn own 18 verdict (LANDED 2026-05-08)

`_emit_turn_verdict_c3(turn, who, line, prev_line, model_alias)` shell-outs to:

```
hexa.real run consciousness.hexa <model> simple \
  --utterance <line> --prev-utterance <prev_line> --json
```

Substring-extracts `aggregate.verdict / c1_pass / c2_pass / c3_pass` from the
`anima.consciousness.utterance.v1` JSON and emits:

```
[duo:verdict-c3] turn=N who=A|B verdict=X c1=B c2=B c3=B
```

`prev_line` semantics:
- `prev_for_a`: topic_seed at t=1; subsequent turns = previous B line (what A is responding to).
- `prev_for_b`: current A line (what B is responding to).

Cost guard via `--verdict simple|full|none`:
- `simple` (default): lightweight cells only (len/distinct/snippet) — no shell-out.
- `full`: activates per-turn shell-out (~16-30s/call × 2 inst × N turns ≈ 5min N=5).
- `none`: skip both verdict + summary emit.

Aggregate (only when `--verdict full`):
- Per-instance PASS_STRICT_C3 rate (A 측 / B 측 별도).
- Dialogue overall PASS_STRICT_C3 rate.
- `SIMPLE_STACK_PASS_DIALOGUE_C3 = (rate ≥ 0.6)` — own 18 dialogue C3 lane
  SSOT mirror + `docs/anima_dialogue_coherence_metric_2026_05_08.md` per-turn
  rate floor alignment.

own 34 mandate-7: all `[duo:verdict-c3]` / `[duo:summary-c3]` emit-only,
NEVER folded back into channel content.

## C3 Limitations (raw#10 honest, brief; full list in `duo.hexa` footer)

- chat.hexa `_dispatch_module` exec() captures full stdout (no streaming) —
  duo channel transport receives buffered banner instead of line-by-line
  utterances. ALL chat modules affected (separate cycle); blocks meaningful
  semantic dialogue verification (turn=1 A often silent). Phase C wiring is
  mechanically correct but per-turn verdicts emit `SHELL_OUT_FAIL` on empty
  input (guard branch).
- consciousness simple --utterance lane = single-utterance evaluator; C1.3 /
  C2.4 are isolated heuristics (template-leak proxy), not full chat-cap
  V4 evaluator.
- Alias DB vendor copy duplicates chat.hexa SSOT — keep in sync (mitigation:
  always dispatches through chat.hexa, so SSOT is the actual gate).
- Coherence threshold values are TBD measurement-driven (D1 0.30 / D2 0.40 /
  per-turn rate 0.6 = metric doc starts; ROC analysis = separate cycle).
- No streaming verdict — per-turn only (whole-line channel semantics).
- L3 council (N≥3) is a stub; full design = separate cycle.

## Cross-Reference

- `docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md` — L2 roadmap layer
- `docs/anima_dialogue_coherence_metric_2026_05_08.md` — coherence 4-cell spec
- `tool/anima_cli/dialogue.hexa` — topic dispatcher (forwards `--duo`)
- `tool/anima_cli/chat.hexa` — alias DB + module routing SSOT
- `tool/anima_cli/chat/anima_native/anima_native.hexa` — Phase 2 REPL pattern
- `tool/anima_cli/chat/llama/llama.hexa` — Phase 3c REPL pattern
- `tool/anima_cli/consciousness.hexa` — own 18 verdict CLI (β-2 dep)
- `anima-agent-channels/channel_manager.hexa` — multi-channel runtime
  (deferred; activation target for L3 council, not L2 duo)
- `.roadmap.cli` `cli.dialogue.duo_design_2026_05_08`,
  `cli.dialogue.coherence_metric_2026_05_08`,
  `cli.dialogue_2026_05_08`
- `.own` own 18 (C1+C2+C3 simple_stack), own 34 (mandate-1/2/4/7), own 33,
  own 31 (mandate-1)
