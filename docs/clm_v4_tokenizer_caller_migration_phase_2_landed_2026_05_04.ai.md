# CLM v4 64K tokenizer caller migration — Phase 2 LANDED (2026-05-04)

## TL;DR

**Phase 2 = 4 callers migrated.** The hardcoded `/tmp/tokenizer_64k_multilingual.model` literal is now replaced by the cache-resolver pattern (HF cache rank-1 → checkpoint dir rank-2 → /tmp legacy fallback rank-3 with stderr WARN) in 4 .hexa files that proxy ubu1 GPU operations. Combined with Phase 1 BG-μ (warmup_probe_real, commit `98b614363`), **5 of 6 known callers are now migrated**. Only the ubu1-only `eval_clm_v4_hellaswag.py` remains (Phase 3, scheduled for the final hexa migration cycle).

All 4 .py source files are renamed to `.py.txt` park form per raw#9 strict. All 4 hexa replacements pass selftest with byte-identical token sequences against Phase 1's BG-μ baseline.

## Per-caller migration table

| Caller | Source .py (now `.py.txt`) | Hexa replacement | F-MIG-1 | F-MIG-2 | F-MIG-3 | F-MIG-4 | Sentinel |
|---|---|---|---|---|---|---|---|
| probe_ubu1_clm_v4_tension | `state/p9_p0_measure_2026_05_03/probe_ubu1_clm_v4_tension.py.txt` | `tool/clm_v4_probe_tension.hexa` | PASS | PASS | PASS | PASS | `__P9_clm_v4_probe_tension__ PASS` |
| measure_ubu1_clm_v4_full_50k | `state/p9_p0_measure_2026_05_03/measure_ubu1_clm_v4_full_50k.py.txt` | `tool/clm_v4_measure_full_50k.hexa` | PASS | PASS | PASS | PASS | `__P9_clm_v4_measure_full_50k__ PASS` |
| sentinel_train_50k | `state/p9_p1_sentinel_2026_05_03/sentinel_train_50k.py.txt` | `tool/p9_sentinel_train_50k.hexa` | PASS | PASS | PASS | PASS | `__P9_p9_sentinel_train_50k__ PASS` |
| qmirror_seeded_ablation_A_2k | `state/p9_qmirror_seeded_2026_05_03/p9_qmirror_seeded_ablation_A_2k.py.txt` | `tool/p9_qmirror_seeded_ablation_A_2k.hexa` | PASS | PASS | PASS | PASS | `__P9_p9_qmirror_seeded_ablation_A_2k__ PASS` |

### F-MIG falsifier definitions (preregistered in spec.md §5, commit `68803d162`)

- **F-MIG-1** — Cache-resolved tokenizer round-trip identity over 16 calibration prompts; vocab=64000.
- **F-MIG-2** — Sample token-id sequences byte-identical across all 4 hexa selftests AND Phase 1 BG-μ warmup_probe verdict (`[44357, 601, 54564, 513, 278, 288, 2590, 55314, 48361, 7072, 55299]` for prompt `"Define hexad as a six-fold integration:"`). Sentencepiece BPE deterministic + cache file sha256-stable per Phase 1 F-TOK-1 evidence.
- **F-MIG-3** — `find <source_dir> -name '*.py' -not -name '*.py.txt'` returns empty for all 3 source dirs after rename.
- **F-MIG-4** — `grep -rn '/tmp/tokenizer_64k_multilingual.model' tool/<replacement>.hexa <source_dir>` excluding `.py.txt` parked files returns ONLY spec-mandated hits (doc-comment + resolver rank-3 fallback per spec §2.3). Zero regressions.

## Phase 1 + Phase 2 cumulative status

5 / 6 callers migrated:

