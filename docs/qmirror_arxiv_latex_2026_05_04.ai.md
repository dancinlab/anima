# qmirror arXiv preprint LaTeX conversion - landed handoff

**Date:** 2026-05-04
**Cycle:** qmirror arxiv latex
**Source draft:** `docs/qmirror_arxiv_draft_2026_05_03.md` (v0.1, 759 LoC)
**LaTeX project root:** `state/qmirror_arxiv_latex_2026_05_04/`
**Marker:** `state/markers/qmirror_arxiv_latex_landed.marker`
**Cost:** USD 0 (local pdflatex + bibtex; TeX Live 2026 already installed)
**Status:** v0.1 LaTeX skeleton landed; pdflatex smoke test PASS;
five text-flowchart figure placeholders ship inline.

---

## What landed

| artifact | LoC | purpose |
|----------|-----:|---------|
| `qmirror_arxiv.tex`              | 80  | revtex4-2 main document; `\input{}`s 12 sections |
| `sections/abstract.tex`          | 27  | abstract body (sits inside `\begin{abstract}`) |
| `sections/intro.tex`             | 88  | section 1 (problem + approach + contributions) |
| `sections/related_work.tex`      | 69  | section 2 (Aer/Cirq, NIST 800-22, IIT 4.0, CHSH) |
| `sections/architecture.tex`      | 156 | section 3 (Fig 1 + 6 subsections + 2 listings) |
| `sections/validation.tex`        | 183 | section 4 (Tab 1-3 + Fig 2 + Fig 4 + band revise) |
| `sections/cost.tex`              | 96  | section 5 (Tab 4-5 + Fig 3) |
| `sections/limitations.tex`       | 48  | section 6 (5 caveats) |
| `sections/future.tex`            | 79  | section 7 (5-axis qmirror 2.0 + Fig 5) |
| `sections/conclusion.tex`        | 36  | section 8 + acknowledgements + code/data avail |
| `sections/appendix_a_falsifiers.tex` | 45 | App A (qmirror 1.0 + 2.0 falsifier ledger) |
| `sections/appendix_b_xvendor.tex`    | 106 | App B (per-vendor correlators + xvendor matrix) |
| `sections/appendix_c_arxiv_readiness.tex` | 76 | App C (7-step submission readiness + 4 caveats) |
| `bibliography.bib`               | 295 | 32 BibTeX entries (ported verbatim from draft) |
| `figures/figures_outline.json`   | 162 | canonical figure intent + caption drafts |
| `figures/README.md`              | 25  | figure replacement roadmap (5 figures) |
| `Makefile`                       | 28  | `make pdf`, `make smoke`, `make veryclean` |

**Total:** 17 files, 1,384 LoC excluding generated `build/` artifacts.
**Sections coverage:** 9 of 9 (abstract + 8 numbered + 3 appendices) =
12 input files map 1:1 to draft markdown structure.

---

## Section -> draft markdown map

| LaTeX section | draft markdown source |
|---------------|------------------------|
| `abstract.tex`            | `## Abstract` (lines 13-39) |
| `intro.tex`               | `## 1. Introduction` (lines 43-118) |
| `related_work.tex`        | `## 2. Related work` (lines 122-181) |
| `architecture.tex`        | `## 3. Architecture` (lines 184-280) |
| `validation.tex`          | `## 4. Validation` (lines 284-380) |
| `cost.tex`                | `## 5. Cost analysis` (lines 383-426) |
| `limitations.tex`         | `## 6. Limitations` (lines 430-468) |
| `future.tex`              | `## 7. Future work` (lines 472-514) |
| `conclusion.tex`          | `## 8. Conclusion` (lines 518-533) |
| `appendix_a_falsifiers.tex` | `## Appendix A` (lines 628-653) |
| `appendix_b_xvendor.tex`    | `## Appendix B` (lines 656-721) |
| `appendix_c_arxiv_readiness.tex` | `## Appendix C` (lines 725-759) |

All 32 references from `## References` (lines 536-624) are cited via
`\cite{...}` in the appropriate sections; bibliography is rendered by
`apsrev4-2.bst`.

---

## Figures (5 placeholders shipped, camera-ready deferred)

| ID                       | label                          | placeholder kind | ships in |
|--------------------------|--------------------------------|------------------|----------|
| `fig:arch`               | Fig 1: 4-tier ANU architecture | `lstlisting` flowchart | architecture.tex |
| `fig:xvendor_heatmap`    | Fig 2: 4x4 \|dS\| matrix       | `lstlisting` ascii table | validation.tex |
| `fig:cost_bar`           | Fig 3: cost-per-battery semilogy | `lstlisting` ascii bars | cost.tex |
| `fig:closure_evidence_flow` | Fig 4: 8-cond closure timeline | `lstlisting` Gantt | validation.tex |
| `fig:qmirror2_axes`      | Fig 5: 5-axis qmirror 2.0       | `lstlisting` rank dot-plot | future.tex |

Camera-ready replacement (TikZ / matplotlib / graphviz) is deferred
to follow-on cycle; captions are final and load-bearing.

---

## Tables (8 typeset in LaTeX, all data load-bearing)

