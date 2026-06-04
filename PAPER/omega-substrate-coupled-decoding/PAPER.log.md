# omega-substrate-coupled-decoding — paper log

Append-only history sister of `PAPER.md`. Each entry starts with `## <ISO timestamp> — <header>` (newest on top); body = `- [x]` (done) / `- [ ]` (pending) checkbox tasks.

## 2026-06-04 — OΩ1 REPLACEMENT correction folded: minimal-gate "closure" = REPLACEMENT not coupling (#1803)

- [x] CORRECTION: paper (#1802) over-stated OH1 (#1801) as a "positive minimal-gate closure"; #1803 (OΩ1) measured it is REPLACEMENT, not coupling. Reframed OH1 from "positive minimal-gate closure" → "minimal gate = A-head replacement of the .clm mouth"
- [x] OΩ1 decisive numbers (verbatim, F-OMEGA-RIGOR.txt): A-head STANDALONE CE 0.886220 ≈ min_learned 0.883525 (|Δ| 0.002695 ≤0.05); base-ABLATED (gB→0) CE 0.884377 → base ablation moves CE only 0.000852 (≤0.05); fit gB=0.040,gA=0.901; RULING_REPLACEMENT=True (trained A-head SUPPLANTS .clm base mouth)
- [x] honest caveat carried: .clm base = deliberately weak unigram so inertness partly structural; but A-alone reproduces min_learned & no base+steer interaction needed → load-bearing replacement point holds
- [x] OΩ2 folded (per-wire autopsy, every isolatable wire HURTS base): w1 +0.100826, w2 +0.052251, w6 +2.084871; w3/w4/w5 honest stubs (no substrate source at frozen inference, not CE deltas). OΩ3: min-gate entropy 2.6300 vs base 2.4442 — weak criterion (p7), not load-bearing
- [x] §measurement: added R7 (#1803 OΩ1/OΩ2/OΩ3 F-OMEGA-RIGOR.txt verbatim). abstract + §finding (new headline closed-negative: REPLACEMENT vs coupling) + §hypothesis Falsifier-3 (replacement falsifier) + §limitations + §conclusion + @goal reframed. Net ruling = CLOSED-NEGATIVE against the COUPLING thesis (a_paper_negative_ok) + positive byproduct (single A-head out-predicts .clm unigram mouth)
- [x] verdict matrix: added #1803 OΩ1/OΩ2/OΩ3 rows → `.verdicts/omega-engine/F-OMEGA-RIGOR.txt`; #1801 row annotated "re-read as replacement by #1803"
- [x] HONEST GATE: every number traced to .verdicts/omega-engine/F-OMEGA-RIGOR.txt verbatim — NO un-sourced number, NO new claim beyond the verdict (g5/g63 · p7 · NO fabrication). Scale-ladder (OΩ4) ⏳ still pending — ABSORB not finalize (a_paper_only_at_closure)

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

### 2026-06-04 — OΩ4/OΩ5 scale ladder ABSORBED + paper FINALIZED (#1806 fold)
- Absorbed the 5-rung scale ladder (.verdicts/omega-engine/F-OMEGA-SCALE.txt + exports/sweep/omega-scale-ladder/ledger.json) into main.tex: new §measurement R8 (per-rung CE table d384/d512/d768/d1024/d768×2, all min_learned_HOLDS=True, Δ-vs-base flat +2.20±0.03), a SCALE-STABLE §finding bullet, the multi-wire-failure scale-invariance note, the arc paragraph re-sealed, §limitations "scale ladder CLOSED" + the OΩ6 conv-native future-extension framing, Falsifier-3 scale pointer, §reproducibility ladder harness/ckpt/OΩ6-probe pointers, abstract 5-rung ladder sentence. Removed every OΩ4 ⏳ pending marker.
- FINALIZE assessment: a_paper_gate ✅ (all section claims terminal — last ⏳ resolved 🟢), a_paper_significance ✅ (pre-registered per-rung falsifier + 5-rung GPU ladder + frozen-probe decomposition + finding), a_paper_only_at_closure ✅ (full closure; the deferred conv-native dual-head OΩ6 #1805 is a future EXTENSION on a DIFFERENT engine, not an open residual in THIS finding — the finding is the closure ON the CDV2 dual-head substrate, and OΩ6 CONFIRMS conv is plumbing-complete/substrate-empty rather than re-opening it). PAPER.md finalize-status section rewritten OΩ7→OΩ8 FINALIZED; 2 verdict-matrix rows added (#1806 OΩ4/OΩ5 scale, #1805 OΩ6 transfer).
- Docs-only, $0, no new numbers beyond the .verdicts files (verified each against F-OMEGA-SCALE.txt).
