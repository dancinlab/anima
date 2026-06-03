# omega-substrate-coupled-decoding — paper log

Append-only history sister of `PAPER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-04 — draft v1 scaffold (OMEGA leak-invariant closure arc, #1783/#1784/#1786/#1791)

- [x] PAPER.tape roster row `@P omega-substrate-coupled-decoding := "./PAPER/omega-substrate-coupled-decoding"`
- [x] PAPER.md snapshot (@title · @goal · milestones · verdict matrix · leak-caveat framing) + PAPER.log.md
- [x] main.tex — 4 a_paper_format sections (§hypothesis falsifier · §method 5+1-wire ablatable bus + learned gate + toy n-gram→real d384 CDV2 + ANU QRNG control · §measurement verbatim CE/KL across #1783/84/86/91 · §finding Δ-vs-baseline + closed-negatives + leak-invariance) + abstract + intro + limitations + reproducibility + conclusion
- [x] verdict matrix — all 4 rungs TERMINAL (🟢 numerical / 🔴 closed-negative); every section claim → `.verdicts/omega-{engine,trained,gate,gpu}/<id>.txt`; NO 🟠/🟡 section (a_paper_gate · a_paper_sections)
- [x] honest leak caveat FOREGROUNDED (abstract + §finding + §limitations): CA-neighbor lookahead → absolute CE leak-optimistic + free-run gen whitespace; CONTRIBUTION = leak-invariant RELATIVE closure + closed-negatives, NOT perplexity/gen-quality (p7 · a_scale_honest_scope · a_paper_negative_ok)
- [ ] references.bib — IIT/transformer-decoding/QRNG literature + 4 anima verdict ledger entries (≥10)
- [ ] figures (≥1 fal.ai or native pgfplots: the 4-baseline CE bar across #1786 toy + #1791 GPU; structured-vs-shuffle separation)
- [ ] companion/{pr-roll,verify-ledger,session-journal}
- [ ] compile clean (xelatex × 3 + bibtex) + arxiv-prep

### significance (a_paper_significance — all present)
- pre-registered falsifiers: (#1783) is substrate state structurally null at the decode, or does the bus close the loop? (#1784/#1786/#1791) does a trained substrate + learned gate carry useful sequential structure, or is it vocab-shuffle noise? (4 pre-declared GPU criteria b/c/floor/structured)
- real measurements: #1783 random-init mock · #1784/#1786 numpy n-gram on 400KB corpus · #1791 trained 35.93M ConsciousDecoderV2 on 120MB multilingual wiki (H100, nvidia-smi 98-99% busy g63)
- finding: Δ vs baseline (GATED beats base/a_only/fixed + structured-vs-shuffle) AND ruled-out axes (fixed A−G degrades · random-init unstructured · quantum RNG no advantage)
