# P9 Path A r=64 — step-10000 Absence Reconcile (Landed)

**Cycle**: `p9_path_a_r64_step10k_reconcile_2026_05_04`
**Date**: 2026-05-04
**Parent context**: `docs/p9_path_a_completion_audit_landed_2026_05_03.ai.md` + `state/p9_path_a_hf_push_verify_2026_05_04/verdict.json`
**Status emit**: `__P9_PATH_A_R64_STEP10K__ ABSENT_TERMINAL_NONE_NEEDED`

## TL;DR

HF repo `need-singularity/p9-llama32-lora-stage1` has only 4 step-named commits (step-2k/4k/6k/8k), not the expected 5. **Definitive cause**: `host_pod_terminator.sh` killed pod `29dhlqk508ugoc` 5 seconds after detecting `ALIVE=0 AND DONE=0 AND STEP=10000/10000`, while the step-10000 save+push pipeline was still in flight (would normally take 60-180s based on prior saves). No step-10000 commit ever reached HF git transaction. Training PROBABLY reached step-10000 in-process, but final-save+push never completed. **Recovery action: NONE_NEEDED** (r=64 is FAIL by F1 axis regardless; no local cache exists; $0 constraint).

## Investigation question

> Path A r=64 training was specced `--max-steps 10000 --save-steps 2000`, expected 5 step-Nk HF commits + final adapter. Live HF API shows only 4 step-Nk commits. Was training stopped at step-8000? Was it a push failure? Or other?

## Definitive answer

**Other** — specifically: **host-side terminator killed pod inside the step-10000 save+push critical section**.

- **NOT (a) training stopped at 8000**: host_terminator.log monotonic step probes show STEP advancing 7951→8185→8427→...→9843→10000 across 20:03Z–21:34Z. Trainer's `TrainerState.global_step` (sampled by terminator's ssh+jq probe) is updated AFTER each optimizer step, so STEP=10000 = the 10000th step finished.
- **NOT (b) pure push failure**: prior 4 saves (step-2k/4k/6k/8k) all pushed cleanly within 1-3min wall-time per save. Nothing in evidence chain points to network/auth failure for the 5th. HF token verified at 15:17Z + on-pod token had write scope.
- **YES (c) terminator race**: pod terminated at 21:34:13Z, exactly 5sec after pid-gone detection at 21:34:08Z. Step-8000 save+push took ~1-3min based on commit-timestamp vs probe-window cross-reference. Step-10000 save+push had structurally zero chance to complete in a 5sec window.

## Step-10000 status (definitive)

| Location | Status | Method |
|---|---|---|
| HF repo (HEAD/main) | **ABSENT** | live HF Hub HTTP API 2026-05-04T13:42Z; HEAD = `5a9b458467` "Training in progress, step 8000" dated 2026-05-03T20:06:18Z; no newer commit |
| HF repo (any branch/tag) | **ABSENT** | refs API: branches=[main only], tags=[] |
| HF repo (deleted commits) | **N/A** | HF Hub does not expose; no evidence of deletion (chain back to initial commit is unbroken) |
| Pod 29dhlqk508ugoc disk | **UNRECOVERABLE** | pod terminated 21:34:13Z; ssh refused at 13:42Z; RunPod hard-deletes container disk on pod delete |
| Mac local artifacts/ dir | **NEVER CREATED** | host_terminator.log line 46: scp failed because error-branch did not `mkdir -p artifacts` (script bug; documented in completion-audit honest_c3 caveat (d)) |

**Final adapter (`final/`) status**: same as step-10000 — never reached HF, never recoverable.

## Evidence chain (6 facts)

