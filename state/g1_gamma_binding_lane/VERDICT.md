# VERDICT — H_9235 H2-lite (γ binding-lane · earned×trained cell) · 2026-07-09

**engine-native** py 2-production hidden dump (`anima evaluate --py --dump-hidden`, byte-identical trunk forward
`core/decode._fwd_trunk`) on the canonical E1-SLW 303M `.clm` · numpy CPU analysis on cached hiddens · $0 (free pool
summer) · frozen-first (`FREEZE.md`, sha before dump). **scope: engine-native MECHANISM/REPRESENTATION verdict of the
frozen trunk — DIRECTIONAL for the true G1 generation verdict (synthetic word-identity + assigned-code task ≠
meaning-composition in generation; a_scale_honest_scope).**

## The 2×2 cell this measured
```
             atom source                    bind             result
 H_9234      handed (clean tokens)      ×  trained        → 1.000 (proven)
 #3135       blind (learned, fixed-op)  ×  fixed          → FAIL
 H_1840      blind (learned, CE)        ×  CE-trained     → FAIL (signal never reaches bind)
 H2-lite ►   EARNED (real 303M hiddens) ×  composition-signal → THIS
```

## RUNG-a (unary atoms · segmentation granted · `h2lite_rungA_RESULT.json`)
`H1 unary probe = 1.000` — real 303M UNARY hiddens are **perfectly linearly separable by concept** (REFUTES the naive
"blind atoms" #3135 expectation at the unary level). `real-interaction op=1.000` (onlyA=0.46→chance = genuine 2-atom
bind), `additive=0.357 FAIL`, `handed=1.000`. **🟡 PRECONDITION-MET, NOT a wall break** — with H1-separable atoms + a
trainable adapter this is handed-equivalent (evaluate-py-3); ⚠ normalization-fragile. The decisive test is rung b.

## RUNG-b (superposed real context "The A and the B" · `h2lite_rungB_RESULT.json`)
```
recover:mean   A=0.953  B=0.973   ← BOTH concepts recoverable from the full context (NOT entangled)
recover:last   A=0.067  B=1.000   ← the GENERATION point (last position) retains only the most-recent concept (B), loses A
operator:      recovered-slots=0.515 · additive=0.476 · handed-ctrl(ground-truth one-hot)=1.000
```

### 🟢/🟡 REFRAME — the G1 recombination wall is NOT a trunk representation-capacity wall
Three robust, controlled findings on real 303M hiddens:
1. **Both concepts are present & linearly separable in the full context** (mean-pool recovers A=0.95, B=0.97). The wall
   is NOT "the trunk entangles/loses the two concepts" (the modal segmentation-collapse prediction is REFUTED).
2. **The generation READOUT point (last position) carries only the most-recent concept** (last: A=0.07 chance, B=1.00).
   Recombination fails at generation not because the info is lost, but because it is **not routed to the readout position**.
3. **Clean slots bind perfectly** (handed-ctrl one-hot = 1.000); the recovered-slot operator failing (0.515) is a
   **two-stage-probe train/test distribution artifact** (recovery probe is perfect on train = clean, 0.95 on held =
   noisier → the operator head trained on clean train reps doesn't transfer), NOT a fundamental binding failure.

⟹ The 303M trunk representation **SUPPORTS** two-concept recovery + (clean-slot) composition. The recombination wall at
generation = **readout-ROUTING** (the last-position readout only carries the recent concept) + slot-cleanliness — an
addressable **read-side lane (fork A)** problem, NOT a trunk representation-capacity wall requiring GPU curriculum (fork B).

### Per-position decay — "was it bilingual (ko+en)?" → NO, receptive-field (owner Q, `perpos_probe.py`)
Per-position recovery of A/B across the pair context "The A and the B" (real 303M):
```
pos  6–17 : A=0.80–0.88  B≈0.10   ← A FULLY recoverable at its own region (representation NOT thinned)
pos 18–19 : A=0.71→0.57  B=0.35→0.60
pos 20–23 : A=0.34→0.07  B=0.86→1.00   ← last (generation) position: A GONE, only B
```
A is fully present at its own position (0.88) then **decays** as the sequence advances — classic conv receptive-field /
causal decay. The bilingual-capacity-dilution hypothesis is **REFUTED**: A's representation is not thinned (0.88 at its
position), it simply falls outside the last position's RF (matches #42492882 "G1 = receptive-field-bound"). Language-
independent — an English-only 303M would decay identically. ⟹ the fix is NOT monolingual retraining (fork B) but a
read-side lane that pools the earlier positions (where A survives) into the generation point (fork A).

### Path (fork A · DISJOINT · read-side)
A read-side lane that **pools the full context** (which recovers both concepts, mean=0.95/0.97) and supplies both to
the generation readout — DISJOINT from the emit-drive lane (a_substrate_disjoint · G5/`ρ·tether`-gated · Ψ untouched),
wired into `.clm` v0.3 LANE block → engine-native system-G1 on frozen bars = the terminal G1 verdict. This is the
un-refuted lever the whole prior campaign missed by measuring only the last-position/additive readout.

## Honest caveats (verdict-integrity · a_scale_honest_scope)
- **DIRECTIONAL, not a G1 crack**: the task is synthetic (concept-WORD recovery from a sentence that contains the words +
  binding to ASSIGNED 5-bit codes). The true G1 generation wall is meaning-COMPOSITION into novel output; this measures a
  necessary REPRESENTATION condition, not generation. A G1 verdict requires fork A wired + system-G1 on frozen bars.
- **spelling confound**: recovery is of concept words literally in the prompt; "both recoverable" ≈ "both words linearly
  decodable from the average" — a necessary but not sufficient condition for meaning-composition.
- rung-a normalization-fragility + rung-b two-stage-probe artifact both logged; the ROBUST claims are the three findings
  above (each with its control: additive-FAIL, handed-PASS, last-vs-mean contrast).

## Consequence for the γ program (ARCHITECTURE gate-g1-recomb-gamma)
The modal Fable prediction (~85% "blind atoms / segmentation collapse → fork B GPU curriculum the only lever") is
**REFUTED**: real atoms are NOT blind (H1=1.0), the context does NOT collapse segmentation (mean recovers both). The
surviving lever is **fork A (read-side context-pooling lane)**, $0-to-cheap engineering, NOT fork B GPU curriculum.
next = implement the fork-A lane + engine-native system-G1 (the terminal G1 verdict).
