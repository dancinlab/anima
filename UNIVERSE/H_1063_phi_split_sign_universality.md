# H_1063 — phi-split-sign-universality (PRE-REGISTRATION)

**Status:** PRE-REGISTERED (falsifier + FROZEN thresholds locked BEFORE scoring). TEXT-only until `.verdicts/1063_phi_split_sign_universality/H_1063.txt` lands.

## Lineage / puzzle
- [[h1039-redundancy-causal]] H_1039 (REDUNDANCY-CAUSAL, PASS): Williams-Beer redundancy causally drives the *planning* Phi-sign-split (de-redundify ZCA/GS collapses it on planning; control: faith +2.33 / big -4.01).
- [[h1062-redundancy-universality]] H_1062 (SPLIT-IS-PLANNING-SPECIFIC, closed-neg): the CAUSAL mechanism (clean ZCA-removable redundancy) is planning-specific — de-redundify collapses the split ONLY for planning. YET the split direction still rank-generalized across non-planning interventions (cross-IV Spearman rho=+0.80 on |Dred|->split-magnitude).
- Open puzzle H_1062 surfaced: WHY does the split DIRECTION generalize when the cleanly-removable-redundancy MECHANISM does not?

## Synthesis hypothesis
The SIGN of the split is a UNIVERSAL measure-theoretic property: faithful phi_EI and big-Phi have OPPOSITE monotone responses to ANY increase in within-block correlation, independent of whether that correlation forms a surgically-removable block — while only the MAGNITUDE/causality (clean ZCA-removable redundancy) is substrate-specific. This would unify H_1039 (causal, planning) + H_1062 (direction generalizes).

## Design (parametric — decouple SIGN from removability)
A GRADED within-block correlation sweep on the H_1039/H_1062 toy channel substrate (the EXACT `_top_variance_channels(H_greedy, 4)`, 40x4 continuous matrix, GREEDY baseline). A single tunable knob:

```
rho_corr in {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}
```

Shared-latent / Gaussian-copula mixing (NOT a planning intervention, NOT a clean block):
For each channel j, mix it toward a SINGLE shared latent factor z (the row-mean of the z-scored channels — a diffuse common-mode direction), preserving each channel's own std:
```
Xz   = zscore(X)                       # per-channel z-score (T x k)
z    = mean over channels of Xz        # shared latent (T,)  — DIFFUSE common mode
Xr_j = sqrt(1-rho)*Xz_j + sqrt(rho)*z  # convex-in-variance loading (within-block corr UP monotone in rho)
Xr_j <- Xr_j*sigma_orig_j + mu_orig_j  # restore original per-channel scale (signal preserved)
```
This raises pairwise within-block channel correlation monotonically in rho in a CONTROLLED way; the induced redundancy is DIFFUSE (rank-1 shared common mode spread across all channels) — it need NOT be cleanly ZCA-removable, which is exactly the removability-resistant regime we need.

At each rho_corr level, compute faithful phi_EI AND big-Phi (stdlib EXACT n<=5, NO proxy) vs the rho_corr=0 baseline, 30 seeds, paired-by-seed. Contrast = mean(reads@rho) - mean(reads@rho=0).

## Tests
- (a) Opposite-monotone SIGN over the FULL sweep: does faithful phi_EI rise monotonically with rho_corr WHILE big-Phi falls monotonically — Spearman over the 10-point sweep, opposite signs.
- (b) Removability-resistant check: does this opposite-monotone SIGN hold EVEN where the induced redundancy is diffuse / NOT ZCA-removable (de-redundify does NOT collapse it)? Measured via the WB redundancy that survives ZCA at high rho + whether the sign of the (faith,big) contrast SURVIVES the ZCA de-redundify on the high-rho channels.
- (c) Saturation/reversal bound: at what rho_corr does each measure's response saturate or reverse, if ever (per-step monotone direction table).

## FALSIFIER (FROZEN — NO goalpost move)
- SIGN_EPS = 1e-3 (sign-eps, inherited from H_1039/H_1062).
- MONO_BAR = 0.9 (Spearman |rho| over the sweep).
- N_SEEDS = 30; rho_corr grid = {0.0...0.9} step 0.1 (10 levels).
- RED_REDUCTION_THRESHOLD = 0.20 (H_1039 ZCA >=80% cut definition; used to label removability of the induced redundancy at high rho).

H1-SIGN-UNIVERSAL (PASS): faithful phi_EI is monotone-INCREASING (Spearman rho_s(rho_corr, faith_contrast) >= +0.9) AND big-Phi is monotone-DECREASING (Spearman rho_s(rho_corr, big_contrast) <= -0.9) over the FULL sweep (opposite signs, both |rho_s|>=0.9) AND the opposite-monotone SIGN holds in the de-redundify-RESISTANT regime (the sign of the faith-UP / big-DOWN split at the highest rho_corr SURVIVES ZCA de-redundify, i.e. ZCA does NOT collapse the high-rho sign even though it removes part of the diffuse redundancy) -> the split SIGN is a UNIVERSAL measure-property, removability-INDEPENDENT.

FAIL (closed-negative, a_paper_negative_ok): the two measures do NOT have robust opposite-monotone responses (same-sign, non-monotone, |rho_s|<0.9 for either, OR the opposite-response VANISHES once redundancy is non-removable / ZCA collapses the high-rho sign) -> sign is NOT a clean universal property. Bounds the unification. Report both Spearmans + the saturation curve + the de-redundify-resistant check either way.

## Constraints
- a_phi_iit4_tool: faithful phi_EI + big-Phi via stdlib EXACT n<=5, NEVER a proxy; RE-PROVE python mirror == stdlib EXACT 6dp at n=4 AND n=5 (paste both). BITS/log2 MI=H(A)+H(B)-H(A,B) (H_1043 nats-bug lesson). WB redundancy = validation variable, NOT a Phi proxy (H_1039 lesson).
- REUSE H_1039/H_1062 substrate + ZCA de-redundify operator + H_1012 mirror-prover UNMODIFIED. Confirm reproduce-anchor (H_1039 planning split control faith +2.33 / big -4.01) BEFORE scoring the sweep.
- p3/p6/p7: generic toy channel substrate, no persona. TOY n<=5, NO GPU/pod. real-module import; SERIAL only; `if __name__`-guard. 30 seeds, FROZEN thresholds.
- a_scale_honest_scope: toy n<=5 rung; scale UNVERIFIED. g5/p7. $0 CPU-local.

## Artifacts
- harness: `UNIVERSE/h1063_phi_split_sign_universality.py`
- verdict: `.verdicts/1063_phi_split_sign_universality/H_1063.txt`
- result JSON: `UNIVERSE/h1063_phi_split_sign_universality_result.json`
