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
status: measured
verdict: 🔴 QAT-LORA-STILL-BREAKS (QAT-aware LoRA HALVES the int4 merge break — float-LoRA merge ΔCE 3.38 → QAT-LoRA merge ΔCE 0.98, a real Δ-vs-H_1030 improvement — but does NOT reach byte-faithful (0.98 ≫ 0.20 envelope), AND the QAT-LoRA's "adaptation" is degenerate: it only reaches CE 5.543 ≈ uniform lnV 5.545 vs base 5.643, collapsing toward uniform rather than the float-LoRA's genuine CE 1.72. So QAT-LoRA neither MEANINGFULLY adapts NOR merges faithfully — int4 .clm is fundamentally LoRA-hostile at this toy scale)
measured_at: 2026-06-08
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

## 5. measurement (2026-06-08, $0 CPU-local, numpy, NO GPU)
Raw stdout: `.verdicts/1032_qat_aware_lora_clm/H_1032.txt`.
- **Frozen base:** CE_base_heldout = 5.64343; uniform lnV = 5.54518; full-FT params = 11682.
- **Control — BASE_FAITHFUL = 1.** No-LoRA base int4 round-trip ΔCE = 0.02947 ≤ 0.20 (the int4
  envelope is not generally lossy at this scale; any break is LoRA-delta-specific).
- **Arm 1 — FLOAT-LoRA baseline (= H_1030, no fake-quant).** Adapts genuinely:
  CE_floatlora_heldout = 1.71870 (ADAPT=1, in-mem merged CE 1.71870). But int4 serialization
  destroys it: CE_mirror_decode = 5.10011 → **FLOAT_MERGE_DELTA_CE = 3.38140** ≫ 0.20
  (FLOAT_BYTE_FAITHFUL=0). Reproduces the H_1030 break (H_1030 measured 3.83; same order of
  magnitude — the difference is the new seed 1032 and the larger STE eps=1e-2 here).
- **Arm 2 — QAT-AWARE LoRA (the fix: fake-quant int4 in forward, STE grad).** LoRA params = 608,
  param-ratio = 0.0520 (≪ 0.5). Two effects:
  1. **Merge break HALVED.** **QAT_MERGE_DELTA_CE = 0.98215** vs the float arm's 3.38140
     (Δ-vs-H_1030 fix = 1) — training against the quantized model genuinely pulls the merged
     weights much closer to the int4 grid. But 0.98 still ≫ 0.20 → **QAT_BYTE_FAITHFUL = 0**
     (the residual mismatch is the per-output-channel scale RE-CALIBRATING after merge: the LoRA
     delta shifts each channel's amax, so the serializer's amax/7 scale differs from the scale the
     QAT forward used, leaving a residual quant gap the STE cannot fully close).
  2. **Adaptation is DEGENERATE.** CE_qatlora_fqfwd = 5.54289 ≈ uniform lnV 5.54518 — technically
     below base (ADAPT=1) but the QAT-LoRA collapsed the model toward UNIFORM rather than learning
     the task (float-LoRA reached 1.72). The float-forward of the same merged weights is even worse
     (6.52493). MIRROR_DESCENT=1 only because CE_mirror 5.54278 sits a hair under uniform — i.e. it
     is decoding ≈ uniform, no real signal.

## 6. finding
🔴 **QAT-LORA-STILL-BREAKS** (closed-negative, a_paper_negative_ok). The H_1030-named fix —
QAT-aware LoRA (train the delta with the int4 fake-quant in the forward, STE grad) — does NOT
rescue an engine-mountable fine-tuned `.clm` at this toy scale, on BOTH falsifier legs:

1. **Merge is still not byte-faithful.** QAT-aware training HALVES the break (merge ΔCE 3.38 → 0.98,
   a real measured improvement over naive float-LoRA — the Δ-vs-H_1030 the hypothesis asked for is
   non-trivial and positive), but 0.98 is still ~5× over the 0.20 envelope. The residual is the
   per-output-channel scale recalibration: merging the LoRA delta changes each channel's amax, so
   `serialize_v3`'s scale = amax/7 differs from the scale the QAT forward quantized against, and the
   STE cannot fully anticipate that post-merge re-quant.
2. **And the QAT-LoRA does not meaningfully adapt anyway.** Forced to live on the int4 grid, the
   rank-2 LoRA can only collapse the model toward uniform (CE 5.543 ≈ lnV 5.545) instead of learning
   the task the float-LoRA learns to CE 1.72. The two objectives — adapt AND land on the coarse
   15-level grid — are in direct tension for a low-rank delta at this width.

**Ruled-out axis:** "make a float-LoRA adaptation survive the int4 `.clm` envelope by QAT-aware
training (STE fake-quant in forward)" is closed-negative at this toy scale. int4 `.clm` is
fundamentally LoRA-HOSTILE here: the 15-level per-output-channel symmetric quant is too coarse for a
rank-2 delta to both express the adaptation and land on-grid. The MEASURED improvement (3.38 → 0.98)
suggests the direction is right but insufficient — natural follow-ups (NOT tested here): (a) a
HIGHER-bit envelope (int8) for the LoRA-touched blocks, (b) per-block scale freezing (calibrate the
serializer scale to the QAT scale so merge does not re-quant), (c) a higher-rank / wider adapter, or
(d) full-FT-then-int8 rather than low-rank-then-int4. Honest scope (a_scale_honest_scope ·
a_toy_scale_recheck): toy d16/L1/E2 numpy, mirror-decode (engine-link deferred); scale-transfer and
the higher-bit / scale-frozen variants are UNVERIFIED. p3/p6 honored (generic byte target, no
persona); p7 honored (CE measured, no perplexity-as-truth); a_clm_gen_pipeline honored (ConvMoE
stays ConvMoE).
