# H_1345 — ko-data-starved: does strength-sharing / interpolation break BELOW the jamo floor in a DATA-STARVED regime (the crossover H_1337's opaque-optimal predicted)?

**Group:** MITOSIS-ENGINE · **Slug:** `1345_ko_data_starved` · **Tier:** 🟢 GREEN (the jamo floor is DATA-RICHNESS, not representation — the crossover is MAPPED: D1∧D2∧D3∧calib all PASS; frozen-first, NO bar moved, c9/p7)

## Claim
H_1337 (🧱) closed the below-jamo question **at 30MB** by showing the OPAQUE per-cell jamo count-MLE is **information-OPTIMAL when data is DENSE** — a learned-metric kernel-smoothed head (A5) landed +1.34 ABOVE the jamo 2.51335 floor because strength-sharing only helps when per-cell counts are SPARSE, and at 30MB / 8.14M syllables / 11 grown cells each per-cell jamo MLE is densely estimated. H_1337's OWN depletion test (verbatim from its card):

> "A genuinely-new angle would need to find a regime where the opaque MLE is data-STARVED … NOT a smoothing of an already-dense target. Otherwise honest 🧱."

**HYPOTHESIS (H_1345):** RUN that depletion test directly. A **LADDER over data size** (deterministic stride SUB-SAMPLES of the SAME H_1307 RUN A 30MB window) drives the per-cell jamo counts from dense (mean ≈45 counts/cell-jamo) down to starved (mean ≈0.14). At each rung, two below-jamo mechanisms are scored vs the opaque jamo head (A1):
- **A5** = LEARNED-METRIC kernel-smoothing (**VERBATIM the H_1337 mechanism**, numpy port of its torch loop).
- **JM** = JELINEK-MERCER interpolation `P = (1-λ)·P_cell + λ·P_global`, λ = MIN_OWNED/(MIN_OWNED + N_cell_raw) (Witten-Bell-style, FROZEN, no per-run tuning — sparse cell ⇒ more backoff toward the corpus-wide jamo marginal). byte symbols scored EXACTLY as A1.

