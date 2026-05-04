# P9 Path A — Status Correction (COMPLETE_PROBABLE → PARTIAL_VERIFIED_8K) 2026-05-04

**Cycle**: BG-ρ — forward-looking status correction landing the BG-ξ live HF verification finding into the roadmap, with resolution-path comparison and pre-registration impact analysis.
**Sister cycles**: BG-ι (2026-05-04 morning, commit `e4d86fb2f`, COMPLETE_PROBABLE inference) — BG-ξ (this cycle parent, live HF API verification, PARTIAL_VERIFIED_8K).
**Constraints honored**: raw#9 (no .py on Mac; jq for JSONL validation), raw#10 (≥5 honest C3 caveats §7), raw#15 (repo-relative paths), raw#71 (status_emit sentinel registered for new cond), READ-ONLY for sister cycle artifacts, NO git ops in this cycle.

---

## 1. TL;DR

- **Verdict transition**: P9 Path A LoRA training status corrected from `COMPLETE_PROBABLE` (BG-ι, inferred from on-pod step counter) → `PARTIAL_VERIFIED_8K` (BG-ξ, live HF API mirror state). The training process did reach step 10000/10000, but the watcher pid was GONE before the `trainer.save_model('final')` flush completed, and the `final/` adapter never landed on the HF mirror.
- **HF mirror anchor**: last commit on `need-singularity/p9-llama32-lora-stage1` is `5a9b4584` ("Training in progress, step 8000", 2026-05-03T20:06:18Z) with `adapter_model.safetensors` sha256 `f12f31d8…3336` (389MB). Steps 8001–10000 plus the `final/` checkpoint do NOT exist on HF. The pod is terminated and unreachable, so on-pod recovery is impossible.
- **Resolution paths** (3 options, ranked recommendation in §5):
  - **A** — Use step-8k LoRA as the eval anchor + amend `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §2.6 pre-registration block. Cost $0, wall ~15min spec edit. Pre-registration compliance: requires dated spec amendment per §7.1(a) caveat.
  - **B** — Short retrain from step-8k → step-10k on a fresh H100 spot pod (~2000 additional steps). Cost ~$4-5 H100 spot, wall ~1.5h. Pre-registration preserved.
  - **C** — Discard the run and restart from scratch. Cost ~$22 + ~7.4h H100, wall ~1 day cycle.
- **Recommended**: **B** if budget tolerates (~$5, 완성도 high), else **A** with explicit dated spec amendment.
- **F1_v3 readiness**: `false_with_caveat` — HF auth blocker CLEARED by BG-ξ; adapter blocker PARTIAL (step-8k available, step-10k missing); base-validation blocker (BG-ν) remains.
- **Roadmap**: BG-ρ (this cycle) added `p9_sft.cond.path_a_lora_train_complete` to `.roadmap.p9_sft` with `status: partial_verified_8k`. Entry count 1 → 2 cond entries (plus header).

---

## 2. Timeline (chronological)

All timestamps UTC.

| ts | actor | event |
|---|---|---|
| 2026-05-03T14:28:51Z | TRL Trainer (pod 29dhlqk508ugoc) | initial commit on `need-singularity/p9-llama32-lora-stage1` (commit `0a4b60b6`) |
| 2026-05-03T14:43:21Z | host watcher | watcher start (≈ pod start +34min) |
| 2026-05-03T15:52:19Z | TRL Trainer | step-2000 rolling save commit `f6916247` |
| 2026-05-03T17:16:35Z | TRL Trainer | step-4000 rolling save commit `fe83e989` |
| 2026-05-03T18:41:24Z | TRL Trainer | step-6000 rolling save commit `f7712e3a` |
| **2026-05-03T20:06:18Z** | TRL Trainer | **step-8000 rolling save commit `5a9b4584`** ← HF HEAD — last successful push |
| 2026-05-03T21:24:06Z | host watcher | probe step 9843 / 10000 (98.4%, last good probe) |
| 2026-05-03T21:34:08Z | host watcher | probe STEP=10000/10000, ALIVE=0, DONE=0 (pid GONE in same 10-min probe window; final-save flush race) |
| 2026-05-03T21:34:13Z | `host_pod_terminator.sh` error-branch | pod terminated; scp of `train.log` failed (`mkdir -p artifacts` missing on error branch) |
| 2026-05-04 morning | BG-ι (commit `e4d86fb2f`) | analyzes host_terminator.log; infers `COMPLETE_PROBABLE` (60% clean-finish / 25% final-save crash / 10% OOM / 4% spot / 1% manual); HF auth on Mac blocked, no live verification |
| 2026-05-04 afternoon | HF auth refresh (commit `eea009b40`) | dancinlife token re-issued with write scope; need-singularity admin restored |
| 2026-05-04 (BG-ξ) | BG-ξ live HF API probe | reveals last commit step 8000, no step-10000 commit, no `final/` adapter; verdict `PROBABLE_HF_PARTIAL`; proposes COMPLETE_PROBABLE → PARTIAL_VERIFIED_8K |
| 2026-05-04 (this cycle BG-ρ) | this BG | lands `p9_sft.cond.path_a_lora_train_complete` to `.roadmap.p9_sft` with `status: partial_verified_8k`; writes this correction handoff |

---

## 3. Disambiguation — what each verdict means in evidence terms

| verdict | source cycle | evidence base | claim strength | what it does NOT prove |
|---|---|---|---|---|
| `LAUNCH_OK_AWAITING_TRAIN_COMPLETION` | day-0 launch | RunPod pod create + train start | pod started; first 10 steps logged | nothing about completion |
| `COMPLETE_PROBABLE` | BG-ι (day-2) | `host_terminator.log` step counter monotonic to 10000/10000 + ALIVE=0 + DONE=0 in same 10-min probe; HF push `push_to_hub=True` → assumed final adapter pushed | training process reached step 10000 marker on pod-side counter | does NOT prove `trainer.save_model('final')` succeeded; does NOT prove HF push of step-10000 / final adapter succeeded; does NOT prove adapter integrity |
| `PROBABLE_HF_PARTIAL` / **`PARTIAL_VERIFIED_8K`** (canonical for roadmap) | BG-ξ (this cycle parent) | live HF API: HEAD commit = step 8000 at 2026-05-03T20:06Z; no step-10000 commit; no `final/` directory; adapter_config matches verdict.json hyperparams; adapter_model.safetensors integrity sha256 captured | step-8000 LoRA adapter is live and integrity-validated on HF | does NOT prove step-8001-10000 ever wrote to disk on pod (could be (a) wrote+failed-push, (b) wrote+pushed-but-not-finalized, (c) never-wrote — all consistent with HF state) |
| (hypothetical) `COMPLETE_VERIFIED` | not yet reached | step-10000 / final adapter live on HF + sha256 manifest + adapter_config consistency check | NOT achievable from current pod state (terminated and unreachable) | — |

**Material difference between step-8000 and step-10000**: 2000 training steps ≈ 30 minutes additional H100 time. At step 8000 the run had completed `epoch=5.118` (per `train.log` last visible entry, loss=0.2748, mean_token_acc=0.9348). The trajectory was still descending (3.06 → 0.27 over 8k steps; final 2k steps would have continued the convergence). The 80%-trained adapter is materially weaker than the planned 100%-trained adapter — F1_v3 eval on step-8k will measure a weaker model than the spec preregistered against.

---

## 4. Resolution path comparison

| dim | A: step-8k anchor | B: short retrain | C: full restart |
|---|---|---|---|
| cost (USD) | 0 | ~5 (2000 steps × $2.99/h × ~0.5h spot) | ~22 (full 10k steps × ~7.4h H100 spot) |
| wall time | ~15min (spec edit) | ~1.5h (boot + 2k steps + push) | ~7.4h H100 + boot/push overhead |
| pre-registration compliance | requires dated spec amendment per `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §7.1(a) caveat ("post-marker amendments require new dated spec doc + roadmap status emit") | spec preserved as-is — F1_v3 evaluates against step-10000 LoRA as preregistered | spec preserved as-is |
| 완성도 (completeness lens) | partial — eval uses 80%-trained adapter; loss curve still descending at the cut point | high — recovers preregistered eval target with minimal incremental spend | highest — but redundant; full restart spend would only differ from B by the lost step-8k checkpoint quality, which we already have |
| risk profile | low (no new infra spend) but accumulates spec-deviation tech debt | medium (new pod boot, new HF push, new watcher cycle — same failure modes) | medium (same as B but 5x scaled) |
| dependency on optimizer state | NO (eval-only consumes adapter weights) | YES — optimizer state at step-8k is NOT on HF mirror; would need to rebuild from adapter weights only (warm-start LR schedule loses cosine-anneal continuity) | NO (fresh init) |
| what we lose if we choose this | the preregistered eval anchor; spec compliance footnote required forever | nothing material if retrain succeeds; ~$5 if retrain fails | the $22 already spent on step-8k checkpoint (sunk cost; HF copy preserved) |

