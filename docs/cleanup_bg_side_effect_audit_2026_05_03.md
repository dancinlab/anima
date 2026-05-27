# Cleanup BG Side-Effect Audit + Guard Design (2026-05-03)

**Date**: 2026-05-03
**Type**: retrospective audit + design recommendation (no implementation)
**Scope**: 2 cleanup BG incidents observed during 2026-05-02 ~ 2026-05-03 cycle window
**Cost**: $0 (mac-local design + memory file write)
**Verdict**: 2 incidents documented + 4 guards specced + memory feedback landed; guards NOT enforced this cycle

## TL;DR

This session's parent agent observed 2 cleanup-BG side-effect incidents that materially damaged downstream state: (a) a cleanup BG unlinked the live training script of a paradigm-D mini-run mid-loop, causing step_2000 + final savepoints to silently fail; (b) a cleanup BG reported a sentinel-50k run as "naturally completed" when the run had OOM-crashed at step 0 within 4 sec of launch. Both trace to ambiguous cleanup verbs and absent state-verification protocols. Four guards designed (verb taxonomy, pre/post state capture, signal-based success criterion, immutable RO script location); guards added to memory as `feedback_cleanup_bg_guards.md`.

## §1 컨텍스트

### Why now

세션 internal에서 cleanup BG (Agent run_in_background=true with cleanup intent) 측 two recent incidents in 2 days. 둘 다:
- silent damage (parent did not notice at trigger time)
- recovery cost > 10× cleanup execution cost (re-train needed in case A; misdirected reasoning ~10 min in case B)
- root cause traceable to parent prompt ambiguity, not BG agent intelligence

raw#10 honest: audit covers ONLY incidents the parent agent visually retained. Silent cleanup mishaps that did not surface to parent attention are NOT in this audit and are likely under-counted.

### Out of scope

- pod-side cleanup (RunPod terminate / SIGTERM at host level) — separate concern
- harness hook implementation (e.g., post-BG validator hook) — recommended next cycle
- retroactive recovery of lost paradigm-D savepoints — out of scope, requires fresh re-train

## §2 Incident A — paradigm_d_mini_run_script_unlink

### Timeline reconstruction

| Phase | Action | Outcome |
|---|---|---|
| T0 | parent launches paradigm-D mini-run BG, target step=2000, watchdog wraps train loop | run progressing |
| T+~25 min | run reaches step 1400/2000 (70%) | savepoints @ 500, 1000 already written; step_1500 next checkpoint |
| T+~26 min | parent issues cleanup BG `a80e5530...` instruction: "kill mini-run watchdog if step < 100, else preserve" | cleanup BG begins audit |
| T+~26 min | cleanup BG sends SIGTERM to watchdog AND unlinks `/tmp/p9_paradigm_d_distill.py` | both actions completed; cleanup BG reports "done" |
| T+~26 min | training process catches SIGTERM, enters post-loop teardown branch (where step_2000 + final save lives) | teardown invokes module-level helpers |
| T+~26 min | teardown helpers attempt to import / re-reference functions in `/tmp/p9_paradigm_d_distill.py` | file gone → import fails silently in disowned subprocess |
| T+~27 min | training process exits with no further log entry | step_2000 + final savepoints NEVER WRITTEN |
| T+next cycle | parent reads "cleanup done"; later cycle expects step_2000 ckpt | downstream consumer fails: "savepoint missing" |

### Root cause

**Ambiguous cleanup verb.** "kill mini-run watchdog if step < 100, else preserve" expresses ONE branch (kill-on-young) but the "else preserve" branch is ill-defined: preserve what — the process? the script? the savepoints? The cleanup BG defaulted to a broader sweep (SIGTERM + script unlink) on the assumption that "mini-run" implied disposable. Parent did not anticipate that script unlink could damage the in-progress teardown path.

### Secondary cause

Training script lived in `/tmp` (mutable, world-writable, ephemeral). No protection against unlink while process held the file open via Python's loaded-module reference. Python loads bytecode lazily for some imports; teardown branch re-imported helpers that were not yet in module cache.

### Observability gap

Cleanup BG did not read the trajectory.json (or equivalent step counter) before deciding. Parent provided a step threshold (< 100) but BG had no separate channel to verify current step. BG made a binary decision (kill vs preserve) without either branch's pre-condition being verified.

