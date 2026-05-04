# nexus launchctl unload recipe — dev.hexa-lang.atlas-absorb-sweeper

**Owner**: BG-η plan-only deliverable, dual-SSoT EOL Phase 5a
**Status**: PLAN-ONLY ($0). DO NOT EXECUTE without user-ack gate.
**Date authored**: 2026-05-04
**Target**: `dev.hexa-lang.atlas-absorb-sweeper` launchd agent

---

## Context

This recipe is invoked as **Phase 5a** of the dual-SSoT EOL plan (sister BG-γ delivered the audit; BG-δ/ε/η produce execution recipes). It is a hard prerequisite for Phase 5c (nexus group A `.own` delete): if the `.own` is removed while the launchd plist is still loaded, the next `StartInterval=600s` tick will spawn `hexa run /Users/ghost/core/nexus/tool/atlas_absorb_sweeper.hexa` against a working tree where the rule no longer governs — silent semantic drift OR repeated EXEC errors with `LastExitStatus≠0` flooding `atlas-absorb-sweeper.err` log.

## Pre-flight gates (HARD, all must pass)

1. **G-PRE-1** — User-ack received: explicit ack tied to this recipe path.
2. **G-PRE-2** — n6 raw_archive snapshot already preserved per Phase 5b plan (sister doc `plan.md §4`). If 5b not done, halt; ordering matters because plist may be referenced by n6 hooks indirectly via `decl` audit chain.
3. **G-PRE-3** — Backup of plist body to anima archive (cmd in step 1).
4. **G-PRE-4** — `atlas_absorb_sweeper.jsonl` ledger checkpointed (cp to archive) so post-unload comparison is possible.
5. **G-PRE-5** — Confirm no in-flight ω-cycle ingest (grep last 5 min of `atlas-absorb-sweeper.log` for active `__ATLAS_ABSORB_SWEEP__` lines without matching PASS/FAIL).

## Step 0 — Capture pre-state evidence

```bash
# Snapshot launchctl current state
launchctl list dev.hexa-lang.atlas-absorb-sweeper \
  > /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/launchctl_list_pre_unload.txt

# Backup plist body (both source and registered locations)
cp -p /Users/ghost/core/nexus/launchd/dev.hexa-lang.atlas-absorb-sweeper.plist \
      /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/plist_source_backup.plist
cp -p /Users/ghost/Library/LaunchAgents/dev.hexa-lang.atlas-absorb-sweeper.plist \
      /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/plist_registered_backup.plist

# Snapshot ledger
cp -p /Users/ghost/core/nexus/state/atlas_absorb_sweeper.jsonl \
      /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/atlas_absorb_sweeper_pre_unload.jsonl

# Snapshot recent log tail (last 200 lines for post-unload comparison)
tail -200 /Users/ghost/.hx/log/atlas-absorb-sweeper.log \
  > /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/sweeper_log_pre_unload_tail.txt
tail -200 /Users/ghost/.hx/log/atlas-absorb-sweeper.err \
  > /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/sweeper_err_pre_unload_tail.txt
```

## Step 1 — Bootout (modern launchctl, macOS 12+)

The plist was bootstrapped originally with `launchctl bootstrap gui/$(id -u)`; the symmetric uninstall is `bootout`.

```bash
# Capture id for reproducibility
UID_HERE=$(id -u)
echo "uid=${UID_HERE}"

# Issue the bootout
launchctl bootout gui/${UID_HERE}/dev.hexa-lang.atlas-absorb-sweeper
echo "bootout_exit=$?"
```

**Expected**: `bootout_exit=0`. If non-zero:
- `5: Input/output error` → service not currently bootstrapped at this domain (check with `launchctl print gui/${UID_HERE}/dev.hexa-lang.atlas-absorb-sweeper`).
- `113: Could not find specified service` → already unloaded; treat as idempotent success.
- Any other non-zero → halt, do NOT proceed to plist removal.

### Legacy fallback (only if bootout fails on macOS 11 or earlier)

```bash
# Old-style unload (pre-macOS 12)
launchctl unload /Users/ghost/Library/LaunchAgents/dev.hexa-lang.atlas-absorb-sweeper.plist
```

## Step 2 — Verify unload (F-NEXUS-UNLOAD-1)

```bash
# Should produce no output
launchctl list | grep dev.hexa-lang.atlas-absorb-sweeper
GREP_EXIT=$?

# Falsifier check: exit code 1 (no match) is the PASS signal
if [ $GREP_EXIT -eq 1 ]; then
  echo "F-NEXUS-UNLOAD-1: PASS"
else
  echo "F-NEXUS-UNLOAD-1: FAIL — service still listed"
  exit 1
fi

# Belt-and-suspenders: print at full domain
launchctl print gui/${UID_HERE}/dev.hexa-lang.atlas-absorb-sweeper 2>&1 | head -5
# Expected: 'Could not find service "dev.hexa-lang.atlas-absorb-sweeper" in domain'
```

