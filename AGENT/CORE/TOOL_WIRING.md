# AGENT role-tool wiring — safe-vs-effectful + env-gate

`exec_real_tool` (`AGENT/CORE/agent_loop.hexa`) routes a gated call frame to its
REAL role surface, by registry **kind**. The single registry is
`tool_registry_full()` (`AGENT/CORE/tool_call_grammar.hexa` §5), each entry shaped
`#{ tier, surface_fn, effectful, kind }`.

## Three-way dispatch

| kind | executor | when it fires |
|---|---|---|
| `toy` | `exec_toy_tool` | always (deterministic table lookup — `fact_lookup`/`mem_read`/`status`) |
| `safe` | `exec_safe_real_tool` | **NOW**, once the tier gate passes (read-only, no side effect) |
| `effect` | `exec_effectful_tool` | tier gate passes **AND** `ANIMA_TOOLS_EFFECTFUL=1` (default OFF) |
| `unknown` | — | honest `‹not wired›` stub (no fabrication) |

The **tier gate is `tool_gate.tool_allowed`**, applied by the loop *before*
`exec_real_tool` — there is **no 2nd gate**. The effectful env-arm is an
*additional* safety opt-in layered on top of the tier gate, not a replacement.

## Registry (tool · tier · effectful · wired)

| tool | tier | effectful | surface |
|---|---|---|---|
| `status` | T0 | no | toy: fixed liveness |
| `mem_read` | T0 | no | toy: fixed slot |
| `fact_lookup` | T1 | no | toy: unknowable table |
| `think` | T0 | no | safe: real reflection echo |
| `repo_status` | T0 | no | safe: real `git status --porcelain` |
| `web_search` | T1 | no | safe: real curl fetch OR honest no-network stub |
| `file_read` | T1 | no | safe: real disk read (`read_file`) |
| `grep` | T1 | no | safe: real `grep -rnI` |
| `market_scan` | T1 | no | safe: MERCHANT read-only descriptor |
| `file_write` | T2 | **yes** | effect: real `write_file` |
| `run_tests` / `code_run` | T2 | **yes** | effect: real `exec` shell cmd |
| `desktop_action` | T2 | **yes** | effect: DESKTOP `ax_*` route |
| `git_commit` | T3 | **yes** | effect: real `git commit` |
| `git_push` | T3 | **yes** | effect: real `git push` |
| `publish` | T3 | **yes** | effect: role surface (bind creds) |
| `merchant_order` | T3 | **yes** | effect: MERCHANT order surface (bind adapter) |
| `live_trade` | T3 | **yes** | effect: role surface (bind adapter) |

## Why effectful defaults SAFE

At wiring time the trained mouth binds call args incorrectly (grounding 0/36,
being fixed separately). An unsupervised destructive path on an unverified mouth
is unacceptable, so effectful tools **default OFF**:

```
# default — plumbing exists, fires nothing destructive
hexa run AGENT/CORE/agent_loop.hexa
#   file_write → "‹effectful tool gated: set ANIMA_TOOLS_EFFECTFUL=1 to enable›"

# armed — the real side-effecting surface fires (operator opt-in)
ANIMA_TOOLS_EFFECTFUL=1 hexa run AGENT/CORE/tool_wiring_armed_probe.hexa
#   file_write → "file_write OK: 19 bytes → /tmp/…"  (real write landed)
```

`effectful_armed()` reads `ANIMA_TOOLS_EFFECTFUL` **fresh per call** (no caching),
mirroring `AGENT/DESKTOP/action.hexa`'s `ANIMA_DESKTOP_DRYRUN` pattern.

## a_core_engine_map preserved

The role surfaces are invoked from `exec_real_tool` **inside** the grounded loop.
The tool RESULT re-enters the engine ONLY via the kosmos anchor
(`kosmos_write_tool_result` → `brain_emit(anchors)`); the CALL exits ONLY via the
generator L3 text slot. No 2nd `.clm` path, no 2nd anchor path is introduced.

## Honesty

- `web_search` with no network/curl → labelled `‹web_search unavailable…›`
  honest stub, **never** a fabricated search result (p5/p7).
- `file_read` of an absent/unreadable path → `‹file_read miss…›`, no fabrication.
- An unknown tool → `‹not wired›`, no silent T0 grant.
- An effectful tool with the env unset → `‹effectful tool gated…›`, no effect.

## Smoke

- `AGENT/CORE/tool_call_grammar.hexa` — unit smoke (grammar + registry tiers).
- `AGENT/CORE/agent_loop.hexa` — ⓑ grounded loop (no-regression) + ⓓ wiring
  (web_search route · file_write F1 gated / F3 tier-refusal · unknown not-wired).
- `AGENT/CORE/tool_wiring_armed_probe.hexa` — F2 effectful arm: default → no
  write; `ANIMA_TOOLS_EFFECTFUL=1` → real write landed (byte-verified).
