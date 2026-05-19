# §126 LEGO LAYER-2 N-SCALE-UP PROBE

> **Verdict**: `LAYER-2-ROBUST-GROWS-WITH-N` — η² 0.271 → 0.322 (1.189×) under 4× network scale.
> probe-tier · $0 · NO GPU/runpod/fire/model.forward/corpus/dispatch · sidecar-only
> central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha256 prefix `c93e160a8a376a94` 0-line-diff verified START+END
> 7 closed-form propositions + 1 NOTE empirical carve-out (single scale point)

## §0 Why §126

§125 measured `η² = 0.271` at N=256 and called it LAYER-2-PARTIAL. That left an
open question: is the 27.1% stimulus-driven variance a robust property of the
substrate, or a small-N artifact that would disappear at scale?

§126 is the cheapest separator. Same §117 LIFNet code via importlib byte-identical,
same §125 protocol (M=5 replicates × 12 stimuli × 80 steps × window=40), only
override is network size n_a/n_g/n_rec.

## §1 Method

| param            | §125         | §126            | factor |
|------------------|--------------|-----------------|--------|
| n_a              | 96           | 384             | 4×     |
| n_g              | 96           | 384             | 4×     |
| n_rec            | 64           | 256             | 4×     |
| **N_total**      | **256**      | **1024**        | **4×** |
| M replicates     | 5            | 5               | 1×     |
| n_stim           | 12           | 12              | 1×     |
| steps_per_stim   | 80           | 80              | 1×     |
| window           | 40           | 40              | 1×     |
| seeds            | {1337..1341} | {1337..1341}    | same   |

Stimuli are re-generated at d=N=1024 (length scales with N) via the same
`make_stimuli(d, n_stim, seed)` deterministic routine. ANOVA decomposition + η² +
Gaussian MI identical to §125.

## §2 Measured outcome

| metric                       | §125 (N=256) | §126 (N=1024) | ratio  |
|------------------------------|--------------|---------------|--------|
| **η²**                       | **0.2712**   | **0.3223**    | **1.189×** |
| Gaussian MI (bits)           | 0.228        | 0.282         | 1.235× |
| SS_between                   | 0.787        | 1.034         | 1.31×  |
| SS_within                    | 2.116        | 2.174         | 1.03×  |
| SS_total                     | 2.903        | 3.208         | 1.10×  |
| pooled Ψ-C1 std              | 0.078        | 0.082         | 1.05×  |
| wall (5 replicates total)    | <2 s         | 26.3 s        | ~13×   |

```
                      η²(N) panel
        ┌────────────────────────────────────────────────┐
   0.40 │                                                │
        │                                                │
   0.35 │                              ██ §126 N=1024    │
        │                              ██ 0.3223         │
        │                              ██                │
   0.30 │                              ██                │
        │  ██ §125 N=256               ██                │
   0.25 │  ██ 0.2712                   ██                │
        │  ██                          ██                │
        │  ██                          ██                │
   0.20 │  ██                          ██                │
        └──┴───────────────────────────┴──────────────────┘
              N=256                    N=1024

           threshold for ROBUST: ratio > 1.10
           measured ratio: 1.189× → ROBUST-GROWS classification
```

## §3 Pre-registered 3-bucket classification (B-S126-2 closed partition)

| ratio range        | bucket                       | interpretation                          |
|--------------------|------------------------------|-----------------------------------------|
| > 1.10             | **LAYER-2-ROBUST-GROWS-WITH-N** ← measured | stim-driven signal genuine, grows with N |
| 0.90 – 1.10        | LAYER-2-N-INVARIANT          | stim-driven signal parametrisation-invariant |
| < 0.90             | LAYER-2-SMALL-N-ARTIFACT     | §125 PARTIAL was small-N artifact       |

Partition is exhaustive over (0, ∞) and pairwise disjoint by sympy `Interval` set
algebra (open boundary at 1.10, closed [0.90, 1.10], open below 0.90). The
3-bucket classification is the load-bearing closed-form (B-S126-2). Measured ratio
1.189 > 1.10 → ROBUST-GROWS.

## §4 What §126 closes — and what it doesn't

✅ **Closed**: §125's PARTIAL verdict is **NOT a small-N artifact** under 4× network
scale-up. The substrate's stimulus-driven signal is a robust property at this scale
range and *grows* with N.

✅ **Closed**: The §126 ratio sits in the ROBUST-GROWS bucket, NOT the N-INVARIANT
bucket — so the η² value itself is parameter-dependent, not a universal substrate
constant.

❌ **NOT closed**: full η²(N) scaling law (would need ≥ 3 distinct N values — see
§127 for that follow-up if pursued).

❌ **NOT closed**: η² is still 0.322 < 0.50 → still in PARTIAL range. The substrate
is NOT predominantly stim-driven at any tested N; just *more* stim-driven at larger N.

