# H_1516 named-anatomical — REAL labeled connectome provenance

## Source (REAL, openly-licensed, citable, NAMED regions)
- **File:** `SCmatrices88healthy.mat` (88 × 90 × 90, float64) — structural connectivity
  matrices of **88 healthy adults**, AAL90 atlas, probabilistic-tractography normalized
  streamline density. Group average (mean over 88 subjects) = the labeled connectome used.
- **Labels:** `AAL_regions.csv` (`;`-delimited `ROI number;ROI name`, 90 rows in matrix
  order) — the EXPLICIT named regions (Hippocampus L/R = 37/38, ParaHippocampal L/R = 39/40,
  Thalamus L/R = 77/78, Caudate L/R = 71/72, Amygdala L/R = 41/42, Insula L/R = 29/30,
  Cingulum Ant L/R = 31/32, frontal regions, etc.). **AAL90 ordering is INTERLEAVED**
  (odd ROI# = Left, even ROI# = Right). This is WHAT LETS us place lanes by their TRUE
  anatomical NAME — the gap H_1512/H_1513 filled with a (hemisphere × graph-role) heuristic
  because the Lausanne-219 connectome they used had no in-repo labels.
- **Atlas:** AAL `ROI_MNI_v4`, **90 regions** — cortical + subcortical (hippocampus,
  thalamus, caudate, putamen, pallidum, amygdala, insula). **EXCLUDES the cerebellum**
  (AAL90, not AAL116). Honest substitution note: H_1512's 15-lane set has no dedicated
  cerebellar forward-model lane, so no lane is forced onto a missing region; the cerebellum
  gap is documented, not relabeled.
- **Distribution:** OSF project 10.17605/OSF.IO/YW5VF (the dataset of the Scientific Data
  paper below). Fetched 2026-06-21 via plain HTTPS GET ($0, no auth):
  - matrices: `https://osf.io/download/6823g/` (4,290,740 B)
  - labels:   `https://osf.io/download/6a8jx/` (2,047 B)
- **License:** **CC-BY-4.0**.

## Citations (record in card)
- A. **Škoch**, B. **Rehák Bučková**, J. **Mareš**, et al., "Human brain structural
  connectivity matrices–ready for modelling," *Scientific Data* **9**:486 (2022).
  DOI 10.1038/s41597-022-01596-9.
- N. **Tzourio-Mazoyer** et al., "Automated Anatomical Labeling of activations in SPM…,"
  *NeuroImage* 15(1):273-289 (2002) — the AAL atlas / named-region scheme.

## Verified structural facts (measured, not assumed)
- group avg shape (90,90); symmetrized; zero diagonal; near-dense (density ≈ 0.998),
  weights min 0 / max ≈ 0.68 / off-diag mean ≈ 0.0073 → BINARIZED at the positive median
  to match the H_1512/1513 binary-adjacency regime (= the binary regime those bars live in).
- Left (odd ROI#) total strength mean ≈ 0.650 vs Right (even) ≈ 0.640 — balanced hemispheres
  (AAL interleaved ordering confirmed; hemisphere honored by ROI parity in the lane mapping).

## Repo note
`SCmatrices88healthy.mat` (4.3 MB binary) is gitignored (`.gitignore` in this dir) — state/
data/weights are local-only by repo policy (`a_hf_registry`), reproducible by re-fetching
the OSF URL above. `AAL_regions.csv` (2 KB, the label SSOT) + this PROVENANCE.md are committed
so the named-region mapping, license, and citation travel with the result.

## Honesty note (c2 · a_eeg_consciousness_record discipline)
REAL published, NAMED structural connectome. NO synthetic matrix is relabeled as real; the
whole point of H_1516 vs H_1512 is the TRUE named placement (not a role heuristic). If the
real named placement is NOT Φ-optimal, that is reported as an honest non-optimal finding
(🟠), not tuned to green — and is itself the interesting answer to "is the brain mysteriously
Φ-optimal?" (no: optimized for cost/economy, not pure integration).
