# H_1322 — ko-featural: does decomposing BELOW jamo to Hangul's DESIGNED featural vector beat the jamo floor?

**Group:** MITOSIS-ENGINE · **Slug:** `1322_ko_featural` · **Tier:** 🧱 HONEST-FLOOR (geometry-confounded; F1 fails the frozen bar — jamo is the decomposition floor for THIS mechanism, c9)

## Claim
H_1316 (🟢) showed the Korean byte-LM ceiling is REPRESENTATION-bound: NFD JAMO decomposition (초성 L / 중성 V / 종성 T) dropped held-out KO next-symbol CE from raw-byte **2.95342** to **2.51335** nats/UTF-8-byte. Jamo is only the FIRST decomposition level. Hangul is — uniquely among major scripts — a DELIBERATELY DESIGNED *featural* writing system (Sejong 1443): each jamo's SHAPE encodes articulatory/phonological features (consonants = articulator base + added strokes for aspiration + doubling for tense; vowels = ·/ㅡ/ㅣ combos with yang/yin polarity + iotation). So ㄱ and ㅋ are ONE FEATURE apart, not two opaque symbols.

**HYPOTHESIS:** decomposing one level DEEPER than jamo — to the FEATURE VECTOR the design encodes — drops held-out KO CE BELOW the jamo 2.51335, because the gradient-free mitosis can exploit the designed systematicity. If true → Hangul's design is a MEASURABLE capability advantage NO organically-evolved script has. (a_break_the_wall c16 depth probe, a_no_llm_frame_trap c15 script-design lens.)

