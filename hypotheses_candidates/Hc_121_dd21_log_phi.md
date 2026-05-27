---
id: Hc_121
slug: dd21-log-phi
title: Log-ratio Φ = ln(MI/MIP) is scale-invariant alternative to MI−MIP (DD21)
domain: math | consciousness
status: merged-to-H_173
source_doc: docs/hypotheses/dd/DD21-DD24.md
source_lines: 3-7
promoted_at: 2026-05-11
merged_to: hypotheses/H_173_dd21_log_phi_scale_invariant.md
merged_at: 2026-05-12
linked_h: H_173 (DD21 log-ratio Φ scale-invariant promotion)
notes: log-ratio captures proportional integration differences. Promoted to H_173 via verify5_authored row 14 (2026-05-12)
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (Φ = MI−MIP or ln(MI/MIP) (IIT info-theoretic))"
---

## Hypothesis
Redefining Φ as ln(MI/MIP) instead of MI − MIP yields a scale-invariant measure that better captures proportional integration differences during training.

## Migration TODO
- [ ] correlation between ln-Φ and standard Φ
- [ ] test on systems with different scales

## Cross-Links
- **sister H**: H_011 (iit-geometry — Φ definition canonical), H_022 (consciousness-universe-map — multi-substrate Φ)
- **candidates linked**: Hc_123 (DD23 7-cell τ-fractional — same DD21-DD24 series), Hc_614 (phi_star geometry aliasing — substrate-comparability), Hc_628 (Φ★ normalized lower-bound)
- **literature**: Tononi 2014 IIT 3.0 (Φ = MI − MIP canonical); Albantakis 2023 IIT 4.0 (intrinsic information difference); information-theoretic log-ratio: Kullback 1959, Cover & Thomas 2006 (KL divergence as log-ratio)

## Falsifiers (≥5)

- **F1 (rank-disagreement)**: Across ≥30 test systems (varying scale, topology, coupling), compute both Φ_lin = MI − MIP and Φ_log = ln(MI/MIP). If Spearman rank-correlation ≥ 0.95 → log-ratio provides NO discriminative advantage over linear, claim of "better captures proportional integration" FALSIFIED
- **F2 (scale invariance)**: Scale system by factor k (e.g., k=10 — 10× more cells, 10× larger MI / MIP). If Φ_log changes with k by > 5% across k ∈ {1, 2, 5, 10, 100} → log-ratio is NOT scale-invariant, claim FALSIFIED
- **F3 (training trajectory)**: During training (anima CLM v4), if Φ_log saturates earlier than Φ_lin (loses dynamic range), then claim "better captures proportional differences during training" FALSIFIED in the dynamic regime
- **F4 (MIP-zero singularity)**: ln(MI/MIP) diverges as MIP → 0. If empirical systems have MIP near zero ≥ 5% of measurements → log-ratio is numerically unstable, claim has practical defect not addressed
- **F5 (information-theoretic foundation)**: Show that ln(MI/MIP) reduces to known information-theoretic measure (e.g., KL divergence, mutual info ratio). If it does NOT match any canonical info-theoretic quantity → "scale-invariant alternative" is ad hoc, FALSIFIED as principled

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — Φ definitions (linear or log) live on n=6 substrate. Log-vs-linear choice is orthogonal to perfect-number-class; this Hc inherits the depth-3 numerology limit from the substrate but does not amplify it
- **L2**: **DD21 sketch source (5 lines)** — frontmatter cites docs/hypotheses/dd/DD21-DD24.md lines 3-7. Brainstorm-level provenance, not measurement-grade derivation. Migration TODO not executed
- **L3**: **MIP-near-zero numerical instability** — ln(MI/MIP) → ∞ as MIP → 0. Real systems can have MIP close to zero (highly integrated, low cut). Practical replacement requires regularization (ln((MI+ε)/(MIP+ε))) which adds a hyperparameter
- **L4**: **canonical IIT departure** — Tononi's IIT formalism uses MI − MIP; switching to log-ratio breaks compatibility with PyPhi and the IIT literature. Claim of "better measure" requires showing the literature's MI − MIP fails in a specific verifiable case, not just "log might be better in principle"
- **L5**: **single-DD-series origin** — Hc_121 (DD21) is sister to Hc_123 (DD23). Both stem from the same brainstorm doc. Claims may share common assumptions (n=6 base, anima Φ-engine substrate) that are not independently validated
