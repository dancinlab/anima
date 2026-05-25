---
title: H100 concurrency policy LANDED — 1-page summary (2026-05-04)
cycle: 2026-05-04
ts: 2026-05-04T00:00:00Z
status: POLICY_LANDED
bg_lane: H100-NOLIMIT
type: ai_native_landed
spec_doc: docs/anima_h100_concurrency_policy_2026_05_04.md
memory_entry: feedback_h100_no_concurrency_limit.md
---

# H100 concurrency policy LANDED (2026-05-04)

5-bullet summary of `docs/anima_h100_concurrency_policy_2026_05_04.md`.

## (a) Policy text

User directive 2026-05-04: **"h100 동시 갯수제한 없음"** — no artificial cap on simultaneous H100 pods. Parallel H100 BG launches are policy-OK. Constraints: RunPod account quota + per-BG `BUDGET_HARD_CAP_USD` + L11 setsid + L13 trap pre-stop scp + session-level default cap $200. Older "1 H100 at a time" or "≤2 pods cap" assumptions are **superseded**.

## (b) Why

User explicit directive 2026-05-04 confirming infra/policy alignment. Older session conventions had implicitly serialized H100 launches due to chat-blocking concerns and budget anxiety; this rule makes the no-cap stance explicit so future sessions don't re-impose artificial limits. Aligns with `feedback_session_multi_bg.md` (≥2 BG parallel mandate) — H100 BGs are also valid members of that ≥2.

## (c) Practical guards

- Per-BG `BUDGET_HARD_CAP_USD` MANDATORY in launch prompt (e.g. $15, $35).
- Explicit dollar projection: concurrency × $2.99/hr × wall.
- L11 setsid: every remote launch `setsid nohup … &`.
- L13 trap pre-stop scp: SIGTERM trap saves savepoint/log/verdict to ubu1 before pod terminates.
- Heartbeat per BG: `state/<bg_id>/heartbeat.ts` separate; watcher auto-stops pod if stale >5min.
- Probe before bulk-launch: N=1 → N=3 → N=9 to discover RunPod ceilings.
- Default session-level sane cap: $200 unless user overrides.
- HF Hub stagger when N>5 to avoid rate limits.

## (d) Memory entry written

- `feedback_h100_no_concurrency_limit.md` landed at `~/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/`
- `MEMORY.md` line appended: `- [H100 no concurrency limit](feedback_h100_no_concurrency_limit.md) — parallel H100 BGs OK; cap by per-BG budget not concurrency count`
- 5 roadmap annotation proposals (additive_only, NOT mutated this cycle): `.roadmap.p9_sft`, `.roadmap.clm`, `.roadmap.blm_brain_lm`, `.roadmap.anima_clm_eeg`, `.roadmap.training`. `.roadmap.eeg` excluded (CPU/EEG, no GPU concurrency).

## (e) Honest C3 (raw#10, 7 caveats from spec §8)

1. "No limit" is policy not infra — RunPod can still rate-limit; per-account ceiling unpublished (typically 5-10).
2. Concurrent burn compounds linearly — 5×$2.99/h = $15/h. 9×24h ≈ $645+. Without per-BG cap, an unattended overnight cycle could burn $1000+.
3. One bad BG can OOM account quota (rare <10 pods, common >10) — locks out *all* future launches in session.
4. HF Hub is shared resource — N concurrent pushes can hit 429s; stagger or proxy when N>5.
5. L11 setsid + L13 trap pre-stop scp MANDATORY at high concurrency — without them, this policy invites disasters that the old "1 H100" cap implicitly prevented.
6. Probe before bulk — N=1→3→9 costs ~$1 vs. risk of 9 simultaneous OUT_OF_CAPACITY failures.
7. Heartbeat per-BG paths only — concurrent fsync to shared heartbeat.ts can corrupt and trigger spurious auto-kill.

## Status

- Spec doc: LANDED (`docs/anima_h100_concurrency_policy_2026_05_04.md`)
- Auto-memory entry: LANDED (`feedback_h100_no_concurrency_limit.md`)
- MEMORY.md index: LANDED (1 line appended)
- Roadmap annotations: PROPOSED (5 files, NOT mutated this cycle, additive_only next-cycle land)
- Git commit: deferred — user/me to commit after review
- Cost: $0 (doc + memory only, no exec)

## References

- Spec: `docs/anima_h100_concurrency_policy_2026_05_04.md` (10 sections, §3 budget mandate, §6 hard limits, §7 roadmap proposals, §8 honest C3 ×7)
- Memory: `feedback_h100_no_concurrency_limit.md`
- Sister: `feedback_session_multi_bg.md`, `feedback_parallel_bg_git_race.md`, `feedback_always_subagent_bg.md`
- Predecessor: `project_runpod_pod_purge_2026_05_03.md`
