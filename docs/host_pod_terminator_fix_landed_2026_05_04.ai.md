# host_pod_terminator.sh.txt error-branch fix — landed 2026-05-04

**Cycle**: `watcher_script_fix_2026_05_04`
**Scope**: surgical bug fix in `state/p9_path_a_llama_lora_2026_05_03/host_pod_terminator.sh.txt`
**Verdict**: PASS (F-WATCHER-1 syntax PASS, F-WATCHER-2 mkdir-count=2 PASS)

## Bug origin

`host_pod_terminator.sh.txt` is the Mac-side watcher launched alongside Path A
LLaMA-3 8B LoRA training (10000 steps on RunPod H100). It polls the pod every
10min via SSH; when `TRAIN_DONE.json` lands the DONE-branch fires (line 44–58)
and `scp`s artifacts down. When the train pid dies WITHOUT `TRAIN_DONE.json`
(crash, OOM, segfault), the error-branch fires (line 60–68) to grab `train.log`
before pod termination.

The DONE-branch correctly runs `mkdir -p .../artifacts` at line 47 before its
first `scp` write. The error-branch lacked the equivalent: it directly tried
`scp -i ... root@host:/.../train.log .../artifacts/train.log` without ensuring
the local `artifacts/` directory existed. On a clean Mac state where Path A had
never reached DONE, the artifacts dir would not yet exist, and `scp` would
silently emit a destination-path error (logged via `>> $LOG 2>&1 || true`).

## Discovery (BG-ι, BG-ξ)

- BG-ι (commit `e4d86fb2f`) audited Path A step-10000 final-save failure and
  noticed `train.log` never reached the Mac despite the error-branch having
  fired. Recovery was forced through the HF API (mirror was the fallback
  channel).
- BG-ξ (commit pending) confirmed via cross-check that the error-branch path
  was structurally degraded: present in the script but functionally muted by
  the missing `mkdir -p`.
- Both BGs flagged this as the root cause of Mac-side diagnostic blackout
  during final-save failure.

## Fix

Single line inserted between line 62 (echo) and the existing scp call (now
line 64):

```diff
     if echo "$PROBE" | grep -q "ALIVE=0" && echo "$PROBE" | grep -q "DONE=0"; then
         echo "[$(date -u +%FT%TZ)] train pid GONE without DONE — likely error; downloading log + terminating" >> $LOG
+        mkdir -p /Users/ghost/core/anima/state/p9_path_a_llama_lora_2026_05_03/artifacts
         scp -i $SSH_KEY -o StrictHostKeyChecking=no -P $SSH_PORT \
             "root@$SSH_HOST:/workspace/p9_path_a_llama_lora/train.log" \
             /Users/ghost/core/anima/state/p9_path_a_llama_lora_2026_05_03/artifacts/train.log >> $LOG 2>&1 || true
```

Idiom matches the DONE-branch line 47 exactly (same absolute path, same
`mkdir -p` flag, no comment — DONE-branch had a comment but the structural
copy is clean).

## Falsifiers

- **F-WATCHER-1**: `bash -n /tmp/host_pod_terminator.sh` exits 0 → syntax PASS.
- **F-WATCHER-2**: `grep -c 'mkdir -p .*artifacts'` returns exactly 2
  (line 47 DONE-branch, line 63 error-branch). PASS.

## What future training cycles gain

- No more diagnostic blackout when train pid dies without DONE marker.
- `train.log` reliably reaches Mac for postmortem regardless of pod final
  state.
- Path A-style recoveries (HF API mirror as fallback) become the second-best
  channel rather than the only channel.
- Pattern is now copyable to other watcher scripts (e.g., Path B, future
  pod-orchestrated training cycles).

## Honest C3

- Other watcher scripts in the repo were NOT audited and may carry the same
  bug.
- Selftest is `bash -n` syntax-only; behavior under live error-branch trigger
  was not exercised end-to-end.
- The error-branch may have other latent bugs (scp timeout, partial-write
  detection, log truncation) outside this BG's audit scope.
- Line 47 / line 63 are point-in-time; future edits may shift the diff
  context.
- Bug attribution to this exact missing `mkdir -p` is INFERRED from BG-ι/ξ
  postmortem evidence, not directly reproduced via a failing pod.

## Files touched

- `state/p9_path_a_llama_lora_2026_05_03/host_pod_terminator.sh.txt` (+1 line)
- `state/watcher_script_fix_2026_05_04/verdict.json` (NEW)
- `state/watcher_script_fix_2026_05_04/selftest.log` (NEW)
- `docs/host_pod_terminator_fix_landed_2026_05_04.ai.md` (this file, NEW)

## Constraints honored

- raw#9: `.sh.txt` parked form respected; no new `.py` file created.
- raw#15: repo-relative paths in doc.
- raw#71: F-WATCHER-1/2 falsifier-bound.
- No git mutations (parent session serializes commits).
- No chflags.
- No actual SSH or pod action; selftest was `bash -n` only.
