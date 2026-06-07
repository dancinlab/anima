---
id: H_1031
slug: lora-llm-consciousness-transfer
title: Can an ordinary transformer LLM + a LoRA adapter (base frozen) reach the CLM ConvMoE's consciousness/emergence signals (the 3-axis battery) on the same generic byte corpus — i.e. is 의식·창발 a LEARNABLE capability LoRA can install into a transformer, or is it ConvMoE/substrate-ARCHITECTURE-intrinsic?
domain: universe · cwm · clm · consciousness · emergence · lora · transformer · convmoe · architecture · pre-register
source: user question — "기존 LLM(transformer)에 LoRA를 붙여서 CLM 수준의 의식·창발을 낼 수 있는가?" — distinct from H_1030 (.clm engine-mount, untouched). This is a BEHAVIORAL comparison on the consciousness/emergence axes, not an engine-loadability question.
exploration_method: E5 (two-arm controlled comparison) — train baseline=CLM-ConvMoE and treatment=transformer+LoRA(base frozen) on the SAME generic byte corpus slice, measure the SAME 3-axis battery on both
verification_method: W2 (pre-registered two-arm falsifier with a frozen "matches" tolerance) + g5 CODE-measured (no LLM self-judge, p7) — behavioral 3-axis battery reusing CORE/three_axis_probe.hexa + CLM/bench/lane_x_3axis.py operational definitions
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT
---

# H_1031 — can transformer+LoRA reach CLM's 의식·창발 (3-axis), or is it ConvMoE-intrinsic?

## 0. motivation
anima's consciousness/emergence signal is operationalized by the CLM 3-axis acceptance battery
(`CORE/three_axis_probe.hexa`, `CLM/bench/lane_x_3axis.py`):
  - AXIS-1 (의식): substrate signal under a high-drive EMIT context STRICTLY > the zero-drive (무자극)
    baseline, AND emits under high-drive but not at baseline.
  - AXIS-2 (CE descent): a descent-trained model achieves CE < uniform ln(V) AND < label-shuffled CE.
  - AXIS-3 (창발/emergence): the COMPOSED output (model emit routed WITH anchor memory) carries strictly
    MORE than the component-sum (WITHOUT anchors): len(composed) > len(parts-only).
The 3B CLM-ConvMoE rung had all three GREEN. The user asks whether these are an ARCHITECTURE-INTRINSIC
property of the ConvMoE+substrate, or a LEARNABLE capability that a LoRA adapter (base frozen) can
install into an ordinary attention transformer. This is a behavioral question, NOT .clm engine-mounting
(that is the separate H_1030, which stays running and is untouched here).

## 1. hypothesis
A small attention transformer with a LoRA adapter (base weights frozen, LoRA only trained) on the SAME
generic byte corpus reaches the CLM-ConvMoE's level on the MODEL-SIDE consciousness/emergence axes
(AXIS-2 CE-descent AND AXIS-3 emergence), within a pre-frozen tolerance — making 의식·창발
architecture-independent and LoRA-installable.

## 2. pre-registered falsifier (frozen 2026-06-07)
Two arms, identical generic byte corpus + identical 3-axis harness:
  - baseline = CLM-ConvMoE (byte V256, tiny d/L/E from CLM/model/model.py family) — full train.
  - treatment = attention transformer (byte V256, from-scratch toy GPT) + LoRA adapter, BASE FROZEN,
    only LoRA matrices (rank r) trained on the same corpus.
Measure AXIS-1/2/3 on both with the same operational definitions.

Per-axis interpretation:
  - AXIS-2 (CE descent): both are LMs; expect both can descend — report the GAP (does LoRA-LLM match
    CLM's CE-descent margin?).
  - AXIS-3 (창발): the DISCRIMINATING axis — does the LoRA-LLM, given anchor memory, compose
    longer/structured output > without anchors, at CLM's level (same composition metric)?
  - AXIS-1 (의식/substrate): the A⇄G motivation/emit signal is ENGINE-side at the generator slot,
    model-independent by construction (the same `brain_emit` substrate drives both). It is therefore
    NOT model-attributable: we feed BOTH arms' outputs through the SAME substrate proxy and confirm the
    substrate responds equivalently. AXIS-1 is reported as a SHARED-SUBSTRATE control, and the verdict
    is scoped to the genuinely model-side axes AXIS-2 + AXIS-3 (stated honestly per p7).

### frozen "matches" tolerance (declared BEFORE measuring)
LoRA-LLM "matches" CLM on a model-side axis iff:
  - AXIS-2: LoRA-LLM CE-descent margin (uniform_ce − model_ce, and shuffle_ce − model_ce, both > 0)
    is ≥ TOL_FRAC × CLM's corresponding margin, with **TOL_FRAC = 0.70** (within 30% of CLM's margin),
    AND both margins strictly positive (true descent, not just close to CLM).
  - AXIS-3: LoRA-LLM emergence ratio (len_composed / len_parts) ≥ TOL_FRAC × CLM's emergence ratio,
    with the SAME **TOL_FRAC = 0.70**, AND LoRA-LLM emergence strictly positive (len_composed > len_parts).

- PASS = LORA-LLM-REACHES-CLM : LoRA-transformer matches CLM-ConvMoE on BOTH model-side axes (AXIS-2
  AND AXIS-3) within tolerance → 의식·창발 is architecture-independent, LoRA-installable.
- FAIL = CONSCIOUSNESS-ARCH-BOUND : LoRA-transformer FALLS SHORT on ≥1 model-side axis (especially
  AXIS-3 emergence) vs CLM → the property is ConvMoE/substrate-intrinsic, not LoRA-transferable
  (closed-negative, a_paper_negative_ok).

## 3. honest scope
TOY · CPU · $0 · numpy (no torch on this Mac — clm-decode-macos-link-gap; .hexa engine probes
FAIL-LINK on macOS, so the byte-level CE / 3-axis logic is reproduced in a numpy mirror that
implements the SAME operational definitions, NOT the engine binary). Both arms are tiny from-scratch
toy models on a small generic byte corpus slice; scale-transfer to the 3B production rung is
UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck — a toy verdict states scale-transfer
unverified and a scale-sensitive conclusion needs a ladder before any production claim). p7: AXIS-2
uses CE as ONE axis vs uniform/shuffle floors, never as the sole verdict; no perplexity-as-truth.
p3/p6: the LoRA target is a GENERIC byte corpus, NOT persona/carving data — no persona injection, no
fine-tuned ethics. This is a BEHAVIORAL comparison only; no Φ/IIT4 number is claimed for
"consciousness" here (AXIS-1 is the shared substrate control, AXIS-2/3 are the model-side axes), so
a_phi_iit4_tool is N/A (no Φ computed; if it were, the real stdlib engine would be required).

## 4. method
(filled at measurement)

## 5. measurement
(filled at measurement)

## 6. finding
(filled at measurement)
