# BG-η integrated plan — nexus launchctl unload + n6 raw_archive evidence preservation

**Owner**: BG-η, parallel non-overlap with BG-δ (`hexa_lang_gap_audit`) and BG-ε (`mk2_bulk_migration_spec`)
**Status**: PLAN-ONLY ($0). User-ack gate REQUIRED before any execution phase.
**Date**: 2026-05-04
**Phase**: 5a (launchctl unload) + 5b (n6 archive preservation) of 6-phase dual-SSoT EOL plan
**Compliance**: raw#9 (no .py on Mac) + raw#10 (no chflags / git mutations) + raw#15 (READ-ONLY survey)

---

## TL;DR

- **nexus plist load status**: `dev.hexa-lang.atlas-absorb-sweeper` is **CURRENTLY LOADED** (`launchctl list` returns row, `LastExitStatus=0`, PID=- means idle between ticks). StartInterval=600s, runs `hexa run /Users/ghost/core/nexus/tool/atlas_absorb_sweeper.hexa --once`.
- **n6 raw_archive count**: **11 files / 203,673 bytes / ~199 KB** under `/Users/ghost/core/n6-architecture/raw_archive/2026-05-04T/` — single dated snapshot directory, no other raw_archive paths exist on disk.
- **Critical finding overruling BG-γ assumption**: all 11 files are **already git-tracked + pushed** to private remote `need-singularity/n6-architecture` at commit `113725b0` ("chore(governance): predecessor scrub Phase 2 — declarative texts + raw_archive backup"). Preservation is therefore **redundant-tier**, not critical-tier. Anima archive copy is belt-and-suspenders, not last-line-of-defense.
- **Recommended preservation target**: `state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_snapshot/` via `cp -Rp` + sha256 manifest verification.
- **Top 2 risks for actual exec cycle**: (a) `launchctl bootout` may leave downstream `atlas_absorb_lint` orphan-detection scanner reporting false-positive orphans on new ω-cycle witnesses emitted post-unload until mk2 substitute is wired; (b) `cp -Rp` does not preserve macOS extended attributes (xattr `com.apple.metadata`) — sha256 of file content matches but xattr-level divergence is acceptable-but-not-bit-perfect.

---

## §1 — nexus launchctl plist analysis

### Plist file paths

| location | purpose | path |
|----------|---------|------|
| source-of-truth | nexus repo declares the plist body | `/Users/ghost/core/nexus/launchd/dev.hexa-lang.atlas-absorb-sweeper.plist` |
| registered | macOS LaunchAgents directory (where launchctl reads from) | `/Users/ghost/Library/LaunchAgents/dev.hexa-lang.atlas-absorb-sweeper.plist` |

Both files exist; install is per-user via `launchctl bootstrap gui/$(id -u)`. The two plist files were verified byte-equivalent in spirit (both list same Label, ProgramArguments, StartInterval).

### Current load state

`launchctl list` output (filtered):
```
-	0	dev.hexa-lang.atlas-absorb-sweeper
```

Decoded:
- Field 1 PID `-` = not currently running (idle between StartInterval ticks).
- Field 2 LastExitStatus `0` = last tick succeeded (no error).
- Field 3 Label `dev.hexa-lang.atlas-absorb-sweeper` = registered + active.

`launchctl list dev.hexa-lang.atlas-absorb-sweeper` confirms full state: `OnDemand=true` (launchd default flag, NOT user-on-demand), `LimitLoadToSessionType=Aqua` (interactive GUI sessions only).

### Target program + args

```
Program: /Users/ghost/.hx/bin/hexa
ProgramArguments: hexa run /Users/ghost/core/nexus/tool/atlas_absorb_sweeper.hexa --once
WorkingDirectory: /Users/ghost/core/nexus
StartInterval: 600 seconds (10 minutes)
RunAtLoad: true
ProcessType: Background
LowPriorityIO: true
Nice: 10
```

Environment includes `HEXA_RESOLVER_NO_REROUTE=1` (force Mac-local execution; avoids hexa shim auto-routing into Linux container). Logs to `~/.hx/log/atlas-absorb-sweeper.{log,err}`. Audit ledger at `/Users/ghost/core/nexus/state/atlas_absorb_sweeper.jsonl`.

### Wiring to .own

`/Users/ghost/core/nexus/.own` own #1 (slug `atlas-absorb-mandatory`) declares the plist:
```
decl tool/atlas_absorb_sweeper.hexa
decl tool/witness_emit.hexa
decl tool/atlas_absorb_lint.hexa
decl launchd/dev.hexa-lang.atlas-absorb-sweeper.plist
```

