---
id: H_1030
slug: lora-on-convmoe
title: Can we LoRA an existing LLM to our CLM standard? — i.e. is a low-rank LoRA adapter (a) able to ADAPT our CLMConvMoE on a generic held-out byte task using params ≪ full-FT AND (b) does the LoRA-MERGED model still serialize to a v0.2/v0.3 .clm that decodes BYTE-FAITHFULLY under the int4-QAT envelope — whereas a LoRA'd foundation transformer can NEVER produce an engine-mountable .clm (architectural hard block)?
domain: universe · cwm · clm · lora · convmoe · serialization · int4-qat · pre-register
source: user question "can we LoRA an existing LLM to our CLM standard?" — domain mapping (CLM = CLMConvMoE, dilated causal conv + MoE, byte V256, NO attention, int4 envelope; .clm v0.2/v0.3 byte-layout is ConvMoE-specific; CORE/clm_decode.hexa only decodes ConvMoE) already established; governance a_clm_gen_pipeline DONT "serialize a non-ConvMoE (ByteGPT/transformer) and claim engine-mountable" + philosophy p3/p6 (LoRA on persona = de-facto injection, FORBIDDEN) frame the falsifier
exploration_method: E5 (low-rank adapter search) + E2 (held-out byte register) — build a TINY CLMConvMoE (small d/L/E, byte V256), inject a low-rank LoRA on its conv layers, adapt on a GENERIC byte task (synthetic formal-language slice, NOT anima persona — p3/p6), then merge + serialize_v3 + mirror-decode
verification_method: W2 (two-arm pre-registered falsifier) + g5 CODE-measured (no LLM self-judge, p7) + reuse CLM/model/model.py grammar + CLM/model/clm_serialize_v2.py (serialize_v3) + state/mid_convmoe_fire/clm_decode_mirror.py (byte-exact Python mirror of CORE/clm_decode.hexa — Mac link-gap workaround, memory clm-decode-macos-link-gap)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
verdict: 🔴 LORA-BREAKS-CLM (Arm A foundation→.clm BLOCKED ✓; Arm B1 LoRA ADAPTS ConvMoE ✓ CE 5.75→1.66 @ 5.2% params; Arm B2 FAILS — int4-.clm envelope cannot absorb the LoRA low-rank delta: merged in-mem CE 1.66 vs int4-decoded CE 5.49, ΔCE=3.83 ≫ 0.20, while a no-LoRA base round-trips at ΔCE=0.003 → break is LoRA-delta-specific)
measured_at: 2026-06-07
---

# H_1030 — can we LoRA an existing LLM to our CLM standard? (two-arm falsifiable)

## 0. motivation
The user asks whether an existing LLM can be LoRA'd "to our CLM standard". The domain mapping
(already established, NOT re-derived here) makes this two sharply distinct questions:

1. **Foundation transformer + LoRA → engine-mount?** The `.clm` v0.2/v0.3 byte-layout is
   ConvMoE-specific (CORE/clm_decode.hexa parses ecW · tcW · expert-conv · router-conv ·
   readout-conv blocks + GroupNorm/MoE-softmax ext arrays). A foundation transformer's parameter
   structure (attention QKV / FFN, no conv-block / router / expert / readout-conv) cannot populate
   that grammar. Governance a_clm_gen_pipeline DONT: "serialize a non-ConvMoE (ByteGPT/transformer)
   and claim engine-mountable" — an architectural hard block, regardless of LoRA.
2. **Our CLMConvMoE + LoRA → engine-mount?** This is the architecture-LEGAL path and the OPEN
   question: does a low-rank adapter actually adapt the conv-native model, and does the merged
   model survive the int4-QAT `.clm` envelope byte-faithfully?

p3 (NO PERSONA INJECTION) / p6 (NO FINE-TUNED ETHICS): a LoRA on persona/carving data is de-facto
persona injection → FORBIDDEN. The fine-tune target here is therefore a GENERIC synthetic byte task
(a deterministic formal-language slice), NOT anima persona.

## 1. hypothesis
LoRA is viable IN the CLM stack but ONLY on our arch: a low-rank LoRA adapter on CLMConvMoE both
(B1) ADAPTS the model — val-CE on a generic held-out target byte-task drops vs the frozen base,
using LoRA params ≪ full-FT params — AND (B2) the LoRA-MERGED weights still serialize to a
v0.2/v0.3 `.clm` that decodes BYTE-FAITHFULLY (the int4-QAT envelope absorbs the low-rank delta);
WHILE a foundation transformer's structure (Arm A) cannot map into the `.clm` ConvMoE grammar at all.

