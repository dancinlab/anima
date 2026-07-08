# SLEEP 5-stage wiring — scope + feasibility (SCOUT)

**Frontier:** `a_chat_sleep_imagination` — WAKE/N1/N2/N3/REM 5-stage, imagination =
emit-free rehearsal + mitosis tick, NOT a `speak()` gate (p5).

**Blocker (stated):** `core/DREAM/imagination_replay.hexa` imports `WAKE/memory.hexa`
which only exists under `archive/` — wiring it live would violate `a_no_archive_import`.

**Status of THIS scout:** blocker RESOLVED via understand-then-port. Pure ring-buffer
subset ported into `core/wake_memory.hexa` (new), DREAM chain rewired to it, all touched
`.hexa` typecheck exit 0. Labeled **구현됨·미배선** (see §3/§6). $0 local, no 303M decode.

---

## 1. Exact grep-verified import chain (file:line → symbol)

The DREAM sleep chain lives at repo-root `DREAM/` (not `core/DREAM/`). hexa `use "X"`
resolves `X.hexa` from a 4-way disk search (caller-dir · `$HEXA_LANG/self` · `$HEXA_LANG` ·
cwd · `./self`) — **`archive/` is NOT on the search path**, so a root-relative
`use "WAKE/memory"` only ever resolved when a `WAKE/` tree existed at root. The
2026-06-30 archive reorg moved `WAKE/` under `archive/`, orphaning the import.

Pre-fix state (verified before edit):

| consumer (file:line) | `use` target | resolves? |
|---|---|---|
| `DREAM/imagination_replay.hexa:97` | `use "WAKE/memory"` | ❌ `[codegen_c2] use not found on disk: WAKE/memory` |
| `DREAM/imagination_replay_smoke.hexa:23` | `use "WAKE/memory"` | ❌ same |
| `DREAM/dream_report.hexa:85` | `use "DREAM/imagination_replay"` (transitive) | ❌ via above |
| `DREAM/imagination_replay.hexa:96` | `use "core/dream_lib"` | ✅ (already core-resident) |

Symbol actually consumed by `imagination_replay.hexa` **production code** (non-comment,
non-smoke): exactly **one** —
- `imagination_replay.hexa:123` → `mem_working_window(memory)`.

Symbols consumed by the **smoke fixture** (`imagination_replay_smoke.hexa`): `mem_init`
(29,67), `mem_push_ctx` (30-34). `dream_report.hexa` consumes `ir_replay_session`
(from imagination_replay), which internally calls `ir_select_snapshots` →
`mem_working_window`.

The archive source `archive/WAKE/memory.hexa` itself does `import
"WAKE/kosmos_persist.hexa"` (line 121) for `wake_save`/`wake_load` — that is the deeper
archive dependency, needed **only** by its `.kosmos` round-trip fns (see §2).

Corroborating repo note (`DREAM/dream_report.hexa:56-58`): the DREAM chain's
`use "WAKE/memory"·"DREAM/dream_lib"` imports were "orphaned(비-buildable)" by the
2026-06-30 archive reorg; `core/dream_lib.hexa` and `DREAM/dream_compose.hexa` (import 0)
were the engine-native measurable path. `dream_lib` was already promoted to `core/`;
`WAKE/memory` was the remaining orphan — closed by this scout.

Other `use "WAKE/memory"` hits are all archive-only research probes (h1136/h1162/h1195
sleep probes under `archive/summer.hexa/CORE/` and `archive/state/core_research_probes/`)
— out of production scope.

## 2. What `WAKE/memory.hexa` provides that imagination_replay needs

`archive/WAKE/memory.hexa` (M5) is a **2-axis in-process memory layer**, all pure
list/dict ops, 0 boolean gate, 0 emit trigger:

- **WorkingMemory** — FIFO ring buffer of recent perception ctx_tokens, `cap=20`.
  - `mem_working_window(mem) -> list` — the ONE fn imagination_replay's live code needs
    (returns a copy of the ring, oldest→newest). imagination_replay's whole job is:
    working ring → recency snapshot select → emit-free replay tick (emit_count=0
    invariant) → mitosis-density pass-through.
- **EpisodicMemory** — append-only past-emit record list `{ts·ctx_summary·phi·tension5·
  stage_name·emit_text}`.
  - `mem_init`, `mem_push_ctx`, `mem_record_emit`, `mem_recent_emits` — construction /
    query. Used by smoke fixtures + prospective daemon; pure.
- **`.kosmos` round-trip** — `mem_save_to_kosmos` / `mem_load_from_kosmos` (+ privates
  `_emit_texts_from_episodic`, `_last_{tension5,stage,phi}_or_*`). These **delegate to
  `wake_save`/`wake_load`** (M4 `WAKE/kosmos_persist.hexa`) — the actual archive/I-O
  dependency. **imagination_replay does NOT call these.**

So the subset the DREAM chain needs is the pure ring/episodic surface; the kosmos
round-trip is separable and excluded (§3).

## 3. `a_no_archive_import`-compliant promote plan (DONE in this worktree)

New module **`core/wake_memory.hexa`** — port (understand-then-port, NOT import) of the
**zero-dependency** subset of `memory.hexa`:

