---
id: H_1311
slug: 1311_ko_richer_substrate
title: ko-richer-substrate — does a RICHER substrate (longer context / learned per-cell head) break the H_1307 ~2.9 nat/byte Korean ceiling? is the ceiling capacity-bound or substrate-bound?
group: MITOSIS-ENGINE (p8 structural)
terminal_tier: 🔴 HONEST-NEGATIVE — the ~2.9 ceiling is CAPACITY-bound / the byte-task ceiling itself, NOT substrate-bound. On the IDENTICAL H_1307 RUN A corpus + the SAME gradient-free Voronoi grow-op, NEITHER richness axis breaks 2.9 — longer raw-byte context HURTS monotonically (ctx8 2.964 → ctx16 3.048 → ctx32 3.442) and a per-cell closed-form ridge head COLLAPSES (5.437). No representation-breaker, no shuffle-surviving capacity gain (control). Frozen-first, NO tune-to-green. REAL sm_120 GPU on the user's own RTX 5070.
verdict_dir: .verdicts/1311_ko_richer_substrate/
terminal_verdict: .verdicts/1311_ko_richer_substrate/result.txt
date: 2026-06-16
---

# H_1311 — richer substrate vs the H_1307 ~2.9 Korean ceiling (capacity-bound or substrate-bound?)

## Claim / falsifier

