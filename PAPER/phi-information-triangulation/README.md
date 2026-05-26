# <slug> — paper title placeholder

> One-line framing of the paper. Replace this block with paper-specific
> notes (status · target length · companion records / data).

## Source layout

- `main.tex` — single-column arxiv-style LaTeX (article class, 11pt A4).
  Ships with a 9-section spine: Introduction · Background · **§Full Pipeline**
  (tier-tagged stage table) · Method · Verify · Results · Limitations
  and honest caveats · Reproducibility · Conclusion. BLUE-MAX appendix
  template at the tail (commented out, fill in when audit-ready).
- `references.bib` — BibTeX, 5 example entries (`@article`, `@book`,
  `@inproceedings`, `@misc` dataset, `@misc` arxiv). All real entries
  must carry a DOI / arxiv id / stable URL. No tier emoji in this file
  (pdflatex chokes; the lint blocks it).
- `companion/` — data records that travel with the paper:
  `verify-ledger.json` · `pr-roll.json` · `session-journal.md` ·
  `adapter-defect-catalog.json`. See `companion/README.md`.
- `Makefile` — engine pinned to **xelatex** (UTF-8/emoji native). Targets:
  `make` · `make figures` · `make figures-clean` · `make wordcount` ·
  `make pages` · `make lint` · `make arxiv-tar` · `make clean` ·
  `make distclean`.

## Build

```bash
make                # → main.pdf (xelatex × 3 + bibtex)
make wordcount      # texcount -1 -sum -merge (falls back to wc -w)
make pages          # pdfinfo Pages
make lint           # commons @D g51 extended (sections + counts + emoji guard + cites)
make arxiv-tar      # out/<slug>-arxiv.tar.gz
make clean          # remove intermediates (PDF preserved)
make distclean      # also remove PDF + out/
```

## Figures

The template ships THREE working figures so `make` produces a paper that
compiles end-to-end with real-looking artwork:

- `figures/_scripts/fig01_example.py` — matplotlib bar chart (3 placeholder
  data points). Replace the `DATA` rows + y-axis label + caption with your
  result; `make figures` regenerates the PDF.
- `figures/_scripts/fig02_line.tex` — standalone TikZ/pgfplots line plot.
  Native LaTeX (no Python dep); replace the `coordinates {...}` rows.
- `figures/_scripts/fig03_pipeline.tex` — TikZ stage-flow diagram for the
  §Full Pipeline section. Relabel the seven nodes for your domain.

Add `fig04`, `fig05`, ... by dropping `figures/_scripts/figNN_<name>.{py,tex}`;
the Makefile picks them up automatically.

Drop other figure sources under `figures/`:

- vector: `.pdf` / `.eps` (preferred for plots)
- raster: `.png` (cover / teaser / AI-generated schematics only)
- TikZ: inline in `main.tex` OR standalone under `_scripts/*.tex`

**Standalone figure pattern (working pattern from the 58p monograph build).**
A `_scripts/*.tex` figure is a *standalone* document (its own `\documentclass`).
The correct wiring in `main.tex` is `\includegraphics{figures/figNN.pdf}` of the
**compiled** PDF — NOT `\input{figures/_scripts/figNN.tex}`. `\input`-ing a
standalone pulls a second `\documentclass` into your paper and breaks the build.
`make figures` compiles each standalone to `figures/figNN.pdf` for you.

For AI-generated figures, keep the verbatim prompt under
`figures/_prompts/<name>.txt` so provenance is reproducible. See
`figures/_prompts/cover.template.txt` for a fal.ai prompt-design guide.
Mark the caption with `% generated via <tool> (prompt: figures/_prompts/<name>.txt)`.

Generate a fal.ai cover via the sidecar plugin:

```bash
/paper fig square_hd figures/_prompts/cover.txt figures/cover.png
```

For a richer reference paper with multiple figures, tables, and 18 real
bibtex entries, see `/paper sample <slug>` (copies the bundled
`sample-nb-bcs-absorbed` verbatim).

## TeX Live dependencies

The preamble ships with `pgfplots` (used by the standalone TikZ figures and
shipped by default in v0.9 — the 58p monograph build had every agent add it by
hand). On a minimal BasicTeX install it is not bundled; install it once:

```bash
sudo tlmgr install pgfplots
```

Other preamble packages (`siunitx`, `booktabs`, `natbib`, `caption`, `listings`)
are in the standard TeX Live / BasicTeX `scheme-medium`; `tlmgr install <pkg>`
any that are missing.

## Monograph mode (v0.9)

For a book-length document (the HEXA-FUSION 58-page monograph pattern), scaffold
with `monograph-init` instead of `new`:

```bash
/paper monograph-init <slug> [N]   # default N=12 appendices
```

This produces the `new` template spine PLUS an `\appendix` block in `main.tex`
that `\input`s N self-contained chapters under `appendix/<L>_*.tex` (each a
`\section` + `\label` + `% TODO` stub), alongside the `companion/` data-record
dir. Fill one appendix at a time:

```bash
/paper fill A           # prints the per-appendix fill runbook (source · \input
                        # wiring check · recompile note)
/paper companion sync   # best-effort refresh of companion/{pr-roll,verify-ledger}.json
```

The Makefile's `$(DOC).pdf` prerequisite list includes `appendix/*.tex` and the
figure PDFs (v0.9), so editing an appendix or a figure triggers a rebuild on the
next `make` — no `make distclean` needed. `/paper lint` auto-detects the
monograph tier (`\appendix` + ≥6 `\input` appendix files) and raises the bar to
≥30 pages, ≥6 figures, and a present `companion/` dir; figure and table counts
traverse main.tex AND every `\input`'d appendix file. The seed reference is
`/paper sample sample-fusion-7gate` (the §Full Pipeline pattern).

## Honest stance

- Every claim traces to a bibtex entry with DOI / arxiv / URL, OR to an
  `atom:<id>` in `companion/verify-ledger.json`.
- Caveats live in `\section{Limitations and honest caveats}` and should
  word-for-word match any companion data record.
- Pre-register thresholds in the methods section — don't pick them after
  seeing results.
- Tier emoji 🔵 closed-form / 🟢 numerical / 🟡 cited / 🟠 wet-lab /
  🔴 falsified — falsified results stay in (honest negative), never deleted.
- `references.bib` MUST stay emoji-free (pdflatex chokes; `make lint`
  blocks it deterministically).

## Engine notes

The default engine is **xelatex** (Makefile pin). Tier emoji and any UTF-8
characters in `main.tex` render natively. pdflatex emits a fatal on the
first literal emoji (encountered on hexa-fusion-7gate); switch back to it
only after stripping every literal emoji from `main.tex` (use the
`\tierBlue` / `\tierGreen` / ... `\providecommand` macros at the top of
`main.tex`, redefined to a non-emoji marker).
