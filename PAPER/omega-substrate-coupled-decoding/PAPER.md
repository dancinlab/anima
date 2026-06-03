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
| #1791-caveat | CA-neighbor lookahead leak → absolute CE leak-optimistic + free-running gen collapses to whitespace; RELATIVE closure finding is leak-INVARIANT | honest caveat (foregrounded) | `.verdicts/omega-gpu/{F-COMPLETE.txt,SUMMARY.txt}` |

ALL section claims are TERMINAL (🟢 numerical / 🔴 closed-negative). NO 🟠 deferred / 🟡 citation-only section. Pending = downstream paper-production tasks only (figures · bib · compile), NOT science verdicts.

## the leak caveat (honest framing — a_paper_negative_ok · p7 · a_scale_honest_scope)

The CONTRIBUTION is the **leak-invariant RELATIVE closure** (GATED beats base/a_only/fixed AND structured-vs-shuffle separation) + the three **closed-negatives**, NOT a perplexity or generation-quality claim. The CDV2 CA-neighbor mixing gives the next-byte head partial architectural LOOKAHEAD, so absolute CE is leak-optimistic and the free-running generation sample collapses to low-entropy whitespace. This is foregrounded in the abstract, §finding, and §limitations — never buried.
