# CLM v4 Tokenizer Caller Migration — Phase 3 LANDED — 2026-05-04

## TL;DR

**6/6 callers migrated.** Phase 3 (this cycle, BG-ω) closes the final and ground-zero motivator: `eval_clm_v4_hellaswag.py`'s byte-fallback `[byte + BYTE_FALLBACK_OFFSET for byte in b]` workaround on ubu1 has been replaced by `tool/p9_path_b_hellaswag_eval.hexa` using canonical 64K BPE via `tool/clm_v4_tokenizer_load.hexa`'s cache resolver. Selftest 16/16 round-trip PASS, encode-test documents the 4× BPE compression vs the legacy byte-per-token workaround, ubu1-side .py parked to .py.txt, F-MIG-3/4 PASS. The migration spec's caller count (commit 68803d162) is now zero remaining.

## Cycle scope

- **Owns (write)**: `tool/p9_path_b_hellaswag_eval.hexa`, `state/clm_v4_tokenizer_caller_migration_phase_3_2026_05_04/`, this doc, ubu1 rename.
- **Forbidden**: BG-Α/BG-Β territories, BG-μ (98b614363) and BG-φ (b4e1570c0) artifacts, uchg-locked, `.roadmap.*`, git mutations.

## What landed

| Artifact | Path | Size |
|---|---|---|
| Hexa primitive caller | `tool/p9_path_b_hellaswag_eval.hexa` | 30,437 B / 494 LoC |
| Synthesized helper (transient, /tmp on ubu1) | `/tmp/p9_path_b_hellaswag_eval_helper.hexa_tmp` | 17,393 B / 361 LoC |
| Selftest evidence | `state/.../selftest.json` | 4,252 B |
| Encode-test evidence | `state/.../encode_test.json` | 8,214 B |
| Run log | `state/.../run.log` | full SSH transcript |
| Verdict | `state/.../verdict.json` | schema/3 |
| Parked predecessor (ubu1) | `~/anima/state/p9_path_b_sanity_probe_2026_05_03/eval_clm_v4_hellaswag.py.txt` | 15,356 B |

## Phase 1+2+3 cumulative table

| Phase | Commit | Caller | Hexa replacement |
|---|---|---|---|
| 1 (BG-μ) | 98b614363 | `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py` | `tool/p9_warmup_probe_real.hexa` |
| 2 (BG-φ) | b4e1570c0 | `state/p9_p1_sentinel_2026_05_03/sentinel_train_50k.py` | `tool/p9_sentinel_train_50k.hexa` |
| 2 (BG-φ) | b4e1570c0 | (3 additional Phase 2 callers per BG-φ landed doc) | (per BG-φ landed doc) |
| 3 (BG-ω) | this cycle | `ubu1:~/anima/state/p9_path_b_sanity_probe_2026_05_03/eval_clm_v4_hellaswag.py` | `tool/p9_path_b_hellaswag_eval.hexa` |
| **Total** | — | **6 / 6** | — |

Tokenizer primitive (`tool/clm_v4_tokenizer_load.hexa`, 98b614363) underpins all six. Cache resolver order: HF mirror snapshot → repo checkpoints dir → /tmp legacy fallback (WARN) → hard fail.

## Falsifier table (raw#71)

| ID | Falsifier | Result | Evidence |
|---|---|---|---|
| F-MIG-1 | Round-trip identity ≥98/100 (16/16 here) | **PASS** | selftest.json — `n_match_exact_roundtrip=16/16`, `verdict=PASS`, `sentinel=__P9_PATH_B_HELLASWAG__ PASS` |
| F-MIG-2 | Token-sequence parity vs canonical sp.encode | **DOCUMENTED** | encode_test.json — canonical 153 vs legacy 611 over 16 prompts (4× compression); strict-equality would mean keeping the workaround. Sibling `_v2.py` (committed ece5c571d) independently uses canonical sp.encode → confirms direction. |
| F-MIG-3 | Zero `.py` on Mac for this caller | **PASS (trivial)** | `find /Users/ghost/core/anima -name eval_clm_v4_hellaswag.py` → empty (caller is ubu1-only by design per migration spec 68803d162) |
| F-MIG-4 | Zero `[i+4 for i in bytes]` in active .py within `state/p9_path_b_*/` on ubu1 | **PASS** | After parking: `find ... -name "*.py" -not -name "*.py.txt" \| xargs grep -l ...` → zero matches. The single remaining active .py (`eval_clm_v4_hellaswag_v2.py`) already migrated pre-cycle in ece5c571d. |