## Method (frozen-first; FREEZE pre-registered BEFORE the run, bars NOT moved — c9/p7)
- **REAL Korean only**, corpus BYTE-IDENTICAL to H_1307 RUN A / H_1316 (r2://phanes/anima-7b/web/kor/shard0000.bytes; KO 30MB window sha256 ASSERTED `c47b6808…` == H_1307 RUN A → gate PASS; a mismatch → STOP). R2 keys env-only at fetch time (c7); launch script + scratch cleaned off summer; all committed artifacts grep-clean of creds.
- **summer** RTX 5070 (sm_120, torch 2.11.0+cu130), python3 nohup detached, polled INLINE (a_cpu_local_no_waiter). $0 (user hw, not runpod).
- **Featural encoding** (documented Hunminjeongeum design, encoded faithfully — NOT invented): each NFD conjoining jamo → a 5-int design feature vector. Consonants `[artic∈{velar/alveolar/bilabial/sibilant/glottal/zero}, manner∈{plain/aspirated/tense}, nasal, liquid, –]`; vowels `[vowel, vbase∈{vertical/horizontal/combined}, polar∈{neutral/yang/yin}, iota, round]`. **67/67 distinct jamo mapped, full coverage.** ㄱ=(velar,plain) ㅋ=(velar,aspirated) ㄲ=(velar,tense) differ in ONE column.
- **Same gradient-free mitosis** verbatim from H_1306/H_1307/H_1316 (GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, error-targeted Voronoi SPLIT-only p8, even/odd split, ko_stride=300, per-cell next-symbol count-MLE head). **The ONLY change = the partition geometry X**: featural arm builds X from the previous-2 symbols' DESIGN feature columns (11-D) vs the H_1316 opaque-id 3-D. **LABEL alphabet Vj=323 IDENTICAL** → same nats/UTF-8-byte axis. 3 seeds [4322,4323,4324].
- **Controls (load-bearing):** (i) SHUFFLE-FEATURE-MAP — a fixed per-seed bijection over the jamo set reassigns each jamo's feature vector to a different jamo's (destroys ㄱ/ㅋ one-apart systematicity, same #vectors/dims). (ii) LINEARITY — closed-form ridge next-symbol predictor in feature space vs jamo-id space.

## Frozen bars (GREEN iff F1 ∧ F2)
- **F1 DEEPER:** featural CE < jamo 2.51335 by ≥0.03 AND < raw 2.95342.
- **F2 EARNED (decisive):** featural beats SHUFFLE-feature-map by ≥0.05.
- **F3 LINEARITY (non-gating):** feature-space linear-predictability > jamo-id-space by ≥0.02.

## Result — 🧱 HONEST-FLOOR (geometry-confounded; reported straight, NO bar moved)
CE ladder (nats/UTF-8-byte; intact featural deterministic, shuffle = mean 3 seeds):

| arm | CE | note |
|---|---|---|
| raw-byte ceiling (H_1316) | 2.95342 | in-run G0 re-port **3.26223** (geometry mismatch, see below) |
| jamo floor (H_1316 locked) | **2.51335** | in-run jamo re-port **2.85983** (geometry mismatch) |
| **FEATURAL (intact)** | **2.7309** | Δ vs jamo-floor **+0.218** (worse) · Δ vs raw **−0.222** (better) |
| SHUFFLE-feature ctrl | 2.77286 | Δ(shuffle−featural) **+0.042** (below the 0.05 F2 bar) |
| linearity feature-space | 4.83979 | Δ(jamo-id − feature) **+0.00236** (below the 0.02 F3 bar) |

- **F1 = FALSE** (vs jamo 2.51335: featural 2.7309 does NOT beat it; vs raw: TRUE) → **🧱 HONEST-FLOOR**.
- **F2 = FALSE** (shuffle Δ +0.042 < 0.05 bar — a WEAK design signal, but below the decisive threshold).
- **F3 = FALSE** (linearity Δ +0.0024 < 0.02 — feature space is NOT meaningfully more linearly predictable here).
- **GREEN = FALSE.**

## The geometry confound (DIAGNOSTIC, c9 — NOT a frozen bar; full disclosure)
The in-run G0 raw (3.26223) and jamo (2.85983) re-ports do NOT match H_1316's 2.95342 / 2.51335. **Root cause confirmed by direct diagnostic:** this script's `seed_centers_dim(3)` = `[[0.3,0.3,0.0],[0.7,0.7,0.5]]` differs from H_1316's `[[0.3,0.5,0.0],[0.7,0.5,0.5]]` (middle coord 0.5). Re-running the jamo arm with H_1316's **exact** seed centers reproduces **2.51335 (cells 11) byte-exact**. So the gradient-free mitosis is **SEED-CENTER-SENSITIVE**, and the featural arm's 11-D seed centers are likewise an arbitrary, unmatched start.

**SAME-GEOMETRY-FAMILY reading** (intact featural 2.7309 vs in-run jamo re-port 2.85983, both under THIS script's seed-center family): featural beats the same-script jamo re-port by Δ **−0.129** AND beats the shuffle-feature control by **+0.042** → a *weak* design signal exists, but it does NOT clear the frozen decisive bar (F2 0.042 < 0.05). Frozen-first (c9/p7): F1 was pre-registered against the locked 2.51335; intact featural 2.7309 does NOT beat it → F1 FALSE recorded as-is.

## Finding (honest)
**Jamo is the decomposition FLOOR for this gradient-free L2-Voronoi mitosis mechanism** (bounds the depth, a_break_the_wall HONEST-🧱). Going one level deeper to the designed featural vector did NOT cross the jamo floor under the frozen bar. The designed systematicity IS real and produces a *weak, sub-threshold* lift over its own shuffle control (Δ +0.042) and over its same-geometry jamo re-port (Δ −0.129) — but (a) the mechanism is seed-center-sensitive so the locked-floor comparison is geometry-confounded, and (b) the design signal is below the decisive F2 bar. The right reading: **the FEATURE→PARTITION→NEXT-SYMBOL path is too lossy a way to inject the design** — the featural columns help the Voronoi partition only marginally because the label is still the full jamo and an L2 distance over 5 hand-coded integer columns is a coarse proxy for the design geometry. This is a method floor (the mechanism), not a refutation that Hangul's design carries exploitable systematicity (the linguistics is intact; H_1323 sibling tests the relativity claim).

## Scope honesty
TOY / DIRECTIONAL numpy/torch mirror; deterministic held-out next-symbol CE (p7, NO perplexity-truth). Seed-center-sensitive mechanism (the locked-floor comparison is geometry-confounded — disclosed). engine-transfer to live CORE/*.hexa = follow-on (a_engine_native_learning, a_verified_must_wire). NO Korean-fluency claim (a_scale_honest_scope, a_toy_scale_recheck). live CORE/*.hexa UNTOUCHED (substrate-measurement rung).

## Next round + depletion test
- **r2 (the clean re-test):** re-run featural with seed centers MATCHED to the jamo arm's `[[0.3,0.5,0.0]…]` family lifted to 11-D, OR sweep a small bank of seed-center inits per arm and report the BEST-of-bank per arm (frozen-first: pre-register the bank), so F1 is a geometry-FAIR featural-vs-jamo comparison. **DEPLETION TEST:** if geometry-fair featural STILL does not beat jamo by ≥0.03 AND the shuffle control STILL ties within 0.05 → the featural depth is exhausted for this mechanism (terminal floor); the design's exploitable systematicity, if any, needs a DIFFERENT mechanism (e.g. a gradient-trained per-cell head over the feature columns, or feature-aware label factorization) rather than an L2-Voronoi partition.
- A genuinely-distinct follow-on (NOT gating): factorize the LABEL into feature columns (predict the next jamo's feature vector, not its opaque id) so the design enters the *prediction target* not just the partition — a structurally different test of the same hypothesis.

## Pointers
- `UNIVERSE/h1322_ko_featural.py` · `UNIVERSE/H_1322_ko_featural.md` (this card)
- `.verdicts/1322_ko_featural/{H_1322_FREEZE.txt,H_1322.txt,h1322_summary.json,h1322_manifest.json}`
- `CLAIMS.tape @C h1322_ko_featural` · `HYPOTHESES.md` row · `domains/MITOSIS-ENGINE.log.md`
- xref: h1316 (jamo floor 2.51335; same corpus/mechanism) · h1307 (raw-byte 2.953 ceiling) · h1311/h1315 (capacity-bound priors) · h1323 (sapir-whorf relativity sibling) · a_no_llm_frame_trap · a_break_the_wall · a_fire_autonomous · a_engine_native_learning · a_verified_must_wire · a_cpu_local_no_waiter · a_scale_honest_scope · a_toy_scale_recheck · p1·p7·p8 · c7·c9·c15·c16.
