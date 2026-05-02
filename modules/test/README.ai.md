---
schema: anima/modules/test/ai-native/1
last_updated: 2026-05-02
ssot:
  entry:    modules/test/hive_bridge_test.hexa
  contract: shared/config/contracts/hive_bridge.json
  audit:    shared/logs/hive_bridge.log
status: live — single-file hive bridge unit test; stub mode (hive offline)
roadmap_entry: 270
---

# anima test modules (AI-native)

Self-contained hive-bridge unit test. Verifies bridge module contract integrity with hive offline (stub mode) — exercises path resolution, PII gate, transport probe, error/ok response shapes, reverse path, graceful degrade, audit log append, and contract-JSON existence.

## TL;DR for an agent reading this cold

- **1 file**, 191 LOC: `hive_bridge_test.hexa`.
- 10 named subtests T1..T10 covering bridge surface end-to-end.
- All tests run with **hive offline** — verifies graceful-degrade path.
- Audit log: `shared/logs/hive_bridge.log` (append).
- Contract path: `shared/config/contracts/hive_bridge.json` (must exist for T10 PASS).

## Architecture map

```
modules/test/
└── hive_bridge_test.hexa     191 LOC — hive bridge unit test (stub mode)
```

10 subtests:

| ID  | Name                       | Verifies                                      |
|-----|----------------------------|-----------------------------------------------|
| T1  | path resolution            | BASE / AUDIT_LOG / CONTRACT path computation  |
| T2  | PII gate block (secret)    | bridge rejects messages containing secret     |
| T3  | PII gate pass (clean)      | bridge accepts clean message                  |
| T4  | transport probe (offline)  | probe returns "offline" without crashing      |
| T5  | err_response structure     | err shape is well-formed                      |
| T6  | ok_response structure      | ok shape is well-formed                       |
| T7  | reverse path stub response | reverse path returns valid stub               |
| T8  | graceful degrade           | ask() fails cleanly when hive absent          |
| T9  | audit log append           | log line appended to shared/logs/hive_bridge.log |
| T10 | contract JSON exists       | shared/config/contracts/hive_bridge.json exists |

## Public API

```hexa
// Whole-file driver — no exported fns
hexa run modules/test/hive_bridge_test.hexa

// Output
//   T1  PASS  path resolution
//   T2  PASS  PII gate block (secret)
//   ...
//   __HIVE_BRIDGE_TEST__ PASS|FAIL  passed=N/10 failed=...
//
// Exit codes
//   0  all 10 pass
//   1  any subtest fail
```

## Invocation patterns

```bash
# Run all 10 subtests
hexa run modules/test/hive_bridge_test.hexa

# Verify contract exists first (T10 prerequisite)
ls shared/config/contracts/hive_bridge.json
```

## Failure modes

- **T9 fail** = `shared/logs/hive_bridge.log` not writable (permissions / dir missing). Create dir + chmod.
- **T10 fail** = contract JSON missing. Required path: `shared/config/contracts/hive_bridge.json`.
- **T4 fail** = transport probe didn't return cleanly offline (regression — hive might be running, polluting test).
- **T8 fail** = ask() didn't degrade gracefully — bridge crashes when hive unreachable. Critical regression.
- **T2/T3 fail** = PII gate logic regression. Test fixture uses literal "secret" string.

## raw#10 caveats

1. **HOME-relative paths.** Test reads `$HOME/Dev/anima` — fails on hosts where the repo is at a different path. Should migrate to `--repo` arg.
2. **Stub mode only.** Live-hive integration test does NOT exist here. Verifying real hive transport requires `tool/hive_bridge_live_test.hexa` (not yet landed).
3. **PII gate fixture is "secret" literal.** Real PII (SSN / email / API key) shapes not exercised.
4. **No teardown of audit log.** T9 appends rows on every run — log grows unbounded. Recommended: rotate via cron.
5. **Single test file** — adding more bridges (e.g. nexus_bridge_test) requires new files; no test runner here.

## File index

| Path | sha256 | LOC |
|------|--------|-----|
| `hive_bridge_test.hexa` | `c6900a8f8634421424d63a1d77e6987017bffa1d2d83f76f1355c3fc76bd0280` | 191 |

shas pinned 2026-05-02.