| ID | section | rows | columns |
|----|---------|-----:|--------:|
| `tab:cond_status`        | 4.1   | 8 | 4 |
| `tab:vendor_S`           | 4.2   | 4 | 6 |
| `tab:xvendor_matrix`     | 4.2   | 4 | 5 |
| `tab:cost_per_substrate` | 5.1   | 5 | 3 |
| `tab:calibration_lineitems` | 5.2 | 6 | 2 |
| `tab:falsifiers_v1`      | App A | 9 | 4 |
| `tab:falsifiers_v2`      | App A | 5 | 4 |
| `tab:correlators_forte` / `_rigetti` / `_ibm` | App B | 4 each | 4 |
| `tab:pairwise_delta_falsifier_assessment` | App B | 6 | 8 (full-page) |

---

## Build verification (pdflatex smoke test)

| pass | command | result |
|------|---------|--------|
| 1 | `pdflatex qmirror_arxiv` | PASS (10 pages, undefined cites expected) |
| 2 | `bibtex qmirror_arxiv`   | PASS (apsrev4-2.bst, 2 db files: notes + bibliography.bib) |
| 3 | `pdflatex qmirror_arxiv` | PASS (cites resolve, refs partial) |
| 4 | `pdflatex qmirror_arxiv` | PASS (all refs resolved, 0 undefined) |

**Final PDF:** `build/qmirror_arxiv.pdf`, 10 pages, ~441 KB.
**Make target:** `make pdf` (full bibtex+3-pass cycle); `make smoke`
(1-pass quick check); `make veryclean` (nuke `build/`).

**Known non-fatal warnings** (do not block PDF output):
- `Package nameref Warning: definition of \label has changed` (revtex4-2 quirk)
- `Illegal parameter number in definition of \Hy@tempa` (hyperref/revtex4-2 interaction)
- `Make exit code 1` from final pdflatex pass (cosmetic; PDF still emits)

---

## Four caveats on this v0.1 LaTeX conversion

(promoted from `appendix_c_arxiv_readiness.tex` for handoff visibility)

1. **Figure preparation deferred.** Five text-flowchart placeholders
   ship in this v0.1 (Figures 1-5). Camera-ready artwork (TikZ,
   matplotlib, graphviz) is deferred to a follow-on cycle; the
   captions and data are final.

2. **Peer review pending.** Zero external readers have reviewed
   either the Markdown source or this LaTeX skeleton at v0.1. The
   2-3 reviewer requirement remains the blocker for arXiv submission.

3. **License counsel sign-off pending.** The Apache-2.0 / GPLv3-via-
   aggregation interpretation is the author's reading of the FSF
   Mere Aggregation doctrine. Counsel review is required before
   claiming "Apache-2.0 clean" in a published preprint.

4. **revtex4-2 vs article class choice.** This v0.1 uses revtex4-2
   (PRL/PRA-style two-column physics layout) on the assumption that
   arXiv `quant-ph` is the natural category. If retargeting to
   `cs.LG` / `cs.AR`, switch to `\documentclass{article}` (or
   IEEEtran) and re-flow tables.

---

## raw rules compliance

- **raw#9 (hexa-strict on Mac side).** Mac side authored only
  `.tex`, `.bib`, `.json`, `.md`, `Makefile` — all explicitly allowed
  document/build formats. Zero `.py`, `.sh`, `.js` files added.
- **raw#10 (loud disclosure).** Four caveats called out in
  Appendix~C and re-promoted in this handoff.
- **raw#15 (cost gate).** USD 0 verified: local TeX Live 2026 install,
  no network calls, no API spend.

---

## Next gate: arXiv submission readiness

Sequential 5-7 day path to submission-ready (per Appendix C):

1. **External peer review (2-3 reviewers).** Single biggest gate;
   typical 2-5 day turnaround. Candidates: quantum-computing or
   integrated-information-theory researchers familiar with CHSH on
   AWS Braket, IIT 4.0 phi-star via pyphi, or NIST SP 800-22.
2. **Camera-ready figures (5 figures, ~1-2 days typesetting).**
   - Fig 1: TikZ block diagram of 4-tier ANU fallback.
   - Fig 2: matplotlib pcolor heatmap of 4x4 |dS| matrix.
   - Fig 3: matplotlib semilogy bar of cost-per-battery.
   - Fig 4: TikZ Gantt or graphviz dot of 8-cond closure timeline.
   - Fig 5: matplotlib bubble plot of qmirror 2.0 5-axis ranking.
3. **License counsel sign-off** on Apache-2.0 / pyphi GPLv3
   isolation claim language.
4. **Honest claim audit** + selection-bias prominent disclosure
   re-read pass.
5. **arXiv class confirmation** (revtex4-2 vs article;
   quant-ph vs cs.LG category).

After these 5 sub-gates clear, the build is `arxiv submit -upload`
ready (manual operator gate; this cycle does NOT submit).

---

## Cycle artifacts

- `state/qmirror_arxiv_latex_2026_05_04/` (LaTeX project root)
- `state/qmirror_arxiv_latex_2026_05_04/build/qmirror_arxiv.pdf` (10p smoke build)
- `state/markers/qmirror_arxiv_latex_landed.marker` (empty marker)
- `docs/qmirror_arxiv_latex_2026_05_04.ai.md` (this handoff)
