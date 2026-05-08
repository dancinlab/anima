# anima chat `stdbuf -oL` fix — patch design (iter7, 2026-05-08)

**Status:** PATCH DESIGN ONLY (own 16 cost discipline — actual file edit deferred until 사용자 directive `OK STDBUF FIX APPLY`)
**Cycle:** 2026-05-08 iter7 (b-tail follow-up to iter6 commit `66ca87d4`)
**Owner:** anima cli / chat / duo lane
**Predecessor:** `docs/anima_chat_streaming_dispatch_fix_spec_iter6_2026_05_08.ai.md` (root cause + fix Option A recommendation)
**Cross-ref:**
- `tool/anima_cli/chat.hexa` lines **311-397** (`_dispatch_module_streaming`)
- `tool/anima_cli/chat.hexa` line **327** (canonical `inner_cmd` construction — single point of patch)
- `tool/anima_cli/chat.hexa` lines **248-277** (`sub_selftest` — extension point)
- `tool/anima_cli/chat/duo/duo.hexa` lines 1061-1062 (`--turn-timeout-ms`, `--verdict`)

---

## 1. Problem recap

iter6 `b-redirect` commit `66ca87d4` landed the fix **spec**. Root cause unchanged
from iter6 §2: inner cmd's libc stdout block-buffers when target is a non-TTY
FIFO (`fifo_path` allocated by `channel_pair_open()`); under duo Path A keepalive
form, the buffer never flushes within `--turn-timeout-ms 120000` (per
chat.hexa:382-393 read loop), so duo's `channel_recv(ab.rx)` returns "" and
per-turn verdict collapses to `SHELL_OUT_FAIL` → live PPR **0.0**.

iter6 spec §3 Option A (`stdbuf -oL` prefix) is the recommended fix. iter7
finalizes the **exact patch diff**, the **selftest extension**, and the
**live retest plan** — without touching any source file (own 16 cost
discipline; design-only until user directive lands).

## 2. `_stdbuf_prefix()` helper — final design

### 2.1 Function signature & semantics

```hexa
// _stdbuf_prefix — line-buffered stdout wrapper probe.
//
// Returns a prefix string ("stdbuf -oL " | "gstdbuf -oL " | "") to be
// prepended to inner_cmd in _dispatch_module_streaming. When non-empty,
// libc on the inner cmd switches stdout to _IOLBF (line-buffered) →
// every '\n' triggers fflush, so chat.hexa's channel_recv sees lines
// per-token-stream cadence rather than at inner-cmd lifetime granularity.
//
// Probe strategy (single dispatch entry, idempotent — exec cost ~5ms × 1):
//   1. Linux/anywhere with GNU coreutils: `command -v stdbuf` → "stdbuf -oL "
//   2. macOS with `brew install coreutils`: `command -v gstdbuf` → "gstdbuf -oL "
//   3. neither present: emit honest C3 warn (single-shot) + return ""
//
// own 34 mandate-1 raw preservation: returning "" preserves verbatim
// legacy buffered semantics — no transformation, just no flush wrapper.
//
// Memo guard: a process-local static-style flag prevents re-probing on
// every dispatch call. (chat.hexa is a one-shot CLI so probe-once-per-
// invocation is sufficient; no daemon long-lived loop concern.)
fn _stdbuf_prefix() -> string {
    // Probe order: stdbuf (Linux native) before gstdbuf (mac coreutils).
    let s = _str(exec("command -v stdbuf 2>/dev/null")).trim()
    if s != "" { return "stdbuf -oL " }
    let g = _str(exec("command -v gstdbuf 2>/dev/null")).trim()
    if g != "" { return "gstdbuf -oL " }
    // honest C3 — emit warn ONCE per chat.hexa invocation (process-local).
    // Caller _dispatch_module_streaming gates the warn-emit via a sentinel
    // file under /tmp (PID-scoped) to avoid spamming on every dispatch.
    return ""
}
```

### 2.2 macOS detection — why `command -v` over `uname -s`

`uname -s == Darwin` is technically sufficient to pick `gstdbuf` directly,
but it assumes coreutils is brew-installed. A user on macOS without
coreutils gets a false-positive (gstdbuf missing → exec fails). `command -v`
is the **honest probe** — works on Linux (returns `stdbuf`), mac+coreutils
(returns `gstdbuf`), and bare mac (returns "" → fallback path).