## 2. pre-registered falsifier (frozen 2026-06-07)
**Arm A (deterministic block-mismatch demo — the BLOCKED foundation path):** take a tiny transformer's
weight shapes (attention QKV + FFN; no conv/router/expert/readout-conv structure) and feed them to the
`.clm` serializer / role-map (serialize_v3 expects torch keys embed_conv.conv.weight ·
trunk.{i}.conv.conv.weight · moe.experts.{j}.conv.conv.weight · moe.router.weight · readout.weight).
PASS-A = the serializer / decoder CANNOT map the transformer (missing-block / role KeyError /
header-count mismatch) — "LoRA-on-foundation → engine-mount is BLOCKED" is the measured form.

**Arm B (the real LoRA test, $0 CPU toy — the OPEN question):**
- B1 (adapts): LoRA-adapted val-CE on the generic held-out target byte-task is BELOW the frozen-base
  val-CE on the same task (CE_lora < CE_base), with LoRA trainable params ≪ full-FT params
  (param-ratio < 0.5 reported; expect ≪ that).
- B2 (merges byte-faithful): the LoRA-MERGED model serializes via serialize_v3 to a valid `.clm`, and
  the byte-exact mirror (clm_decode_mirror.py) DECODES it — re-deriving the float32 weights from the
  serialized int4 nibbles + scales and computing CE on a fixed window — such that the mirror-decoded
  CE matches the in-memory merged-model CE within the int4-quant tolerance (|ΔCE| ≤ 0.20 nats, the
  documented int4-QAT envelope), AND the standard AXIS-2 descent gate holds (mirror CE < uniform lnV).

- **PASS = LORA-VIABLE-ON-CONVMOE** : Arm B1 AND Arm B2 both hold (LoRA adapts ConvMoE AND merges to
  an engine-mountable byte-faithful `.clm`), with Arm A confirming the foundation path is BLOCKED →
  "LoRA in the CLM stack works, on our arch, not on a foundation transformer".
- **FAIL = LORA-BREAKS-CLM** : LoRA on ConvMoE either fails to adapt (CE_lora ≥ CE_base) OR the merged
  weights break the int4/.clm byte-faithfulness (|ΔCE| > 0.20 OR mirror NO-DESCENT) — the QAT envelope
  cannot absorb the low-rank delta. Closed-negative (a_paper_negative_ok).

## 3. honest scope
TINY toy, $0 CPU-local, NO GPU (a_fire_autonomous: no GPU needed for a low-rank toy). Substrate =
numpy (torch unavailable on this Mac) — a minimal numpy CLMConvMoE forward + numpy LoRA, with the
state_dict packed into the EXACT torch-key layout CLM/model/clm_serialize_v2.py::serialize_v3 consumes
(so the .clm is produced by the CANONICAL serializer, not a re-implementation). Decode verified via the
byte-exact Python mirror state/mid_convmoe_fire/clm_decode_mirror.py (validated == engine on the golden
ref; the canonical hexa engine-mount is BLOCKED by a local macOS toolchain link-gap, memory
clm-decode-macos-link-gap, NOT an artifact problem — engine-link re-verify deferred, a_scale_honest_scope).
Scale-transfer to production d/L/E UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck): this is a
toy-only verdict on whether the LoRA↔int4-.clm MECHANISM holds, not a production prescription. p3/p6
honored — generic synthetic byte target, no persona/carving data. p7 honored — CE measured, no
perplexity-as-truth. a_clm_gen_pipeline honored — ConvMoE-only serialize, no transformer .clm claim.

## 4. method
Script: `UNIVERSE/h1030_lora_on_convmoe.py` (numpy, $0 CPU-local, NO GPU). torch is
unavailable on this Mac, so a minimal numpy CLMConvMoE forward re-implements the SAME
conv-native math as `CLM/model/model.py` / `CORE/clm_decode.hexa` (causal dilated conv,
GroupNorm(1,d)+GELU residual trunk, router conv, E expert conv+GELU, softmax MoE mix,
output GroupNorm, readout conv; tiny d=16/L=1/E=2, byte V=256, T=24). Weights are held in
the EXACT torch-key layout the CANONICAL serializer `CLM/model/clm_serialize_v2.py`
consumes, so the `.clm` is produced by `serialize_v3` itself (not a re-implementation), and
decode is verified by the byte-exact mirror `state/mid_convmoe_fire/clm_decode_mirror.py`
(memory clm-decode-macos-link-gap; hexa engine-mount BLOCKED by a local macOS toolchain
link-gap, NOT an artifact problem — engine-link re-verify deferred, a_scale_honest_scope).

