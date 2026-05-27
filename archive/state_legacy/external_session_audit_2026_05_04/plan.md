# External-session uncommitted file audit + commit-group classification plan
**Date**: 2026-05-04
**Owner**: BG-ψ (read-only audit)
**Scope**: full uncommitted working tree as observed at session start
**Mutation policy**: READ-ONLY — this audit produces a plan; user/parent decides commit actions
**Conversation territory note**: BG-φ owns `tool/clm_v4_*.hexa` + `tool/p9_*.hexa` + `state/clm_v4_tokenizer_caller_migration_phase_2_2026_05_04/`; BG-χ owns `state/p9_base_validation_prereq_exec_2026_05_04/` + ubu1 cache. This audit covers ALL OTHER uncommitted entries.

---

## §1. Total inventory (raw count)

`git status --short` reports **123 entries**:
- **Modified (tracked)**: 32 files
- **Untracked**: 89 entries (61 docs + 23 state/ dirs-or-files + 4 tool/ files + 1 root .gitignore-affected dir)
- **Submodule dirty**: 2 (`m ready`, `? references/tribev2`)

`git diff --stat HEAD` reports `34 files changed, 598 insertions(+), 144 deletions(-)` (modified-only stat — does NOT include untracked).

---

## §2. Per-track classification

External-session signal: predominantly `2026-05-03` date stamps + `*.ai.md` AI-native handoff suffix + corresponding `state/<dir>_2026_05_03/` ledgers. Last-day work that did NOT come from THIS conversation's commits (verified against `git log` — our commits are e2ce92413 onwards on 2026-05-03 + everything 2026-05-04).