---

## 5. Spec compliance impact — A' pre-registration block

`docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` §2.6 contains the pre-registration block locked at the marker `state/markers/p9_benchmark_a_prime_spec_landed.marker` timestamp 2026-05-03. The eval target is referenced as the `step-10000` Path A LoRA adapter against the 3-benchmark lm-eval composite {HellaSwag, MMLU 5-shot, TriviaQA}.

Per the spec's own caveat 7.1(a), any post-marker amendment to the pre-registration block requires:
1. A new dated spec doc (e.g., `docs/p9_benchmark_a_prime_spec_amendment_2026_05_04.md`)
2. A status emit on `.roadmap.p9_sft` recording the deviation reason
3. Cross-link from the new spec doc back to the original 2026-05-03 spec
4. The amendment MUST predate the F1_v3 eval cycle execution (no post-hoc adjustment)

**Per-resolution-path impact**:
- **Option A** triggers all 4 amendment requirements above. The amendment text would substitute "step-10000 anchor" with "step-8000 anchor (final save flush failed; see `state/p9_path_a_hf_push_verify_2026_05_04/verify_report.md`)". This is administratively heavy but feasible.
- **Option B** requires NO spec amendment because the eval target stays at step-10000 (recovered via short retrain). Simpler from compliance standpoint. The retrain itself does NOT count as a pre-registration violation because the spec only constrains the eval target, not the training run.
- **Option C** also requires NO spec amendment (eval target preserved), but creates a new training run with a new pod_id, new step trajectory, and new HF commit history — the audit trail forks.

