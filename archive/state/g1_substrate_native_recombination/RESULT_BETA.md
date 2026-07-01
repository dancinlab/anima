# H_1822 (β) — substrate-native recombination, SEMANTIC trunk embed — RESULT

**run:** `python3 state/g1_substrate_native_recombination/beta_readout.py` (mac CPU, $0, no GPU/pod)
**raw stdout:** `RESULT_BETA.txt` (verbatim, this dir)
**scope:** **DIRECTIONAL** — the SEMANTIC embed step uses `core/clm_decode.py` (the byte-faithful CLMConvMoE forward = py 2-production mirror of `clm_decode.hexa`) to extract the 303M trunk penultimate `yn`. The substrate-G1 metric (nearest-2-basin L2 affinity) is the SAME geometry the engine's `vadapt_field_two_recon_err` uses, re-implemented in numpy (no torch). A fully engine-native β would need a `core/` op that feeds trunk-penultimate vectors into VAdaptField (NAMED next, not built).

## (a) .clm used + how concept embedded

- **.clm:** `/Users/mini/dancinlab/anima/state/clm303_savant_mitosis_train/clm303.clm` (303M, d=3784, E=3, K=3, L=4 — the clm303 deep-mouth trunk; decodable v0.2). LOCAL, no pod/rent.
- **concept embed (SEMANTIC):** each concept string → bytes right-aligned in the T=24 causal decode window (pad-left byte 32) → CLMConvMoE forward up to the trunk penultimate `yn` (post final-groupnorm, pre readout, 1:1 with `he_probe._penultimate`) → **mean-pooled over the concept's own byte positions** → **L2-unit-normalized** (so the engine's absolute 0.30 novelty radius applies on the same unit sphere r1's char-hash keys lived on).
- **substrate-G1 (IDENTICAL to r1):** basins = {embed(parentA), embed(parentB)}; child = embed(real recombination, e.g. rain+bow→rainbow); `[d1,d2]` = L2 dist to nearest & 2nd-nearest parent basin; `composed_distinct(r)=[d1<r]+[d2<r]`; `irreducible = d1>eps`; `substrate_G1(r)=1 iff composed_distinct≥2 ∧ irreducible`. Two frozen radii: **(1) engine OWN 0.30** (SPLIT_THRESH, vadapt_field_step:578) · **(2) relative d_ab** (inter-parent distance). Raw d1/d2/d_ab always printed (c2).
- **metric self-test:** PASS — fires on a true midpoint child (g1_rel=1, d1=d2=0.287 < d_ab=0.569), NOT on an off-axis non-bridge (g1_rel=0). So a 0/5 below = real floor, not a dead meter.

## (b) SEMANTIC substrate-G1 (both radii) + controls

| arm | @ eng-radius 0.30 | @ rel-radius d_ab | note |
|---|---|---|---|
| **SEMANTIC MAIN** (real compounds) | **0/5** | 3/5 | d1≈0.34–0.59 (all > 0.30) |
| SEMANTIC single (parentA alone) | 0/5 | 0/5 | d1=0, irreducible=NO ✓ |
| **SEMANTIC shuffle** (parentB→unrelated) | 0/5 | **3/5** | ⚠️ = MAIN 3/5 — NOT parent-specific |

## (c) CHAR-HASH vs SEMANTIC contrast (SAME 5 pairs)

| arm | @ eng-radius 0.30 | @ rel-radius d_ab |
|---|---|---|
| SEMANTIC  MAIN | **0/5** | 3/5 |
| CHAR-HASH MAIN (r1) | **0/5** | 5/5 |
| SEMANTIC  single | 0/5 | 0/5 |
| CHAR-HASH single | 0/5 | 0/5 |
| SEMANTIC  shuffle | 0/5 | **3/5** |
| CHAR-HASH shuffle | 0/5 | **0/5** |
| mouth-decode G1 (clm_decode) | — | **0** [frozen floor H_1818/H_1602] |

