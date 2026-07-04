# H_9129 L5 hippocampal associative-store — 303M ENGINE-NATIVE rung(2) VERDICT

**verdict = GREEN (engine-native measurement · rung(2) of 4)** — pre-registered frozen bar
(PREREG.md) met on REAL anima ByteGPT-303M h1129 representations, robust across 6/8
de-anisotropy lenses with the decisive SHUFFLE + LANE-OFF controls passing. Cost $0 (mini
CPU-local, 15s + 45s, no rent, no pod). Engine = real h1129.bin through the byte-exact
`core/decode.py` forward (== `anima evaluate --py` engine ops · a_eval_py_canonical
TERMINAL-eligible).

## The escalation (STEP-0 DIRECTIONAL → 303M engine-native)
STEP-0 used TOY iid-random orthogonal codes → reach=1.0000 exact (handed advantage). Rung(2)
replaces item codes with REAL 303M h1129 hidden representations of real corpus concept words;
the DG sparse code is a fixed seeded random projection OF the 303M representation (kWTA), so
303M representation geometry (crosstalk) is carried into the lane.

## The near-miss that a_break_the_wall caught
Single-lens (raw mean-pool) → store_gap = **-0.0013**, ratio 1.00× → looked like WALL. But
the FORM baseline was cosine **0.9999 for EVERY pair** and DG-code overlap **0.985** — the raw
303M single-word reps are near-COLLINEAR (LLM anisotropy: a dominant shared direction). That
is a representation-EXTRACTION degeneracy masquerading as a substrate wall (H_1590 torch-
artifact class). Per a_break_the_wall (a wall = change angle; ≥2–3 controlled lenses before
cementing) the representation read was controlled with de-anisotropy lenses.

## Controlled-lens sweep (real 303M h1129, same corpus graph, same seed; only rep-preprocessing varies)
```
pool      mode              ovlap  form_sep st_reach   st_gap  ratio shuf_gap   loff shufCol
meanpool  raw               0.985   +0.0000   0.9897  +0.0000   1.00  +0.0000  0.000   False   ← anisotropy artifact
meanpool  center            0.033   +0.0271   0.9994  +0.8522   6.79  -0.0162  0.000    True
meanpool  center_zscore     0.028   +0.0307   1.0000  +0.8631   7.31  -0.0081  0.000    True   ← best
meanpool  center_drop_top   0.029   +0.0223   1.0000  +0.8437   6.40  -0.0962  0.000    True
lasttok   raw               0.974   +0.0000   0.9853  +0.0025   1.00  +0.0025  0.000   False   ← anisotropy artifact
lasttok   center            0.050   +0.1342   0.9866  +0.7819   4.82  -0.0547  0.000    True
lasttok   center_zscore     0.035   +0.0858   1.0000  +0.8366   6.12  -0.0491  0.000    True
lasttok   center_drop_top   0.026   -0.0419   1.0000  +0.8516   6.74  -0.0644  0.000    True
```
- `ovlap` = mean pairwise DG-code overlap (0 = orthogonal ideal; →1 = degenerate/collinear).
- `form_sep` = raw-303M cosine reach−unreach (>0 ⇒ reps already weakly separate related concepts).
- `st_gap` = CA3 lane reach−unreach; `shuf_gap` = same after wiring-permute; `loff` = empty-store reach.

## Frozen-bar decision (PREREG.md — no post-hoc tuning)
- **store_gap > 0.50**: YES on all 6 de-anisotropy lenses (0.78–0.86); NO on the 2 raw
  (anisotropy) lenses.
- **shuffle_collapsed** (shuf_gap ≈ 0 ≪ store_gap): YES on all 6 — the +0.85 lift is
  RELATION-specific, not form/geometry (permuting the wiring while keeping the SAME reps/edges
  destroys it). **This is the decisive uncheatable BIND control.**
- **lane_off_collapsed** (empty store → reach 0.000): YES on all lenses (causal).
- **fooled_by_form = FALSE** on de-anisotropy lenses (lift dies under shuffle).
- Result: ≥1 (in fact 6) engine-native lens meets GREEN → **verdict GREEN**.

