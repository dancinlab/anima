# anima HF Cycle 2 cleanup auto-fire prep landed (2026-05-05)

BG: BG-HF-CLEANUP-AUTOFIRE-PREP — verify + master script, no destructive ops, no commit.

## What landed

- `state/anima_hf_cleanups_2026_05_07_auto_fire.bash` (chmod +x) — auto-fire master
- `state/hf_cleanup_autofire_prep_2026_05_05/verdict.json` — verdict
- `docs/anima_hf_cleanup_autofire_prep_landed_2026_05_05.ai.md` — this doc

Existing cleanup scripts referenced (unchanged):

- `state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash` — review window ends 2026-05-06T23:26:12Z, EXPECTED_SIBLINGS=16, ubu1 stage `/home/aiden/anima_clm_release_v1_staging` (~7GB)
- `state/p9_pbeta_hf_upload_2026_05_05/cleanup_pbeta_2026_05_08.bash` — review window ends 2026-05-07T03:48:00Z, EXPECTED_SIBLINGS=6, ubu1 stage `/home/aiden/anima_pbeta_50k_step50000` (~108MB)

## Verify results

- clm cleanup `bash -n` syntax — PASS
- pbeta cleanup `bash -n` syntax — PASS
- clm cleanup dry-run — GATE 1 FAIL as expected
- pbeta cleanup dry-run — GATE 1 FAIL as expected
- autofire master `bash -n` — PASS
- autofire master `check-only` — PASS (both dry-runs hit GATE 1 FAIL as designed; exit 1)
- ubu1 staging dir state — UNREACHABLE at prep time (ssh ubu1 timed out at 192.168.50.119); not a blocker — cleanup script GATE 2 + ssh test re-validates at fire time

## Auto-fire modes

- check-only (default) — dry-run both
- fire-clm — clm cleanup only
- fire-pbeta — pbeta cleanup only
- fire-all — clm then pbeta serial with 5s spacer

Master script wraps each cleanup. Both inner scripts gate on GATE 1 (review window elapsed) and GATE 2 (HF repo intact: siblings count + commit sha match snapshot). Failure of either gate aborts before any rm.

## Recommended sequencing

1. clm PUBLIC promote — after 2026-05-06T23:26:12Z (review window close)
2. 24h grace — let consumers download post-promote
3. clm cleanup — at/after 2026-05-07T23:26:12Z via fire-clm
4. pbeta PUBLIC promote — after 2026-05-07T03:48:00Z
5. 24h grace
6. pbeta cleanup — at/after 2026-05-08T03:48:00Z via fire-pbeta

If private-stay decision: skip promote steps; GATE 2 validates regardless of visibility.

`--delete-mac-mirror` flag (optional second pass) on each cleanup removes the mac stage mirror dirs:

- `state/clm_v4_hf_release_v1_upload_stage_2026_05_04`
- `state/p9_pbeta_paradigm_d_50k_hf_upload_stage_2026_05_05`

## Pre-fire requirements

- review window elapsed (GATE 1)
- HF repo intact at expected sha + sibling count (GATE 2)
- `secret get huggingface.token --raw` returns non-empty
- `ssh ubu1` reachable
- PUBLIC promote completed + 24h elapsed (recommended)

## Constraints honored

- no cleanup execution (review windows pre-elapse)
- no ubu1 staging mutation
- no HF Hub mutation
- no git commit
