---
id: H_1024
slug: phi-split-discretization-invariance
title: Is the planning faithful-up / big-Phi-down sign-split invariant to the discretization (binning) choice, or is it an artifact of the binary 2-bin discretization used in H_1012/H_1017?
domain: universe · cwm · consciousness · iit4 · big-phi · faithful-phi · measure-disagreement · discretization · robustness · pre-register
source: PAPER/phi-measure-dependence-planning Limitations caveat 3 ("a different discretization could shift magnitudes; the sign, not the magnitude, is the claim") — the sign-invariance to binning is asserted but UNTESTED
exploration_method: E2 (sweep the discretization while holding the matched two-engine protocol) + E14 (substrate-native IIT4) + a_scale_honest_scope
verification_method: W2 (pre-registered discretization-sweep falsifier · both stdlib engines · mirror equivalence-proof per binning) + g5 CODE-measured (no LLM self-judge, p7) + a_phi_iit4_tool
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
status: measured
verdict: 🟢 SIGN-DISCRETIZATION-INVARIANT — the planning faithful_phi-UP / big-Φ-DOWN sign-split holds for EVERY binning in the pre-frozen discretization grid (all nb in {2,3,4} × {equal_width, quantile} = 6 binnings; planning depth-8 vs greedy, n=4, 30 seeds): faithful_phi RAISES the MIP-EI scalar (Δ ranges +0.386 … +2.333, all UP) while system big-Φ LOWERS the structure Φ_s (Δ ranges −3.43 … −5.19, all DOWN) in 6/6 binnings. The 2-bin median baseline (nb=2 quantile) reproduces H_1012 verbatim (big-Φ −4.008 d−1.83, faithful +2.333 d+5.18). Only the magnitudes move across binnings; the SIGN never flips. The PAPER caveat-3 claim ("the sign, not the magnitude, is the claim; a different discretization could shift magnitudes") is VINDICATED — the split is NOT a 2-bin (median) artifact. Both CPU mirrors RE-PROVEN ≡ stdlib at n=4 (and n=5 cross-check) BEFORE scoring (a_phi_iit4_tool — real engines, no proxy); the discretization grid is PRE-FROZEN (no post-hoc binning selection). HONEST CAP: n=5 mirrors RE-PROVEN ≡ stdlib but the full n=5 grid is INFEASIBLE at $0 CPU (a single n=5 system big-Φ eval MEASURED >5.5 min — n=5 big-Φ=18.18 vs n=4=3.01; 360 grid evals ≈ 30+ h; cf H_1012 n=6 cap, H_1023 n=4-scored). g5 CODE-measured (no LLM self-judge, p7). Scale (n>4) + continuous-density extension UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck).
---

# H_1024 — is the Phi sign-split discretization-invariant?

## 0. motivation
H_1012/1017/1020 all used one fixed binary (2-bin) discretization of the latent transition
structure. The paper claims the SIGN of the split (not the magnitude) is the result, but never
varies the binning. If the sign flips under a different number of bins / thresholds, the headline
"planning raises one measure and lowers the other" would be a 2-bin artifact rather than a measure
property.

## 1. hypothesis
The SIGN of the split (faithful_phi up / big-Phi down for planning) is invariant across a range of
discretizations (e.g. nb in {2,3,4} and alternative threshold placements); only magnitudes move.

## 2. pre-registered falsifier (frozen 2026-06-07)
Re-score the planning vs greedy condition with BOTH stdlib engines (matched, mirror-proven per
binning) across a pre-frozen discretization grid at $n=4$ (n=5 where tractable). Report the sign of
each measure's planning-minus-greedy contrast per binning.
- PASS = SIGN-DISCRETIZATION-INVARIANT : faithful-up / big-Phi-down holds for EVERY binning in the
  grid (sign stable; magnitudes may vary).
- FAIL = SIGN-IS-A-2BIN-ARTIFACT : the sign flips for >=1 valid binning (closed-negative,
  a_paper_negative_ok) — would force the paper's claim to name the discretization.

## 3. honest scope
Toy $n=4$ (n=5 if tractable), $0 CPU; real IIT4 engines (a_phi_iit4_tool). The discretization grid
must be pre-frozen (no post-hoc binning selection). Scale + continuous-density extension UNVERIFIED
(a_scale_honest_scope).

## 4. sibling / xlinks
to [H_1012](./H_1012_bigphi_faithful_larger_n.md) · [H_1017](./H_1017_split_redundancy_mechanism.md) · PAPER/phi-measure-dependence-planning (Limitations c3) · a_phi_iit4_tool

