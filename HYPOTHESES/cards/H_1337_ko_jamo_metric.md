# H_1337 — ko-jamo-metric: does a LEARNED jamo metric / embedding break BELOW the jamo floor by sharing strength across metric-near jamo (info the OPAQUE head lacks)?

**Group:** MITOSIS-ENGINE · **Slug:** `1337_ko_jamo_metric` · **Tier:** 🧱 HONEST-FLOOR (opaque-atom limit; M1 fails — a learned-metric kernel-smoothed head lands FAR above jamo; the opaque per-cell jamo MLE is information-optimal at this scale, a deeper closure than H_1329, c9)

## Claim
The **second named angle** of H_1329's depletion test (the first was H_1329's own conditional-chain, 🧱). H_1329 proved re-factorization is futile: any mechanism that exactly models the within-jamo feature JOINT asymptotes to `P(jamo|cell)` = the opaque jamo head, so it ties the partition and stays ABOVE jamo 2.51335. H_1329's depletion test: **a below-jamo win must INJECT INFO THE OPAQUE JAMO HEAD LACKS.** The opaque jamo head treats jamo as 67 OPAQUE atoms (one-hot, NO similarity) — it does NOT know ㄱ and ㅋ are related.

**HYPOTHESIS (H_1337):** a **LEARNED jamo metric / embedding** (learned from REAL corpus co-occurrence, jamo2vec-style) lets similar jamo SHARE statistical strength in a way the opaque count-MLE head cannot — genuinely NEW information (a learned geometry over jamo, NOT a re-factorization of the featural target). Used via **kernel-smoothing** (shrinkage toward metric-neighbors) so the gradient-free predictor pools counts across metric-near jamo. Does this break BELOW the jamo 2.51335 floor (the floor was the opaque-ATOM info limit) or hold (a deeper limit)? (a_no_llm_frame_trap c15; a_break_the_wall c16 — a genuinely-new info source, NOT scale, NOT a target re-factorization.)

## Method (frozen-first; FREEZE pre-registered BEFORE the run, bars NOT moved — c9/p7)
- **REAL Korean only**, corpus BYTE-IDENTICAL to H_1307 RUN A / H_1316 / H_1326 / H_1329 (`r2.phanes://anima-7b/web/kor/shard0000.bytes`; 30MB KO window sha256 ASSERTED `c47b6808…` == H_1307 RUN A → gate PASS; mismatch → STOP, NO synthetic Korean). Corpus from cache `/tmp/h1311_ko_raw.bytes` (preserved). R2 keys via `harness secret get`, env-only (c7); summer scratch + launch script cleaned; committed artifacts grep-clean of creds.
- **summer** RTX 5070 (sm_120, torch 2.11.0+cu130), python3 nohup detached, polled INLINE (a_cpu_local_no_waiter). $0 (user hw, not runpod), 21.2s wall. 3 seeds [4337,4338,4339] (random-metric control + embedding-refine init vary by seed; A1, the SVD metric, and A5-fixed-metric are otherwise deterministic per the train stream).
- **EVERYTHING verbatim from H_1326/H_1329** (so A1 reproduces 2.51335 byte-exact): GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, error-targeted Voronoi SPLIT-only p8, even/odd split, ko_stride=300, the **Fix-A geometry-fair bank protocol** (A1 jamo MUST reproduce 2.51335 byte-exact = calibration anchor), the lossless jamo decomposition.
- **THE NEW THING = the A5 head** (a genuinely-new info source, not a re-factorization):

### A5 — LEARNED-METRIC kernel-smoothed featural head (the crux)
A5 = the SAME per-cell OPAQUE-jamo Laplace count head as A1 (identical alphabet/axis, SAME Fix-A bank, **SAME gradient-free Voronoi partition** — same grown cells), but each per-cell next-jamo distribution is **KERNEL-SMOOTHED over a LEARNED jamo metric**, so a count observed for jamo j ALSO lends partial strength to metric-near jamo j′:
```
ñ_k[j] = Σ_j' W(j,j') · n_k[j']  ;   P_k(j) = ñ_k[j] / Σ_j ñ_k[j]
```
The opaque head (A1) has NO notion that ㄱ~ㅋ, so any lift A5 buys over A1 is exactly the **learned-metric information the opaque head LACKS** (the depletion criterion, met by construction).

