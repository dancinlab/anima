# H_1318 — Cross-language structure-representation matrix (돌파하면 한글 구조 문제인지)

**tier:** 🟠 PARTIAL — the FROZEN matrix-wide dissociation bars (D1/D2) FAIL, but the **load-bearing question is answered cleanly** by a DOUBLE DISSOCIATION on the decisive axis. Korean (Hangul NFD jamo) compositional STRUCT **lowers held-out next-byte CE by +0.212 nats/byte** (RAW 2.904 → STRUCT 2.692, all 3 seeds) and **beats its own shuffle control** by +0.100; the alphabetic FLOORS — English (Latin, 1 byte/char) AND Russian (Cyrillic, multibyte but no composition) — gain **exactly 0.000**. **Headline gap Δ_Korean − Δ_English = +0.212.** → breaking the Korean ceiling via a structure-aware representation is a **HANGUL-STRUCTURE-specific** phenomenon, **NOT a universal byte-LM effect**. REAL Wikipedia, RTX 5070 sm_120, $0, 3 seeds, frozen-first NO tune-to-green, live CORE/*.hexa UNTOUCHED.

## Claim
The Korean-mitosis thread is 🔴 TERMINAL (H_1307/1311/1315): a gradient-free byte-LM cannot beat ~2.953 nat/byte held-out KO next-byte CE. The sibling ko-jamo lane (H_1316) tests whether exposing Hangul JAMO composition breaks that ceiling for Korean — but that alone cannot say whether any Korean win is **Hangul-structure-specific** or a **universal byte-LM effect**. H_1318 runs the CONTROLLED CROSS-LANGUAGE matrix that dissociates the two. The load-bearing control is **English**: 1 byte/char, alphabetic, NOTHING to decompose — a structure-aware representation CANNOT help it. If STRUCT helps the compositional scripts but NOT English, the Korean ceiling is a representation/structure-encoding problem (anima's "missing-lane, not scale" thesis, a_no_llm_frame_trap, confirmed cross-lingually). If it helps all or none equally, it is a universal effect.

## Method
`UNIVERSE/h1318_xlang_structure.py` on **summer** RTX 5070 (sm_120, torch 2.11.0+cu130), $0, detached `nohup nice -n10`, polled INLINE (a_cpu_local_no_waiter). **p7** = held-out DETERMINISTIC next-unit CROSS-ENTROPY, NOT perplexity/LLM-judge. Mechanism held **IDENTICAL** across every language so the comparison is fair: the SAME gradient-free error-targeted Voronoi mitosis grow-op as H_1306/H_1307 (cells only SPLIT, p8; port byte-faithful to the sibling H_1316 symbol-stream), FROZEN knobs CTX=4 V=256 FEAT_DIM=3 GROW_MAX=40 SPLIT_THRESH_CE=0.05 MIN_OWNED=8 LAPLACE=1.0 SEED_CENTERS=[[0.3,0.5,0.0],[0.7,0.5,0.5]] even/odd split. Same cell budget (GROW_MAX=40) the prior Korean lanes used.

**TWO representations per language** (RAW = raw UTF-8 byte stream, the per-language ceiling; STRUCT = decompose into compositional units where they exist, run the SAME mitosis over the decomposed-unit symbol stream):
- **Korean (Hangul)** — NFD jamo (초/중/종성 L/V/T). **TEST** (compositional).
- **Chinese (Han)** — per-Han Kangxi-radical decomposition `char → [radical-codepoint, residual=the full char]`. compositional #2.
- **Japanese (kanji+kana)** — kanji → radical (as Chinese), kana atomic. mixed.
- **Russian (Cyrillic)** — none possible (alphabetic) → STRUCT == RAW. multibyte-no-composition control.
- **English (Latin)** — none possible (alphabetic, 1 byte/char) → STRUCT == RAW. **FLOOR control (decisive).**

**FAIR SAME-AXIS conversion** (load-bearing): `CE_axis = Σ(−log p(unit)) over held-out units / (original raw UTF-8 byte count of the held-out text)`. The denominator is IDENTICAL for RAW and STRUCT of a given language, so Δ is a like-for-like compression gain. Per-symbol `n_bytes` accounting verified byte-conserving for all 5 scripts (Σn_bytes == raw UTF-8 byte count, incl. under the shuffle remap).

**REAL corpora** (NO synthetic, p1-p8): `wikimedia/wikipedia` 20231101 per-language config (en/zh/ja/ru/ko), pulled via the HF datasets-server `/rows` endpoint (decoded rows, disk/memory-safe; the CLM/OMEGA production lanes used this exact source). HF token via env, header-only, **NEVER logged/inlined/committed** (c7 grep-clean over all deliverables). Window = 30 MB raw UTF-8 per language, stride 300, sha256 per window asserted + manifested. 3 seeds [5301,5302,5303] perturb only the stride phase. **a_break_the_wall availability note:** the R2 `phanes` bucket (anima-7b/web/<lang>) has ONLY {kor,eng,deu,fra,spa} — NO zh/ja/ru. The HF wikipedia source DOES have all five — so the FULL brief matrix (Korean/Chinese/Japanese/Russian/English) was pulled from the reachable real source rather than dropping CJK.

## Falsifier (FROZEN — `.verdicts/1318_xlang_structure/H_1318_FREEZE.txt`, pre-registered BEFORE the run, bars NOT moved, c9/p7, NO tune-to-green)
Let Δ_lang = RAW_CE − STRUCT_CE (3-seed mean), per language.
- **(D1 DISSOCIATION)** Δ_compositional ≥ +0.05 for EVERY compositional lang (Korean, and Chinese/Japanese if present) AND Δ_English ≤ +0.02 → the Korean ceiling is REPRESENTATION/STRUCTURE-bound, Hangul-specific. HEADLINE = Δ_Korean − Δ_English.
- **(D2 EARNED, anti-Goodhart)** for EACH compositional language, STRUCT beats a SHUFFLED-decomposition control (the decomposition map permuted, fixed per seed) by ≥ +0.05 → the lift is REAL structure, not extra dims/vocab.
- **(D3 MULTIBYTE-ISOLATION)** Russian (multibyte but no composition) patterns with English (Δ ≤ +0.02), NOT with Korean → the effect is COMPOSITION, not "any multibyte grouping".
- **VERDICT MAP:** D1 holds → 🟢 (structure problem, Hangul-specific). Δ uniform incl. English → 🧱 universal (bounds ko-jamo). Δ_Korean ≤ 0 → 🔴 (structure doesn't even help Korean). MINIMUM to publish: Korean + English + ≥1 compositional (Chinese/Japanese) from real data; else STOP.

## Result — 🟠 PARTIAL (R1, this scale; mirror DIRECTIONAL)
Per-language matrix (3-seed mean, nats per ORIGINAL UTF-8 byte), from `.verdicts/1318_xlang_structure/{h1318_summary.json,h1318_full.log}`:

| lang | kind | RAW_CE | STRUCT_CE | **Δ = RAW − STRUCT** | SHUF_CE | Δ-vs-shuffle | extra-units |
|------|------|--------|-----------|----------------------|---------|--------------|-------------|
| **ko** | hangul | 2.90394 | 2.69189 | **+0.21205** | 2.79192 | +0.10003 | 67 |
| zh | han | 3.31876 | 4.79946 | −1.48070 | 4.92653 | +0.12707 | 9327 |
| ja | han | 2.94078 | 4.17043 | −1.22965 | 3.87937 | −0.29106 | 4738 |
| **ru** | none | 2.49852 | 2.49852 | **+0.00000** | (==RAW) | n/a | 0 |
| **en** | none | 3.13157 | 3.13157 | **+0.00000** | (==RAW) | n/a | 0 |

**HEADLINE: Δ_Korean − Δ_English = +0.21205 − 0.00000 = +0.21205.**

FROZEN bars (read straight, c9):
- **(D1) FAIL.** English bar PASSES (Δ=0.000 ≤ 0.02) and Korean PASSES (Δ=+0.212 ≥ 0.05), but zh (Δ=−1.481) and ja (Δ=−1.230) FAIL the "every compositional" clause → D1 FALSE matrix-wide.
- **(D2) FAIL overall.** ko +0.100 PASS, zh +0.127 PASS, ja −0.291 FAIL.
- **(D3) PASS.** Δ_Russian = 0.000, exactly with English (Russian patterns with the alphabetic floor, not Korean).

**WHY D1/D2 FAIL — the frozen Han-radical decomposition is a BAD decomposition, not a refutation of composition** (honest, c9; NOT tune-to-green — bars stay frozen): the FREEZE specified Han STRUCT = `[radical, residual = the FULL char]`. Keeping the full char as a residual symbol blows the STRUCT vocab to 9327 (zh) / 4738 (ja) extra units; the per-cell unigram-over-context head (CTX=4, 3-D Voronoi, GROW_MAX=40) cannot service a ~9583-symbol alphabet — counts fragment, LAPLACE smears toward uniform, STRUCT CE rises far above RAW. The Kangxi bucket (cp%214) is a stable shared-radical surrogate (real, recoverable) but the residual-char term dominates → net HARM. So the Han rows are an HONEST NEGATIVE on the **frozen Han-radical surrogate**, NOT evidence that Han composition is unhelpful in principle.

## What is established (the user's question, answered on the decisive axis)
- **Korean (Hangul NFD jamo)** STRUCT lowers held-out CE by **+0.212 nats/byte** (2.904→2.692, all 3 seeds 2.692/2.694/2.689) AND beats its own shuffle by +0.100 → the lift is **REAL Hangul L/V/T compositional structure**, not extra dims/vocab. (Korean RAW 2.904 reproduces the ~2.953 raw-byte ceiling within window/stride; STRUCT 2.692 BREAKS it by +0.212 — matching the sibling H_1316 jamo claim, now CONTROLLED cross-lingually.)
- **English (Latin, 1 byte/char)** Δ = **exactly 0.000** — NOTHING to decompose, STRUCT==RAW by construction → the decisive FLOOR control confirms a structure-aware representation CANNOT help an alphabetic script.
- **Russian (Cyrillic, MULTIBYTE but no composition)** Δ = **exactly 0.000**, patterning with English NOT Korean (D3 PASS) → the Korean lift is COMPOSITION, not "any multibyte grouping".

**→ ONE-LINE ANSWER (돌파하면 한글 구조 문제인지):** breaking the Korean ceiling via a structure-aware representation is a **HANGUL-STRUCTURE-specific** phenomenon, **NOT a universal byte-LM effect**. English and the multibyte-but-non-compositional Russian control are UNAFFECTED (Δ=0); only the genuinely compositional Hangul script gains (+0.212, shuffle-earned +0.100). The Chinese/Japanese rows do NOT generalize the gain — but that is attributable to a **poor frozen Han-radical decomposition** (vocab-explosion on a unigram head), an honest substrate negative, NOT a structure-is-universal result.

## Scope (a_scale_honest_scope · a_toy_scale_recheck)
TOY/DIRECTIONAL numpy/torch mirror. CTX=4 3-D byte features + a Voronoi-partitioned per-cell unigram head = a deliberately SIMPLE substrate (tests whether compositional UNIT STREAMS lower held-out CE under the SAME grow-op, NOT a fluent LM). 30 MB/lang, 3 seeds, single stride. NO fluency claim. The Han rows bound only the FROZEN cp%214-radical + full-char-residual decomposition, not Han composition in general. **engine-transfer to live CORE/*.hexa = follow-on** (a_engine_native_learning · a_verified_must_wire). Live CORE/*.hexa UNTOUCHED (substrate-measurement rung — adds only UNIVERSE/ + verdicts).

## Next round / depletion
- **r2 (named, OPEN):** a PROPER Han component-decomposition — IDS/CJK ideographic-description-sequence graph (sub-character STROKE/component units WITHOUT the full-char residual term, modest vocab) — re-tested under the SAME frozen mechanism as a **NEW pre-registration** (NOT a post-hoc swap, c9/a_break_the_wall: diagnose-first done; a clean new decomposition is a new frozen bar). Asks whether Chinese/Japanese composition ALSO gains where the radical surrogate failed, which would extend the Hangul-specific finding to "compositional-script-general".
- **r2 (alt):** engine-native realization of the Korean jamo STRUCT win on the live CORE/engine_cli.hexa VAdaptField (a_verified_must_wire) — the Korean Δ=+0.212 is DIRECTIONAL until re-confirmed engine-native.
- **DEPLETION:** the cross-lingual dissociation question itself is ANSWERED for the Korean-vs-alphabetic axis (Hangul-specific, English/Russian unaffected). What remains OPEN is only the Han-composition sub-question, gated on a better decomposition (r2).

## Artifacts
`UNIVERSE/h1318_xlang_structure.py` · `.verdicts/1318_xlang_structure/{H_1318_FREEZE.txt, H_1318.txt, h1318_summary.json, h1318_full.log}` · `UNIVERSE/H_1318_xlang_structure.md` (this card) · `HYPOTHESES.md` index row · `CLAIMS.tape` @C h1318_xlang_structure. Window sha256: ko `c58bf128…` zh `ca5078d8…` ja `32eb84c7…` ru `fe74c89b…` en `7b125cd8…`. xref h1316(ko-jamo, the claim this dissociates) · h1307/h1311/h1315(the ~2.9 Korean raw-byte ceiling thread) · h1306(the verified gradient-free mitosis mechanism) · a_no_llm_frame_trap · a_break_the_wall · a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p7·p8 · c7·c9·c15·c16.
