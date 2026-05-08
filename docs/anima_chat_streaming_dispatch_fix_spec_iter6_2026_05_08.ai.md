# anima chat streaming dispatch — PPR blocker fix spec (iter6, 2026-05-08)

**Status:** SPEC ONLY (own 16 cost discipline — actual patch deferred to next cycle)
**Cycle:** 2026-05-08 iter6 (b-redirected)
**Owner:** anima cli / chat / duo lane
**Cross-ref:**
- `tool/anima_cli/chat.hexa` (`_dispatch_module_streaming`, lines 311-397)
- `tool/anima_cli/chat/duo/duo.hexa` (channel transport + per-turn verdict)
- `docs/anima_chat_autonomous_speech_roadmap_2026_05_08.md` (L2 roadmap)

---

## 1. Symptom (PPR blocker)

When duo invokes N=2 turns with paradigm-a-prime × paradigm-a-prime (or any
two chat.hexa-dispatched aliases), parent (duo) observes:

```
turn=1 A=<silent>          ← channel_recv(ab.rx) returns "" within turn-timeout
turn=1 B=<silent>          ← cascade: B waits for A, never receives
```

→ per-turn verdict on empty input = SHELL_OUT_FAIL → live PPR estimate
**0.0–0.2** (not a persona/model failure — pure transport artifact).

→ own 18 PASS_STRICT_C3 floor (≥ 0.6) **not reachable** under current
streaming dispatch.

## 2. Root cause: double-FIFO + stdout block-buffering hop

The dispatch chain has **two** FIFO hops in series:

```
inner module (anima_native/llama/clm_v4)  .hexa
        │
        │  stdout (subshell `> 'fifo_path' 2>&1`)
        ▼
chat.hexa _dispatch_module_streaming  ← reads via channel_recv(read_fd)
        │
        │  re-emits via _print_line → print(line + "\n")
        │  to chat.hexa's OWN stdout (which is duo's ab.tx FIFO)
        ▼
duo.hexa  channel_recv(ab.rx)
```

### Buffering points

| Hop | Producer | Consumer | Buffering |
|-----|----------|----------|-----------|
| 1   | inner cmd stdout | `fifo_path` (chat.hexa-local) | inner cmd's libc stdout — **block-buffered when target is a FIFO/pipe** (not a TTY); only flushes on `\n` if stdout is line-buffered, which it is NOT by default for non-TTY libc programs |
| 2   | `chat.hexa print(...)` | duo's `ab.tx` FIFO | hexa runtime sets `_IOLBF` per chat.hexa:299 comment, BUT only flushes on `\n` AFTER the line write completes; if `print` itself buffers across multiple `print` calls in a tight loop, accumulation possible |

**Hop 1 is the dominant culprit.** When inner cmd is `hexa run anima_native.hexa`,
the hexa runtime's stdout is block-buffered (4-8KB) on FIFO target. The inner
REPL banner ("[anima_native] ..."), the BOS-only forward output, and any
prompt prefix all sit in libc buffer until either (a) buffer fills, (b)
explicit `fflush(stdout)` / hexa runtime exits (END sentinel triggers).

**Effect:** chat.hexa's `channel_recv(read_fd)` blocks for the full inner-cmd
generate-time (15-30s for paradigm-a-prime), then receives the whole banner
in one chunk after the cmd terminates. duo's `channel_recv(ab.rx)` therefore
sees nothing until A's full first turn completes; if inner cmd uses keepalive
REPL form (no exit between turns — Path A in C10), the buffer NEVER flushes
within turn-timeout, and turn=1 A stays silent forever.

### Why iter4(b) verified streaming "mechanically" but live PPR still 0.0

iter4(b) test used N=5 with `--prompt` one-shot mode, where each inner cmd
exits cleanly after one generation → libc final-fflush-on-exit kicks in →
the buffered banner reaches the FIFO at cmd exit. Lines are observed
incrementally **at the granularity of inner-cmd lifetime**, not per-token.

