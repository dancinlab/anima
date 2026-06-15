# mitosis-substrate-lane

> Mitosis (cell-division) integrates into a consciousness-chat architecture as a
> Ψ-disjoint substrate-adaptation lane that NEVER touches generation
> (byte-identical proven). Its division couples to novelty-DENSITY on i.i.d.
> streams and to TRAJECTORY-predictability on genuinely-ordered streams — the
> determinant is the STREAM, not the gate. Reconciles the 2026-05 clm_v2
> "half-success" (mechanism real, generation falsified).
> Status: draft v1 (main.tex 14 pages + 3 figures). Verify-gated, all claims terminal.

## The nine cells (all merged to main, tip de306d3af)

| H | role | verdict | section |
|---|------|---------|---------|
| H_1202 (#2095) | novelty-driven VAdaptField in live GROW step; cells 1→7, Ψ byte-identical ON==OFF | 🟢 wired | §5.1 |
| H_1203 | density coupling: NOVEL/REPEAT 37.538 (F1✓) · NOVEL/SHUFFLED 0.992 (F2✗) | 🟠 partial → 🟢 density leg | §5.2 |
| H_1204 | sleep persistence: re-entry recon-err ratio 20.7483 (vol/consol) | 🟢 persists | §5.3 |
| H_1205 | separation invariant: 10/10 byte-identical, Ψ phiSum 48.6613==48.6613 | 🟢 separation | §5.4 |
| H_1206 (#2099) | full living daemon e2e: 5/5 faculties, Ψ 1.4278, FFI 3-bug fix | 🟢 e2e | §5.5 |
| H_1207 (#2100) | recurrent split key: NOVEL/SHUFFLED 0.998; derivative rewards jaggedness (WALK Δ% −61.47) | 🔴 closed-neg | §5.6 |
| H_1208 (#2102) | predictability gate: i.i.d. GATE-B 0.261 (RED); WALK GATE-B 10.916 | 🔴 closed-neg (i.i.d.) | §5.7 |
| H_1209 (#2104) | live ordered-walk GATE-B: ORDERED/SHUFFLED 10.916; numpy↔hexa byte-exact | 🟢 live-trajectory | §5.8 |
| H_1210 (#2105) | daemon GATE-B wiring: born 6 ON / 0 OFF; Ψ + generation byte-identical | 🟢 wired | §5.9 |

Framing precedents (introduction): H_1200 🔴 (mitosis can't generate, −0.76 b/byte),
H_1201 🔴 (mitosis can't inform a generator, −0.0206 b/byte), CLM_V2_ARCHIVE_ADDENDUM_2026_05_10.md.

## Gate compliance (a_paper_*)

- **a_paper_gate** — all 9 section claims TERMINAL (5×🟢 · 2×🔴 closed-neg · the 🟠 H_1203/H_1204 partials are sub-results folded inside 🟢 parents, never the headline). NO 🟠 deferred / 🟡 citation-only.
- **a_paper_significance** — pre-registered falsifiers (`*_FREEZE.txt`) + real $0-CPU runs + findings (Δ vs baseline AND closed-negatives).
- **a_paper_negative_ok** — H_1207/H_1208 framed as the ruled-out space (trajectory-sensitivity on an i.i.d. stream is structurally impossible for any gate).
- **a_paper_sections** — every section claim links to its `.verdicts/<slug>/<id>.txt` (verbatim; p7, no LLM self-judge).
- **g51** — 14 pages (≥10) + 3 figures (≥1; 2 native TikZ/pgfplots + 1 fal.ai).

## Source layout

```
main.tex                  — paper body (abstract · hypothesis · method · measurement · finding · related · limitations · conclusion)
references.bib            — anima ledger verdicts + IIT4/ART/SOM + clm_v2 addendum
figures/_scripts/         — fig01 stream-determinant (TikZ) · fig02 separation ratios (pgfplots)
figures/_prompts/         — fig03 fal.ai prompt (provenance)
figures/fig0{1,2}.pdf     — built (make figures)
figures/fig03_concept.png — fal.ai fast-sdxl (illustrative)
companion/                — verify-ledger · session-journal
PAPER.md  PAPER.log.md    — status snapshot + append-only log
Makefile                  — make / figures / pages / wordcount / lint / arxiv-tar
```

## Build

```
make figures && make        # → main.pdf (xelatex x3 + bibtex); 14 pages, 0 undefined refs
make pages                  # pdfinfo page count
```