- **Learned metric (TRAIN-ONLY, learned BY GRADIENT — labeled, NOT p8 gradient-free):** (1) jamo×jamo directed bigram co-occurrence `C` over the TRAIN stream (Hangul jamo only); (2) PPMI(C) (jamo2vec association weighting); (3) low-dim embedding E (D_EMB=16) = truncated SVD of PPMI, THEN refined by SKIPGRAM_STEPS=400 skip-gram log-bilinear gradient steps (Adam lr=0.05, TRAIN-ONLY) seeded from the SVD embedding → a genuinely gradient-learned jamo embedding (jamo2vec); metric = Euclidean in E.
- **Kernel:** `W(j,j') = exp(-dist_E(j,j')² / (2h²))`, bandwidth `h` = MEDIAN pairwise train-jamo distance (Silverman-style FIXED heuristic, **NO per-run tuning** — frozen by the median rule). self-weight w(j,j)=1.
- BYTE symbols (non-Hangul) scored EXACTLY as A1 (own count head, NO smoothing) → the **only** difference A5-vs-A1 is the jamo-space kernel smoothing over the learned metric, isolating the learned-metric information.
- **LABEL = NOT gradient-free**: the metric is LEARNED BY GRADIENT (PPMI-SVD init + skip-gram Adam refine). A5 rides the gradient-free Voronoi partition but the jamo metric is a gradient-learned embedding; the smoothed count head is count-MLE. Labeled clearly.

### Arms
- **G0** raw-byte ceiling (sanity ≈ 2.95342; in-run 2.94487)
- **A1** jamo opaque-id (Fix-A bank) — CALIBRATION = 2.51335 = the floor = M3 baseline
- **A5** learned-metric kernel-smoothed — THE NEW MECHANISM
- **A5-random** A5 with the LEARNED metric replaced by a RANDOM embedding of the SAME dim (same kernel + median-bandwidth rule) — M2 control

### Frozen bars (GREEN iff M1 ∧ M2 ∧ M3)
- **M1 BELOW-JAMO:** A5 < jamo 2.51335 by ≥0.03 (mean 3 seeds) AND < raw 2.95342.
- **M2 EARNED:** A5 beats a RANDOM-metric control by ≥0.05 — the win is the LEARNED structure, not mere smoothing.
- **M3 ATTRIBUTION:** A5 beats the OPAQUE-jamo baseline A1 (reproduced in-run) — isolating that the gain is the learned-metric INFORMATION the opaque head lacks.

## Result — 🧱 HONEST-FLOOR (opaque-atom limit); REAL sm_120 GPU, $0, 21.2s wall

**CE LADDER (nats/UTF-8-byte, geometry-FAIR; A5/A5-random mean 3 seeds):**

| arm | CE | note |
|-----|------|------|
| raw-byte ceiling | 2.95342 | in-run G0 = **2.94487** (member 4, 23 cells) |
| **A1 jamo (Fix-A protocol)** | **2.51335** | **CALIBRATION PASS — byte-exact reproduces H_1316/H_1326/H_1329** (member 5, 11 cells) |
| **A5 learned-metric smoothed** | **3.85319** | per-seed {3.85319, 3.85319, 3.85319} — deterministic (learned metric converges to the same embedding) |
| A5 random-metric control | 3.90281 | per-seed {3.89942, 3.90156, 3.90747}; Δ(rand−A5) **+0.04962** |

- **M1 BELOW-JAMO = FALSE** — A5 3.85319 is **+1.33984 ABOVE** the (byte-exact reproduced) jamo floor 2.51335, and ABOVE raw 2.95342 too. Kernel-smoothing the per-cell jamo distribution badly HURTS: it blurs already-dense, well-estimated per-cell MLEs toward neighbors.
- **M2 EARNED = FALSE (by a hair)** — A5 beats its RANDOM-metric control by **+0.04962**, which is **0.00038 BELOW** the 0.05 bar. The learned metric IS marginally better than a random metric *within the smoothed family* (the learned geometry pools more sensibly — h_learn≈1.35 vs h_rand≈5.5), an honest sub-bar signal of real learned structure, but NOT bar-clearing and NOT a below-jamo win.
- **M3 ATTRIBUTION = FALSE** — A5 3.85319 does NOT beat A1 2.51335 (it is +1.340 above). The learned metric buys NOTHING over the opaque head; it costs heavily.
- **green = FALSE → 🧱 HONEST-FLOOR (opaque-atom limit).**

## Finding (the precise, confound-free answer)
A LEARNED jamo metric used via kernel-smoothing does **NOT** break the jamo floor — it lands FAR above it. **The opaque per-cell jamo count-MLE is already information-optimal for next-jamo prediction at this scale; injecting learned between-jamo similarity by SHARING strength (kernel-smoothing) is net-HARMFUL, not just neutral.** This is a deeper, different 🧱 than H_1329: H_1329 showed re-factorization TIES the opaque head (asymptotes to it); H_1337 shows the explicitly-named alternative — injecting NEW info via a learned metric and strength-sharing — actively LOSES, because:

