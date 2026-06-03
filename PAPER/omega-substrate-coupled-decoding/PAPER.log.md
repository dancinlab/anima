# omega-substrate-coupled-decoding — paper log

Append-only history sister of `PAPER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-04 — OΩ7 ABSORB: H1→OH1 leak-free arc folded (#1800 closed-neg multi-wire → #1801 positive minimal-gate)

- [x] §measurement: added R5 (#1800 F-TRAINED-LEAKFREE) + R6 (#1801 F-OH1-MINGATE) verbatim; R4 (#1791) re-labeled "leaky" (causal_ca=False) with explicit caveat
- [x] R5 — leak-free d512 (85,816,384 params, causal_ca=True, leak 0.000e+00, val_ce 0.8285 competent): FULL multi-wire gate FALSIFIED (GATED 3.643508 > base 3.097779 > a_only 1.144612 lives in ONE wire; g*=[−0.145311,+3.368538,−0.999118]; full-bus KL on 2.071722 ≈ shuf 2.080136 ratio 0.995955; structured gain_real +1.953167 ≫ shuf −2.429212) → 🔴 closed-negative
- [x] R6 — OH1 minimal gate gB·base+gA·A HOLDS: min_learned 0.883525 ≤ a_only 1.144181 AND < base 3.097779 (Δ+0.261 / Δ+2.214); fit gB=0.040,gA=0.901,gG=0.000; CROSS_CHECK reproduces #1800 to 6 decimals (base |Δ|0.000000, a_only |Δ|0.000431, full_AG |Δ|0.006349) → 🟢
- [x] §finding reframed HONEST: "coupling concept right, multi-wire gate formula wrong — closure lives in ONE wire"; multi-wire FALSIFIED added as a closed-negative; minimal A-wire gate is the positive closure form; H1→OH1 arc bullet (terminal-on-two-points)
- [x] abstract (iv) + leak-caveat + §limitations + §hypothesis Falsifier-3 + verdict matrix updated; ⏳ scale-ladder (OΩ4 concurrent) marked PENDING — ABSORB not finalize (a_paper_only_at_closure)
- [x] HONEST GATE: every number traced to .verdicts/omega-engine/{F-TRAINED-LEAKFREE,F-OH1-MINGATE}.txt verbatim — NO un-sourced number, NO new claim beyond the verdicts (g5/g63 · p7 · NO fabrication)

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
