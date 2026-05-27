# P9 Path A — Llama-3.2-3B LoRA Training COMPLETE 2026-05-04

**Cycle**: BG-ι day-2 completion verdict on P9 Path A LoRA SFT (pod `29dhlqk508ugoc`).
**Sister docs**: `docs/p9_path_a_completion_audit_landed_2026_05_03.ai.md` (post-mortem audit, day-1, 21:30Z), `docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md` (canonical alias plan), `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` (anchor switch).
**Constraints honored**: raw#9 (no .py on Mac; pod-side py was transient and is now gone), raw#10 (≥4 honest C3 caveats below), raw#15 (repo-relative paths), READ-ONLY for committed files, NO git ops in this cycle.

---

## TL;DR (handoff)

- **Final step**: 10000 / 10000 reached at `2026-05-03T21:34:08Z` per `state/p9_path_a_llama_lora_2026_05_03/host_terminator.log` (last monotonic probe). Pid disappeared in same 10-min window without `TRAIN_DONE.json` flush, so terminator took the error-path branch.
- **Verdict**: `COMPLETE_PROBABLE` — training reached final step (high confidence); HF push of `final/` adapter remains live-unverified (medium confidence). The day-1 audit ranked clean-completion at 60% / final-save crash at 25%.
- **Cost actual**: $22.18 (7.418 h × $2.99/hr) vs projected $21.50 → **+3.2% over projection**, 44% of $50 per-pod cap, well within the $85 hard cap.
- **F1_v3 eval readiness**: **CONDITIONAL — gated on HF re-auth + `siblings` enumeration**. Day-2 status (Mac side) shows `hf auth whoami` still returns `Invalid user token`; recovery path unchanged from day-1 audit recommendation.
- **Next-cycle trigger**: HF re-auth → `hf models info dancinlab/p9-llama32-lora-stage1` → if `adapter_model.safetensors` confirmed → naming-decision rename workflow → A' base-validation gate (`p9_sft.cond.benchmark_a_prime_base_validation`) → F1_v3 eval against {HellaSwag, MMLU 0-shot, TriviaQA EM}.

---

## 1. Training trajectory (final timeline)

Source: `state/p9_path_a_llama_lora_2026_05_03/host_terminator.log`, complete monotonic step progression, 10-min cadence.

| elapsed | timestamp | step | progress |
|---:|---|---:|---:|
| 0 min | 2026-05-03T14:43:21Z (watcher start ≈ pod start +34min) | — | — |
| 60 min | 2026-05-03T15:43:24Z (extrapolated) | ~1400 | 14% |
| 210 min | 2026-05-03T18:03:23Z | 5111 | 51.1% |
| 351 min | 2026-05-03T20:23:53Z | 8427 | 84.3% |
| 391 min | 2026-05-03T21:04:02Z | 9372 | 93.7% |
| 411 min | 2026-05-03T21:24:06Z | 9843 | 98.4% |
| 421 min | **2026-05-03T21:34:08Z** | **10000** | **100.0%** ALIVE=0 |

**Step rate**: ~23.4 steps / min averaged over 391–411 min window (consistent with the 2.46 s/iter projection from `state/p9_path_a_health_audit_2026_05_03/cost_projection.json`).

**Cost band actual**:
- Pod create → delete = 7.418 h (verified `state/p9_path_a_completion_audit_2026_05_03/cost_analysis.json`).
- Effective spend: $22.18, +$0.68 over $21.50 projection = +3.2% (within ±10% acceptance band).

---

## 2. Final state

