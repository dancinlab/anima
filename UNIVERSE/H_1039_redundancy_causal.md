# H_1039 — Is the planning Phi-split CAUSED by redundancy? (ablation test)

Status: PRE-REGISTERED (generation-only; not yet measured)
Lane: zero-cost CPU toy. Engines: stdlib faithful_phi + iit4_bigphi (a_phi_iit4_tool, no proxy).

## Hypothesis
H_1017 (prior GREEN) showed planning's mutual-information rise is REDUNDANCY-dominated
(Williams-Beer I_min PID: delta-redundancy +9.40 vs delta-synergy -1.04). That is a
CORRELATIONAL mechanism. This hypothesis tests it CAUSALLY: if the redundancy among the
planning channels is the cause of the faithful-UP / big-Phi-DOWN sign-split (scalar EI credits
redundant copies as integration-up, while big-Phi sees them as reducible-down), then surgically
REMOVING the redundancy should COLLAPSE the split.

## Method (sketch)
- Reuse the H_1004/H_1017 planning-vs-greedy substrate + PID harness.
- Intervention: orthogonalize / decorrelate the planning channels (e.g. ZCA-whiten or
  Gram-Schmidt the depth-ladder rollout channels before building the TPM) so the
  Williams-Beer redundancy term delta-red goes to ~0 while preserving total signal.
- Re-measure faithful phi_EI and big-Phi contrast (planning vs greedy) on the de-redundified
  substrate. Compare against the un-orthogonalized control.

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = removing the redundancy COLLAPSES the split: on the de-redundified substrate the
  faithful-UP / big-Phi-DOWN sign-disagreement vanishes (joint sign condition fails) while it
  holds on the matched control -> redundancy is the CAUSAL driver of the split (confirms the
  H_1017 mechanism causally).
- H1 FAIL = the split SURVIVES de-redundification -> redundancy is correlated-but-not-causal;
  the split has another driver (publishable closed-negative, a_paper_negative_ok). State the
  exact delta-red-reduction threshold and sign-eps (1e-3) before running.

## Honest scope (a_scale_honest_scope)
Toy n<=6 TPM; production-scale UNVERIFIED. Orthogonalization is one de-redundification operator;
others (PCA-drop, channel-ablation) are robustness follow-ups. g5 CODE-measured (p7).

## Verdict
PENDING — tier added only AFTER `.verdicts/1039_redundancy_causal/H_1039.txt` lands (g73).
