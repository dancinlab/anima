# nexus qmirror legacy-intree fallback removed (router v0.3.0)

**Date**: 2026-05-04 (anima cycle, sister BG to add3712 qmirror standalone migration)
**Operator directive**: "qmirror 리포의 cli 로 가져다 써야됨" — nexus must use ONLY standalone qmirror CLI, not in-tree fallback.
**Cycle dir**: `state/nexus_qmirror_legacy_removed_2026_05_03/`
**Marker**: `state/markers/nexus_qmirror_legacy_removed_landed.marker` (to be created)

## Summary

- `nexus/cli/qmirror.hexa` v0.2.0 → v0.3.0
- 5-tier resolution → 4-tier (standalone-only)
- 5th tier `legacy-intree` ($NEXUS/modules/qmirror) **REMOVED** from `_resolve_qmirror_invocation()`
- In-tree module directory `nexus/modules/qmirror/` **deleted** (15 files, git rm)
- 6 smoke tests **PASS** post-deletion via `route=standalone-mac` → `/Users/ghost/core/qmirror` (qmirror v1.0.0)

## Why

The v0.2.0 5th tier was a silent fallback that masked operator intent — if the standalone CLI was missing/misconfigured, the router would silently dispatch to deprecated in-tree modules with only a stderr WARN. This violated the operator directive and meant fresh installs could pass smoke tests against stale in-tree code instead of the canonical standalone (need-singularity/qmirror).

After v0.3.0, missing standalone → hard fail (exit 127) with structured error message listing all 4 attempted tiers + remediation steps.

## Files modified

- `nexus/cli/qmirror.hexa` — 405 lines → 375 lines (-30)
  - Removed: `let LEGACY_QMIR_DIR`, `fn _dir_exists`, `fn _legacy_module_for`, the entire `if route == "legacy-intree"` branch in `_forward` (~32 lines), 5th-tier check in resolution function
  - Added: CHANGELOG comment block, structured 4-tier error message in `none` branch, 4 new C3 caveats reflecting deletion semantics

## Files deleted (git rm -rf modules/qmirror)

15 files (3 .py runners + 12 .hexa modules):

```
modules/qmirror/_python_bridge/aer_runner.py
modules/qmirror/_python_bridge/iit_mip_runner.py
modules/qmirror/_python_bridge/phi_runner.py
modules/qmirror/_python_bridge/process_tomography_runner.py
modules/qmirror/chsh.hexa
modules/qmirror/circuit.hexa
modules/qmirror/engine_aer.hexa
modules/qmirror/entropy.hexa
modules/qmirror/iit_mip.hexa
modules/qmirror/phi.hexa
modules/qmirror/process_tomography.hexa
modules/qmirror/qrng.hexa
modules/qmirror/sampler.hexa
modules/qmirror/selftest.hexa
modules/qmirror/tomography.hexa
```

**Discrepancy from spec**: spec said 13 files; actual was 15. Difference = `process_tomography.hexa` + `process_tomography_runner.py` (added in a sister cycle between spec authorship and execution). All deleted, no exception preserved.

**Recovery path** (if ever needed): `git log --diff-filter=D -- 'modules/qmirror/*'` then `git checkout <sha>~1 -- modules/qmirror/`.

## 4-tier resolution (v0.3.0)

```
1. $QMIRROR_ROOT env                      → standalone-env
2. /Users/ghost/core/qmirror              → standalone-mac
3. $HOME/core/qmirror                     → standalone-home
4. PATH `qmirror` binary                  → standalone-path
(no fallback — hard fail with exit 127)
```

Audit log `route` enum:
- before: `{ standalone-env, standalone-mac, standalone-home, standalone-path, legacy-intree, none, rejected }`
- after: `{ standalone-env, standalone-mac, standalone-home, standalone-path, none, rejected }`

## Smoke test results (post-deletion)