**On-disk artifacts** (Mac, `state/p9_path_a_llama_lora_2026_05_03/`):
- `host_terminator.log` — complete probe timeline (final entry: `pod terminated (error path)` 21:34:13Z, then `watcher exit`).
- `verdict.json` — initial launch verdict (`LAUNCH_OK_AWAITING_TRAIN_COMPLETION`); not updated post-training.
- `F1_v3_pending.json` — pre-train pending marker; still pending.
- No `artifacts/` directory was created (the watcher's scp call failed: `open local "...artifacts/train.log": No such file or directory` because `mkdir -p artifacts` is only on the DONE branch, not the error branch — see `host_pod_terminator.sh.txt` lines 48 vs 65).

**Pod state**: terminated and unreachable (`ssh ... -p 14783 root@103.207.149.110` → `Connection refused`, confirmed 2026-05-04T06:57Z). RunPod GraphQL `pod(id:"29dhlqk508ugoc")` returns null per day-1 audit. **No on-pod recovery is possible.**

**Anomalies**:
1. Watcher's error-path branch fired despite `STEP=10000/10000` reached — race window between pid exit and `TRAIN_DONE.json` write (script writes the marker AFTER `trainer.save_model('final')` and `tok.save_pretrained`, both of which can take seconds-to-minutes for a 3B-param adapter).
2. Error-branch scp failed silently because the watcher script's `mkdir -p artifacts` only exists in the DONE branch (line 47 of `host_pod_terminator.sh.txt`), not in the error branch (line 63-65). Result: `train.log` never made it back to Mac.
3. No NaN/inf evidence (loss trajectory was clean through audit checkpoint at step 1090 per `state/p9_path_a_health_audit_2026_05_03/health.json`); no later loss snapshots exist on Mac side.

**Verdict**: `COMPLETE_PROBABLE` — step 10000 definitive, final adapter HF push circumstantial. See §3 for ranked causes.

---

## 3. F1_v3 readiness — prerequisite chain

Per `.roadmap.p9_sft cond.3` and `cond.benchmark_a_prime_base_validation`, F1_v3 verdict requires:

```
[1] Path A LoRA training complete                           ← THIS CYCLE: COMPLETE_PROBABLE
       ↓
[2] HF push of adapter live-verified                        ← BLOCKED on hf auth re-login
       ↓
[3] cond.benchmark_a_prime_base_validation = PASS           ← unmet (separate BG, ~6-17h ubu1)
       ↓
[4] F1_v3 eval pipeline runs on Llama base + Llama+LoRA     ← awaits [2] + [3]
       ↓
[5] cond.3 verdict emit __P9_F4_VERDICT__                   ← awaits [4]
```

**Status today (2026-05-04)**:
- [1] ✅ probable (this doc)
- [2] ❌ Mac `hf auth whoami` still `Invalid user token` (verified now); recovery path unchanged
- [3] ❌ unmet, separate BG cycle not yet launched
- [4]/[5] gated on [2]+[3]

**Can F1_v3 eval run now?** **NO.** Two prerequisites missing: HF re-auth (5-min unblock) AND base-validation gate (6-17h cycle on ubu1, $0). The 5-min HF re-auth is the cheap gate to flip first because it determines whether the entire 7.4h / $22.18 LoRA spend converted into a usable artifact at all.

---

## 4. Honest C3 (raw#10)

1. **Probe-cadence completion-detection lossy**: the Mac-side `host_terminator.log` captured `STEP=10000/10000 ALIVE=0 DONE=0` in a single 10-min window, conflating "training finished cleanly + final save took longer than poll budget" with "training crashed at step 10000". The 60/25/10/4/1 attribution from the day-1 audit is statistical, not falsifiable from on-disk evidence alone. Final adapter integrity cannot be confirmed without reaching HF.
2. **Checkpoint integrity unverified**: no sha256 / parameter-rank verification has been performed on any pushed `adapter_model.safetensors`. We have not even confirmed the file exists on the HF mirror — the `siblings` enumeration that would confirm presence requires HF auth that is currently broken on Mac. `hub_strategy="every_save"` should have produced 5 commits (steps 2k/4k/6k/8k/10k) but the last save_step boundary is exactly step 10000, which is the same step that crashed; if the crash happened mid-`save_steps` callback, even the step-10k commit may be incomplete.
3. **Cost actual vs projected discrepancy**: +3.2% over projection ($22.18 vs $21.50) — within band, but the +$0.68 delta partially reflects 18 minutes of pod-create overhead that wasn't fully amortized into the projection's per-step rate. For the next training pod, the projection model should add a fixed $0.90 pod-overhead term up front rather than absorbing it into step rate.
4. **Silent-failure surfaces not visible**: NaN/inf loss, OOM at final save, HF push 401/timeout, network partition during step-10k commit — none of these are observable from the surviving Mac-side artifacts. The watcher's error-branch was supposed to scp `train.log` back, but the `mkdir -p` was missing from that branch (see §2 anomaly 2), so even the diagnostic log never made it home. **This is a watcher-script bug** that should be fixed before the next training launch (recommendation: move `mkdir -p artifacts` to the top of the script, before the polling loop).
5. **F1_v3 vs F1_v2 superseding**: `F1_v3_pending.json` references the BLEU-1 holdout-500 v2 falsifier semantics. Per `.roadmap.p9_sft cond.3` note, F1 was upgraded to v3 (3-benchmark lm-eval composite per A' switch) on 2026-05-03. The pending marker pre-dates this upgrade; the eval cycle when it fires must use F1_v3 logic (`docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §2.4), not the v2 BLEU-1 path.

---

## 5. Next-cycle handoff

**Unblocks (assuming HF push verifies)**:
1. **A' base-validation gate** (`p9_sft.cond.benchmark_a_prime_base_validation`, currently `unmet`) — separate BG cycle on ubu1, ~6-17h wall, $0 (local).
2. **F1_v3 eval pipeline** (`p9_sft.cond.3`) — runs after base-validation passes; produces `__P9_F4_VERDICT__` emit.
3. **Paradigm A vs D cross-axis verdict** (`tool/p9_a_d_cross_axis_verdict.hexa`) — composes Path A (this cycle, Φ★-axis) with Path D (logit-axis distill, `state/p9_paradigm_d_distill_2026_05_03/`).
4. **HF savepoint canonical-alias rename** (`docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md`) — `hf repos move` from `p9-llama32-lora-stage1` → `llm-llama32-3b-paradigm-a-prime-sft-stage1`.

**Recommended ordering** (next session):
1. (5 min) `hf auth login --force` on Mac OR run from ubu1 if its token is still valid.
2. (5 min) `hf models info dancinlab/p9-llama32-lora-stage1` → confirm `adapter_config.json` + `adapter_model.safetensors` + tokenizer files in `siblings`. If `final/` is missing, accept `step-10000` as fallback.
3. (10 min) Execute naming-decision post-completion workflow: manifest dump → `hf repos move` → re-upload finalized README.
4. (BG, 6-17h) Launch base-validation BG per `.roadmap.p9_sft cond.benchmark_a_prime_base_validation` on ubu1.
5. (BG, ~2-4h) Launch F1_v3 eval BG once both [2] and base-validation are GREEN.

---

## 6. Roadmap update proposal (DO NOT apply — propose only)

A new cond is the cleanest representation. Append to `.roadmap.p9_sft` `required_conditions`:

```jsonl
{"id":"p9_sft.cond.path_a_lora_train_complete","desc":"P9 Path A LoRA SFT training reached step 10000/10000 on RunPod H100 SXM (pod 29dhlqk508ugoc). Cost actual $22.18 vs projected $21.50 (+3.2%). HF push of final adapter circumstantial PROBABLE; live-verify gated on Mac hf auth recovery. F1_v3 evaluation NOT yet runnable — chains through cond.benchmark_a_prime_base_validation.","verifier":{"type":"manual_review","manual_override_path":"state/markers/p9_path_a_lora_train_complete.marker","status_emit":"__P9_PATH_A_LORA_TRAIN__ <COMPLETE|COMPLETE_PROBABLE|INCOMPLETE|UNKNOWN>"},"status":"met","evidence":["state/p9_path_a_llama_lora_2026_05_03/host_terminator.log final entry STEP=10000/10000 at 2026-05-03T21:34:08Z","state/p9_path_a_completion_audit_2026_05_03/cost_analysis.json $22.18 / 7.418h","state/p9_path_a_llama_lora_2026_05_03/verdict_complete.json","docs/p9_path_a_completion_audit_landed_2026_05_03.ai.md (day-1 post-mortem)","docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md (day-2 verdict + handoff)"],"blocker_reason":"","ts":"2026-05-04","cross_link":{"chains_to":["p9_sft.cond.benchmark_a_prime_base_validation","p9_sft.cond.3"],"f1_v3_eval_blocked_on":["HF auth recovery on Mac (5min)","cond.benchmark_a_prime_base_validation = PASS"],"sister_cycle":"p9_path_a_completion_audit (day-1 post-mortem)"}}
```

**Status emit**: `__P9_PATH_A_LORA_TRAIN__ COMPLETE_PROBABLE`.

**Why a new cond rather than mutating cond.2**: cond.2 is the broader S3 9-combo sweep, of which Path A is one combo (the Φ★-axis anchor). Path A standing alone has its own completion semantics distinct from "all 9 combos finished".

---

## 7. Outputs

- `docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md` — this handoff.
- `state/p9_path_a_llama_lora_2026_05_03/verdict_complete.json` — machine-readable verdict (Deliverable B).

Inputs referenced (read-only):
- `state/p9_path_a_llama_lora_2026_05_03/host_terminator.log`
- `state/p9_path_a_llama_lora_2026_05_03/host_pod_terminator.sh.txt`
- `state/p9_path_a_llama_lora_2026_05_03/train_llama_lora.py.txt`
- `state/p9_path_a_llama_lora_2026_05_03/verdict.json`
- `state/p9_path_a_llama_lora_2026_05_03/F1_v3_pending.json`
- `state/p9_path_a_llama_lora_2026_05_03/runpod_pod_info.json`
- `state/p9_path_a_health_audit_2026_05_03/cost_projection.json`
- `state/p9_path_a_health_audit_2026_05_03/health.json`
- `state/p9_path_a_completion_audit_2026_05_03/cost_analysis.json`
- `state/p9_path_a_completion_audit_2026_05_03/hf_push_status.json`
- `state/p9_path_a_completion_audit_2026_05_03/termination_cause.json`
- `docs/p9_path_a_completion_audit_landed_2026_05_03.ai.md` (sister)
- `docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md` (sister)
- `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` (anchor switch)
- `.roadmap.p9_sft` (cond.3, cond.benchmark_a_prime_base_validation reference)