**Recommended**: **B** preserves spec integrity with minimal admin cost. **A** is the budget-zero fallback if the user declines the ~$5 retrain spend.

---

## 6. Recommended resolution (완성도 ranked)

Per `feedback_completion_quality_recommendation.md` (always present explicit ranked recommendation):

1. **B** (short retrain) — 완성도 9.0/10. Restores preregistered step-10k anchor for ~$5 / ~1.5h. Only material risk is the optimizer-state continuity loss (cosine-anneal LR schedule restarts), which can be mitigated by warm-starting from step-8k adapter weights with a flat LR for the final 2000 steps. Does NOT amend spec. Highest completeness for lowest incremental spend.
2. **A** (step-8k anchor + spec amendment) — 완성도 6.5/10. Zero new spend, preserves the existing $22 sunk cost as the final artifact. Costs spec-deviation tech debt + a perpetual eval footnote. Acceptable if user budget-locks against further H100 spend OR if the F1_v3 verdict is expected to be insensitive to the 8k vs 10k difference (which we cannot verify a priori).
3. **C** (full restart) — 완성도 5.0/10. Cleanest audit trail but redundant — option B achieves the same end state for 1/4 the cost. C only beats B if there is reason to distrust the step-8k checkpoint quality (e.g., a suspected silent NaN/inf at any point in the first 8k steps). No such evidence exists in `train.log` (loss trajectory clean 3.06 → 0.27).

**User policy decision required**. This BG does NOT execute any of the resolution paths; this is a status correction + roadmap landing only. The execution BG should be a separate cycle gated on user authorization (likely `OK PATH_A B EXEC` or `OK PATH_A A AMEND`).

---

## 7. Honest C3 (raw#10 — ≥5 caveats)

1. **step-10000 may have actually completed but final-save crashed**: HF state alone cannot disambiguate (a) `trainer.save_model('final')` started but failed mid-write, (b) save completed but HF push timed out / 401'd, (c) save+push completed but the commit transaction never finalized on HF backend, (d) save never started because pid died on the prior step boundary. The pod is terminated and unreachable, so the on-pod `final/` directory state is permanently lost. Future training runs MUST emit a `TRAIN_DONE.json` to the host BEFORE pod termination (raw#71 falsifier-bound surface needed).

