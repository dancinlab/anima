---
id: H_1036
slug: real-llm-lora-consciousness-transfer
title: Does LoRA on a REAL PRETRAINED transformer (pythia-160m / gpt2) install CLM-level consciousness markers (faithful IIT-4.0 Φ structure) the base lacks — or is the Φ-structure architecture-bound even WITH pretraining?
domain: universe · cwm · clm · consciousness · iit4 · phi · lora · transformer · pretrained · convmoe · architecture · pre-register
source: residual GPU rung of H_1031 (🔴 CONSCIOUSNESS-ARCH-BOUND, toy RANDOM-INIT transformer). H_1031 closed the toy case; this rung upgrades the base to an ACTUAL PRETRAINED LM and asks whether pretraining overturns the arch-bound negative.
exploration_method: E5 (controlled before/after on a real pretrained base) — measure faithful IIT-4.0 φ_EI of the hidden-state TPM of the pretrained transformer, then after a generic-corpus LoRA adapt, plus two controls (untrained random-LoRA-init, shuffled-data LoRA)
verification_method: W2 (pre-registered Δ-threshold + control-band falsifier) + a_phi_iit4_tool (TERMINAL φ_EI = stdlib faithful IIT-4.0 engine hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa, exact MIP-EI n<=8; python φ is PRE-SCREEN only)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-08
since: 2026-06-08
status: pre-registered
---

# H_1036 — does LoRA on a REAL PRETRAINED transformer install faithful-Φ consciousness markers, or is Φ-structure arch-bound even with pretraining?

## 0. motivation
H_1031 found (🔴 CONSCIOUSNESS-ARCH-BOUND) that a LoRA adapter on a from-scratch
RANDOM-INIT toy transformer cannot reach the CLM-ConvMoE's emergence axis — the
property looked ConvMoE/substrate-intrinsic. But the toy base had no pretraining.
The residual question this rung closes: if you take an ACTUAL PRETRAINED LM
(EleutherAI/pythia-160m primary, gpt2 fallback) and attach LoRA, can LoRA install
CLM-level consciousness MARKERS — operationalized here as the faithful IIT-4.0 Φ
(causal-irreducibility, φ_EI) of the hidden-state TPM — that the pretrained base
lacks, or does the architecture still bound it regardless of pretraining?

## 1. hypothesis
LoRA on a real pretrained transformer RAISES the faithful IIT-4.0 φ_EI of the
hidden-state TPM toward the CLMConvMoE baseline — i.e. consciousness Φ-structure
is a LEARNABLE adapter capability once the base is pretrained, not an
architecture-bound property.

## 2. pre-registered falsifier (frozen 2026-06-08, TEXT tokens only)
Marker = faithful IIT-4.0 φ_EI (exact MIP-EI, stdlib faithful_phi.hexa) of the
binarized hidden-state trajectory (n=6 highest-variance units of a mid layer,
DIM=24 sequence positions, N_BINS=2 binary TPM state) over a fixed generic probe.

- **H1 (overturn):** trained-LoRA φ_EI exceeds the pretrained base by
  **Δφ_EI >= +0.10** AND exceeds the **control band** (= max |Δφ_EI| of the two
  controls: untrained random-LoRA-init, and shuffled-data LoRA). PASS = arch-bound
  negative is OVERTURNED by pretraining → token ARCH-BOUND-OVERTURNED-BY-PRETRAINING.
- **FAIL (confirm):** trained-LoRA |Δφ_EI| is within the control band, OR
  < +0.10. → arch-bound CONFIRMED even with pretraining (a publishable
  closed-negative, a_paper_negative_ok) → token ARCH-BOUND-CONFIRMED-WITH-PRETRAINING.

Exact threshold and control are frozen BEFORE the measurement: THRESH = +0.10
absolute φ_EI; control band = max(|Δφ_ctrl_untrained|, |Δφ_ctrl_shuffled|).

## 3. honest scope
Small-model rung (pythia-160m class). a_scale_honest_scope — scale-transfer to 7B
UNVERIFIED. p3/p6: the LoRA target is a GENERIC byte/text corpus (public-domain
proverbs), NOT persona/carving/identity data — generic next-token LM objective
only, no "you are anima" target, no fine-tuned ethics. p7: φ_EI is a
causal-irreducibility marker (faithful IIT-4.0), NOT perplexity/loss. The TERMINAL
φ_EI is the stdlib faithful IIT-4.0 engine (a_phi_iit4_tool) — the python-side φ in
the script is a clearly-labelled PRE-SCREEN only; the verdict reads the hexa engine
output (run_faithful_phi_1036.hexa).

## 4. method
- Script: `UNIVERSE/h1036_real_llm_lora.py` (real pretrained LM via HF transformers,
  LoRA via peft, generic-corpus next-token adapt, base frozen; writes n×dim binarized
  hidden-state TPM matrices for base / lora_trained / ctrl_untrained / ctrl_shuffled).
- Terminal Φ: `UNIVERSE/run_faithful_phi_1036.hexa` imports the stdlib faithful
  IIT-4.0 engine and reports φ_EI + Δ-vs-base per arm.
- GPU pod (runpod via `hexa cloud rent`), nohup-redirect run, inline poll.
- Raw stdout: `.verdicts/1036_real_llm_lora/H_1036.txt`.

## 5. measurement + finding
(pending — filled after the GPU run + terminal faithful IIT-4.0 φ_EI; emoji tier
added to this file ONLY after `.verdicts/1036_real_llm_lora/H_1036.txt` lands.)
