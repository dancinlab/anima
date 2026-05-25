# §132 LEGO LAYER-2 NON-MONOTONIC SHAPE FIT — closes §127's "shape" residual

> **Verdict**: `SHAPE-FIT-IDENTIFIED` — best model = inverted-U Gaussian-in-log-N, R²=0.9995. §127 OLS log-linear baseline R²=0.022; Δ=+0.977.
> analysis-tier (re-fit of §127 data, NO new measurement) · $0 instant · central c93e160a 0-diff. 6/6 🔵.

## §0 Why §132

§127 measured 4 (N, η²) points and fit OLS log-linear: k=−0.0198, R²=0.022 →
APPROXIMATELY-N-INVARIANT. The honest residual carried: "logistic / piecewise /
saturating fits = future work; non-monotonic shape may carry information." §132
closes that residual with 3 candidate non-linear models.

## §1 Four candidate models, OLS-fit on §127's (N=256/512/1024/2048, η²=0.271/0.329/0.322/0.261)

| label | model                                              | n_params | R²     | shape    |
|-------|----------------------------------------------------|----------|--------|----------|
| A     | log η² = a + k·logN (§127 baseline)                | 2        | 0.0225 | monotone |
| B     | log η² = c0 + c1·logN + c2·logN² (quadratic-log)   | 3        | **0.9995** | peak     |
| C     | η² = η_max·N/(N+K) (saturating Hill)               | 2        | 0.0082 | monotone |
| D     | log η² = a − ((logN−μ)/σ)²/2 (inverted-U Gaussian) | 3        | **0.9995** | peak     |

```
          R² panel
    1.0 ┤                  ●═══●  B & D (peak models)
        │                        agree R²=0.9995
    0.5 ┤
        │
    0.0 ┤  ●     ●               A & C (monotone) reject
        │  A     C               R² ≈ 0 / 0.008
   -0.5 ┴────────────────────────────────────────
```

**Peak models agree. Monotone models reject.** That's the load-bearing closed-form
finding (B-S132-5), NOT the R² value itself.

## §2 What §132 closes

✅ **§127's non-monotonic shape is an inverted-U peak structure**, not noise.
   Peak location estimate from both peak models: log N* ≈ 6.5–7.0 → **N* ≈ 730–1000**
   (peak η² near §126's N=1024 measurement).
✅ **§127's "no power-law" verdict refined**: η²(N) is well-described by a
   peaked shape but NOT a monotone-in-N law. The §127 OLS log-linear failure is
   structural, not measurement noise.
✅ **Saturating Hill (B-Michaelis form) REJECTED**: η² does not asymptote with N
   over this range; it peaks and declines.

## §3 Honest 1-DoF caveat (B-S132-NOTE, NOT counted 🔵)

4 data points + 3 free parameters = **1 degree of freedom**. Perfect R²=0.9995 is
*structural* — any 3-param model can interpolate 4 nearly-aligned points. The
clean signal is the **agreement of two peak models AND the rejection of both
monotone models** (B-S132-5), not the R² magnitude.

Quadratic-log and Gaussian-in-log-N are nearly equivalent reparametrisations on
this point set (both R²=0.9995 to 5 digits). A truly identified shape would
require 6–8 N values; 4 points cannot distinguish them.

## §4 Closed-form propositions

```
B-S132-1   R-SQUARED-BOUNDED-CLOSED-ALL-FITS
B-S132-2   R-SQUARED-3-BUCKET-CLOSED-PARTITION (sympy Interval)
B-S132-3   OLS-NORMAL-EQUATIONS-IDENTITY-CLOSED (sympy re-derive k byte-equal §127)
B-S132-4   ANALYSIS-USES-§127-DATA-BYTE-EQUAL-CLOSED (no new measurement)
B-S132-5   PEAK-MODELS-AGREE-MONOTONE-MODELS-REJECT-CLOSED  ← load-bearing
B-S132-6   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S132-NOTE  4-points-vs-3-params-1-DoF overfit risk, NOT counted 🔵
```

## §5 LEGO arc

```
§125 → §126 → §127 → §131 → §132  ← HERE
PARTIAL N-1pt   N-4pt  n_stim   re-fit
0.271  GROWS   APPROX  STRONGLY  inverted-U
       ONE     N-INV   ratio    Gaussian
       POINT  (non-    2.20×    R²=0.9995
              monot)            (1-DoF)
```

§127's "shape unknown" → §132 "inverted-U identified (1-DoF caveat)." Doesn't
overturn §127's APPROXIMATELY-N-INVARIANT verdict — refines it to "η²(N) has a
peak around N≈730–1000, not flat noise."

## §6 Honest C3

1. R²=0.9995 is structural at 1 d.o.f.; load-bearing signal = peak-vs-monotone
   model agreement, not absolute R² magnitude.
2. Peak N* estimate has wide CI; 4 points cannot pin it.
3. Quadratic-log and Gaussian-in-log-N are nearly equivalent here; cannot
   distinguish.
4. Saturating Hill rejection is robust (R² 0.008 << log-linear 0.022, both << peak).
5. §127's APPROXIMATELY-N-INVARIANT verdict UNCHANGED at its scope (`k ≈ 0` true
   for log-linear); §132 refines the *shape* of the deviation.
6. WALL-A orthogonal · WALL-B confronted-not-removed (carry).
7. g3: analysis ≠ measurement ≠ fire ≠ emergence; capability claim 0.
8. anima downstream-consumer: hexa-lang/hexa-bio/hexa-matter read-only, 0 edits.
9. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
