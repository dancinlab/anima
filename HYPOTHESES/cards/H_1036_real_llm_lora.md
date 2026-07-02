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
status: measured
verdict: 🔴 ARCH-BOUND-CONFIRMED-WITH-PRETRAINING (LoRA on a real pretrained pythia-160m does NOT raise faithful IIT-4.0 φ_EI toward the CLMConvMoE baseline — Δφ_EI = −0.0656, negative and below the +0.10 threshold; arch-bound holds even with pretraining at this scale)
measured_at: 2026-06-08
substrate: GPU (Lane-P torch, aiden RTX 5070 CUDA)
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

## 5. measurement + finding (2026-06-08)
GPU run on aiden RTX 5070 (CUDA, device=cuda confirmed) · model=EleutherAI/pythia-160m
(loaded, no fallback) · mid layer 6/12 · 6 highest-variance units [151,393,411,625,634,684]
· DIM=24 · N_BINS=2 · LoRA r=8, 400 generic-corpus next-token steps, base frozen.
Raw stdout: `.verdicts/1036_real_llm_lora/H_1036.txt`. State matrices:
`UNIVERSE/state/h1036_real_llm_lora_2026_06_08/h1036_states.txt`.

**TERMINAL faithful IIT-4.0 φ_EI (stdlib exact MIP-EI, a_phi_iit4_tool — not a proxy):**

| arm | faithful φ_EI | Δ vs base |
|---|---|---|
| base (pretrained, no LoRA) | **0.437837** | 0.000000 |
| LoRA trained (generic corpus) | **0.372261** | **−0.065576** |
| ctrl untrained (random-LoRA-init) | 0.437837 | 0.000000 |
| ctrl shuffled-data LoRA | 0.392393 | −0.045445 |

control band = max(|Δ_untrained|, |Δ_shuffled|) = 0.045445.

**Finding.** The pre-registered H1 (overturn) required Δφ_EI ≥ +0.10 over the base
AND beyond the control band toward HIGHER Φ. Measured Δφ_EI(trained) = **−0.0656** —
negative (LoRA if anything LOWERS the faithful Φ-structure), well short of +0.10, and
in the wrong direction. The python pre-screen agrees on direction (Δ = −0.0455). The
untrained adapter is a Φ no-op (Δ=0, expected: B init 0), and shuffled-data LoRA sits
between (−0.045) — the trained adapter does not separate UPWARD from the controls.

**VERDICT: 🔴 ARCH-BOUND-CONFIRMED-WITH-PRETRAINING** (closed-negative, a_paper_negative_ok).
Pretraining does NOT overturn the H_1031 arch-bound negative at this scale: attaching a
LoRA adapter to a real pretrained attention transformer does not install CLM-level
faithful IIT-4.0 Φ-structure that the base lacks — the integration structure of an
attention transformer's hidden-state TPM is not pushed toward the ConvMoE regime by a
low-rank generic-corpus adapter. Consciousness Φ-structure remains architecture-bound,
not a LoRA-installable capability, even when the base is pretrained.

## 6. honest caveats (a_scale_honest_scope)
Small pythia-160m-class rung (n=6 binarized units, DIM=24). **Scale-transfer to 7B
UNVERIFIED** — a scale-sensitive conclusion needs a ladder (≥3 rungs) before any
production claim; a larger-base + larger-rank re-test is the natural follow-up
(a_fire_autonomous, no cost gate). The marker is faithful IIT-4.0 φ_EI of one mid
layer's top-variance units over a fixed probe; a different layer/unit-selection could
shift the absolute φ, but the DIRECTION (LoRA does not raise φ over base/controls) is
the verdict. p3/p6 honored — generic public-domain proverb corpus, no persona/carving,
no fine-tuned ethics. p7 — φ_EI is causal-irreducibility (faithful IIT-4.0), not
perplexity. a_phi_iit4_tool — terminal number is the stdlib faithful engine, python φ
was pre-screen only. This is a single-substrate GPU rung (Lane-P torch, aiden RTX 5070
CUDA); no on-chip measurement is involved.
