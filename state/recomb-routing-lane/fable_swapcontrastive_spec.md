# Step-2 follow-on: swap-contrastive lane training. Give me the exact paired-data + loss spec (one pass).

Your Outcome-B verdict fired. The plain-CE-trained xattn lane:
  train T1=0.497 T2=0.315(CI_lo0.19) PASS (held-out associative CE improves), BUT
  geometry-matched swap-margin n=132: Dzero=-0.0005, Dlit=+0.0009, DshufV=-0.0007, ALL |D|<0.01 (no specificity).
  lane weights near-init: a=1.015, b=-1.986 (init 1,-2), Wo mean-abs=0.0053 (zero-init, barely grew).
So plain CE improved absolute CE generically (span/format shaping) without concept-specific routing, and the
routing gradient was too weak to move Wo off ~0. Your pre-registered follow-on = swap-contrastive loss. I'll
implement it in one pass; nail these:

Setup I have: precompute of 705 SINGLE-block training docs (frozen trunk yn[T,d] + base_logits + tok), 40 train /
8 val concepts (8 kws each), doc geometry FILLER + "concept: k0..k4. " + GAP(128-224) + STEM + TARGET(kw span).
Lane forward exactly your earlier spec (Q/K/V=yn@W, eligible i<t-64, gate=sigmoid(a*(logN-H)/logN+b) on attn
entropy only, bias=g*tau*tanh(ctx@Wo/tau), tau=8). Torch trainer, AdamW.

Questions:
1. **Paired data**: for the contrastive negative I need, per training item, the SAME target span read under a
   SWAPPED concept block (Dp's block replacing D's, same GAP/STEM/target, byte-length matched). That yn is NOT in
   my single-doc precompute. Cheapest correct construction: (a) precompute a second "swap" doc per item (Dp block
   + same gap/stem/target) = ~700 more frozen forwards, or (b) reuse in-batch other-concept docs as negatives
   without a matched target. Which — and if (a), how many negatives per positive (1 fixed Dp, or K sampled)?
2. **Loss**: exact form. Options: margin hinge L_c = mean(max(0, m - (CE_swap - CE_match))) with margin m=? ; or
   softmax/InfoNCE over {match, K swaps} on the target-span summed logprob; total L = CE_span(match) +
   0.1*KL_silence + lambda_c * L_c. Give m or the InfoNCE temperature, lambda_c, and whether to keep the 70/30
   retrieval/associative mix or go associative-heavy (the specificity lives in associative).
3. **Wo-stuck-at-zero**: is near-zero Wo a symptom the loss will fix, or do I also need an init/lr change (e.g.
   Wo small-random instead of zero, higher lr on Wo, or drop the KL-silence weight that may over-suppress)? One
   concrete change if warranted.
4. **Eval + verdict**: same geometry-matched swap-margin (n=132, cluster-bootstrap, lit gate). Same CRACK bar
   (CI_lo(Dzero)>0 AND CI_lo(Dzero-DshufV)>0 AND lit alive; BREAK if Dzero>=0.10)? And the terminal: if the
   swap-contrastive lane ALSO lands Dzero≈0 with lit alive, is THAT the frozen-final-state readout class terminal
   (the last member of the routing-lane family), or is there one more pre-registered step before 🧱?

Be concrete enough to code without guessing. If you judge swap-contrastive unlikely to move Wo given the near-init
result (i.e. the frozen final-state simply lacks routable concept structure at the emit point), say so and give
the $0 terminal argument + the mid-stack-tap note instead of a training spec.
