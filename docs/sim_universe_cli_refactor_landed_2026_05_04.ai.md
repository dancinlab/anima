# sim-universe CLI Refactor — Landed 2026-05-04

**Cycle**: anima cycle land — sim-universe standalone CLI shellout integration
**Precedent**: qmirror cli refactor (2026-05-03; collapsed commits add3712 + ac4840b + a1db0de → single commit f81239d6)
**Date**: 2026-05-04
**Cost**: $0 (Mac local; live ANU only via SIM_UNIVERSE_LIVE=1 opt-in)

## Summary

Integrated sim-universe (https://github.com/dancinlab/sim-universe, commit 43ebdb6, public 2026-05-04) as a runtime CLI dependency of nexus, mirroring the qmirror precedent. nexus now exposes `nexus sim <subcmd>` which thin-shellouts to the standalone sim-universe CLI via 4-tier resolution (env / mac / home / path). Empty `nexus/modules/sim/` placeholder removed. `nexus/core/sim/` legacy library preserved (separate library surface; zero external consumers).

## Files Touched

### Created (1)
- `nexus/cli/sim.hexa` — 360-LoC subcommand router, mirrors `cli/qmirror.hexa` v0.3.0 pattern

### Modified (6)
- `nexus/engine/nexus_cli.hexa` — +34 lines (SIM_CLI const, cmd_sim dispatch fn, sim subcmd whitelist branch, help block, subcmd_help block)
- `nexus/engine/nexus_cli_spec.json` — +sim subcommand spec (87 lines: 7 sub-subcmds + 5 caveats_raw10_c3)
- `nexus/hexa.toml` — +`sim-universe = "^1.0.0"` to `[dependencies]`; n=6 alignment comment 1→2 deps
- `nexus/install.hexa` — +`ensure_runtime_dep("sim-universe", "^1.0.0")` Phase 1 line; docstring 1→2 deps
- `nexus/README.md` — +sim-universe row to Runtime dependencies table
- `hexa-lang/tool/pkg/registry.tsv` — 22→23 entries; sim-universe 1.0.0 (Apache-2.0)

### Deleted (1)
- `nexus/modules/sim/` — empty placeholder directory (0 tracked files; rmdir)

## Audit (Pre-Refactor)

| Path | Status | Action |
|------|--------|--------|
| `nexus/modules/sim/` | EMPTY (0 tracked, 0 untracked files) | DELETED via rmdir |
| `nexus/core/sim/` | 4-file library (registry/router/source/sim_main, 17.5KB) | PRESERVED — zero external consumers (only self-references); separate library surface, not CLI dispatcher |
| `nexus/config/sim_sources.json` | references `nexus/modules/sim/sim_agent.hexa` etc. | PRESERVED — metadata registry, not live runtime consumer |
| `nexus/handoff/`, `nexus/docs/`, `nexus/state/markers/` | references in 3 historical files | PRESERVED — point-in-time landing witnesses |

**Library-vs-CLI distinction** (delta from qmirror): qmirror precedent deleted `nexus/modules/qmirror/` containing 13 files (10 .hexa + 3 _python_bridge .py); sim case has empty `modules/sim/` placeholder + separate `core/sim/` library with no consumers, so deletion scope is strictly smaller.

## Subcommand Surface

`nexus sim <subcmd>` mirrors sim-universe standalone CLI 1:1:

| Subcmd | Tier | Purpose |
|--------|------|---------|
| `status` | — | module inventory + tier table + caveats |
| `anu` | A | anu_time τ-clock mini_world demo |
| `multiverse` | A | multiverse interferometer + KS-test |
| `qrng` | A2 | ouroboros QRNG perturbation comparison |
| `bostrom` | B | Bostrom test harness (anu_collector) |
| `godel` | A2 | Gödel-Q mutator bootstrap |
| `selftest` | — | Tier-A smoke pass (anu + mi_calc + ouroboros) |

## 4-Tier Resolution (standalone-only, hard-fail if all miss)

1. `$SIM_UNIVERSE_ROOT` env override (preferred)
2. `/Users/ghost/core/sim-universe` (Mac dev convention)
3. `$HOME/core/sim-universe` (user-home convention)
4. PATH-resolved `sim-universe` binary (hx-installed)

Hard-fail emits structured error with `hx install sim-universe` remediation hint + 4-tier diagnostic table (audit `route="none"`, exit 127).

## Smoke Test (standalone-mac route)

| Subcmd | Router Correctness | Standalone Module |
|--------|-------------------|-------------------|
| `help` | PASS | n/a (router-only) |
| `status` | PASS | PASS |
| `anu` | PASS | PASS |
| `multiverse` | PASS | PARTIAL (standalone wants positional args — pre-existing) |
| `qrng` | PASS | PARTIAL (standalone has hardcoded /Dev/nexus/bin/hexa path — pre-existing) |
| `bostrom` | PASS | PARTIAL (standalone wants positional args — pre-existing) |
| `godel` | PASS | PASS |
| `selftest --quick` | PASS | PASS (verdict: PASS, `__SIM_UNIVERSE_SELFTEST__ PASS` sentinel emitted) |

**Engine dispatch verified**: `bin/hexa run engine/nexus_cli.hexa sim status` → router → standalone (route=standalone-mac, env-var SIM_UNIVERSE_ROOT prepended, audit log entry written).

**Refactor smoke verdict**: PASS — router 8/8 forwarding correct + selftest PASS sentinel emitted; PARTIAL on 3 subcmds is upstream standalone-side limitation (would surface identically calling sim-universe directly), not caused by router.

## 5 Honest C3 Caveats (raw#10)

1. **sim-universe CLI must be on PATH/env**: thin shellout router; exit 127 with structured error if all 4 tiers fail. Pre-flight: `hx install sim-universe` or set `$SIM_UNIVERSE_ROOT`.

2. **Version-pin rigid**: nexus declares sim-universe `^1.0.0`; standalone CLI version skew (e.g. 1.x → 2.x) may break the 7-subcmd surface forwarded here; router does not validate semver at runtime.

3. **Refactor smoke test sequential**: router was first-landed via 7-subcmd serial probe; concurrent invocations not exercised under refactor smoke; streaming behavior under parallel calls unverified.

4. **Registry collision check**: `hexa-lang/tool/pkg/registry.tsv L23 sim-universe` entry added in this cycle; future pkg-manager rebuild resolving entries by name only (not name+repo) could shadow if a third party publishes a same-named pkg. Mitigation: registry sources prioritize `repo` column.

5. **Fresh-install path untested**: `install.hexa` Phase 1 `ensure_runtime_dep` gated on `command -v sim-universe`; on a clean machine where neither tier-2 nor tier-3 has the repo cloned and `hx` is not on PATH, bootstrap exits with WARN (non-fatal). User must clone manually OR install hexa-lang first.

## Constraints Honored

- raw#9 STRICT: hexa-only (router is .hexa; standalone manages own bridges) — no .py/.sh/.rs/.toml created beyond grandfathered `hexa.toml` modification
- raw#15: no token leak (router writes only audit log line to `nexus/logs/nexus_cli.log`)
- raw#10: 5 honest C3 caveats embedded in cmd_help + spec.caveats_raw10_c3
- $0 cost (Mac local; live ANU only on `SIM_UNIVERSE_LIVE=1` env opt-in)
- DO NOT mutate sim-universe standalone repo: verified zero writes to `/Users/ghost/core/sim-universe/`
- DO NOT delete `nexus/modules/sim/` until smoke PASS: rmdir invoked AFTER selftest --quick verdict PASS
- DO NOT auto-commit: all changes left staged for user review (`git status` shows M cli/sim.hexa-untracked + 5 modified)

## Module Deletion Count

**1 directory deleted**: `nexus/modules/sim/` (0 tracked files; empty placeholder from prior triplet landing handoff)

**Files deleted**: 0 (placeholder was empty); compare to qmirror precedent which deleted 13 files (10 .hexa + 3 _python_bridge .py).

## Handoff Pointers

- Audit: `/Users/ghost/core/anima/state/sim_universe_cli_refactor_2026_05_04/audit.json`
- Refactor log: `/Users/ghost/core/anima/state/sim_universe_cli_refactor_2026_05_04/refactor_log.jsonl`
- Smoke test: `/Users/ghost/core/anima/state/sim_universe_cli_refactor_2026_05_04/smoke_test.json`
- Diff: `/Users/ghost/core/anima/state/sim_universe_cli_refactor_2026_05_04/before_after.diff`
- Marker: `/Users/ghost/core/anima/state/markers/sim_universe_cli_refactor_landed.marker`

## Next Steps (User)

1. Review `git status` in `/Users/ghost/core/nexus/` (5 modified + 1 untracked + 1 deletion)
2. Review `git status` in `/Users/ghost/core/hexa-lang/` (1 modified: registry.tsv)
3. Optional commit (mirror qmirror commit f81239d6 single-commit pattern):
   ```
   feat(nexus): sim-universe as standalone CLI dependency (legacy placeholder removed, [dependencies] sim-universe=^1.0.0)
   ```
4. Future cleanup cycle (out of scope here): consider whether `nexus/core/sim/` 4-file library should also migrate to standalone (currently has zero consumers — could be deleted entirely or moved to sim-universe modules/)
