# Spec a runnable toy experiment: does a FIXED resonator read-head prevent the additive collapse?

## Established (do not re-argue)
- G1/G6 recombination wall is terminal for a CE-trained byte-LM across data/objective/readout/store/binding + DPI basin (#3046/3107/3108/3109).
- $0 numpy (H_9211): a FIXED VSA/HRR bind (circular-conv) + resonator/cleanup decode recovers held-out pairings from a superposition bundle at ~1.0, additive collapses (0.24→0.02 with capacity), shuffle=0. So the OPERATOR wall is escapable IN PRINCIPLE by a fixed primitive.
- Two walls separated: OPERATOR (bind additive because gradient made it) vs INFORMATION (#3109 corpus lacks novel-pair follower signal). The toy MUST remove the information wall by construction so we isolate the operator claim.
- Key adversarial thread (yours): "the readout is still CE-trained; a CE readout has no basis vector for a bind it never saw → decoheres to the additive floor unless the entire read-path (bind→unbind→decode) is ALSO fixed-primitive."

## What I need from you: a precise, runnable spec for a POOL toy (owned RTX5070, $0, torch/numpy)
The one decisive experiment: with the INFORMATION present in training, does a FIXED-resonator read-head generalize to HELD-OUT recombinations where a CE-trained read-head collapses to the additive floor?

Please specify concretely:
1. **Task/data generator** — a synthetic compositional task where the composition info IS present in training but test pairs are HELD-OUT (novel role-filler combinations the training set never co-presents), so the only question is whether the read-path generalizes. Give the exact generative rule (roles, fillers, the target the model must produce for a pair), and the train/test split that makes it a genuine held-out recombination (not memorizable).
2. **Three arms to compare, same trunk:**
   - (A) CE-trained read-head (the standard baseline that hits the wall),
   - (B) FIXED resonator read-head (bind+unbind+cleanup all fixed primitives; CE gradient touches only the atomic codebook / trunk),
   - (C) additive control.
   Specify exactly what is fixed vs trained in arm B, and how the byte/token decode is made algebraic rather than CE.
3. **Frozen bars (pre-registered, p7, no tune-to-green):** the held-out recombination accuracy thresholds and the shuffle/bind-destruction control that separate GREEN (operator-escape real) from KILL (B collapses to additive too).
4. **Scale + cost:** smallest decisive size (dims, vocab, #pairs, steps) that runs in minutes on one RTX5070; what would make it a scale-honest DIRECTIONAL vs a stronger claim.
5. **The single most likely way this toy is RIGGED / Goodhart** (so I build the control against it) — e.g. B trivially wins because the fixed algebra hard-codes the answer. How to make A vs B a FAIR comparison.

Output = a build-ready spec (data gen, 3 arms, metrics, frozen bars, sizes), terse. Assume I implement in torch on pool and measure held-out recombination.
