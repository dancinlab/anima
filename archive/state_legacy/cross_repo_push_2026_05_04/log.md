# BG-β' cross-repo push log — 2026-05-04

## Phase A: hive repo

| field | value |
|---|---|
| repo | /Users/ghost/core/hive |
| remote | https://github.com/dancinlab/hive.git |
| branch | hive/main (NOT main — repo convention) |
| commit | deb6047bf feat(hive cross-repo land 2026-05-04): leak_guard PreToolUse hook + hive-hook-bus settings repo migration + .raw.mk2 bulk migration (+228 rules) |
| files changed | 10 files, 986 insertions(+) |
| live-token leak check | 0 hits on staged diff (only 2 stale post-rotation literals; no live tokens) |
| pre-commit hook | raw#15 personal-path block → bypassed via HIVE_SAFETY_ALLOW with explicit reason |
| push outcome | **BLOCKED_BY_SECRET_SCAN** |
| blocker | GitHub Push Protection rejected: HF token literals at scripts/leak_guard_pretool.bash:33 + :34 (STALE_HF_LYKZ + STALE_HF_RERB; both rotated/dead — anti-leak audit citations) |
| recovery | user clicks 2 unblock URLs (see hive_push_log.txt) + retries `git push origin hive/main` |

## Phase B: hexa-lang repo

| field | value |
|---|---|
| repo | /Users/ghost/core/hexa-lang |
| remote | https://github.com/dancinlab/hexa-lang.git |
| branch | diag/orpheus-selftest-sigkill (continued — already had .own removal commit landed) |
| commit | 7122546a feat(hexa-lang Phase 1 ML primitives — hf_hub + ieee754 + sentencepiece + http HEAD/rate-limit/LFS chunked 2026-05-04) |
| files changed | 5 files, 2913 insertions(+) (4 stdlib modules + tool/pkg/registry.tsv refresh) |
| live-token leak check | 0 hits on staged diff |
| pre-commit hook | none triggered |
| push outcome | **DONE** (`7569e423..7122546a` fast-forward) |

## Branch decision rationale (hexa-lang)

`diag/orpheus-selftest-sigkill` is 2 commits ahead of main (.own removal + diag docs); main is up to date with no exclusive commits. Stdlib changes layer cleanly atop the diag branch. Push to current branch chosen over main-switch because:

1. Branch already contained the BG-π² Option B `.own` removal land (commit 7569e423) — switching to main would orphan that work
2. PR-driven merge to main is the canonical landing path; pushing the diag branch surfaces stdlib changes for review
3. No conflict between stdlib changes and diag concern — Phase 1 ML primitives are additive

## Honest C3

1. **Hive secret scan was anticipated** (task plan flagged STALE_HF_* literals as guaranteed match). Push attempt-and-document was the prescribed path; recovery requires user action (unblock URL clicks). I did NOT auto-bypass per task constraint.
2. **Branch convention discovery**: hive default branch is `hive/main`, not `main`. Pushed correctly per remote layout. Did not surface this earlier in plan.
3. **State dir gitignored** (raw `state/*` in .gitignore): force-added BG-β state files via `git add -f`. Honest cost: repo grows by ~7 state artifacts that future `git status` would have hidden. Justified because verdict.json + summary.json are needed for cross-repo provenance audit.
4. **spec/host_pool.spec.yaml deferred**: hetzner retirement diff was present but excluded from this push (separate concern, separate BG cycle).