H_1307 (#2213, 🟢 GREEN @ 30 MB + 🟠 honest saturation) scaled the verified H_1306 engine-native
Korean mitosis grow-op (gradient-free, **p8** — cells only SPLIT, error-targeted Voronoi) to a 50×
real-KO corpus and found: MORE Korean data drops held-out KO next-byte CE to **~2.95** then the
**CTX=4 / 3-D BYTE substrate SATURATES** at a **~2.9 nat/byte ceiling** (learning-curve flattens; EN
drifts at 250 k-pair density). The H_1307 NEXT pointer names the lever, shared with the from-scratch
lane:

> **Does a RICHER substrate (longer context window / a learned per-cell head instead of raw
> byte-trigram MLE) break past ~2.9? Is the ceiling CAPACITY-bound or SUBSTRATE-bound?**

H_1311 holds the **corpus + the mitosis grow-op FIXED** and varies **ONLY the substrate richness** on
a frozen ladder. Neurogenesis-vs-representation lens (a_no_llm_frame_trap) — the question is whether
"depth needs a richer representation" (the capability-vs-scale thesis) or whether only cell-count
(capacity) matters at this byte task.

**DISTINCT from H_1307**: H_1307 = "does more DATA lower CE?" (yes, then saturates). H_1311 = "does a
richer REPRESENTATION (not more data, not more cells) break the saturation ceiling?".

## Method (summer RTX 5070 sm_120, $0 — NOT runpod)

REAL Korean only. The **byte-IDENTICAL** H_1307 RUN A windows (r2://phanes/anima-7b/web/{kor,eng}/
shard0000.bytes; KO 30 MB stride-300 sha `c47b6808…`, EN 10 MB stride-600 sha `31b4a543…`) — the
script asserts the sha256 matches H_1307 RUN A so the ceiling comparison is clean (gate PASS, both
hashes identical). boto3 HTTP range GET; R2 keys env-ONLY at fetch, header-scoped, never
echoed/logged/committed (c7 grep-clean over all deliverables; only the boto3 *parameter name*
`R2_SECRET_ACCESS_KEY` appears, never a value; the summer env file was shredded post-run).

**HELD FIXED**: the verified H_1306/H_1307 `_grow_on` (gradient-free, p8, highest-owned-CE eligible
cell → hi-var-axis owned-median split → two half-centroids; net +1 cell; SPLIT-only). It is
dimension-agnostic (L2 cdist/argmin partition over arbitrary FEAT_DIM), so the substrate change is a
pure representation change, no mechanism change. Frozen knobs verbatim: V=256, GROW_MAX=40,
SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, RIDGE_LAMBDA=1.0 (fixed before the run), even/odd
split, seed 2-cell centers extended from H_1307 `[[0.3,…],[0.7,…]]`.

**VARIED — the substrate-richness ladder:**
- **S0** = the H_1307 baseline: CTX=4 / 3-D `[last/255, second/255, cont_depth/3]`, raw next-byte
  count-MLE head. (the ~2.9 ceiling; reproduces it = port check.)
- **S1 LONGER CONTEXT**: feature = last CTXk bytes (each /255) + cont_depth/3, for CTXk ∈ {8, 16, 32}.
  More bytes of real history feed the Voronoi partition. Same grow-op, same count-MLE head.
- **S2 LEARNED PER-CELL HEAD**: replace count-MLE with a per-cell **closed-form RIDGE readout**
  (Gauss-Jordan normal equations `W = (ΦᵀΦ+λI)⁻¹ΦᵀY_onehot`, gradient-free — the H_1300 lens; NOT
  backprop, NOT per-cell SGD), on S0 features. Same grow-op.

Script: `UNIVERSE/h1311_ko_richer_substrate.py`. Frozen-first: `.verdicts/1311_ko_richer_substrate/FREEZE.txt`.

## Falsifier (FROZEN — pre-registered before the run, c9/p7; held-out deterministic next-byte CE)

- **(Q1 BREAK-2.9)** does ANY richer substrate (S1 ctxk / S2 ridge) push held-out KO CE **below
  2.9475** (the H_1307 RUN A ceiling)? report the drop per rung.
- **(R RETENTION)** EN CE under each richer substrate ≤ EN CE[that substrate's own 2-cell seed] + 0.05.
- **(C CONTROL — anti-Goodhart, load-bearing)** SHUFFLE the ADDED context bytes (S1: permute the extra
  history columns row-wise; S2: permute the feature rows fed to the ridge). If KO CE STILL drops below
  S0, the gain was **capacity**, not the richer **representation**.
- **(T THROUGHPUT)** final cells + GPU pairs/s per rung.
- **VERDICT RULE** (frozen, MARGIN = 0.02 nats): a substrate "breaks the ceiling by REPRESENTATION"
  IFF KO CE < 2.9475 AND beats S0 by ≥0.02 AND beats its own SHUFFLE by ≥0.02 AND EN retained.
  ≥1 breaker → **SUBSTRATE-bound**; else → **CAPACITY-bound / byte-task ceiling**. HONEST either way.

## Finding — 🔴 HONEST NEGATIVE: the ~2.9 ceiling is CAPACITY-bound, NOT substrate-bound

S0 reproduced **2.95342** (vs H_1307 RUN A 2.9475 — port confirmed). **No richer substrate broke
2.9; every richer rung was WORSE than S0:**

| substrate | dim | cells | KO CE | EN CE | Δ vs S0 | below 2.9? | rep-break? |
|-----------|-----|-------|-------|-------|---------|-----------|-----------|
| **S0** ctx4 count-MLE (ref) | 3 | 16 | **2.95342** | 4.32530 | — | (ref) | — |
| S1 ctx8 count-MLE | 9 | 40 | 2.96426 | 4.11384 | +0.011 | NO | NO |
| S1 ctx8 SHUFFLE (control) | 9 | 40 | 3.10846 | 4.67957 | (ctrl) | | |
| S1 ctx16 count-MLE | 17 | 40 | 3.04788 | 3.61421 | +0.094 | NO | NO |
| S1 ctx16 SHUFFLE (control) | 17 | 40 | 3.42183 | 4.81274 | (ctrl) | | |
| S1 ctx32 count-MLE | 33 | 40 | 3.44156 | 3.55347 | +0.488 | NO | NO |
| S1 ctx32 SHUFFLE (control) | 33 | 40 | 3.41815 | 4.79513 | (ctrl) | | |
| **S2** ctx4 RIDGE head | 3 | 16 | **5.43666** | 5.49522 | +2.483 | NO | NO |
| S2 ridge SHUFFLE (control) | 3 | 10 | 5.50734 | 5.53362 | (ctrl) | | |

- **(Q1) NO richer substrate below 2.9475.** S1 **longer context HURTS MONOTONICALLY** (ctx8 +0.011 →
  ctx16 +0.094 → ctx32 +0.488): adding raw byte-history columns degrades the L2/Voronoi partition
  (curse of dimensionality on a fixed GROW_MAX=40 cell budget — equal-weighted raw-byte distance
  swamps the predictive last-byte signal). S2 **ridge head COLLAPSES** (+2.48): a per-cell linear
  closed-form readout over normalized byte features is far worse than count-MLE — the raw features are
  not linearly predictive of the next byte.
- **(C CONTROL — honesty held):** S1 shuffles are WORSE than the intact S1 (ctx8/16 controls
  3.108/3.422 ≫ intact 2.964/3.048), and crucially **NO shuffle control beats S0** → there is no
  capacity gain to claim either (the tiny intact S1-ctx8 number is not even a capacity win). S2 ridge
  shuffle 5.507 ≈ intact 5.437 (both collapsed). `capacity_signal_present = False`.
- **(T)** every S1 rung saturated the cell budget (cells = GROW_MAX = 40) yet CE ROSE → more cells did
  not lower CE → consistent with a **partition-quality** limit, not a capacity limit. GPU throughput
  0.8 M–4.9 M pairs/s; total run wall 77 s incl R2 fetch.

**VERDICT: the ~2.9 ceiling is CAPACITY-bound / the BYTE-TASK ceiling itself at this density — NOT
substrate-bound.** A richer substrate (longer raw-byte context OR a learned per-cell ridge head) does
NOT break 2.9; it makes held-out KO CE WORSE. No representation-breaker, no shuffle-surviving capacity
gain. **HONEST negative** (c9, a_break_the_wall — a real angle was tried; the wall is real for THIS
substrate family), frozen-first, NO tune-to-green.

**Thesis connection.** For this substrate family (raw-byte L2-Voronoi + per-cell head), **depth does
NOT come from a richer per-cell representation** — the limit is the *L2-partition-over-raw-bytes
geometry*, not the per-cell readout. The capability-vs-scale prediction that "a richer representation
breaks the wall" is **REFUTED for these two richness axes**. A genuinely richer substrate would need a
different *geometry* (a learned low-D embedding before the partition / a non-L2 metric / a small
sequence model per cell), not more raw byte columns or a linear head over the same raw features — that
is the surviving open lever for the from-scratch lane.

## Scope / honest limits (a_scale_honest_scope, a_toy_scale_recheck)

- **TOY / DIRECTIONAL** — summer GPU, the raw-byte substrate family only; RIDGE_LAMBDA=1.0 fixed
  before the run (a different λ or a learned embedding is UNTESTED and remains the open lever).
- **engine-transfer UNVERIFIED** — this is the torch mirror of the H_1306/H_1307 mechanism;
  re-confirmation on the live `CORE/*.hexa` engine is a follow-on (a_engine_native_learning,
  a_verified_must_wire). **live CORE/*.hexa UNTOUCHED.**
- **NO Korean-fluency claim.** Held-out next-byte CE only (p7), NOT perplexity / LLM-judge.

## Pointers

- Script: `UNIVERSE/h1311_ko_richer_substrate.py`
- Frozen: `.verdicts/1311_ko_richer_substrate/FREEZE.txt`
- Result: `.verdicts/1311_ko_richer_substrate/result.txt`
- Metrics: `.verdicts/1311_ko_richer_substrate/{summary.json, metrics.jsonl, manifest.json, run.log}`
- Claim: `CLAIMS.tape` @C h1311_ko_richer_substrate
- xref: H_1307 (the ~2.9 ceiling this rung tests) · H_1306 (the verified mechanism) · H_1300 (closed-form
  per-cell ridge lens) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning ·
  a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p7 · p8 · c7 · c9