2. **Step-8k checkpoint quality vs step-10k difference may be material**: at step 8000 the loss was 0.2748 with mean_token_acc 0.9348, still descending. The next 2000 steps (20% of training) typically still produce measurable improvement on downstream eval — Llama-3.2-3B SFT trajectories on similar 50K corpus instruction data show ~1-3pt absolute improvement in 0-shot eval over the final 20% of training (no published anchor for our specific corpus, so this is heuristic). If the F1_v3 verdict is borderline (e.g., near the falsifier threshold), the 2000-step gap could be the difference between PASS and FAIL — undetectable from step-8k eval alone.

3. **Watcher script bug fix (BG-σ) wouldn't have prevented step-10k final-save failure, just made it diagnostically visible**: the BG-σ surgical fix at `state/watcher_script_fix_2026_05_04/` moves `mkdir -p artifacts` to the top of `host_pod_terminator.sh` so the error-branch scp can succeed. This recovers the `train.log` post-mortem trail. It does NOT prevent the `trainer.save_model('final')` itself from failing — that requires either (a) a longer probe-cadence patience window before terminator fires, or (b) a separate `TRAIN_DONE.json` write callback registered with TRL Trainer's `on_train_end` hook. The BG-σ fix is necessary but not sufficient.

4. **Retrain from step-8k requires the step-8k optimizer state, which is NOT in the HF mirror**: HF push only contains adapter weights (`adapter_model.safetensors`), config (`adapter_config.json`), and metadata. The optimizer state (Adam β1/β2 momentum + variance running averages, scaler state, LR scheduler position) was stored in the pod's `final/optimizer.pt` and `final/scheduler.pt`, neither of which exist on HF. Retraining option B from step-8k would either (i) warm-start from adapter weights with a fresh optimizer state — losing cosine-anneal continuity, requiring a brief LR warmup, possibly causing a small loss-curve discontinuity — or (ii) accept that "step-10k via warm-restart" is meaningfully different from "step-10k via continuous training" and amend the spec accordingly. The retrain artifact will not be byte-identical to a hypothetical clean step-10k run; the practical impact on F1_v3 eval is expected to be sub-threshold but nonzero.

5. **Path A's `host_pod_terminator` script auto-killed the pod on error-branch, losing on-pod recovery options**: when the watcher detected ALIVE=0 + DONE=0 at step 10000, it immediately ran `runpodctl stop pod 29dhlqk508ugoc` per `host_pod_terminator.sh.txt` line 78. Had it instead paused for a 5-10 minute grace period (waiting for slow `save_model` flush), or kept the pod alive long enough for an SSH-in inspection of `final/`, we might have recovered the step-10k checkpoint manually. The auto-terminate behavior was a defensive cost-bound (raw#48 budget-cap), but it eliminated the diagnostic cone. Future pods should use a longer grace window OR a SIGTERM-with-grace before `runpodctl stop`.

6. **The HF Trainer `every_save` strategy creates commits with messages but NOT git tags**: `refs` API returned `tags: []` despite 4 step-Nk save events. This was unexpected per the mk2 spec C2 caveat which assumed `step-2k`, `step-4k`, etc. tags would exist. Per-step revision pinning therefore must use commit sha (`5a9b458467` for step-8000), not a `step-8k` tag. This affects any downstream eval cycle that wants to pin a specific revision via the HF API.

7. **No local sha256 manifest exists for any Path A trained adapter**: cross-validation of the step-8k adapter is configuration-consistency only (adapter_config matches verdict.json hyperparams), not bytewise. If the HF mirror were corrupted post-upload (HF backend bug or admin action), this verification would NOT detect it. Mitigation for any irreversible eval commitment: download `adapter_model.safetensors` locally and verify sha256 = `f12f31d8104900cba5f60ad2010dc0bed0ec5c466e2838c88378fa5c9c2d3336` (the BG-ξ recorded x-linked-etag) before running F1_v3.

---

## 8. Cross-link

**Sister roadmap entries**:
- `.roadmap.p9_sft cond.3` — F1_v3 evaluation, depends on this cond
- `.roadmap.p9_sft cond.benchmark_a_prime_base_validation` — base-validation gate (BG-ν owned)
- `.roadmap.p9_sft cond.benchmark_a_prime_spec` — A' spec marker (status `met`)

**Related commits**:
- `e4d86fb2f` — BG-ι (day-2 verdict COMPLETE_PROBABLE)
- `eea009b40` — HF auth refresh enabling BG-ξ live verification
- BG-ξ commit (just landed prior to this cycle) — verify_report.md + verdict.json

