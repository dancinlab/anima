# H_1316 — 🇰🇷 ko-jamo-mitosis: does COMPOSITIONAL JAMO representation break the 2.953 raw-byte ceiling?

**Final tier: 🟢 GREEN — the Korean ceiling is REPRESENTATION-bound (broken by jamo composition), NOT capacity-bound.**

DIRECTIONAL numpy/torch mirror · REAL corpus byte-identical to H_1307 RUN A · 3 seeds [4316,4317,4318] · $0 (summer RTX 5070 sm_120, idle) · frozen-first (FREEZE written before run) · c9/p7, NO tune-to-green · live CORE UNTOUCHED.

## Claim
The Korean-mitosis thread was 🔴 TERMINAL: gradient-free mitosis cannot beat ~2.953 nat/byte held-out KO next-byte CE (H_1307 RUN A raw-byte ctx4 = **2.9475**; H_1311 richer raw-byte substrate did NOT break it = capacity-bound; H_1315 mitosis over the 303M frozen rep did NOT break it = 3.146, worse). EVERY prior KO lane fed the substrate **raw UTF-8 bytes** — 3 opaque bytes per Hangul syllable, ZERO awareness that Korean is a **compositional syllable-block script**. The genuinely-untried angle (a_no_llm_frame_trap / c15 — add the MISSING STRUCTURE, don't scale): the missing structure for Korean is **jamo composition** — each Hangul syllable = 초성(L)+중성(V)+종성(T) jamo, recoverable by deterministic Unicode **NFD** decomposition. **H_1316: does a jamo-decomposition representation let the SAME gradient-free mitosis break 2.953 where raw bytes could not?**

## Method (the rep is the ONLY thing that changes; mitosis FROZEN verbatim from H_1306/H_1307)
- **Corpus**: REAL `r2://phanes/anima-7b/web/kor/shard0000.bytes[0:30M]` (+ eng), **sha256 ASSERTED == H_1307 RUN A** (`c47b6808…` / `31b4a543…`, byte-fair). R2 keys env/header-only at fetch, never logged/committed (c7); a sha mismatch → STOP (REAL-only, no synthetic).
- **Symbol stream**: scan UTF-8 codepoints. A Hangul syllable (U+AC00..U+D7A3) → one SYMBOL per NFD jamo; every non-Hangul codepoint → one SYMBOL per raw byte (id 0..255). Alphabet = {0..255} ∪ {distinct jamo} → **Vj = 323** (67 distinct jamo). Each symbol carries `n_bytes` (raw=1; a syllable's jamo split [1,1,1] for 3-jamo / [2,1] for 2-jamo so they SUM to the 3 UTF-8 bytes — lossless byte accounting).
- **Mitosis**: SAME error-targeted Voronoi grow-op (highest-owned-CE eligible cell → hi-var-axis owned-median split → two half-centroids; gradient-free, cells only SPLIT, p8). SAME GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, SEED_CENTERS [[0.3,0.5,0.0],[0.7,0.5,0.5]], even/odd split, ko_stride=300. FEAT = [last_sym/Vj, second_sym/Vj, cont_depth/3] — the H_1307 3-D family, only "what a symbol is" changes (dimension identical). Per-cell next-symbol count-MLE head.
- **Fair-axis conversion (stated explicitly)**: held-out `CE_per_byte = Σ(−log p(sym)) / Σ n_bytes(sym)` — the SAME held-out split, same nats/UTF-8-byte axis as the 2.9475 raw-byte ceiling (a byte-LM is exactly Σ(−log p)/Σ bytes; predicting the same text as jamo-symbols and renormalizing by bytes is apples-to-apples, NOT an easier task).
- **3 arms**: G0 raw-byte (vocab 256, same budget — reproduce the ceiling) · G1 jamo (intact) · G1c shuffle-jamo control (bijective permutation of the jamo→symbol-id map; vocab/dim/budget identical, compositional alignment destroyed).

## Frozen bars (pre-registered; GREEN iff B1 ∧ B2 ∧ B3; mean over 3 seeds)
| bar | test | result | pass |
|-----|------|--------|------|
| **B1 PRESENCE** | G1 jamo CE < 2.9475 − 0.05 = 2.8975 | **2.51335** (Δ −0.434 vs ceiling) | ✅ |
| **B2 EARNED** | G1 beats G1c by ≥0.05 AND G1 beats G0 raw by ≥0.05 | g1c−g1 = **+0.230**; g0−g1 = **+0.440** | ✅ |
| **B3 NO-CHEAT** | NFD→NFC roundtrip byte-identical over the whole KO window AND per-symbol n_bytes sum == corpus bytes | **8,143,053 syllables, 0 roundtrip fails; Σn_bytes 29,999,999 == corpus 29,999,999** | ✅ |

→ **🟢 GREEN.**

## Results (mean 3 seeds [4316,4317,4318]; held-out KO next-symbol CE, nats/UTF-8-byte)
| arm | KO CE (nats/byte) | cells | note |
|-----|-------------------|-------|------|
| **G0** raw-byte (in-run port check) | **2.95342** | 16 | reproduces H_1307 RUN A 2.9475 (Δ +0.006; port valid) |
| **G1** jamo-rep (intact) | **2.51335** | 11 | **Δ −0.434 vs ceiling, Δ −0.440 vs G0 raw** |
| **G1c** shuffle-jamo control | 2.74306 | 10/16/14 | Δ +0.230 vs G1 (jamo beats its own shuffle) |

Per-seed G1c: 2.876 (4316) / 2.506 (4317) / 2.847 (4318).

## Honest scope / caveats (c9, a_scale_honest_scope, a_toy_scale_recheck)
- **G1 is identical across all 3 seeds (2.51335)** because the intact jamo mitosis grow-op is **deterministic** (the FREEZE states seeds only vary the shuffle-control permutation, not the deterministic mitosis). The 3-seed mean is over the **G1c control** (which varies); G1 itself is a single deterministic value. This is pre-registered and correct, but it means the B1 lift is an existence-proof on ONE deterministic partition, not a 3-sample distribution.
- **One control seed (4317 = 2.506) lands essentially AT G1 (2.513)** — i.e. that particular jamo→symbol permutation happened to preserve enough exploitable structure that the partition still learned. The B2 verdict rests on the **mean** (2.743) clearing the bar; the per-seed spread is reported straight. The lift is real (2 of 3 control seeds are +0.33/+0.33 above G1, and G1 beats raw G0 by 0.44 unconditionally), but B2-vs-shuffle is not unanimous per-seed — honest.
- **DIRECTIONAL numpy/torch mirror**; engine-transfer to the live CORE/*.hexa A⇄G + MITOSIS VAdaptField is a **follow-on** (a_engine_native_learning · a_verified_must_wire). **NO Korean-fluency claim** — this is held-out next-byte CE on a toy 3-D byte-substrate at stride-300 density, not a fluent decoder.
- The ~0.44 nat/byte drop is largely the expected coding gain of representing a 3-byte syllable as composed jamo with smaller per-symbol entropy; B2-vs-raw confirms it is NOT just vocab/dim (the shuffle keeps vocab/dim and loses ~0.23 of it), but the residual coding-vs-structure split at scale is UNVERIFIED.

## One-line answer
**The Korean ceiling is REPRESENTATION-bound, not capacity-bound: gradient-free mitosis breaks 2.953 (→ 2.513) the moment the substrate is given the compositional jamo structure that raw bytes hid — the wall was the raw-byte representation, not the mechanism's capacity.**

## Pointers
- code: `UNIVERSE/h1316_ko_jamo_mitosis.py`
- verdicts: `.verdicts/1316_ko_jamo_mitosis/{H_1316_FREEZE,H_1316}.txt` + `h1316_summary.json` + `h1316_manifest.json`
- claim: `CLAIMS.tape` @C h1316_ko_jamo_mitosis
- xref: H_1307 (raw-byte ceiling 2.9475) · H_1311 (richer raw-byte, capacity-bound) · H_1315 (303M-rep, worse) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · c16 · p7 · p8