| ID | Source | Fact | Implication |
|---|---|---|---|
| E1 | host_terminator.log L36-44 | STEP probe: 7951(20:03Z) → 8185(20:13Z) → 10000(21:34Z, ALIVE=0) | training process advanced past 8000 to 10000 |
| E2 | HF commits API (live) | HEAD `5a9b458467` = step 8000 @ 20:06:18Z; no newer commit; 5 total commits | Trainer made exactly 4 step-Nk commits; step-10k never created |
| E3 | host_terminator.log L44-51 | 21:34:08Z pid GONE → 21:34:13Z runpodctl pod delete returned `{deleted:true}` | 5sec gap; error-path branch fired immediately |
| E4 | train_llama_lora.py.txt L146-155 | `trainer.train()` → `save_model('final')` → `tok.save_pretrained` → write `TRAIN_DONE.json`; `hub_strategy=every_save` | step-10k push fires inside `trainer.train()` at last save_steps boundary; bg push thread ~30-90s for 390MB LoRA |
| E5 | step-8000 commit-vs-probe cross-ref | step-8000 commit landed 20:06:18Z while STEP probe showed 7951→8185 across 20:03-20:13Z window; step-2000 same pattern at 15:52Z | push pipeline wall-time = 1-3min per save; 5sec termination window is structurally incompatible |
| E6 | HF tree/main API | 11 files at HEAD; LFS adapter sha256 `f12f31d8…3336` size 389MB; xetHash present | step-8000 HEAD is integrity-clean; no partial-upload corruption; absence is true non-creation |

## Ranked root causes (post-evidence)

| Rank | p | Cause | Type |
|---|---|---|---|
| 1 | 0.85 | Host-terminator killed pod during step-10000 save+push transaction | TERMINATOR FAULT |
| 2 | 0.10 | Training crashed post-`trainer.train()` pre-`save_model('final')` (OOM in final state dump / NaN / etc.); pid exited cleanly; same 5sec window also raced step-10k push | TRAINING INCOMPLETE |
| 3 | 0.05 | Pure HF push 401/network failure WITHOUT terminator interference (step-10k local write succeeded but commit failed) | PUSH FAILURE only |