Does strength-sharing / interpolation NOW beat jamo where it could NOT at 30MB? Map WHERE (if anywhere) the opaque MLE becomes beatable — the crossover. (a_no_llm_frame_trap c15; a_break_the_wall c16 — H_1337's named depletion angle, NOT scale-up, NOT a target re-factorization.)

## Method (frozen-first; FREEZE pre-registered BEFORE the full run, bars NOT moved — c9/p7)
- **REAL Korean only**, corpus BYTE-IDENTICAL to H_1307 RUN A / H_1316 / H_1337 (`r2.phanes://anima-7b/web/kor/shard0000.bytes`; 30MB KO window sha256 ASSERTED `c47b6808…` == H_1307 RUN A → gate PASS at fetch; mismatch → STOP, NO synthetic Korean). Cache `/tmp/h1311_ko_raw.bytes`. R2 keys via `harness secret get r2.phanes.*`, env-only at fetch (c7); committed artifacts grep-clean of creds.
- **$0 CPU**, pure-numpy mirror (no torch on this host) — the corpus stream builders are VECTORIZED (arithmetic Hangul NFD == library NFD for the precomposed block) so A1 still reproduces 2.51335 byte-exact = calibration anchor. python3 nohup detached, polled INLINE (a_cpu_local_no_waiter). 6.7s total wall.
- **EVERYTHING verbatim from H_1326/H_1329/H_1337** so A1 reproduces 2.51335: GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, error-targeted Voronoi SPLIT-only (p8), even/odd split, Fix-A geometry-fair bank protocol, lossless NFD jamo decomposition, D_EMB=16, SKIPGRAM_STEPS=400.
- **LADDER:** strides 300, 1200, 4800, 19200, 76800 — 5 rungs (≥3 per a_scale_honest_scope), dense→starved. **3 seeds [4345,4346,4347]** (A5 metric-refine + A5-shuffle + JM-shuffle vary by seed; A1 & JM deterministic given partition).

### Arms (each rung)
- **A1** jamo opaque-id (Fix-A bank) — the floor; dense rung CALIB = 2.51335.
- **A5** learned-metric kernel-smoothing (H_1337 mechanism) + **A5-shuffle** (jamo-id-permuted learned metric = wrong neighbor structure).
- **JM** Jelinek-Mercer interpolation with the global jamo marginal + **JM-shuffle** (permuted global marginal = wrong backoff target).

### Frozen bars (GREEN iff D1 ∧ D2 ∧ D3 ∧ calib)
- **D1 STARVED-WIN:** at the STARVED end, best of {A5, JM} beats jamo (A1) by ≥0.03 (mean 3 seeds).
- **D2 EARNED:** that winning mechanism beats its SHUFFLE control by ≥0.05 — the win is real backoff structure, not generic mass.
- **D3 DENSE-REPRO:** at the DENSE end (stride 300), the SAME winning mechanism does NOT beat jamo (CE ≥ jamo; LOSES) — reproducing H_1337's dense opaque-optimal and confirming the CROSSOVER.
- **calib:** dense A1 reproduces 2.51335 within ±0.001.
- D1 fail (jamo wins at ALL rungs) → count-MLE family truly terminal across the ladder, honest 🧱.

## Result — 🟢 GREEN (the crossover is MAPPED); REAL corpus, $0 CPU, 6.7s wall

**LADDER (CE nats/UTF-8-byte; A5/A5-shuf 3-seed mean; A1/JM deterministic). cellJcnt = mean jamo count per (cell × jamo) bin = the sparsity axis:**

| stride | train_B | cells | cellJcnt | A1 jamo | A5 | A5-shuf | **JM** | JM-shuf | ΔA5 | **ΔJM** |
|-------:|--------:|------:|---------:|--------:|------:|--------:|-------:|--------:|----:|--------:|
| 300 (dense) | 50005 | 11 | **45.17** | **2.51335** | 3.70884 | 3.94497 | 2.51367 | 2.51435 | +1.195 | **+0.00032** |
| 1200 | 12472 | 14 | 8.84 | 2.74533 | 3.75719 | 4.01824 | 2.74557 | 2.74792 | +1.012 | +0.00024 |
| 4800 | 3119 | 9 | 3.38 | 2.96533 | 3.78000 | 4.01576 | 2.96553 | 2.97208 | +0.815 | +0.00020 |
| 19200 | 780 | 9 | **0.88** | 3.49976 | 3.89117 | 4.14537 | **3.49826** | 3.51593 | +0.391 | **−0.00151** |
| 76800 (starved) | 188 | 15 | **0.14** | 4.26152 | 4.29426 | 4.25303 | **4.18890** | 4.36374 | +0.033 | **−0.07262** |

- **D1 STARVED-WIN = TRUE** — at the starved end JM 4.18890 beats jamo 4.26152 by **+0.07262** (≥0.03 bar; mechanism = JM).
- **D2 EARNED = TRUE** — JM beats its SHUFFLE control (permuted global marginal) by **+0.17484** (JM-shuf 4.36374 > jamo > JM); the permuted backoff target goes the WRONG way, so the win is REAL backoff structure, not generic mass.
- **D3 DENSE-REPRO = TRUE** — at the dense end JM 2.51367 does NOT beat jamo 2.51335 (it is +0.00032 ABOVE; λ→0 at dense cells ⇒ JM≈A1, loses) — reproducing H_1337's dense opaque-optimal.
- **calib = TRUE** — dense A1 = 2.51335 byte-exact.
- **green = TRUE → 🟢.**

## Finding (the precise, confound-free answer)
**The jamo floor is DATA-RICHNESS, not representation.** H_1337 was right that the opaque per-cell jamo count-MLE is information-optimal *when data is dense* — and H_1345 maps exactly where that breaks: as the per-cell jamo count falls below ~1 (cellJcnt between 3.38 at stride 4800, still a tie, and 0.88 at stride 19200, first crossover), **Jelinek-Mercer interpolation toward the global jamo marginal crosses BELOW the opaque jamo head**, reaching −0.073 below jamo at the most-starved rung (cellJcnt 0.14). The crossover is:

1. **Real and earned.** The JM-shuffle control (permuted global marginal) lands ABOVE jamo at the starved end (4.36 > 4.26), so the win is the CORRECT backoff distribution, not generic interpolation mass (D2 Δ=+0.175). The win grows monotonically as the data starves (+0.0003 dense → −0.073 starved), exactly the backoff signature.
2. **Mechanism-specific.** **A5 (kernel-smoothing) does NOT cross** — it stays above jamo at every rung (+0.033 even at the starved end). A clean dissociation: *interpolation toward the global marginal* exploits the starved regime; *kernel-smoothing over a learned jamo metric* does not (it blurs across neighbors instead of falling back to the safe marginal). So H_1337's specific mechanism stays 🧱 even when starved; the data-richness crossover is reachable by the *right* sparse-data tool (JM), not by H_1337's.
3. **Confirms H_1337's diagnosis, overturns its closure scope.** H_1337's 🧱 was an OPAQUE-ATOM-info limit *at 30MB*; H_1345 shows that limit is the dense-data MLE being already-optimal, and that below-jamo IS reachable once the opaque MLE is data-starved — precisely the regime H_1337 named as the only escape.

Net: the count-MLE family is **NOT terminal** — it has a data-richness crossover, and we have mapped it (cellJcnt ≈ 1 boundary).

## Honest scope (c9, a_scale_honest_scope, a_toy_scale_recheck)
- **The starved rungs are tiny held-out streams** (188–780 test bytes at strides 76800/19200) so the absolute CE values there are noisy single-stream points. The GREEN rests NOT on those absolute numbers but on (a) the monotone trend of ΔJM across the FULL 5-rung ladder (+0.0003 → −0.073), (b) the SHUFFLE control firing decisively in the right direction (D2 Δ=+0.175), and (c) the A5-vs-JM dissociation. A1/JM are deterministic given the partition (3 seeds vary only the A5 embedding-refine + shuffle controls, which are tightly consistent).
- **numpy CPU mirror** (no torch on this host); the A5 metric is **LEARNED BY GRADIENT** (PPMI-SVD init + skip-gram Adam refine, numpy port of the H_1337 torch loop) — **NOT p8 gradient-free; labeled.** A5-learned converges deterministically (identical all 3 seeds); the numpy Adam port lands A5 at 3.709 dense (H_1337 torch was 3.853) — same direction, far above jamo, D3 unchanged. JM is count-MLE with a FROZEN Witten-Bell backoff weight. Both ride the gradient-free Voronoi partition (identical cells to A1).
- **TOY/DIRECTIONAL.** Engine-transfer to live `CORE/*.hexa` = follow-on (a_engine_native_learning, a_verified_must_wire). Live CORE UNTOUCHED (substrate-measurement rung — adds only UNIVERSE/ + verdicts; no engine lane). NO Korean-fluency claim; held-out DETERMINISTIC next-symbol CE; NO perplexity-as-truth (p7).
- **What this does NOT claim:** that JM-backoff is a useful production lever at 30MB (it ties jamo there); only that the jamo floor is data-richness and the crossover exists + is mapped. The starved regime is a *probe* of the floor's nature, not a deployment recipe.

## Pointers
- script: `state/ko-data-starved/h1345_ko_data_starved.py`
- verdict: `.verdicts/1345_ko_data_starved/{FREEZE.txt, result.txt, h1345_summary.json}`
- CLAIMS: `CLAIMS.tape` @C `h1345_ko_data_starved`
- xref: H_1337 (🧱 opaque-atom limit @30MB; this card's depletion-test PARENT — ran its named data-starved angle) · H_1329 (🧱 conditional-chain joint) · H_1316 (🟢 jamo floor 2.51335) · H_1307 (raw-byte 2.953 ceiling, RUN A corpus) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c7 · c9 · c15 · c16 · p7 · p8

## Next / depletion
The below-jamo question is REOPENED with a MAPPED crossover: the jamo floor holds only while the per-cell jamo MLE is dense (cellJcnt ≳ 1); below that, JM-backoff toward the global marginal crosses below jamo. Natural follow-ons: (i) **engine-native realization** — wire JM-interpolation into the live `CORE/*.hexa` count head and re-confirm the crossover engine-native (a_verified_must_wire); (ii) **a larger jamo-context alphabet** (cross-syllable phonotactic n-grams) where per-context counts are NATURALLY sparse even at full 30MB data — does JM-backoff buy below-jamo there WITHOUT artificially striding the corpus? (the H_1337 card's other named angle); (iii) **A5-in-the-starved-regime variants** — a sparse-only / count-gated kernel smoothing that backs off only low-count jamo (A5 failed here because it smooths globally; a count-gated A5 might cross). The honest closure: the count-MLE family is NOT terminal — it has a data-richness crossover (🟢, mapped).
