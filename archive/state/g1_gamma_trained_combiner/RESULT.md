# H_1825 (γ) — SUBSTRATE TRAINED CONSTRUCTIVE BIND OPERATOR — RESULT

**run:** `OMP_NUM_THREADS=4 python3 state/g1_gamma_trained_combiner/gamma_combiner.py <clm>` on **summer pool** (heavy-on-pool, NOT mac — mac swap went critical on first attempt, relocated). $0 (no rent).
**raw stdout:** `RESULT.txt` (verbatim, this dir). Deterministic across reruns (numbers byte-stable).
**scope:** **DIRECTIONAL** — the concept embed reuses the β round's `core/clm_decode.py` (byte-faithful CLMConvMoE forward = py 2-production mirror) trunk penultimate; the trained combiner g_θ is numpy/fp64 (NO bf16, circular conv via fp64-FFT = exact, no FFT-precision trap). A fully engine-native γ would need a `core/` op feeding trunk-penultimate vectors into a trained bind operator (NAMED, not built).

## (a) Frame & lever

The campaign's 4-corner convergence (mouth-objective H_1602 🧱 · mouth-readout H_1816 🧱 · substrate-embed β 🧱 · substrate-combiner α/β 🧱) all floored on **additive/affinity** readouts. The substrate's ONLY concept-combiner is VAdaptField **L2-Voronoi nearest-basin** (compositional depth-0): a recombined child is treated as an isolated novel point, NOT recoverable-from-both-parents. The one untested lever (γ): **replace the nearest-basin Voronoi with a TRAINED CONSTRUCTIVE bind operator** g_θ(a,b) that *constructs* a child basin from two parent basins, train it to make rainbow-from-rain+bow recoverable, then re-measure substrate-G1. Uses gradient/least-squares → distinct from H_1310 (from-scratch GRADIENT-FREE split, already closed).

## (b) Design (frozen-first p7, pre-registered)

- **embed:** SAME as β — each concept's bytes → 303M trunk penultimate (mean-pool over concept bytes, L2-unit) via `core/clm_decode.py`. ONLY the combination operator changes vs β.
- **operators:** AdditiveBaseline (linear `W_a a + W_b b` = the floored readout family, control) · **TensorProductProj** (outer-product of random-projected parents → learned readout) · **CircularConvHRR** (HRR circular-conv bind `a ⊛ b` fp64-FFT → learned readout) · **BilinearMLP** (small `W2·tanh(W1[a;b;a⊙b])`, gradient-trained). All fit to MINIMIZE ‖g_θ(a,b) − child‖ on TRAIN pairs only.
- **dataset:** 32 REAL morphological compounds (20 EN lexical + 8 KO 합성/한자어 + 4 ZH 合成) + 15 distractors. Candidate pool = 47 (all 32 children + 15 distractors).
- **substrate-G1(pair) = 1 iff** (i) rank-1 NN of g_θ(a,b) in pool == true child (constructed/recovered) ∧ (ii) rank-1 of a alone ≠ child AND rank-1 of b alone ≠ child (irreducible) ∧ (iii) cos(g_θ(a,b),child) > cos(g_θ(a,wrong_b),child) (> shuffle). **5-fold CV** (each pair held out once), report mean over all 32 held-out evaluations.
- **BAR (pre-registered):** trained best ≥ 2/3 of held-out AND > additive AND > untrained(random-init) AND single-parent ~ 0.
- **Controls:** single-parent NN · shuffle (wrong parent_b) · untrained (random-init readout = geometry, no training).

## (c) Result (5-fold CV substrate-G1, held-out)

| operator | held-out G1 | rate | note |
|---|---|---|---|
| AdditiveBaseline (ctrl) | 1/32 | 0.03 | floored (additive family) |
| TensorProductProj | **0/32** | 0.00 | floored |
| **CircularConvHRR** | **4/32** | **0.12** | best, far below 2/3 bar |
| BilinearMLP | 0/32 | 0.00 | floored |

