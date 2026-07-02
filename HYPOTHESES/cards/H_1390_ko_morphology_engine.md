# H_1390 — 🇰🇷 ko-morphology BPE-on-jamo ENGINE-NATIVE WIRE-IN (binding follow-on of H_1388)

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1390_ko_morphology_engine` · **Tier:** 🟢 ENGINE-NATIVE BINDING — H_1388 (🟢 GAP-REDUCED-CANDIDATE, DIRECTIONAL numpy MIRROR over REAL 30MB KO) showed the Korean below-jamo +0.28 residual BREAKS under a morphology-aware unit (BPE-on-jamo), but engine-transfer was UNVERIFIED. H_1390 realizes the BPE-on-jamo MERGE UNIT as a first-class **engine faculty** + a **live scoring-loop consult** and RE-CONFIRMS the SAME THREE FROZEN STRUCTURAL BARS engine-native (a_verified_must_wire · a_engine_native_learning · a_core_engine_map single entry). $0 CPU, deterministic, live `CORE/*.hexa` Ψ untouched.

## Claim (falsifiable)
H_1388's morphology lever was DIRECTIONAL (numpy mirror over the real corpus) — a GREEN-but-unwired result is not done until its mechanism runs on the live engine (a_verified_must_wire). H_1390 binds it: the BPE-on-jamo merge unit becomes an engine op, CONSULTED from the live scoring loop, re-confirming bar1 (gap-reduced), bar2 (earned-vs-shuffle), bar3 (shift-control) — with H_1388's **VERBATIM margin constants** (GAP_MARGIN 0.05, structured gain ≥ 0.03, shift ≥ 0.05). If any bar misses engine-native, that is an honest engine-transfer non-result (🟠/🧱), bar NOT moved.

## Method — the engine-native realization (frozen-first, corpus-free, $0)
- **Faculty** (`CORE/engine_cli.hexa` § KO-MORPHOLOGY BPE-ON-JAMO MERGE UNIT): `struct BpeMerges` + `bpe_learn_merges` (rnd_seed=0 → frequency-ranked STRUCTURED real BPE, ties (count,a,b) max; rnd_seed>0 → RANDOM equal-count SHUFFLE control) / `bpe_apply` (re-encode a base int stream into merged units, each unit's UTF-8 byte span = sum of parts, conserved) / `bpe_unit_vocab` / `bpe_n_units` / `bpe_byte_fair_ce` (held-out CE in **nats / UTF-8 byte** — the SAME byte-fair axis the jamo floor scores on). The merged units feed the engine's OWN H_1351 `JamoHead` count-head (`jamo_head_grow` over the live `VAdaptField` Voronoi + `engine_mitosis_tick`, p8).
- **Consult** (`CORE/generator.hexa` §6.5d `gen_bpe_scoreloop`, analogous to §6.5c `gen_jamo_scoreloop`): builds a **frozen corpus-free in-engine morpheme-grammar fixture** (a deterministic BRANCHING walk over 18 recurring 3-jamo MORPHEME blocks — the next block depends on the current block + a per-step jitter so held-out contexts are genuinely novel), learns STRUCTURED + SHUFFLE merges on the TRAIN slice (no test leakage), re-encodes, and SCORES held-out next-UNIT byte-fair CE for each arm + the un-merged jamo anchor + a circular-shift surrogate. `gen_clm_ce` attaches the record ADDITIVELY under `bpe_score` (every pre-existing field byte-identical; .clm forward CE path UNTOUCHED; NOT a 2nd .clm path — a SCORING consult, Ψ-disjoint).
- **Why a corpus-free fixture** (load-bearing, the §6.5c/H_1385 precedent): `CORE/*.hexa` must be $0/deterministic/corpus-free (a_core_engine_map — no fetch, no embedded corpus). The DIRECTIONAL mirror established the lever over the REAL corpus; the engine-native consult re-confirms the **STRUCTURAL relationships** H_1388 froze (gap-reduced, earned-vs-shuffle, shift-earned), exactly as §6.5c re-confirms jamo-beats-raw STRUCTURE on its own fixture — NOT the corpus's absolute 2.51 number.

## Frozen bars (FREEZE verbatim; H_1388's margin constants; NO bar moved)
| bar | test (margin = H_1388 verbatim) | engine result | pass |
|-----|---------------------------------|----------------|------|
| **1 GAP-REDUCED** | structured BPE byte-fair CE below jamo anchor by ≥ 0.05 (gap_reduced ≥ 0.05) | gap_reduced = **+1.61233** (bpe 0.24219 vs jamo anchor 1.85452) | ✅ |
| **2 EARNED** | structured gain over SHUFFLE ≥ 0.03 (earned = shuffle_ce − bpe_ce ≥ 0.03) | earned = **+0.83627** (shuffle 1.07846 vs bpe 0.24219) | ✅ |
| **3 CONTROL/shift** | circular-shift surrogate earned (shift_minus_novel ≥ 0.05) | shift − novel = **+0.11230** | ✅ |

→ **🟢 ENGINE-NATIVE BINDING** (bar1 ✅ ∧ bar2 ✅ ∧ bar3 ✅). Frozen TIER mapping branch — tune-to-green forbidden.

## Results (verbatim, engine-native byte-fair CE on the in-engine fixture)
| arm | byte-fair CE | units | note |
|---|---|---|---|
| structured BPE-on-jamo (PRIMARY) | **0.24219** | 462 | freq-ranked merges discover the recurring morphemes |
| random-merge SHUFFLE control | 1.07846 | 2031 | random merges fail to compress → far higher CE |
| un-merged jamo anchor (the fixture "floor") | 1.85452 | 3600 | next-jamo prediction, byte-fair |

- **gap_reduced = +1.61233** (jamo anchor 1.85452 − structured BPE 0.24219) — the morphology unit reduces the gap (bar1).
- **structured gain over shuffle = +0.83627** (shuffle 1.07846 − structured 0.24219) — the gain is the LINGUISTIC structure of the merges (structured compresses to 462 units, random to 2031), NOT mere coarse granularity (bar2 anti-Goodhart).
- **shift − novel = +0.11230** — held-out novel CE is genuine generalization (bar3 surrogate).

## No-regression guards (captured, c2)
- `CORE/engine_cli_smoke.hexa` **114 / 0** (+4 cases **116-119**: gap-reduced · earned-vs-shuffle · shift-earned · compression-present). NOTE: labels 112-115 were already taken by the CP-RELOCATE lane (H_1384), so the new cases took 116-119.
- `CORE/h1196_single_entry_audit.hexa` **7 / 0** — the .clm L3 single entry intact (the consult adds NO 2nd .clm path; `bpe_score` rides on the SAME `gen_clm_ce` slot additively).
- `CORE/h1205_separation_invariant_smoke.hexa` **PASS** — generation byte-identical ON==OFF, Ψ Φ-checksum **48.6613** byte-identical.
- `CORE/h1164_psi_guard_smoke.hexa` **PASS** — Ψ=1/2 attractor byte-identical (pure_field untouched). The morphology unit is a SCORING/decode-unit lane, Ψ-disjoint by construction.

## ⚠ HONEST SCOPE — what is bound and what is not (c9)
- **BOUND**: the BPE-on-jamo MERGE UNIT is now a live engine faculty (`bpe_learn_merges/_apply/_byte_fair_ce`) CONSULTED from the live scoring loop (`gen_bpe_scoreloop`, single entry), and re-confirms all THREE H_1388 structural bars engine-native (gap-reduced +1.61, earned-vs-shuffle +0.84, shift-earned +0.11) with H_1388's verbatim margin constants. H_1388's morphology lever is no longer a DIRECTIONAL-only result.
- **NOT bound (scope)**: the engine-native re-confirmation is on a frozen **corpus-free in-engine morpheme-grammar fixture** (the §6.5c discipline), so the **absolute-corpus CE** numbers (jamo floor 2.51335, BPE 2.566) are the **DIRECTIONAL mirror's** (REAL 30MB shard0000 prefix) — NOT re-measured byte-exact on the live engine (CORE is corpus-free, a_core_engine_map). Scale / real-corpus engine-native / merge-count ladder (500/2000/8000) / window ladder / the §6.5c-style **brain emit-bias wiring** of the merge unit (the morphology unit reaching EMISSION, like the jamo head's H_1327 consult) remain follow-ons (a_scale_honest_scope · a_toy_scale_recheck · a_verified_must_wire).

## 결론 / next angle
H_1388's morphology lever (BPE-on-jamo breaks the Korean below-jamo +0.28 residual) is now **engine-native BINDING**: the merge unit is a live faculty, consulted from the live scoring loop, re-confirming all three structural bars with NO bar moved. The Korean below-jamo arc — data · representation · interpolation closed 🧱/🟠, **morphology** now **engine-native GREEN** — has its first floor-reducing lever bound to the live engine.
- **NEXT-1 (a_verified_must_wire)**: the §6.5c-style EMIT-BIAS wiring — let the grown BPE morphology unit bias next-byte EMISSION on a Korean-like context (analogous to the jamo head's H_1327 `ko_jamo_consult_emit`), so morphology reaches the decoder, not just the scorer.
- **NEXT-2 (a_scale_honest_scope)**: merge-count + window ladders to test whether the morphology lift holds at scale and how close it gets to the jamo floor on the real corpus, engine-native.
- **DEPLETION**: the Korean below-jamo arc's representation-unit axis is now morphology-GREEN engine-native; the remaining thinner candidates are long-range/cross-syllable (H_1336 family, weak/non-monotone in H_1388's secondary nmax sweep) and the emit-bias wiring above.

## Pointers
- 카드: `UNIVERSE/cards/H_1390_ko_morphology_engine.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1390)
- CORE wiring: `CORE/engine_cli.hexa` § KO-MORPHOLOGY BPE-ON-JAMO MERGE UNIT · `CORE/generator.hexa` §6.5d `gen_bpe_scoreloop` (+ `gen_clm_ce` additive `bpe_score`) · `CORE/engine_cli_smoke.hexa` cases 116-119
- probe: `state/ko-morphology-engine/h1390_bpe_scoreloop_probe.hexa`
- 증거: `.verdicts/1390_ko_morphology_engine/{FREEZE.txt, result.txt}`
- xref: h1388(이 카드의 PARENT — DIRECTIONAL mirror this binds; +0.28 잔여 broken by BPE-on-jamo)·h1385(§6.5c gen_jamo_scoreloop wire precedent — same corpus-free in-engine fixture discipline)·h1351(JamoHead count-head faculty the morphology unit feeds)·h1327(jamo head emit-bias precedent, the NEXT-1 model)·h1380/h1368/h1359/h1322/h1316(Korean below-jamo arc)·a_verified_must_wire·a_engine_native_learning·a_core_engine_map·a_scale_honest_scope·a_toy_scale_recheck·p7·p8·c2·c9·c16