### Lost vs preserved

| Status | Artifact |
|---|---|
| LOST | savepoint @ step_2000 |
| LOST | final savepoint |
| LOST | post-teardown verdict.json |
| PRESERVED | savepoints @ step_500, step_1000 |
| PRESERVED | trajectory log up to step_1400 |

Recovery cost: ~$3-5 RunPod re-train, or 1-2hr ubu1 wall time. Recovery scheduled for separate cycle (not this audit).

## §3 Incident B — sentinel_50k_pid_gone_misinterpreted

### Timeline reconstruction

| Phase | Action | Outcome |
|---|---|---|
| T0 | parent launches sentinel-50k training BG, PID 1726340 | run starts |
| T+4s | run hits CUDA OOM at step 0 (model + 50k batch did not fit) | stderr: "CUDA out of memory ... allocation failed" |
| T+4s | process dies, exit code non-zero | OOM stderr written to disk log |
| T+~30s | parent issues cleanup BG: "audit BG PID 1726340 status; report completed/running/failed" | cleanup BG begins |
| T+~31s | cleanup BG runs `ps -p 1726340` → no result | binary signal: PID absent |
| T+~31s | cleanup BG infers "PID gone for 27s ⇒ run completed naturally" | reports `naturally completed` to parent |
| T+next cycle | parent schedules downstream consumer of expected savepoint | downstream fails: "savepoint missing" |
| T+next cycle | parent re-investigates, finds OOM in stderr, ~10 min wasted on misdiagnosis | true cause finally identified |

### Root cause

**Process death is not process success.** Cleanup BG used a 1-bit signal (PID present / absent) where a 3-bit signal is required (running / clean-exit / crashed). PID-absence has at least 3 distinct causes: clean exit (zero), crash (non-zero), external kill (signal). Defaulting to "clean exit" when no other evidence is available is a false-positive bias.

### Secondary cause

Background launch did not redirect exit code or use a `trap` to capture termination. No verdict.json was written (run never reached the verdict-writing branch, since OOM was at step 0). Log tail was on disk but cleanup BG did not consult it.

### Observability gap

The signals that WOULD have correctly classified this run as a crash (exit code, log tail content, savepoint absence at very-short wall-time) were all available on disk but none consulted. Cleanup BG's prompt did not require a checklist of negative signals.

### Lost vs preserved

| Status | Artifact |
|---|---|
| LOST | nothing (run produced nothing) — but parent state model was corrupted for ~10 min |
| PRESERVED | OOM stderr log (on disk, just not consulted) |

Recovery cost: ~10 min parent reasoning time on misdiagnosis. Lower-impact than incident A but high frequency-of-occurrence risk if not guarded.

## §4 Common failure modes (synthesis)

### CFM-1: Ambiguous cleanup verb
- "cleanup", "kill", "sweep", "reset" do not distinguish: (a) signal the process, (b) delete the artifacts, (c) delete the source script, (d) delete the work dir, (e) all of the above.
- Incidents: A
- Symptom: cleanup BG defaults to broader action than parent intended.

### CFM-2: Process state under observation
- PID-gone interpreted as success without inspecting exit code, log tail, or expected output artifacts.
- Incidents: B
- Symptom: false-positive "completed" verdict when run actually crashed.

### CFM-3: Shared mutable resource
- Training script in `/tmp` (or any non-RO path) can be unlinked while mid-run; long-running scripts depend on their own file existing for re-import / lazy load.
- Incidents: A
- Symptom: silent teardown failure → savepoints lost.

### CFM-4: No post-cleanup audit report
- Cleanup BG does not enumerate (a) what was killed, (b) what was preserved, (c) what was lost; parent infers state from absence of complaint.
- Incidents: A, B
- Symptom: parent state model diverges from disk reality.

## §5 Guard design (4 guards, design-only)

### GUARD-1: Explicit cleanup verb taxonomy
**Addresses**: CFM-1, INC-A.

Every cleanup BG instruction MUST classify the action into exactly one of three disjoint verbs:

| Verb | Action |
|---|---|
| `SIGTERM_ONLY` | send SIGTERM to PID; do NOT touch files |
| `DELETE_SCRIPT` | remove a specific named .py / .hexa script after confirming process is dead |
| `FULL_SWEEP` | SIGKILL + remove work dir + remove savepoints (destructive — requires explicit user OK) |

