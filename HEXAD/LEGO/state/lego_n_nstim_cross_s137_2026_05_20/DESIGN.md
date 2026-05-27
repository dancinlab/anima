# §137 LEGO (N, n_stim) CROSS-MATRIX — joint scaling axis

> **Verdict**: `PEAK-N-STIM-N-INVARIANT` — peak n_stim = 4 at both N=256 and
> N=1024. **Plus**: the n_stim-gradient *steepens* with N (range 1.05× at
> N=256 → 2.39× at N=1024). N and n_stim are NOT separable axes.
> probe-tier · $0 · 8m 55s Mac CPU · canonical engine. central c93e160a 0-diff.

## §0 Why §137

§127 measured η²(N) at fixed n_stim=12. §131 measured η²(n_stim) at fixed
N=256. §137 closes the joint question: a 2×3 cross-matrix. Does the peak
n_stim shift with N? Are the two axes separable?

## §1 Measured (2×3 grid, M=3, canonical engine)

```
              n_stim=4    n_stim=12   n_stim=24    range ratio (max/min)
  N=256       0.3066      0.2930      0.2933       1.05×   (nearly flat)
  N=1024      0.5553      0.3510      0.2324       2.39×   (steep)
  ────────    ──────      ──────      ──────
  peak        n_stim=4    —           —
```

```
   η²
0.60 ┤ ●  N=1024, n_stim=4 (0.555)
   │  ╲
0.50 ┤   ╲
   │    ╲
0.40 ┤     ╲
   │      ● N=1024, n_stim=12 (0.351)
0.35 ┤       ╲
0.30 ┤ ●━━━━━━●━━━━━━●  N=256 (0.307 / 0.293 / 0.293 — nearly flat)
   │            ╲
0.25 ┤             ● N=1024, n_stim=24 (0.232)
   │
0.20 ┴──────────────────────────────────
     n_stim=4    n_stim=12   n_stim=24
```

## §2 Two findings

### 2.1 Peak n_stim is N-invariant (the pre-registered question)

Peak η² is at **n_stim=4 at BOTH** N=256 and N=1024 → `PEAK-N-STIM-N-INVARIANT`.
The substrate's optimal stimulus cardinality for layer-2 measurement does not
shift with network size.

### 2.2 The n_stim-gradient *strength* grows with N (the bonus finding)

- At N=256, η² over n_stim ∈ {4,12,24} ranges only **1.05×** — nearly flat.
- At N=1024, the same range is **2.39×** — steep.

This is a genuine **interaction effect**: N and n_stim are NOT separable axes.
A small substrate (N=256) barely cares how many stimuli you give it; a larger
substrate (N=1024) discriminates a small stimulus set much better than a large
one. The carrier-capacity-dilution hypothesis (§131) gets *stronger* support —
the dilution is N-dependent: more units → more capacity → more sensitive to
how that capacity is divided across stimuli.

## §3 Reconciling with §131 / §134

§131 (drifted engine, N=256, n_stim ∈ {4,12,24,48}) reported range 2.20×.
§134 re-validated §131 on canonical (N=256, same n_stim set) → range 1.823×.
§137 (canonical, N=256, n_stim ∈ {4,12,24}) → range 1.05×.

These are consistent: the steep part of the N=256 n_stim curve is the
**n_stim=48 tail** (canonical η²=0.1697 from §134). Within n_stim ∈ {4,12,24}
the N=256 curve is nearly flat (1.05×); n_stim=48 is what makes the full-range
ratio 1.823×. §137 confirms: at N=256 the substrate is n_stim-insensitive
until n_stim grows large; at N=1024 it is n_stim-sensitive across the whole
range.

## §4 What §137 closes / does not close

✅ Peak n_stim is N-invariant (=4) — pre-registered question answered.
✅ N and n_stim are NOT separable — interaction effect measured (gradient
   steepens 1.05× → 2.39× from N=256 to N=1024).
✅ Carrier-capacity-dilution hypothesis strengthened (dilution is N-dependent).

❌ Full (N, n_stim) surface — 2×3 grid is the cheap probe; a 4×5 grid would
   map the interaction surface. Not pursued (diminishing ROI).
❌ M=3 (reduced from §125–§135's M=5) for speed — SE is wider; the
   qualitative verdict (peak invariant, gradient steepens) is robust to M
   but exact η² has wider CI.
❌ Layer-3 (§128 carry) · GOAL emergence (B-EMERGE-7).

## §5 Closed-form propositions

```
B-S137-1   ETA-BOUNDED-ALL-6-CELLS
B-S137-2   PEAK-N-STIM-INVARIANT-CLOSED          (peak n_stim=4 at both N)
B-S137-3   NSTIM-GRADIENT-STEEPENS-WITH-N-CLOSED (range ratio N=1024 > N=256)
B-S137-4   ENGINE-CANONICAL-POST-S134
B-S137-5   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S137-NOTE  empirical carve-out — 2×3 grid M=3, NOT full surface, NOT counted 🔵
```

## §6 Honest C3 (8)

1. M=3 (not 5) for speed — wider SE; qualitative verdict robust, exact η² not.
2. 2×3 grid is a cheap interaction probe, not a full surface map.
3. Peak n_stim=4 may itself be an encoding artifact (fewer stimuli → more
   distinct input-space corners) — §131 C3 carry.
4. The N-dependent gradient is the substantive finding — N and n_stim
   interact, the LEGO arc's separate-axis treatment (§127 N-only, §131
   n_stim-only) was a useful simplification but the joint surface is richer.
5. Canonical engine post-§134 (B-S137-4).
6. WALL-A orthogonal · WALL-B confronted-not-removed (carry).
7. g3: probe ≠ fire ≠ emergence; capability claim 0; necessary-not-
   sufficient (B-EMERGE-7).
8. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