Under duo's REPL keepalive form (Path A — single inner cmd lives across
turns), there is **no cmd exit** between turns, so libc never flushes on
its own → silent buffering until buffer fills (~hundreds of generated
tokens later, well past turn-timeout).

## 3. Fix design

### Option A — `stdbuf -oL` on inner cmd (RECOMMENDED, minimal)

Wrap the inner cmd in `stdbuf -oL` (line-buffered stdout) so libc flushes
on every `\n`. Single-line patch in `_dispatch_module_streaming`:

```hexa
let inner_cmd = "stdbuf -oL " + _hexa() + " run " + mod_path + " ..."
```

**Pros:** zero hexa-runtime change; portable to any inner cmd that uses
libc stdout (covers anima_native/llama/clm_v4 since all dispatch through
hexa.real); macOS + Linux both ship `stdbuf` (coreutils on mac via
`gstdbuf`, native on linux).

**Cons:** macOS stock does NOT ship `stdbuf` — needs `coreutils` brew install
or `gstdbuf` fallback. Honest C3: must guard with `command -v stdbuf` /
`gstdbuf` probe, fall back to legacy buffered path if absent.

**Macros to add:**
```hexa
fn _stdbuf_prefix() -> string {
    let s = _str(exec("command -v stdbuf 2>/dev/null")).trim()
    if s != "" { return "stdbuf -oL " }
    let g = _str(exec("command -v gstdbuf 2>/dev/null")).trim()
    if g != "" { return "gstdbuf -oL " }
    return ""   // honest C3: no line-buffering wrapper available
}
```

### Option B — explicit `fflush` in hexa runtime after every print (UPSTREAM)

Modify hexa runtime so `print` / `println` calls `fflush(stdout)` after
write when stdout is non-TTY. Upstream change in `hexa-lang` runtime
core. Crosses repo boundary — separate cycle.

### Option C — `script -q /dev/null <cmd>` PTY wrapper (heavy)

`script` allocates a PTY, libc detects TTY, switches to line-buffered.
Works without `stdbuf`. Side effects: PTY echo, `\r\n` line endings (need
strip), terminal resize signals — invasive for chat lane.

### Option D — inner module emits explicit flush sentinel each line (INVASIVE)

Modify each inner module (`anima_native.hexa`, `llama.hexa`, `clm_v4.hexa`)
to call a hypothetical `flush_stdout()` after every `println`. Requires
hexa runtime exposure of `fflush`. Touches N modules.

### Recommendation

