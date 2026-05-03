# Pending state/ docs/ audit — uncommitted-by-track plan (2026-05-04)

> read-only audit. NO git add / git commit / source-edit performed. raw#15 repo-relative paths.
>
> baseline ref: `c3ea60dd4` (anima-eeg cycle 8 followup) just landed; this audit re-runs `git status --short` and groups remaining residue by inferred track.

## 0. Overall counts

- 46 entries in `git status --short`
  - 40 untracked (`??`)
  - 4 modified tracked file (` M`)
  - 1 modified submodule (` m ready`)
  - 1 missing/untracked submodule path (`?  references/tribev2` — see Risk Flag #2)

---

## 1. Inventory by track

### 1.1 anima-eeg / anima-clm-eeg cycle-8 (already committed)

Empty — `c3ea60dd4` + `e2ce92413` covered the cycle-8 land. No leftover EEG-scoped files in the residue. PASS.

### 1.2 P9 SFT track (paradigm D, paradigm J, P1.5 ensemble, A' path, path A, path B)

Largest track. Spans benchmark-switch (A'), best-of-9 distill (D), 50K production (J), holdout-500 cv ensemble (P1.5), Llama-LoRA salvage path (Path A), and HellaSwag sanity probe (Path B).

| path | type | size | content hint |
|---|---|---|---|
| `.roadmap.p9_sft` | M | +1 line | adds `p9_sft.cond.paradigm_d_distill` cond entry (Mistral-7B → CLM v4 350M soft-logit distill, F-D-1) |
| `state/p9_a_prime_main_eval_2026_05_03_verdict.json` | ?? | small | A' main eval verdict (schema `anima/p9_a_prime_main_eval/verdict/1`, ref §2.4) |
| `state/p9_a_prime_main_eval_pipeline_2026_05_03/` | ?? | 28K | `eval_llama_lora_ckpt.py.txt`, `extract_base_per_example.sh.txt`, `loader_smoketest.{py.txt,json}` (`.py.txt` = raw#9 staged-not-executed) |
| `state/p9_p1_5_ensemble_2026_05_03/` | ?? | 1.0M | 4-seed reeval per-prompt JSONs (s43/44/45) + `compute_ensemble.py` (1 untracked .py — raw#9 RISK) + `verdict_4seed.json` |
| `state/p9_paradigm_d_25k_2026_05_03/` | ?? | 12K | `verdict.json` only (mini-run readout) |
| `state/p9_paradigm_d_50k_2026_05_03/` | ?? | 12K | `verdict.json` only (production readout) |
| `state/p9_paradigm_d_distill_2026_05_03/` | ?? | 24K | `launch_status.json` + `trajectory_reconstructed.json` + `verdict_reconstructed.json` (PARTIAL_PASS, 2000/2000 + post-loop silent exit) |
| `state/p9_paradigm_j_50k_2026_05_03/{comparison_matrix,launch.log,train.log,trajectory,verdict}.json` | ?? | 28K | FAIL_J: CUDA OOM at step 0 |
| `state/p9_path_a_health_audit_2026_05_03/` | ?? | 12K | `health.json`, `cost_projection.json`, `watchdog_status.json` |
| `state/p9_path_a_llama_lora_2026_05_03/` | ?? | 40K | `verdict.json` + `*.sh.txt` + `*.py.txt` (staged scripts) + `runpod_pod_info.json` + `host_terminator.log` |
| `state/p9_path_b_sanity_probe_2026_05_03/` | ?? | 84K | `result.json` + `hellaswag_raw.json` + `run.log` |
| `tool/p9_a_prime_verdict.hexa` | ?? | small | A' verdict computation tool (raw#9 hexa) |
| `docs/p9_a_prime_path_decision_landed_2026_05_03.ai.md` | ?? | — | A' path decision (CLM v4 base = ARCHITECTURAL_BLOCKER) |
| `docs/p9_p1_5_ensemble_4seed_landed_2026_05_03.ai.md` | ?? | — | holdout-500 cv verdict |
| `docs/p9_paradigm_d_distill_landed_2026_05_03.ai.md` | ?? | — | PARTIAL_PASS land doc |
| `docs/p9_paradigm_d_distill_spec_2026_05_03.md` | ?? | — | spec ~470 LoC |
| `docs/p9_paradigm_d_spec_landed_2026_05_03.ai.md` | ?? | — | spec land doc |
| `docs/p9_paradigm_j_50k_landed_2026_05_03.ai.md` | ?? | — | FAIL_J land doc |
| `docs/p9_path_b_sanity_probe_landed_2026_05_03.ai.md` | ?? | — | HellaSwag empirical settle |

Inferred land timestamps (from filenames + file mtimes): all 2026-05-03 day, sweep across afternoon/evening (mtimes 21:45 → 23:54 KST).

### 1.3 HF upload mk2 (naming convention, upload pipeline, pre-push hook)

| path | type | size | content hint |
|---|---|---|---|
| `tool/hf_upload_mk2.hexa` | ?? | — | HF upload mk2 tool (raw#9 STRICT hexa-only) |
| `tool/hf_upload_mk2_pre_push_hook.hexa` | ?? | — | pre-push CI hook |
| `tool/hf_readme_template.md` | ?? | — | README template for upload mk2 |
| `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` | ?? | — | naming spec |
| `docs/anima_hf_naming_mk2_spec_landed_2026_05_03.ai.md` | ?? | — | naming spec land |
| `docs/anima_hf_upload_mk2_spec_2026_05_03.md` | ?? | — | upload pipeline spec |
| `docs/anima_hf_upload_mk2_landed_2026_05_03.ai.md` | ?? | — | upload pipeline land |
| `state/hf_upload_audit/` | ?? | 16K | per-call JSONL audit logs (`20260503T15{1303,1321,1335,1341}Z_*.jsonl`) |
| `state/hf_upload_ledger_2026_05.jsonl` | ?? | small | top-level monthly ledger (dry_run entries vs `need-singularity/clm-v4-{base-mirror,sft-stage1}`) |

Markers landed: `state/markers/anima_hf_naming_mk2_spec_landed.marker`, `anima_hf_upload_mk2_landed.marker`, plus 16 `hf_upload_mk2_*.marker` ts-suffixed run markers.

### 1.4 BLM phase 5 stimulus-aligned spec

| path | type | size | content hint |
|---|---|---|---|
| `.roadmap.blm_brain_lm` | M | +2 lines | adds `cond.phase5_aligned_spec` (S1 event-trigger LOCKED) + `cond.phase5_aligned_exec` (unmet, awaits next BG) |
| `docs/blm_phase5_stimulus_aligned_pipeline_spec_2026_05_03.md` | ?? | — | spec doc only (DRAFT, exec 미인가) |
| `docs/blm_phase5_aligned_spec_landed_2026_05_03.ai.md` | ?? | — | spec land (friendly preset) |

Marker landed: `state/markers/blm_phase5_aligned_spec_landed.marker`.

> NOTE: original task description mentioned "`.roadmap.blm_brain_lm +2`" — the leading `.roadmap.eeg` and a third roadmap from earlier `git status` snapshot are NO LONGER modified post-`c3ea60dd4`. Only `.roadmap.blm_brain_lm` and `.roadmap.p9_sft` remain modified. (See Risk Flag #3.)

### 1.5 CLM v4 tokenizer restoration

| path | type | size | content hint |
|---|---|---|---|
| `state/clm_v4_tokenizer_restoration_2026_05_03/` | ?? | 2.2M | `tokenizer_64k_multilingual.{model,vocab}` (1.3M+0.99M) + `integrity_report.json` + `README.md` |
| `docs/clm_v4_tokenizer_restored_2026_05_03.ai.md` | ?? | — | restoration doc — Mac sister-repo had the original artifact; pushed to HF mirror + ubu1 cache |

Marker landed: `state/markers/clm_v4_tokenizer_restored_2026_05_03.marker`.

### 1.6 Consciousness laws root cause fix

| path | type | size | content hint |
|---|---|---|---|
| `state/consciousness_laws_root_cause_fix_2026_05_03/` | ?? | 16K | `audit.json` + `before_after_diff.json` + `missing_keys_list.json` |
| `docs/consciousness_laws_root_cause_fix_landed_2026_05_03.ai.md` | ?? | — | replaces Path B band-aid with schema-aware loader (c2-v1 vs v6 split documented) |

Marker landed: `state/markers/consciousness_laws_root_cause_fix_landed.marker`.

> Source-side `.py` change to `consciousness_laws.py` is NOT in this residue — implies it was already committed earlier OR landed inside `ready/` submodule. (See Honest C3 §5.1.)

### 1.7 py_to_hexa (raw#9) audit + enforcement land

| path | type | size | content hint |
|---|---|---|---|
| `state/py_to_hexa_audit_2026_05_03/` | ?? | 60K | `audit.json` + `backup/` (4 `.py` files retired: `_all_kick_extract_run.py`, `_pcg32_reference.py`, `anima_holographic_ib_ksg_validate_prod.py`, `hf_upload_runner.py`) |
| `docs/py_to_hexa_only_landed_2026_05_03.ai.md` | ?? | — | LANDED status doc |

Cross-track: enforces raw#9 strict; the `.py` files in `backup/` are retired-not-deleted (per memory `feedback_py_to_hexa_only`).

### 1.8 Ops / infra

| path | type | content hint |
|---|---|---|
| `config/h100_pods.json` | M | +14 lines: 1 live RunPod pod auto-synced (`29dhlqk508ugoc` @ `103.207.149.110:14783`); `updated_at` bumped to 2026-05-03T14:57:13Z. Per memory `project_runpod_pod_purge_2026_05_03` all 6 EXITED H100s were terminated; this entry represents a NEW pod added post-purge. |
| `state/worktree_merge_plan.json` | M | timestamp drift only (`generated_at` 13:47:31Z → 15:17:32Z) — no body change |
| `ready` | m | submodule dirty: own `git status` shows `D .claude/settings.json`, `D CLAUDE.md`, multiple `D` deletions of `CLAUDE.md` files, `M` to `infinite_evolution.py` + `philosophy_lenses.py`, etc. (sub-repo HEAD = `ef7aae81f`). NOT this audit's scope to commit; submodule has its own land cycle. |
| `references/tribev2` | ? | submodule path — see Risk Flag #2 |

### 1.9 docs/ai-native/

| path | content hint |
|---|---|
| `docs/ai-native/clm_eeg_smoke_v6_real_run_2026_05_03.ai.md` | clm_eeg smoke v6 real run land |
| `docs/ai-native/rail_audit_sidecar_policy_2026_05_03.ai.md` | rail_audit sidecar policy |

Cross-track candidate: `clm_eeg_smoke_v6_real_run` likely belongs to BG-α scope (clm-eeg harness real smoke). `rail_audit_sidecar_policy` was committed as `.gitignore` rule in `c3ea60dd4` per its commit message (`BG-C rail_audit gitignore`). Defer to BG-α/BG-β coordination.

### 1.10 Uncategorized leftovers

None. All 46 entries categorized above.

---

## 2. Per-track recommended commit scope

| # | Track | Files (count) | Recommended subject | Notes |
|---|---|---|---|---|
| 1 | CLM v4 tokenizer restoration | 4 (1 doc + 1 dir w/ 4 files) | `feat(clm v4 tokenizer restored 2026-05-03): 64K BPE multilingual artifact + integrity report + README` | Self-contained. INCLUDE the binary `.model` file (1.3M data) — NOT a regenerable artifact (whole point of the cycle is recovery from sister repo). Confirm `.gitignore` line 30 `*.safetensors` does NOT block `.model`. SAFE. |
| 2 | Consciousness laws root cause fix | 4 (1 doc + 3 JSONs) | `fix(consciousness laws schema loader 2026-05-03): replace Path B band-aid with c2-v1/v6 schema-aware loader + audit JSONs` | Self-contained. Source `.py` change presumed already in `ready/` submodule or pre-committed. |
| 3 | py_to_hexa raw#9 enforcement | 2 entries (1 doc + 1 dir) | `chore(py to hexa raw9 strict 2026-05-03): retire 4 .py files to backup + audit ledger + land doc` | DEFER `state/py_to_hexa_audit_2026_05_03/backup/*.py` decision: per memory `py_to_hexa_only` `.py` is BANNED on Mac. Backups should be R2/local-only OR moved out of repo. RISK: committing `.py` files to git (even in `backup/`) violates raw#9. Recommend committing ONLY `audit.json` + doc, gitignore the `backup/` subdir. |
| 4 | BLM phase 5 spec | 3 (1 roadmap-mod + 2 docs) | `feat(blm phase 5 stimulus-aligned spec 2026-05-03): event-trigger sync S1 LOCKED + roadmap cond.phase5_aligned_{spec,exec}` | Self-contained spec-only land. |
| 5 | HF upload mk2 | 9 (3 tools + 4 docs + 1 dir + 1 ledger) | `feat(anima hf upload mk2 2026-05-03): naming convention + upload pipeline + pre-push hook + dry-run audit ledger` | Self-contained. All 3 tools are `.hexa` (raw#9 OK). Ledger entries are dry_run only. Cross-track: `state/hf_upload_audit/` may grow during real uploads — gitignore-vs-commit decision needed (recommend commit current entries, gitignore future via pattern). |
| 6 | P9 SFT umbrella | 19 (1 roadmap-mod + 8 docs + 1 tool + 1 root JSON + 8 dirs) | Multi-commit recommended (split): | See sub-table below. |
| 7 | Ops infra (config + worktree timestamp) | 2 modified | `chore(ops 2026-05-03): h100_pods auto-sync new RunPod node + worktree_merge_plan timestamp refresh` | Tiny self-contained. |
| 8 | docs/ai-native (BG-α/BG-β coord) | 2 docs | DEFER: coordinate with BG-α and BG-β scopes; `clm_eeg_smoke_v6_real_run` may belong to BG-α deliverable bundle. | Cross-track |
| 9 | `ready` submodule dirty | 1 entry | DEFER (out of scope; submodule self-commits) | Risk Flag #1 |
| 10 | `references/tribev2` working dir | 1 entry | DEFER (gitlink/working-dir mismatch — see Risk Flag #2) | Risk Flag #2 |

### 2.1 P9 SFT split (track 6)

P9 SFT residue covers 5 sub-tracks. Recommend per-sub-track commits to keep blast radius small:

| sub | files | subject |
|---|---|---|
| 6a | `state/p9_p1_5_ensemble_2026_05_03/` + `docs/p9_p1_5_ensemble_4seed_landed_*.ai.md` | `state(p9 p1.5 ensemble 4seed 2026-05-03): holdout-500 cv verdict + per-seed JSONs` — RISK: `compute_ensemble.py` violates raw#9. RECOMMEND port to `.hexa` BEFORE commit OR exclude `.py` from add. |
| 6b | `state/p9_paradigm_d_25k_*/` + `_50k_*/` + `_distill_*/` + `docs/p9_paradigm_d_distill_*.ai.md` + `docs/p9_paradigm_d_distill_spec_*.md` + `docs/p9_paradigm_d_spec_landed_*.ai.md` | `feat(p9 paradigm d distill 2026-05-03): spec + 25k/50k/distill verdicts (PARTIAL_PASS) + .roadmap entry` — bundle the `.roadmap.p9_sft` modification HERE (the +1 line is `cond.paradigm_d_distill`). |
| 6c | `state/p9_paradigm_j_50k_2026_05_03/` + `docs/p9_paradigm_j_50k_landed_*.ai.md` | `state(p9 paradigm j 50k 2026-05-03): FAIL_J CUDA OOM at step 0 + comparison matrix` |
| 6d | `state/p9_path_a_*/` × 2 + `docs/p9_a_prime_path_decision_landed_*.ai.md` + `tool/p9_a_prime_verdict.hexa` + `state/p9_a_prime_*` × 2 | `feat(p9 a-prime path decision + path a llama lora 2026-05-03): verdict tool .hexa + main eval pipeline + watchdog + cost projection` — RISK: `*.py.txt` and `*.sh.txt` are pre-staged scripts (`.txt` extension is raw#9 dodge). Confirm intent. |
| 6e | `state/p9_path_b_sanity_probe_*/` + `docs/p9_path_b_sanity_probe_landed_*.ai.md` | `state(p9 path b sanity probe 2026-05-03): hellaswag empirical settle CLM v4 base ≈random` — depends on / cross-links 6d. |

---

## 3. Commit ordering plan

Self-contained tracks first, cross-track-dependent last; raw#9 cleanup blocks all `.py`-touching commits.

1. **Track 7 (Ops infra)** — 2-line config + timestamp; trivial; lowest risk; first to clear `git status` noise.
2. **Track 1 (CLM v4 tokenizer)** — self-contained; includes 2.2M binary which deserves its own clean commit for blame-traceability.
3. **Track 2 (consciousness laws RCF)** — self-contained.
4. **Track 4 (BLM phase 5 spec)** — self-contained spec-only; touches `.roadmap.blm_brain_lm` only.
5. **Track 5 (HF upload mk2)** — self-contained but multi-file (9); commit after BLM so smaller commits land first for easier `git log` review.
6. **Track 6b (P9 paradigm D)** — must land BEFORE 6a/6c/6d/6e since it owns the `.roadmap.p9_sft` modification (single-line +1 cond entry); subsequent P9 commits add zero roadmap diff.
7. **Track 6c (P9 paradigm J)** — independent of 6d/6e.
8. **Track 6e (P9 path B sanity probe)** — referenced by 6d's path-decision; commit before 6d so 6d can refer to it as predecessor.
9. **Track 6d (P9 A' path decision + Path A)** — depends on 6e; cleanup `.py.txt`/`.sh.txt` clarity needed before commit.
10. **Track 6a (P9 P1.5 ensemble)** — depends on `.py`-vs-`.hexa` decision (raw#9); land last in the P9 sub-cluster.
11. **Track 3 (py_to_hexa enforcement land)** — semantically the META commit ("we removed all the `.py`"); should land AFTER all other tracks have been .py-cleaned, so the audit truthfully says "0 .py remain". Consider deferring entirely until sub-tracks 6a/6d resolve their `.py`/`.py.txt`/`.sh.txt` residue.
12. **Track 8 (docs/ai-native)** — coordinate with BG-α/BG-β; defer to those agents' scopes.
13. **Tracks 9-10 (`ready`, `references/tribev2`)** — out of scope for this audit; address in a separate submodule-cleanup cycle.

---

## 4. Risk flags

### Flag #1 — `m ready` (lowercase = submodule with modified working tree)

The submodule at `ready/` (HEAD `ef7aae81f`) has an internally dirty working tree: deletes of `CLAUDE.md` files across multiple subdirs, modifications to `.py` files (`infinite_evolution.py`, `philosophy_lenses.py`), and `D .claude/settings.json`. **DO NOT** include `ready` in any commit from this audit's scope — submodule has its own land cycle and the parent-repo gitlink should only advance after the submodule itself commits + pushes. The dropped `CLAUDE.md` files inside `ready/` may be intentional consolidation but warrants user confirmation.

### Flag #2 — `references/tribev2` (gitlink-vs-working-dir mismatch)

`git ls-files --stage references/tribev2` returns a `160000` gitlink at `1731059aa7d6...` (i.e., it IS tracked as a submodule), but `git status --short` shows `? references/tribev2` (UNTRACKED) — meaning the working-dir checkout has `.git` as a **directory** (regular clone), NOT a submodule gitfile pointing into `.git/modules/...`. There is also NO `.gitmodules` file in the repo root. This is an **inconsistent submodule state**: the index has a gitlink but no submodule config and the working dir is a standalone clone (origin = `facebookresearch/tribev2`, fork remote = `dancinlife/tribev2`). Likely repair paths:
- (a) ratify as submodule: create `.gitmodules`, fix `references/tribev2/.git` to a gitfile pointing into `.git/modules/references/tribev2/`, recommit.
- (b) demote to plain checkout: `git rm --cached references/tribev2`, add to `.gitignore`.
- (c) stay broken (current).

DO NOT touch in this read-only audit. Flag for separate resolution cycle. Same situation likely applies to other `references/*` entries (5 more gitlinks: Documentation, OpenBCI_*, V3_Hardware_Design_Files) — none surfaced as `?` because their working dirs are presumably consistent.

### Flag #3 — task brief mentions roadmaps that are NO LONGER modified

Original task said "`.roadmap.blm_brain_lm`, `.roadmap.eeg`, `.roadmap.p9_sft`" all modified. Post-`c3ea60dd4` only `.roadmap.blm_brain_lm` + `.roadmap.p9_sft` remain modified. `.roadmap.eeg` was committed within the cycle-8 followup. This is good — confirms the cycle-8 commit landed eeg-scope cleanly. The "+1" / "+2" annotations in the brief are stale by one commit.

### Flag #4 — raw#9 violations in untracked residue

- `state/p9_p1_5_ensemble_2026_05_03/compute_ensemble.py` (9.1K) — actual `.py`, NOT `.txt` staged. Per memory `feedback_py_to_hexa_only` and `.gitignore` line 4 (`**/*.py`), this would be REJECTED by `git add` if attempted. CONFIRMS .gitignore protection working.
- `state/p9_path_a_llama_lora_2026_05_03/*.py.txt` + `*.sh.txt` (4 entries) — `.txt`-suffixed shadow scripts. Pattern is consistent (raw#9-aware "park" form) but borderline. Confirm with user before committing.
- `state/p9_a_prime_main_eval_pipeline_2026_05_03/eval_llama_lora_ckpt.py.txt` + `loader_smoketest.py.txt` + `extract_base_per_example.sh.txt` — same `.py.txt`/`.sh.txt` pattern.
- `state/py_to_hexa_audit_2026_05_03/backup/*.py` (4 entries) — actual `.py` files retired to backup. Per `.gitignore` `**/*.py` these are blocked from `git add`. SAFE.

### Flag #5 — `state/clm_v4_tokenizer_restoration_2026_05_03/tokenizer_64k_multilingual.model` is 1.3M binary

`.gitignore` line 25 blocks `*.pt`, line 30 blocks `*.safetensors`, but `.model` (sentencepiece protobuf) is NOT in the ignore list. The `file` command reports `data` (binary). 1.3M is well under GitHub's 100MB hard limit but adds permanent repo bulk. RECOMMEND committing — restoration is the entire point of the track and the artifact is canonical. Do NOT use Git LFS (no LFS config in repo).

### Flag #6 — `state/hf_upload_ledger_2026_05.jsonl` location

Top-level monthly ledger placed in `state/` root rather than under a per-cycle subdir. If pattern continues, consider gitignore via `state/hf_upload_ledger_*.jsonl` and keep ledger as local-only OR explicit per-month commit. Currently 2 entries, both `dry_run`, no real upload.

---

## 5. Honest C3 (raw#10 caveats)

**5.1 — `consciousness_laws.py` actual source change is invisible.**
The `state/consciousness_laws_root_cause_fix_*/` track has audit JSONs + a land doc but no corresponding modified source file in the residue. The actual `.py` (or `.hexa`) edit could be: (a) inside `ready/` submodule (its dirty working tree shows `M anima/modules/agent/philosophy_lenses.py` but not `consciousness_laws.py` directly — possibly elsewhere), (b) already committed in an earlier cycle, (c) only conceptual/spec at this stage. Read-only audit cannot confirm which.

**5.2 — Cannot verify HF upload mk2 ran without dual-lock conflicts.**
`state/hf_upload_audit/` shows 4 JSONL run-logs all marked `dry_run` (`mode: dry_run` in ledger). No real-mode upload yet. If a real upload happens before these are committed, the audit dir will grow and may interleave with real-side races (raw#10: cannot pre-judge that interaction from current state).

**5.3 — `p9_paradigm_d_25k` vs `_50k` vs `_distill` relationship unclear.**
Three sibling dirs with different step counts. From verdict file sizes (10.9K, 9.4K, 5.6K) and the `_distill` having `_reconstructed` suffix files (`trajectory_reconstructed.json`, `verdict_reconstructed.json`), my best guess is: 25K = mid-run checkpoint readout, 50K = full-run verdict, distill = the post-loop silent-exit reconstruction (PARTIAL_PASS docs say "2000/2000 steps + post-loop silent exit"). But these could also be 3 separate spec-vs-exec attempts. Cannot distinguish from filenames alone.

**5.4 — `p9_path_a` two-dir split rationale.**
`p9_path_a_health_audit_*` (3 JSONs: health/cost/watchdog) vs `p9_path_a_llama_lora_*` (verdict + scripts + pod info). Either parallel sub-aspects of the same Path A run OR sequential phases. From mtimes (`health_audit/` files at 00:23-24 vs `llama_lora/` files mostly at 23:01-34 prev day), they were written at different times — `llama_lora/` first, then `health_audit/` is the watchdog+post-mortem tier. Likely intended as one logical commit with `_health_audit/` derivative.

**5.5 — Marker timestamps not cross-validated.**
`state/markers/*.marker` files were enumerated but their content (typically empty file with ts in name) was not opened — verifying `*_landed.marker` actually corresponds to current land state would require reading each file. Skipped per scope.

**5.6 — `references/tribev2` gitlink hash `1731059aa...` predates the working dir mtime.**
The working-dir clone (mtime 2026-05-02 21:58, content 5.6M) may or may not match `1731059aa...`. `git diff` for a submodule with broken wiring returns nothing useful. Cannot confirm sync state read-only.

**5.7 — Did NOT inspect every doc body.**
Only 1-line headers extracted. Cross-references between docs (e.g., does `p9_paradigm_d_distill_landed.ai.md` properly link `p9_paradigm_d_distill_spec.md` as predecessor?) NOT verified.

---

## 6. Recommended commit-1 next-action

**Track 7 (Ops infra)** — single tightly-scoped commit:
- `git add config/h100_pods.json state/worktree_merge_plan.json`
- subject: `chore(ops 2026-05-03): h100_pods auto-sync 1 live RunPod node + worktree_merge_plan timestamp refresh`
- rationale: zero-ambiguity, 16 lines total, no `.py`/binary risk, immediately reduces `git status` to 44 entries and proves the audit-plan-to-commit pipeline works before tackling larger tracks.

After Track 7, proceed to Track 1 (CLM v4 tokenizer — self-contained, including the 1.3M `.model` binary) as the second commit.

---

## 7. Hard constraints honored

- raw#15: all paths above are repo-relative.
- READ-ONLY: no `git add`, no `git commit`, no source-edit, no `chflags`. The only filesystem mutation performed by this audit was creating the deliverable file at `state/docs_pending_audit_2026_05_04/audit_plan.md`.
- raw#10: §5 enumerates 7 explicit caveats about read-only-inspection limits.
