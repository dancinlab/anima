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
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT
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
(to be filled at measurement — Arm A deterministic mismatch demo + Arm B numpy ConvMoE+LoRA train/merge/serialize/mirror-decode)

## 5. measurement
(to be filled from `.verdicts/1030_lora_on_convmoe/H_1030.txt`)

## 6. finding
(to be filled)