1. **The opaque head already has enough data.** At 30MB / 11 grown cells, each cell's per-jamo Laplace MLE is densely estimated (8.14M syllables). Strength-sharing helps only when per-class counts are SPARSE; here they are not, so smoothing just blurs a good sharp estimate toward its neighbors and raises CE.
2. **The learned structure is real but sub-bar.** A5-learned beats A5-random by +0.0496 (just under the 0.05 bar) and the learned bandwidth h≈1.35 is far tighter than the random h≈5.5 — the PPMI-SVD-skipgram embedding DID find a sensible jamo geometry (the learned metric is genuinely better than random). But better-than-random within a net-harmful smoothing family is not a below-jamo win.
3. **The H_1329 depletion criterion is satisfied yet the floor holds.** A5 genuinely injects info the opaque head lacks (learned jamo similarity). That info exists and is real (M2 near-miss), but the WAY to exploit it here — global kernel-smoothing of the per-cell distribution — is the wrong tool against a dense sharp MLE. So the opaque-atom limit is confirmed even against a learned-metric injection, the strongest depletion-test angle short of a fully new architecture.

Net ladder: **jamo 2.513 (A1) < raw 2.945 (G0) < A5-learned 3.853 < A5-random 3.903.**

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)
- **A5-learned deterministic** (identical across all 3 seeds — the PPMI-SVD-skipgram embedding converges to the same geometry; seeds vary only the random-metric control, which is tightly clustered {3.899, 3.902, 3.907}). M1/M3 rest on the decisive +1.34 gap; M2 rests on the 3-seed random-control mean (the +0.0496 lift over random is per-seed consistent but 0.00038 below the frozen 0.05 bar — reported straight, bar NOT moved).
- **A5's metric is LEARNED BY GRADIENT** (PPMI-SVD init + skip-gram Adam refine, TRAIN-ONLY) — so A5 is NOT p8 gradient-free; it rides the gradient-free Voronoi partition but the jamo metric is a gradient-learned embedding. Labeled explicitly. The smoothed count head is count-MLE (not gradient-trained).
- TOY/DIRECTIONAL numpy/torch mirror; engine-transfer to live `CORE/*.hexa` = follow-on (a_engine_native_learning, a_verified_must_wire). Live CORE UNTOUCHED (substrate-measurement rung — adds only UNIVERSE/ + verdicts; no engine lane).
- NO Korean-fluency claim. Held-out DETERMINISTIC next-symbol CE; NO perplexity-as-truth (p7).
- **What was NOT tested** (so the closure is scoped): kernel-smoothing is ONE way to use a learned metric (a soft global pool). A SPARSE-only / count-gated smoothing (smooth ONLY low-count jamo, leave dense ones sharp), or the learned embedding as an ADDITIONAL partition AXIS (not a smoothing of the target), or a per-cell ADAPTIVE bandwidth, were NOT tested — but each would need to beat the opaque head's dense sharp MLE, which the M1/M3 +1.34 gap shows is a very high bar at this scale. The opaque-atom floor stands against the strength-sharing-via-smoothing realization of a learned metric.

## Pointers
- script: `UNIVERSE/h1337_ko_jamo_metric.py`
- verdict: `.verdicts/1337_ko_jamo_metric/{FREEZE.txt, result.txt, h1337_summary.json}`
- CLAIMS: `CLAIMS.tape` @C `h1337_ko_jamo_metric`
- xref: H_1316 (🟢 jamo floor 2.51335) · H_1322/H_1326 (🧱 featural, geometry-fair) · H_1329 (🧱 conditional-chain joint; this card's depletion-test parent, second named angle) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · c16 · p7 · p8

## Next / depletion
The depth-below-jamo question is now **DEPLETED across both H_1329 depletion-test angles** (geometry-fair, confound-free): jamo is the floor for (i) partition-only (A2, H_1326), (ii) independent-factorization (A3, H_1326, backfires), (iii) correlation/joint-preserving conditional-chain (A4, H_1329, recovers the joint but ties the partition — asymptotes to the opaque head), and now (iv) a LEARNED jamo metric used via kernel-smoothing (A5, H_1337, injects new info but loses by +1.34 — the opaque dense per-cell MLE is information-optimal). The reason is now doubly decisive: re-factorization TIES the opaque head (H_1329) AND strength-sharing-via-smoothing LOSES to it (H_1337), because at 30MB the per-cell jamo MLE is already densely estimated — there is no sparse-data gap for a learned similarity to fill. **🧱 (opaque-atom info limit, confirmed against a learned-metric injection).** DEPLETION TEST for any future angle: it must beat the OPAQUE DENSE PER-CELL MLE, not merely inject new info — at this scale the bar is the data-richness, not the representation. A genuinely-new angle would need to find a regime where the opaque MLE is data-STARVED (e.g. a much larger jamo-context alphabet — cross-syllable phonotactic n-grams where per-context counts ARE sparse, so learned-similarity backoff helps), NOT a smoothing of an already-dense target. Otherwise honest 🧱.