| # | Caller | Phase | Hexa | Commit |
|---|---|---|---|---|
| 1 | warmup_probe_real | Phase 1 (BG-μ) | `tool/p9_warmup_probe_real.hexa` | `98b614363` |
| 2 | probe_ubu1_clm_v4_tension | Phase 2 (this BG-φ) | `tool/clm_v4_probe_tension.hexa` | (pending parent commit) |
| 3 | measure_ubu1_clm_v4_full_50k | Phase 2 (this BG-φ) | `tool/clm_v4_measure_full_50k.hexa` | (pending parent commit) |
| 4 | sentinel_train_50k | Phase 2 (this BG-φ) | `tool/p9_sentinel_train_50k.hexa` | (pending parent commit) |
| 5 | qmirror_seeded_ablation_A_2k | Phase 2 (this BG-φ) | `tool/p9_qmirror_seeded_ablation_A_2k.hexa` | (pending parent commit) |
| 6 | eval_clm_v4_hellaswag | Phase 3 (pending) | `tool/p9_path_b_hellaswag_eval.hexa` (TBD) | — |

Both phases share the same primitive: `tool/clm_v4_tokenizer_load.hexa` (Phase 1, commit `98b614363`). All hexa replacements re-emit the same `_resolve_tokenizer()` function inline (HF cache → ckpt dir → /tmp WARN-fallback → FileNotFoundError pointing to plan.md Step 2).

## Phase 3 remaining

**Caller 6 — `ubu1:~/anima/state/p9_path_b_sanity_probe_2026_05_03/eval_clm_v4_hellaswag.py`**

This caller is ubu1-only and uses **byte-fallback** (`[i+4 for i in bytes]`), NOT real sentencepiece — it's a workaround that predates Phase 1's cache resolver. Phase 3 migration target:

1. Replace byte-fallback with real `sp.encode()` against the cache-resolved tokenizer.
2. Emit `tool/p9_path_b_hellaswag_eval.hexa` Mac-side hexa wrapper following the same pattern.
3. Park the ubu1 .py via raw#37 (the file lives on ubu1, not Mac repo, so park form is moot — instead deprecate and replace).
4. Verify F-MIG-1/2/3/4 falsifiers (with F-MIG-2 token-sequence parity additionally checking real-sp vs byte-fallback diff is "expected: byte-fallback was a workaround, real sp.encode is preferred").

## In-flight gate verdict

**OPEN** — at BG start:

- `ssh ubu1 'pgrep -af "sentinel_train_50k|measure_ubu1_clm_v4|probe_ubu1_clm_v4|qmirror_seeded_ablation"'` returned NONE_UBU1.
- Mac `pgrep -af '...'` (filtered for the pgrep-self-match) returned empty.

No in-flight training depended on any of these 4 callers; migration window was OPEN; all 4 callers cleared.

## Honest C3

1. **F-MIG-2 token-sequence parity is logically tight, not literally bit-compared against historical .py runs.** The strongest evidence available is byte-equality of sample_token_ids_prompt0 across all 4 hexa selftests AND Phase 1 BG-μ warmup_probe verdict (`[44357, 601, ...]`). Sentencepiece BPE is deterministic; the cache file's sha256 is bit-identical to the prior `/tmp` file per Phase 1 F-TOK-1. A literal historical-output bit-compare would require .py invocation on Mac (raw#9 violation, out of scope). Same caveat as Phase 1 honest-c3 #2.

2. **F-MIG-4 grep finds 12 literal '/tmp/tokenizer_64k_multilingual.model' hits across the 4 new .hexa files** (3 per file × 4). All are: (a) doc-comment historical record at line 5 of each .hexa, (b) resolver rank-3 deprecation-WARN fallback per spec §2.3, (c) "TOKENIZER: was '/tmp/...' — now resolved" doc-comment. These are NOT regressions — same codified resolver behavior as Phase 1's `tool/p9_warmup_probe_real.hexa`. Future tightening could extract the literal into a shared constants module, but that's gold-plating beyond F-TOK-4 scope.

