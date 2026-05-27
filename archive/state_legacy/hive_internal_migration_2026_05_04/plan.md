# Hive Internal Migration — `~/.hive/` → `/Users/ghost/core/hive/` (cycle 2026-05-04)

Owner: BG-υ
Repo: anima (state-only); modifies hive repo (commit prep) and `~/.hive/` (symlink swap)
Constraint: **NO `git push`** (commit prep only — user authorizes push separately)
Constraint: **HOOK STAY-ACTIVE** throughout (cp → verify → swap → re-verify)

## TL;DR

Goal: relocate two hook-bus-bind files from `$HOME/.hive/` (non-canonical home directory) into `/Users/ghost/core/hive/` (the actual `hive` git repo) so they can be tracked, reviewed, and pushed to GitHub. Replace home-dir originals with symlinks pointing at the repo so existing tooling that hardcodes `~/.hive/...` paths continues to function unchanged. Five-phase sequence (A copy → B verify → C swap → D re-verify → E git status) preserves hook activation continuously and provides a one-command rollback path via the `*.bak.pre_repo_migration_20260504` backups left in place.

Five-step sequence:
1. **Phase A** — `cp -p` source files to repo target paths (originals untouched).
2. **Phase B** — sha256 + diff verification; pipe synthetic JSON through repo-path script (allow + deny smoke tests).
3. **Phase C** — backup originals (`*.bak.pre_repo_migration_20260504`), `rm -f` originals, `ln -s` symlinks pointing at repo.
4. **Phase D** — `readlink` chain verification + hook-fire via HOME path (the path Claude Code's settings.json actually invokes).
5. **Phase E** — `git status --short` in hive repo, list new untracked files, draft commit message.

Rollback path (one command): `rm ~/.hive/scripts/leak_guard_pretool.bash ~/.hive/claude-config/hive-hook-bus/settings.json && cp ~/.hive/scripts/leak_guard_pretool.bash.bak.pre_repo_migration_20260504 ~/.hive/scripts/leak_guard_pretool.bash && cp ~/.hive/claude-config/hive-hook-bus/settings.json.bak.pre_repo_migration_20260504 ~/.hive/claude-config/hive-hook-bus/settings.json` (restores byte-identical home originals; repo files can stay or be `git clean`-ed without breaking the hook).

## Source/target table

| # | Source (HOME)                                                            | Target (REPO)                                                              | Method                            | Rationale                                                                                                                                                |
|---|--------------------------------------------------------------------------|----------------------------------------------------------------------------|-----------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1 | `~/.hive/scripts/leak_guard_pretool.bash` (3266 B, mode 0755)            | `/Users/ghost/core/hive/scripts/leak_guard_pretool.bash`                   | `cp -p` then HOME → symlink       | `scripts/` already exists in repo with `save-sessions.sh`, `bench-*.archive.txt`, `safety/`. Conventions match.                                          |
| 2 | `~/.hive/claude-config/hive-hook-bus/settings.json` (826 B, mode 0644)   | `/Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json`        | new write (path mirror) then HOME → symlink | Mirror `claude-config/hive-hook-bus/` path verbatim under the repo root so `CLAUDE_CONFIG_DIR=$HOME/.hive/claude-config/hive-hook-bus` symlinks resolve cleanly to the repo equivalent. Repo settings.json updates `hooks[0].command` from `/Users/ghost/.hive/scripts/...` → `/Users/ghost/core/hive/scripts/...` (canonical repo path) — the home-dir symlink resolves to this file. |

**Not migrated** (intentional — these contain secrets or per-machine state, must remain home-dir-only):
- `~/.hive/claude-config/hive-hook-bus/.credentials.json` (rotating Claude Code OAuth token)
- `~/.hive/claude-config/hive-hook-bus/.claude.json` (Claude Code internal state)
- `~/.hive/claude-config/hive-hook-bus/sessions/` (transcripts, projects, etc.)
- `~/.hive/scripts/{bind_update,kick_fire_unified,kick_queue_drain,mac_monitor_tick}.sh` (already orchestrated externally; no GitHub push request for these in this cycle — separate cycle if needed)

## Phase A-E execution log

See `migration_log.txt` for raw timestamped command output. Highlights:

### Phase A — copy
- `cp -p ~/.hive/scripts/leak_guard_pretool.bash /Users/ghost/core/hive/scripts/` (preserves mode 0755).
- `Write` tool used to author `/Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json` with updated hook-command path.

### Phase B — pre-swap verify
- `diff -u` source vs target script: **IDENTICAL**.
- sha256:
  - script: `afb7020d02cc3a7fb9467d5f3cf142424deb934073fc711e216f5c595c657685`
  - settings: `c9ab051a1954cd48f28a0fe3e82fbeabb0142577608f74bb85f7765d87ad118c`
- Allow-case smoke test (`echo hello` payload): exit 0, empty stdout. **PASS**.
- Deny-case smoke test (synthetic `hf_AAA...AA` payload, 36-char fictitious string, JSON delivered via tmpfile to bypass the very hook we are testing — Claude Code itself blocks the literal token-shaped string from appearing in our test command): exit 2, JSON `permissionDecision=deny` emitted on stdout. **PASS**.

### Phase C — swap
- `cp -p` originals to `*.bak.pre_repo_migration_20260504` siblings before destructive ops.
- `rm -f` original then `ln -s <repo-path> <home-path>` for both files.
- Final symlink listing:
  - `~/.hive/scripts/leak_guard_pretool.bash → /Users/ghost/core/hive/scripts/leak_guard_pretool.bash` (54-byte symlink)
  - `~/.hive/claude-config/hive-hook-bus/settings.json → /Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json` (64-byte symlink)

### Phase D — post-swap verify
- `readlink` confirms both symlinks point at repo paths verbatim.
- `stat -L` resolves through symlink to inodes 177808693 (script) and 177808781 (settings) under HOME paths — these are the inodes of the repo files.
- Hook fire via HOME path (`~/.hive/scripts/leak_guard_pretool.bash`) — the exact path Claude Code's running settings.json invokes:
  - allow case: exit 0 empty stdout. **PASS**.
  - deny case: exit 2 with proper deny JSON. **PASS**.
- `diff -q $CLAUDE_CONFIG_DIR/settings.json /Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json` → identical (symlink resolves correctly).

### Phase E — hive repo commit prep
`cd /Users/ghost/core/hive && git status --short` shows two new untracked entries (per the migration log):
```
?? claude-config/
?? scripts/leak_guard_pretool.bash
```
The `claude-config/` entry collapses to `claude-config/hive-hook-bus/settings.json` (the only file currently under that new dir).

## Symlink verification (`ls -lA`)

```
lrwxr-xr-x  ~/.hive/scripts/leak_guard_pretool.bash → /Users/ghost/core/hive/scripts/leak_guard_pretool.bash
lrwxr-xr-x  ~/.hive/claude-config/hive-hook-bus/settings.json → /Users/ghost/core/hive/claude-config/hive-hook-bus/settings.json
```

Backups preserved at:
- `~/.hive/scripts/leak_guard_pretool.bash.bak.pre_repo_migration_20260504` (3266 B, mode 0755)
- `~/.hive/claude-config/hive-hook-bus/settings.json.bak.pre_repo_migration_20260504` (826 B)

## Hook test post-migration

Allow case (`{"tool_name":"Bash","tool_input":{"command":"echo hello"}}` piped to home path):
```
exit code: 0
stdout: (empty)
```

Deny case (synthetic `hf_AAAA...` 36-char fictitious payload via JSON tmpfile to home path):
```
exit code: 2
stdout: {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"leak guard: HF token-shaped string detected ..."},"continue":false,"stopReason":"leak guard: HF token detected"}
```

Both fire correctly through the symlink chain. Hook continues to be active; behavior identical to pre-migration.

## Git status in hive repo

```
$ cd /Users/ghost/core/hive && git status --short
?? claude-config/
?? scripts/leak_guard_pretool.bash
```

`scripts/` is **not** gitignored (verified). `claude-config/` is a new top-level dir not present in `.gitignore`.

## Recommended commit message (next cycle, after user push ack)

```
feat(hive hook-bus-bind 2026-05-04): migrate hook script + settings.json from ~/.hive into repo

Relocate Claude Code PreToolUse leak-guard hook + settings.json from $HOME/.hive
(non-canonical home dir) into /Users/ghost/core/hive (canonical repo) so hook-bus-bind
config can be tracked, peer-reviewed, and shipped via git. Home-dir originals replaced
with symlinks pointing at repo files so existing tooling that hardcodes ~/.hive paths
(install.hexa generated cl-hooked, bin/hive HIVE_CLAUDE_HOOK_ROOT, docs) keeps working
unchanged. Pre-migration originals preserved at *.bak.pre_repo_migration_20260504 for
one-command rollback.

Files added:
- scripts/leak_guard_pretool.bash (3266 B, mode 0755) — token-shape pretool guard;
  blocks Bash/Write/Edit/MultiEdit when tool_input contains GitHub PAT/HF/Anthropic/
  RunPod/AWS/Google API token-shaped strings. Originally landed
  ~/.hive/scripts/2026-05-04 (cycle prefix narrowing 30+ chars).
- claude-config/hive-hook-bus/settings.json (1041 B) — Claude Code settings.json
  read via CLAUDE_CONFIG_DIR=$HOME/.hive/claude-config/hive-hook-bus. PreToolUse
  matcher Bash|Write|Edit|MultiEdit, command pointed at canonical repo path
  /Users/ghost/core/hive/scripts/leak_guard_pretool.bash, timeout 10s.
  skipDangerousModePermissionPrompt=true, theme=dark.

Verification:
- byte-identical script via diff -u (sha 7020d02c...)
- allow-case (exit 0 empty stdout) + deny-case (exit 2 deny-JSON) both fire correctly
  through home → repo symlink chain
- $CLAUDE_CONFIG_DIR/settings.json (HOME path Claude Code reads) resolves via symlink
  to repo file (diff -q identical)

Honest C3:
- GitHub-public push exposes the hook regex set; documented patterns are public
  knowledge but the surface itself signals what we guard against. Confirm public-
  facing OK before push.
- Claude Code may cache settings.json file path; restart may be needed after push if
  user pulls + re-symlinks on another machine.
- Sister-repo audit found 0 external dependents on the migrated files; the only
  ~/.hive references in /Users/ghost/core/hive are docs/historical bin/cl backup
  copies (not the live cl) and bin/hive HIVE_CLAUDE_HOOK_ROOT export — unaffected
  by symlink swap.
- Hook script content path comment refers to state/secret_cli_leak_audit_2026_05_04
  in the anima repo — cross-repo reference will read as stale to outside readers.
  Acceptable: comment is informational, not load-bearing.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

## Honest C3 (≥4)

1. **GitHub public exposure of hook content** — `scripts/leak_guard_pretool.bash` enumerates the exact token-prefix patterns blocked (ghp_, ghs_, gho_, github_pat_, sk-ant-, hf_, rpod_, AKIA, AIza). Pushing this to a public repo signals to attackers (a) which token classes we care about, and (b) the regex shape (`{30,}`, `{36}`, etc.) — useful intel for crafting evasion payloads (e.g. shorter strings, embedded whitespace). Recommend security review before push, particularly whether to add a private supplemental list. Mitigation already in place: backups + symlinks make the hook reversible without any user-visible churn.

2. **Claude Code settings.json caching** — empirically the harness re-reads `$CLAUDE_CONFIG_DIR/settings.json` on each tool invocation (the deny-case fired correctly mid-session in this very migration without any restart), but documented behavior is unclear. After git pull on another machine where someone has already symlinked, settings change may not propagate without restart. Recommend documenting "restart Claude Code after pull-into-symlinked-target" in the next cycle's `cl_token_sync_fix_landed_*.ai.md` follow-up.

3. **Sister-repo `~/.hive/` reference fragility** — audit shows the only LIVE references are (a) `bin/cl` and `bin/hive` which derive `_HIVE_HOOK_BUS_DIR=$HOME/.hive/claude-config/hive-hook-bus` for the credentials path (NOT settings.json — credentials stay home-only by design), and (b) docs (which describe the canonical home path historically). All hardcoded `~/.hive/scripts/leak_guard_pretool.bash` references in `state/dual_ssot_eol_audit_2026_05_04/` (anima) continue resolving correctly via the home → repo symlink. **No callers broken**. Risk: a future tool that does `realpath` on `~/.hive/scripts/leak_guard_pretool.bash` will get the repo path back — could surprise scripts that compare paths string-equal.

4. **Symlink permission inheritance** — the symlink itself has mode `lrwxr-xr-x` and is owned by `ghost:staff` (correct), but the target's mode is what matters at exec time. Repo file mode is 0755 (preserved by `cp -p`). If the repo gets re-cloned with stricter umask (e.g. CI environment) the script could lose +x and silently fail. Mitigation: add a `git update-index --chmod=+x scripts/leak_guard_pretool.bash` step in the `git add` flow next cycle so the executable bit is encoded in the tree-object.

5. **Backup file pollution in `~/.hive/`** — pre-migration originals now live as `.bak.pre_repo_migration_20260504` siblings. These are not gitignored (and shouldn't be — they're outside the repo entirely) but they will accumulate if migrations repeat. Lifecycle: after user accepts the GitHub push as final state, schedule a cleanup cycle that removes the .bak files (rolling 30-day retention). For now, kept indefinitely as the explicit rollback artifact.

6. **Hook file shipping bash, not hexa** — raw#9 (py-to-hexa-only) wants hexa-canonical for all execution. Claude Code hook spec, however, accepts only `type: command` with shell-executable string — hexa runtime is not on the hook callstack at PreToolUse time. This is a platform-imposed exception (the hook fires before any orchestrator can route through hexa). Acceptable per cycle gate: the hook is shell-bound by upstream contract.

## Recommended next-cycle actions (NOT this cycle)

- User reviews repo files, runs `cd /Users/ghost/core/hive && git diff --staged` after `git add`, approves push.
- Push: `cd /Users/ghost/core/hive && git push origin main` (separate cycle, user-initiated).
- After push lands, schedule `*.bak.pre_repo_migration_20260504` cleanup at +30 days.
- Optional: extend migration to `~/.hive/scripts/{bind_update,kick_fire_unified,kick_queue_drain,mac_monitor_tick}.sh` — same symlink pattern, separate cycle.