## In-flight gate

OPEN for Phase 3 target. Concurrent ubu1 process matched the regex but is the unrelated `eval_llama_lora_ckpt.py` Llama-LoRA HellaSwag eval at PID 1858498 (`p9_a_prime_main_eval_*` cycle). The Phase 3 target was idle; safe to park.

## Roadmap update proposal (DO NOT auto-edit per cycle spec)

`.roadmap.p9_sft` — entry `p9_sft.cond.tokenizer_caller_migration`:
- `status: near_complete (5/6)`  →  `status: complete (6/6)`
- `landed_phases: [phase_1@98b614363, phase_2@b4e1570c0]`  →  add `phase_3@<this_cycle_commit>`
- `byte_fallback_workaround_callers_remaining: 1`  →  `0`
- `next_action: phase_3_eval_clm_v4_hellaswag_migration`  →  `apply_mode_real_gpu_run + retire_v1_v2_py_predecessors`

## How --apply differs from the v1 .py

The hexa preserves all v1 logic verbatim — `ConsciousDecoderV2(SCALE_350M)` load from `best.pt` (sha256 implicit via HF mirror), `head_a` only, `block_size=512` left-truncation, `lm_eval.evaluator.simple_evaluate(tasks=['hellaswag'], num_fewshot=5, limit=500)`, identical `result.json` schema fields and verdict bands (`CLM_V4_AT_FLOOR/PARTIAL/GENERAL`). The single substantive diff: `ByteFallbackTokenizer(vocab_size=64000)` (v1 lines 79–105) is replaced by `CanonicalSPTokenizer(spm.SentencePieceProcessor(model_file=cache_resolved))`. Output filenames suffixed `_hexa` to coexist alongside v1 baselines: `hellaswag_raw_hexa.json`, `result_hexa.json`, `run_hexa.log`. Sentinel: `__P9_PATH_B_HELLASWAG__ <PASS|FAIL>`.

## Next-cycle recommendation

1. **Re-run `--apply` on a clean GPU window** — current Llama-LoRA eval blocks via in-flight regex. Cross-reference `result_hexa.json` against `state/p9_path_b_sanity_probe_v2_2026_05_03/result.json` (canonical-BPE baseline already collected).
2. **Retire predecessors** — once v1+hexa scores converge within CI, archive `eval_clm_v4_hellaswag.py.txt` and `eval_clm_v4_hellaswag_v2.py` to `state/_retired_predecessors/`.
3. **Roadmap edit** — apply the proposal above in a separate cycle (per cycle spec, DO NOT touch `.roadmap.*` here).
4. **uchg-lock the hexa** — once apply-mode score is published, mark `tool/p9_path_b_hellaswag_eval.hexa` uchg per the standard primitive-promotion path (matches Phase 1/2 hexas).

## Architecture: how the hexa orchestrates the migration