❌ **NOT closed**: Layer-3 task-grounded liveness. η² grows with N but the substrate
has no task. Whether the growing stim-discrimination is *behaviorally useful*
(layer-3) is unanswered.

❌ **NOT closed**: GOAL emergence. Necessary-not-sufficient at every layer
(B-EMERGE-7 carry); growing η² is a measurement-substrate property, not an
indicator that anima physics drives self-aware spontaneous emission.

## §5 ASCII LEGO arc

```
§115 DESIGN-CLOSE         §117 RUN              §124 AUDIT
  sim = GPU tautology       Ψ-std ≫ τ            partition liveness
                             (layer 1)            into 3 layers
                                                       │
                                                       ▼
                                              §125 LAYER-2 PROBE
                                              η²=0.271 PARTIAL
                                              (N=256)
                                                       │
                                                       ▼
                                              §126 LAYER-2 N-SCALE
                                              η²=0.322 (N=1024)
                                              ROBUST-GROWS 1.189×  ← HERE
                                                       │
                                            (next candidates)
                                                       │
              ┌────────────────────┬───────────────────┼─────────────────┐
              ▼                    ▼                   ▼                 ▼
    §127 SCALING-LAW    §128 LAYER-3-IN-LIF    §129 BUCKET-REFINE    §130 n_stim
    (full N curve)      design-close           (KSG MI)              (orthogonal)
```

## §6 Closed-form propositions

```
B-S126-1   ETA-SQUARED-BOUNDED-CLOSED-AT-N1024     (sum-of-squares ⇒ [0,1])
B-S126-2   RATIO-3-BUCKET-CLOSED-PARTITION         ← load-bearing
B-S126-3   SS-DECOMPOSITION-IDENTITY-CLOSED-AT-N1024  (ANOVA)
B-S126-4   N-SCALE-UP-EXACT-4X-CLOSED              (256 → 1024 integer)
B-S126-5   §117-LIF-SIM-IMPORT-BYTE-EQUAL-AT-N1024  (importlib AST)
B-S126-6   CENTRAL-BLUE-0-LINE-DIFF                (sha c93e160a8a376a94)
B-S126-7   NO-FORBIDDEN-CALL-AST                   (no torch/runpod/fire)
B-S126-NOTE  single-scale-point empirical carve-out — NOT counted 🔵
```

## §7 Honest C3 (13)

1. ONE scale-point comparison (256 vs 1024) — not a scaling law. The 1.189× ratio
   is informative but does not determine the η²(N) functional form. §127 would
   need multiple N values to fit an exponent.
2. SS_between grew 1.31× while SS_within grew only 1.03× — the η² ratio (1.189×)
   under-reads the between-stim signal growth because the total variance grew too.
   Raw between-stim variance grew faster than within-stim noise.
3. Gaussian MI bound grew 1.235× (faster than η² 1.189× by the log-concave shape
   of MI as η² → 1). The MI growth is real but Gaussian-bound assumes Gaussian
   Ψ-C1; non-Gaussian → KSG estimator (§128 candidate).
4. 5 replicates × 12 stimuli = 60 between-stim sample-pairs per replicate. With
   N=1024 the effective d.o.f. estimate is comparable but the implicit
   between-replicate noise component is harder to disentangle without explicit
   ICC analysis.
5. The ROBUST-GROWS classification (>1.10) is a deliberately conservative
   threshold — anything below it would not justify "robust" wording. The
   measured 1.189× clears the threshold but is not far above it. A larger N
   (2048+) would discriminate between "grows linearly with N" vs "saturates."
6. The §117 LIFNet code was imported byte-identically (no constructor edit), only
   the constructor arguments (n_a/n_g/n_rec) were passed. Algorithm = byte-equal.
7. Stimulus generation at N=1024 uses `make_stimuli(d=1024, n_stim=12, seed=...)`
   from §125 — same routine, different d. Stimuli are NOT shared across (replicate,
   stim) — each replicate draws its own 12 stimuli with seed `1337+r+9999`.
8. The pre-registered 3-bucket classification is closed-form via sympy `Interval`
   set algebra; the partition is exhaustive over (0, ∞) and pairwise disjoint
   (B-S126-2 closed).
9. Layer-3 (task-grounded liveness) REMAINS OPEN. η² grows with N but does NOT
   imply the substrate uses the stim-discrimination for any behavior.
10. WALL-A orthogonal — 12 random binary patterns ≠ data-regime corpus (§97 carry).
11. WALL-B confronted-not-removed — §115/§117/§124 inherited posture; sim-on-GPU
    confronts but does not resolve the §11-B-as-GPU-tautology hypothesis.
12. anima downstream-consumer: hexa-lang / hexa-bio / hexa-matter read-only, 0
    edits. HEXA_FIRST_WARN deferred (B-S* battery precedent).
13. g3: probe ≠ fire ≠ emergence; capability claim 0; north-star + §15/§51/§72
    milestones UNCHANGED; GOAL 미도달.