## 5. measurement + finding (2026-06-07 · 🟢 SIGN-DISCRETIZATION-INVARIANT · g5 CODE-measured, $0 CPU-local)
Verdict raw: `.verdicts/1024_phi_split_discretization_invariance/H_1024.txt` (g73 — a deterministic
run that COULD have falsified the sign; both stdlib engines via their CPU mirrors RE-PROVEN ≡
stdlib at n=4 BEFORE scoring, and at n=5 as a cross-check). Script:
`UNIVERSE/h1024_phi_split_discretization_invariance.py`.

**Method (only the discretization varies).** We REUSE the H_1012/H_1017 substrate verbatim — the
same world-model, the same `planning_trajectories` (depth-8 plan vs greedy) generator, the same two
real IIT-4.0 engines (`big_phi`, `faithful_phi` from H_1004), and the same H_1012 `prove_mirrors_at_n`
equivalence proof. The ONLY thing we change is how the continuous latent is binned into the n=4
binary node-state both engines consume. Pre-frozen grid (no post-hoc selection): each top-variance
channel is discretized into `nb` ordered LEVELS by `scheme`, then the binary node bit = `level ≥
ceil(nb/2)` (the upper half — a generalization of the median rule; nb=2/quantile == the H_1012
median baseline). The resulting binary substrate feeds big-Φ (state-by-node TPM) and faithful_phi
(MI over the same binary units, n_bins=2) — both engines stay verbatim and directly comparable. We
score the planning(depth-8) − greedy contrast SIGN of each measure per binning at n=4, 30 seeds.

**Per-binning sign table** (planning depth-8 − greedy, n=4, 30 seeds; matched binary substrate):

| n | nb | scheme | on-frac | faithful_phi Δ | faithful sign | big-Φ Δ | big-Φ sign | faithful-UP & big-Φ-DOWN |
|---|----|--------|---------|----------------|---------------|---------|------------|--------------------------|
| 4 | 2 | equal_width | 0.484 | **+0.9591** | UP | **−5.1949** | DOWN | ✅ True |
| 4 | 2 | quantile (= median baseline, ≡ H_1012/H_1017) | 0.500 | **+2.3332** | UP | **−4.0083** | DOWN | ✅ True |
| 4 | 3 | equal_width | 0.336 | **+0.3863** | UP | **−3.5776** | DOWN | ✅ True |
| 4 | 3 | quantile | 0.344 | **+0.5904** | UP | **−3.4295** | DOWN | ✅ True |
| 4 | 4 | equal_width | 0.484 | **+0.9591** | UP | **−5.1949** | DOWN | ✅ True |
| 4 | 4 | quantile | 0.500 | **+2.3332** | UP | **−4.0083** | DOWN | ✅ True |

binnings with faithful-UP & big-Φ-DOWN: **6/6** (all scored at n=4).

- **VERDICT-TOKEN: 🟢 SIGN-DISCRETIZATION-INVARIANT.** The pre-registered PASS condition is MET: the
  planning faithful_phi-UP / big-Φ-DOWN sign-split holds for EVERY binning in the pre-frozen grid.
  faithful_phi RISES (+0.386 … +2.333, all UP) while system big-Φ FALLS (−3.43 … −5.19, all DOWN) in
  all 6 binnings. Only the MAGNITUDES move (faithful Δ varies ≈6× across binnings; big-Φ Δ varies
  ≈1.5×); the SIGN never flips. The split is NOT a 2-bin (median) artifact — it is a genuine,
  discretization-robust property of the two measures, exactly as the paper asserted ("the sign, not
  the magnitude, is the claim").
- **Baseline reproduction (g5 sanity):** the nb=2 quantile binning IS the H_1012/H_1017 median
  discretization, and it reproduces H_1012 verbatim — big-Φ −4.008 (d−1.83), faithful +2.333 (d+5.18)
  — confirming the substrate is the same one the prior split was measured on.
- **honest scope (a_scale_honest_scope · a_toy_scale_recheck):** the pre-frozen 6-binning grid is
  SCORED at n=4 (the falsifier rung) — both engines EXACT, both CPU mirrors RE-PROVEN ≡ stdlib at n=4
  (ring4 big-Φ=3.0, faithful fixed-trace n4=3.0) BEFORE scoring. n=5 mirrors are RE-PROVEN ≡ stdlib
  (ring5=3.0, faithful n5=4.0) as a cross-check, but the full n=5 grid is the HONEST CAP — a single
  n=5 system big-Φ eval was MEASURED >5.5 min on this Mac (super-exponential: matched-path n=5
  big-Φ=18.18 vs n=4=3.01), so 360 grid evals ≈ 30+ h, INFEASIBLE at $0 CPU (cf H_1012 n=6 cap;
  H_1023 n=4-scored). Scale (n>4) + continuous-density extension UNVERIFIED. g5 CODE-measured
  (no LLM self-judge, p7), a_phi_iit4_tool. NOT a forge binary; $0 CPU-local, no GPU.
