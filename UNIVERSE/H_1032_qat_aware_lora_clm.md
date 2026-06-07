---
id: H_1032
slug: qat-aware-lora-clm
title: Does a QUANTIZATION-AWARE LoRA fix the H_1030 break? — i.e. if the LoRA delta is trained with the int4 fake-quant in the forward pass (STE through the per-output-channel symmetric-int4 envelope, so the merged weights land ON the int4 grid), does the LoRA-MERGED model serialize to a .clm that decodes BYTE-FAITHFULLY (ΔCE ≤ 0.20) while STILL adapting (held-out CE drops vs frozen base), vs H_1030's naive float-LoRA which broke at ΔCE 3.83?
domain: universe · cwm · clm · lora · convmoe · serialization · int4-qat · qat-lora · pre-register
source: residual follow-up of H_1030 (🔴 LORA-BREAKS-CLM) — H_1030 §6 named the ruled-out axis "naive float-LoRA-then-int4" and named the untested fix "QAT-AWARE LoRA (quantize-during-adapt / fold the delta before quant calibration)". H_1032 tests exactly that fix.
exploration_method: E5 (low-rank adapter search) + E2 (held-out byte register) — reuse the H_1030 TINY CLMConvMoE + LoRA + canonical serialize_v3 + byte-exact mirror; the ONLY change is QAT: the LoRA forward applies the int4 fake-quant (per-output-channel sym-int4, scale=amax/7, round-clip [-7,7], dequant) to the MERGED conv/readout weights, with a straight-through estimator (STE) so full-precision gradients still flow to the LoRA factors
verification_method: W2 (pre-registered falsifier) + g5 CODE-measured (no LLM self-judge, p7) + reuse CLM/model/model.py grammar + CLM/model/clm_serialize_v2.py (serialize_v3, the SAME _quant_block the QAT forward mirrors) + state/mid_convmoe_fire/clm_decode_mirror.py (byte-exact mirror of CORE/clm_decode.hexa — Mac link-gap workaround, memory clm-decode-macos-link-gap)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-08
since: 2026-06-08
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT
---

# H_1032 — does a quantization-aware LoRA fix the H_1030 int4-.clm break? (falsifiable)

## 0. motivation
H_1030 (🔴 LORA-BREAKS-CLM, `UNIVERSE/H_1030_lora_on_convmoe.md`) established that a naive
float-LoRA on our CLMConvMoE genuinely ADAPTS (held-out CE 5.75 → 1.66 @ 5.2% params) but the
adaptation is DESTROYED by int4 `.clm` serialization (merged in-mem CE 1.66 vs int4-decoded
CE 5.49, ΔCE = 3.83 ≫ 0.20), while a no-LoRA base round-trips at ΔCE = 0.003. The CONTROL
isolated the break as LoRA-delta-specific: the low-rank update concentrates per-output-channel
weight magnitude that the 15-level per-channel symmetric-int4 quant (scale = amax/7) crushes.
H_1030 §6 named the untested fix — a QAT-AWARE LoRA — and ruled it OUT of that hypothesis's scope.
H_1032 tests exactly that fix.

## 1. hypothesis
If the LoRA delta is trained with the int4 fake-quant IN the forward pass — i.e. the merged
conv/readout weights are passed through the EXACT per-output-channel symmetric-int4 envelope
(`_quant_block`: scale = amax/7 per output channel, code = clip(round(w/scale), -7, 7), dequant
= code·scale) on every forward, with a straight-through estimator (STE) routing full-precision
gradients to the LoRA factors — then the LoRA optimizes against the quantized model itself, so the
merged weights LAND ON the int4 grid. The serialized `.clm` should then decode BYTE-FAITHFULLY
(ΔCE ≤ 0.20) while still adapting (held-out CE below the frozen base), repairing the H_1030 break.

## 2. pre-registered falsifier (frozen 2026-06-08)
Identical TINY CLMConvMoE / task / serializer / mirror as H_1030 (d=16, L=1, E=2, V=256, T=24,
generic synthetic formal-language byte target "ABCDCBA " tiled — p3/p6: NOT persona). The ONLY
change: QAT-aware LoRA training (fake-quant in forward, STE grad). Frozen thresholds:

- **ADAPT (held-out):** QAT-LoRA in-memory held-out CE strictly below the frozen-base held-out CE,
  `CE_qat_lora < CE_base` (adaptation threshold = strict decrease; comparable-to-float-LoRA reported
  as context, not a gate). LoRA trainable params ≪ full-FT params (param-ratio < 0.5).