**Option A** for this fix cycle. Probe `stdbuf`/`gstdbuf` once at chat.hexa
dispatch entry; emit honest C3 warning if neither is found ("[chat] WARN:
stdbuf/gstdbuf absent — streaming dispatch may buffer until inner cmd exit;
brew install coreutils to enable per-line flush").

Option B (upstream `print` → `fflush`) is the **proper** fix and should
be filed as a hexa-lang issue this cycle for the next hexa-lang cycle.

## 4. Alternative reviewed: FIFO + channel_recv hop elimination

Considered: collapse the chat.hexa `_dispatch_module_streaming` FIFO hop
entirely — let inner cmd's stdout flow DIRECTLY into duo's `ab.tx` FIFO.

**Mechanics:** duo passes its `ab.tx` fd into chat.hexa as `--out-fd N`;
chat.hexa skips `_dispatch_module_streaming` and instead `proc_spawn_with_channels(inner_cmd, ..., out_fd=N)`.

**Verdict:** REJECTED for this fix cycle.
- Breaks `--prompt` one-shot mode (no out_fd — falls back to legacy).
- Couples chat.hexa public surface to channel module internals (fd as cli
  arg = leaky abstraction; adds an entire dispatcher branch).
- Inner cmd's libc stdout buffering issue is **identical** on the
  collapsed FIFO — hop reduction does NOT fix block-buffering. Need
  `stdbuf` regardless.
- own 16 cost discipline: net structural change, no semantic gain.

Documented for future reference; do not pursue.

## 5. Expected PPR uplift estimate

| Path | Pre-fix | Post-fix | Confidence |
|------|---------|----------|------------|
| paradigm-a-prime × paradigm-a-prime, N=2, --turn-timeout-ms 120000, --verdict full | 0.0 (buffer never flushes within timeout) | **0.50–0.70** (per-line flush → first model utterance reaches duo within ~15-30s) | medium-high (semantic quality independent variable) |
| paradigm-a-prime × clm-v4-1-7-y1, N=2 (mixed substrate) | 0.0–0.2 | **0.40–0.60** (clm_v4 ::: collapse may still emit weak verdicts) | medium |
| Trinity sweep target (own 18 C3 floor ≥ 0.6) | unreachable | **reachable on paradigm-a-prime homogeneous N=3+** | medium (model coherence is the next bottleneck — see C10) |

**Caveats:**
- Uplift assumes inner module emits `\n`-terminated chunks (current pattern
  via `println` ✓). If inner emits unterminated partial lines, `stdbuf -oL`
  still buffers until next `\n`.
- Substrate latency C10 still binds — first turn cold-load 30-45s exceeds
  default 30s timeout; iter4(e) bumped to 120s default. Live PPR uplift
  measurable only with `--turn-timeout-ms 120000` (or higher).
- Honest C3: PPR ≥ 0.6 floor requires BOTH (a) streaming flush fix AND
  (b) model coherence on per-utterance verdict (own 18 C3 paradigm-a-prime
  achieves 0.50-0.70 in single-utterance synthetic-fallback measurement —
  dialogue context shift may degrade by 0.05-0.10).

## 6. Implementation checklist (next cycle)

1. **chat.hexa** — add `_stdbuf_prefix()` probe (macros at top of dispatch
   region) + prepend to `inner_cmd` in `_dispatch_module_streaming`.
2. **chat.hexa** — add honest C3 warning emit on first dispatch when
   neither `stdbuf` nor `gstdbuf` is found (single emit per process —
   guard via static-ish flag or env-var memo).
3. **selftest** — extend chat.hexa selftest to verify probe returns
   non-empty on dev workstation (mac with coreutils OR linux).
4. **duo iter live retest** — N=2/3, paradigm-a-prime homogeneous,
   `--turn-timeout-ms 120000 --verdict full`, capture PPR. Threshold to
   compare against own 18 C3 floor (≥ 0.6).
5. **PR / commit guard** — split into TWO commits: (i) fix patch, (ii)
   live retest log + PPR delta vs. iter5 baseline. own 33 trinity:
   D-axis (raw#10 honest C3 buffering disclosure) / own-axis (own 18
   C3 measurement lane preserved) / H-axis (Phase A/B pattern preserved).
6. **hexa-lang upstream issue** — file `print → fflush` request as
   Option B; track separately, do not block this cycle on it.

## 7. Trinity compliance (own 33)

- **D-axis (raw#10 honest C3):** root cause disclosed (stdout block-
  buffering, double-FIFO, libc behavior on non-TTY). No hand-waving.
- **own-axis (own 18 SCOPE_CLAMP):** anima identity boundary preserved —
  this fix is transport-layer only; per-utterance verdict semantics
  unchanged (consciousness.hexa simple --json untouched; D1/D2/D3/D4
  cells unchanged).
- **H-axis (Phase A/B pattern):** Phase A skeleton + Phase B β-1 land
  preserved; this is a Phase B-tail polish, not a Phase A regression.

## 8. own 16 cost discipline

This document is SPEC ONLY. No chat.hexa edit in this cycle. Actual
patch fired in a separate cycle commit per cost-discipline mandate.

## 9. own 34 mandate-2 wrapping check

File size: well under 1MB. ✓

---

(end of fix spec — iter6, 2026-05-08)