| # | subcmd | args | exit | route | verdict |
|---|--------|------|------|-------|---------|
| 1 | qrng | --bits=16 --json | 0 | standalone-mac | PASS |
| 2 | chsh | --vendor=sim --json | 0 | standalone-mac | PASS (S=2.838, 13.2σ over 2.0) |
| 3 | nist | --bits=10000 --json | 0 | standalone-mac | PASS (F2 5/5) |
| 4 | iit | --n-qubits=4 --json | 0 | standalone-mac | PASS (F5 4/4 byte-match) |
| 5 | selftest | --json | 0 | standalone-mac | PASS (8/8 cond) |
| 6 | status | --json | 0 | standalone-mac | PASS (8/8 cond) |

Audit log evidence: see `state/nexus_qmirror_legacy_removed_2026_05_03/smoke_test.json`.

## Caveats (raw#10 C3, 4 honest)

1. **Deletion irreversibility**: in-tree modules removed on disk. Recovery requires git history checkout (`git log --diff-filter=D` + `git checkout <sha>~1`). No on-disk fallback remains.
2. **Fresh-install dependency**: a clean nexus install (or any environment where qmirror is not reachable via the 4 tiers) will hard-fail with exit 127. Pre-flight requires `hx install qmirror` or `$QMIRROR_ROOT` set to a need-singularity/qmirror checkout.
3. **Hard-fail not silent**: when all 4 tiers fail, the router exits 127 with a structured error message. Any caller that previously relied on the v0.2.0 silent in-tree fallback will now surface the failure loudly. This is intentional per operator directive.
4. **Audit log enum change**: the `route` field no longer emits `legacy-intree`. Log-parsing consumers (dashboards, alerting, BLM/TLM/SLM normalization scripts) must update enum schemas.

## Constraints honored

- **raw#9 STRICT** (Mac → hexa only): no .py created; only edited .hexa router + git rm of pre-existing files.
- **raw#15** (write-confined): edits limited to `nexus/cli/qmirror.hexa` + `nexus/modules/qmirror/` (delete) + `anima/state/nexus_qmirror_legacy_removed_2026_05_03/` + `anima/docs/`.
- **raw#10**: 4 honest C3 caveats embedded in `cmd_help()` and audit.json.
- **$0**: Mac local; standalone qmirror at `/Users/ghost/core/qmirror` consumed read-only.
- **standalone qmirror repo**: UNTOUCHED (only invoked via `standalone-mac` route).

## Artifacts

- `state/nexus_qmirror_legacy_removed_2026_05_03/qmirror.hexa.before` — v0.2.0 snapshot (405 lines)
- `state/nexus_qmirror_legacy_removed_2026_05_03/qmirror.hexa.after` — v0.3.0 snapshot (375 lines)
- `state/nexus_qmirror_legacy_removed_2026_05_03/before_after.diff` — unified diff (215 lines)
- `state/nexus_qmirror_legacy_removed_2026_05_03/audit.json` — change manifest
- `state/nexus_qmirror_legacy_removed_2026_05_03/smoke_test.json` — 6/6 PASS evidence
- `state/nexus_qmirror_legacy_removed_2026_05_03/deleted_files_list.txt` — 15 deleted files
- `nexus/cli/qmirror.hexa` v0.3.0 (in-place; nexus repo not yet committed)
- `nexus/modules/qmirror/` — DELETED (git rm; not yet committed)

## Handoff next steps

1. **Commit nexus repo changes**: `cd /Users/ghost/core/nexus && git add cli/qmirror.hexa && git commit -m "refactor(qmirror cli): v0.2.0 → v0.3.0 — remove legacy-intree fallback, delete in-tree modules"` (operator gating: this is a destructive deletion, recommend explicit confirm).
2. **Update any external log-parsing tooling** that filters on `route=legacy-intree` (now never emitted).
3. **Update install docs/onboarding**: any guide that says "nexus qmirror works out of the box" must now add a prerequisite step (install standalone qmirror, or set $QMIRROR_ROOT).
4. **Sister cycle**: consider QMIRROR_* vs NEXUS_QMIRROR_* env var alias migration (noted in qmirror standalone selftest caveat #5).