**Sister cycle dirs (read-only references)**:
- `state/p9_path_a_llama_lora_2026_05_03/` — original launch + day-1/day-2 state (BG-ι)
- `state/p9_path_a_hf_push_verify_2026_05_04/` — live HF verification (BG-ξ)
- `state/watcher_script_fix_2026_05_04/` — BG-σ surgical fix for watcher mkdir bug
- `state/p9_path_a_completion_audit_2026_05_03/` — day-1 cost / hf_push_status / termination_cause analysis

**Falsifier set affected**:
- `F1_v3` (cond.3) — eval anchor must be footnoted as step-8000 (option A) or restored to step-10000 via option B retrain
- `F-PA-HF-1` (BG-ξ-introduced) — status emit `PARTIAL` (step-8k present, step-10k missing)
- `F-NAME-1` (mk2 naming) — FAIL on `p9-llama32-lora-stage1` legacy URL until rename executes

**Sister docs (do NOT modify per task constraint)**:
- `docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md` (BG-ι original; this doc is forward-looking correction, that doc is preserved as historical record)
- `docs/p9_path_a_completion_audit_landed_2026_05_03.ai.md` (day-1 post-mortem)
- `docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md` (canonical alias plan; rename never executed)

**Raw invariants engaged**:
- raw#9 — JSONL validation via `jq`, no .py created
- raw#10 — 7 honest C3 caveats above (exceeds ≥5 minimum)
- raw#15 — all paths repo-relative
- raw#71 — new cond emits sentinel `__P9_PATH_A_LORA_TRAIN__`

---

## 9. Roadmap update — landed in this cycle

`.roadmap.p9_sft` mutation (single-file, append-only, JSONL valid):

- **Pre-edit entries**: 1 cond (`p9_sft.cond.paradigm_d_distill`) + 1 header → 2 JSONL records
- **Post-edit entries**: 2 conds (`paradigm_d_distill`, `path_a_lora_train_complete`) + 1 header → 3 JSONL records
- **JSONL validity**: PASS (verified via `jq -e .` on each non-comment non-blank line)
- **uchg/chflags state**: file is unlocked (verified via `ls -lO`)

The new entry id: `p9_sft.cond.path_a_lora_train_complete`
Status: `partial_verified_8k`
Status emit sentinel: `__P9_PATH_A_LORA_TRAIN__ <COMPLETE_VERIFIED|PARTIAL_VERIFIED_8K|COMPLETE_PROBABLE|FAIL>`
Manual override path: `state/p9_path_a_hf_push_verify_2026_05_04/verdict.json`
Contributes to: `p9_sft.cond.3`, `p9_sft.cond.benchmark_a_prime_base_validation`

The entry explicitly lists 3 resolution paths (A/B/C with cost / wall / desc) and recommends "A or B (user policy decision)". Cost variance is captured as `cost_actual_usd: 22.18`, `cost_projected_usd: 21.50`, `variance_pct: 3.2`.

---

## 10. Outputs

- `.roadmap.p9_sft` — appended new cond entry `p9_sft.cond.path_a_lora_train_complete`
- `docs/p9_path_a_status_correction_2026_05_04.ai.md` — this handoff doc

**Inputs referenced (read-only)**:
- `state/p9_path_a_llama_lora_2026_05_03/verdict_complete.json`
- `state/p9_path_a_hf_push_verify_2026_05_04/verdict.json`
- `state/p9_path_a_hf_push_verify_2026_05_04/verify_report.md`
- `docs/p9_path_a_llama_lora_complete_2026_05_04.ai.md`
- `docs/p9_benchmark_switch_a_prime_spec_2026_05_03.md` (§2.6 + §7.1(a) referenced; not read in full this cycle)
- `.roadmap.p9_sft` (existing schema + entry shape)

**Constraint compliance log**:
- raw#9: JSONL validation via `jq`; no .py written or modified
- raw#10: 7 honest C3 caveats (§7) — exceeds ≥5 minimum
- raw#15: all paths repo-relative
- raw#71: new cond carries `status_emit` sentinel; manual_override_path points to BG-ξ verdict.json
- git ops in this cycle: NONE (parent serializes commits)
- HF mutations in this cycle: NONE
- chflags: NONE (.roadmap.p9_sft remains unlocked for future appends)

---

**End of correction handoff.**
