# commit message swap correction — 441ffe732 ↔ e9a914c97 (2026-05-04)

## Scope

Two commits landed during cycle-8 BG fan-out 3 (P9 SFT + HF upload mk2 parallel BG suite, 2026-05-03 → 2026-05-04 boundary) have **subject lines that do NOT match their content**. This doc is a forward-looking pointer for future blame/log readers; no history rewrite was performed.

## Root cause

Two parallel `Agent run_in_background=true` subagents (BG-δ owning P9 SFT track, BG-ε owning HF upload mk2 track) operated on the same git working tree concurrently. Each ran `git add <files>` followed by `git commit -m "..."`. Because git's index is a process-shared file, both BGs' staged file sets contaminated each other's commits when their `add → commit` windows overlapped.

The `subject` strings travel with the commit hash but the `tree` reflects whatever was actually staged at commit time. Result: subject↔content mismatch on 2 of the 8 commits in the c3ea60dd4..334266d28 range.

## Actual mapping

### `441ffe732` — subject says "state(p9 sft paradigm j 50k 2026-05-03): FAIL_J CUDA OOM at step 0 + comparison matrix"

**Actual content (19 files, +2478 LoC)**: 13 HF upload mk2 files + 6 P9 paradigm J 50k state files, mixed.

HF mk2 files in this commit:
- `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md`
- `docs/anima_hf_naming_mk2_spec_landed_2026_05_03.ai.md`
- `docs/anima_hf_upload_mk2_landed_2026_05_03.ai.md`
- `docs/anima_hf_upload_mk2_spec_2026_05_03.md`
- `state/hf_upload_audit/.gitkeep`
- `state/hf_upload_audit/20260503T151303Z_need-singularity__clm-v4-base-mirror.jsonl`
- `state/hf_upload_audit/20260503T151321Z_need-singularity__clm-v4-base-mirror.jsonl`
- `state/hf_upload_audit/20260503T151335Z_need-singularity__clm-v4-sft-stage1.jsonl`
- `state/hf_upload_audit/20260503T151341Z_need-singularity__clm-v4-base-mirror.jsonl`
- `state/hf_upload_ledger_2026_05.jsonl`
- `tool/hf_readme_template.md`
- `tool/hf_upload_mk2.hexa`
- `tool/hf_upload_mk2_pre_push_hook.hexa`

P9 paradigm J 50k files in this commit (matching subject):
- `docs/p9_paradigm_j_50k_landed_2026_05_03.ai.md`
- `state/p9_paradigm_j_50k_2026_05_03/comparison_matrix.json`
- `state/p9_paradigm_j_50k_2026_05_03/launch.log`
- `state/p9_paradigm_j_50k_2026_05_03/train.log`
- `state/p9_paradigm_j_50k_2026_05_03/trajectory.json`
- `state/p9_paradigm_j_50k_2026_05_03/verdict.json`

### `e9a914c97` — subject says "feat(hf upload mk2 2026-05-03): naming convention + upload pipeline + pre-push hook + dry-run audit ledger"

**Actual content (26 files, +107104 LoC)**: P9 a-prime + Path A track files only. **Zero HF files.** The body of this commit elaborately describes the HF mk2 feature (naming spec, pre-push hook, ledger schema, F-NAME-1, F-HF-UPLOAD-1) — that prose is accurate about HF mk2 itself, but those files actually live in `441ffe732`, not here.

P9 a-prime + Path A files in this commit:
- `docs/p9_a_prime_eval_pipeline_landed_2026_05_03.ai.md`
- `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md`
- `docs/p9_path_a_health_audit_landed_2026_05_03.ai.md`
- `docs/p9_path_a_naming_decision_2026_05_03.md`
- `docs/p9_path_a_naming_decision_landed_2026_05_03.ai.md`
- `state/p9_a_prime_main_eval_2026_05_03_verdict.json`
- `state/p9_a_prime_main_eval_pipeline_2026_05_03/{base_per_example_correctness,loader_smoketest,pipeline_meta}.json`
- `state/p9_a_prime_main_eval_pipeline_2026_05_03/{eval_llama_lora_ckpt,loader_smoketest,extract_base_per_example,run_all_lora_ckpts}.{py,sh}.txt`
- `state/p9_path_a_health_audit_2026_05_03/{cost_projection,health,watchdog_status}.json`
- `state/p9_path_a_llama_lora_2026_05_03/{F1_v3_pending,runpod_pod_info,verdict}.json`
- `state/p9_path_a_llama_lora_2026_05_03/{host_pod_terminator,launch_v3}.sh.txt`
- `state/p9_path_a_llama_lora_2026_05_03/{retemplate_to_llama,train_llama_lora}.py.txt`
- `state/p9_path_a_llama_lora_2026_05_03/host_terminator.log`
- `state/p9_path_a_naming_2026_05_03/README_canonical.md`
- `tool/p9_a_prime_verdict.hexa`

## Effect on tooling

- `git log --oneline` is misleading for these 2 hashes. Always cross-check with `git show --name-only <hash>` when reading either of them.
- `git blame` on any HF mk2 file points to `441ffe732` (paradigm-J subject). True authorship is the BG-ε HF upload mk2 BG.
- `git blame` on any P9 a-prime / Path A file points to `e9a914c97` (HF subject). True authorship is the BG-δ 6d sub-commit.
- Any future `git revert <hash>` on these two would unwind unexpected file sets — read the actual tree first.

## Why no history rewrite

- All file content is correctly present on `main` HEAD (verified via `git ls-files`).
- Working tree is consistent — only the commit message metadata is wrong.
- `git reset --soft <prior>` + sequential redo would fix the metadata but is destructive of in-flight reflog state and adds redo risk for negligible gain (2 commit subjects vs full sequential redo of 8 commits).
- User chose "안전하게" path 2026-05-04 → leave-as-is + this correction doc. Reversal-of-decision later is still possible via reflog (commits and their swapped contents reachable via `git reflog --all`).

## Honest C3 (raw#10)

1. This doc is the source of truth for the swap. If it is itself ever lost or moved, future readers have no other in-tree pointer.
2. The `441ffe732` body still claims "State-only (no source change)" — false: it lands `tool/hf_*.hexa` (3 source files). The `e9a914c97` body's HF mk2 prose is accurate-about-mk2 but mis-located.
3. No tests or build artifacts were affected by the swap — both commit subsets were lit-only / state-only / tool-only with no cross-track import dependencies. If future cycles hit a reproducibility issue tied to either hash, this doc is the first-stop diagnostic.
4. The race lesson is a session-protocol gap: parallel BG subagents that share a git working tree must serialize via per-BG `git worktree` or an external lockfile. Captured to memory under `feedback_parallel_bg_git_index_race.md`.

## Pointer block

- swap pair: `441ffe732` ↔ `e9a914c97`
- discovery cycle: 2026-05-04 BG-ε self-report (raw#10 honest C3 in BG-ε final report)
- BG-δ self-report cross-confirmation: same cycle, C3.1 + C3.2
- prior-cycle context: `state/docs_pending_audit_2026_05_04/audit_plan.md` (BG-γ)
