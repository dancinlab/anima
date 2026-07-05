# DESIGN TASK — anima G1 escape: the authored-transferable-data positive-control battery

You are designing the single most-decisive $0 experiment for anima's G1 recombination wall, given the
NEWEST reframing. Output a DESIGN spec only (no code): each experiment = name · hypothesis · exact
generative/measurement procedure · FROZEN pass/kill bar · which decision it forks. Be adversarial —
find the cheapest probe that could still FALSIFY the escape claim before any GPU spend.

## The wall (now fully reframed — TARGET/DATA side, proven on real 303M)
G1 recombination wall = a 303M byte-LM holds in-distribution structure but held-out recombination = 0.
Two decisive results just closed the mechanism side and opened the data side:
- **Mechanism CAPABLE (sweep):** on a fair pure-bilinear non-commutative target with disjoint concept
  split, trained bilinear binding mechanisms EARN cross-distribution transfer where additive floors ~0
  and order-shuffle collapses: hypernet 0.911 · TPR 0.586 · FiLM 0.512 · slot 0.236. So the mechanism
  class can transfer *a transferable target*.
- **Target NOT transferable (crux #3032, REAL 303M reps):** FiLM predicts the 303M's own joint pair-rep
  h(a,b) from singles at cross R² 0.8656 — IDENTICAL to additive 0.8661 (delta -0.0005). The real
  303M+corpus composition is ADDITIVE; carries NO transferable bilinear interaction. Matches §4 (joint
  R² ≤ additive), F2 (composition powered only as in-distribution collocation, held-out starved),
  H_6163 (frozen 303M rep carries no generalizing falsifiability representation).
- **Conclusion:** the wall is TARGET/DATA-transferability side, NOT mechanism-capacity and NOT model
  size. A cleverer readout or bigger model cannot help. **Escape = authored transferable-form data +
  any bilinear mechanism.**

## The untested crux (what I want you to design)
Nobody has yet run the mirror-image of the #3032 crux: instead of measuring FiLM-vs-additive on a model
trained on the EXISTING collocational corpus, TRAIN a (toy) byte-LM with pure next-token CE on AUTHORED
transferable-form data, then measure FiLM-vs-additive on ITS learned reps over held-out disjoint concept
pairs. This forks the whole program:
- If FiLM > additive by margin on the authored-data model → authored transferable data DOES induce
  target-side transferable bilinear structure that survives byte-LM CE → the escape is real, the 303M
  GPU fire (train on authored corpus) is warranted.
- If FiLM ≈ additive even on authored data → byte-LM CE collapses composition back to additive
  REGARDLESS of data → the escape is deeper than "just author the data"; reopen. Negative is decisive.

## What I need — a ranked $0 battery around that crux
1. **Authored-transferable-corpus GENERATOR spec.** What exactly makes composition held-out-transferable
   AND non-commutative AND learnable by byte-LM CE from raw byte-context (not pre-segmented role/filler
   vectors)? Give the concrete generative grammar: concept vocabulary, disjoint train/held-out concept
   split, the composition rule (must be a fixed concept-agnostic non-commutative operator so it
   generalizes to unseen concept pairs — the analog of the sweep's fixed tensor T), reversal/negative
   balance, surface realization as bytes. Include the anti-Goodhart controls (shuffle-order, additive
   baseline, in-distribution-collocation confound: the corpus must NOT let a plain additive/lookup model
   win, or the harness is INVALID — pre-register the anchor-validation rule).
2. **The measurement.** Toy byte-LM (small, CPU/owned-pool numpy — pre-register size), pure autoregressive
   next-token CE, NO role/filler head scaffold (mirror rung-3). Extract per-concept single reps + joint
   pair reps; fit FiLM (bilinear) and additive readouts on TRAIN concept pairs; test cross R² on HELD-OUT
   disjoint concept pairs; shuffle-order control. Frozen pass bar (margin) + kill bar.
3. **Ablation ladder** — vary corpus transferability (fully-transferable ↔ half-collocational ↔ pure
   in-distribution-collocation) and locate where FiLM-over-additive appears/disappears. This yields the
   actionable spec for the real F2 303M corpus build (the "authored transferable data" recipe).
4. **The strongest adversarial kill** — where is this toy most likely to give a spurious PASS that will
   NOT survive real distributed byte-context 303M? Design the cheapest guard against it.
5. **303M fire go/no-go** conditioned on each battery outcome + one-line cost estimate.

Keep it engine-native honest: toy = DIRECTIONAL (a_toy_scale_recheck), only 303M core/-decode = TERMINAL;
p7 no tune-to-green (bars frozen before running); negative/kill is a valid, publishable result.