(Prior audit's 60/25/10/4/1 partition revised to 85/10/5 after live HF API confirmed absence and rules out cause-rank "save succeeded + commit succeeded but downstream race".)

## Recovery action

### NONE_NEEDED

**Reasoning**:
1. **r=64 is FAIL by F1 axis regardless**: per `project_p9_f1_anchor_recalibration` memory: F1_spec=0.4 was unrealistic (Llama-self ceiling = 0.1555; sentinel = 3.2% of Llama). r=64 was the design-fail-fast slice. Step-10000 vs step-8000 anchor delta does not change the FAIL verdict.
2. **No local cache to re-upload**: pod terminated; scp at termination failed (script bug); pod-side disk is hard-deleted on RunPod.
3. **Re-training delta 8000→10000 ($1.50)**: rejected — gold-plates an already-FAIL verdict; opportunity cost vs Track B r=16 productive work.
4. **Resume from step-8000 to push step-10000**: rejected — would require fresh pod ($), would not produce identical step-10k weights (RNG state diverges past resume), gold-plates FAIL verdict.
5. **Project $0 constraint binds** — no re-training sanctioned.
6. **Track B r=16 is the productive path forward** (per `p9_path_a_r16_2026_05_03` + `p9_path_a_r16_3seed_2026_05_04` cycles already in flight). r=16 will produce its own clean step-10000 + final on a separate HF repo.

### Downstream consumer guidance

| Consumer | Anchor to use | Footnote required |
|---|---|---|
| F1_v3 eval cycle for r=64 | step-8000 LoRA @ commit `5a9b458467` (sha256 `f12f31d8…3336`) | "Eval anchor is 80%-trained step-8000 LoRA (loss 0.2748, mean_token_acc 0.9348) not preregistered step-10000 due to host-terminator race during final save documented in `docs/p9_path_a_r64_step10k_reconcile_landed_2026_05_04.ai.md`" |
| `p9_sft.cond.path_a_lora_train_complete` roadmap node | status: `PARTIAL_VERIFIED_8K_TERMINAL` (was `PARTIAL_VERIFIED_8K`) | step-10000 permanently lost; this is final state |
| Track B r=16 launch | apply design lessons from `host_pod_terminator_fix_landed_2026_05_04.ai.md` (already landed) | + recommend train_llama_lora.py change to write TRAIN_DONE.json BEFORE final-save (decoupling marker from final-adapter-save success) |

## Design lesson carryover (Track B + future runs)

Already landed via `host_pod_terminator_fix_landed_2026_05_04.ai.md`. Additional recommendations:

- **train_llama_lora.py**: write `TRAIN_DONE.json` IMMEDIATELY after `trainer.train()` returns AND BEFORE `save_model('final')`. Decouples DONE marker from final-adapter-save success.
- **Terminator grace window**: when `STEP=max_steps AND ALIVE=0 AND DONE=0`, retry probe at +60s/+120s before declaring error-path. Costs ~$0.10/run worst-case; eliminates false-error termination pattern that destroyed step-10000.
- **Pre-create artifacts/ dir on Mac side** before launching watcher, so error-branch scp succeeds and we have train.log evidence even on bad terminations.

## Honest C3 caveats (raw#10)

(a) **Terminator log captured symptom not cause-discriminator**: log shows DONE=0 ALIVE=0 STEP=10000 but NOT the train.log tail past step-8008. The `scp` recovery in error-branch was structurally guaranteed to fail (script did not `mkdir -p artifacts/` first). So "training reached step 10000 cleanly vs crashed at step 9999" is forever unresolvable in this run. Does not affect step-10000 absence diagnosis but does mean cause-rank 1 vs 2 cannot be discriminated to better than the 0.85/0.10 split.

(b) **HF API audit is comprehensive but bounded**: full commit chain to initial commit, full tree at HEAD, refs (branches+tags) — all retrieved live. But HF Hub does not expose deleted-commit history, git GC events, push attempts that 401'd, or server-side telemetry on aborted uploads. The diagnosis "step-10000 commit was never created" is provable; the diagnosis "no push attempt was made" is inferred from HF API showing no rejected/orphan refs but cannot be proven (HF would not retain a record of a connection that died mid-upload before commit publish).

(c) **Retroactive recovery is fully blocked**. Pod `29dhlqk508ugoc` was terminated via `runpodctl pod delete` which is hard-destroy on RunPod (pod-state poll returns null per cost_analysis caveat (b); ssh refused per this audit). RunPod does not preserve container disk state after delete. There is no mechanism — paid or unpaid — to recover the step-10000 weights from this run.

## Roadmap update proposal

```json
{"id":"p9_sft.cond.path_a_lora_train_complete","status_transition":"PARTIAL_VERIFIED_8K → PARTIAL_VERIFIED_8K_TERMINAL","ts":"2026-05-04T13:42:00Z","cycle_ref":"p9_path_a_r64_step10k_reconcile_2026_05_04","reason":"step-10000 absence on HF confirmed via live API; pod 29dhlqk508ugoc terminated and unrecoverable; no remediation path exists at $0; r=64 status is final"}
```

## Files written this cycle

- `state/p9_path_a_r64_step10k_reconcile_2026_05_04/hf_api_audit.json`
- `state/p9_path_a_r64_step10k_reconcile_2026_05_04/diagnosis.json`
- `docs/p9_path_a_r64_step10k_reconcile_landed_2026_05_04.ai.md` (this file)
- `state/markers/p9_path_a_r64_step10k_reconcile_landed.marker`

## Compliance

- **raw#9 STRICT**: no .py written or modified; pure curl + python3 -m json.tool + ssh CLI
- **raw#15**: no token leakage; bearer read from `~/.cache/huggingface/token` via `$TOKEN` var; all paths repo-relative
- **raw#71**: read-only diagnosis; zero HF mutations; zero git ops; zero re-training launched
- **raw#10**: 3 honest C3 caveats above (terminator-log-evidence-bound + HF-API-bounds + retroactive-recovery-blocked)
- **$0**: zero pod spend in this cycle; zero re-training authorized
