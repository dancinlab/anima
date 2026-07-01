# H_6161 INHIBITION-AS-COMPOSITIONAL-NOISE — STAGE-1 FAIR cheap-gate RESULT (2026-07-02)

**TIER: 🧱 DIRECTIONAL-FLOOR (NOT-SUPPORTED).** torch mirror = DIRECTIONAL. GPU NOT authorized.
Same operator-agnostic compositional toy as H_6162; sweep trunk dropout dp∈{0,0.1,0.25(GZ),0.4}, 5 seeds.
oracle_ok=True (task compositionally solvable → floor is real).

## Primary bar (does LOWER inhibition than GZ=0.25 lift held-out composition?) — FAIL
best-dp<GZ held-out − dp=GZ held-out, per seed: 0.000 / +0.080 / −0.027 / **−0.127** / −0.116.
n(Δ≥+0.15)=**0/5**, no_regress=False. dp=0.25 is even BEST for seed 4304 (0.370) — opposite of the
"lower inhibition helps" prediction. Held-out is noise across dp, no consistent band. → FLOOR.

## Secondary MECHANISM read (the interesting part) — An&Du direction CONFIRMED but INERT for G1
HE-proxy (homomorphism generalization residual) rises ~monotonically with inhibition:
seed7 dp{0,0.1,0.25,0.4} → HE {0.087, 0.242, 1.929, 3.047}; same trend all seeds. So inhibition **does**
degrade the homomorphism structure exactly as An&Du predict (noise-degrades-composition). **But** that
degradation does NOT translate into any held-out composition change — held-out floors regardless of HE.

## Reading (converges with H_6162)
Homomorphism structure is dial-able (up via L_HE / H_6162, down via inhibition / here) and the HE-proxy
tracks it, yet **held-out G1 recombination is invariant to it**. Homomorphism is not the G1 lever. Both
axes reconfirm the trunk-objective floor (DPI meta-law); regularization-band and objective-form both 🧱.

## Provenance
summer pool CPU, torch, OMP=4, $0. FREEZE.md (pre-registered), toy_inhibition_gate.py, run.log, result.json.