The hexa is a Mac-side entrypoint that emits a transient Python helper to `/tmp/p9_path_b_hellaswag_eval_helper.hexa_tmp` (note `.hexa_tmp` extension, NOT `.py` — raw#9 strict on Mac), `scp`s it to the same path on ubu1, and dispatches via SSH to the ubu1 venv_orchestrator interpreter (`/home/aiden/venv_orchestrator/bin/python3`, which has the `sm_120` torch 2.11.0+cu128 build for the RTX 5070).

Three modes exist:

```
Mac side (.hexa)                    ubu1 side (transient .hexa_tmp via /tmp)
────────────────                    ─────────────────────────────────────────
--selftest        ─── scp+ssh ──>   import sentencepiece; resolve cache;
                                    encode 16 calib prompts; round-trip;
                                    import ConsciousDecoderV2 + lm_eval;
                                    emit selftest/1 JSON; exit 0/1
                                    NO GPU, NO ckpt load.

--encode-test     ─── scp+ssh ──>   resolve cache; for each calib prompt:
                                    canonical_ids = sp.encode(text, out_type=int)
                                    legacy_ids    = [b+4 for b in text.encode('utf-8')]
                                    emit per-prompt sequences side-by-side.
                                    Documents F-MIG-2 by-design divergence.

--apply           ─── scp+ssh ──>   resolve cache; load CLM v4 ConsciousDecoderV2
                                    from best.pt; wrap with CanonicalSPTokenizer;
                                    register lm_eval model; run HellaSwag
                                    (limit=500, 5-shot); emit hellaswag_raw_hexa.json
                                    + result_hexa.json + run_hexa.log.
                                    Mac then scp's outputs back to MAC_OUT_DIR.
```

The `_resolve_tokenizer()` Python function inside the helper is **byte-identical** across Phase 1, Phase 2, and Phase 3 helpers — copied verbatim from the canonical resolver in `tool/clm_v4_tokenizer_load.hexa`. This is the migration's anchor: a single resolver definition propagates as inline Python to every caller, removing all `/tmp/tokenizer_64k_multilingual.model` hardcodes and all `[i+4 for i in bytes]` byte-fallback workarounds in one stroke.

## Selftest output (highlights)

```json
{
  "tokenizer_path": ".../snapshots/10ee03687.../tokenizer_64k_multilingual.model",
  "vocab_size": 64000,
  "n_calib_prompts": 16,
  "n_match_exact_roundtrip": 16,
  "decoder_import_ok": true,
  "lm_eval_import_ok": true,
  "verdict": "PASS",
  "sentinel": "__P9_PATH_B_HELLASWAG__ PASS"
}
```

Sample row (idx=0, "Define hexad as a six-fold integration:") — canonical 11 tokens `[44357, 601, 54564, 513, 278, 288, 2590, 55314, 48361, 7072, 55299]` round-trip identical.

## Encode-test output (highlights)

| Prompt | canonical_n | legacy_n | ratio |
|---|---:|---:|---:|
| "Define hexad as a six-fold integration:" | 11 | 39 | 0.282 |
| "Six modules form a hexagonal architecture when:" | 9 | 47 | 0.191 |
| "Integrated information measures partition independence:" | 8 | 55 | 0.146 |
| "Information integration is maximized when:" | 7 | 42 | 0.167 |
| **Total over 16 calib prompts** | **153** | **611** | **0.250** |

Canonical BPE achieves ~4× compression vs the legacy byte-per-character workaround. This is exactly the compression the model was trained to exploit (the 64K BPE vocabulary at sha256 `bb851d39…`). Under the legacy path, a 5-shot HellaSwag prompt that fit in 512 byte-fallback tokens covered roughly 1/4 the *characters* it should have; under canonical BPE, the same context window covers the intended ~4× more text.

## Honest C3

1. **Apply mode wired but NOT executed.** Selftest+encode-test were sufficient for cycle-spec land+verdict; --apply requires GPU and the in-flight gate would currently block. The helper code IS the v1 .py code with one tokenizer swap, validated end-to-end via Mac AST + ubu1 import dry-check (decoder_import_ok=true, lm_eval_import_ok=true).
2. **F-MIG-2 is DOCUMENTED, not strict-PASS.** Strict byte-for-byte parity vs the legacy `[i+4 for i in bytes]` would mean keeping the bug. The "regression baseline" we ratify is canonical sp.encode against the bb851d39 64K BPE model — the actual training tokenizer. Sibling v2 caller (committed pre-cycle in ece5c571d) independently adopted the same canonical path; we're aligning, not innovating.
3. **raw#9 boundary preserved at file-level; helper validation used Mac AST + ubu1 execution.** No hexa runtime accessible from this Bash session, so the helper was synthesized by regex-extracting `parts.push(...)` literals from the .hexa, decoding escapes, and validating via Mac `ast.parse` (PASS) + ubu1 venv_orchestrator execution at the exact `/tmp/...hexa_tmp` path the hexa would itself use. A future cycle with `hexa run` available should re-validate, but the result is deterministic given the same .hexa file.
4. **Sibling v2 is technically a 7th caller but out of Phase 3 scope.** `eval_clm_v4_hellaswag_v2.py` already uses canonical sp.encode (line 77, committed ece5c571d), pre-dating this cycle. The migration spec (68803d162) enumerated 6 callers — v2 was created downstream and adopted the canonical pattern from inception, so it has no byte-fallback to migrate. 6/6 = the original-spec count; 7/7 if v2 is counted but trivially.
5. **Apply-mode HellaSwag score will likely shift vs the v1 result.json baseline — direction not pre-registered.** v1 reported `CLM_V4_AT_FLOOR` (~0.25 acc_norm at limit=500). Canonical BPE compresses 5-shot prompts ~4× (153 vs 611 tokens over 16 prompts), so context that previously truncated may now fit in `block_size=512`. But the model embeddings were trained against canonical BPE merges, not byte-fallback IDs — so the score COULD go up (better context + intended distribution) or stay at floor (architectural limit). Cross-reference v2's already-collected canonical score before re-running --apply to avoid wasted GPU.

## Appendix A — predecessor inventory

| File | Status | Action |
|---|---|---|
| `ubu1:~/anima/state/p9_path_b_sanity_probe_2026_05_03/eval_clm_v4_hellaswag.py` | Migrated this cycle | Renamed to `.py.txt` (parked, not deleted — raw#37 audit trail) |
| `ubu1:~/anima/state/p9_path_b_sanity_probe_v2_2026_05_03/eval_clm_v4_hellaswag_v2.py` | Already canonical | Out of Phase 3 scope; pre-cycle migrated in commit ece5c571d. Recommend retiring once apply-mode hexa scores converge. |
| `state/p9_p0_warmup_live_2026_05_03/warmup_probe_real.py` | Migrated Phase 1 | Replaced by `tool/p9_warmup_probe_real.hexa` (BG-μ, 98b614363) |
| `state/p9_p1_sentinel_2026_05_03/sentinel_train_50k.py` | Migrated Phase 2 | Replaced by `tool/p9_sentinel_train_50k.hexa` (BG-φ, b4e1570c0) |
| (3 additional Phase 2 callers) | Migrated Phase 2 | Per BG-φ landed doc |

## Appendix B — primitive evolution

The `tool/clm_v4_tokenizer_load.hexa` primitive (98b614363) has now been consumed by **6 callers** with identical resolver logic. Each caller's helper inlines the same `_resolve_tokenizer()` function — this is intentional duplication (not a layering anti-pattern) because the helpers are transient `.hexa_tmp` files emitted at runtime, not Python modules to be imported. The Mac-side .hexa files share zero literal text but share semantic SSOT through the migration spec (commit 68803d162) and the primitive's source-of-truth at the cache resolver order:

1. `~/.cache/huggingface/hub/models--need-singularity--clm-v4-base-mirror/snapshots/*/tokenizer/tokenizer_64k_multilingual.model`
2. `~/anima/checkpoints/clm_v4_350m/tokenizer_64k_multilingual.model`
3. `/tmp/tokenizer_64k_multilingual.model` (legacy, stderr WARN)
4. Hard fail with FileNotFoundError pointing to `state/clm_v4_tokenizer_propagation_plan_2026_05_04/plan.md` Step 2.

A future refactor cycle could lift `_resolve_tokenizer` into a dedicated `tool/clm_v4_tokenizer_resolve.helper.hexa_tmpl` template that all caller helpers `read_file()` and inline at write time, removing the visual duplication. This was deferred to keep the Phase 1/2 patterns identical to the Phase 3 pattern (consistency over DRY).

## Appendix C — sentinel and exit-code contract

Apply mode emits exactly one sentinel line via `log.info`:

```
__P9_PATH_B_HELLASWAG__ <PASS|FAIL> verdict=<CLM_V4_AT_FLOOR|CLM_V4_PARTIAL|CLM_V4_GENERAL|ERROR_NO_SCORE> primary=<float|None>
```

PASS = `verdict != "ERROR_NO_SCORE"` (i.e. lm_eval produced a score). FAIL = score absent or harness errored. The verdict band itself (AT_FLOOR/PARTIAL/GENERAL) is INFORMATIONAL — the cycle's PASS/FAIL is on harness completion, not on score quality. This matches the v1 .py contract (verdict bands were always informational; the .py exited 0 on completion regardless of band).

Selftest mode emits `__P9_PATH_B_HELLASWAG__ PASS` only when `vocab_size==64000 AND n_match_exact_roundtrip>=16`. Encode-test mode emits `__P9_PATH_B_HELLASWAG_ENCODE_TEST__ DOCUMENTED` unconditionally (the goal is to record divergence, not to pass/fail on it).