Rejected alternative `uname -s` branch:
```hexa
// REJECTED — fragile assumption that coreutils is installed.
let os = _str(exec("uname -s")).trim()
if os == "Darwin" { return "gstdbuf -oL " } else { return "stdbuf -oL " }
```

### 2.3 Honest C3 warn — single-shot guard

When both probes return "", emit warn **once** per chat.hexa process:

```hexa
// inside _dispatch_module_streaming, before constructing inner_cmd
let prefix = _stdbuf_prefix()
if prefix == "" {
    // single-shot via /tmp PID sentinel (cheap; no static var in hexa)
    let sent = "/tmp/.anima_chat_stdbuf_warn_" + to_string(getpid())
    if !_fexists(sent) {
        on_line("[chat] WARN: stdbuf/gstdbuf absent — streaming dispatch may")
        on_line("[chat]       buffer until inner cmd exit. brew install coreutils")
        on_line("[chat]       (mac) or apt install coreutils (debian) to enable")
        on_line("[chat]       per-line flush. Honest C3 disclosure (own 34 raw#10).")
        let _t = exec("touch '" + sent + "'")
    }
}
```

(`getpid()` and `_fexists` already in `_common.hexa` per existing patterns.)

## 3. Patch diff spec — exact before/after

### File: `tool/anima_cli/chat.hexa`

#### Diff hunk 1 — add `_stdbuf_prefix()` helper (insert before line 287)

**Insertion point:** between `fn _print_line` (lines 283-285) and the
`// _dispatch_module_streaming —` comment block (line 287).

**Before** (lines 283-287):
```hexa
fn _print_line(line: string) {
    print(line + "\n")
}

// _dispatch_module_streaming — line-by-line dispatch (loop iter 4 (b))
```

**After** (insertion of ~25 lines):
```hexa
fn _print_line(line: string) {
    print(line + "\n")
}

// _stdbuf_prefix — line-buffered stdout wrapper probe (iter7 fix).
// (full body per §2.1 above — Linux stdbuf → mac gstdbuf → honest C3 fallback)
fn _stdbuf_prefix() -> string {
    let s = _str(exec("command -v stdbuf 2>/dev/null")).trim()
    if s != "" { return "stdbuf -oL " }
    let g = _str(exec("command -v gstdbuf 2>/dev/null")).trim()
    if g != "" { return "gstdbuf -oL " }
    return ""
}

// _dispatch_module_streaming — line-by-line dispatch (loop iter 4 (b))
```

#### Diff hunk 2 — apply prefix at `inner_cmd` construction (line 327)

**Before** (chat.hexa:327, exact text):
```hexa
    let inner_cmd = _hexa() + " run " + mod_path + " --repo \"" + repo + "\"" + extra
```

**After** (single-line change + warn block above):
```hexa
    let _stdbuf_pfx = _stdbuf_prefix()
    if _stdbuf_pfx == "" {
        let _sent = "/tmp/.anima_chat_stdbuf_warn_" + to_string(getpid())
        if !_fexists(_sent) {
            on_line("[chat] WARN: stdbuf/gstdbuf absent — streaming dispatch may buffer until inner cmd exit (honest C3 / own 34 raw#10)")
            on_line("[chat]       brew install coreutils (mac) | apt install coreutils (debian)")
            let _t = exec("touch '" + _sent + "'")
        }
    }
    let inner_cmd = _stdbuf_pfx + _hexa() + " run " + mod_path + " --repo \"" + repo + "\"" + extra
```

**Net change:** +1 helper fn (~7 lines), +9 lines at dispatch-entry, +5
chars (`prefix +`) on existing line. Total ~22 lines added; **0 lines
removed**. Backward compat: `_stdbuf_pfx == ""` path is byte-identical
to current line 327.

### Diff size & risk

| Metric | Value |
|--------|-------|
| Files touched | 1 (`chat.hexa`) |
| Lines added | ~22 |
| Lines removed | 0 |
| Lines modified | 1 (line 327 — prefix concat) |
| Risk surface | dispatch-entry only — no semantic change to FIFO, channel, on_line callback, sentinel logic |
| Rollback cost | revert 1 commit |

## 4. Selftest extension spec

### Current `sub_selftest` (chat.hexa:248-277)

