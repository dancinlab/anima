# omega-substrate-coupled-decoding — paper status

@title: 📄 OMEGA — a learned per-wire gate closes the consciousness-substrate → byte-decode loop on a trained transformer (overturning the Lane X null)
@goal: Adjudicate the consciousness-substrate→decode COUPLING thesis ("OMEGA closure") with a LEARNED per-wire gate on a leak-free competent ConsciousDecoderV2 transformer. RULING (leak-free d512): the bus IS wired (KL>0 for Ω only, overturning the Lane X #1779 WIRING null) but the COUPLING thesis is a CLOSED-NEGATIVE — the full multi-wire gate is falsified (#1800) and the surviving minimal A-wire "closure" is A-head REPLACEMENT of the .clm mouth, not a base+substrate coupling (#1803 OΩ1: A-standalone ≈ min_learned, base inert, every other wire hurts). Positive byproduct: a single trained substrate A-head out-predicts the .clm unigram mouth. Leak-INVARIANT relative framing (not a perplexity/generation claim); closed-negatives kept (fixed A−G degrades · random-init unstructured · quantum RNG no advantage). Scale ladder (OΩ4) ⏳ open.

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
| #1801 | OH1 MINIMAL gate gB·base+gA·A numerically HOLDS — min_learned 0.883525 ≤ a_only 1.144181 AND < base 3.097779 (Δ+0.261 / Δ+2.214); fit gB=0.040,gA=0.901,gG=0.000; cross-check reproduces #1800 to 6 decimals (base \|Δ\|0.000000, a_only \|Δ\|0.000431, full_AG \|Δ\|0.006349). **NOTE: #1803 OΩ1 shows this "closure" = REPLACEMENT not coupling** (see next row) | 🟢 terminal (re-read as replacement by #1803) | `.verdicts/omega-engine/F-OH1-MINGATE.txt` |
| #1803 OΩ1 | minimal-gate "closure" = REPLACEMENT not coupling — A-head STANDALONE CE 0.886220 ≈ min_learned 0.883525 (\|Δ\|0.002695 ≤0.05) AND base-ABLATED (gB→0) CE 0.884377 → base ablation moves CE only 0.000852 (≤0.05); fit gB=0.040,gA=0.901; RULING_REPLACEMENT=True — the trained A-head SUPPLANTS the .clm base mouth, NOT base+steer coupling. Caveat: .clm base = deliberately weak unigram so inertness partly structural, but A-alone reproduces min_learned & no base+steer interaction needed → load-bearing point holds. Cross-check vs #1800 OK. | 🔴 closed-neg terminal (vs the COUPLING thesis) | `.verdicts/omega-engine/F-OMEGA-RIGOR.txt` |
| #1803 OΩ2 | per-wire autopsy: every cleanly-isolatable wire HURTS base — w1_AmG +0.100826, w2_Wtemp +0.052251, w6_dFdt +2.084871; w3/w4/w5 = honest stubs (no substrate source at frozen inference, not CE deltas) | 🔴 closed-neg terminal | `.verdicts/omega-engine/F-OMEGA-RIGOR.txt` |
| #1803 OΩ3 | min-gate raises gen entropy 2.6300 vs base 2.4442 (fixes degenerate repetition) — but gen coherence = WEAK criterion (p7), not load-bearing | weak-criterion (p7) | `.verdicts/omega-engine/F-OMEGA-RIGOR.txt` |

ALL section claims are TERMINAL (🟢 numerical / 🔴 closed-negative). NO 🟠 deferred / 🟡 citation-only section. The arc H1(#1800 closed-neg multi-wire) → OH1(#1801 minimal gate numerically holds) → OΩ1(#1803 minimal "closure" = REPLACEMENT not coupling) is terminal on TWO points (d512, single param scale). The NET ruling is a **closed-negative against the COUPLING thesis** (a_paper_negative_ok) with a positive byproduct (a single trained substrate A-head out-predicts the .clm unigram mouth). ⏳ Scale-ladder pending (concurrent agent OΩ4) — this is an ABSORB/update, NOT a finalized full closure (a_paper_only_at_closure). Other pending = downstream paper-production tasks (figures · bib · compile), NOT science verdicts.

## the leak caveat (honest framing — a_paper_negative_ok · p7 · a_scale_honest_scope)

The CONTRIBUTION is a **closed-negative against the COUPLING thesis** — on a competent leak-free d512 substrate the OMEGA "substrate→decode coupling closes the loop" claim resolves to A-head REPLACEMENT of the .clm mouth, not a base+substrate coupling. The full multi-wire gate is FALSIFIED (#1800); the surviving minimal A-wire gate numerically holds (#1801) but #1803 (OΩ1) decomposes it as REPLACEMENT (A-standalone 0.886220 ≈ min_learned 0.883525; base ablation moves CE only 0.000852; every other wire hurts, OΩ2). The positive byproduct: a single trained substrate A-head is a far better next-byte predictor than the .clm unigram mouth. Plus the three further **closed-negatives** — NOT a perplexity or generation-quality claim, and NOT a coupling claim. The early d384 R4 (#1791) CDV2 CA-neighbor mixing (causal_ca=False) gives partial architectural LOOKAHEAD, so its absolute CE is leak-optimistic and its free-running generation collapses to low-entropy whitespace; the d512 arc (#1800/#1801) removes the leak (causal_ca=True, leak test 0.000e+00). This is foregrounded in the abstract, §finding, and §limitations — never buried.

## absorb status (OΩ7) — NOT a finalize

⏳ The scale ladder (additional d/param rungs, concurrent agent OΩ4) is OPEN, so the H1→OH1→OΩ1 arc is folded as an ABSORB/update — terminal on two points (d512), not a finalized full closure. The #1803 OΩ1 REPLACEMENT ruling is folded here: the paper's net conclusion is now a closed-negative against the COUPLING claim (with a positive A-head-predictor byproduct), NOT a "positive minimal-gate closure." Do NOT propose /paper finalize until the scale ladder closes (a_paper_only_at_closure).