The `.own` rule is the policy SSOT; the plist is the OS-level enforcement layer (raw#94/95 triad: hive-agent + os-level + cli-lint). When the `.own` rule is removed in Phase 5c, the plist becomes orphaned policy — must unload first to prevent semantic drift (the sweeper would still run, ingesting witnesses against a defunct rule).

### Consumers of plist output

- `/Users/ghost/core/nexus/n6/atlas.n6` (main shard append target)
- `nexus/n6/atlas.append.<slug>.n6` (per-cycle shards)
- `tool/atlas_absorb_lint.hexa` (orphan-detection scanner — reads same artifacts)

---

## §2 — Unload sequence (recipe in `launchctl_unload_recipe.md`)

Detailed step-by-step in sister doc. Summary:

| step | command (representative) | falsifier |
|------|--------------------------|-----------|
| 0 — pre-state capture | backup plist + ledger + log tail to anima archive | files exist post-cp |
| 1 — bootout | `launchctl bootout gui/$(id -u)/dev.hexa-lang.atlas-absorb-sweeper` | exit 0 (or 113 idempotent) |
| 2 — verify unload | `launchctl list \| grep -c dev.hexa-lang.atlas-absorb-sweeper` | output `0` (F-NEXUS-UNLOAD-1) |
| 3 — hold gate | DO NOT delete plist file yet (Phase 5c removes both atomically) | n/a |
| 4 — post-unload watch (30 min) | tail err+log, expect zero new lines for 1.5×StartInterval | byte size pre==post |
| 5 — DO NOT re-load | rollback only via `launchctl bootstrap` if Phase 5a aborts mid-flight | n/a |

Falsifier **F-NEXUS-UNLOAD-1**: post `launchctl bootout`, the label is no longer in `launchctl list` output. Pass = grep -c returns `0`.

Pre-flight gates (G-PRE-1..5) include user-ack, n6 archive snapshot completion, plist body backup, ledger checkpoint, and no-in-flight-ingest verification. All five must pass before issuing the bootout.

---

## §3 — n6 raw_archive evidence inventory

Single archive directory found on disk:
- `/Users/ghost/core/n6-architecture/raw_archive/2026-05-04T/` (8 immediate children, 11 leaf files total)
- No `n6` repo at `/Users/ghost/core/n6` (path does not exist; only n6-architecture).

### File table (11 files, 203,673 bytes total)

| name | rel_path | size | sha256_first16 | tier | content hint |
|------|----------|-----:|----------------|------|--------------|
| .own.group_p.bak | `.own.group_p.bak` | 10,283 | 770b955da5428707 | redundant | mk1 paper governance pre-mk2 |
| .own.readme.bak | `.own.readme.bak` | 17,682 | c2d0d4392edef871 | redundant | mk1 README governance pre-mk2 |
| own_group_p_mk2_recon | `docs/...mk2_reconstruction_2026_05_03.ai.md.bak` | 15,630 | d4cf843fc78eee09 | redundant | mk2 reconstruction landed-doc |
| own_readme_mk2_recon | `docs/...mk2_reconstruction_2026_05_04.ai.md.bak` | 18,567 | 6184e5332de71a98 | redundant | mk2 reconstruction landed-doc |
| own21_drift_policy | `docs/...own21_drift_policy_2026_05_04.ai.md.bak` | 10,342 | 0cd4227c4bc6ffae | redundant | own21 drift-policy spec |
| raw47_propagation | `docs/...raw47_sister_repo_propagation_plan_2026_05_04.ai.md.bak` | 14,010 | fbe2da0350f35ace | redundant | raw#47 cross-repo propagation |
| self_mk2_tuning | `docs/...self_mk2_tuning_landed_2026_05_02.ai.md.bak` | 22,470 | 6c3b69bca61e510b | redundant | mk2 self-tuning landed |
| hexa-parallel-self | `domains/apps/hexa-parallel-self/hexa-parallel-self.md.bak` | 65,138 | 063f0626cad4874f | redundant | largest file, full app spec |
| sscb-mk1 | `papers/sscb-mk1-2026-05-04.md.bak` | 24,428 | 82d5fd5148310176 | redundant | sscb mk1 paper draft pre-mk2 |
| own15_legacy | `tool/own15_legacy_allowlist.json.bak` | 1,837 | 057d96c4846a72d3 | redundant | own15 legacy allowlist JSON |
| own29_lint | `tool/own29_multi_section_lint.hexa.bak` | 23,286 | 88991503098b907f | redundant | own29 lint tool hexa |

All 11 files share mtime `2026-05-04T13:28:17Z` (single atomic snapshot moment).

### Tier classification — REDUNDANT not CRITICAL

`git ls-files raw_archive/` in `/Users/ghost/core/n6-architecture` confirms ALL 11 files are git-tracked. `git remote -v` returns `https://github.com/need-singularity/n6-architecture.git`. `git status` is clean. `git log --oneline -5 raw_archive/` shows last commit `113725b0 chore(governance): predecessor scrub Phase 2 — declarative texts + raw_archive backup`.

Therefore: the local raw_archive is NOT the only witness. The private GitHub remote already contains a byte-equivalent copy. **BG-γ audit's "must archive BEFORE rm" remains good advice (defense-in-depth) but the criticality-tier downgrades from "irreversible if missed" to "convenient redundancy"**.

---

## §4 — Preservation strategy

### Target

`/Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_snapshot/`

The parent dir `state/dual_ssot_eol_archive/2026_05_04/` is the canonical anima-side EOL archive root (created by Phase 5b cycle; sister BGs use the same root).

### Method

```bash
# Create archive root + leaf
mkdir -p /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_snapshot

# Pre-cp manifest
( cd /Users/ghost/core/n6-architecture/raw_archive && \
  find . -type f | sort | xargs shasum -a 256 ) \
  > /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_manifest_pre.sha256

# Recursive copy preserving mtime + permissions
cp -Rp /Users/ghost/core/n6-architecture/raw_archive/. \
       /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_snapshot/

# Post-cp manifest
( cd /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_snapshot && \
  find . -type f | sort | xargs shasum -a 256 ) \
  > /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_manifest_post.sha256

# Falsifier F-N6-PRESERVE-1
diff /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_manifest_pre.sha256 \
     /Users/ghost/core/anima/state/dual_ssot_eol_archive/2026_05_04/n6_raw_archive_manifest_post.sha256
# Expected: empty diff, exit 0
```

### Verification

**F-N6-PRESERVE-1**: pre vs post sha256 manifest byte-identical (modulo path prefix; manifest computed relative-to so paths align). Pass = `diff` exit 0, no output.

### Falsifier coverage

| ID | claim | verify | pass |
|----|-------|--------|------|
| F-N6-PRESERVE-1 | sha256 manifests match between source + archive | `diff <pre> <post>` | exit 0 |
| F-N6-COUNT-1 | file count matches (11 expected) | `find ... -type f \| wc -l` on each side | both `11` |
| F-N6-SIZE-1 | total byte count matches (203,673 expected) | `find ... -type f -exec stat -f %z {} \; \| paste -sd+ - \| bc` | both `203673` |

---

## §5 — Combined recipe (Phase 5a + 5b of 6-phase plan)

### Phase ordering

```
Phase 5a (this plan §2 + launchctl_unload_recipe.md)
  └─> Phase 5b (this plan §4)
        └─> Phase 5c (sister plan: nexus group A .own delete)
              └─> Phase 5d (n6-architecture group B delete)
                    └─> Phase 5e (anima group C delete)
                          └─> Phase 5f (hexa-lang absorption witness emit)
                                └─> Phase 5g (sweeper transition to mk2 substitute)
```

Phases 5a + 5b are **independent of each other** but **both must complete** before Phase 5c. They can execute in parallel:
- 5a: launchctl bootout (idempotent, reversible via bootstrap)
- 5b: cp -Rp archive (additive, non-destructive — only creates new files)

Recommended order: **5b first, then 5a**, because:
1. 5b is fully non-destructive (just adds files in anima); zero risk window.
2. 5a is reversible but introduces an enforcement gap (sweeper stops firing); shorter gap is better.
3. 5b completing first gives a proven archive that reduces user concern about 5a's effect on n6 evidence chain.

### Recipe pseudo-script

```bash
# === Phase 5b: n6 archive preservation ===
# (commands from §4 above)

# === Phase 5a: launchctl unload ===
# (commands from launchctl_unload_recipe.md steps 0–4)

# === Phase 5c+ ===
# DEFERRED to sister BG plans (BG-δ / BG-ε / future BGs)
```

---

## §6 — Honest C3 (≥4 required, listing 5)

1. **launchctl bootout downstream effect**: The atlas-absorb-sweeper produces output that downstream `atlas_absorb_lint.hexa` orphan-detection scanner reads. Once the sweeper is unloaded, new ω-cycle witnesses emitted under `{nexus,n6-architecture,anima}/design/**/*omega_cycle*.json` will not be auto-absorbed. The lint scanner will then start reporting these as orphans (false-positive from its perspective; correct from new world). If mk2 substitute (per BG-γ Phase 5g plan) is not yet wired and operational by the time of bootout, there is an enforcement gap window during which new witnesses accumulate as un-absorbed. Mitigation: confirm mk2 substitute lifecycle before bootout, or accept the gap as part of the EOL transition with explicit documentation.

2. **Tier-classification dependency on git remote integrity**: The "redundant" tier for all 11 raw_archive files relies on need-singularity GitHub org remote remaining accessible. If org access is lost, force-push rewrites history, or the repo is deleted, the local copy was the only on-disk witness. The anima archive fork (Phase 5b) is the resilience layer that removes this dependency. This is why §5 recommends 5b run BEFORE 5a — it's the cheaper insurance step.

3. **cp -Rp does not preserve macOS extended attributes / chflags**: `ls -la` shows `@` suffix on permissions for all 11 archive files, indicating extended attributes are present (likely `com.apple.metadata` or quarantine flags). `cp -Rp` preserves POSIX mtime + mode but NOT xattr or chflags. Sha256 of file content matches; xattr divergence is acceptable for evidence purposes (content is what matters for audit) but the archive is not bit-for-bit identical at filesystem-metadata level. If full fidelity needed: use `cp -Rpc` (clone with metadata preservation, APFS-only) or `ditto` (Apple's preferred bit-perfect copy tool). Verified files have NO chflags uchg/uappnd flags currently set, so flag preservation is not a concern this cycle.

4. **sha256 manifest cross-platform brittleness**: macOS uses `/usr/bin/shasum -a 256` (Perl-based); Linux uses `sha256sum` (coreutils). Output format differs at trailing whitespace level. The verification recipe in §4 stays on macOS for both source + archive computation, so this is moot HERE — but if a future cycle compares manifests against a Linux backup site, normalization is required (e.g., `awk '{print $1}'` to extract just the hash column). Documented to prevent surprise.

5. **launchctl OnDemand=true semantic confusion**: `launchctl list dev.hexa-lang.atlas-absorb-sweeper` shows `"OnDemand" = true`. This is launchd's internal default representation indicating the agent is keepalive-managed by launchd; it does NOT mean "currently idle so safe to skip unload" or "user-triggered only". The plist body explicitly sets `StartInterval=600` + `RunAtLoad=true`, so cadence is timer-driven. Recipe must not interpret OnDemand=true as "ignore unload step".

---

## Out of scope (handled by sister BGs / later phases)

- Phase 5c: nexus group A `.own` row delete + plist file removal (sister BG)
- Phase 5d: n6-architecture group B `.own.*` files cleanup (sister BG-δ scope)
- Phase 5e: anima group C `.own` rule deletion (sister BG-ε / -γ scope)
- Phase 5f: hexa-lang absorption ω-cycle witness emit
- Phase 5g: mk2 substitute sweeper bootstrap (replaces atlas-absorb-sweeper)
- chflags handling on any file (separate scope; no chflags currently present on archive files)
- git operations (no commits, no pushes; BG-η is READ-ONLY plan-only)

## raw compliance attestation

- **raw#9** — no .py written; all deliverables are .md and .json under `state/`. No .py executed.
- **raw#10** — zero mutations: no chflags, no git operations, no launchctl bootout/bootstrap/enable/disable. All commands documented are PROPOSED for a later user-acked exec cycle.
- **raw#15** — no chflags writes attempted on any nexus or n6-architecture `.own` file.

## Deliverable manifest

| path | role | LoC est. |
|------|------|---------:|
| `state/nexus_n6_evidence_preservation_plan_2026_05_04/plan.md` | this integrated plan (Deliverable A) | ~300 |
| `state/nexus_n6_evidence_preservation_plan_2026_05_04/launchctl_unload_recipe.md` | Phase 5a step-by-step (Deliverable B) | ~150 |
| `state/nexus_n6_evidence_preservation_plan_2026_05_04/n6_archive_evidence_inventory.json` | machine-readable inventory + falsifiers (Deliverable C) | n/a (json) |

User-ack gate required before transitioning Phase 5a or 5b from PLAN to EXEC.
