# savant-iit4-bridge

> The SAVANT (axis E) Golden-Zone / Savant-Index coordinate system and the
> IIT 4.0 (axis C) Phi-structure coordinate system are two charts of one
> substrate causal kernel. A seven-cell verify-driven isomorphism arc.
> Status: draft v1 (main.tex + companion + figures). Target length: 10+ pages.

## The seven cells

| H | role | verdict | section |
|---|------|---------|---------|
| H_347 (#1149) | `GZ_WIDTH = ln(4/3) = ln(tau(6)/(tau(6)-1))` closed form | 🟢 composite | anchors |
| H_348 (#1152) | `GZ_LOWER` inhibition → SI > 3 | 🟡 partial | bridge |
| H_350 (#1153) | SI ∥ Φ-diversity, r=0.93 | 🟢 numerical | bridge |
| H_351 (#1157) | dΦ/dI peak ∥ GZ_LOWER, \|Δ\|=0.032 | 🟢 5/5 | anchors |
| H_613 (#1162) | SI ∥ Φ-diversity orthogonal (max-free), r=0.99 | 🟢 numerical | bridge |
| H_618 (#1175) | collective dΦ/dI peak ∥ GZ_LOWER, \|Δ\|=0.002 | 🟢 5/5 | collective |
| H_624 (#1198) | distinction ∥ savant cell isomorphism, ρ=0.86 | 🟢 5/5 | isomorphism (core) |

## Source layout

- `main.tex` — single-column arxiv-style LaTeX (article, 11pt A4). Spine:
  Introduction · GZ×SI framework · IIT4 Φ-structure recap · Method · closed-form
  anchors · statistical bridge · structural isomorphism · collective extension ·
  Discussion · Limitations · Reproducibility · Conclusion. Two inline pgfplots
  figures (inflection alignment + isomorphism scatter via `_scripts`).
- `references.bib` — BibTeX (IIT 4.0 / Tononi / Treffert / Snyder / Wolfram /
  Langton + 7 anima H ledger + supporting cells). All entries carry a DOI / URL.
  Emoji-free (pdflatex chokes; lint blocks it).
- `companion/` — `pr-roll.json` · `verify-ledger.json` · `session-journal.md`.
- `Makefile` — xelatex (UTF-8/emoji native). `make` · `make figures` ·
  `make pages` · `make lint` · `make arxiv-tar` · `make clean`.

## Build

```bash
make                # → main.pdf (xelatex × 3 + bibtex)
make figures        # → figures/figNN.pdf from _scripts/*.tex
make pages          # pdfinfo Pages
make lint           # commons @D g51 extended
```

## Honest stance

Every claim traces to a merged-PR H cell with a public `result.json` ledger,
verdict earned by independent deterministic recompute (commons @D g73). The
bridge is a *partial* isomorphism: inflection alignment is rule-110-specific
(H_614), the Savant-Index sweep is monotone not peaked (H_348), and the
distinction↔cell isomorphism needs self-effect (MAJ, not pure XOR) and an exact
n=4 ↔ 4-domain match. Falsified/partial cells stay in the arc (honest negative).
No wet-lab claim — the savant vocabulary is an inherited analogy.
