# H_6164 GPU SCALE-LADDER (owner GPU go 2026-07-02) — RESULT

**TIER: 🧱 FLOOR-DIRECTIONAL — structural-bind does NOT scale-amplify to a G1 lever.**
aiden RTX 5070 pool GPU, torch=DIRECTIONAL, $0. Tests whether H_6164's cheap sub-threshold
tensor-product lift (+0.05..0.11) crosses +0.15 AND grows with scale (scale = amplifier of a real lever).

## Ladder (arms: add / hadamard / bilinear / tensorproduct(full outer-product); 3 seeds)
| rung | D | steps | oracle | best-binder Δ (mean) | tensorproduct Δ (mean) |
|---|---|---|---|---|---|
| 0 | 96  | 10k  | 1.0 (solvable) | +0.076 | **+0.024** |
| 1 | 160 | 45k  | 1.0 (solvable) | +0.028 | **−0.027** |
| 2 | 256 | 120k | 0.12–0.22 (UNDERTRAINED) | +0.062 | +0.022 |

## Reading — decisive on the CLEAN rungs
- rung0 & rung1 are cleanly solvable (oracle=1.0). Across them the tensor-product delta goes **+0.024 → −0.027**
  — it does NOT grow, does NOT approach +0.15, and turns NEGATIVE at larger scale. The scaling-lever
  hypothesis (delta grows AND crosses +0.15) is FALSIFIED on the clean rungs.
- rung2 (D=256) is UNDERTRAINED (oracle 0.12–0.22, add train_acc 0.14) → that rung alone is INCONCLUSIVE
  (needs far more steps), but it does not rescue the hypothesis: the clean-rung trend is already anti-growth.
- The H_6164 cheap-toy "consistent tensor-product lift" was **config-specific noise** — at D=96/BS=512 it
  flipped to collapse (seed4302 TP=0.0) and at rung1 the mean TP delta is negative.

## Verdict
Structural-bind (Hadamard / bilinear / full tensor-product) is NOT a scale-amplified G1 lever. Confirms
H_1840 (γ bypass-denied bilinear FALSIFIED) at GPU scale from a cleaner angle. The owner-authorized GPU
fire returned a clean FLOOR. G1 recombination wall holds axis-invariant across objective, regularization,
data-coverage, and structural-bind — at both toy and (clean-rung) scale. DPI meta-law reconfirmed.

(Caveat per a_toy_scale_recheck: rung2 top-scale is undertrained; a fully-clean D=256 rung would need
~5–10× more steps. Not pursued — the clean rungs already falsify scaling, and 303M anima retrain is the
proper terminal if ever revisited, but the trend de-motivates it.)

## Provenance
scale_ladder_v2.py, run_v2.log, result_v2.json. aiden RTX 5070, torch 2.10, $0 (fleet-contended ~2.5hr wall).