3. **Gitignore coverage is asymmetric.** Callers 1+2 .py.txt files (in `state/p9_p0_*`) are explicitly gitignored (`.gitignore:194 state/p9_p0_*/`). Callers 3+4 (`state/p9_p1_sentinel_*`, `state/p9_qmirror_seeded_*`) have NO explicit gitignore rule — the parent dirs were ALREADY in `??` untracked status BEFORE this BG (per session-start git status). Renaming `.py` to `.py.txt` removes the `**/*.py` global ignore match but does NOT change the parent dir's untracked posture. **Recommendation for parent session**: consider adding `state/p9_p1_*/` and `state/p9_qmirror_*/` rules symmetric with line 194, OR add `**/*.py.txt` globally. NOT done by this BG (.gitignore is repo policy, out of BG-φ scope).

4. **Selftest scope is intentionally narrow.** Selftests do tokenizer round-trip + decoder/peft import dry-check + (for caller 4) qmirror DRBG dry-instantiate. NO GPU forward, NO ckpt load, NO train loop. Apply-mode bodies preserve the original .py logic verbatim with ONLY the tokenizer-load hardcode swapped for `_resolve_tokenizer()`. Therefore F-MIG-1/2 evidence proves tokenizer wiring; it does NOT prove apply-mode train semantics are byte-identical. Validation of apply-mode equivalence would require a paired (`.py.txt` vs `.hexa --apply`) run-and-compare which is OUT of raw#9 scope. Phase 3 should consider a short ubu1-only paired run on at least one caller (e.g., probe_tension N=10) before retiring `.py.txt` files permanently.

5. **Caller 3 (sentinel_train_50k) is the highest-stakes migration of this cycle** — it's the actual 50K sentinel that gates Phase 2 entry per the `p9_sft.cond.*` roadmap. The hexa wrapper preserves: δ curriculum (early=0.5/mid=1.0/late=2.0), savepoint schedule (5K/10K/25K/50K), HF push to `need-singularity` org, full F1_BLEU1 + F2_phi + F3_tension_mse verdict logic (`F2_PASS_FULL` / `F2_PASS_TIGHT` / `F2_VIOLATION_AT_FINAL`). However the helper is regenerated on each `--apply` invocation from this .hexa SSOT — if a future edit introduces a bug, all subsequent runs use the buggy wrapper. Mitigation: AST validation runs on Mac before scp; ubu1 catches semantic errors at runtime. **Suggested Phase 3 enhancement**: add a `--dry-apply` mode that emits the helper to /tmp + does `sp.encode` on a tiny synthetic batch + decoder build (without ckpt load) to catch import/path regressions before GPU consumption.

## Roadmap update proposal

(Parent session owns roadmap commits — DO NOT edit `.roadmap.*` files from this BG.)

- **Node**: `p9_sft.cond.tokenizer_caller_migration`
- **From**: `partial`
- **To**: `near_complete`
- **Fraction**: 5/6 (Phase 1 = 1 closed; Phase 2 = 4 closed this cycle; Phase 3 ubu1-only = 1 pending)

## Cross-links

- **Spec**: `state/clm_v4_tokenizer_caller_migration_spec_2026_05_04/spec.md` (commit `68803d162`)
- **Phase 1 verdict**: `state/clm_v4_tokenizer_caller_migration_exec_2026_05_04/verdict.json` (commit `98b614363`)
- **Phase 1 handoff**: `docs/clm_v4_tokenizer_caller_migration_landed_2026_05_04.ai.md` (commit `98b614363`)
- **Phase 1 primitive**: `tool/clm_v4_tokenizer_load.hexa` (commit `98b614363`)
- **Phase 1 exemplar**: `tool/p9_warmup_probe_real.hexa` (commit `98b614363`)
- **Propagation plan**: `state/clm_v4_tokenizer_propagation_plan_2026_05_04/plan.md` (Step 2 = ubu1 cache prime, prerequisite for cache-rank-1 hits)

## Files touched this cycle

### Created (Mac repo)

