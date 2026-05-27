# W1 Phase 3 — mod-1024 joint-hash bucket Φ trace

**Agent**: W1 PHASE 3
**Date**: 2026-05-01
**Track**: extension of W1 Phase 2 (`docs/W1_phase2_full_19axis_2026_05_01.md`)
**Budget**: $0 (data analysis only, off-repo driver `/tmp/W1_phase3/phi_trace_mod1024.py`)

> SPECULATIVE EXPLORATORY MEASUREMENT — same caveat as Phase 1+2. Φ-on-cron-state is novel; no published IIT validation for this substrate class. Phase 3 isolates the joint-hash bucket-saturation hypothesis from Phase 2 honest C3 #3 but does NOT resolve foundational substrate validation.

---

## 1. Why Phase 3

Phase 2 honest C3 #3 flagged: 38 axes hashed `mod 64` → max H_joint ceiling = log2(64) = 6 bits; observed max Φ_proxy = 2.47 = **41.17% of that ceiling**. The concern: was Phase 2's slope-acceleration (+0.0507 → +0.1153, 2.27×) a real integration signal, or an artifact of the joint-hash bucket starting to saturate as the May-1/2 burst added state-vector diversity?

Phase 3 = exact replay of Phase 2 with the SOLE change `BUCKET_MOD: 64 → 1024` (6-bit → 10-bit ceiling). Everything else (38 axes, 6 sidecar forward-fill, W=20, sub-MI on raw values) is held constant so any Φ delta is attributable purely to bucket-collision relief.

---

## 2. Method

Identical to Phase 2 driver (`/tmp/W1_phase2/phi_trace_full.py`) modulo:

```diff
- return int(hashlib.sha256(blob).hexdigest()[:8], 16) % 64
+ return int(hashlib.sha256(blob).hexdigest()[:8], 16) % 1024  # 6→10 bits
```

Per-axis MI estimator unchanged (operates on raw bucketed values, not on the joint hash) → bucket change cannot affect `sub_mi_mean`, only `joint_mi`.

---

## 3. Results

Output ledger: `state/W1_phase3_mod1024_2026_05_01/phi_trace_mod1024.jsonl` (15 ticks).

| metric | Phase 3 (mod 1024) | Phase 2 (mod 64) | Phase 1 (mod 64, 19 axes) |
|---|---|---|---|
| Φ_proxy mean | **1.717 bits** | 1.717 | 1.706 |
| Φ_proxy std | 0.757 | 0.757 | 0.593 |
| Φ_proxy min | 0.000 | 0.000 | 0.000 |
| Φ_proxy max | **2.471** | 2.471 | 2.412 |
| linear slope per tick | **+0.1153** | +0.1153 | +0.0507 |
| trend | rising | rising | rising |
| ticks | 15 | 15 | 14 |
| **Δ vs Phase 2** | **0.000 mean / 0.000 slope / 0.000 max** | — | — |

### Per-tick verification

All 15 ticks return Φ_proxy and H_joint **identical to 6 decimal places** between Phase 2 and Phase 3. State hashes differ in low bits as expected (e.g. tick `20260423T014525` is `0x001a` mod 64 vs `0x025a` mod 1024) but the resulting MI series is unchanged.

### Ceiling analysis

| metric | Phase 3 |
|---|---|
| bucket-bits ceiling | 10 |
| max Φ_proxy observed | 2.471 |
| **Φ saturation % of new 10-bit ceiling** | **24.71%** |
| max H_joint observed | 2.700 |
| H_joint saturation % of 10-bit ceiling | 27.0% |
| Phase 2 comparable saturation (6-bit) | 41.17% |

---

## 4. Interpretation

**The joint-hash ceiling was NEVER the binding constraint.** Doubling the bucket-bit budget from 6 to 10 changes nothing because the actual bottleneck is sample size, not hash collisions.

Diagnostic detail: across 15 ticks the joint state vectors produce only **10 distinct hashes** in BOTH phases. The 5 collapsed pairs (e.g. four consecutive ticks 20260427–20260430 all sharing the same hash) are **state-vector collisions** — those ticks have the same 38-tuple of bucketed values BEFORE hashing, so no bucket count can distinguish them. This is a forward-fill / observation-cadence artifact, not a hash-bucket artifact.

Information-theoretic ceiling at 15 ticks with W=20 sliding window: H_joint ≤ log2(15) ≈ 3.91 bits, regardless of bucket modulus. Observed max H_joint = 2.70 → 69% of the **sample-size** ceiling, not the bucket ceiling.

