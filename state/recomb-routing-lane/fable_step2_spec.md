# Step 2 (trained cross-attention retrieval lane) — give me the exact implementable spec.

Your Step-1 pointer-cache prediction was correct. Engine-native results on the 303M byte-LM, n=48 pairs,
6-point (lambda,T) grid, swap-margin Delta (m = CE(swap)-CE(match), Delta = mean(m_on - m_off)):

    off baseline: m_zero = -0.0836, m_lit = +0.2034
    ALL grid points (lam 0.1/0.2 x T 0.05/0.1; 0.4 still finishing but identical trend):
      zero-overlap Delta = +0.033 .. +0.034,  bootstrap CI ALWAYS includes 0  (e.g. [-0.021,+0.090])
      pairing-shuffle Delta = -0.012 (kills the small positive)
      cross-doc Delta = -0.059 .. -0.069
      LIT-overlap Delta (positive control) = +1.22 (lam0.1) -> +1.40 (lam0.2), grows with lambda
      crack = False on every cell

Reading: the cache does VERBATIM copy strongly (positive control huge, scales with lambda) but distributed
held-out-concept retrieval is a non-significant +0.033 nudge, pairing-shuffle-killed. Exactly your "Step 1
passes lit, fails zero -> escalate to Step 2". crossdoc negative = the cache is context-specific (good).

I will implement Step 2 myself in torch on an idle RTX5070 ($0). I need your PRECISE, one-shot-implementable
spec so I don't rework a 300-line trainer. I have the retrain corpus builder available: 48 training concepts
(concept-level disjoint from the 12 eval concepts ocean/forest/engine/music/market/medicine/desert/galaxy/
kitchen/law/glacier/circuit), each 8 keywords; build_corpus makes FILLER + "concept: kw kw kw kw kw. " + GAP
(>128 bytes) + STEM + target-byte, 70% retrieval / 30% associative. I have decode.clm_forward_hidden_logits(W,
tok, T) -> (yn[T,d=3784], base_logits[T,V=256]), the exact production trunk.

Specify concretely:
1. **Lane forward** — single-head cross-attention. Give exact tensor ops: Q=W_q·yn_t (d->dh, dh=?), K=W_k·yn_i,
   V=W_v·yn_i over which positions i (all j<t? include t? causal?), attn scaling (1/sqrt(dh)?), how attn output
   maps to a logit bias via W_o (dh->V), W_o init (you said "tied/init to trunk unembed" — the trunk readout is
   a conv `_conv1d(x, roWt, roB)` not a clean unembed matrix; how do I tie/init W_o to it concretely?), gate g
   (scalar? sigmoid of what?), tau clip. Final: logits += clip(g·(W_o·attn), ±tau)?
2. **Training** — loss masked to target span only: the corpus target is a SINGLE byte after the stem. Is the
   masked-span loss just CE at that one position, or do I need multi-byte target spans (if so, how to build
   them anti-copy)? Optimizer/lr/epochs/batch/wd/dh. What stops the same gate-smoothing backdoor here (the gate
   sees yn_t)? Should g NOT see yn_t (e.g. g = sigmoid(scalar) only, or g from the attn entropy)?
3. **Eval application** — in the swap-margin harness, at EACH continuation position t (not just target), apply
   the trained xattn with keys/values = all prior positions [0,t). Same Delta_zero bar. What is the correct
   pairing-shuffle control for a LEARNED xattn (permute K-row vs V-row alignment)? Keep cross-doc + lit positive
   control. n>=48.
4. **Pre-registered crack + kill** — exact threshold on zero-overlap Delta (CI, and vs pairing-shuffle), and
   the positive-control gate (lit must stay >0). If it lands on ~pairing-shuf again, is THAT the terminal cement
   for the whole frozen-readout augmentation class (your Q2 condition), or is there a step-3 before terminal?

Be concrete enough to code without guessing. If Step 2 is unlikely to beat +0.033 given these Step-1 numbers,
say so and give the $0 terminal argument instead — I would rather cement honestly than burn a GPU on a
foregone escalation.