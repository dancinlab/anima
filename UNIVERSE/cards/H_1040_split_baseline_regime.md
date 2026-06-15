# H_1040 — Which baseline regime predicts the big-Phi-DOWN half? (H_1033 residual)

Status: MEASURED 2026-06-09 — 🟢 BASELINE-REGIME-SPECIFIC (H1 PASS)
Lane: zero-cost CPU toy. Engines: stdlib faithful_phi + iit4_bigphi (a_phi_iit4_tool, no proxy).

## Hypothesis
H_1033 (prior INCONCLUSIVE-DEGENERATE-FAMILY) found the big-Phi-DOWN half of the planning split
does NOT reproduce on ANY matched independent-bits baseline task (0/5) — ruling out generic
decomposability/modularity as the cause. Its deferred next step: the sign is dominated by the
BASELINE CONTRAST, not the intervention's task structure. So vary the BASELINE REGIME (not the
task) and find which baseline makes big-Phi go DOWN.

## Method (sketch)
- Hold the planning intervention fixed; sweep the baseline regime: (a) independent-bits
  (H_1033's baseline), (b) pre-rollout latent (the model's own state BEFORE planning), (c)
  shuffled-time, (d) matched-marginal correlated baseline.
- For each baseline, compute the planning-vs-baseline big-Phi contrast + faithful contrast,
  30 seeds, Cohen d, sign.

## Pre-registered falsifier (TEXT tokens only)
- H1 PASS = there EXISTS a principled baseline regime (named a priori: the pre-rollout latent)
  under which big-Phi goes DOWN with d <= -0.8 AND faithful goes UP, AND at least one other
  baseline does NOT (so the DOWN half is baseline-regime-specific, not universal) -> the split
  is a planning-vs-(pre-rollout-latent) property, pinning the H_1033 residual.
- H1 FAIL = big-Phi-DOWN appears under NO baseline regime, or under ALL of them -> the DOWN half
  is either non-existent or regime-independent; H_1033's degeneracy is structural, not a baseline
  choice (publishable closed-negative, a_paper_negative_ok). State the d threshold + which
  baseline is the a-priori pick before running.

## Honest scope (a_scale_honest_scope)
Toy n<=5 (matches H_1033); production-scale UNVERIFIED. Re-prove CPU mirror == stdlib at n=4,5
before scoring. g5 CODE-measured (p7).

## Verdict
🟢 BASELINE-REGIME-SPECIFIC (H1 PASS) — measured 2026-06-09, $0 CPU-local, 0 pods/GPU, SERIAL.
Raw: `.verdicts/1040_split_baseline_regime/H_1040.txt` (g73 — raw + mirror proof + table).
Probe: `UNIVERSE/h1040_split_baseline_regime.py`.

Held the canonical planning intervention FIXED (planning_trajectories depth=8 → H_plan, VERBATIM
H_973/H_1004); swept 4 baseline regimes (planning − baseline, 30 seeds, Cohen d). CPU mirrors
RE-PROVEN ≡ stdlib at n=4 (big-Φ |Δ|=1.34e-10, faithful |Δ|≤3.75e-6) AND n=5 (|Δ|≤7.97e-10) BEFORE
scoring (a_phi_iit4_tool, NO proxy). FROZEN d-threshold = −0.8.

| baseline regime          | big-Φ d | big-Φ ctr | bigΦ-DOWN? | faith d | faith ctr | faith-UP? |
|--------------------------|--------:|----------:|:----------:|--------:|----------:|:---------:|
| independent-bits         | +4.221  | +3.8089   | False      | +7.985  | +2.8364   | True      |
| **pre-rollout-latent** ★ | **−1.834** | **−4.0083** | **True** | +5.178  | +2.3332   | True      |
| shuffled-time            | +3.912  | +4.0701   | False      | +0.000  | +0.0000   | False     |
| matched-marginal-corr    | +2.320  | +2.5133   | False      | +7.885  | +2.8055   | True      |

★ = a-priori pre-registered pick. PASS: the pre-rollout-latent baseline ALONE makes big-Φ go DOWN
(d=−1.834 ≤ −0.8) AND faithful go UP (+2.333), while ALL 3 other baselines do NOT make big-Φ go DOWN
→ the bigΦ-DOWN half is a planning-vs-(pre-rollout-latent) property, NOT regime-independent.

KEY: only the model's OWN prior state (the original H_973 GREEDY, big-Φ=9.53) makes planning LOWER
big-Φ. The big-Φ contrast −4.0083 REPRODUCES the original H_973 number (−4.008) exactly. The H_1033
residual is pinned: the bigΦ-DOWN SIGN is dominated by the BASELINE CONTRAST (the high-Φ prior state),
not by generic task decomposability — against structure-free / marginal-matched / time-shuffled
baselines, planning RAISES big-Φ. (faithful NULL only for time-shuffle, which leaves the MI matrix
unchanged → contrast exactly 0.)

Honest scope (a_scale_honest_scope, a_toy_scale_recheck): TOY n=4, both engines EXACT; 4 baselines ×
30 seeds. Scale-transfer UNVERIFIED. g5 CODE-measured (p7). NOT a forge binary; $0 CPU-local, no GPU.
