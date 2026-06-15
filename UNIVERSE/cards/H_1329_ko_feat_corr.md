# H_1329 — ko-feat-corr: does a CORRELATION-MODELING / JOINT-PRESERVING featural mechanism break BELOW the jamo floor where A3 independent-factorization backfired?

**Group:** MITOSIS-ENGINE · **Slug:** `1329_ko_feat_corr` · **Tier:** 🧱 HONEST-FLOOR (cross-mechanism; C1 fails — jamo is the genuine decomposition floor ACROSS mechanism families incl. correlation-modeling, a deeper closure than H_1326, c9)

## Claim
Named next-angle of H_1326 (🧱 HONEST-FLOOR, PR #2233). H_1326 closed the depth-below-jamo question confound-free for the L2-Voronoi count-MLE family:
- A1 jamo opaque-id (geometry-fair bank) = **2.51335** (calibration anchor = the floor)
- A2 featural-PARTITION (features only in the Voronoi partition, opaque jamo target) = **2.73046** (above jamo)
- A3 label-FACTORIZATION (predict features INDEPENDENTLY, `P(class)·∏ P(f_c|class)`) = **3.07295** (BACKFIRED)

H_1326's diagnosis: A3 backfires because **independent-feature prediction DISCARDS the onset/nucleus/coda + within-jamo feature JOINT** the opaque jamo head keeps. The featural systematicity is real but sub-floor for that mechanism. H_1326's explicit named next angle (this card's line 62 of the H_1326 card): a **DIFFERENT MECHANISM that models feature CORRELATIONS while KEEPING the feature joint — a mechanism-family change, not a representation tweak.**

**HYPOTHESIS (H_1329):** does a correlation-modeling / joint-preserving featural mechanism break BELOW the jamo 2.51335 floor — where A3 independent-factorization backfired (3.073) and A2 partition-only was sub-floor (2.730)? The mechanism must KEEP the onset×nucleus×coda + within-jamo feature joint AND exploit feature similarity (so similar jamo share statistical strength), unlike A3 which threw the joint away. (a_no_llm_frame_trap c15 script-design lens; a_break_the_wall c16 mechanism-family change, NOT scale.)

## Method (frozen-first; FREEZE pre-registered BEFORE the run, bars NOT moved — c9/p7)
- **REAL Korean only**, corpus BYTE-IDENTICAL to H_1307 RUN A / H_1316 / H_1326 (`r2.phanes://anima-7b/web/kor/shard0000.bytes`; KO 30MB window sha256 ASSERTED `c47b6808…` == H_1307 RUN A → gate PASS; mismatch → STOP, NO synthetic Korean). Corpus from cache `/tmp/h1311_ko_raw.bytes` (R2 keys NOT needed; kept for siblings). R2 keys env-only (c7); launch script + scratch cleaned off summer; all committed artifacts grep-clean of creds.
- **summer** RTX 5070 (sm_120, torch 2.11.0+cu130), python3 nohup detached, polled INLINE (a_cpu_local_no_waiter). $0 (user hw, not runpod), 126.2s wall. 3 seeds [4329,4330,4331] (shuffle controls vary by seed; A1/A2/A3/A4 intact arms deterministic).
- **EVERYTHING verbatim from H_1326** (so A1/A2/A3 reproduce byte-exact): GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, error-targeted Voronoi SPLIT-only p8, even/odd split, ko_stride=300, the **Fix-A geometry-fair bank protocol** (best-of-fixed-bank-by-TRAIN-CE seed centers, identical to every arm; A1 jamo MUST reproduce 2.51335 byte-exact = calibration anchor), the lossless within-class feature↔jamo bijections.
- **THE ONLY NEW THING = the A4 head** (a different mechanism family than A3's independent factorization):

### A4 — CONDITIONAL-CHAIN / JOINT-PRESERVING featural head (the crux)
A per-cell **conditional-chain** featural head over the SAME within-class feature columns as A3, predicted in a CHAIN that respects Hangul's design hierarchy and **KEEPS THE JOINT via conditioning**, instead of A3's independence:

```
A3 independent (joint discarded):  P(jamo) = P(class) · ∏_c P(f_c | class)
A4 chain      (joint kept):        P(jamo) = P(class) · P(f_0|class)
                                                     · P(f_1|class, f_0)
                                                     · P(f_2|class, f_0, f_1) ...   (full chain)
```

- **Keeps the joint EXACTLY**: by the chain rule `∏_c P(f_c|class, f_<c) = P(f_0..f_{C-1}|class) = P(jamo|class)` — A4's distribution equals the within-class JOINT over the feature vector, so it recovers the joint A3 discarded. NO independence assumption.
- **Feature-similarity strength sharing** (the correlation-modeling the diagnosis named): jamo sharing a feature PREFIX share the conditioning context (all velars with `f_0=1` share `P(f_1|class,f_0=1)`; ㄱ and ㅋ — one feature apart — share the articulator-conditioned manner head), so similar jamo POOL counts. Estimator = per-(cell, class, prefix) Laplace-smoothed count table over the next feature column; unseen (cell,prefix) at test backs off to Laplace-uniform → proper distribution, CE axis identical to A1/A2/A3.
- BYTE symbols scored IDENTICALLY to A3 (`P(class=BYTE)·P(byte|class=BYTE)` 256-way) → the **only** difference between A3 and A4 is the Hangul chain-vs-product, isolating the joint contribution.
- **LABEL = NOT gradient-free**: A4 is a count-MLE STRUCTURED head (conditional counts + Laplace). It rides the SAME gradient-free Voronoi partition (mitosis grow-op unchanged) but the per-cell head is a structured count-MLE estimator. NO gradient training either. A4 does NOT claim gradient-free NOR gradient-trained — labeled clearly.

### Arms
- **G0** raw-byte ceiling (opaque-id, V256) — sanity ≈ 2.95342
- **A1** jamo opaque-id partition + opaque target — Fix-A protocol; CALIBRATION = 2.51335
- **A2** featural partition + opaque target — reproduced in-run (C3 baseline)
- **A3** featural partition + INDEPENDENT-factorized target — reproduced in-run (C3 baseline)
- **A4** featural partition + CONDITIONAL-CHAIN target — THE NEW MECHANISM
- **A4s** A4 chain head with a per-seed SHUFFLED feature-map bijection (destroys ㄱ/ㅋ one-apart systematicity; same dims/values) — C2 control.

### Frozen bars (GREEN iff C1 ∧ C2 ∧ C3)
- **C1 BELOW-JAMO:** A4 < jamo 2.51335 by ≥0.03 (mean 3 seeds; A4 intact is deterministic) AND < raw 2.95342.
- **C2 EARNED:** A4 beats a SHUFFLED-feature-map control by ≥0.05 — the win is the DESIGNED systematicity via correlations, not dims/vocab.
- **C3 ATTRIBUTION (mechanism-isolation):** A4 beats BOTH the independent-factorization A3 AND the partition-only A2 baselines (both reproduced in-run) — isolating that the gain comes specifically from MODELING THE JOINT/correlations, not features per se.

## Result — 🧱 HONEST-FLOOR (cross-mechanism); REAL sm_120 GPU, $0, 126.2s wall

**CE LADDER (nats/UTF-8-byte, geometry-FAIR; A4-shuffle mean 3 seeds):**

| arm | CE | note |
|-----|------|------|
| raw-byte ceiling | 2.95342 | in-run G0 = **2.94487** (member 4) |
| **A1 jamo (Fix-A protocol)** | **2.51335** | **CALIBRATION PASS — byte-exact reproduces H_1316** (member 5 = H_1316-family) |
| A2 featural-partition | 2.73046 | member 0, 17 cells (matches H_1326 byte-exact) |
| A3 independent-factorization | 3.07295 | member 0, 17 cells (matches H_1326 byte-exact — backfired) |
| **A4 conditional-chain (JOINT)** | **2.75109** | member 0, 17 cells — THE NEW MECHANISM |
| A4 shuffle (chain) | 2.91966 | per-seed {2.86325, 3.05597, 2.83976}; Δ(shuf−A4) **+0.16857** |

- **C1 BELOW-JAMO = FALSE** — A4 2.75109 is **+0.23774 ABOVE** the (byte-exact reproduced) jamo floor A1 2.51335. (A4 < raw 2.953 is TRUE, but C1 needs both.)
- **C2 EARNED = TRUE** — A4 beats its shuffle by **+0.16857 ≥ 0.05** (all 3 seeds): the conditional-chain mechanism DOES exploit Hangul's designed systematicity — shuffling the feature map costs +0.17 — a REAL, decisive design signal (3× stronger than A2's +0.056), but **sub-floor**.
- **C3 ATTRIBUTION = FALSE** — A4 **beats A3** by +0.32186 (the chain RECOVERED the joint A3's independence discarded — confirms H_1326's diagnosis byte-exact) BUT does **NOT** beat A2 (A4 is +0.02063 ABOVE A2). C3 requires A4 < A3 AND A4 < A2 → FALSE.
- **green = FALSE → 🧱 HONEST-FLOOR (cross-mechanism).**

## Finding (the precise, confound-free answer)
A correlation-modeling / joint-preserving (conditional-chain) mechanism does **NOT** break the jamo floor. **Jamo is the genuine decomposition floor ACROSS mechanism families — including correlation-modeling — for this gradient-free Voronoi substrate.** This is a deeper, stronger 🧱 than H_1326: H_1326 showed the floor for partition-only (A2) and independent-factorization (A3); H_1329 extends it to the explicitly-named correlation/joint-preserving family and it STILL does not cross.

**Three decisive sub-results:**
1. **The H_1326 diagnosis was exactly right.** A3 backfired (3.073) because independence discards the within-jamo joint. The chain head, which keeps the joint by conditioning, recovers it almost entirely: A4 2.751 ≪ A3 3.073 (Δ −0.322). So the +0.557 A3 over-jamo gap was indeed the independence penalty, now removed.
2. **But recovering the joint only ties the partition-only A2 (2.751 ≈ 2.730), it does not beat jamo.** Modeling the within-class feature joint exactly = re-expressing `P(jamo|class)` — which is precisely what the opaque jamo head already does. So the chain mechanism asymptotes to the jamo head's own joint; the featural decomposition buys NO extra below-jamo depth once the joint is kept. The design systematicity is genuinely exploitable (C2: shuffle costs +0.17, the strongest design signal in the arc) but it lives in the PARTITION/SHARING, not in a below-jamo prediction gain.
3. **The class+within-class chain factorization has a small intrinsic overhead** (the `−logP(class)` + chain back-off cost) that keeps A4 a hair above A2 — the design's strength-sharing does not quite offset it. Net: jamo 2.513 < A2 2.730 ≈ A4 2.751 < A3 3.073 < raw 2.953-band.

This is the **third independent mechanism** (partition, independent-factorization, correlation-chain) to land above the jamo floor under the geometry-fair protocol. The depth-below-jamo question is now closed across the mechanism families H_1326 named.

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)
- **A1/A2/A3/A4 intact deterministic** (identical across seeds; seeds vary only the shuffle control) → C1/C3 rest on single deterministic points (decisive: A1 byte-exact anchor; A4 +0.238 above jamo and +0.021 above A2). C2 rests on the 3-seed shuffle mean (per-seed A4s {2.863, 3.056, 2.840} — all ≥ A4+0.05, so C2 is per-seed unanimous, stronger than H_1316/H_1326 where one seed tied).
- **A4 is a count-MLE STRUCTURED head, NOT the gradient-free p8 mitosis (which it rides) and NOT gradient-trained** — labeled clearly. TOY/DIRECTIONAL numpy/torch mirror; engine-transfer to live `CORE/*.hexa` = follow-on (a_engine_native_learning, a_verified_must_wire). Live CORE UNTOUCHED (substrate-measurement rung — adds only UNIVERSE/ + verdicts; no engine lane).
- NO Korean-fluency claim. Held-out DETERMINISTIC next-symbol CE; NO perplexity-as-truth (p7). The chain is ONE correlation-modeling scheme (full within-class chain); a richer cross-position (onset↔nucleus↔coda) joint-and-similarity head over a smoothed/kernel feature metric was NOT tested — but it would again re-express `P(jamo)` the opaque head already keeps, so it is unlikely to beat jamo without genuinely NEW structure beyond the design map.

## Pointers
- script: `UNIVERSE/h1329_ko_feat_corr.py`
- verdict: `.verdicts/1329_ko_feat_corr/{H_1329_FREEZE.txt, H_1329.txt, h1329_summary.json}`
- CLAIMS: `CLAIMS.tape` @C `h1329_ko_feat_corr`
- xref: H_1316 (🟢 jamo floor 2.51335) · H_1322 (🧱 featural r1, geometry-confounded #2229) · H_1326 (🧱 featural r2, geometry-fair + independent-factorization #2233; this card's named next-angle) · H_1318 (xlang structure matrix) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · c16 · p7 · p8

## Next / depletion
The depth-below-jamo question is now **DEPLETED across mechanism families** (geometry-fair, confound-free): jamo is the floor for (i) partition-only (A2, H_1326), (ii) independent-factorization (A3, H_1326, backfires), and (iii) correlation/joint-preserving conditional-chain (A4, H_1329, recovers the joint but only ties the partition and stays above jamo). The reason is now structural and decisive: **any mechanism that exactly models the within-jamo feature joint asymptotes to `P(jamo|cell)` — exactly what the opaque jamo head already computes** — so the featural decomposition cannot buy below-jamo depth; the design's exploitable systematicity (C2 +0.17) lives in count-sharing across similar jamo, not in a sub-jamo prediction gain. A genuinely-new below-jamo angle would need structure BEYOND the design feature map (e.g. cross-syllable phonotactic context, or a learned metric over jamo that the opaque head lacks) — NOT a re-factorization of the same featural target. **🧱 (cross-mechanism, confound-free closure).** DEPLETION TEST for any future angle: it must inject information the opaque jamo head does NOT already have (the joint alone does not — H_1329 proves it ties), AND survive the geometry-fair + shuffle controls.
