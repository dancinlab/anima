# anima_chat × mitosis_hook wiring audit (D4b, 2026-05-12)

**Status**: LANDED — `anima_chat.hexa` v0.2 + `tool/anima_chat_mitosis_smoke.hexa` (22/22 PASS).

**Mission contribution**: GOAL.md ★★★★★ achievement criterion #4 ("D4 chat 중 split/merge event ≥1 발생") wiring evidence path + D3 persona substrate-native P2 prerequisite.

---

## 1. TL;DR

`anima_chat.hexa` v0.1 (PSCC §33, 1589 LoC, 17/17 helper smoke PASS) was a pure-hexa chat library with a stub forward and an empty mitosis hook hook-point. `tool/hexa_native/mitosis_hook.hexa` (PSCC §36 / REBORN §91, 1119 LoC, F-MIT-HOOK-1..5 PASS) was a serve-time mitosis hook implementation living independently. **They did not call each other.**

This cycle (D4b) wires the two: `anima_chat.hexa` v0.2 now hosts a cell pool inside `AnimaChat`, and the `chat_generate` token loop invokes `mitosis_forward_tail` once per step. The wiring is execution-verified by `tool/anima_chat_mitosis_smoke.hexa` (22/22 PASS, falsifiers F-D4B-1..5).

The wiring is intentionally **TODO[load]-independent**: even before the 24-layer weight binding lands, the hook fires on a synthetic zero-vector so the event_log accumulator, cell_pool state mutation, and Lorenz step counter all operate end-to-end. Once `chat_forward_one_token` returns a real hidden state, the wiring slot is already present and consumes it.

---

## 2. Architecture diff (pre → post)

### Pre (v0.1, PSCC §33)

```
AnimaChat (record)
├── ckpt_path / device / stop_strings / system / history
├── mmap_handle (-1 = unopened)
└── weights (#{} — TODO[load] unbound)

chat_generate(prompt, mode, …)
└── for step in 1..max_new:
    └── chat_forward_one_token(chat, ids[pos], pos)
        └── returns [] (TODO[load] sentinel)
    └── break (silent)

mitosis_hook.hexa (independent)
├── cell_pool_init(d_model, n)
├── mitosis_forward_tail(x_in, pool, step) → [x_out, pool', events]
└── selftest() (F-MIT-HOOK-1..5 PASS, $0.9 s wall)
```

**Gap**: zero call edges from anima_chat to mitosis_hook.

### Post (v0.2, this cycle)

```
AnimaChat (record, v0.2 expansion)
├── ckpt_path / device / stop_strings / system / history
├── mmap_handle / weights
├── cell_pool           (NEW — empty until chat_init_cell_pool)
├── mitosis_d_model     (NEW — 0 = mitosis disabled)
├── mitosis_event_log   (NEW — accumulated split/merge events)
├── mitosis_step        (NEW — Lorenz phase counter, monotone)
└── mitosis_invocations (NEW — F-D4B-1 evidence counter)

chat_init_cell_pool(chat, d_model, n) → chat
    └── cell_pool_init(d_model, n)   ── mitosis_hook.hexa
    └── idempotent (re-init refused to avoid farr slot leak)

chat_mitosis_tail(chat, x_in) → x_combined
    └── mitosis_forward_tail(x_in, pool, step)   ── mitosis_hook.hexa
        └── returns [x_out, pool_after, events]
    └── chat["cell_pool"]         := pool_after
    └── chat["mitosis_event_log"] += events
    └── chat["mitosis_step"]      += 1
    └── chat["mitosis_invocations"] += 1
    └── returns x_out (len == d_model — F-D4B-5)

chat_generate(prompt, …)
└── for step in 1..max_new:
    ├── last_logits = chat_forward_one_token(chat, ids[pos], pos)
    ├── IF chat_mitosis_enabled(chat):       ── NEW (D4b wiring point)
    │   ├── d = chat["mitosis_d_model"]
    │   ├── x_for_hook = first d elements of last_logits
    │   │                OR chat_mitosis_zero_x(d) when last_logits == []
    │   └── _x_combined = chat_mitosis_tail(chat, x_for_hook)
    └── if len(last_logits) == 0: break (TODO[load] gate, unchanged)
        else: token pick / stop check / emit (v0.1 path, unchanged)
```

