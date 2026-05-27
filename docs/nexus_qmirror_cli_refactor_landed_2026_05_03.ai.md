# nexus → qmirror standalone CLI refactor — LANDED 2026-05-03

**Marker**: `state/markers/nexus_qmirror_cli_refactor_landed.marker`
**Anima cycle**: 2026-05-03
**Constraints**: raw#9 (hexa-only Mac) · raw#15 (write-confined) · raw#10 (4 C3 caveats) · $0 (Mac local)

## Summary

User directive: `"nexus는 그럼 qmirror를 qmirror cli로 연결해서 쓰도록 처리하자"`
(translation: "nexus should connect to qmirror via the qmirror CLI")

Refactored `nexus/cli/qmirror.hexa` from a pure-local dispatcher (importing
in-tree modules at `$NEXUS/modules/qmirror/*.hexa`) into a thin pass-through
shellout to the standalone qmirror CLI. All 6 nexus qmirror subcmds now
delegate to `/Users/ghost/core/qmirror/cli/qmirror.hexa` (standalone, v1.0.0).

## Audit findings

Single in-code consumer in nexus that referenced `modules/qmirror/`:

| Path | Kind | Refactor action |
|------|------|-----------------|
| `nexus/cli/qmirror.hexa` | router | rewrite as shellout (this PR) |
| `nexus/engine/nexus_cli_spec.json` | spec doc | no change (descriptive only; dispatch still owned by router) |
| `nexus/test/test_qmirror_cli.hexa` | test | no change (CLI surface preserved) |
| `nexus/modules/qmirror/*.hexa` (13 files) | in-tree backend | RETAINED as DEPRECATED fallback (untouched) |
| `nexus/state/markers/qmirror_*.marker` | history | n/a (not consumers) |

Net: **1 file modified** (`nexus/cli/qmirror.hexa`).

## Refactor design — 5-tier resolution

```
nexus qmirror <subcmd> [flags]
  ↓
nexus/cli/qmirror.hexa::main → _forward(sub, extras)
  ↓
_resolve_qmirror_invocation():
  1. $QMIRROR_ROOT env                  → label "standalone-env"
  2. /Users/ghost/core/qmirror           → label "standalone-mac"
  3. $HOME/core/qmirror                  → label "standalone-home"
  4. PATH-resolved `qmirror` binary      → label "standalone-path"
  5. $NEXUS/modules/qmirror (DEPRECATED) → label "legacy-intree" + stderr WARN
  ↓
exec("[QMIRROR_ROOT=...] hexa run <cli-or-bin> <sub> <args>; echo __NEXUS_QMIRROR_RC__:$?")
  ↓
strip rc trailer + print to user; audit-log {route, exit_code, args}
```

The router preserves the nexus-side surface (subcmd whitelist, --help, --json,
--quiet, audit logging to `nexus/logs/nexus_cli.log` with new `route` +
`router_version` fields) while the standalone owns ALL subcmd logic, flag
parsing, and Python bridge management.

`router_version` bumped: `0.1.0` → `0.2.0`.

## Smoke tests — 6/6 PASS

All run via `cd nexus && hexa run cli/qmirror.hexa <sub>` after deploy.
Resolution route observed: `standalone-mac` for all 6.

| # | Subcmd | Args | Result | Evidence |
|---|--------|------|--------|----------|
| T1 | status | (none) | PASS | verdict PASS (8/8); 5 caveats from standalone surfaced |
| T2 | chsh | --json | PASS | `{"qmirror":"1.0.0","S_line":"S = 2.838","pass":true}` |
| T3 | nist | --bits=1000 --json | PASS | `F2 PASS n=5/5 max_amp_err=0; pass:true` |
| T4 | iit | --json | PASS | `F5 cond.6 reproduce all 4 systems byte-identical match; pass:true` |
| T5 | qrng | --bits=32 --json | PASS | `__QMIRROR_QRNG__ PASS; pass:true` |
| T6 | selftest | --json | PASS | `F1..F5 sweep PASS; cond table 8/8` |

