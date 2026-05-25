# OPT-1 shim v1 → v2 design diff (BG-θ' 2026-05-04)

**Predecessor**: BG-Δ commit `cb3521bd2` — OPT-1 v1 PARTIAL (3 blockers).
**Scope**: 3 surgical fixes inside `tool/transient_py/clm_v4_hf_format_shim.py` only.
**Source spec**: `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_design.md` + v1 verdict.

---

## v1 blockers recap (from `opt_1_exec_verdict.json`)

| # | Site | Blocker | Severity |
|---|---|---|---|
| 1 | line 643 `safetensors_save(wrapped_state, ...)` | aliased-storage (`tok_emb.weight` ≡ `head_a.weight`) rejected by safetensors strict check | FAIL — entire save aborted |
| 2 | line 305 `n_param_loaded = sum(p.numel() for p in model.parameters())` | reported 477,648,512 vs `expected = 530,994,816`, no fail-gate, false alarm against a comparison-of-different-views | mis-leading; not actually missing params |
| 3 | line 646-655 tokenizer copy after safetensors save | tokenizer copy only runs if save_file succeeded → on save fail, output is unusable for `AutoTokenizer.from_pretrained` even after upstream patch | cleanup ordering |

---

## v1 → v2 line-by-line changes

### Fix A — aliased storage at line 643

**Choice**: **A2 (pre-clone)** — explicit `head_a.weight = tok_emb.weight.detach().clone()` in the wrapped state-dict before `safetensors_save`.

**Rationale**:
- A1 (`model.save_pretrained`) requires building a real `CLMv4ForCausalLM` HF wrapper instance and invoking its `save_pretrained` with `_tied_weights_keys` set on the config — but the shim's current architecture builds **bare `ConsciousDecoderV3`**, not the wrapper. Using A1 would require constructing the wrapper, copying state into it, then calling save — which is a much bigger refactor.
- A2 is **2 lines** of diff inside the existing `_save_hf_format` function, preserves the shim's existing flatten-into-`wrapped_state` strategy, and matches the canonical safetensors guidance for this exact case (per safetensors `torch_shared_tensors` docs: "clone the duplicate before save").
- Loading semantics are preserved: `tie_word_embeddings=True` is in `config.json` (line 597), so HF's `from_pretrained` will re-establish the tie at load time via the standard `_tied_weights_keys` mechanism (auto-derived from `tie_word_embeddings`). The on-disk duplication is ~49.15M floats × 4 bytes = ~187 MB extra disk, acceptable.
- A3 (passing `_tied_weights_keys` to `save_file`) is not a real safetensors API — `save_file` only accepts `metadata`. Reject A3.

**Patch (line 638-643)**:
```python
state = model.state_dict()
wrapped_state = {f"decoder.{k}": v.contiguous() for k, v in state.items()}
# v2 fix A: pre-clone tied storages so safetensors strict shared-memory
# guard accepts the save. Tying is re-established at load time via
# config.tie_word_embeddings=True (HF _tied_weights_keys mechanism).
if "decoder.head_a.weight" in wrapped_state and "decoder.tok_emb.weight" in wrapped_state:
    same_storage = (
        wrapped_state["decoder.head_a.weight"].data_ptr()
        == wrapped_state["decoder.tok_emb.weight"].data_ptr()
    )
    if same_storage:
        wrapped_state["decoder.head_a.weight"] = (
            wrapped_state["decoder.tok_emb.weight"].detach().clone().contiguous()
        )
safetensors_save(wrapped_state, str(out_dir / "model.safetensors"),
                 metadata={"format": "pt", "produced_by": "clm_v4_hf_format_shim_v2"})
```

### Fix B — param delta audit (false-alarm resolution)