- `tool/clm_v4_probe_tension.hexa`
- `tool/clm_v4_measure_full_50k.hexa`
- `tool/p9_sentinel_train_50k.hexa`
- `tool/p9_qmirror_seeded_ablation_A_2k.hexa`
- `state/clm_v4_tokenizer_caller_migration_phase_2_2026_05_04/verdict.json`
- `state/clm_v4_tokenizer_caller_migration_phase_2_2026_05_04/run.log`
- `state/clm_v4_tokenizer_caller_migration_phase_2_2026_05_04/selftest_clm_v4_probe_tension.log`
- `state/clm_v4_tokenizer_caller_migration_phase_2_2026_05_04/selftest_clm_v4_measure_full_50k.log`
- `state/clm_v4_tokenizer_caller_migration_phase_2_2026_05_04/selftest_p9_sentinel_train_50k.log`
- `state/clm_v4_tokenizer_caller_migration_phase_2_2026_05_04/selftest_p9_qmirror_seeded_ablation_A_2k.log`
- `docs/clm_v4_tokenizer_caller_migration_phase_2_landed_2026_05_04.ai.md` (this doc)

### Renamed (park form, raw#9)

- `state/p9_p0_measure_2026_05_03/probe_ubu1_clm_v4_tension.py` → `.py.txt` (gitignored)
- `state/p9_p0_measure_2026_05_03/measure_ubu1_clm_v4_full_50k.py` → `.py.txt` (gitignored)
- `state/p9_p1_sentinel_2026_05_03/sentinel_train_50k.py` → `.py.txt` (parent dir already untracked)
- `state/p9_qmirror_seeded_2026_05_03/p9_qmirror_seeded_ablation_A_2k.py` → `.py.txt` (parent dir already untracked)

### Transient (ubu1, never committed; raw#37)

- `/tmp/clm_v4_probe_tension_helper.hexa_tmp`
- `/tmp/clm_v4_measure_full_50k_helper.hexa_tmp`
- `/tmp/p9_sentinel_train_50k_helper.hexa_tmp`
- `/tmp/p9_qmirror_seeded_ablation_A_2k_helper.hexa_tmp`

## Raw invariants applied

- **raw#9 strict**: PASS — zero new .py files on Mac. All helpers emitted to `/tmp/<caller>_helper.hexa_tmp` (`.hexa_tmp` extension, NOT `.py`); raw#37 transient-py-on-Linux scp'd to ubu1 + executed via `/home/aiden/venv_orchestrator/bin/python3`; never persisted to Mac repo.
- **raw#10 honest C3**: 5 items above (≥4 required).
- **raw#15 SSOT repo-relative**: PASS — paths in this doc are repo-relative; absolute paths only for ubu1 HF cache (HF design, unavoidable).
- **raw#37 transient-py-on-Linux**: PASS — all 4 helpers run on ubu1 only, never persisted to Mac.
- **raw#71 falsifier preregistered**: PASS — F-MIG-1/2/3/4 preregistered in spec.md §5 commit `68803d162` + Phase 1 BG-μ verdict carry-forward.

## Next-cycle action recommendation

**Phase 3 (final)**: Land `tool/p9_path_b_hellaswag_eval.hexa` replacing the ubu1-only byte-fallback eval at `ubu1:~/anima/state/p9_path_b_sanity_probe_2026_05_03/eval_clm_v4_hellaswag.py`. Once that lands, all 6 known callers are migrated and the migration cycle closes.

**Optional Phase 4 (gitignore symmetry)**: Add `state/p9_p1_*/` and `state/p9_qmirror_*/` to `.gitignore` (or add `**/*.py.txt` globally) to symmetrize with the existing `state/p9_p0_*/` rule at line 194. Repo-policy decision; out of BG-φ scope.

**Optional Phase 5 (apply-mode parity)**: Add a paired ubu1-only run-and-compare for at least one caller (e.g., `probe_tension --apply N=10`) to validate apply-mode train semantics are byte-identical, BEFORE permanently retiring `.py.txt` files.
