---
date: 2026-05-05
agent: BG-HF-CYCLE-2-CLEANUP-PREP
cycle: clm_v4_hf_release_v1_upload_2026_05_04 — cleanup phase prep
status: SCHEDULED — earliest run 2026-05-07 post 48h review window
ssot_artifacts:
  - state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash
  - state/clm_v4_hf_release_v1_upload_2026_05_04/cron_install_recipe.txt
predecessor: state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json (HF Cycle 2 upload LANDED 2026-05-04T23:26:12Z)
target_repo: dancinlab/clm-v4-mk2-v1 (private at v1)
review_window_ends_48h_utc: 2026-05-06T23:26:12Z
---

# anima HF Cycle 2 cleanup SCHEDULED (2026-05-05)

## §1 What is scheduled

Post 48h review window cleanup for HF Cycle 2 upload (`dancinlab/clm-v4-mk2-v1`). Earliest run: 2026-05-07T00:00:00Z. Two artifacts staged:

- `cleanup_2026_05_07.bash` — 2-gate guarded cleanup (GATE 1 review window elapsed; GATE 2 HF repo intact siblings=15 + commit_sha=80440a1d) + verb=DELETE_SCRIPT verified pre/post-state. Targets ubu1 staging dir `/home/aiden/anima_clm_release_v1_staging` (~7GB) by default; mac stage mirror retained unless `--delete-mac-mirror` flag is passed.
- `cron_install_recipe.txt` — explicit RECOMMENDATION: do NOT install cron, manual operator run preferred. 5 reasons enumerated (one-shot scope, GATE 2 needs human judgment on drift, F-CLM-RELEASE-1/2 sanity tests must precede cleanup, ssh-agent availability, cleanup-bg-guards mandate). Cron form provided for completeness with 5+ failure modes flagged.

## §2 Why scheduled (not auto-executed)

- 48h review window for HF upload (`dancinlab/clm-v4-mk2-v1`) ends 2026-05-06T23:26:12Z; cleanup must NOT precede window close (re-upload may be needed if F-CLM-RELEASE-1/2 sanity tests fail)
- F-CLM-RELEASE-1 (`AutoModelForCausalLM.from_pretrained(repo, trust_remote_code=True)` fresh shell) + F-CLM-RELEASE-2 (1-batch forward returns finite logits shape `[1,T,64000]`) MUST PASS during review window before cleanup; ubu1 staging is the re-upload source if these fail
- 7GB ubu1 stage is negligible disk pressure on 5070ti workstation; rushing cleanup has no upside
- promote-to-public decision is a separate cycle (.roadmap.clm cond.2 plan §1 step 9); should also precede cleanup ideally

## §3 Honest C3 (raw#10)

- C1 cleanup is operator-discretion not auto-cron — script will only run when operator explicitly invokes; this is by design per cleanup-bg-guards memory feedback (verb classification + human judgment required for drift cases)
- C2 GATE 2 commit_sha check `80440a1d38db9addc4445bb959057558a57f4230` will hard-fail if user re-pushes README edit during review window (legitimate change re-shifts HEAD); operator must update `COMMIT_SHA` in script before running OR skip GATE 2 manually if drift is expected — script is conservative, not adaptive
- C3 ssh ubu1 reachability assumed — if ubu1 is down or key forwarding broken, GATE 2 still passes (HF API check) but CLEANUP-A delete-step fails late; consider running `ssh ubu1 'echo ok'` smoke before invoke to fail-fast at $0 cost
- C4 mac stage mirror (`state/clm_v4_hf_release_v1_upload_stage_2026_05_04/`) holds only 3 text files (README.md + LICENSE + manifest.json copy); kept by default since they're small + may serve as audit-trail; `--delete-mac-mirror` flag opt-in only
- C5 secret CLI dependency — script calls `secret get huggingface.token --raw`; if HF token rotates between upload-time and cleanup-time, GATE 2 still works (token only needs read scope on private repo), but a fully-rotated/revoked token would 401 the API call → GATE 2 FAIL → operator must refresh secret cache and re-run
- C6 GATE 1 timestamp check uses string comparison on ISO 8601 UTC timestamps — works because Z-suffixed RFC3339 is lexicographically orderable; if local timezone shifts (DST), the check is unaffected since both sides are UTC literals
- C7 cleanup verb is DELETE_SCRIPT (not FULL_SWEEP / SIGTERM_ONLY) — matches feedback_cleanup_bg_guards.md mandate that scope-limited delete operations record verb explicitly + verify pre+post state; script does emit pre-state + post-state reports, satisfying the feedback's "never equate PID-gone to success" principle by checking directory absence post-rm explicitly

## §4 Cross-link

- Upload verdict: `state/clm_v4_hf_release_v1_upload_2026_05_04/verdict.json` (HF Cycle 2 LANDED, 12/12 sha256 match, siblings=15)
- Repo: https://huggingface.co/dancinlab/clm-v4-mk2-v1 (private)
- Promote-public is separate: `.roadmap.clm cond.2` plan §1 step 9 (NOT this cleanup)
- Cleanup script: `state/clm_v4_hf_release_v1_upload_2026_05_04/cleanup_2026_05_07.bash`
- Cron recipe: `state/clm_v4_hf_release_v1_upload_2026_05_04/cron_install_recipe.txt`

## §5 Recommendation (ranked)

- rank-1: MANUAL RUN by operator on 2026-05-07 or later, after F-CLM-RELEASE-1 + F-CLM-RELEASE-2 sanity tests pass; default invocation (no `--delete-mac-mirror`)
- rank-2: SKIP cleanup entirely if ubu1 disk pressure is non-issue (7GB on 5070ti workstation is negligible); deferred indefinitely is safe
- rank-3: macOS launchd one-shot StartCalendarInterval — cleaner than cron for one-shot but still requires PATH + ssh-agent solving; NOT recommended
- rank-4: cron entry per recipe — least recommended, listed for completeness only