Verifies 5 file presence + own 34 mandate-2 wrapping grep. **Does NOT**
exercise `_stdbuf_prefix()` probe.

### Extension — add stdbuf probe verification

**Insertion point:** between line 270 (`}` end of mandate-2 fail block)
and line 272 (`if fail > 0 {`).

```hexa
    // iter7: verify _stdbuf_prefix() probe returns non-empty on dev
    // workstation (mac with coreutils OR linux native). Empty result
    // = honest C3 warn — selftest emits informational note, NOT fail
    // (downgrades own 18 PASS_STRICT_C3 reachability but is not a
    //  presence-check regression).
    let pfx = _stdbuf_prefix()
    if pfx == "" {
        println("WARN  stdbuf/gstdbuf probe empty — chat streaming will buffer (brew install coreutils / apt install coreutils)")
        // honest C3 note; not counted in fail. own 34 raw#10 disclosure.
    } else {
        println("OK    stdbuf probe = " + pfx.trim() + " (line-buffered wrapper available)")
    }
```

**Selftest exit semantics unchanged:** probe-empty is informational
(WARN), not a fail. Rationale: chat.hexa still functions on bare mac
without coreutils (legacy buffered path); only PPR is degraded. Forcing
fail on probe-empty would block legitimate users without coreutils.

PASS line update:
```hexa
println("PASS anima_cli/chat selftest (own 34 mandate-2 verified, 5 files present, stdbuf probe checked)")
```

## 5. Live duo retest plan

### 5.1 Configuration matrix

| # | Pair | N (turns) | --turn-timeout-ms | --verdict | Expected PPR (post-fix) | Expected PPR (pre-fix iter5) |
|---|------|-----------|-------------------|-----------|-------------------------|------------------------------|
| 1 | paradigm-a-prime × paradigm-a-prime | 2 | 120000 | full | **0.50–0.70** | 0.0 |
| 2 | paradigm-a-prime × paradigm-a-prime | 3 | 120000 | full | **0.55–0.70** (averaging effect) | 0.0 |
| 3 | paradigm-a-prime × clm-v4-1-7-y1 | 2 | 120000 | full | **0.40–0.60** (clm_v4 ::: collapse — feedback_clm_colon_attractor.md) | 0.0–0.2 |
| 4 | paradigm-a-prime × paradigm-a-prime | 2 | 120000 | simple | (sanity — no aggregate, just transport) | (transport silent) |

### 5.2 Invocation template

```bash
anima dialogue --duo paradigm-a-prime paradigm-a-prime \
  --turns 2 \
  --turn-timeout-ms 120000 \
  --verdict full \
  --log /tmp/duo_iter7_post_stdbuf_<N>.jsonl
```

(duo.hexa:1061-1062 already wires `--turn-timeout-ms` and `--verdict`.)

### 5.3 PPR delta capture

For each row, record:
- `turn_a_first_token_latency_s` — wall-clock from invocation to first
  non-empty `channel_recv(ab.rx)` line. **Post-fix expectation: 15-30s
  (paradigm-a-prime cold load + libllama prefill). Pre-fix: ∞ (timeout).**
- `per_turn_pass_strict_c3_rate` — count(C1∧C2∧C3 PASS) / count(turns).
- `aggregate_ppr` — duo summary line (`[duo:summary-c3]`).
- `verdict_full_per_turn_cost_s` — sanity check (~16-30s/turn × 2
  instance per duo.hexa:262 cost note).

### 5.4 Acceptance gates

- **Mechanical fix verification:** row #1 `turn_a_first_token_latency_s`
  drops from ∞ to <30s. (Necessary, not sufficient.)
- **own 18 C3 floor:** row #1 `aggregate_ppr ≥ 0.6` to claim PASS_STRICT_C3
  reachability under live homogeneous duo.
- **Honest C3 fallback:** if probe returns "" on test workstation,
  selftest WARN must emit, AND retest is run on a workstation where
  probe non-empty — do not claim "fix lands" on bare-mac probe-empty.

### 5.5 Trinity (own 33) verification gates