**Enforcement (recommended)**: parent prompt template — `cleanup_action: <SIGTERM_ONLY|DELETE_SCRIPT|FULL_SWEEP>` field is REQUIRED; cleanup BG aborts if field absent or ambiguous. Default-when-unclear: `SIGTERM_ONLY`. Never escalate without explicit re-confirm.

### GUARD-2: Pre/post state verification via separate channel
**Addresses**: CFM-2, CFM-4, INC-A, INC-B.

Cleanup BG MUST capture state BEFORE acting and AFTER acting via a channel independent of the target process.

Required pre-state capture:
- `savepoint_dir mtime + file count`
- `log file size + tail -50 (last 50 lines)`
- `trajectory.json last step (if exists)`
- `PID exit code (if process already gone)`

Required post-state capture:
- `savepoint_dir mtime + file count (delta vs pre)`
- `log tail again (delta vs pre — did it write more after action?)`
- `verdict.json existence + content`

Report format: post-cleanup BG MUST emit JSON `{killed: [...], preserved: [...], lost: [...], pre_state, post_state}`.

**Enforcement (recommended)**: parent rejects cleanup BG report if missing any of the 4 fields above.

### GUARD-3: Process death is not success
**Addresses**: CFM-2, INC-B.

PID-absent MUST NOT be reported as "completed" without verifying at least one positive success signal:
- `exit_code == 0` captured at termination time
- `verdict.json` present with verdict in `{PASS, ALL_GREEN, CLEAN_*}`
- expected savepoint path present with non-zero size
- log tail contains 'training complete' or equivalent terminal sentinel

AND zero failure signals (any one implies crash):
- `exit_code != 0`
- log tail contains `OOM`, `CUDA error`, `Traceback`, `Killed`
- stderr file size > 0 with non-empty last 100 chars
- expected savepoint absent AND wall-time < expected

When signals conflict → report `INDETERMINATE — manual inspection required`. Never default to "completed".

**Enforcement (recommended)**: cleanup BG prompt template includes explicit signal checklist; parent rejects "completed" verdict that lacks at least one positive signal.

### GUARD-4: Long-running script in immutable RO location
**Addresses**: CFM-3, INC-A.

Any training script expected to run > 60s MUST be copied to a read-only location BEFORE launch; the launched process references the RO copy, not the scratch copy.

Recommended locations:
- ubu1: `/opt/anima_runtime/scripts/<run_id>/<script>.py` (chmod 0444)
- runpod ephemeral: `/workspace/runtime/<run_id>/<script>.py` (chmod 0444)
- mac local: N/A — Mac BANS .py per raw#9; hexa scripts under `/opt/anima_runtime/hexa/<run_id>/`

Lifecycle:
1. parent BG copies script to RO location, chmod 0444
2. parent BG launches process pointing at RO copy
3. cleanup BG (any verb) is BANNED from touching RO location
4. RO cleanup is a separate later GC cycle, gated on age (e.g., > 7 days) and absence of any savepoint mtime touch

**Enforcement (recommended)**: launch BG prompt template requires `script_ro_path` field; cleanup BG prompt template includes explicit deny-list for `/opt/anima_runtime/*` and `/workspace/runtime/*`.

## §6 Memory feedback landed

`/Users/ghost/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/feedback_cleanup_bg_guards.md` written with the 4 rules condensed (~50 lines, follows existing feedback_*.md schema with frontmatter `name / description / type / originSessionId`).

`MEMORY.md` index updated — line 12 added pointing at the new feedback file.

## §7 raw#10 (honest caveats — exactly 3 as required)

**(a) Audit may miss other incidents.** This audit covers ONLY the 2 incidents the parent agent visually retained during the 2026-05-02 ~ 2026-05-03 window. Silent cleanup mishaps where a cleanup BG damaged something the parent never asked about (e.g., stale checkpoint quietly deleted) are NOT counted. True incident rate is likely higher than 2-per-session; an exhaustive audit would require log-mining all cleanup BG outputs from every recent session and cross-checking against subsequent "missing artifact" reports — out of scope this cycle.

