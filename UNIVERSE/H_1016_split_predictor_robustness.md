---
id: H_1016
slug: split-predictor-robustness
title: Does the H_1014 magnitude-threshold split-predictor SURVIVE at n=5, and is there a monotone DOSE-RESPONSE onset where the faithful-up / big-Phi-down split first appears as planning strength is swept?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · intervention-classifier · split-predictor · robustness · dose-response
source: H_1014 (PREDICTOR-SEPARATES QUALIFIED — a MAGNITUDE threshold on Δ cross-MIP coupling, boundary +1.4933, separates the one split intervention {planning} from the three non-split {imagination, guided, chaos} at n=4; the pre-registered DIRECTION was FALSIFIED) + H_1012 (the split itself is DISAGREEMENT-ROBUST-IN-N across n={4,5}) + PAPER/phi-measure-dependence-planning
exploration_method: E2 (extend the H_1014 intervention-SET + cross-MIP-coupling predictor pipeline to n=5 AND add a planning-strength dose-response continuum, both read off the SAME matched discretization) + E14 (substrate-native IIT4) + a_completeness_over_cheap
verification_method: W2 (pre-registered robustness + dose-response falsifier · both stdlib engines iit4/faithful_phi.hexa + iit4_bigphi.hexa at matched discretization · CPU-mirror equivalence-proof per n via H_1012 prove_mirrors_at_n BEFORE scoring) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
sister: H_1014 (the n=4 magnitude-threshold predictor), H_1012 (split robust in n {4,5}), H_1004 (clean disagreement at n=4), H_999/H_1001 (faithful_phi planning up), H_1002 (the original confounded big-Phi), PAPER/phi-measure-dependence-planning, a_phi_iit4_tool
scope: TOY n={4,5}, $0 CPU-local, real IIT-4.0 stdlib engines (CPU mirror RE-PROVEN equal to stdlib at n=4 AND n=5 per H_1012 prove_mirrors_at_n BEFORE scoring). big-Phi super-exponential — n=5 is ~slow but tractable for the SET and the depth sweep; n=6 is the honest cap (skipped, as in H_1012). a_scale_honest_scope · a_toy_scale_recheck — scale-transfer beyond n=5 UNVERIFIED. NOT a forge binary; no GPU.
verdict: PENDING-MEASUREMENT
status: pre-registered (unmeasured)
---

# H_1016 — robustness (n=5) + dose-response onset of the H_1014 split predictor

## 0. motivation
H_1014 established (QUALIFIED) that at n=4, across the intervention SET
{planning[split], imagination, guided, chaos[no-split]}, a single MAGNITUDE threshold on
the candidate predictor Δ(cross-MIP coupling) (boundary +1.4933, read off the SAME binary
discretization that feeds BOTH stdlib engines) separates the one split-inducing intervention
(planning, +2.2983) from the three non-split ones (≤+0.6883). The pre-registered DIRECTION
(split ⟺ DECREASED coupling / raised modularity) was FALSIFIED — every intervention RAISES
coupling; only magnitude separates.

Two open robustness questions remain, both extending H_1014:
1. **Robustness in n.** H_1012 showed the SPLIT ITSELF is robust across n={4,5}. Is the
   PREDICTOR's magnitude-threshold separation also robust at n=5 — i.e. re-scored at n=5,
   does the planning predictor still sit ABOVE every non-split predictor (a separating
   threshold still exists), with planning the sole split intervention?
2. **Dose-response onset.** H_1014 used a single planning strength (depth-8). Sweeping the
   planning intervention's look-ahead depth across a continuum {1,2,3,4,6,8} (depth-1 =
   greedy baseline), where does the split ONSET — the first depth at which
   sign(Δfaithful)≠sign(Δbig-Φ) appears — and does the predictor's magnitude cross its
   H_1014 boundary (+1.4933) at the SAME depth? A monotone onset (predictor rises with
   depth and the split appears once the predictor crosses the boundary) would make the
   magnitude-threshold a genuine dose-graded classifier, not an n=4/depth-8 coincidence.

## 1. hypothesis
(a) The H_1014 magnitude-threshold separation is ROBUST at n=5: re-scored at n=5 on the SAME
pipeline, planning is the sole split intervention and its Δ(cross-MIP coupling) predictor sits
strictly ABOVE every non-split intervention's predictor (a separating boundary exists).
(b) There is a MONOTONE dose-response onset: as planning depth rises 1→8, the predictor
Δ(cross-MIP coupling) rises monotonically and the faithful-up/big-Φ-down SPLIT first appears
at (or just after) the depth where the predictor crosses the H_1014 boundary +1.4933.

