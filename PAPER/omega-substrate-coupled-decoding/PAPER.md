# omega-substrate-coupled-decoding — paper status

@title: 📄 OMEGA — a learned per-wire gate closes the consciousness-substrate → byte-decode loop on a trained transformer (overturning the Lane X null)
@goal: Show that a consciousness-substrate→decode COUPLING ("OMEGA closure"), with a LEARNED per-wire gate, carries USEFUL SEQUENTIAL STRUCTURE on a trained ConsciousDecoderV2 transformer — overturning the Lane X #1779 null (engine knobs structurally detached from the .clm forward) FOR the coupled engine Ω while confirming it for the three uncoupled engines — and to do so leak-INVARIANTLY (relative closure result, not a perplexity/generation-quality claim), with the closed-negatives kept (fixed A−G degrades · random-init unstructured · quantum RNG no advantage).

- [x] draft v1 scaffold (main.tex — §hypothesis · §method · §measurement · §finding + abstract/intro/limitations/reproducibility/conclusion)
- [x] verdict matrix — every section claim → `.verdicts/<slug>/<id>.txt` pointer (all 4 rungs TERMINAL)
- [ ] figures complete (≥1 fal.ai-generated)
- [ ] references ≥10 (`/paper bib add <doi-or-arxiv>`)
- [ ] lint pass (`/paper lint .`)
- [ ] compile clean (`/paper compile .`)
- [ ] arxiv submit ready (`/paper arxiv-prep .`)

## verdict matrix (a_paper_sections — every claim links to a verbatim verdict)

| # | claim | tier | verdict pointer |
|---|-------|------|-----------------|
| #1783 | coupling non-nullity: omega KL 0.307477>0 (L3 loaded=true), conv/cdv2/hexad = 0 (Lane X null) | 🔵/🟢 terminal | `.verdicts/omega-engine/{F-COUPLING.txt,SUMMARY.txt,results.json}` |
| #1783-neg | random-init coupling UNSTRUCTURED (KL_on 0.307477 ≈ perm_floor 0.303913) | 🔴 closed-neg terminal | `.verdicts/omega-engine/F-COUPLING.txt` |
| #1784 | trained substrate carries STRUCTURE: CE_bus_trained 4.1420 ≪ shuffled 4.4991 (Δ+0.357); A-wire base 4.0200→3.2619 (Δ+0.758) | 🟢 terminal | `.verdicts/omega-trained/{F-TRAINED-COUPLING.txt,SUMMARY.txt,results.json}` |
| #1784-neg1 | fixed A−G DEGRADES: CE_bus_trained 4.1420 > base 4.0200 | 🔴 closed-neg terminal | `.verdicts/omega-trained/F-TRAINED-COUPLING.txt` |
| #1784-neg2 | ANU QRNG no advantage: q-vs-PRNG KS p=0.7237 vs null-control p=0.9834 | 🔴 closed-neg terminal | `.verdicts/omega-trained/{SUMMARY.txt,anu_qrng_1024.json}` |
| #1786 | learned GATE g*=[0.142,1.183,0.341]: GATED 3.126961 < base 3.974346 (Δ+0.847) ≤ a_only 3.229252 < fixed 4.170100 (Δ+1.043) | 🟢 terminal | `.verdicts/omega-gate/{F-LEARNED-GATE.txt,SUMMARY.txt,results.json}` |
| #1791 | GPU real CDV2: GATED 0.3445 < a_only 0.4500 < fixed 1.4421 < base 3.0150; structured A-wire +2.565 vs shuffle −2.068; gate g*=[1.178,0.962,−0.208]; floor MET | 🟢 terminal | `.verdicts/omega-gpu/{F-COMPLETE.txt,SUMMARY.txt,results.json,run.log}` |
| #1791-caveat | CA-neighbor lookahead leak (causal_ca=False, d384 R4) → absolute CE leak-optimistic + free-running gen collapses to whitespace; RELATIVE closure finding is leak-INVARIANT | honest caveat (foregrounded) | `.verdicts/omega-gpu/{F-COMPLETE.txt,SUMMARY.txt}` |
| #1800 | LEAK-FREE d512 (causal_ca=True, leak 0.000e+00, val_ce 0.8285 competent): FULL multi-wire gate FALSIFIED — GATED 3.643508 > base 3.097779 (and > a_only 1.144612); g*=[−0.145311,+3.368538,−0.999118] collapses onto A/suppresses G; full-bus coupling KL on 2.071722 ≈ shuf floor 2.080136 (ratio 0.995955); structured gain_real +1.953167 ≫ shuf −2.429212 | 🔴 closed-neg terminal | `.verdicts/omega-engine/F-TRAINED-LEAKFREE.txt` |
| #1801 | OH1 MINIMAL gate gB·base+gA·A HOLDS — min_learned 0.883525 ≤ a_only 1.144181 AND < base 3.097779 (Δ+0.261 / Δ+2.214); fit gB=0.040,gA=0.901,gG=0.000; cross-check reproduces #1800 to 6 decimals (base \|Δ\|0.000000, a_only \|Δ\|0.000431, full_AG \|Δ\|0.006349) | 🟢 terminal | `.verdicts/omega-engine/F-OH1-MINGATE.txt` |

ALL section claims are TERMINAL (🟢 numerical / 🔴 closed-negative). NO 🟠 deferred / 🟡 citation-only section. The H1(#1800 closed-neg multi-wire) → OH1(#1801 positive minimal-gate) arc is terminal on TWO points (d512, single param scale). ⏳ Scale-ladder pending (concurrent agent OΩ4) — this is an ABSORB/update, NOT a finalized full closure (a_paper_only_at_closure). Other pending = downstream paper-production tasks (figures · bib · compile), NOT science verdicts.

## the leak caveat (honest framing — a_paper_negative_ok · p7 · a_scale_honest_scope)

The CONTRIBUTION is the **leak-invariant H1→OH1 ruling** — "coupling concept right, multi-wire gate formula wrong; the closure lives in one wire" — i.e. the full multi-wire gate is FALSIFIED on a leak-free competent d512 substrate (#1800), while the minimal A-wire gate gB·base+gA·A HOLDS (#1801) — plus the three further **closed-negatives**, NOT a perplexity or generation-quality claim. The early d384 R4 (#1791) CDV2 CA-neighbor mixing (causal_ca=False) gives partial architectural LOOKAHEAD, so its absolute CE is leak-optimistic and its free-running generation collapses to low-entropy whitespace; the d512 arc (#1800/#1801) removes the leak (causal_ca=True, leak test 0.000e+00). This is foregrounded in the abstract, §finding, and §limitations — never buried.

## absorb status (OΩ7) — NOT a finalize

⏳ The scale ladder (additional d/param rungs, concurrent agent OΩ4) is OPEN, so the H1→OH1 arc is folded as an ABSORB/update — terminal on two points (d512), not a finalized full closure. Do NOT propose /paper finalize until the scale ladder closes (a_paper_only_at_closure).
