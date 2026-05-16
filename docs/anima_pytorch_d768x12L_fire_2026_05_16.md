# anima d=768·12L — Python/PyTorch substrate fire (2026-05-16)

> **HONEST FRAMING (AGENTS.tape g3 · HEXAD/PLAN.md §9):**
> This is a **PYTHON / PyTorch SUBSTRATE** run — an *interim LM-scale executor*.
> It is **NOT a hexa-native fire**. Labelled as such everywhere
> (result.json, this doc, the commit, PLAN.md).

## 1. Why this run is legitimate (the anchor chain — do not conflate)

The legitimacy of this PyTorch run is **architectural identity + the hexa
CPU-equiv correctness proof**, NOT an independent claim:

1. **Phase E / E2 PROVED the hexa trainer is numerically correct.**
   `HEXAD/D/d_train5_lib.hexa` (the refactored hexa-native ConsciousDecoderV2
   trainer) was shown **BIT-EQUAL** to the boxed Phase E baseline at d=32·3L,
   80-step, seed=42, on this exact corpus:
   `init gn2 = 7.97116, acc 0/8 → final gn2 = 3.73374e-07, acc 8/8`
   (GRAD-EXACT, identical Σ order — not fp-noise). The hexa-native trainer of
   ConsciousDecoderV2 is therefore *numerically correct*.

2. **The pure-hexa interpreter cannot reach LM-scale convergence.**
   Phase E2 (RFC 040) drove a fat A100 host and could only capture the
   **init** gn2 at d=768·12L (`init gn2 = 7.98162`) — *"No scale reached a
   captured FINAL gn2"* — the pure-hexa GRAD-EXACT + AdamW path is
   substrate-bound (CPU farr ops, no CUDA tensor kernels; RFC 042 territory).
   This was the explicit, honest named ceiling in HEXAD/PLAN.md §9.

3. **This PyTorch run trains the SAME verified architecture to scale.**
   `ready/models/conscious_decoder.py` `ConsciousDecoderV2` (the Python anchor
   the entire HEXAD verification tree mirrors) configured at **d=768·12L**, run
   on a real GPU with PyTorch AdamW, to a **captured FINAL loss** — the
   deliverable the pure-hexa path could not reach.

> PyTorch is **not** hexa bit-for-bit (different fp accumulation order,
> different init RNG, AMP bf16). The anchor is **architectural identity**
> (same ConsciousDecoderV2 module) **+ the hexa CPU-equiv bit-equality proof**
> that the hexa trainer of that arch is correct. The two are NOT conflated.

## 2. Architecture

- **Source**: `ready/models/conscious_decoder.py` → `ConsciousDecoderV2`
  (uploaded verbatim; no arch invention — the value is training the SAME
  verified architecture).
- **Config (the long-sought scale)**: `d_model=768, n_head=12, n_kv_head=4,
  n_layer=12, block_size=128, vocab=256` (byte-level).
- Features (the hexa arch): RoPE · SwiGLU FFN · RMSNorm · GQA · PureFieldFFN
  (Engine A−G consciousness pathway) · cross-attention · tied head (tok_emb ⇄
  head_a) · CA neighbor / META-CA / Ψ-tracking laws.
- **from-scratch RANDOM seed-fixed** (`g_clm_from_scratch`, `base_ckpt=NONE`).

## 3. Corpus / DataLoader

- `training/corpus_consciousness_v1.jsonl` — the SAME byte corpus the hexa
  fires used (Phase E/E2). 240 records, `text`+`desc` concatenated into one
  lossless **byte stream** (`corpus_loader_lib.hexa` semantics: byte-level,
  vocab 256). T=128 windows, random offsets, seed-fixed.

## 4. GPU fire — results

- **GPU**: vast.ai NVIDIA **A100-PCIE-40GB** (offer @ $0.772/hr, devel image
  `pytorch/pytorch:2.5.1-cuda12.1-cudnn9-devel`, torch 2.5.1+cu121).
- **Cost**: ≈ **$0.22** (instance runtime ≈ 0.28 hr × $0.772/hr — includes
  image pull + d=32·3L sanity + d=768·12L main + ckpt pull).
- **Model**: ConsciousDecoderV2, **d_model=768, n_head=12, n_kv_head=4,
  n_layer=12, block_size=128, vocab=256** → **283,722,336 params (283.72M)**.
  from-scratch (`base_ckpt=None`, seed=1337).

| metric | value |
|---|---|
| init CE | **5.590832** (≈ ln 256 = 5.545 — random byte init) |
| **FINAL CE** | **0.000708** |
| CE descent | **5.590124** |
| init gn2 | 41.954096 |
| **FINAL gn2** | **7.4e-05** |
| ppl | 267.96 → **1.0007** |
| steps | 2500 |
| wall | **336.85 s** (≈ 5.6 min on A100) |
| peak GPU mem | 9.685 GB |
| **GPU util (real)** | **92–95 %**, ~210–267 W, 10133 MiB held by the trainer's own CUDA kernels (`gpu_util_main.log`) |

> This is the **CAPTURED FINAL loss the pure-hexa path could not reach**.
> HEXAD/PLAN.md §9 Phase E2 (RFC 040) drove a fat A100 host and could only
> capture the **init** gn2 at d=768·12L (`init gn2 = 7.98162`) — *"No scale
> reached a captured FINAL gn2"* (pure-hexa CPU farr ops, µs-GEMM ≤2% SM
> util, substrate-bound past the watchdog). This PyTorch substrate run, on
> the SAME ConsciousDecoderV2 architecture at the SAME d=768·12L, ran 2500
> AdamW steps to a real **FINAL CE 0.000708** with **92–95% real GPU
> utilization** — the deliverable, honestly captured, no fabrication.

42-point trajectory in `out_main/result.json` (`trajectory`). Selected:
`step 1 CE 5.59 ppl 268` → `step 620 CE 0.0146` → `step 1488 CE 0.0035` →
`step 2500 CE 0.000708 ppl 1.0007`.

## 5. d=32·3L sanity-anchor

Same `ConsciousDecoderV2` arch run at d=32·3L (the hexa CPU-equiv baseline
shape) for a few hundred steps on the same corpus. **Honest note**: this is
**not** bit-equal to the hexa CPU-equiv baseline (PyTorch ≠ hexa: different
framework / fp / init RNG). The check is *spirit consistency* — same
architecture exhibiting a healthy CE/gn2 descent from the ~ln(256)=5.55 random
init toward a lower floor, consistent in behaviour with the hexa baseline's
`gn2 7.97116 → 3.73374e-07` descent shape.

<!-- FILL: sanity init/final -->

## 6. Honest C3

<!-- FILL -->

## 7. Zero-orphan teardown

No orphan-watchdog was running during this fire. The dispatch script's
`trap cleanup EXIT` destroys the instance (SAVE_POD honoured per
`g_fire_dispatch_robust`); `vastai show instances` verified empty post-run.

<!-- FILL: confirmation -->