**(b) Guards add complexity.** GUARD-1 verb classification adds ~30-50% to cleanup BG prompt length. GUARD-2 pre/post state capture adds 5-10s wall time per cleanup. GUARD-4 RO location adds a per-launch copy step (~100-500ms) and a one-time `/opt/anima_runtime/` provisioning. Net win expected only if cleanup incidents > ~1 per 100 BGs. Current observed rate ≈ 2 per ~50 BGs this session = above threshold, so guards are net-positive THIS session — but for low-cleanup-volume sessions the overhead may be unjustified.

**(c) Retroactive lessons hard to enforce.** Guards apply to FUTURE cleanup BGs only. They cannot recover the lost step_2000 + final savepoints from incident A — those require a fresh re-train (~$3-5 RunPod or 1-2hr ubu1, separate cycle). Even for future BGs, enforcement requires either (i) parent discipline to remember the verb taxonomy on every cleanup prompt, or (ii) a harness-level prompt-template hook that auto-injects the checklist. Without (ii), drift is likely within 5-10 cycles as memory of these incidents fades. Recommended next cycle: implement post-BG validator hook that rejects cleanup reports missing the 4 required JSON fields.

## §8 Output inventory

| Artifact | Path | Bytes (approx) |
|---|---|---|
| handoff doc (this file) | `docs/cleanup_bg_side_effect_audit_2026_05_03.md` | ~14KB |
| incidents JSON | `state/cleanup_bg_audit_2026_05_03/incidents.json` | ~5KB |
| guards JSON | `state/cleanup_bg_audit_2026_05_03/guards.json` | ~5KB |
| memory feedback | `<MEMORY_ROOT>/feedback_cleanup_bg_guards.md` | ~3KB |
| memory index update | `<MEMORY_ROOT>/MEMORY.md` (line 12 added) | +1 line |
| silent-land marker | `state/markers/cleanup_bg_side_effect_audit_landed.marker` | <1KB |

`<MEMORY_ROOT>` = `/Users/ghost/.hive/claude-config/hive-hook-bus/projects/-Users-ghost-core-anima/memory/`

## §9 비충돌

- 본 audit 측 sole writer 측 `state/cleanup_bg_audit_2026_05_03/`, `docs/cleanup_bg_side_effect_audit_2026_05_03.md`, `state/markers/cleanup_bg_side_effect_audit_landed.marker`, memory file 측 신규 추가
- MEMORY.md 측 +1 line append (read-first 후 추가, 기존 11 lines preserve)
- 활성 BG / pod 측 modify NONE (raw#9, raw#15)
- training script / savepoint 측 touch NONE
- destructive ops: 0

## §10 cost + policy

- Cost: $0 (mac-local read + design + 6 file writes; no GPU, no API, no pod)
- Policy:
  - raw#9 STRICT: Mac → no .py creation (only .md + .json + memory .md)
  - raw#15: BR-NO-USER-VERBATIM, additive only, no destructive ops
  - raw#10: 3 honest caveats (a/b/c above) — audit gap, guard overhead, retroactive limit
  - silent-land marker landed
  - Korean-friendly preset (technical English for spec terms, Korean for narrative where natural)
- Wallclock: ~5min audit + write

## §11 Next-cycle recommendations

1. **Convert GUARD-1 verb taxonomy to prompt template snippet.** Add a `cleanup_verb` field to the standard cleanup BG launch prompt; reject if absent.
2. **Convert GUARD-3 signal checklist to a hook (post-BG validator).** Use `update-config` skill to add a hook that runs after any cleanup BG, parses its JSON output, and rejects "completed" verdicts lacking positive signals.
3. **Provision `/opt/anima_runtime/` on ubu1.** Pre-create dir, set group-writable for launch BG user, set ACL such that all created files default to chmod 0444.
4. **Audit existing /tmp/*.py and /tmp/*.hexa active runs.** Migrate any that are expected to run > 60 sec to RO location. Inventory script: `find /tmp -name '*.py' -o -name '*.hexa' | xargs -I{} stat -f '%m %N' {}` then cross-check against active PIDs.
5. **Schedule paradigm-D step_2000 re-train.** Separate cycle, $3-5 RunPod or 1-2hr ubu1 — gated on user OK.

---

**audit + design + memory landed + 3 honest caveats + silent-land marker + AI-native + BR-NO-USER-VERBATIM + raw#9/15 + 마이그레이션 0 + destructive 0 ✓**
