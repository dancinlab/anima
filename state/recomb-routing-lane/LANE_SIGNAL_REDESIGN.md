# Fable lane training-signal redesign (H_9235 · copy-trap fix)

**(A) — buildable, with a pre-registered kill-switch at each gate. The core fix: derivtrace-with-inline-definitions was never the right training distribution — its target leaks. Train in the verdict format itself, pair-split.**

## Why the copy trap resolves this way

The system-G1 verdict fails held-out today, which means **at verdict time the composed target is NOT copyable from context** (if it were, the trunk's induction head would pass held-out too — copy is pair-agnostic). So the train/test mismatch is the whole bug: you trained on a format where the target leaks (CE≈0, zero residual) and test on a format where it doesn't. Candidate (d) is correct and reduces to: **CE in the verdict-format distribution on a TRAIN split of pairs**. Candidate (b)'s objection ("not the real generation task") inverts — the no-copy format *is* the real task; derivtrace-with-defs was the scaffold. (a) is dead as a loss on copy data: swapping B swaps what's copyable, CE≈0 both ways, difference ≈0 — keep it as a post-hoc diagnostic only. (c) is #3135 by construction: the "wired so it also helps real generation" step is exactly the thing you can't hand.

## The loss / what to dump

Corpus: derivtrace variant where the prompt carries the **concept names/cues only, definitions absent from the copyable window** (match the ρ·weave verdict format as exactly as possible), target = composed span. Pair-split: every held-out pair's *concepts* must each appear in ≥k train pairs (concept-covered, pair-disjoint) — otherwise held-out tests memory, not routing.

Dump per example: causal mean-pool `yn` at composed-span positions, base logits there, target bytes, **word-initial position mask**, pair ids.

Loss (numpy, frozen trunk):

```
L = Σ_{t ∈ word-initial composed positions} CE(base_logit_t + g·W2·gelu(W1·pool_t), y_t)
```

Word-initial-only matters: a pooled-context logit bias is nearly static across a span, so it can only act as a lexical prior tilt — but that's sufficient, because once the first byte of wA/wB is tilted the trunk autocompletes the word. The trunk's residual is concentrated at word-initial bytes; loss elsewhere is noise. This also keeps the lane's role honest: routing (which words to surface), not generation.

Generalization mechanics: this target is *easier* than the XOR pre-check, not harder — surfacing "wA wB" for pair (A,B) is a **factorized per-concept lookup** (detect concept-i in pool → bias its word-initial bytes), and each concept is seen in other train pairs. Pair-agnostic by construction. XOR proved the pool supports even conjunctive readout; this needs only unary routing to the emit position, which is exactly the fork-A reframe (info in pool at 0.95/0.97, lost only at generation point).

## Gate order ($0-first, each gate has a terminal)

1. **$0 smoke (5-ex)**: base CE lane-OFF at word-initial composed positions in the no-copy format. Must be substantially > 0 (≳1 nat). If ≈0 → trunk memorized pair→output in *weights*, residual doesn't live in context → the format redesign can't help; go to gate-2's probe immediately.
2. **Trainability probe before the lane**: fit a same-capacity MLP probe pool_yn → target-word-id on TRAIN pairs. If the probe can't fit *train*, no loss can — the frozen pool doesn't support name→word lookup. **That is the (B) terminal**: route exists (XOR) but no real-task signal trains it — H_1840 one level up, wall = learning signal not representation. This probe is the single cheapest confirming test you asked for.
3. **Train the lane** on train pairs. Train CE must drop.
4. **Frozen crack criterion** (pre-register before step 3): engine-native system-G1 on HELD-OUT pairs, surfacing(lane-ON) > surfacing(lane-OFF), with (i) shuffled-pool control collapsing the effect, (ii) concept-ablation specificity (drop A from context → wA bias vanishes; the (a) swap-B counterfactual lives here), (iii) train-pair vs held-out-pair gap reported verbatim. Train-fits-but-held-out-flat = **#3135 one level up, confirmed**: the pre-check's pair-agnosticity was a property of the handed XOR structure, and fork-A closes as the handed-atom illusion. Report it as such.

## Most-likely failure

Not capacity, not copy — **underspecification**: in the no-copy format the composed continuation is one of many plausible outputs, so the CE gradient part-points at frequency priors and the lane learns a marginal unigram tilt (the additive floor wearing a new hat). Two mitigations baked in above: word-initial-only loss (concentrates gradient on the concept-specific bytes) and the ablation-specificity control in the crack criterion (a unigram-tilt lane fails (ii) — bias won't track which concepts are in the pool). If the lane passes train CE but fails specificity, that's the additive floor, not a routing win — don't tune toward the green.

Adversarial bottom line on your last question: the 0.98 pre-check proves the pool and the route, nothing about the real target's structure. But the real target's structure (factorized lookup) is strictly weaker than XOR, so if this dies it dies at gate 1 or 2 — cheaply, before any training — and the verdict writes itself: signal-wall, not representation-wall.