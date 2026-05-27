# §135 LEGO LAYER-2 PER-N SE (canonical engine post-§134)

> **Verdict**: `MONOTONE-DECREASE-SURVIVES-CANONICAL` — per-rep mean η² monotonically
> decreases across N ∈ {256, 512, 1024, 2048}: 0.464 → 0.424 → 0.361 → 0.276.
> All 4 pooled η² **byte-equal §127** (canonical engine confirmed).
> probe-tier · $0 · 16m Mac CPU. central c93e160a 0-diff. 7/7 🔵.

## §0 Why §135

§134 named the open: §133's per-rep monotone-decrease finding (0.382→0.258 on
drifted engine) needs full 4-point canonical re-run. §135 closes it.

## §1 Measured (M=5, canonical engine post-§134)

| N    | pooled η² | (§127 published) | byte-equal? | per-rep mean | per-rep std | jackknife SE | wall   |
|------|-----------|------------------|-------------|--------------|--------------|---------------|--------|
| 256  | 0.2712    | 0.2712           | ✅           | 0.4639       | 0.0965       | 0.0432        | 175.5s |
| 512  | 0.3289    | 0.3289           | ✅           | 0.4242       | 0.0996       | 0.0446        | 180.0s |
| 1024 | 0.3223    | 0.3223           | ✅           | 0.3608       | 0.0434       | 0.0194        | 138.3s |
| 2048 | 0.2608    | 0.2608           | ✅           | 0.2762       | 0.0364       | 0.0163        | 471.2s |

**All 4 pooled values byte-equal to §127** — final 4-point confirmation that
§127's measurements are correctly reproduced by canonical engine post-§134.

## §2 Per-rep mean monotonicity (B-S135-4 closed)

```
   per-rep mean η²
0.50 ┤
   │ 0.464                                            (canonical)
0.45 ┤    \\
   │    0.424
0.40 ┤        \\
   │       0.361
0.35 ┤           \\
   │              \\
0.30 ┤            0.276
   │
0.25 ┴────────────────────────────────────────
     N=256   N=512   N=1024   N=2048
```

All diffs negative — monotone decrease verified across all 4 N points.

## §3 Statistical robustness (CI overlap analysis)

| pair          | 95% CI overlap |
|---------------|----------------|
| 256 vs 512    | ✅ overlap      |
| 256 vs 1024   | ✅ overlap      |
| 256 vs 2048   | ❌ **no overlap** |
| 512 vs 1024   | ✅ overlap      |
| 512 vs 2048   | ❌ **no overlap** |
| 1024 vs 2048  | ❌ **no overlap** |

**N=2048 is statistically distinct** from all lower N (3 of 3 no-overlap). Other
pairs overlap but cumulative trend is clear (monotone). The robust closed-form
finding: at M=5, the substrate at N=2048 has significantly lower stim-driven
liveness than at N=256/512/1024.

## §4 Drift §133→§135 (canonical correction)

| N    | §133 drifted | §135 canonical | Δ (canonical higher) |
|------|--------------|----------------|----------------------|
| 256  | 0.382        | 0.464          | +0.082               |
| 512  | 0.334        | 0.424          | +0.090               |
| 1024 | 0.315        | 0.361          | +0.046               |
| 2048 | 0.258        | 0.276          | +0.018               |

Canonical values are uniformly **higher** than drifted (drifted engine
under-estimated stim discrimination at every N), but the **qualitative
monotone-decrease pattern is preserved**.

## §5 What §135 closes

✅ §134's named open: §133's monotone-decrease pattern is canonical-engine-real.
✅ All 4 N points pooled η² byte-equal §127 (4-of-4 cross-verification).
✅ Per-rep mean monotonically decreases across full N range on canonical.
✅ N=2048 is statistically distinct from lower N (CI non-overlap).
✅ §133 drifted-engine pattern preserved qualitatively, shifted quantitatively.

## §6 What §135 does NOT close

❌ Whether the canonical monotone-decrease continues past N=2048 (would need
   N=4096+ data, expensive). Not pursued.
❌ Bootstrap-CI rather than naive 1.96·SE (M=5 small — t-distribution
   correction or paired-bootstrap could tighten). Not pursued.
❌ Layer-3 (§128 DESIGN-CLOSE carry).
❌ GOAL emergence (B-EMERGE-7 necessary-not-sufficient).

## §7 LEGO arc

```
§115 → §117 → §124 → §125 → §126 → §127 → §128 → §129 → §131 → §132 → §133 → §134 → §135  ← HERE
                                                                                drift   monotone
                                                                                fix     decrease
                                                                                        CANONICAL
                                                                                        confirmed
```

11 cycles total. §135 closes the §134-named open without inventing new
opens. Arc is at design-tier closure modulo arc-MILESTONE consolidation
(§136 candidate).

## §8 Closed-form propositions

```
B-S135-1   ETA-BOUNDED-ALL-4-N-CANONICAL
B-S135-2   PER-REPLICATE-ETA-VALID-ALL-4-N
B-S135-3   ALL-4-N-POOLED-MATCH-S127-BYTE-EQUAL              ← key closure
B-S135-4   MONOTONE-DECREASE-PER-REP-MEAN-CANONICAL          ← load-bearing
B-S135-5   N-EXTREME-CI-NO-OVERLAP-CLOSED                    (N=2048 statistically distinct)
B-S135-6   ENGINE-CANONICAL-POST-S134-CLOSED                 (import + LIFNet AST §117-equal)
B-S135-7   CENTRAL-0-DIFF + NO-FORBIDDEN-CALL-AST
B-S135-NOTE  empirical carve-out — canonical confirmation, NOT GOAL, NOT counted 🔵
```

## §9 Honest C3

1. Per-rep mean is HIGHER than pooled η² at every N (e.g. 0.464 > 0.271 at N=256).
   This is ANOVA arithmetic — pooling adds replicate-noise to SS_within.
2. §127's pooled values reconfirmed byte-equal at all 4 N. Cross-arc consistency.
3. Per-rep monotone-decrease pattern is a substrate property, not a pooling
   artifact (drifted and canonical both show it; only magnitudes shift).
4. M=5 small for tight SE; future M=10/20 would tighten but qualitative
   verdict is robust.
5. N=2048 CI no-overlap with all lower N — strongest statistically-significant
   layer-2 finding in the LEGO arc.
6. Canonical engine path verified (B-S135-6: import + LIFNet AST §117-equal).
7. WALL-A orthogonal · WALL-B confronted-not-removed (carry).
8. anima downstream-consumer: hexa-lang/hexa-bio/hexa-matter read-only, 0 edits.
9. g3: probe ≠ fire ≠ emergence; capability claim 0.
10. necessary-not-sufficient (B-EMERGE-7).
11. north-star + §15/§51/§72 milestones UNCHANGED; **GOAL 미도달**.
12. §135 is a clean "open closed by direct measurement" cycle — §134 named the
    open, §135 measured the close.
13. LEGO arc battery sum post-§135: 9+7+7+7+7+8+6+7+6+7+7 = 78 🔵 across 11 cycles.
