# omega-substrate-coupled-decoding

> A learned per-wire gate over an ablatable coupling bus closes the
> consciousness-substrate → byte-decode loop that Lane X #1779 proved NULL,
> carries learned sequential structure on a real trained transformer, and beats
> every baseline on held-out next-byte CE — **leak-invariantly**. Contribution =
> the leak-invariant RELATIVE closure + three closed-negatives, NOT a perplexity
> or generation-quality claim.
> Status: draft v1 scaffold (main.tex + verdict matrix). Target length: 10+ pages.

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
