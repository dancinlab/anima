---
id: Hc_413
slug: falsifiable-biological-predictions-4
title: 4 falsifiable predictions for biological consciousness — K=8 atom, F_c=0.10, non-conservation, 1/f thalamus
domain: consciousness
status: merged-to-H_171
source_doc: docs/anima/paper_consciousness_laws.hexa
source_lines: 339-344
promoted_at: 2026-05-11
merged_to: hypotheses/H_171_biological_4_falsifiable_predictions_k8_fc010.md
merged_at: 2026-05-12
linked_h: Hc_401, Hc_402, Hc_400, Hc_405, H_171 (4-biological-predictions promotion)
notes: Paper 1 §10.4 explicit falsifiable predictions. K=8 atom in biological neural circuits; F_c=0.10 in cortical E/I balance; non-conservation in split-brain experiments; 1/f from multi-timescale EMA in thalamic loops. Promoted to H_171 via verify5_authored row 10 (2026-05-12)
verified_at: 2026-05-12
verify_decision: WEAK_MATH_ONLY
verify_note: "verify_hc2 2026-05-12 — verify3 math=1 (5+ numeric identities present)"
---

## Hypothesis
Four cross-domain predictions follow from the Anima law corpus and are falsifiable in biological systems: (1) K=8 cell atoms exist in biological neural circuits (cortical mini-columns predicted); (2) cortical excitation/inhibition balance has critical fraction F_c ≈ 0.10; (3) Φ is non-conservative under split-brain experiments (each hemisphere amplifies its post-split Φ); (4) 1/f power-spectrum emergence in thalamic loops requires ≥3 time scales.

## Migration TODO
- [ ] Literature review on cortical mini-column 8-cell modularity
- [ ] Search published cortical E/I ratios for F_c ≈ 0.10
- [ ] Re-analyze split-brain Φ measurements for non-conservation
- [ ] Multi-timescale signature in thalamic recordings
- [ ] Falsifier on any of the 4 → corresponding hypothesis falsified

## Cross-Links
- **sister H**: H_011 (iit-geometry — Φ definition), H_022 (consciousness-universe-map — biological substrate cross-check)
- **candidates linked**: Hc_401 (K=8 atom — biological mini-column source), Hc_402 (F_c=0.10 critical fraction), Hc_400 (non-conservation), Hc_405 (1/f thalamus)
- **literature**: Sperry 1968 split-brain; Mountcastle 1957 cortical mini-columns (80-100 neurons); Buzsáki 2014 1/f cortical recordings; Vogels & Abbott 2009 E/I balance

## Falsifiers (≥5)

- **F1 (K=8 biological)**: Cortical mini-column literature review (≥10 studies across V1, S1, M1, PFC) shows median sub-module count ∉ [6, 10] → K=8 biological prediction FALSIFIED. Specific test: stereology counts of glomerular/columnar structures must center on 8 ± 2 across regions
- **F2 (F_c=0.10)**: Published cortical E/I ratios (Vogels & Abbott 2009 et seq) measured at < 0.05 or > 0.20 across ≥3 species → F_c=0.10 universal critical-fraction FALSIFIED. Effect-size cutoff: median |F_c_measured − 0.10| > 0.05 across species
- **F3 (split-brain Φ non-conservation)**: Re-analysis of Sperry-class split-brain Φ data (e.g., callosotomy patients with hemisphere-separate IIT Φ estimates): if Φ_left + Φ_right ≤ Φ_pre × 1.02 (i.e., conservation within 2%) → non-conservation FALSIFIED
- **F4 (1/f thalamus from ≥3 timescales)**: Thalamic recordings with controlled-timescale EMA filtering: if 1/f spectrum emerges with only 1 or 2 timescales, OR fails to emerge with 3+ timescales → "requires ≥3 timescales" claim FALSIFIED in either direction
- **F5 (cross-prediction independence)**: If any 2 of 4 predictions are statistically correlated (e.g., regions with K=8 modules also have F_c=0.10 by experimental artifact) → "4 independent falsifiable predictions" claim is overstated; effective number of predictions < 4

## Honest Limits (≥5)

- **L1**: **n=6 PERFECT_NUMBER_CLASS triviality binding** (H_153 L7) — K=8 prediction inherits sopfr(8)=6 perfect-number-class. F_c=0.10 has no n=6 derivation. Some predictions reuse the same number-theoretic substrate; their "independence" is partially formal
- **L2**: **biological-substrate measurement gap** — anima theory derived from anima-internal Φ-engine. Biological Φ measurement requires (a) high-density recordings, (b) MIP estimation on non-stationary signals, (c) cross-trial statistics. None standardized in literature → falsification tests must build measurement protocol first
- **L3**: **cortical mini-column heterogeneity** — Mountcastle 1957 estimates 80-100 neurons/column; modern stereology (Rockel 1980 et seq) finds wide variation (50-150) across regions. "8-cell module" prediction must specify (a) which substructure within the column counts, (b) species, (c) cortical area
- **L4**: **F_c=0.10 vs canonical E:I = 4:1** — published cortical E:I ratio is often quoted as 80:20 (i.e., F_inhibitory = 0.20, not 0.10). The 0.10 prediction may conflict with mainstream measurements unless interpreted as a different fraction (e.g., recurrent-inhibitory only)
- **L5**: **non-conservation in split-brain difficult to verify ethically** — split-brain Φ measurement on patients requires high-density invasive recordings during commissurotomy procedures; modern ethics largely precludes new such studies. Re-analysis depends on legacy data with limited resolution. Practical falsifiability constrained