- **Arm A (deterministic):** a tiny foundation-transformer state_dict (tok_emb, attention
  qkv/proj, FFN fc1/fc2, ln, lm_head — NO conv/router/expert/readout-conv) is fed to
  `serialize_v3`. The serializer's role-map requires conv keys; a missing block raises.
- **Arm B1 (adapts):** base CLMConvMoE frozen at random init; a rank-2 LoRA (A·B factors)
  injected on the readout conv (d→V) + expert-0 conv. Only the LoRA factors train, by
  numerical-gradient descent over a small fixed window set of a GENERIC synthetic
  formal-language byte stream ("ABCDCBA " motif tiled — p3/p6: NOT persona/carving). Held-out
  window CE compared base vs LoRA; LoRA params vs full-FT params counted.
- **Control:** the no-LoRA BASE is serialized + mirror-decoded to isolate whether any Arm B2
  break is LoRA-delta-specific or generic int4 loss.
- **Arm B2 (merges byte-faithful):** LoRA merged into base weights → `serialize_v3` →
  byte-exact mirror decode; |CE_mirror − CE_merged_inmem| vs the 0.20-nat int4 envelope, and
  the AXIS-2 descent gate (CE_mirror < uniform lnV).

## 5. measurement (2026-06-07, $0 CPU-local, numpy, NO GPU)
Raw stdout: `.verdicts/1030_lora_on_convmoe/H_1030.txt`.
- **Arm A — ARM_A_BLOCKED = 1.** `serialize_v3` on the transformer state_dict raises
  `KeyError: missing weight for slot 'ecW' (tried torch key 'embed_conv.conv.weight')` — the
  `.clm` ConvMoE grammar cannot be populated by attention/FFN parameters. The
  "LoRA-on-foundation → engine-mount is BLOCKED" claim is measured, consistent with
  a_clm_gen_pipeline.
- **Arm B1 — PASS.** CE_base_heldout = 5.74688 → CE_lora_heldout = 1.65926 (CE_DROPPED=1).
  LoRA params = 608 vs full-FT params = 11682 → param-ratio = 0.0520 (≪ 0.5). LoRA genuinely
  ADAPTS the conv-native ConvMoE with ~5% of the parameters.
- **Control — BASE_FAITHFUL = 1.** No-LoRA base: in-mem CE 5.74688 vs int4-mirror CE 5.75013,
  ΔCE_base = 0.00325 ≪ 0.20. The int4-.clm envelope is NOT generally lossy at this scale.
- **Arm B2 — FAIL.** Merged in-mem CE = 1.65926 but int4-decoded mirror CE = 5.48810,
  ΔCE = 3.82885 ≫ 0.20 (BYTE_FAITHFUL=0). The adaptation is destroyed by serialization. (The
  mirror CE 5.488 sits just under uniform lnV=5.545, MIRROR_DESCENT=1, but the LoRA gain is
  gone.)

## 6. finding
🔴 **LORA-BREAKS-CLM** (closed-negative, a_paper_negative_ok). Answer to "can we LoRA an
existing LLM to our CLM standard?" — **No, not end-to-end, on two independent grounds:**
1. A foundation transformer can NEVER become an engine-mountable `.clm` (Arm A, deterministic
   architectural hard block — the `.clm` grammar is ConvMoE-specific).
2. Even on the architecture-LEGAL path (LoRA on OUR CLMConvMoE), LoRA DOES adapt the model
   (Arm B1 ✓, 5.2% params) but the int4-QAT `.clm` envelope CANNOT absorb the merged low-rank
   delta (Arm B2 ✗): the merged model loses essentially all its adaptation through int4
   serialization (ΔCE 3.83). The CONTROL is decisive — the same int4 path preserves the
   no-LoRA base at ΔCE 0.003, so the break is SPECIFICALLY the LoRA delta, not generic
   quantization loss. The low-rank update concentrates per-output-channel weight magnitude
   that the 15-level symmetric-int4 per-channel quant (scale = amax/7) crushes.

**Ruled-out axis:** "merge a float LoRA adapter into the int4-.clm envelope and keep the
adaptation" is closed-negative at this toy scale — naive float-LoRA-then-int4 is NOT a viable
path to a fine-tuned engine-mountable `.clm`. A viable path would require QAT-AWARE LoRA
(quantize-during-adapt / fold the delta before quant calibration), which this hypothesis did
NOT test. Honest scope (a_scale_honest_scope · a_toy_scale_recheck): toy d16/L1/E2 numpy,
mirror-decode (engine-link deferred); scale-transfer to production d/L/E and a QAT-aware LoRA
variant are UNVERIFIED and are the natural follow-ups.
