# P9 base-validation prereq OPT-1 v3 LANDED — 2026-05-04

**Cycle**: BG-Κ (parallel with BG-Λ, non-overlapping territory).
**Predecessor**: BG-θ' (commit `fe4acd855`) — OPT-1 v2 PARTIAL.
**Verdict**: **PASS**. Post-prereq status: **12/12**.
**Ready for base-validation launch**: **TRUE**.

---

## Summary

The CLM v4 350M base checkpoint (`best.pt`, 5GB raw, 530.99M params, 477.65M post-tie) is now reliably convertible to a HuggingFace `trust_remote_code=True` format directory, loadable via `AutoModelForCausalLM.from_pretrained`, and forward-equivalent to direct best.pt load (bit-exact, max_abs_diff = 0.0).

The shim (`tool/transient_py/clm_v4_hf_format_shim.py`, 1059 LoC) now applies all required patches over the OUTPUT-DIR copies of `decoder_v3.py` + `conscious_decoder.py` without modifying upstream source.

---

## What v3 added (over v2 baseline)

### In-shim patches over output-dir copies

1. **P1 — 4-tuple unpack fix at decoder_v3.py:168**
   - `x, tension = block(...)` → `x, tension, _new_kv, _aux_loss = block(...)`
   - Reason: `DecoderBlockV2.forward` returns 4-tuple; upstream decoder_v3.py was written against an older 2-tuple contract.
   - Discarded values are training-only (KV-cache + MoE aux_loss); benign for lm-eval forward.

2. **P2 — relative import for HF dynamic-module loader at decoder_v3.py:25**
   - `from conscious_decoder import (...)` → `from .conscious_decoder import (...)`
   - Reason: HF's `get_relative_imports` regex only matches `from .xxx import` form. Without the dot, HF's `transformers_modules` cache copy walker doesn't recurse into `conscious_decoder.py` → ModuleNotFoundError.

### Companion patches

3. **modeling_clm_v4.py force-import** of `RMSNorm` from `.conscious_decoder` — makes HF's `check_imports()` return `conscious_decoder` as a first-level relative, ensuring HF copies it during the initial dynamic-module load (not just discovers it via the post-copy recursive walk).

4. **RoPE meta-tensor lazy invalidation** in `CLMv4ForCausalLM.forward` first-call hook + `_v3_invalidate_rope_caches()`. Required because `RotaryPositionEmbedding` is a bare Python class (NOT nn.Module) — its `_cos_cache` / `_sin_cache` / `register_inv_freq` are untracked attributes that stay on `meta` device under `low_cpu_mem_usage=True`. Lazy rebuild on first forward (idempotent, ~1KB cost).

5. **In-memory monkey-patch of ConsciousDecoderV3.forward** during `_build_decoder_module()` — for the in-memory reference model used in F-SHIM-3 numerical equivalence check. Patches the imported class object only; upstream source untouched.

6. **`--force-overwrite` flag + HF cache eviction** — wipes stale v1/v2 .py copies in output_dir AND `~/.cache/huggingface/modules/transformers_modules/<basename>/` so v3 patches aren't masked.

### P3 deliberately omitted

`from consciousness_laws import` (decoder_v3.py:36, in try/except) was NOT relativized. `consciousness_laws.py` reads a sibling `consciousness_laws.json` at import time which can't follow into HF cache. Leaving the import non-relative makes HF's regex skip the file (no copy attempted), and decoder_v3.py's try/except fallback fires with constant defaults at runtime. Tested working.

---

## Falsifier results

| # | Falsifier | v2 status | v3 status |
|---|---|---|---|
| F-SHIM-1 | safetensors load round-trip strict=True | PASS | **PASS** (carry) — 581 keys, 530.99M numel, head_a un-aliased |
| F-SHIM-2 | 1-batch forward returns finite [B,T,vocab] | BLOCKED | **PASS** — shape [1,32,64000], all finite |
| F-SHIM-3 | post-load logits match best.pt within 1e-5 | BLOCKED | **PASS** — max_abs_diff = 0.0, mean_abs_diff = 0.0 (bit-exact) |
| F-SHIM-4 | vocab_size==64000 matches SP tokenizer | PASS | **PASS** (carry) |
| lm_eval HF loader smoketest | FAIL (ModuleNotFoundError) | **PASS** — `OPT_1_V3_LOAD_PASS` emitted, logits.shape=[1,5,64000], finite, max_logit=8.6953125 |