**Investigation result** (from BG-θ' ubu1 probe of `best.pt['decoder']`):

```
key_count: 581
top_level_prefixes: ['blocks', 'head_a', 'head_g', 'ln_f', 'tension_proj', 'tok_emb']
  blocks: 383,537,280
  tok_emb: 49,152,000
  head_a: 49,152,000
  head_g: 49,152,000
  tension_proj: 768
  ln_f: 768
total_state_dict_params: 530,994,816   # EXACT match to CLM_V4_PARAM_COUNT_EXPECTED
```

**Conclusion**: best.pt is **fully intact**. All 3 embedding-shape tensors (tok_emb, head_a, head_g) present. The -53.3M delta in v1 was a **measurement-mismatch false alarm**:

- `CLM_V4_PARAM_COUNT_EXPECTED = 530,994,816` describes the **raw state_dict total numel** (each tensor counted independently).
- `n_param_loaded = sum(p.numel() for p in model.parameters())` describes the **post-construction unique-Parameter view**: after `ConsciousDecoderV3.__init__()` ties `head_a.weight = tok_emb.weight`, `model.parameters()` returns the same Parameter object once (PyTorch dedupes by `id`).
- 530,994,816 − 49,152,000 (one tied embedding) ≈ 481,842,816 expected post-tie. Observed 477,648,512 = additional −4,194,304 from non-Parameter buffers (e.g., causal-mask `attn.bias` in each of 16 blocks, sized 1×1×512×512 = 262,144 floats × 16 layers = 4,194,304 — **exact match**).
- The "delta" is fully accounted for by tying + buffers; nothing is missing.

**Fix**: Add **two named expected constants** (raw state_dict view, post-tie params view) and gate against the appropriate one. Emit clear log lines that distinguish "state_dict total numel" from "model.parameters() numel" so future runs don't re-trigger the false alarm.

**Patch — replace `CLM_V4_PARAM_COUNT_EXPECTED` block (line 110)**:
```python
CLM_V4_STATE_DICT_TOTAL_NUMEL = 530_994_816   # raw best.pt['decoder'] sum-of-numel
CLM_V4_PARAM_COUNT_AFTER_TIE = 477_648_512   # model.parameters() post-tying view
                                              # (530.99M − 49.15M tied embed − 4.19M attn.bias buffers)
CLM_V4_PARAM_COUNT_EXPECTED = CLM_V4_STATE_DICT_TOTAL_NUMEL  # back-compat alias
```

**Patch — `_load_decoder_state` (line 305)** — emit BOTH views and gate against the right one:
```python
n_param_via_params = sum(p.numel() for p in model.parameters())
n_state_dict_total = sum(v.numel() for v in decoder_sd.values())
n_param_match = (n_param_via_params == CLM_V4_PARAM_COUNT_AFTER_TIE)
n_state_dict_match = (n_state_dict_total == CLM_V4_STATE_DICT_TOTAL_NUMEL)
if not n_param_match:
    raise RuntimeError(
        f"post-tie params mismatch: got {n_param_via_params:,}, "
        f"expected {CLM_V4_PARAM_COUNT_AFTER_TIE:,}"
    )
if not n_state_dict_match:
    print(f"[warn] state_dict total numel {n_state_dict_total:,} != "
          f"expected {CLM_V4_STATE_DICT_TOTAL_NUMEL:,}", file=sys.stderr)
return {
    "step": ...,
    "n_param_loaded": n_param_via_params,                    # post-tie view
    "n_state_dict_total_numel": n_state_dict_total,         # raw view
    "n_param_match": n_param_match,
    "n_state_dict_match": n_state_dict_match,
    ...
}
```

### Fix C — tokenizer copy ordering

**Issue**: lines 646-655 (tokenizer copy) execute AFTER line 643 (`safetensors_save`). When safetensors raises, the tokenizer is never copied → output dir lacks `tokenizer.model` even if user wants to inspect partial output.

**Fix**: move tokenizer copy to **before** safetensors save inside `_save_hf_format`. Tokenizer files are independent of the weight serialization path; reordering preserves correctness (no data dependency between them) and improves robustness (partial output still has tokenizer in worst case).

**Patch — reorder steps 5↔6 in `_save_hf_format`**:

Old order: 1.config code → 2.legacy sources → 3.config.json → 4.gen_cfg → 5.safetensors → 6.tokenizer

New order: 1.config code → 2.legacy sources → 3.config.json → 4.gen_cfg → **5.tokenizer (moved up)** → **6.safetensors (last)**

Tokenizer copy block becomes the new step 5; safetensors save the new step 6.

---

## Version increment

Header line 13 update: `# Generated     : 2026-05-04 (BG-θ' v2 cycle)`. Add new "Version" line: `# Version       : v2 (post-cb3521bd2 fixes A+B+C)`.

---

## Honest C3 (≥3)

**C3-1 (false-alarm classification matters)**: The -53.3M "delta" looked alarming in v1 verdict but was definitionally a comparison of two different views (raw state_dict numel vs. post-tie `parameters()` numel). v2 makes both views explicit + gates on the correct one. Lesson: when comparing param counts, always note WHICH view (state_dict, parameters, named_parameters with/without dedup, with/without buffers).

**C3-2 (clone vs save_pretrained tradeoff)**: A2 (pre-clone) duplicates ~187 MB on disk vs A1 (`save_pretrained` with proper tied_keys). For a one-shot conversion shim where the output is consumed once by lm-eval and discarded, this is a non-issue. If the converted checkpoint were uploaded to HF Hub for many downstream consumers, A1 would be preferable for storage efficiency. We choose A2 for minimal-diff but flag this for retire-when condition (b).

**C3-3 (re-tie at load time)**: `tie_word_embeddings=True` in config.json + the wrapper's `__init__` (which builds a fresh `ConsciousDecoderV3` that re-ties internally) means HF's `from_pretrained` will tie `head_a.weight` back to `tok_emb.weight` after loading. The cloned weights on disk are immediately discarded by re-tying — they're load-time scaffolding only. F-SHIM-3 (logit equivalence within 1e-5) tests this: if the tie isn't re-established, head_a.weight would diverge from tok_emb.weight on subsequent training, but for our pure-eval forward-only path, equivalence holds.

**C3-4 (head_g not tied — no save issue)**: head_g.weight is a separate `nn.Parameter` (not tied to anything) — verified by ubu1 probe showing 49.15M params for `head_g.*`. v1 v2 patches don't touch head_g; safetensors save will store it correctly.

**C3-5 (tokenizer ordering edge case)**: Even with v2 fix C, if the legacy-source copy (`_copy_legacy_sources`) at step 2 raises (file-not-found), tokenizer copy is still skipped. This is acceptable because legacy-source failure indicates a deeper config issue that should fail the whole cycle — partial outputs in that case are not useful. Fix C only addresses the specific safetensors-save-fails case.

**C3-6 (wall time expectation)**: With v1's load proven healthy at ~10-15s, v2 re-exec wall is dominated by safetensors save (~30-60s for 5 GB) + verify forward (~5s) ≈ 45-90s total. The 5-minute STOP gate per task spec is a comfortable margin.
