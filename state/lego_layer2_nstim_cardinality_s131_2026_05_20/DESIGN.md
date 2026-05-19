# §131 LEGO LAYER-2 STIMULUS-CARDINALITY PROBE

> **Verdict**: `STRONGLY-NSTIM-DEPENDENT` — η² range ratio 2.199× (peak 0.308 at n_stim=4, trough 0.140 at n_stim=24).
> probe-tier · $0 · NO GPU/runpod/fire · 7m 14s Mac CPU wall. central c93e160a 0-diff. 7/7 🔵.

## §0 Why §131

§127 measured η²(N) across 4 N points at fixed n_stim=12 → APPROXIMATELY-N-INVARIANT.
§131 asks the orthogonal question: at fixed N=256, how does η² depend on n_stim?

## §1 Method

- N=256 fixed (n_a=96, n_g=96, n_rec=64) — same as §125 baseline.
- n_stim ∈ {4, 12, 24, 48} (geometric step ×~2, 12× cardinality range).
- M=5 replicates per n_stim, seeds {1337..1341}.
- Imports `HEXAD/LEGO/lego_engine.py` canonical lib (post-§129 promote —
  **first LEGO probe written against the canonical engine SSOT**, B-S131-4).

## §2 Measured

| n_stim | η²      | Gaussian MI (bits) | wall   |
|--------|---------|--------------------|--------|
| 4      | 0.3084  | 0.265              | 23.6s  |
| 12     | 0.2178  | 0.177              | 61.5s  |
| 24     | 0.1402  | 0.109              | 149.8s |
| 48     | 0.1535  | 0.120              | 198.7s |

- **η² peaks at the lowest n_stim** (n=4) — B-S131-6 Boolean closed.
- η² range ratio η²_max / η²_min = 0.308 / 0.140 = **2.199×**.
- Mostly monotonic decrease 4→24, slight rise 24→48 (noise band).

```
                η²(n_stim) panel
   ┌────────────────────────────────────────────┐
0.35│ ● 0.308                                    │
   │                                            │
0.30│                                            │
   │                                            │
0.25│           ● 0.218                          │
   │                                            │
0.20│                                            │
   │                                  ● 0.153   │
0.15│                       ● 0.140              │
   │                                            │
0.10│                                            │
   └──┴────────────┴────────────┴────────────┴──┘
      n_stim=4     n_stim=12    n_stim=24    n_stim=48

   Pre-registered: > 1.50 → STRONGLY ←  measured 2.199
                   1.10–1.50 → MILDLY
                   < 1.10 → INVARIANT
```

## §3 Pre-registered 3-bucket classification (B-S131-2)

| range ratio        | bucket                       | sympy Interval                |
|--------------------|------------------------------|-------------------------------|
| > 1.50             | **STRONGLY-NSTIM-DEPENDENT** ← measured | open (3/2, ∞)         |
| 1.10–1.50          | MILDLY-NSTIM-DEPENDENT       | closed [11/10, 3/2]           |
| < 1.10             | NSTIM-INVARIANT              | half-open (0, 11/10]          |

Partition exhaustive over (0,∞) and pairwise disjoint. Measured 2.199× ∈ (3/2, ∞)
→ STRONGLY-NSTIM-DEPENDENT.

## §4 What §131 closes (and what it doesn't)

✅ **n_stim is a stronger η² modulator than N** in the §117 LIF substrate at the
   tested parametrisation. (η² range across n_stim: 2.20× · η² range across N
   in §127: 0.329/0.261 = 1.26× — n_stim's range is ~1.7× larger.)

✅ **§125's n_stim=12 was a mediocre choice** for measuring η² — closer to the
   trough than to the peak. The original arc would have measured stronger
   stimulus-driven liveness at n_stim=4.

✅ **Carrier capacity hypothesis** consistent with data: Ψ-C1 ∈ [0,1] is a
   bounded carrier; denser stimulus packing dilutes between-stim signal.
   Honest carry: this is a *consistent* explanation, not a proven mechanism.

❌ **NOT closed**: full η²(n_stim) curve — 4 points span 12× cardinality but
   the slight rise 24→48 may signal a second regime that 8/16/32/etc. points
   would map.

❌ **NOT closed**: whether the peak shifts at different N values (would need
   the (N, n_stim) cross matrix, §132 candidate).

❌ **NOT closed**: layer-3 (still §128 DESIGN-CLOSE-REQUIRES-TASK).

❌ **NOT closed**: GOAL emergence (necessary-not-sufficient B-EMERGE-7).

## §5 LEGO arc

```
§115 → §117 → §124 → §125 → §126 → §127 → §128 → §129 → §131  ← HERE
                              N-axis  N-scale  scaling  layer-3  engine  n_stim axis
                                                       close    promote  STRONGLY
                                                                          n_stim-DEP
                                                                          ratio 2.20×
```

## §6 Closed-form propositions

```
B-S131-1   ETA-BOUNDED-ALL-NSTIM-POINTS
B-S131-2   RANGE-RATIO-3-BUCKET-CLOSED-PARTITION    ← load-bearing
B-S131-3   SS-DECOMPOSITION-IDENTITY-ALL-NSTIM (ANOVA at every n_stim)
B-S131-4   ENGINE-IS-CANONICAL-LEGO-LIB-POST-§129   ← first probe on canonical engine
B-S131-5   N-FIXED-NSTIM-VARIES-ORTHOGONALITY (N=256 invariant, n_stim varies)
B-S131-6   ETA-PEAK-AT-MIN-NSTIM-MEASURED (Boolean)
B-S131-7   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S131-NOTE  empirical carve-out — 4-cardinality-point measurement, NOT counted 🔵
```

## §7 Honest C3 (13)

1. n_stim=4 peak may be an *encoding* effect: fewer stim means each stim's
   half-active pattern occupies a more distinct corner of the 256-dim input
   space, making cosine-of-spike-rate easier to discriminate.
2. n_stim=48 slight rise (vs 24) suggests a second regime; 4 points
   insufficient to resolve.
3. §125's "PARTIAL" verdict at η²=0.218 was n_stim=12, near the η² trough.
   At n_stim=4 the same arc could have called LAYER-2-STRONGLY-PARTIAL or
   nearly STRONG (0.308 still < 0.50 STRONG threshold).
4. Range ratio 2.199 was computed as max/min over 4 points — different
   sample of n_stim could yield different ratio.
5. Total wall 7m 14s — n_stim=48 dominated (198s = 46% of total) because
   wall scales linearly with n_stim at fixed N.
6. Engine SSOT used = `HEXAD/LEGO/lego_engine.py` (post-§129 promotion).
   This is the first probe written against the canonical engine instead of
   importlib of state/s117/lego_sim.py. B-S131-4 closed.
7. WALL-A orthogonal · WALL-B confronted-not-removed (§115/§117/§124 carry).
8. anima downstream-consumer: hexa-lang/hexa-bio/hexa-matter read-only,
   0 edits. HEXA_FIRST_WARN deferred (B-S* sidecar precedent).
9. Probe-tier, not run-tier — `lego_engine.py` itself unchanged (sha
   constant during §131); only probe scripts wrote new files.
10. g3: probe ≠ fire ≠ emergence; capability claim 0.
11. necessary-not-sufficient at every layer (B-EMERGE-7).
12. north-star + §15/§51/§72 milestones UNCHANGED; GOAL 미도달.
13. The valuable output: n_stim is a stronger lever than N at this scale —
    informs future probe design (peak η² is achievable at n_stim=4).