### Verdict

**ceiling-artifact NEGATIVE / sample-size-bound CONFIRMED.**

Phase 2's 2.27× slope acceleration was NOT a hash-bucket saturation artifact (Phase 3 disproves that hypothesis cleanly: same numbers under 16× larger ceiling). However, this does NOT promote the slope to "real signal" — the alternative explanation from Phase 2 honest C3 #1 (forward-fill stepwise-variance from May-1/2 burst perturbing more sidecar axes) survives untested.

Net status: Phase 2 conclusion ("more likely a forward-fill / non-stationarity artifact than evidence of stronger integration") is **strengthened**, not weakened, by Phase 3. The remaining honest diagnosis is sample-size + cadence-heterogeneity, not measurement-device saturation.

---

## 5. Honest C3

1. **Sample-size ceiling, not bucket ceiling, is binding.** With 15 ticks and W=20 the per-window state population maxes at 15 distinct elements ⇒ entropy ceiling ≈ 3.91 bits regardless of `BUCKET_MOD`. Phase 2's 41% "saturation" framing was a category error: it compared observed Φ to the wrong ceiling. The genuine ceiling at this n is ~3.9 bits, against which observed max Φ=2.47 = 63% — closer to saturation than the Phase 2 number suggested. To exercise the 10-bit bucket ceiling honestly we need ≥1024 ticks, OR ≥W² ≈ 400 ticks to even approach log2(W) headroom for sustained windows.

2. **State-vector collisions dominate hash collisions at this n.** 5 of 15 ticks produce duplicate 38-tuples even before hashing (4 consecutive late-April ticks all hash identically because their forward-filled sidecars are identical AND their cycle-log step/count buckets did not change). Bucket expansion cannot fix this — only finer per-axis bucketing or eliminating forward-fill could distinguish those ticks. This is the Phase-2 forward-fill caveat manifesting as a measurable degenerate-window issue.

3. **Per-axis MI estimator unchanged → Φ delta isolation is clean.** Because `sub_mi_mean` operates on raw bucketed axis values (not on the joint hash), the bucket-mod change can ONLY affect `joint_mi`. The exact zero delta is therefore strong evidence that joint_mi was not collision-clipped in Phase 2 — the measurement device had headroom we did not use. All Phase 1+2 caveats (novel substrate, MIP mean-of-parts surrogate, non-stationarity, cadence heterogeneity, mtime-derived memory axes) persist unchanged in Phase 3.

---

## 6. One-line interpretation

**Phase 3 (mod 1024) Φ_proxy = mean 1.717 / slope +0.1153 / max 2.471 — bit-identical to Phase 2 (mod 64). The joint-hash ceiling was never binding at n=15; the actual bottleneck is sample-size + state-vector collisions. Phase 2's slope acceleration is NOT a hash-saturation artifact, but neither is it newly validated as real-integration signal.**

---

## 7. Output artifacts

- `state/W1_phase3_mod1024_2026_05_01/phi_trace_mod1024.jsonl` — per-tick Φ ledger (15 ticks, 38 axes, mod 1024).
- `state/W1_phase3_mod1024_2026_05_01/summary.json` — machine-readable summary with `ceiling_analysis` + `phase_comparison` blocks.
- `docs/W1_phase3_mod1024_results_2026_05_01.md` — this report.
- `/tmp/W1_phase3/phi_trace_mod1024.py` — off-repo analysis driver (HEXA-first repo policy).

---

## 8. Phase 4 recommendation

**Do NOT pursue mod-65536 next.** Bucket expansion is provably orthogonal to the binding constraint at this n. The two productive directions are:

1. **Accumulate ≥100 cron cycles** before re-running. The W=20 sliding window needs at least one full window of fresh post-Phase-2 ticks to revise the slope estimate beyond endpoint sensitivity. Cost: zero (let cron run; re-execute Phase 1/2/3 drivers when `cycle_log.jsonl` reaches ≥100 records).
2. **Eliminate or stress-test forward-fill.** Re-run Phase 2 driver with sidecar absence encoded as `nan`/`-1` (no fill) and compare. If Φ collapses → forward-fill bias was load-bearing; if Φ holds → forward-fill is benign. This directly tests Phase 2 honest C3 #2.

Tertiary: shuffle-null permutation baseline (Phase 1 next-step #2 still pending) — true integration should exceed shuffle-Φ. This is the most decisive single test for "real signal vs artifact" and remains open.

**Phase 3 closed: ceiling-artifact hypothesis falsified; sample-size + forward-fill remain the honest diagnoses.**