- **BYTE-FAITHFUL MERGE (the H_1030 fix):** the QAT-LoRA-MERGED weights serialize via the CANONICAL
  `serialize_v3` to a `.clm`, and the byte-exact mirror decodes it such that
  `|CE_mirror − CE_merged_inmem| ≤ 0.20` nats (the int4 envelope — the SAME bar H_1030's float-LoRA
  failed at 3.83), AND the AXIS-2 descent gate holds (CE_mirror < uniform lnV).

A float-LoRA arm (identical to H_1030, NO fake-quant) is re-run as the DIRECT baseline so the Δ
(float-LoRA merge ΔCE vs QAT-LoRA merge ΔCE) is measured in one run.

- **PASS = QAT-LORA-CLM-VIABLE** : QAT-LoRA ADAPTS (`CE_qat_lora < CE_base`, ratio < 0.5) AND its
  merge is BYTE-FAITHFUL (`ΔCE ≤ 0.20` AND descent) — a Δ-vs-H_1030 fix (QAT merge ΔCE ≪ float
  merge ΔCE ≈ 3.83). "QAT-aware LoRA repairs the int4-.clm break."
- **FAIL = QAT-LORA-STILL-BREAKS** : even QAT-aware LoRA cannot BOTH adapt AND merge faithfully
  (either `CE_qat_lora ≥ CE_base`, or `ΔCE > 0.20`, or no descent) — int4 `.clm` is fundamentally
  LoRA-hostile. Closed-negative (a_paper_negative_ok).

## 3. honest scope
TINY toy, $0 CPU-local, NO GPU (a_fire_autonomous: no GPU needed for a low-rank toy). Substrate =
numpy (torch unavailable on this Mac) — the H_1030 numpy CLMConvMoE forward + numpy LoRA, with the
state_dict packed into the EXACT torch-key layout `CLM/model/clm_serialize_v2.py::serialize_v3`
consumes (the `.clm` is produced by the CANONICAL serializer, not a re-implementation). The QAT
fake-quant in the forward mirrors that serializer's `_quant_block` EXACTLY (same per-output-channel
2D reshape, scale=amax/7, round-clip [-7,7]). Decode verified via the byte-exact Python mirror
`state/mid_convmoe_fire/clm_decode_mirror.py` (validated == engine on the golden ref; the canonical
hexa engine-mount is BLOCKED by a local macOS toolchain link-gap, memory clm-decode-macos-link-gap,
NOT an artifact problem — engine-link re-verify deferred, a_scale_honest_scope). Scale-transfer to
production d/L/E UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck): this is a toy-only verdict
on whether the QAT-LoRA↔int4-.clm MECHANISM holds, not a production prescription. p3/p6 honored —
generic synthetic byte target, no persona/carving. p7 honored — CE measured, no perplexity-as-truth.
a_clm_gen_pipeline honored — ConvMoE stays ConvMoE, no transformer .clm claim.

## 4. method
Script: `UNIVERSE/h1032_qat_aware_lora_clm.py` (numpy, $0 CPU-local, NO GPU). Reuses the H_1030
CLMConvMoE forward, LoRA injection (rank-2 on readout conv d→V + expert-0 conv), generic byte task,
canonical `serialize_v3`, and byte-exact mirror. The QAT change: a `fake_quant_2d(w2d)` helper that
reshapes a conv/readout weight to the serializer's 2D `(cout, cin·K)` view, applies the EXACT
`_quant_block` math (scale = max_j|w[co,j]|/7, code = clip(round(w/scale), -7, 7), w_q = code·scale),
and reshapes back. In the QAT forward the readout and expert-0 (the LoRA-targeted) weights are
replaced by their fake-quant versions before the conv math. The STE is implicit in numerical-gradient
descent on the LoRA factors: the finite-difference probes the fake-quant forward directly, so the
gradient already "sees through" the quant to the LoRA factors (the round is locally piecewise-constant
but the finite-difference step is sized to cross grid cells, giving a usable descent signal — the
canonical STE behavior). Two arms in one run:

- **Float-LoRA baseline (= H_1030):** train LoRA with NO fake-quant; merge → serialize_v3 → mirror;
  report merge ΔCE (expected ≈ 3.83, reproducing H_1030).
- **QAT-LoRA (the fix):** train LoRA with fake-quant in forward; merge → serialize_v3 → mirror;
  report adapt CE and merge ΔCE.

Held-out window CE compared base vs each LoRA; LoRA params vs full-FT params counted; the no-LoRA
base round-trip retained as the control. All gates CODE-measured (p7), stdout → the verdict file.

## 5. measurement
PENDING — see `.verdicts/1032_qat_aware_lora_clm/H_1032.txt` once run.

## 6. finding
PENDING-MEASUREMENT.