Audit log entries (verified):

```
{"caller":"qmirror_router","subcmd":"qmirror iit","args":"--json","exit_code":0,"route":"standalone-mac","router_version":"0.2.0"}
{"caller":"qmirror_router","subcmd":"qmirror qrng","args":"--bits=32 --json","exit_code":0,"route":"standalone-mac","router_version":"0.2.0"}
{"caller":"qmirror_router","subcmd":"qmirror selftest","args":"--json","exit_code":0,"route":"standalone-mac","router_version":"0.2.0"}
```

## In-tree deprecation policy

`nexus/modules/qmirror/` (13 files) was **NOT** removed in this cycle.
Rationale:

1. Refactor smoke test is mock-only; real-QPU + live ANU edge cases unswept (caveat #3).
2. Standalone may be unreachable in some environments (CI sandbox, offline) — fallback preserves continuity.
3. Removal can land in a follow-up cycle once the standalone is `hx install`-published and PATH-resolvable everywhere.

Router emits a `stderr` WARN on every legacy-intree invocation, surfacing the
deprecation to operators without breaking them.

## C3 caveats (raw#10)

1. **Reachability**: qmirror standalone CLI must be at one of the 4
   resolution paths; if missing, router falls back to DEPRECATED in-tree
   modules with stderr WARN — silent failure mode if PATH/env unset and
   in-tree dir present (path #5 succeeds without operator intent).

2. **Version pinning**: router does NOT pin a qmirror version. Consumers
   depending on a specific qmirror schema/output should pin via
   `QMIRROR_ROOT=/path/to/specific/revision`.

3. **Refactor parity**: 6 subcmds verified PASS in **mock mode only**.
   Real-QPU vendors (`chsh --vendor=ionq` w/ API key), `qrng` live ANU
   (`NEXUS_QMIRROR_LIVE=1`), and exotic flag combinations not exhaustively
   swept — drift may surface in edge cases. File issue if observed.

4. **Sandboxed write fallback**: nexus repo write succeeded in this run
   (not sandboxed). For future runs where nexus is read-only, the refactored
   file is preserved at
   `state/nexus_qmirror_cli_refactor_2026_05_03/qmirror.hexa.after` for
   manual deployment via `cp ... → nexus/cli/qmirror.hexa`.

## Files

**Modified (live)**:
- `/Users/ghost/core/nexus/cli/qmirror.hexa` (668 → 405 lines; router_version 0.1.0 → 0.2.0)

**Created (state)**:
- `state/nexus_qmirror_cli_refactor_2026_05_03/audit.json`
- `state/nexus_qmirror_cli_refactor_2026_05_03/refactor_log.jsonl`
- `state/nexus_qmirror_cli_refactor_2026_05_03/before_after.diff` (854 lines)
- `state/nexus_qmirror_cli_refactor_2026_05_03/qmirror.hexa.before` (snapshot, 668 lines)
- `state/nexus_qmirror_cli_refactor_2026_05_03/qmirror.hexa.after` (snapshot, 405 lines)
- `state/nexus_qmirror_cli_refactor_2026_05_03/smoke/{01_status..06_selftest}.out`
- `state/markers/nexus_qmirror_cli_refactor_landed.marker`
- `docs/nexus_qmirror_cli_refactor_landed_2026_05_03.ai.md` (this file)

**Untouched (per constraint)**:
- `/Users/ghost/core/qmirror/**` (qmirror standalone — consumer-side refactor only)
- `/Users/ghost/core/nexus/modules/qmirror/**` (in-tree backend — DEPRECATED but retained)

## Next cycle hooks

- `hx install qmirror` publication + nexus router default-route to `standalone-path`
- Live mode parity sweep (real-QPU + live ANU) before hard-removing in-tree
- Migrate `NEXUS_QMIRROR_*` env vars → `QMIRROR_*` (sister cycle, deferred)
- Once standalone is universally reachable: physically remove
  `nexus/modules/qmirror/` and the `legacy-intree` branch from router
