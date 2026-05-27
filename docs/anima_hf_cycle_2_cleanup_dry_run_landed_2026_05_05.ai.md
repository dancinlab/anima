# anima HF Cycle 2 Cleanup — Dry-Run Landed (2026-05-05)

**Cycle**: hf_cycle_2_cleanup_dry_run_2026_05_05
**BG lane**: BG-HF-CLEANUP-DRY-RUN
**Parent cycle**: clm_v4_hf_release_v1_upload_2026_05_04
**Script under verification**: `state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash`
**Verdict**: `state/hf_cycle_2_cleanup_dry_run_2026_05_05/verdict.json`

## Scope

$0 dry-run. No mutation of cleanup script, ubu1 staging dir, or HF Hub repo. Verifies cleanup script preconditions before scheduled execution at-or-after 2026-05-06T23:26:12Z (review window close + grace).

## Results Summary

| Check | Result | Notes |
|---|---|---|
| shellcheck | N/A | not installed on mac |
| bash -n syntax | PASS | exit 0 |
| GATE 1 time gate fires | PASS | `[cleanup ERR] GATE 1 FAIL: review window not yet elapsed`, exit 1, as expected |
| HF Hub repo private | PASS | private=true |
| HF Hub commit sha | PASS | `80440a1d38db9addc4445bb959057558a57f4230` matches upload-time |
| HF Hub siblings count | DRIFT | API returns 16; cleanup script expects 15 (off-by-one in script L13) |
| HF Hub siblings list match verdict | PASS | exact match against verdict.json siblings_list (16 entries) |
| ubu1 staging dir live | PASS | 7.0G, 15 files at /home/aiden/anima_clm_release_v1_staging/ |
| ubu1 ssh reachable | PASS | NOW (real run-time reachability is a runtime dependency) |
| current → review window close | 44.21h | window closes 2026-05-06T23:26:12Z |

## Critical Finding — BLOCKER for 2026-05-07 Run

`cleanup_2026_05_07.bash` L13 sets `EXPECTED_SIBLINGS=15` but the actual repo has **16** siblings. GATE 2 will abort the cleanup with `siblings_count=16 != expected 15` unless the constant is corrected.

**Root cause**: `state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json` L70 records `"siblings_count": 15` while L72 `siblings_list` enumerates 16 files. The cleanup script copied the bad number from L70 instead of `len(siblings_list)`. HF Hub itself is correct — the 16th file is `tokenizer_64k_multilingual.vocab` which is paired with `.model` (both present, both expected, both leak-guard scanned in original L2 pass).

**Fix** (NOT performed this BG per `DO NOT modify cleanup_2026_05_07.bash` instruction):
```bash
# in state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash L13:
EXPECTED_SIBLINGS=16  # was 15 — corrected per dry-run drift analysis
```
Operator should also update `verdict.json` L70 `"siblings_count": 15` → `16` for record-keeping accuracy (does NOT affect cleanup execution).

## Files Touched This Cycle

- created: `state/hf_cycle_2_cleanup_dry_run_2026_05_05/verdict.json`
- created: `docs/anima_hf_cycle_2_cleanup_dry_run_landed_2026_05_05.ai.md` (this file)
- read-only: `state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash`
- read-only: `state/clm_v4_hf_release_v1_upload_2026_05_04/cron_install_recipe.txt`
- read-only: `state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json`

## Ready for 2026-05-07 Run?

**No, blocked on 1 fix** (siblings count constant 15→16). After fix: yes.

**Recommended run window**: 2026-05-06T23:26:12Z to 2026-05-07T23:26:12Z (24h grace).
**Recommended invocation**: manual (cron_install_recipe rank-1).
```
cd /Users/ghost/core/anima
bash state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash
```

Optional `--delete-mac-mirror` flag to also remove the 3-file mac stage mirror.

## Honest C3 (≥5 — see verdict.json `honest_c3` for full text)

1. dry-run is shellcheck+bash -n+time-gate sanity, NOT full path coverage (rm + post-state never executed)
2. cleanup is irreversible after run; recovery cost ~30min + 1 upload cycle
3. no automated review-outcome check; cleanup runs blind to F-CLM-RELEASE-1/2 results
4. ssh ubu1 reachability is a runtime dependency
5. HF Hub state can drift between dry-run and actual run
6. **drift discovered**: EXPECTED_SIBLINGS=15 off-by-one (actual=16); BLOCKER for run
7. shellcheck unavailable on mac; only bash -n ran

## Next Actions Ranked

- rank-1: User patches `cleanup_2026_05_07.bash` L13 `EXPECTED_SIBLINGS=15` → `EXPECTED_SIBLINGS=16` before 2026-05-07
- rank-2: User patches `verdict.json` L70 `siblings_count: 15` → `16` for record accuracy (cosmetic)
- rank-3: User runs F-CLM-RELEASE-1 + F-CLM-RELEASE-2 sanity tests during 44h remaining review window
- rank-4: User runs cleanup manually on 2026-05-07 within recommended 24h window
- rank-5: User decides public-promotion separately (cleanup is independent of promotion decision)

## Constraint Compliance

- raw#9 (md+json+bash carve-out): respected — only md + json written, no .py
- raw#10 (≥5 honest C3): 7 entries in verdict.json honest_c3
- raw#15: respected
- DO NOT modify cleanup_2026_05_07.bash: respected
- DO NOT delete ubu1 staging: respected
- DO NOT mutate HF Hub: respected (only GET requests)
- DO NOT git commit: respected