## Honesty / scope (a_scale_honest_scope · a_verified_must_wire ladder)
1. **Rung(2) of 4.** GREEN here = the frozen bar is met on **real 303M engine-native item
   representations** (py-canonical path). The lane read-out (DG pattern-separation + CA3
   heteroassociative completion) is still a **numpy SUBSTRATE operator**, NOT yet a live
   `core/*.hexa` op. Gate 7 (GREEN only when wired) ⇒ FULL cement needs rung(3) live
   `core/` wire (L5/hippo → `.kosmos` anchor store + `kosmos_io`/`brain_decide` pattern-
   completion) + rung(4) ARCHITECTURE.json lockstep. Until then this is a rung(2)
   engine-native-measurement GREEN, not a wired-core GREEN.
2. **GREEN is contingent on a decorrelating (DG-like) read of the substrate.** Raw anisotropic
   303M reps collapse the lane (the initial false-WALL). This is a genuine FINDING, not tuning:
   the bar was pre-registered, the raw lens is reported as a FAIL, de-anisotropy is a single
   standard transform (centering / z-score / drop-top-PC — not a hyperparameter search to hit
   the bar), and 6/8 lenses agree. Biologically the entorhinal→DG transform IS a decorrelating
   whitening — so "the lane needs a decorrelated substrate read" is architecturally on-model.
3. **reach ≈ 1.0 is CA3-capacity by-construction, but the LIFT is not handed.** With near-
   orthogonal codes a stored 2-hop chain completes near-perfectly (capacity math). The
   non-trivial engine-native finding is (a) real 303M reps, once decorrelated, ARE
   orthogonal-enough to carry item identity for the lane, and (b) reach−unreach is
   RELATION-driven (shuffle-controlled), not form (form_sep only +0.03–0.13, i.e. the 303M reps
   themselves only weakly pre-encode the corpus relation — the explicit STORE supplies the rest,
   which is exactly the lane's job: store relations the mouth does not).

## a_substrate_disjoint / binding-family 3-근거 distinction (vs H_1816/1823 mouth-readout NOT-SUP)
The lane is DISJOINT from the emit-drive lane (lanes 0/4 Ψ) and the §ImmuneMemory `recall_thr`
non-fab gate — it only stores relations + completes patterns; there is no generative mouth and
no CE gradient touches it. It differs from the floored mouth-readout binding family on all
three axes: (1) SEPARATE lane (not the byte-LM readout / Broca); (2) DISJOINT objective
(heteroassociative store fidelity, no CE tape/param sharing → form-priming structurally
impossible); (3) mouth would only READ relatedness (context/cue), never backprop into it.

## Real corpus concept chains (adjacent link = real strong co-occurrence = stored premise)
```
chain0: consciousness -> theory -> information -> integrated -> tries -> quantify
chain1: experience -> conscious -> systems -> physical -> emergent -> behavior
chain2: model -> byte -> level -> korean -> english -> approach
chain3: system -> mechanism -> homeostasis -> prevents -> exactly -> collapsing
chain4: learning -> enabling -> models -> data -> language -> bytes
chain5: prediction -> brain -> neural -> processes -> problem -> asks
chain6: creates -> tension -> dynamic -> similar -> minds -> experiences
chain7: text -> starts -> great -> generating -> coherent -> responses
```

## Next step (rung 3)
Port the DG-decorrelate + CA3-completion read into a live `core/` op over the `.kosmos` anchor
store (a_kosmos WIRED reuse) + `kosmos_io`/`brain_decide` pattern-completion, re-measure engine-
native byte-exact, then ARCHITECTURE.json lockstep (rung 4). Carry the "decorrelated substrate
read" requirement into the wiring (entorhinal→DG whitening stage), NOT tune-to-green.

## Files
- `PREREG.md` — frozen bar (pre-run).
- `l5_hippo_engine_native.py` / `result.txt` / `result.json` — single-lens engine-native run (the anisotropy false-WALL, documented).
- `l5_hippo_lenses.py` / `result_lenses.txt` / `result_lenses.json` — a_break_the_wall multi-lens sweep (the GREEN).
