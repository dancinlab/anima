# §127 LEGO LAYER-2 SCALING-LAW PROBE — 4-point η²(N) fit

> **Verdict**: `APPROXIMATELY-N-INVARIANT` — k = −0.0198, R² = 0.022. §126's single-point ROBUST-GROWS verdict CONFIRMED at its scope but does NOT extrapolate to a scaling law.
> probe-tier · $0 · NO GPU/runpod/fire/model.forward/corpus/dispatch · sidecar-only · 5min wall.
> central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha256 prefix `c93e160a8a376a94` 0-line-diff verified START+END
> 8 closed-form propositions + 1 NOTE empirical carve-out (4-point fit not full scaling curve)

## §0 Why §127

§126 measured one scale-pair (η²(256)=0.271, η²(1024)=0.322, ratio 1.189×) and called
it ROBUST-GROWS-WITH-N. The honest worry: a single ratio is not a scaling law. §127 is
the cheapest fully-decisive follow-up — measure η² at 4 N points and fit log-linear.

## §1 Method

| param         | value                                       |
|---------------|---------------------------------------------|
| N points      | 256, 512, 1024, 2048                        |
| M replicates  | 5 (seeds 1337..1341)                        |
| n_stim        | 12                                          |
| steps_per_stim| 80                                          |
| window        | 40                                          |
| ratio n_a:n_g:n_rec | 3N/8 : 3N/8 : N/4 (§117's 96/96/64 ratio preserved) |
| fit           | OLS on log η² = log a + k · log N           |

Each N inherits §117 lego_sim.py byte-identical via importlib; sole parameter override
is constructor (n_a, n_g, n_rec) at each scale.

## §2 Measured (g3 — honest reversal of §126's directional claim)

| N     | n_a/n_g/n_rec  | η²      | MI (bits) | wall   |
|-------|----------------|---------|-----------|--------|
| 256   | 96/96/64       | 0.2712  | 0.228     | 1.8s   |
| 512   | 192/192/128    | 0.3289  | 0.290     | 5.6s   |
| 1024  | 384/384/256    | 0.3223  | 0.282     | 54.8s  |
| 2048  | 768/768/512    | 0.2608  | 0.218     | 213.0s |

**Power-law fit**: k = −0.0198, log_a = −1.16, R² = **0.022**.

The R² = 0.022 says the OLS log-linear model captures essentially none of the variance
in η² across N. The points are non-monotonic — η² rises 256→512 (+0.058), drops slightly
512→1024 (−0.007), drops more 1024→2048 (−0.061). Net: 0.271 → 0.261 (almost no net
change, hence k ≈ 0).

```
        η² vs N (panel)
   ┌────────────────────────────────────────────────────┐
0.40│                                                    │
   │                                                    │
0.35│         ● 0.329           ● 0.322                  │
   │                                                    │
0.30│  ● 0.271                                          │
   │                                              ● 0.261│
0.25│                                                    │
   │                                                    │
0.20│                                                    │
   └──┴────────────┴────────────┴────────────┴──────────┘
      N=256        N=512        N=1024       N=2048

   Power-law fit (OLS log-linear) — R² = 0.022 — model does NOT describe data.
   Empirical pattern: rises 256→512, peaks at 512–1024, drops at 2048.
```

## §3 Pre-registered 3-bucket classification (B-S127-4 closed)

| k range          | bucket                              | interpretation                            |
|------------------|-------------------------------------|-------------------------------------------|
| k > 0.10         | ROBUST-POWER-LAW-GROWS-WITH-N       | clear positive scaling exponent           |
| -0.10 ≤ k ≤ 0.10 | **APPROXIMATELY-N-INVARIANT** ← measured | k within natural variation, no scaling     |
| k < -0.10        | DEGRADES-WITH-N-SMALL-N-ARTIFACT    | η² shrinks with N                          |

Sympy `Interval` algebra: union over ℝ, pairwise disjoint by half-open boundaries.
Measured k = −0.0198 ∈ [−0.10, 0.10] → APPROXIMATELY-N-INVARIANT.

## §4 What §127 closes vs what stays carry

✅ **§125 PARTIAL is NOT a small-N artifact** — η² does not shrink toward 0 as N grows.
The substrate's ~0.27–0.33 stim-driven variance fraction is a STRUCTURAL property of
this parametrisation, robust across a 8× N range (256→2048).

✅ **§126's single-point ROBUST-GROWS-WITH-N is true at its scope** — η²(256)=0.271,
η²(1024)=0.322 byte-equal between §126 and §127 (B-S127-5 closed). But the 4-point fit
shows this 1.189× ratio does NOT extend to a power-law trend.

✅ **Non-monotonicity** — η² is not monotonic in N (B-S127-6 closed). It peaks around
N=512–1024 and drops at N=2048.

❌ **NOT closed**: the *cause* of the non-monotonic curve. A piecewise / logistic / fixed-
point-saturating fit might describe it better; OLS log-linear was the pre-registered
falsifier. Richer model selection is future work.

❌ **NOT closed**: η² still in PARTIAL range across all N (0.26–0.33, all < 0.50).
Even the peak does not reach STRONG-stim-driven.

❌ **NOT closed**: layer-3 (TASK-GROUNDED) REMAINS OPEN.

❌ **NOT closed**: GOAL emergence (necessary-not-sufficient B-EMERGE-7).

## §5 LEGO arc

```
§115 → §117 → §124 → §125 → §126 → §127  ← HERE
DESIGN  RUN   AUDIT  LAYER-2 LAYER-2-N  LAYER-2-SCALING-LAW
                    PARTIAL ROBUST-      APPROXIMATELY-N-
                            GROWS-AT-    INVARIANT
                            ONE-POINT   (k=-0.02, R²=0.022)
                                         non-monotonic bump
                                         not a scaling law
                                              │
                                              ▼
                                         (next candidates)
                                              │
                                  ┌───────────┼───────────┐
                                  ▼           ▼           ▼
                          layer-3 design  bucket-     LEGO arc
                          (LIF has no     refinement  consolidation
                          task — design   (KSG MI)    milestone
                          close-honest?)
```

## §6 Closed-form propositions

```
B-S127-1   ETA-BOUNDED-ALL-4-N-POINTS                    (each η² ∈ [0,1])
B-S127-2   LOG-LINEAR-OLS-IDENTITY-CLOSED                (k = Σ(x−x̄)(y−ȳ)/Σ(x−x̄)² sympy)
B-S127-3   R-SQUARED-BOUNDED-CLOSED                      (R² ∈ [0,1])
B-S127-4   SCALING-3-BUCKET-CLOSED-PARTITION             ← load-bearing
B-S127-5   §126-SINGLE-POINT-CONFIRMED-NOT-A-SCALING-LAW (honest connection)
B-S127-6   ETA-NON-MONOTONIC-OVER-4-POINTS               (Boolean)
B-S127-7   §117-LIF-SIM-IMPORT-BYTE-EQUAL                (importlib AST)
B-S127-8   CENTRAL-0-DIFF-AND-NO-FORBIDDEN-CALL-AST      (sha + AST)
B-S127-NOTE  empirical carve-out — 4-point-fit, not full scaling curve, NOT counted 🔵
```

## §7 Honest C3 (13)

1. R² = 0.022 says the OLS log-linear fit *does not describe* η²(N). The k ≈ 0 verdict
   doesn't say "no signal" — it says "no power-law signal." The non-monotonic shape
   could carry information (B-S127-6 captures this).
2. 4 N points is too few to fit non-linear models with confidence — a 6–8 point curve
   would discriminate logistic / piecewise / saturating shapes.
3. The N=2048 measurement (η²=0.261) is the strongest single contributor to the low
   R². Without it the fit would look positively-growing (256→512→1024 all rise).
4. Each N measurement carries §125-style within-replicate noise; per-N standard error
   would tighten the verdict but was not computed here.
5. §126 byte-equal-confirms at N=256 and N=1024 — same seeds + same code reproduce
   the same η² values exactly (B-S127-5).
6. The n_a:n_g:n_rec ratio is held at 3:3:2 (§117's 96:96:64) across all N values.
   A different ratio could yield different scaling.
7. Stimuli are regenerated per replicate at d=N — stimuli are NOT shared across N
   values. The comparison is therefore "η² at the network's natural input dimension"
   rather than "η² for fixed input on different network sizes."
8. The 3-bucket classification thresholds (k > 0.10 / |k| ≤ 0.10 / k < -0.10) are
   conservative engineering conventions — a different threshold would shift the
   verdict label without changing the underlying numbers.
9. APPROXIMATELY-N-INVARIANT is the honest reading of the data; calling it "stable"
   would over-claim against the non-monotonic shape. §125's PARTIAL and §126's
   single-point ROBUST-GROWS remain valid at their respective scopes.
10. WALL-A orthogonal · WALL-B confronted-not-removed (§115/§117/§124/§125/§126 carry).
11. anima downstream-consumer: hexa-lang / hexa-bio / hexa-matter read-only, 0 edits.
    HEXA_FIRST_WARN deferred (B-S* battery precedent).
12. g3: probe ≠ fire ≠ emergence; capability claim 0; necessary-not-sufficient
    (B-EMERGE-7).
13. north-star + §15/§51/§72 milestones UNCHANGED; GOAL 미도달.