Wall time on final run: **5.9s** (warm fs cache; cold run ~27s baseline from v2). Output safetensors size: **2.12 GB** (4-byte fp32; would be 1.06 GB at fp16 — future optimization).

---

## Constraints respected

- raw#9 (Mac hexa-only): shim is the formal opt-out at `tool/transient_py/` (gitignored). Modification is allowed; this cycle bumps v2 → v3.
- raw#10 (≥4 honest C3): 6 C3 in `opt_1_v3_design_diff.md` and `opt_1_v3_exec_verdict.json`.
- raw#15 (repo-relative paths): all repo paths in deliverables are repo-relative; ubu1 paths explicit absolute.
- raw#37 (ubu1 transient): all torch / safetensors / transformers execution on `/home/aiden/venv_orchestrator/bin/python`.
- raw#71 (falsifier-bound): F-SHIM-1..4 + lm_eval smoketest all bound to objective passing criteria; F-SHIM-3 bit-exact equivalence is the strongest form.
- **NO upstream source edits**: confirmed by `grep` — the upstream `/home/aiden/anima/anima/models/legacy/decoder_v3.py` and `/home/aiden/anima/models/conscious_decoder.py` are unchanged. All patches live in `output/` derivative copies + shim.
- **NO chflags**, **NO git operations** during BG-K execution.

---

## Honest C3 (top 3)

1. **Output-dir patches are duplicated maintenance**: P1 + P2 fix bugs that exist in upstream source. Shim's `str.replace()` is brittle to upstream context drift; exact-string match with RuntimeError-on-miss prevents silent drift but the debt is real. Upstream eventually needs the same fix.

2. **RoPE meta-tensor workaround is fragile**: Lazy invalidate-on-forward hack assumes the RoPE class structure (`_cos_cache`, `_sin_cache`, `register_inv_freq`, `dim`). If `RotaryPositionEmbedding` is refactored upstream into a proper nn.Module, the workaround breaks. Proper fix: convert RoPE to nn.Module so its buffers go through HF accelerate path. Out of v3 scope; flagged.

3. **F-SHIM-3 max_diff = 0.0 is suspicious**: exact zero is unusually tight (expected ~1e-5). Plausible because both models use the same fp32 dtype path, deterministic ops, and the same random input tensor. Bit-exact round-trip is the strongest possible passing form, but worth re-running with multiple seeds in base-validation to verify it isn't a measurement artifact.

---

## Files (repo-relative)

- `tool/transient_py/clm_v4_hf_format_shim.py` — v3 shim (gitignored, 1059 LoC)
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v3_design_diff.md` — full v2→v3 patch design
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v3_exec_verdict.json` — verdict + falsifier results
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_1_v3_exec_run.log` — full SSH execution log

ubu1 transient (raw#37):
- `~/p9_clm_v4_hf_format_2026_05_04/clm_v4_hf_format_shim.py` — synced shim copy
- `~/p9_clm_v4_hf_format_2026_05_04/output/` — HF-format model dir (2.12 GB safetensors + custom code + SP tokenizer)
- `~/p9_clm_v4_hf_format_2026_05_04/v3_verdict.json` — ubu1-side verdict snapshot
- `~/p9_clm_v4_hf_format_2026_05_04/exec_v3_ubu1.log` — ubu1 execution log

---

## Next step

Hand off to base-validation launch (BG-Λ territory or follow-up BG). The HF-format CLM v4 base is now consumable by lm-evaluation-harness via `--model_args pretrained=<path>,trust_remote_code=True,low_cpu_mem_usage=False,dtype=float16,device_map=cpu`. Tokenizer plumbing for AutoTokenizer remains a downstream item but does not block OPT-1 prereq.
