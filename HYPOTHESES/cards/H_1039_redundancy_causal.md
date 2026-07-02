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
🟢 REDUNDANCY-CAUSAL (H1 PASS) — 2026-06-09. De-redundifying the planning channels
(ZCA-whiten primary; Gram-Schmidt robustness, both on the continuous top-variance channels
before median-binarization) REMOVES the Williams-Beer redundancy (control |Δred|=9.40 →
ZCA 97.3% cut / GS 99.6% cut, both clearing the >=80% frozen threshold) AND COLLAPSES the
split (SPLIT False on BOTH de-redundified arms) WHILE the split HOLDS on the matched control
(SPLIT True: faith +2.33 UP / big-Φ −4.01 DOWN). Redundancy is the CAUSAL driver of the
split — H_1017's correlational mechanism confirmed CAUSALLY, consistent across both operators.

Raw + mirror≡stdlib proof (n=4 AND n=5, a_phi_iit4_tool, no proxy) + de-redundified-vs-control
table: `.verdicts/1039_redundancy_causal/H_1039.txt` (g73). Code:
`UNIVERSE/h1039_redundancy_causal.py`. JSON: `UNIVERSE/h1039_redundancy_causal_result.json`.

| arm        | faith Δ | faith | big-Φ Δ  | big-Φ | Δredund | SPLIT |
|------------|---------|-------|----------|-------|---------|-------|
| control    | +2.3332 | UP    | −4.0083  | DOWN  | +9.3958 | True  |
| dered_zca  | −0.0709 | DOWN  | −3.0843  | DOWN  | −0.2563 | False |
| dered_gs   | +0.0023 | UP    | +1.2000  | UP    | +0.0396 | False |

HONEST SCOPE: TOY n=4 EXACT (mirrors proven n=4,5); production-scale UNVERIFIED. ZCA primary,
GS robustness; PCA-drop / channel-ablation are follow-up operators. The PID is the
intervention-validation variable (NOT a Phi proxy). SERIAL CPU, $0, no GPU/pod. g5 (p7).
