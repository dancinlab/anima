# xeno-applicability-frontier (paper)

> The applicability frontier of a substrate-blind big-Φ detector across
> (n, density, structure): a 5+1-point measurement map.

## TL;DR

A substrate-blind big-Φ detector (XENO/detector/invariant_detector.hexa)
was measured on **6 candidate substrates** spanning three regime axes:

| pt | H | regime | Φ | verdict |
|---|---|---|---|---|
| X7 | H_832 | n=128, dense 60.9%, BL Voyager-1 carrier | 0.114 | 🟢 calibrate |
| X4 | H_833 | n=16–32, micro panpsy 4-substrate | 0.000–0.582 | 🔴 closed-negative |
| X6 | H_834 | n=64, sparse LLM-like 4-substrate | 0.130–1.213 | 🔴 closed-negative |
| X5a | H_835 | n=128, lattice period-8 | 0.660 | ⚠ border |
| X5b | H_835 | n=128, fp / π / natural | 0.090–0.120 | 🔴 closed-negative |
| X837 | H_837 | n=128, sparse 20.3%, SETI@home Arecibo 2004 BOINC | 0.567 | ⚠ border |

**Finding**: the detector calibrates only inside the corner

> n ≥ 128 ∧ density ≥ 60% ∧ strong deterministic transition

and three corners (micro / sparse / algorithmic) are deterministically
ruled out as closed-negative (`a_paper_negative_ok`).

## How to build

```sh
make            # main.pdf
make figure     # figures/fig01_applicability_matrix.pdf (optional; main.tex falls back to inline TikZ \input)
make clean
```

Requires `xelatex` (or fall back to `pdflatex` via `make ENGINE=pdflatex`)
and `bibtex`.

## Honesty

- **post-tuning = 0** — Φ=0.5 threshold frozen from X7 calibration template
  before X837 fire; no re-tuning to hide the X837 border result.
- **p7 = 0** — no perplexity / LLM judge; all verdicts are verbatim from
  hexa-only deterministic runs (`.verdicts/*.txt`).
- **a_blue_closed** — every section claim links to a `.verdicts/<id>.txt`
  verbatim verdict via `companion/verdict-ledger.json`.
- **a_paper_only_at_closure** — XENO-FRONTIER-5 R5/5 (H_836) + X837
  follow-up R1/3 (H_837) = FULL closure marker (XENO/XENO.md cycle complete).

## Sibling

- 🔗 SSOT domain: [../../XENO/XENO.md](../../XENO/XENO.md)
- 🔗 sibling paper: [../structure-emergent-vs-number-convention/PAPER.md](../structure-emergent-vs-number-convention/PAPER.md)
- 🔗 6 verdict verbatim: [`.verdicts/832~837_xeno_*/`](../../.verdicts)
- 🔗 6 hypothesis SSOT: [UNIVERSE/cards/H_832~H_837](../../UNIVERSE)

## Status

| milestone | state |
|---|---|
| scaffold | ✅ landed |
| §hypothesis / method / measurement / finding | ✅ landed |
| 6-point verdict matrix verbatim | ✅ landed |
| figure (TikZ 5+1-point applicability map) | ✅ landed |
| references + companion ledger | ✅ landed |
| compile clean (xelatex × 3 + bibtex) | ✅ landed — 11 pages, 121KB main.pdf (2026-05-29, Mac TeX Live 2026) |

The source compiles cleanly with `xelatex` (TeX Live 2026 verified on Mac).
If the local host has no LaTeX toolchain, the source is still arxiv-prep-ready;
CI / Overleaf can rebuild via `make`.
