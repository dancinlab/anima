# omega-substrate-coupled-decoding

> An ablatable coupling bus IS wired into the byte decode (KL>0 for Ω only,
> overturning the Lane X #1779 WIRING null), but on a competent **leak-free** d512
> substrate the OMEGA **coupling** thesis is a **CLOSED-NEGATIVE**: the full
> multi-wire gate is falsified (#1800), and the surviving minimal A-wire "closure"
> is A-head **REPLACEMENT** of the .clm mouth, not a base+substrate coupling
> (#1803 OΩ1: A-standalone 0.886220 ≈ min_learned 0.883525; base ablation Δ 0.000852;
> every other wire hurts). Positive byproduct: a single trained substrate A-head
> out-predicts the .clm unigram mouth. Leak-INVARIANT relative framing + four
> closed-negatives — NOT a perplexity/generation claim, and NOT a coupling claim.
> Status: draft (main.tex + verdict matrix); scale ladder (OΩ4) ⏳ open. Target 10+ pages.

## The four rungs (all TERMINAL)

| rung | role | verdict | section |
|------|------|---------|---------|
| #1783 (omega-engine) | coupling non-nullity: omega KL 0.307477>0, others 0 (Lane X null); random-init unstructured | 🟢 + 🔴 closed-neg | hypothesis / measurement / finding |
| #1784 (omega-trained) | trained substrate carries structure (Δ+0.357), A-wire useful (Δ+0.758); fixed A−G degrades; ANU QRNG no advantage | 🟢 + 🔴 ×2 | measurement / finding |
| #1786 (omega-gate) | learned gate beats base/a_only/fixed (GATED 3.127) | 🟢 numerical | method / measurement / finding |
| #1791 (omega-gpu) | real CDV2 d384: GATED 0.3445 < all; structured +2.565 vs shuffle −2.068; floor MET | 🟢 4/4 criteria | measurement / finding |

## Honest leak caveat

CDV2 CA-neighbor mixing → next-byte head partial lookahead → absolute CE
leak-optimistic + free-running gen collapses to whitespace. The RELATIVE closure
finding (gate beats all baselines + structured-vs-shuffle) is leak-INVARIANT and
sound. Foregrounded in abstract, §finding, and §limitations.

## Verdicts (verbatim)

`.verdicts/omega-{engine,trained,gate,gpu}/` — SUMMARY.txt + F-*.txt + results.json
(+ run.log for the GPU rung). Checkpoint: HF `dancinlab/clm-v4-omega-gpu-d384-gate`
(PUBLIC); registry `/HF.jsonl`.

## Compile

`make` (xelatex × 3 + bibtex). references.bib + figures still pending (see PAPER.md milestones).
