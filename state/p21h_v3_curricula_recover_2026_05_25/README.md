# F-CURRICULA-1 fire recovery — DISPATCHER ORPHAN (2026-05-25)

**verdict: NO_TRAIN_OCCURRED · launcher class-1 silent failure · pod idle 158min · $3.92 burnt**

## What this is

Recovery record for the F-CURRICULA-1 PURE fire (`P21H_curriculum_v2` variant)
on runpod pod `c25njysjdga2vb` (1× A100 SXM, $1.49/hr) launched
2026-05-25 ~10:56 UTC. Pod ran for ~158 minutes with **zero training
activity** — class-1 silent failure at launcher.

## Symptom

`/workspace/p21hr/train.log` final lines (full 23-line copy in
`train_log_remote_final.txt`):

```
[launch] accelerate=1.13.0
[launch] python3 -u qwen 1337
python3: can't open file '/root/qwen': [Errno 2] No such file or directory
```

`out_main/` empty. No `[P21H]` step lines. GPU utilization 0%, mem
427MiB (driver baseline). No remote python process. No kosmos anchors.

## Root cause

`launch_trainer_p21h.sh` final line:
```bash
echo "[launch] python3 -u $@"
exec python3 -u "$@"
```

The dispatcher that fired c25njysjdga2vb passed argv
`(qwen, 1337)` only — no `train_p21h_v3.py` script path — so the
script execed `python3 -u qwen 1337` → ENOENT, instant exit.

### Why this happened despite #423

PR #423 (`fix(PURE): dispatch_p21h_v3 train_launch full argv + missing
dep + result path`, merged 2026-05-24 22:04 KST) **already fixed**
this exact bug at `dispatch_p21h_v3.hexa:364-389`. The current main
file passes the full argparse argv:

```hexa
let argv = [
    "bash", p21hr + "/launch_trainer_p21h.sh",
    p21hr + "/train_p21h_v3.py",
    "--wiki-corpus", _pod_wiki_corpus_path(p21hr),
    ...full flags...
]
```

So the c25njysjdga2vb fire (dispatched 2026-05-25 ~10:56 UTC, **after**
#423 landed) used either:
  - a stale local worktree / branch that hadn't pulled #423,
  - the legacy bash sibling
    `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/dispatch_p21h_v3_runpod.sh`,
  - or a path that bypassed the v0.2 dispatcher entirely.

The dispatcher state log at `/tmp/p21h_fire.log` line 17-18:
```
[corpus_scp_override] uploaded ./state/pure_phase_d_curriculum_v2_2026_05_24/merged_curriculum_v2.jsonl → ...
[train_launch] started; remote pid 298 · log /workspace/p21hr/train.log
```
shows it DID use the .hexa dispatcher (the `[corpus_scp_override]`
banner is only in dispatch_p21h_v3.hexa). Yet the remote train.log
shows only 2 positional args. Either:
  - The remote `launch_trainer_p21h.sh` file on the pod was stale,
    AND/OR
  - The argv was passed correctly but the pod-side script invocation
    ate the script path before exec'ing python3.

A definitive root cause requires re-fire with full argv-echo on the
pod's wrapper. Filed to hexa-lang for canonical hardening.

## Cost

- pod runtime: ~158 min @ $1.49/hr ≈ **$3.92 burnt**
- value: 0 (no model, no eval, no claim)

## Why WATCHDOG didn't catch it

`dispatch_p21h_v3.hexa` `result_pull_with_wait` polls only for
`result.json` appearing. The launcher crashing within 15 sec is
indistinguishable from "still training" — both produce "no
result.json yet". `SAVE_POD=1` correctly retained the pod for
external Monitor (so we COULD inspect post-hoc), but there's no
early-life check (e.g. `[P21H] step=` line within 5 min).

## Actions taken

1. **Filed hexa-lang inbox patch** —
   `core/hexa-lang/inbox/patches/cloud-launch-trainer-script-arg-missing.md`
   recommends adding `hexa cloud nohup --early-life-check <sec>` flag
   to poll the remote pid within first window and fail-fast on
   class-1 failures.

2. **Pod destroyed** — `runpodctl pod delete c25njysjdga2vb`
   succeeded 2026-05-25 (no artifacts to lose, since none existed).
   Verified pod no longer in `runpodctl pod list`.

3. **No HF upload** — nothing to upload (no checkpoint, no model
   card subject). `a_hf_complete` blocks PUBLIC uploads of partial /
   null artifacts; the artifact set is empty so the rule is vacuously
   satisfied.

4. **No CLAIMS.tape update** — F-CURRICULA-1 produced no verifiable
   claim (no model, no closure_auto_judge verdict). CLAIMS.tape gates
   only terminal 🔵/🟢/🔴 model-level claims. The dispatcher-bug
   discovery is a process anchor, not a model claim, and lives here +
   in the hexa-lang inbox.

## Files in this dir

- `README.md` (this file)
- `train_log_remote_final.txt` — verbatim 23-line train.log from the
  pod before teardown (captured for the inbox patch evidence)

## Re-fire plan

Before any re-fire of F-CURRICULA-1:

1. **Smoke test** — run `dispatch_p21h_v3_smoke.hexa` (50-step
   dry-run) on a cheaper pod first. Catch class-1 launcher failures
   in 5 min, not 158 min.

2. **Argv echo verify** — modify the on-pod `launch_trainer_p21h.sh`
   to echo the full argv it received BEFORE pip installs, so a stale
   wrapper is visible immediately:
   ```bash
   echo "[launch] received argv: $0 $*"
   echo "[launch] script-path arg (\$1) = $1"
   ```

3. **Early-life poll** — until hexa-lang adds
   `--early-life-check`, wrap dispatcher with a 5-min post-fire
   `hexa cloud poll <pid>` + abort + teardown if dead.

Expected wall for the full fire (post-fix): ~6 hr × $1.49 ≈ $8-9
per the prior p21h-random pattern (PSCC §44-style, 5K steps Qwen
1.5B on A100 SXM).

## Lesson Index

- `feedback_dispatcher_silent_class1_failure_2026_05_25` (proposed) —
  WATCHDOG on `result.json` is NOT enough; need early-life pid
  liveness check (60-120s) to catch script-arg / import / OOM-at-load
  failures before the full WATCHDOG window expires.
- Pairs with `feedback_agent_bash_pool_route_runpod_orphan` (different
  orphan mechanism: ssh routing vs script-path-arg).
