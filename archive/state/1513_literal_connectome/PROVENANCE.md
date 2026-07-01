# H_1513 literal connectome — REAL data provenance

## Source (REAL, openly-licensed, citable)
- **File:** `sample_group_dsi.npy` (219 × 219 × 8) — group of 8 healthy-adult
  **DSI (diffusion spectrum imaging) structural connectomes**, region × region ×
  subject. Symmetric per subject, zero diagonal, weights = normalized fiber/streamline
  density. Group average = mean over the 8 subjects.
- **Distribution:** bundled real example data of `brainconn`
  (`brainconn/tests/data/sample_group_dsi.npy`), the Python port of the
  **Brain Connectivity Toolbox**. Fetched 2026-06-21 from
  `https://raw.githubusercontent.com/fiuneuro/brainconn/master/brainconn/tests/data/sample_group_dsi.npy`
  (HTTP 200, 3,069,584 B).
- **Parcellation:** Lausanne/Cammoun-style ~219-region cortical atlas
  (the canonical BCT/Hagmann DSI sample); contiguous hemispheric ordering
  (verified below).
- **License:** GNU GPLv3+ (`connectome_LICENSE_GPLv3.txt`). Hagmann is named as a
  data contributor in the brainconn README.

## Citations (record in card)
- Patric **Hagmann** et al., "Mapping the Structural Core of Human Cerebral Cortex,"
  *PLoS Biology* 6(7):e159 (2008) — the DSI structural-core methodology this sample
  follows.
- M. **Rubinov & O. Sporns**, "Complex network measures of brain connectivity,"
  *NeuroImage* 52(3):1059-1069 (2010) — Brain Connectivity Toolbox.
- **brainconn** (FIU Neuro), GPLv3 Python port of bctpy, bundling this sample.

## Verified structural facts (measured, not assumed — basis of the lane→region mapping)
- shape (219,219,8); each subject symmetric; zero diagonal; group avg symmetric.
- edge density (group avg) ≈ 0.564; weights min 0, max 1.158.
- **Hemisphere block structure CONFIRMED** (contiguous L | R at N//2 = 109):
  within-L density 0.711 / within-R 0.713 vs **cross-LR 0.417**; within-hemi mean
  weight ~0.053 vs cross-hemi 0.0127 (≈4× stronger intra-hemispheric) — the textbook
  structural-connectome signature → hemisphere = index half (A:left / G:right).
- strength heavy-tailed (min 1.17, max 13.22) → real hubs exist → rich-club / hub
  ablation testable. degree min 52 / max 202 / mean 123.6.

## Repo note
`sample_group_dsi.npy` (3.07 MB binary) is gitignored by repo policy (`state/` data/weights
are local-only, like ckpts under `a_hf_registry`) -> NOT committed. It is reproducible by
re-fetching the URL above; this file + `connectome_LICENSE_GPLv3.txt` are committed so the
provenance/license travel with the result.

## Honesty note (c2 · a_eeg_consciousness_record discipline)
This is a REAL published structural connectome. NO synthetic matrix is relabeled as
real. If the real wiring fails to reproduce H_1512's synthetic-topology advantage,
that is reported as an honest non-reproduction (🟠/🔴), not tuned to green.