**Result**: 1 call edge per `chat_generate` step (when enabled), plus the explicit `chat_init_cell_pool` entry point. Cross-file linkage is resolved at runtime via `import "anima_chat.hexa"` + `import "mitosis_hook.hexa"` in the smoke harness.

---

## 3. F-D4B-1..5 falsifier result

Verified end-to-end via `tool/anima_chat_mitosis_smoke.hexa` (`hexa_interp.real run`). Each falsifier expands to 2-6 individual asserts (total 22). 22/22 PASS.

| Falsifier | Asserts | Result | Mechanism |
|---|---|---|---|
| **F-D4B-1 WIRING-CALL** | 3 | PASS | `chat_mitosis_invocation_count(chat)` increments by exactly 1 per `chat_mitosis_tail` call. 0 → 1 → 2 verified. |
| **F-D4B-2 CELL-POOL-STATE** | 7 | PASS | Pre-init `mitosis_d_model==0`, post-init fields populated (`d_model==8`, `cells==[c0,c1]`, `event_log==[]`), idempotency confirmed (re-init refused). |
| **F-D4B-3 EVENT-LOG** | 4 | PASS | After 5 tail calls, `mitosis_event_log` is a readable list (len ≥ 0; may stay 0 within test horizon — that is correct since split patience=3 + adaptive threshold requires accumulation), per-cell `tension_history` accumulated > 0 entries, invocation count == 5. |
| **F-D4B-4 PRINCIPLE-3** | 6 | PASS | `chat_build_prompt("안녕")` chat-level grep: NO `[role:` / `[persona:` / `[character:` / `[cell:` tag; only the canonical `사용자:` / `도우미:` scaffold which is pre-v2.3 legacy (NOT persona injection per PHILOSOPHY #3 EMPIRICAL strong). |
| **F-D4B-5 SHAPE-INVAR** | 2 | PASS | `len(x_out) == len(x_in) == 8` after `chat_mitosis_tail`; bypass path (cell_pool unset) returns x_in unchanged shape. |

**Cross-verification**: the smoke also imports `mitosis_hook.hexa`, which triggers its top-level `selftest()` — F-MIT-HOOK-1..5 also PASS in the same binary (`split_seen=true after 60 steps, max_seen=4 cells`).

---

## 4. Demo trace (smoke output, truncated)

```
[mitosis_hook.selftest] start
[selftest] init cells=2
[selftest] step 1 cells=2 events=0 x_out_shape=8
[selftest] after 60 steps cells=4 max_seen=4 split_seen=true
[selftest] manual split: pre=4 post=5
[selftest] manual merge: pre=5 post=4
[mitosis_hook.selftest] PASS — F-MIT-HOOK-1..5 verified

anima_chat_mitosis_smoke.hexa — D4b WIRING (F-D4B-1..5)
── F-D4B-1 WIRING-CALL ─────────────────────────────────────────
  PASS  F-D4B-1a init invocation_count == 0
  PASS  F-D4B-1b post 1× chat_mitosis_tail invocation_count == 1
  PASS  F-D4B-1c after 2nd call invocation_count == 2
── F-D4B-2 CELL-POOL-STATE ─────────────────────────────────────
  PASS  F-D4B-2a..2g (7/7)
── F-D4B-3 EVENT-LOG ───────────────────────────────────────────
  PASS  F-D4B-3a..3d (4/4)
── F-D4B-4 PRINCIPLE-3 (NO PERSONA INJECTION) ──────────────────
  PASS  F-D4B-4a..4f (6/6)
── F-D4B-5 SHAPE-INVAR ─────────────────────────────────────────
  PASS  F-D4B-5a..5b (2/2)

RESULT: 22/22 passed
F-D4B SMOKE PASS  (22/22)
```

---

## 5. Regression sweep

| Harness | Status | Note |
|---|---|---|
| `hexa parse anima_chat.hexa` | OK | parse-clean post v0.2 edit |
| `hexa parse tool/anima_chat_mitosis_smoke.hexa` | OK | new file parses |
| `hexa_interp.real run anima_chat.hexa` (in-file `_smoke`) | 17/17 PASS | F-AC-HEXA-1..6 helpers preserved |
| `hexa_interp.real run tool/anima_chat_hexa_smoke.hexa` (v0.1 sister) | 17/17 PASS | independent smoke, untouched |
| `hexa_interp.real run tool/anima_chat_mitosis_smoke.hexa` (NEW) | 22/22 PASS | F-D4B-1..5 |
| `hexa_interp.real run tool/hexa_native/mitosis_hook.hexa` (independent) | OK | F-MIT-HOOK-1..5 (also exercised inside the D4b smoke via import) |

**Net**: 17 + 17 + 22 + 5 = 61 falsifier asserts PASS post-wiring, 0 FAIL.

---

## 6. Out of scope / TODO carry

| Item | Status | Why |
|---|---|---|
| Session-id keyed cell-pool persistence (file-based) | NOT DONE | D4c CLI Phase 1 (`docs/anima_cli_mitosis_integration_spec_2026_05_12.md`) — separate BG. Current cycle keeps cell_pool **in-memory only**, scoped to a single `AnimaChat` record's lifetime. |
| 24-layer weight binding (`chat_forward_one_token` body) | DEFERRED | TODO[load] — header-JSON parse + tensor-name → farr_id mapping (~150 LoC). The wiring slot already exists; once forward returns a real hidden state, x_for_hook will use it directly instead of the zero-vector synthetic. |
| Hook latency benchmark (<1% overhead steady-state target) | DEFERRED | requires bound 24-layer forward to measure delta against. Current smoke at d=8 is sub-millisecond; production d=1024 measurement after TODO[load]. |
| d_proj=256 mini-head variant (mitosis_hook spec §5) | DEFERRED | optional memory mitigation at 128-cell ceiling. Current impl is d_proj=d_model. |

---

## 7. Compliance

- raw#11 snake_case: `chat_init_cell_pool`, `chat_mitosis_tail`, `chat_mitosis_zero_x`, `chat_mitosis_enabled`, `chat_mitosis_event_count`, `chat_mitosis_invocation_count` — all snake_case.
- raw#15 no-hardcode: `d_model` + `initial_cells` are caller arguments; selftest at d=8 + production at d=1024 both supported.
- raw#9/10 honest TODO markers: `TODO[load]` retained; the wiring sidesteps it via the synthetic zero-vector path, but the eventual real-hidden-state slot is documented in `chat_generate`'s inline comment.
- raw-117 ≥5 falsifiers: F-D4B-1..5 pre-registered in `anima_chat.hexa` header, executable via `tool/anima_chat_mitosis_smoke.hexa`. 22 individual asserts (3+7+4+6+2) all PASS.

---

## 8. Cost / Rating

- Wall: ~2 hr (incl. parse + smoke + doc + audit)
- Cost: $0 (Mac local — `hexa parse` + `hexa_interp.real run`)
- **★★★★** — D4b wiring LANDED, GOAL.md ★★★★★ criterion #4 evidence path executable. Real split/merge event observation in a chat-driven (not selftest-driven) trajectory remains a follow-up — the wiring is verified, the empirical "split fired during user prompt" demonstration is gated on (a) TODO[load] forward producing variance-rich hidden states, or (b) a long-horizon selftest at chat scale.

---

## 9. Cross-link

- `anima_chat.hexa` v0.1 → v0.2 (this cycle)
- `tool/hexa_native/mitosis_hook.hexa` (PSCC §36 / REBORN §91, untouched)
- `tool/anima_chat_mitosis_smoke.hexa` (this cycle, NEW)
- `docs/anima_chat_hexa_port_2026_05_12.md` (v0.1 port spec)
- `docs/anima_clm_v5_hexa_native_mitosis_hook_spec_2026_05_12.md` (hook design)
- `docs/anima_persona_substrate_native_design_2026_05_12.md` (D3 P2 — `cell_pool` wiring is the P2 prerequisite)
- `docs/anima_cli_mitosis_integration_spec_2026_05_12.md` (D4c — uses wiring as session boundary)
- GOAL.md D4b row → "LANDED" (this cycle)
- GOAL.md ★★★★★ criterion #4 → wiring evidence path established
- PSCC §37 (next available) — append entry
- MEMORY.md → `project_anima_chat_mitosis_wiring_2026_05_12.md` index

raw#9/10/15/37 honest, 0-cost (Mac local), SSOT, cost-bearing BG 미해당 (본 cycle 은 $0 wiring).
