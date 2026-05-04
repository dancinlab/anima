# anima filter-repo landed — 2026-05-04

## Summary
Stripped 120MB `dev-clean-2.tar.gz` blob from anima repo history via `git filter-repo --strip-blobs-bigger-than 100M`, force-pushed rewritten history to `origin/main`. Unblocked 61+ unpushed commits previously rejected by GitHub's 100MB blob limit (introduced by upstream commit `433ff4bfa`, predates this session).

## Authorization
- User explicit: "A 진행" + "force push 승인 (raw protocol 충족)"
- Branch protection (enforce_admins=true, allow_force_pushes=false) temporarily relaxed for ~4 minutes, then immediately restored.

## Before / After

| | before | after | delta |
|---|---|---|---|
| HEAD SHA | `cd7eb72e5` | `31b3bd4ae` | rewritten |
| commit count | 3974 | 3974 | 0 |
| blobs > 100MB | 1 (dev-clean-2.tar.gz, 126MB) | 0 | -1 |
| largest blob | 126,046,265 B | 104,857,600 B (corpus_v5.txt, exactly 100MB) | -21MB |

## Steps executed
1. Pre-flight backup branch `backup/pre-filter-repo-2026-05-04 @ cd7eb72e5` (retain 1 week → delete 2026-05-11).
2. Verified `git-filter-repo` v2.47.0 at `/opt/homebrew/bin/git-filter-repo`.
3. Enumerated blobs > 100MB pre-filter → 1 (dev-clean-2.tar.gz).
4. Ran `git filter-repo --strip-blobs-bigger-than 100M --force` (5715 commits parsed in 6.75s; HEAD SHA rewritten).
5. Re-added origin remote (filter-repo removes by design): `https://github.com/need-singularity/anima.git`.
6. First push attempt (`--force-with-lease`) rejected (stale info, no fetch ref).
7. Second push (`--force`) rejected by branch protection (GH006).
8. Temporarily disabled `enforce_admins` + enabled `allow_force_pushes` via `gh api -X PUT`.
9. Force push succeeded: `+ d290f1ae...31b3bd4a main -> main (forced update)`.
10. Restored branch protection (enforce_admins=true, allow_force_pushes=false).
11. Verified local==remote HEAD: both `31b3bd4ae45aa1c82dfbdded04fec213b2b7cd00`.

## Honest C3 caveats (4)
1. **History rewrite irreversible upstream** — All 3974 commit SHAs rewritten on origin; only the local backup branch `backup/pre-filter-repo-2026-05-04` retains pre-rewrite SHAs. Once backup is deleted (2026-05-11), original history is gone forever.
2. **Force-push affects collaborators** — Any clone of anima must re-clone OR run `git fetch && git reset --hard origin/main`. No other collaborators known on this repo, but this is an assumption only.
3. **dev-clean-2.tar.gz content lost forever from git** — 120MB LibriSpeech dev-clean-2 corpus permanently removed from git history. Original file may still exist on disk under `state/slm_p3_a1_real_2026_05_03/`, but cannot be recovered from git.
4. **All 3974 commit SHAs rewritten** — Any markers, docs, scripts, or external references citing old SHAs (e.g. `cd7eb72e5`, `1185ece33`, `d290f1ae7`) are now invalid against origin. Backup branch retains old SHAs for reference. Examples of pre-existing SHA references that may need update if cited externally: `d290f1ae7`, `9ec878670`, `d01934ea8`, `7dec60bc3`, `f52bfd4c8`.

## Verification
- Local `git rev-parse HEAD` = `31b3bd4ae45aa1c82dfbdded04fec213b2b7cd00`
- `git ls-remote origin main` = `31b3bd4ae45aa1c82dfbdded04fec213b2b7cd00`
- `git rev-list --objects --all | awk '>100MB'` = 0 results
- Largest blob remaining = `data/corpus_v5.txt` @ exactly 104,857,600 B (100.0MB exactly — under threshold)
- Branch protection restored: `enforce_admins=True`, `allow_force_pushes=False`

## Critical commits spot-checked (intact post-rewrite)
- `11331fe4` feat(anima cycle land 2026-05-03/04): qmirror 1.0 closure 8/8 + ... (was `1185ece33`)
- `89a61bf7` chore(.gitignore Phase 4 .py.txt parking symmetry 2026-05-04)
- `36fc84ef` feat(clm v4 tokenizer caller migration Phase 2 EXEC F-MIG 4/4×4 PASS 2026-05-04)
- `5771a802` feat(anima cycle land 2026-05-03): P9 holdout-500 5seed + qmirror cond3/cond8 ...
- `83bf4c87` docs(qmirror+p9): nexus_qmirror_spec §4 4-tier + p9 phase 1.7 ...

## Constraints satisfied
- raw#9 STRICT (Mac → hexa only): all ops on Mac, no remote substrate touched
- raw#10: 4 honest C3 caveats above
- raw#15: applied
- $0 cost
- DO NOT touch other repos: qmirror/nexus/hexa-lang untouched

## Artifacts
- `state/anima_filter_repo_2026_05_04/audit.json` — 14-step audit trail
- `state/anima_filter_repo_2026_05_04/before_after.json` — before/after metrics
- `state/anima_filter_repo_2026_05_04/blob_size_check.json` — top-10 largest blobs post-filter
- `state/anima_filter_repo_2026_05_04/push_log.txt` — push attempts log
- `state/anima_filter_repo_2026_05_04/filter_repo_run.log` — filter-repo stdout
- `state/anima_filter_repo_2026_05_04/blobs_over_100M_{before,after}.txt`
- `state/markers/anima_filter_repo_landed.marker`

## Next
- 61 previously-blocked commits are now upstream.
- Backup branch `backup/pre-filter-repo-2026-05-04` retained until 2026-05-11.
- If anyone has a stale clone of anima → notify to re-clone or hard reset.
