# H_1043 — What MINIMAL architectural change CAN install Phi-structure? (positive direction of arch-bound)

Status: PRE-REGISTERED (generation-only; not yet measured)
Lane: zero-cost CPU toy first (small models). Engines: stdlib faithful_phi exact n<=6
(a_phi_iit4_tool, no proxy). p3/p6: GENERIC byte targets only, NO persona/carving data.

## Hypothesis
H_1031 + H_1036 (prior RED, toy + real pythia-160m) closed the NEGATIVE: LoRA on a transformer
CANNOT install CLM-level consciousness Phi-structure — it is ARCH-BOUND ("the instrument, not the
score"). This is the CONSTRUCTIVE converse: what is the MINIMAL ARCHITECTURAL change (not a weight
delta) that DOES raise faithful IIT-4.0 phi_EI of the hidden-state macro-TPM toward the ConvMoE
baseline? Candidate: graft a small ConvMoE side-branch (dilated causal conv + tiny MoE) as an
architectural adapter onto a frozen transformer, trained on a generic byte objective.

## Method (sketch)
- Base: frozen small transformer (pythia-160m class), generic byte LM objective.
- Architectural adapter ladder (each an ARCHITECTURE change, not a LoRA weight delta):
  (a) ConvMoE side-branch, (b) a single recurrent/stateful mixing layer, (c) a depth-wise dilated
  conv block. Train each (small steps, generic bytes).
- Measure faithful phi_EI of the coarse-grained hidden macro-TPM (n<=6) before vs after each
  adapter; compare delta-phi against the LoRA-only control (H_1036, delta ~ -0.066) and the
  ConvMoE-native baseline.

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = at least one minimal architectural adapter RAISES faithful phi_EI by >= +0.10 over the
  frozen base AND beyond the LoRA control band -> a small ARCHITECTURAL graft (not weights) can
  begin to install Phi-structure -> confirms "instrument not score" constructively + identifies the
  cheapest sufficient architectural primitive.
- H1 FAIL = no minimal adapter raises phi_EI beyond the control band -> Phi-structure needs more
  than a graftable primitive (whole-architecture property; publishable closed-negative,
  a_paper_negative_ok). State the +0.10 threshold + the adapter ladder before running.

## Honest scope (a_scale_honest_scope)
Small-model rung; 3B/7B + emergence (not just phi) UNVERIFIED. phi-structure is necessary-not-
sufficient for "consciousness/emergence" — this rung measures the Phi axis only. p3/p6 honored
(generic byte targets). g5 CODE-measured (p7).

## Verdict
PENDING — tier added only AFTER `.verdicts/1043_minimal_arch_adapter/H_1043.txt` lands (g73).