## Step 3 — Hold gate before plist removal

After F-NEXUS-UNLOAD-1 PASS, the plist FILE is still on disk at:
- `/Users/ghost/Library/LaunchAgents/dev.hexa-lang.atlas-absorb-sweeper.plist`
- `/Users/ghost/core/nexus/launchd/dev.hexa-lang.atlas-absorb-sweeper.plist`

DO NOT delete in this recipe. Plist removal is part of Phase 5c (nexus group A delete) which removes the entire `.own` rule including its `decl launchd/...plist` line — both unwire together.

## Step 4 — Post-unload monitoring window (≥30 min)

```bash
# Watch err log for any spurious post-unload activity (should be quiet)
tail -f /Users/ghost/.hx/log/atlas-absorb-sweeper.err &
TAIL_PID=$!

# Wait 30 min (1.5x StartInterval = 900s buffer beyond next-tick boundary)
sleep 1800

kill $TAIL_PID

# Compare pre vs post log file size — should be IDENTICAL (no new lines)
PRE=$(stat -f "%z" /Users/ghost/.hx/log/atlas-absorb-sweeper.log)
sleep 5
POST=$(stat -f "%z" /Users/ghost/.hx/log/atlas-absorb-sweeper.log)
if [ "$PRE" = "$POST" ]; then
  echo "log-size-stable: PASS (no post-unload ticks)"
else
  echo "log-size-stable: FAIL — sweeper still firing somehow (pre=$PRE post=$POST)"
fi
```

## Step 5 — DO NOT re-load

The plist is being **deprecated**, not paused. The dual-SSoT EOL absorbs nexus into hexa-lang substrate; the atlas-absorb mechanism is migrating to mk2 governance with its own enforcement chain. Re-loading would re-introduce the old enforcement on a `.own` that has been deleted in Phase 5c — this is exactly the failure mode this recipe exists to prevent.

If a regression-rollback is needed:
1. Restore `.own` from anima archive snapshot.
2. THEN restore plist via `launchctl bootstrap gui/$(id -u) <plist-path>`.
3. THEN `launchctl enable gui/$(id -u)/dev.hexa-lang.atlas-absorb-sweeper`.

Order is the inverse of unload.

## Rollback recipe (only if Phase 5a aborts mid-flight)

```bash
# If we issued bootout but then need to roll back (e.g., G-PRE-2 fails post-bootout)
launchctl bootstrap gui/$(id -u) /Users/ghost/Library/LaunchAgents/dev.hexa-lang.atlas-absorb-sweeper.plist
launchctl enable gui/$(id -u)/dev.hexa-lang.atlas-absorb-sweeper

# Verify re-load
launchctl list | grep dev.hexa-lang.atlas-absorb-sweeper
# Expected: line present, PID may be - until next StartInterval boundary
```

## Falsifier summary

| ID | claim | verify | pass-condition |
|----|-------|--------|----------------|
| F-NEXUS-UNLOAD-1 | bootout produced empty launchctl listing for label | `launchctl list \| grep -c dev.hexa-lang.atlas-absorb-sweeper` | output `0` |
| F-NEXUS-LOG-QUIET | no new log lines for 1800s post-unload | stat size pre vs post | `pre == post` byte size |
| F-NEXUS-ERR-CLEAN | no new err lines for 1800s post-unload | stat size pre vs post on .err | `pre == post` byte size |

## Honest C3

1. `launchctl bootout` semantics changed across macOS versions; macOS 13+ may emit warnings about deprecated subcommand forms even on success — parse exit code, not stderr text.
2. `LimitLoadToSessionType=Aqua` means service only loads in interactive GUI sessions; if executing this recipe over `ssh` (no Aqua session), `launchctl list` may not show the service even though it's bootstrapped — verify from a Terminal.app shell, not headless ssh.
3. The 30-min observation window assumes only one consumer chain (atlas_absorb_lint). If hidden consumers exist (e.g., a hive-agent that polls atlas-absorb-sweeper.jsonl), they may continue producing alerts — those are out of scope here but should be tracked separately.
4. `OnDemand=true` in launchctl-list output is launchd's internal default representation, NOT a contract to skip ticks; do not interpret it as "currently idle so skip unload".

## Out of scope

- Plist file deletion (Phase 5c)
- `.own` row removal (Phase 5c)
- chflags handling (Phase 5d separate)
- Hexa-lang substrate side absorption witness (Phase 5g)
