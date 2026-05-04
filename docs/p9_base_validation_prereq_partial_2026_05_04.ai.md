# P9 base-validation prereq partial landing — OPT-A done, OPT-1 pending

**Date**: 2026-05-04 (UTC 00:48Z)
**Cycle**: BG-χ OPT-A Llama-3.2-3B base download retry
**Status**: PARTIAL — 11/12 prereqs landed; OPT-1 (CLM v4 HF format shim) deferred to post-quota-reset cycle

---

## Summary (TL;DR)

BG-π hit HF quota before completing OPT-A and OPT-1. BG-χ (this cycle) retried OPT-A only — atomic ~5min op — and confirmed PASS:

- **HF auth** (post eea009b40 token re-write): whoami-v2 returns `dancinlife` (PASS, no 401)
- **Gated access** to `meta-llama/Llama-3.2-3B`: ACCEPTED (HEAD config.json → HTTP 200, x-repo-commit matches; field `gated="manual"` but token authorized)
- **Download**: 15/15 files cached, 12GB on disk (incl. `original/` PyTorch consolidated.pth ~5.5GB; raw safetensors ~6.4GB across 2 shards). Snapshot `13afe5124825b4f3751f836b40dafda64c1ed062`.
- **Smoketest** (CPU fp16, 1 forward pass): logits.shape=`[1,3,128256]`, vocab_size=128256, hidden_size=3072 → **PASS**

OPT-1 (CLM v4 HF format shim) is the remaining prereq for full 12/12 base-validation launch readiness. Deferred to next cycle when BG-π's HF quota resets at 2026-05-04 12:10pm KST.

---

## Prereq matrix delta

| # | Prereq | Pre-BG-χ | Post-BG-χ |
|---|--------|----------|-----------|
| 1-10 | (existing prereqs from BG-ν handoff) | ✓ | ✓ |
| 11 | **OPT-A: Llama-3.2-3B base downloaded + smoketest** | ✗ | **✓ (this cycle)** |
| 12 | OPT-1: CLM v4 HF format shim | ✗ | ✗ (next cycle) |
| **Total** | | **10/12** | **11/12** |

---

## Why OPT-A was required (anchor-A spec dependency)

Per `state/p9_base_validation_prep_2026_05_04/launch_handoff.md`:

- Spec §3.1 anchor-A baseline = `Llama-3.2-3B` **base** (not Instruct)
- Llama-3.2-3B-Instruct was pre-cached on ubu1 (different artifact, RLHF-tuned)
- Using Instruct in place of base would require spec amendment (§2.6 caveat per §7.1(a)) with new dated spec doc
- Cleaner path: download base, hold spec stable

OPT-A therefore unblocks anchor-A without spec churn.

---

## What's still blocked (OPT-1)

OPT-1 is the CLM v4 HF format shim — converts CLM v4's native checkpoint format (64K SentencePiece tokenizer + custom architecture wrapping) into a HuggingFace-compatible directory so lm-eval-harness can load it the same way it loads Llama-3.2-3B base.

Reasons OPT-1 is heavier than OPT-A:

1. Requires longer compute (model state_dict transcoding, tokenizer reformatting, config.json synthesis)
2. Tokenizer format mismatch: CLM v4 SentencePiece (64K) vs HF-standard tokenizer.json (BPE/tiktoken-style)
3. Validation step needed (sanity gen on shim'd model, compare to native CLM v4 inference path)

Estimated ~30-90min once started; was the expected source of BG-π's quota burn.

---

## Honest C3 (≥4 per raw#10)

1. **Gated access ToS-bound**: Meta retains right to revoke `meta-llama/Llama-3.2-3B` access; current grant is on account `dancinlife` and tied to the cached HF token. Machine relocations or token rotations may require re-acceptance.
2. **Download size variability**: 12GB cache includes `original/` PyTorch consolidated.pth which lm-eval/transformers does not consume. Selective `--include "*.safetensors" "*.json" "tokenizer*"` would save ~46% (~5.5GB). Not done here for spec compliance — full clone is what `hf download <repo>` defaults to.
3. **Tokenizer format gap with CLM v4**: Llama-3.2-3B base uses 128256-vocab tiktoken-style BPE; CLM v4 uses 64K SentencePiece. Anchor-A comparison must hold tokenizer constant per-substrate (Llama tokenizer for Llama path, CLM v4 SentencePiece for CLM v4 path) — not interchange. OPT-1 must explicitly handle tokenizer translation in spec §3.1.
4. **CPU smoketest blind to GPU paths**: smoketest ran fp16 on CPU (raw#37 transient OK; avoids GPU contention). Does not validate CUDA kernels, flash-attention, sm_120 (RTX 5070) compat, or OOM at full bs/ctx. H100 launch may surface GPU-only failures the smoketest cannot pre-detect.
5. **Spec §3.1 example drift**: Spec snippet predicted `logits.shape=[1,2,128256]` (2 tokens for "hello world"); actual was 3 due to default `add_special_tokens=True` prepending BOS. Behavior is correct; spec example is the deviant. Update on next amendment cycle.

---

## Next cycle (post quota reset 12:10pm KST)

1. **OPT-1**: Build CLM v4 HF format shim
   - Output dir: `state/clm_v4_hf_format_shim_2026_05_04/` (or next-day stamp if reset slips)
   - Convert CLM v4 latest checkpoint → HF-loadable AutoModelForCausalLM artifact
   - Smoketest analogous to OPT-A (CPU fp16, 1 forward pass, shape/vocab/hidden assert)
2. **12/12 ready**: trigger anchor-A base-validation launch (spec'd elsewhere)

---

## Deliverable trail

- `state/p9_base_validation_prereq_exec_2026_05_04/opt_a_verdict.json` (machine-readable verdict)
- `state/p9_base_validation_prereq_exec_2026_05_04/opt_a_run.log` (full SSH transcript)
- `docs/p9_base_validation_prereq_partial_2026_05_04.ai.md` (this file)

NO git operations performed in BG-χ — parent session serializes commits per scope guard.