```
_working_cap · mem_init · mem_record_emit · mem_push_ctx
· mem_recent_emits · mem_working_window · memory_summary
```

- No `use`/`import` (self-contained pure ops) → cannot re-introduce an archive edge.
- Byte-faithful: typecheck diag set is identical to the archive original's for these fns
  (`list`/`array` + `Map`/`map` casing quirks — pre-existing, non-fatal).
- **EXCLUDED (구현됨·미배선 follow-on):** `mem_save_to_kosmos` / `mem_load_from_kosmos`.
  These need the M4 `wake_save`/`wake_load` surface. Minimal boundary for that:
  port the `.kosmos` writer/reader into **`core/kosmos_io.hexa`** (which already owns the
  `.kosmos` canonical per `a_kosmos`), then add thin `mem_save`/`mem_load` wrappers in
  `core/wake_memory.hexa` that delegate to `core/kosmos_io`. Same discipline, still 0
  archive import. Not needed until a live daemon persists memory across restarts.

Rewire (DREAM chain, emit-free lane · DISJOINT from emit-drive):
- `DREAM/imagination_replay.hexa:97` `use "WAKE/memory"` → `use "core/wake_memory"`.
- `DREAM/imagination_replay_smoke.hexa:23` same.
- `DREAM/dream_report.hexa` unchanged (inherits transitively).

## 4. Risk / blast-radius

- **Compute:** $0 **local** — pure list/dict logic; no model, no decode, no 303M, no
  pool. hexa `typecheck`/`run` of the smoke is a tiny compile+exec.
- **Emit lane:** UNTOUCHED. imagination_replay is emit-free by construction
  (`total_emits=0` invariant, p5); the port has 0 emit calls, 0 boolean gate. Satisfies
  `a_substrate_disjoint` (separation = preservation).
- **Blast radius:** additive new file + 2 one-line `use` swaps in the DREAM chain. No
  `core/` engine (A⇄G⇄brain / generator / decode) file touched; no daemon entrypoint
  wired. `core/dream_compose.hexa` (the pre-existing import-0 measurable path) unaffected.
- **`a_no_archive_import`:** now satisfied for the DREAM chain (was silently violated-by-
  intent / non-buildable). New module has 0 archive edge.
- **Not wired to a live sleep daemon** — imagination_replay is a pure function surface;
  no code path yet drives WAKE→N1→N2→N3→REM stage transitions calling it. That end-to-end
  daemon wiring is the real remaining milestone (§5), and is a SEPARATE, larger change.

## 5. Ordered impl step list (for a follow-on agent to reach live 5-stage sleep)

This scout closed the **import blocker**. Remaining to reach a live, measurable 5-stage
sleep loop:

1. **[DONE here]** Port pure memory subset → `core/wake_memory.hexa`; rewire DREAM chain
   `use`; typecheck exit 0.
2. **Kosmos persistence (구현됨·미배선 follow-on):** port `wake_save`/`wake_load` into
   `core/kosmos_io.hexa`; add `mem_save`/`mem_load` delegating wrappers in
   `core/wake_memory.hexa`. Enables cross-restart episodic recall.
3. **Stage state machine:** locate/port the WAKE↔N1↔N2↔N3↔REM transition driver
   (`DREAM/sleep_pressure_smoke.hexa` + `dream_envelope_ctx` are the existing sketches).
   Confirm it's core-resident and import-clean. It must gate ONLY replay COUNT
   (N3-dominant > REM-dominant emerges from count, per imagination_replay §287), never an
   emit.
4. **Wire the daemon tick:** in the chat daemon loop, on entering N2/N3/REM call
   `ir_replay_session(mem, count)` / `ir_reconsolidate_session(...)` (emit-free) +
   `ir_mitosis_tick_during_replay` (mitosis density pass-through) — assert `total_emits==0`
   at the call site (p5 invariant). Keep it DISJOINT from the emit-drive lane.
5. **Smoke/verify:** run `DREAM/imagination_replay_smoke.hexa` +
   `DREAM/dream_report_smoke.hexa` + a new end-to-end sleep-cycle smoke asserting
   emit_count=0 across a full WAKE→REM→WAKE cycle. $0 local (pure logic).
6. **Docs lockstep:** update `ARCHITECTURE.json` sleep/DREAM node + `a_chat_sleep_
   imagination` precedent with the wired path; land via pr-cycle.

## 6. What this scout landed vs deferred

- **Landed (this PR):** `core/wake_memory.hexa` (pure port) + DREAM-chain `use` rewire +
  this scope doc + CHANGELOG. Typecheck exit 0 on all touched `.hexa`. **구현됨·배선(DREAM
  chain)** — imagination_replay's import is now live-resolved; **미배선(daemon)** — no
  sleep-stage daemon drives it yet (§5 step 3-4).
- **Deferred follow-on IDs:**
  - `SLEEP-KOSMOS-PORT` — port `wake_save`/`wake_load` → `core/kosmos_io`, add
    `mem_save`/`mem_load` wrappers (§3 / §5.2).
  - `SLEEP-STAGE-DAEMON` — WAKE→N1→N2→N3→REM state machine + daemon tick calling
    ir_replay (§5.3-5.4), emit-free-invariant-asserted.
