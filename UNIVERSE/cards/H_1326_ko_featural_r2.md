# H_1326 — ko-featural r2: is jamo the genuine, confound-free decomposition floor (geometry-fair + label-factorization)?

**Group:** MITOSIS-ENGINE · **Slug:** `1326_ko_featural_r2` · **Tier:** 🧱 HONEST-FLOOR (confound-free; G1 fails geometry-fair — jamo is the genuine decomposition floor for THIS mechanism family, c9)

## Claim
r2 of H_1322 (🧱 HONEST-FLOOR, PR #2229), whose r1 agent DISCLOSED two confounds (c16 / a_break_the_wall = wrong method, NOT a real wall):
1. **GEOMETRY CONFOUND** — r1's `seed_centers_dim(3)=[[0.3,0.3,0.0],[0.7,0.7,0.5]]` differed from H_1316's exact centers `[[0.3,0.5,0.0],[0.7,0.5,0.5]]` (middle coord 0.5); the gradient-free mitosis is SEED-CENTER-SENSITIVE, so r1's in-run jamo re-port was 2.85983 (NOT the locked 2.51335). The featural-vs-locked-jamo comparison was geometry-confounded.
2. **LOSSY PATH** — features drove ONLY the Voronoi PARTITION; the prediction TARGET stayed the OPAQUE jamo id, so Hangul's designed systematicity never entered the TARGET.

This lane fixes BOTH, pre-registered frozen-first, and asks the clean question: **once the test is geometry-fair AND the design can enter the prediction target, does Hangul's featural design give a measurable depth advantage BELOW the jamo floor 2.51335, or is jamo the genuine confound-free floor?** (a_no_llm_frame_trap c15 script-design lens, NOT scale.)

## Method (frozen-first; FREEZE pre-registered BEFORE the run, bars NOT moved — c9/p7)
- **REAL Korean only**, corpus BYTE-IDENTICAL to H_1307 RUN A / H_1316 (`r2://phanes/anima-7b/web/kor/shard0000.bytes`; KO 30MB window sha256 ASSERTED `c47b6808…` == H_1307 RUN A → gate PASS; mismatch → STOP). R2 keys env-only (c7); launch script + scratch cleaned off summer; cache `/tmp/h1311_ko_raw.bytes` preserved for siblings; all committed artifacts grep-clean of creds.
- **summer** RTX 5070 (sm_120, torch 2.11.0+cu130), python3 nohup detached, polled INLINE (a_cpu_local_no_waiter). $0 (user hw, not runpod). 3 seeds [4326,4327,4328] (perturb the shuffle control only; A1/A2/A3 deterministic).
- **MITOSIS FROZEN verbatim** from H_1306/H_1307/H_1316 (GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, error-targeted Voronoi SPLIT-only p8, even/odd split, ko_stride=300). The ONLY changes = (A) the geometry-fair bank protocol and (B) the optional label-factorization scoring head.

### Fix A — GEOMETRY-FAIR seed-center protocol (identical to EVERY arm)
ONE pre-registered **best-of-a-fixed-bank-by-TRAIN-CE** protocol, applied IDENTICALLY to every arm. For partition-dim `d`, the bank = a FROZEN 5-pattern grid + the H_1316-FAMILY member (body 0.3/0.7, interior coords pinned to 0.5, last coord 0.0/0.5) lifted to `d`. The winner is the member with the lowest TRAIN held-out CE (even/odd within train — NO test peeking); that ONE is scored on TEST. Same bank rule + same selection criterion for every arm → no per-arm seed-center advantage. **CALIBRATION ANCHOR:** the jamo arm under this protocol MUST reproduce H_1316's 2.51335 byte-exact (the H_1316-family member is in its bank and is its best).

### Fix B — LABEL-FACTORIZATION (the deeper test — design enters the TARGET)
A second scoring head whose TARGET is the FACTORED feature vector, not the opaque jamo id: per cell, predict (a) the next symbol's CLASS c∈{INITIAL,MEDIAL,FINAL,BYTE} via count-MLE, then (b) GIVEN the class, predict each design feature COLUMN INDEPENDENTLY via per-column count-MLE, then COMPOSE: `−logP(jamo) = −logP(class) + Σ_col −logP(feat_col|class)`. The within-class (feature tuple)↔(jamo id) maps are pre-verified **LOSSLESS BIJECTIONS** (initial 19, medial 21, final 27 — all distinct tuples) so the factored distribution is honestly comparable on the SAME jamo alphabet and nats/UTF-8-byte axis. The independence is a MODELLING choice (an UPPER BOUND on the joint) — exactly the test: does factorizing a hard ~51-way choice into easy low-cardinality choices PAY OFF?

### Arms
- **G0** raw-byte ceiling (opaque-id, V256) — sanity ≈ 2.95342
- **A1** jamo opaque-id partition + opaque target — Fix-A protocol; CALIBRATION = 2.51335
- **A2** featural partition + opaque target — Fix A only (r1's arm, now geometry-fair)
- **A3** featural partition + FACTORIZED target — Fix A + Fix B (design in partition AND target)
- **A2s/A3s** same arms with a per-seed SHUFFLED feature-map bijection (destroys ㄱ/ㅋ one-apart systematicity; same dims/values) — controls.

### Frozen bars (GREEN iff G1 ∧ G2)
- **G1 GEOMETRY-FAIR DEPTH:** BEST=min(A2,A3) beats the jamo arm A1 by ≥0.03 (mean 3 seeds) AND beats raw 2.953.
- **G2 EARNED:** BEST beats its OWN shuffled-feature control by ≥0.05 — the gain is the DESIGNED systematicity, not dims/vocab.
- **G3 FACTORIZATION-ATTRIBUTION** (diagnostic, reported even if non-gating): does A3 beat A2? Isolates whether the design pays off in the TARGET (Fix B) vs the PARTITION (Fix A).

## Result — 🧱 HONEST-FLOOR (confound-free); REAL sm_120 GPU, $0, 79.1s wall

**CE LADDER (nats/UTF-8-byte, geometry-FAIR; shuffle mean 3 seeds):**

| arm | CE | note |
|-----|------|------|
| raw-byte ceiling | 2.95342 | in-run G0 = **2.94487** (member 4) |
| **A1 jamo (Fix-A protocol)** | **2.51335** | **CALIBRATION PASS — byte-exact reproduces H_1316** (member 5 = H_1316-family) |
| A2 featural-partition | 2.73046 | member 0, 17 cells |
| A3 label-factorization | 3.07295 | member 0, 17 cells |
| A2s shuffle (featural) | 2.78694 | Δ(shuf−A2) **+0.05648** |
| A3s shuffle (factorized) | 4.28914 | Δ(shuf−A3) +1.21619 |
| **BEST = A2** | **2.73046** | shuffle-of-best = 2.78694 |

- **G1 GEOMETRY-FAIR DEPTH = FALSE** — BEST 2.73046 does NOT beat the (now byte-exact reproduced) jamo floor A1 2.51335; it is **+0.217 ABOVE** it. (BEST < raw 2.953 is TRUE, but G1 requires both.)
- **G2 EARNED = TRUE** — A2 beats its shuffle by +0.05648 ≥ 0.05: the featural partition carries a REAL but **sub-floor** design signal (consistent with r1's same-geometry +0.042 reading, now decisively above the bar under the fair protocol).
- **G3 FACTORIZATION = FALSE** — A3 (3.07295) does NOT beat A2 (2.73046); Δ −0.3425. Putting the design into the TARGET via independent-feature factorization makes it WORSE (the per-column independence assumption discards the cross-feature joint that the opaque jamo head keeps intact).
- **green = FALSE → 🧱 HONEST-FLOOR.**

## Finding (the precise, confound-free answer)
With the geometry confound ELIMINATED (jamo arm reproduces 2.51335 byte-exact under a bank protocol applied identically to every arm), **jamo is the genuine decomposition floor for this L2-Voronoi gradient-free mechanism family.** Hangul's designed featural systematicity IS real and IS exploitable (G2: shuffling it costs +0.056 in the partition; +1.22 in the factorized target) — but it does NOT push CE below the jamo floor, in EITHER the partition (A2 +0.217 above) OR the target (A3 +0.557 above; factorization HURTS). The r1 sub-bar signal was not a hidden win waiting for a fair test; it was the real ceiling of what feature-geometry buys this mechanism. The r1 🧱 stands, now confound-free: a clean honest closure.

WHY the target-factorization (Fix B) BACKFIRES (the precise structural reason): the opaque-jamo head predicts the FULL joint over 51 jamo from each cell's empirical co-occurrence; the factorized head assumes the design features are conditionally INDEPENDENT given the cell, which they are NOT (Korean phonotactics couple onset/nucleus/coda). The independence penalty (Σ of per-column surprisals ignoring their correlation) exceeds the cardinality-reduction benefit. So the design pays off NEITHER below jamo NOR in the target — a precise result, not a confound.

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)
- **A1/A2/A3 deterministic** (identical across seeds; seeds vary only the shuffle controls) → G1/G3 rest on single deterministic points (decisive: A1 byte-exact anchor, A2/A3 both far above). G2 rests on the 3-seed shuffle mean (per-seed A2s ∈ {2.851, 2.783, 2.727} — seed 4328 ties A2, so G2-vs-A2 leans on the mean, same caveat as H_1316).
- **TOY/DIRECTIONAL** numpy/torch mirror; engine-transfer to live `CORE/*.hexa` = follow-on (a_engine_native_learning, a_verified_must_wire). Live CORE UNTOUCHED (substrate-measurement rung — adds only UNIVERSE/ + verdicts; no engine lane).
- NO Korean-fluency claim. The independence-factorization is ONE factorization scheme; a NON-independent (e.g. autoregressive over the 3 feature axes) target head was NOT tested — but that would re-introduce the joint the opaque head already keeps, so it is unlikely to beat jamo without new structure.
- Held-out DETERMINISTIC next-symbol CE; NO perplexity-as-truth (p7).

## Pointers
- script: `UNIVERSE/h1326_ko_featural_r2.py`
- verdict: `.verdicts/1326_ko_featural_r2/{H_1326_FREEZE.txt, H_1326.txt, h1326_summary.json}`
- CLAIMS: `CLAIMS.tape` @C `h1326_ko_featural_r2`
- xref: H_1316 (🟢 jamo floor 2.51335) · H_1322 (🧱 featural r1, geometry-confounded #2229) · H_1318 (xlang structure matrix) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · c16 · p7 · p8

## Next / depletion
The depth-below-jamo question for the L2-Voronoi mechanism is now **DEPLETED** confound-free: jamo is the floor; the design's systematicity is exploitable but sub-floor; target-factorization (independent features) backfires. A genuinely-new angle would need a DIFFERENT mechanism (not L2-Voronoi count-MLE) that can exploit feature systematicity WITHOUT discarding the onset/nucleus/coda joint — e.g. an engine-native mitosis variant whose head models feature correlations. That is a mechanism-family change, not a representation tweak. **🧱 (confound-free closure).**
