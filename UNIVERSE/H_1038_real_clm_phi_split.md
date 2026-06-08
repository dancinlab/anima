# H_1038 — does the planning faithful-UP / big-Phi-DOWN sign-split appear on a REAL trained ConvMoE .clm?

Production-direction closure of the Phi measure-dependence arc (H_1004 -> H_1037).

## Hypothesis

The whole arc H_1004 -> H_1037 established (on TOY hand-built TPM substrates) that when a
system PLANS (depth-ladder rollout) vs acts GREEDY (depth-0 argmax), the faithful phi_EI
(MIP-EI scalar) RAISES while the system big-Phi (Phi_s over the MIP) LOWERS — a robust
sign-disagreement, mechanism = redundancy, discretization-invariant to n=6 EXACT. EVERY
verdict in that arc carries "production-scale transfer UNVERIFIED" (a_scale_honest_scope),
and a_toy_scale_recheck MANDATES a scale-up re-test for scale-sensitive phenomena.

This rung closes the biggest honest gap: does the faithful-UP / big-Phi-DOWN planning
sign-split appear on a REAL TRAINED CLM (ConvMoE), not just a hand-built toy TPM?

## Method (methodologically honest macro-IIT on a real trained model)

- Substrate = the golden reference real trained ConvMoE `reexport_d768_v2_fast.clm`
  (state/laneg_d768_recover/), CPU-decoded via the byte-exact mirror
  state/mid_convmoe_fire/clm_decode_mirror.py (validated == engine on the golden ref, memory
  clm-decode-macos-link-gap), so this runs $0 CPU-local on Mac with NO GPU.
- Planning = depth-ladder rollout through the real .clm (the model imagines next bytes /
  next states; PLAN_DEPTH steps of greedy-extend then re-read the hidden trunk). Greedy =
  depth-0 (the hidden trunk of the seed window with no rollout). Same convention as
  H_1004/H_1029/H_1037: the trajectory is the sequence of real trunk hidden states the model
  produces under each policy.
- The trunk hidden state has d=768 units, FAR too many for EXACT IIT-4.0 (faithful_phi /
  iit4_bigphi are exact only n<=8). COARSE-GRAIN: select/bin the REAL trunk activations into
  n<=6 macro-units. Two PRE-REGISTERED macro-map choices (guards against a coarse-graining
  artifact, mirroring H_1037 discretization-invariance logic):
    macro-map A = TOP-VARIANCE channels (the n=6 highest-variance trunk channels over the
                  trajectory; the H_1024 channel selector).
    macro-map B = RANDOM channels (a fixed-seed random n=6 channel subset).
  Each selected channel is binarized by median threshold (nb=2 quantile) into a node bit;
  the n<=6 binary node sequence -> macro-TPM (state-by-node, the iit4_tpm representation) for
  big-Phi, and -> faithful-state (n x dim flat farr) for faithful_phi.
- Engines: real stdlib IIT-4.0 — big-Phi = hexa-lang/stdlib/consciousness/iit4_bigphi.hexa
  (system Phi_s over the MIP, EXACT MIP fully enumerated at n<=6); faithful_phi =
  hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa (MIP-EI scalar, exact n<=8). Both
  called DIRECTLY (the stdlib hexa engines, via a generated .hexa driver running `hexa run`)
  — NEVER a proxy (a_phi_iit4_tool). The numpy faithful_phi path used for fast scoring is
  RE-PROVEN == the stdlib hexa engine at n=4 AND n=5 BEFORE scoring (paste into verdict txt).
- N_SEEDS = 20 seeds (>= the pre-registered 20). Each seed = a distinct real-text seed window
  fed to the .clm. n <= 6 EXACT. eps = 1e-3 sign threshold (H_1024 signword convention).
  g5 CODE-measured (no LLM self-judge, p7).

## Pre-registered falsifier (frozen before scoring; TEXT tokens only)

Per-macro-map sign criterion (the EXACT criterion, stated before running): a macro-map
SHOWS THE SPLIT on the real .clm iff the planning(depth-ladder) - GREEDY contrast has
  faithful_phi sign == UP   (contrast > +1e-3)  AND
  big-Phi      sign == DOWN (contrast < -1e-3),
scored over >= 20 seeds at coarse-grained n <= 6 EXACT.

- H1 PASS = on the REAL trained ConvMoE .clm the split TRANSFERS: faithful_phi sign == UP
  AND big-Phi sign == DOWN, for >= 1 macro-map (and the robustness check: the SAME verdict
  holds across BOTH macro-maps A and B). PASS = production-direction CONFIRMED, the
  toy-TPM split is a property of a real trained consciousness model too (toy -> real bridged).