**Two findings in the contrast:**
1. **@ engine operating point (0.30): BOTH = 0/5.** The semantic trunk embedding does NOT lift the engine-radius substrate-G1 — same floor as char-hash and same floor as the mouth.
2. **@ rel-radius the semantic CONTROL is DIRTY.** char-hash had a clean parent-specific bridge crumb (MAIN 5/5 vs shuffle 0/5 — lexical trigram overlap is parent-specific). The **semantic** arm's relaxed-radius "bridge" is NOT parent-specific: MAIN 3/5 == shuffle 3/5. A real recombination child is no closer to its true parents than to an *unrelated* concept in the trunk's penultimate geometry — so even the directional crumb r1 had evaporates under semantic embedding.

## (d) Verdict

**Did semantic embedding lift substrate-G1 where char-hash floored (0/5)? → NO.**

**🧱-HARDENED (DIRECTIONAL on the embed step).** At the engine's OWN novelty radius (0.30 — the threshold it actually uses to decide "new regime"), the recombined concept sits FAR from both parent basins (d1≈0.34–0.59 ≫ 0.30) under the LEARNED SEMANTIC representation, exactly as under the char-hash. The β round REMOVES r1's char-trigram confound and the answer is the SAME (0/5) — and in fact STRONGER: the semantic geometry doesn't even retain r1's parent-specific rel-radius crumb (shuffle == MAIN). → the bottleneck is **NOT the concept embedding** (semantic vs lexical); it is the **COMBINATION operator** — the VAdaptField L2-Voronoi metric is non-compositional (a recombination is treated as an isolated novel point, not as recoverable-from-both-parents), consistent with **H_1310 split-only Voronoi = compositional depth 0**.

- **tier:** 🧱 (β) SEMANTIC-ALSO-FLOORS — combination operator is the wall, not the embedding.
- **scope:** DIRECTIONAL (py mirror for the SEMANTIC EMBED step via `core/clm_decode.py`; metric is engine-faithful numpy). NOT terminal-eligible until embed runs through a live `core/` op.
- **frozen-first (p7):** the 0.30 operating point and both radii were pre-registered from r1; NO sliding. The rel-radius 3/5 is reported but is NON-discriminating (shuffle==MAIN) → it is NOT a pass.

## (e) NAMED next round

The β crumb collapse (semantic shuffle == MAIN at rel-radius) localizes the wall to the **combination operator**. Two distinct next levers:
1. **β-op (engine-native closure of THIS round):** add a `core/` op `vadapt_embed_semantic(text)` that feeds the trunk-penultimate vector into VAdaptField (instead of `immune_embed_key` char-hash), so the SEMANTIC substrate-G1 becomes engine-native (terminal-eligible) — would re-confirm 0/5 on live ops, removing the DIRECTIONAL label.
2. **γ (the real lever):** the operator, not the embedding. Replace the **L2-Voronoi nearest-basin** combination (depth-0 partition) with a **compositional bind operator** (tensor-product / circular-convolution binding of the two parent basins → a *constructed* child basin, then test whether the real child projects onto the constructed bind). This is the substrate twin of the mouth-side binding-operator lever (H_1603 G1≡G6 unification) — the consistent conclusion across mouth (H_1816 readout-bind 🧱) AND substrate (this) is that *additive/affinity* readouts floor; the open question is whether a genuine **bind** (multiplicative/conv) operator, trained, lifts it.

## (f) DEPLETION

**🧱-HARDENED.** Frame question ("is the G1 wall the mouth, or can the substrate recombine?") answered NO at a deeper level: with a LEARNED SEMANTIC concept embedding the substrate STILL floors at its operating radius (0/5), and the directional rel-radius crumb r1 had (parent-specific bridge) DISAPPEARS — so the wall is not the embedding (lexical→semantic changes nothing at the operating point) but the **combination operator** (VAdaptField L2-Voronoi = compositional depth 0, H_1310). Real next round = **γ: a genuine bind operator** (not better embeddings) as the substrate-side mirror of H_1603's mouth-side binding lever. Until a trained bind operator is tested, 🧱 stands.