### Track A — quantum/IIT consciousness (qmirror + iit4 + ionq + penrose_hameroff + anima_physics)
- **.roadmap.* modified (5)**: `.roadmap.anima_physics`, `.roadmap.iit4`, `.roadmap.ionq`, `.roadmap.penrose_hameroff`, `.roadmap.qrng`
- **docs/ modified (8)**: `anima_nexus_qrng_dependency_wire_*.md`, `hexa_lang_attr_review_for_qmirror_*.md`, `ibm_cloud_env_setup_runbook_*.md`, `ibm_cloud_experiment_list_*.md`, `nexus_qmirror_phase3_calibration_runbook_*.md`, `nexus_qmirror_spec_*.md`, `qmirror_cond3_band_revise_landed_*.ai.md`, `qmirror_cond3_ibm_n1_landed_*.ai.md`, `qmirror_cond8_braket_landed_*.ai.md`, `qmirror_n2_cross_vendor_revision_*.md`
- **docs/ untracked (~25)**: all `qmirror_*` and `nexus_*qmirror*` `.ai.md` + `.md` (qmirror_2_axes_*, qmirror_arxiv_draft_*, qmirror_canonical_migration_*, qmirror_closure_*, qmirror_cond4_nist_*, qmirror_cond7_alpha_burst_*, qmirror_cond7_alpha_*, qmirror_crosstech_band_revise_*, qmirror_dp_noise_*, qmirror_dual_mirror_autosync_*, qmirror_first_unblock_*, qmirror_github_xref_*, qmirror_hf_mirror_pushed_*, qmirror_license_audit_*, qmirror_nexus_migration_plan_*, qmirror_spec_xref_update_*, qmirror_standalone_finish_*, qmirror_standalone_pushed_*, qmirror_top5_unblock_*, qmirror_unblock_exec_plan_*, qmirror_vqe_h2_*, hx_install_qmirror_spec_*, nexus_cli_qmirror_landed_*, nexus_qmirror_closure_*)
- **state/ untracked (5)**: `nexus_qmirror_ibm_heron_alpha_*`, `nexus_qmirror_ibm_heron_alpha_burst_*`, `nexus_qmirror_ibm_heron_alpha_burst_v2_*`, `state/nexus_qmirror_nist_*` (3 new subfiles)
- **state/ modified (2)**: `state/nexus_qmirror_nist_*/verdict.json`, `state/anima_eeg_core_phase5_verify_*/verify_results.json`
- **External purpose**: large qmirror cycle — substrate-mapping IIT 4.0 + IonQ + IBM Heron + NIST entropy audit + arxiv draft prep + cross-vendor revisions. Each .roadmap entry adds `verified_via_qmirror_2026_05_03` and `qmirror_canonical_2026_05_03` annotation fields (additive, semantics-preserving — observed in `.roadmap.iit4` and `.roadmap.qrng` diffs).
- **Modification scope**: roadmap = additive field append (non-destructive); docs = entirely new files mostly; nexus_qmirror_spec_*.md = +64 LoC additions (new sections).
- **Conflict risk vs our commits**: **LOW**. Our 2026-05-04 commits touched `.roadmap.p9_sft`, `tool/clm_v4_*`, `tool/p9_*`, `tool/host_pod_terminator.sh.txt` — no overlap with qmirror/iit4/ionq/qrng track.
- **Commit recommendation**: split into 3 commits — (A1) docs+state qmirror exec evidence (~25 files, ~5 state dirs); (A2) docs/* nexus_qmirror_spec_*.md +64-line spec extension + nexus_qmirror_phase3_calibration_runbook_* +2 (canonical SSOT update); (A3) `.roadmap.{anima_physics,iit4,ionq,penrose_hameroff,qrng}` annotation bundle (post-evidence).

### Track B — n_substrate framework (n_substrate + sim + theory_validation)
- **.roadmap.* modified (3)**: `.roadmap.n_substrate`, `.roadmap.sim`, `.roadmap.theory_validation`
- **docs/ modified (5)**: `n_12_v3_ibm_quantum_prep_*.md`, `n_substrate_n12_aws_prep_*.md`, `n_substrate_n12_ionq_penrose_hameroff_spec_*.md`, `n_substrate_n12_quantum_pivot_*.md`, `n_substrate_n13_photonic_iit_spec_*.md`
- **state/ untracked (1)**: `phi_v3_robustness_sweep_2026_05_03/`
- **External purpose**: n12 substrate cohort — IBM/AWS quantum prep + n13 photonic IIT + φ v3 robustness.
- **Modification scope**: docs = additive (10-14 LoC each); roadmap = additive annotation cluster (likely qmirror cross-link).
- **Conflict risk**: **LOW**. No overlap with our commit territory.
- **Commit recommendation**: bundle with Track A (qmirror umbrella) — n_substrate + theory_validation + sim roadmap annotations are downstream of qmirror.cond.* substrate substitution.

### Track C — p9_sft (training, paradigm D/J)
- **.roadmap.* modified**: NONE (we already committed `.roadmap.p9_sft` in c0c29e999; external did NOT further mutate)
- **docs/ untracked (7)**: `p9_paradigm_d_25k_a100_aborted_*.ai.md`, `p9_paradigm_d_kl_preflight_landed_*.ai.md`, `p9_paradigm_j_50k_v2_landed_*.ai.md`, `p9_path_a_completion_audit_landed_*.ai.md`, `p9_path_b_sanity_probe_v2_landed_*.ai.md`, `p9_pd_25k_a100_health_audit_landed_*.ai.md`, `p9_qmirror_seeded_landed_*.ai.md`
- **state/ untracked (8)**: `p9_paradigm_d_25k_a100_*/`, `p9_paradigm_d_25k_h100_*/`, `p9_paradigm_d_kl_preflight_*/`, `p9_paradigm_j_50k_v2_*/`, `p9_path_a_completion_audit_*/`, `p9_path_a_hf_push_verify_2026_05_04/`, `p9_path_a_watchdog_armed_*/`, `p9_path_b_sanity_probe_v2_*/`, `p9_pd_25k_a100_health_audit_*/`, `p9_qbench_resample_*/`, `p9_qmirror_seeded_*/`, `d_25k_eval_auto_trigger_*/`
- **External purpose**: p9 paradigm D 25k a100/h100 launches + paradigm J 50k v2 + path A completion audit + path B sanity probe v2 + qmirror-seeded paradigm.
- **Modification scope**: all NEW state/ + .ai.md handoffs — no in-place edits.
- **Conflict risk**: **MEDIUM**. Our commit c0c29e999 set p9_path_a status to `PARTIAL_VERIFIED_8K`; the external `p9_path_a_completion_audit_*` and `p9_path_a_hf_push_verify_2026_05_04/` may have updated verdict semantics. Also `state/p9_path_a_hf_push_verify_2026_05_04/` is **2026-05-04 dated**, suggesting this might be a CONCURRENT session running on this checkout.
- **Files to AUDIT BEFORE COMMIT**: `state/p9_qmirror_seeded_*/p9_qmirror_seeded_ablation_A_2k.py` — **raw#9 violation candidate** (`.py` on Mac side, BANNED per session memory). Verify if it's an ubu1-target artifact or local Mac-side write before committing.
- **Commit recommendation**: split — (C1) p9_qbench/d_25k_eval/path_a_watchdog/path_b_v2/d_kl_preflight (paradigm-D + ancillary) bundle; (C2) p9_path_a_completion_audit + p9_path_a_hf_push_verify_2026_05_04 (verdict reconciliation — must verify alignment with our c0c29e999 first); (C3) p9_qmirror_seeded (cross-track Track A overlap — defer to Track A umbrella OR commit with explicit Track A xref).

### Track D — anima_eeg_core (Hjorth root-cause)
- **Modified (1)**: `anima-eeg-core/tool/modules/_metrics/hjorth_native.hexa` (+229 LoC, dockerized SIGKILL fix — adds `_hjorth_mean_streaming` + `_var_*_only` per-channel evaluators)
- **docs/ untracked (1)**: `anima_eeg_core_hjorth_root_cause_landed_*.ai.md`
- **state/ untracked (1)**: `anima_eeg_core_hjorth_root_cause_*/` (audit.json + before_after.diff + dmesg_excerpt.txt + .before snapshot)
- **External purpose**: hjorth_native dockerized hexa-runtime cgroup OOM (exit 137 SIGKILL) root-cause + streaming-evaluator fix; original public-API path retained byte-identical.
- **Modification scope**: 1 file +229 LoC additive (no removal); ancillary state/ ledger for audit trail.
- **Conflict risk**: **LOW**. No overlap with our commits. anima-eeg-core last touched in `181b927c6` (legacy commit, pre-cycle).
- **Commit recommendation**: single self-contained commit (`fix(anima-eeg-core hjorth_native sigkill 2026-05-03): streaming per-channel eval + audit ledger`).

### Track E — anima_hf_naming_mk2 (committed-spec extension)
- **Modified (2)**: `docs/anima_hf_naming_convention_mk2_spec_2026_05_03.md` (+98 LoC), `tool/hf_upload_mk2.hexa` (+45/-19 LoC, 96-line diff)
- **docs/ untracked (3)**: `anima_hf_naming_family_reconcile_*.ai.md`, `mk2_naming_paradigm_amendment_landed_*.ai.md`, `hexa_lang_module_versioning_landed_*.ai.md`, `hexa_lang_module_versioning_spec_*.md`
- **state/ untracked (1)**: `mk2_naming_paradigm_amendment_*/`
- **External purpose**: family enum reconciliation (added `nlm`/`llm`) + `paradigm-{letter}` stage-prefix amendment (unblocks Paradigm-J HF recovery rejection) + version bump 2.0.0 → 2.0.2 + Alpine `printenv` → POSIX `echo` polish.
- **Modification scope**: tool/hf_upload_mk2.hexa = additive (regex extensions), version bump documented; spec doc = additive 98 LoC of §3.2.1 + §3.3 spec sections.
- **Conflict risk**: **MEDIUM-LOW**. `tool/hf_upload_mk2.hexa` was committed in e9a914c97 (anima HF upload mk2 land). External re-edited a committed file — NOT a clobber (additive only) but signals an external session actively maintaining this file. We did NOT touch it ourselves so no double-touch.
- **Commit recommendation**: single combined commit (`feat(anima HF mk2 amendment 2026-05-03): family enum {nlm,llm} + paradigm-{letter} stage prefix + version 2.0.2 + Alpine echo polish`).

### Track F — anima_dot_own namespace (new spec)
- **Modified (1)**: `.gitignore` (+12 LoC, `tool/transient_py/*.py` policy)
- **docs/ untracked (2)**: `anima_dot_own_namespace_spec_*.md`, `anima_dot_own_namespace_spec_landed_*.ai.md`
- **tool/ untracked (1)**: `tool/transient_py/` (atp_pytorch.py + README.md)
- **External purpose**: `.own N` namespace formalization — `tool/transient_py/` directory for auto-generated python (regenerable from .hexa transpiler).
- **Modification scope**: spec land + scaffold dir + .gitignore policy.
- **Conflict risk**: **LOW** — does not touch our territory.
- **Files to AUDIT BEFORE COMMIT**: `tool/transient_py/atp_pytorch.py` is **`.py` on Mac side** — per session memory feedback `py -> hexa only`, this is a raw#9 violation. The .gitignore policy already excludes `*.py` here, so the file would NOT be committed anyway IF the .gitignore lands first. **Sequencing matters**: commit .gitignore + scaffold (.gitkeep + README.md) WITHOUT atp_pytorch.py.
- **Commit recommendation**: single commit (`feat(anima .own namespace 2026-05-03): tool/transient_py/ scaffold + .gitignore policy`); explicitly EXCLUDE `tool/transient_py/atp_pytorch.py` from index.

### Track G — hexa-lang upstream / transpiler / interp / atp / qwalk / llm_agent
- **docs/ untracked (~10)**: `atp_pytorch_transpile_landed_*.ai.md`, `hexa_interp_rebuilt_*.ai.md`, `hexa_lang_module_versioning_*.{md,ai.md}`, `hexa_lang_upstream_audit_*.{md,ai.md}`, `hexa_to_py_transpiler_prototype_*.md`, `llm_agent_mi_landed_*.ai.md`, `anima_qwalk_landed_*.ai.md`, `cleanup_bg_side_effect_audit_*.md`
- **state/ untracked (~7)**: `atp_transpile_audit_*/`, `hexa_interp_rebuild_*/`, `hexa_to_py_audit_*/`, `llm_agent_mi_*/`, `anima_qwalk_*/`, `cleanup_bg_audit_*/`, `cosmetic_polish_batch_*/`, `transpiled_py/`
- **tool/ untracked (4)**: `d_25k_completion_watchdog.hexa`, `guard3_post_bg_validator.hexa`, `hexa_to_py_transpiler.hexa`, `hexa_to_py_transpiler_test.hexa`
- **External purpose**: hexa-lang module versioning + interp rebuild + hexa→py transpiler prototype + ATP pytorch transpile + qwalk + LLM agent MI + cleanup BG side-effect audit + cosmetic polish batch.
- **Files to AUDIT**: `state/transpiled_py/test{1,2,3}_*.py` and `state/p9_qmirror_seeded_*/p9_qmirror_seeded_ablation_A_2k.py` — **raw#9 violation candidates**. Determine whether they live in a transient/gitignored namespace OR are gitignore-evading.
- **Conflict risk**: **LOW**. tool/ adds 4 new .hexa primitives (no overlap with our tool/clm_v4_* / tool/p9_*).
- **Commit recommendation**: split into (G1) hexa-lang upstream audit + module versioning (spec+land); (G2) atp pytorch transpile + transpiler prototype (links Track F); (G3) hexa interp rebuild; (G4) llm_agent_mi + qwalk + cleanup_bg_audit + cosmetic_polish_batch (independent landings).

### Track H — BLM phase5 + phi v3
- **state/ untracked (3)**: `blm_phase5_aligned_exec_*/`, `blm_phase5_qmirror_normalized_*/`, `phi_v3_robustness_sweep_*/`
- **docs/ untracked (1)**: `blm_phase5_aligned_exec_landed_*.ai.md`
- **External purpose**: BLM phase5 stimulus-aligned exec + qmirror-normalized variant + φ v3 robustness sweep. Note BLM phase5 spec was committed in `e1f644579` — this is the EXEC follow-on.
- **Conflict risk**: **LOW**. No overlap.
- **Commit recommendation**: single commit (`state(blm phase5 aligned exec + qmirror-normalized + phi v3 sweep 2026-05-03)`); φ v3 sweep can fold here OR with Track A.

### Track I — ops auto-sync (auto-sync ticks)
- **Modified (4)**: `config/h100_pods.json` (pod registry refresh — 99ziv0qfjnjbbf+29dhlqk508ugoc → fuewrx9moxe6gz, 2026-05-03 21:27Z → 2026-05-04 00:28Z), `state/runpod_credit_status.json` (balance $327.841 → $335.026), `state/weight_precache_eta.json` (timestamp tick), `state/worktree_merge_plan.json` (timestamp tick)
- **External purpose**: scheduled hook auto-sync — these are NOT external session work; they are runtime-tick artifacts.
- **Conflict risk**: **NONE** (idempotent timestamp refresh).
- **Commit recommendation**: bundle as `chore(ops 2026-05-04)` umbrella commit — typical pattern matches `0ca45002b` and `650f268c3`.

### Track Z — submodules
- **`m ready`** (modified gitlink), **`? references/tribev2`** (untracked submodule pointer)
- Per existing plan `state/submodule_cleanup_plan_2026_05_04/plan.md` (committed in `161d01106`), defer to that cleanup cycle.
- **Commit recommendation**: DEFER. Do not include in any of A-I commits.

---

## §3. Conflict surface report

Cross-reference of our 2026-05-04 commits (e2ce92413 .. c0c29e999 .. 8afb12181 .. 98b614363) against external uncommitted edits:

| File / dir | Our commit | External state | Conflict | Risk |
|---|---|---|---|---|
| `.roadmap.p9_sft` | c0c29e999 (path A status correction) | NOT further modified | None | NONE |
| `tool/hf_upload_mk2.hexa` | committed in e9a914c97 (NOT ours) | re-edited by external (+45/-19) | None | LOW (we never touched) |
| `tool/clm_v4_tokenizer_load.hexa` + `tool/p9_warmup_probe_real.hexa` | 98b614363 | NOT touched by external | None | NONE |
| `tool/host_pod_terminator.sh.txt` | 8afb12181 | NOT touched by external | None | NONE |
| `state/p9_path_a_*` directories | c0c29e999 references existing dirs | external added `p9_path_a_completion_audit_*/` + `p9_path_a_hf_push_verify_2026_05_04/` + `p9_path_a_watchdog_armed_*/` | Different subdirs — additive | LOW |

**Total double-touch surface**: **0** (zero file overlap between our commits and external uncommitted edits).

**Verdict reconciliation watch** (Track C):
- Our c0c29e999 set p9_path_a status `COMPLETE_PROBABLE` → `PARTIAL_VERIFIED_8K` based on 8K-step partial verification.
- External `state/p9_path_a_completion_audit_2026_05_03/{cost_analysis,termination_cause,hf_push_status}.json` may carry alternate verdict semantics. Before committing Track C2, the user MUST cross-read these JSONs against our roadmap entry to confirm semantic alignment (or surface conflict).

---

## §4. Files to EXCLUDE from any commit

| Path | Reason | Severity |
|---|---|---|
| `state/p9_qmirror_seeded_2026_05_03/p9_qmirror_seeded_ablation_A_2k.py` | raw#9 violation (.py on Mac) | HIGH — block commit |
| `state/transpiled_py/test1_simple_add.py`, `test2_stdlib_proc.py`, `test3_lora_stub.py` | raw#9 violation candidates (transpiler output, may be intentionally transient) | HIGH — verify gitignore coverage first |
| `state/transpiled_py/__pycache__/` | binary cache | HIGH |
| `tool/transient_py/atp_pytorch.py` | raw#9 violation; `.gitignore` policy excludes it but only AFTER policy lands | HIGH — sequence matters |
| `tool/transient_py/__pycache__/` | binary cache | HIGH |
| `state/nexus_qmirror_nist_2026_05_03/sample_1mbit.bin` | binary blob 125 KB (NIST entropy raw bytes) | MEDIUM — consider git-lfs or exclude |
| Auto-sync ticks (Track I) | should commit only as `chore(ops)` umbrella, NOT bundled with feat commits | LOW — sequencing only |
| `m ready`, `? references/tribev2` | submodule cleanup deferred to existing plan | DEFER |

---

## §5. Recommended commit-order (if user authorizes external-session land)

Dependency chain — spec must land before exec; .roadmap annotations land last (downstream of evidence):

1. **D — anima_eeg_core hjorth root-cause** (self-contained; lowest risk; unblocks selftest CI)
2. **F — anima .own namespace + .gitignore policy** (must precede G2 transpiler commits to gate `.py` exclusion)
3. **G1 — hexa-lang upstream audit + module versioning** (foundational hexa-lang infrastructure)
4. **G2 — atp pytorch transpile + hexa→py transpiler prototype** (depends on F .gitignore)
5. **G3 — hexa interp rebuild** (independent)
6. **G4 — llm_agent_mi + qwalk + cleanup_bg_audit + cosmetic_polish_batch** (independent landings; cosmetic_polish_batch already referenced by Track E hf_upload_mk2 polish)
7. **E — anima HF mk2 amendment** (depends on cosmetic_polish_batch reference being committable)
8. **A1 — qmirror exec evidence bundle** (large; ~25 docs + ~5 state dirs)
9. **A2 — nexus_qmirror_spec_*.md +64 LoC + phase3 calibration runbook +2** (canonical SSOT update)
10. **C1 — p9 paradigm-D + ancillary** (paradigm-D 25k/50k + qbench + d_kl_preflight + path_a_watchdog + path_b_v2)
11. **C2 — p9 path A completion audit + hf_push_verify** (REQUIRES user verdict reconciliation against our c0c29e999 first)
12. **C3 — p9 qmirror_seeded** (Track A xref; commit AFTER A1 lands; EXCLUDE the .py)
13. **H — BLM phase5 aligned exec + qmirror-normalized + phi v3 sweep** (executes BLM phase5 spec from e1f644579)
14. **B — n_substrate + sim + theory_validation roadmap annotations** (downstream of qmirror canonical)
15. **A3 — `.roadmap.{anima_physics,iit4,ionq,penrose_hameroff,qrng}` annotation bundle** (LAST — qmirror cross-link annotations require A1+A2 evidence committed first)
16. **I — `chore(ops 2026-05-04)`** (auto-sync ticks bundle; can land anytime; recommend last for cleanest history)
17. **Z — submodules** (DEFER per existing plan)

**Top-3 commit-1 candidates by lowest-risk + highest-clarity**:
1. **D (hjorth root-cause)** — single-file +ledger, zero-conflict, surfaces a real bug fix
2. **F (.own namespace .gitignore)** — must land first to gate G2 transpiler outputs
3. **I (ops auto-sync)** — pure idempotent ticks, no semantic content, unblocks "clean working tree" check

---

## §6. Honest C3 caveats (raw#10)

1. **Read-only inspection limits intent inference**. This audit observed file content only; cannot determine whether external sessions are STILL running or have terminated. If external is mid-cycle, committing now may capture a half-landed state.
2. **External session may STILL be running**. File mtimes for `state/runpod_credit_status.json` and `config/h100_pods.json` are 2026-05-04 00:28-00:44 UTC (today, hours-recent) — auto-sync hooks ARE active and will continue ticking, generating fresh diffs after any commit.
3. **`.roadmap.*` external edits NOT user-reviewed**. The 8 modified .roadmap files contain qmirror cross-link annotations added without our review. If the user disagrees with any annotation (e.g., "qmirror canonical entropy substrate" claim for `.roadmap.qrng`), those need revert before commit. We CANNOT review annotation correctness from a tooling perspective alone.
4. **`tool/hf_upload_mk2.hexa` modification scope inferred from diff**. The 96-line diff was sampled (head -80 covered ~50% of changes). A pure-additive verdict is provisional — there may be subtle semantic shifts in the unsampled tail (lines 50-96) that this audit did NOT inspect. Recommend full read before committing Track E.
5. **Working-tree state ≠ index state**. `git status --short` shows working-tree changes; we did NOT run `git diff --staged` or `git ls-files --stage` to detect whether external session also performed `git add`. If staging was done externally, the index may already contain partial bundles inconsistent with our commit-order recommendation.
6. **`p9_qmirror_seeded_ablation_A_2k.py` and `transpiled_py/*.py` raw#9 status uncertain**. These may be intentional transpiler outputs (gitignore-policy-anchored) OR raw#9 violations. Without reading the file headers + xref to spec docs, cannot definitively classify. Conservative default: EXCLUDE from index, ask user before committing.
7. **125 KB `sample_1mbit.bin` binary**. NIST entropy raw bytes — appropriate for state/ ledger but candidate for git-lfs or external storage if repo size matters; this audit did NOT check repo size policy.

---

## §7. Recommended next-action (≤3 sentences for parent/user)

**Recommend commit-1 = Track D (anima_eeg_core hjorth root-cause)** — single self-contained file + audit ledger with zero conflict surface, real bug-fix with clear narrative, lowest risk to land independently. Before committing Track C2 (p9 path A completion audit + hf_push_verify_2026_05_04), the user MUST cross-read `state/p9_path_a_completion_audit_2026_05_03/{cost_analysis,termination_cause,hf_push_status}.json` against our `c0c29e999` `PARTIAL_VERIFIED_8K` verdict to confirm semantic alignment. Tracks F + G2 must land in that order to gate `.py` exclusion via `.gitignore`; do NOT include `state/p9_qmirror_seeded_*/p9_qmirror_seeded_ablation_A_2k.py`, `state/transpiled_py/*.py`, or `tool/transient_py/atp_pytorch.py` in any commit until raw#9 status is confirmed.