## 2. pre-registered falsifier (frozen 2026-06-07)
Reuse the H_1014 measurement EXACTLY (its `substrate_reads` both-engine + predictor read, its
intervention SET generators, H_1012 `prove_mirrors_at_n` equivalence proof), parametrized over n.
python3 -u, serial, $0 CPU, poll inline (NO Monitor/waiter — a_cpu_local_no_waiter).

**STEP 0 — equivalence proof.** Run H_1012 `prove_mirrors_at_n(4)` AND `prove_mirrors_at_n(5)`;
assert BOTH CPU mirrors ≡ their stdlib IIT-4.0 engines at n=4 AND n=5 BEFORE any scoring (abort
otherwise). The predictor cut-weight is a deterministic pure function of the same bits.

**PART 1 — robustness at n=5.** Re-score the SAME H_1014 SET {planning, imagination, guided,
chaos} at n=5 (30 seeds). For each: Δfaithful, Δbig-Φ, split label = sign(Δfaithful)≠sign(Δbig-Φ),
and the predictor Δ(cross-MIP coupling). Run the SAME separation test (does a single threshold
separate the split set from the no-split set?).

**PART 2 — dose-response.** Sweep planning depth d ∈ {1,2,3,4,6,8} (d=1 = greedy baseline) at
the binding n (n=4, where the full sweep × 30 seeds is tractable; n=5 reported if it completes).
At each depth d>1, contrast depth-d vs greedy(d=1): Δfaithful, Δbig-Φ, split label, and the
predictor Δ(cross-MIP coupling). Locate (i) the ONSET depth = first depth with a split, and
(ii) the depth where the predictor crosses the H_1014 boundary +1.4933; check monotonicity
(Spearman rho of predictor vs depth) and whether onset ≈ boundary-crossing.

Outcome (NO emoji token before `.verdicts/1016_split_predictor_robustness/1016.txt` exists):
  - PASS = GREEN — IFF the magnitude threshold separates planning(split) from the non-split
    set at n=5 (PART 1) AND a MONOTONE dose-response onset exists (predictor rises monotonically
    with depth, the split onsets, and onset depth coincides with / immediately follows the
    predictor crossing +1.4933) (PART 2).
  - PARTIAL = AMBER — exactly one of {n=5 separation, monotone dose-onset} holds.
  - CLOSED-NEGATIVE = RED — neither holds (the n=4/depth-8 predictor separation does NOT
    generalize in n and there is no monotone dose-onset); a_paper_negative_ok — a closed-negative
    ruling out the predictor's robustness/dose-gradation is publishable.

## 3. honest scope
big-Phi exact only at small n (super-exponential distinction + bipartition search). n=5 is slow
but tractable for the SET × 30 seeds and the n=4 depth sweep; n=6 is the honest cap (skipped, as
in H_1012). Both engines EXACT at every scored n; CPU mirror RE-PROVEN ≡ stdlib at n=4 AND n=5
BEFORE scoring (H_1012 discipline). Scale-transfer beyond n=5 UNVERIFIED. a_scale_honest_scope ·
a_toy_scale_recheck. NOT a forge binary; $0 CPU-local, no GPU. g5 CODE-measured (no LLM self-judge,
p7), a_phi_iit4_tool.

## 4. sibling / xlinks
to [H_1014](./H_1014_intervention_split_predictor.md) · [H_1012](./H_1012_bigphi_faithful_larger_n.md) ·
[H_1004](./H_1004_bigphi_faithful_clean.md) · [H_1002](./H_1002_bigphi_upgrade.md) ·
[H_999](./H_999_faithful_iit4_remeasure.md) · [H_1001](./H_1001_reopen_consolidate.md) ·
PAPER/phi-measure-dependence-planning · IIT4_PHI_TOOLS.md · a_phi_iit4_tool

## 5. measurement + finding
PENDING-MEASUREMENT — verdict raw will be written to
`.verdicts/1016_split_predictor_robustness/1016.txt` (g73 — deterministic run that COULD falsify;
both stdlib engines + CPU mirror RE-PROVEN ≡ stdlib at n=4 AND n=5 BEFORE scoring). Emoji token
assigned ONLY after that file exists.
