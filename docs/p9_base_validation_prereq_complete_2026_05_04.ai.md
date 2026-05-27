# P9 Base Validation Prereq — OPT-1 Exec Status (PARTIAL)

ts_utc: 2026-05-04T01:55:04Z
cycle: opt_1_exec_2026_05_04
verdict: **PARTIAL** (not the success-path doc — this is the partial-state handoff per BG-Δ instructions)

## TL;DR

OPT-1 (CLM v4 HF format shim conversion) was attempted and **failed at safetensors save**, not at load. Pre-flight, transfer, and dry-run all passed. The actual conversion correctly loaded the 5 GB best.pt checkpoint (step=20000, ce=0.046, best_phi=37.270) but `_save_hf_format()` raised `RuntimeError: shared tensors` because `decoder.tok_emb.weight` and `decoder.head_a.weight` alias the same storage (intentional weight tying — `tie_word_embeddings=True`). The shim's own configuration documents this tying in four locations, but its serializer at line 643 calls `safetensors.torch.save_file()` directly without resolving aliased storages, which the strict shared-memory guard rejects.

**Prereq status remains 11/12. Base-validation BG cycle CANNOT launch yet.** Shim v2 is required.

## What completed

- Pre-flight (5/5): shim source exists Mac-side, best.pt symlink resolves on ubu1, 587 GB disk free, transformers + safetensors loadable, HF auth valid (user `dancinlife`).
- Shim transfer to ubu1 (`~/p9_clm_v4_hf_format_2026_05_04/clm_v4_hf_format_shim.py`, 36715 bytes, 789 LoC).
- Dry-run on ubu1: PASS — plan emitted, expected_param_count=530,994,816, expected_decoder_keys=581, vocab_size=64000.
- Checkpoint LOAD path on ubu1: PASS — `[shim] decoder loaded: step=20000, ce=0.04630279541015625, best_phi=37.270, params=477,648,512`.
- Output dir partially populated: `__init__.py`, `config.json`, `configuration_clm_v4.py`, `conscious_decoder.py`, `decoder_v3.py`, `generation_config.json`, `modeling_clm_v4.py` (62,649 B total).

## What blocked

Bug at `tool/transient_py/clm_v4_hf_format_shim.py:643` — `safetensors_save(wrapped_state, ...)` rejects tied storages.

Stack:
```
RuntimeError: Some tensors share memory ... [{'decoder.tok_emb.weight', 'decoder.head_a.weight'}].
A potential way to correctly save your model is to use `save_model`.
```

The shim's *config* declares `tie_word_embeddings=True` (lines 354, 597) and its `set_input_embeddings()` re-applies tying at line 451-452 — but the serializer doesn't pre-clone or use `model.save_pretrained(safe_serialization=True)` (which would handle ties via HF's `_tied_weights_keys` machinery).

Per BG-Δ scope rule "DO NOT modify the shim source", no fix was applied. This is a BG-Β shim-v2 task.

## Secondary concern (not the primary blocker, but flagged)

Loaded `params=477,648,512` is 53.3 M LESS than the dry-run expected `530,994,816`. Closest single-tensor explanations:
- `head_g` (second head, 64000×768 = 49.15 M) absent from best.pt: ~92% of gap.
- Embedding double-count error in expected constant: also ~49.15 M; ~92% of gap.
- Either way, ~4 M residual unexplained — needs key-by-key audit before any base-validation interprets the numbers.

The shim did NOT flag this delta as a load-time falsifier. Even if save is fixed, this discrepancy must be resolved before lm-eval scores can be trusted as representing "the 530 M CLM v4 architecture".

## Falsifier matrix

| Falsifier | Verdict | Reason |
|---|---|---|
| F-SHIM-1 safetensors load round-trip | BLOCKED_NOT_RUN | model.safetensors never written |
| F-SHIM-2 1-batch forward finite [B,T,vocab] | BLOCKED_NOT_RUN | --verify gated on save |
| F-SHIM-3 logit equiv to best.pt within 1e-5 | BLOCKED_NOT_RUN | same |
| F-SHIM-4 vocab_size == 64000 | BLOCKED_NOT_RUN | no end-to-end load |
| lm_eval AutoModelForCausalLM smoketest | BLOCKED_NOT_RUN | requires safetensors |

## Resource accounting

- Wall: ~22 s (FAIL pre-save, no 30-60 min compute incurred).
- RAM peak: not sampled (process exited too fast); load phase succeeded so peak was likely the planned ~5 GB transient.
- Disk consumed: ~99 KB on ubu1 (shim + partial output). Output dir intact for inspection.

## Next action — exact handoff to BG-Β

Required edits to `tool/transient_py/clm_v4_hf_format_shim.py`:

1. **Tied-weight save fix** at `_save_hf_format()` (around line 643). Pick one:
   - Replace direct `safetensors_save()` with `model.save_pretrained(out_dir, safe_serialization=True)` (HF auto-handles ties).
   - OR pre-clone: `wrapped_state["decoder.head_a.weight"] = wrapped_state["decoder.tok_emb.weight"].detach().clone()` before the `safetensors_save()` call. Note: this defeats tying on disk; option A is preferred.

2. **Param-count audit gate** at load: assert `loaded_params == expected_param_count` (or exit with explicit failure) before proceeding. Currently the -53.3 M delta is silent. Determine ground truth: either correct `expected_param_count` constant to 477,648,512 (if best.pt is design-correct and missing head_g is intended) or fail load if best.pt is incomplete.

3. **Tokenizer-copy ordering** so it doesn't depend on safetensors save success — copy tokenizer files first OR independently, since output dir currently looks viable but lacks tokenizer.

After shim-v2 lands, re-exec is fast (~1-2 min, dominated by torch.load) — load already proven healthy. A subsequent BG-Δ' should re-run dry-run + execute + F-SHIM-1~4 + lm_eval smoketest.

## Prereq scoreboard

Before this cycle: 11/12 (per BG-Β design 387200362).
After this cycle: **11/12 (unchanged)**.
Ready for base-validation launch: **NO**.

## Artifacts

- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_exec_verdict.json` — full structured verdict
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_exec_run.log` — full SSH/exec log
- ubu1: `~/p9_clm_v4_hf_format_2026_05_04/clm_v4_hf_format_shim.py` — transferred shim copy
- ubu1: `~/p9_clm_v4_hf_format_2026_05_04/output/` — partial output (no weights)
- ubu1: `~/p9_clm_v4_hf_format_2026_05_04/dry_run_ubu1.log`, `exec_ubu1.log` — raw remote logs

## Honest C3 (top 3 of 5 — full set in verdict.json)

1. **Shim self-contradiction**: tying is configured in 4 places but the serializer ignores it, and the shim's own RuntimeError message quotes the canonical fix. This is a known-pattern bug, not an environment quirk.
2. **Param-count -53.3 M not flagged**: the shim proceeded past load even though loaded count was 53.3 M short of expected. Without a load-time gate, future runs could silently produce HF dirs that don't match the 530 M architecture claim.
3. **Scope-bound non-fix**: BG-Δ explicitly was told not to modify shim source; with that rule, OPT-1 cannot complete on this revision. No silent workaround attempted. Hand-off is clean.