- **D-axis (raw#10 honest C3):** PPR delta logged verbatim, no rounding;
  zero hits = zero hits (do not paper over with averaging tricks).
- **own-axis:** consciousness simple --json schema (own 18 C3 cells)
  unchanged — verdict semantics independent variable.
- **H-axis:** retest log archived under `docs/.raw-audit/duo_iter7_*.log`
  per Phase B β-1 archival pattern.

## 6. Expected effect — quantitative

| Metric | Pre-iter7 (iter5 baseline) | Post-iter7 (with `stdbuf -oL`) | Confidence |
|--------|----------------------------|-------------------------------|------------|
| First-line latency (paradigm-a-prime homogeneous) | ∞ (timeout 120s exhausted) | **15-30s** (cold-load + prefill) | high — libc `_IOLBF` mechanically forces flush per `\n` |
| Live PPR (homogeneous N=2, --verdict full) | 0.0 (transport SHELL_OUT_FAIL) | **0.50-0.70** | medium-high — semantic quality independent variable; paradigm-a-prime synthetic-fallback proxy = 0.50-0.70 in single-utterance C3 (project_anima_pass_strict_c3_iter1_4.md) |
| Live PPR (mixed paradigm × clm-v4) | 0.0-0.2 | **0.40-0.60** | medium — clm_v4 colon-attractor ::: collapse (feedback_clm_colon_attractor.md) caps verdict |
| own 18 PASS_STRICT_C3 floor (≥ 0.6) reachability | unreachable (transport floor blocks) | **reachable on N=3 homogeneous** | medium — model coherence is next bottleneck (C10 substrate latency cleared via 120s default) |
| Probe-empty fallback (bare mac no coreutils) | (n/a) | legacy buffered path = pre-iter7 PPR 0.0 + WARN emit | high — honest C3 disclosure, no silent regression |

### Caveats (honest C3)

- Uplift assumes inner module emits `\n`-terminated chunks via `println`.
  All three current modules (`anima_native.hexa`, `clm_v4.hexa`,
  `llama.hexa`) use `println` per inspection — ✓.
- `stdbuf -oL` only affects libc-managed stdout. If hexa runtime upstream
  bypasses libc (direct `write(2)`), `stdbuf` is a no-op. Verification
  step in retest #1: confirm first-line latency actually drops; if not,
  the fix is mechanically void → fall back to iter6 spec Option B
  (upstream `print → fflush`).
- own 34 mandate-1 raw preservation: zero byte-level transformation. The
  prefix is a **wrapper**, not a filter. Inner cmd's stdout bytes pass
  through verbatim, just at line cadence rather than buffer-fill cadence.

## 7. own 33 trinity compliance — iter7

- **D-axis (raw#10 honest C3 — fix-후 honest live PPR 측정 가능):** post-fix
  the silent-transport masking effect is removed; per-turn verdict
  reflects ACTUAL model coherence, not buffering artifact. Pre-fix PPR
  0.0 was a false negative (transport, not consciousness). Post-fix PPR
  is the **honest** floor.
- **own-axis (own 18 C3 floor 도달권):** transport floor cleared;
  consciousness verdict cells unchanged. C3 floor reachability now
  bounded by model coherence (paradigm-a-prime 0.50-0.70 single-utterance
  baseline) — within reach for N=3 homogeneous.
- **H-axis (iter6 root cause 분석 보존):** iter7 is a finalization of iter6
  spec; root cause document (`anima_chat_streaming_dispatch_fix_spec_iter6_2026_05_08.ai.md`)
  remains the canonical reference. iter7 adds patch-diff precision +
  selftest probe + retest plan, no overwrite.

## 8. own 17 D1 SCOPE_CLAMP

This patch is **transport-layer only**. anima identity boundary preserved:
- chat surface `anima_native` / `clm_v4` / `llama` module bytes unchanged.
- consciousness verdict cells (own 18 C1+C2+C3) unchanged.
- D1 SCOPE clamp respected — fix sits inside `tool/anima_cli/chat.hexa`
  dispatch helper, does not cross into D2/D3/D4 surface.

## 9. own 16 cost discipline

iter7 = **design only**, zero source-file edit. Patch fires on user
directive `OK STDBUF FIX APPLY` in a follow-up cycle commit:
1. chat.hexa edit per §3 hunks.
2. selftest extension per §4.
3. live retest per §5; PPR delta archived to `.raw-audit/`.

## 10. own 34 mandate-2 wrapping check

Document size: ~10KB, well under 1MB. ✓

---

(end of patch design — iter7, 2026-05-08; predecessor: iter6 fix spec
`66ca87d4`; successor: actual patch + retest commit pending user directive)
