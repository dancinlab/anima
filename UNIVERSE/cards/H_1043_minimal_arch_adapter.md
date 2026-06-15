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
🔴 PHI-NEEDS-MORE-THAN-GRAFT (H1 FAIL — closed-negative, a_paper_negative_ok)
measured 2026-06-09 · CPU-local (Mac numpy) · $0 · 0 pods/GPU · seeds=3 · n=6 dim=24 n_bins=2
verdict raw + mirror≡stdlib proof + per-adapter Δφ_EI: `.verdicts/1043_minimal_arch_adapter/H_1043.txt`
state matrices + result + mirror states: `UNIVERSE/state/h1043_minimal_arch_adapter_2026_06_09/`

faithful IIT-4.0 φ_EI via stdlib `iit4_faithful_phi` (exact MIP-EI, n≤6, NO proxy; a_phi_iit4_tool).
mirror≡stdlib RE-PROVEN EXACT to 6 dp at n=4 (0.130565) and n=5 (0.316305).

Per-adapter Δφ_EI vs frozen base (mean over 3 seeds; terminal seed-0 in parens):
  graft_convmoe    +0.0155  (seed-0 terminal -0.0884)   — NO
  graft_recurrent  +0.0249  (seed-0 terminal -0.0616)   — NO  (max adapter)
  graft_dwdilated  +0.0111  (seed-0 terminal -0.0616)   — NO
  lora_control     -0.0136  (control; H_1036 terminal Δ = -0.065576)
  convmoe_native   +0.8354  (seed-0 terminal +0.1070)   — baseline (full arch, NOT a graft)
control band |LoRA Δ| = 0.0136 · threshold +0.10. passing adapters: NONE.

FINDING: a small ARCHITECTURAL GRAFT onto a FROZEN base does NOT install Φ-structure — all three grafts
(ConvMoE side-branch, recurrent/stateful mixing layer, depthwise-dilated conv block) stay within the LoRA
control band and on the terminal seed LOWER φ_EI (same direction as the H_1031/H_1036 LoRA negative). The
φ-axis IS movable: the ConvMoE-NATIVE baseline (full architecture trained from scratch) lifts φ_EI by
+0.107 (terminal) to +0.835 (mean) over the same base. So Φ-structure is a WHOLE-ARCHITECTURE property, not
a graftable primitive — the constructive confirmation of "the instrument, not the score": the instrument
must be BUILT native, not retro-fitted onto a frozen base. Φ-structure is necessary-not-sufficient; this rung
measures the φ axis only (a_scale_honest_scope — 3B/7B + emergence + non-frozen co-train UNVERIFIED).