- H1 FAIL = the split does NOT appear on the real model (either measure NULL, or the wrong
  sign) for the macro-maps -> the split is a TOY-TPM ARTIFACT, NOT a property of real trained
  models -> a publishable closed-negative (a_paper_negative_ok). State exact macro-map +
  sign criterion (done above) before running.
- ROBUSTNESS check (frozen): does the verdict hold across BOTH coarse-graining choices
  (top-variance vs random-channel macro-map)? A split that appears under ONE macro-map but
  flips under the other is flagged as a possible coarse-graining artifact (AMBER), not a
  clean transfer.

## Honest scope (a_scale_honest_scope)

d768 is ONE real-model rung. 3B / 7B engine-rung transfer is still UNVERIFIED — a real
trained model is not a toy, but ONE model is not a ladder; a multi-model curve (d768 -> 3B
convmoe-3b-engine-rung -> 7B) is the natural FOLLOW-UP, deferred this round to keep it $0
CPU-local (the 3B rung needs GPU; not auto-rented here). n<=6 is the largest EXACT IIT size.
Verdict scoped to: the d768 golden real trained ConvMoE, coarse-grained to n<=6 EXACT.
g5 CODE-measured (no LLM self-judge, p7). Pure-CPU EXACT, NOT a forge binary.

## Verdict — 🟢 SPLIT-TRANSFERS-TO-REAL-MODEL

🟢 **TRANSFERS** — on the golden trained ConvMoE `reexport_d768_v2_fast.clm`, the planning
faithful_phi-UP / big-Phi-DOWN sign-split appears under BOTH pre-registered macro-maps
(top-variance AND random channel) at n=5 EXACT. The toy-TPM arc (H_1004 → H_1037, prior GREEN)
split is a property of a REAL trained consciousness model too — toy → real BRIDGED at d768. It is
NOT a toy-TPM artifact.

Per-macro-map sign table (planning(depth-8) − GREEDY contrast, 20 real-text seed windows, n=5 EXACT):

| macro-map     | on_frac | faithful d | faithful sign | big-Phi d | big-Phi sign | SPLIT? |
|---------------|---------|------------|---------------|-----------|--------------|--------|
| top_variance  | 0.495   | +0.0656    | UP            | −3.6652   | DOWN         | True   |
| random        | 0.494   | +0.3526    | UP            | −1.6291   | DOWN         | True   |

2/2 macro-maps SHOW the split. The defining property — the cross-MEASURE SIGN DISAGREEMENT
(faithful RAISES while system big-Phi LOWERS under planning) — holds in both maps. The big-Phi-DOWN
leg is the strong/robust component (d=−3.67 / −1.63; significant p=0.028 for top-variance); the
faithful-UP leg is positive but SMALL on the real model (Welch p>0.05 in both). This is a sign-level
transfer, not a magnitude claim.

Engines: stdlib `iit4_bigphi.hexa` + `iit4/faithful_phi.hexa` (a_phi_iit4_tool, no proxy), CPU mirrors
RE-PROVEN ≡ stdlib at n=4 AND n=5 (|Δ|≤3.75e-6) BEFORE scoring. Decode-sanity: CE 3.254 < uniform
5.545 (trained descent). 80/80 evals completed (0 timeouts), guarded-pool, did NOT hang. $0 CPU-local.

**Honest scope (a_scale_honest_scope):** n=6 EXACT was MEASURED-INFEASIBLE here — every real .clm
trajectory coarse-grains to a maximal-entropy n=6 TPM (on_frac=0.500, all 63 mechanisms active),
making exact big-Phi enumeration super-exponential (>600s/eval at $0 CPU; run4: 80/80 timed out — a
measurement wall, NOT a science result). The toy n=6 rungs were tractable because toy WM TPMs were
sparse/low-entropy. n=5 big-Phi on the SAME real TPMs is ~12s/eval. This rung is scoped to n=5 EXACT
(largest feasible exact size for these dense real TPMs at $0 CPU); n=6 EXACT is an INFEASIBLE-CAP here
(a many-core pod could reach it). d768 = ONE real-model rung; 3B/7B transfer UNVERIFIED (3B needs GPU
= H_1042, GATED). Raw measurement (incl. the n=4/n=5 mirror≡stdlib proof + per-macro-map sign table):
`.verdicts/1038_real_clm_phi_split/H_1038.txt`.