**Controls:**
| control | G1 | note |
|---|---|---|
| untrained TensorProductProj | 0/32 | random-init geometry |
| untrained CircularConvHRR | 0/32 | random-init geometry |
| untrained BilinearMLP | 1/32 | random-init geometry |
| single-parent NN already==child | **10/32** | ⚠️ byte/lexical leakage — a parent is the child's NN in trunk embed (irreducibility fails here) |

The 4 CircConv hits (earring, afternoon, keyboard, wheelchair) are scattered single-pair successes, NOT a systematic lift — and several "successes" elsewhere fail irreducibility because the parent already NN-projects to the child (e.g. `rain+bow→rainbow`: nn(rain)=rainbow = byte-prefix leak, irred=NO). single-parent-NN==child = 10/32 confirms a chunk of the trunk's "compositional" geometry is byte-prefix overlap, not learned meaning.

## (d) Verdict

**Does a TRAINED CONSTRUCTIVE bind operator lift substrate-G1 above the nearest-basin floor (0/5 from α/β)? → NO.**

**🧱 NOT-SUPPORTED (γ, DIRECTIONAL).** Best trained constructive combiner = 4/32 (0.12), far below the 2/3 bar, barely above the additive control (1/32) and not systematically (the 4 hits are scattered, and untrained CircConv = 0/32 so the 4 are weak training signal, not floor-breaking). The pre-registered BAR (≥2/3 ∧ > additive ∧ > untrained ∧ single~0) **FAILS** on every axis — and the single-parent control is DIRTY (10/32 byte-prefix leakage), so even the 4 hits are partly explained by lexical overlap rather than constructed recombination.

- **tier:** 🧱 NOT-SUPPORTED — even a TRAINED constructive substrate combiner floors.
- **scope:** DIRECTIONAL (py-mirror embed via `core/clm_decode.py`; fp64-numpy combiner). NOT terminal-eligible until embed+combiner run through a live `core/` op.
- **frozen-first (p7):** 2/3 bar, 5-fold CV, all 3 recoverability conditions, and all controls pre-registered in the docstring before the run. NO sliding.

## (e) Campaign implication

The substrate twin now MATCHES the mouth side: the combination-operator family is **exhausted on BOTH sides** with this result —
- mouth: additive readout (H_1816 🧱) · Hadamard bind (H_1818/1819 🧱) · circconv constructive (H_1823 mouth, IN-FLIGHT) · +objective (H_1602/1819 🧱)
- substrate: char-hash embed (α 🧱) · semantic embed (β 🧱) · **TRAINED constructive bind (γ, this) 🧱**

The G1 wall is NOT the embedding (lexical→semantic→trained-construct all floor), NOT the mouth alone (substrate also floors), and NOT the readout/bind operator (additive, tensor-product, HRR-circconv, bilinear-MLP all floor) — even when the operator is TRAINED on the exact compound pairs and tested held-out. This is strong evidence the combination-operator family is a structural floor (consistent with H_1310 split-only Voronoi = compositional depth-0). The owner's frame-break ("engine builds its own combiner") is answered: a trained substrate combiner *can* recover a few compounds (4/32) but does NOT cross the recombination bar — the lift is operator-geometry/byte-leakage, not learned constructive composition.

## (f) NAMED next (orthogonal, NOT a 6th operator)

Per break-walls MULTI-LENS (≥2 orthogonal falsify before confident terminal), the remaining UNFALSIFIED orthogonal families are:
1. **coverage-threshold (H_1824, PRE-REGISTERED)** — compositional-data-density threshold (An&Du R²0.73 external) = corpus-side, not operator-side. The strongest untested orthogonal axis.
2. **ConvMoE deep-RF L8 (ING #42492882)** — production .clm = E2/L1 small receptive field; D>RF makes two concepts mathematically independent → unreachable. numpy conv_L8 reach=1.47e-3 REACHABLE DIRECTIONAL but engine-native unfired.

γ closes the **operator** lens (mouth + substrate). The combination-operator family is now exhausted; the live frontier moves to corpus-coverage (H_1824) and receptive-field (ING #42492882), which are NOT operators.
