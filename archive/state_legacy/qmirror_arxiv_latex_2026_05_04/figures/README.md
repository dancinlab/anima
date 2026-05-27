# qmirror arXiv preprint - figures directory

**Date:** 2026-05-04
**Status:** v0.1 placeholders inline in `sections/*.tex` (lstlisting text-flowcharts).

Camera-ready replacements (deferred to follow-on cycle, not blocking
v0.1 LaTeX land):

| ID | label | suggested tool | data source |
|----|-------|----------------|-------------|
| fig:arch                | Figure 1: 4-tier ANU architecture     | TikZ block diagram or draw.io PDF | `nexus/.roadmap.qmirror`, `architecture.tex` |
| fig:xvendor_heatmap     | Figure 2: 4x4 \|Delta S\| heatmap     | matplotlib pcolor / seaborn       | `state/qmirror_chsh_xvendor_2026_05_03/verdict.json` + `state/nexus_qmirror_ibm_2026_05_03/verdict.json` |
| fig:cost_bar            | Figure 3: cost-per-battery semilogy   | matplotlib bar(yscale='log')      | `cost.tex` table |
| fig:closure_evidence_flow | Figure 4: 8-cond closure timeline   | TikZ Gantt or graphviz dot        | `state/qmirror_*/verdict.json` x 8 |
| fig:qmirror2_axes       | Figure 5: 5-axis 2.0 progression      | matplotlib bubble plot            | `state/qmirror_2_axes_2026_05_03/ranked_axes.json` |

Drop the rendered PDFs into this directory and update the relevant
`\begin{figure}` blocks in `sections/*.tex` to `\includegraphics`.

See `figures_outline.json` (ported from
`state/qmirror_arxiv_draft_2026_05_03/figures_outline.json`) for the
canonical figure intent and caption drafts.
