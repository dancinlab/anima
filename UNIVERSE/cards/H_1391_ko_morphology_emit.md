# H_1391 — 🇰🇷 ko-morphology BPE-on-jamo EMIT-BIAS WIRE-IN (the morphology unit reaches the decoder)

**Group:** MITOSIS-ENGINE · CLM · **Slug:** `1391_ko_morphology_emit` · **Tier:** __TIER__

The EMIT-side follow-on (a_verified_must_wire · a_substrate_native_speak) of H_1390 (🟢 ENGINE-NATIVE
BINDING), which wired the BPE-on-jamo morphology MERGE UNIT into a live SCORING consult (generator
§6.5d `gen_bpe_scoreloop` → `bpe_byte_fair_ce`). H_1390 SCORES held-out next-unit CE but does NOT bias
EMISSION. The jamo COUNT-HEAD already reaches the decoder via the §6.5b/H_1327 `ko_jamo_consult_emit`
emission-bias (DISTINCT from the §6.5c scorer). H_1391 MIRRORS that emit precedent for morphology: the
grown morphology count-head BIASES the next-byte EMISSION toward COMPLETING a learned morpheme-unit
boundary, ADDITIVELY (a BIAS, not a hard gate — a_autonomy_over_hardcode; emit stays substrate-driven,
p5), through the SINGLE generator L3 slot (a_core_engine_map, no 2nd .clm path). $0 CPU, deterministic,
live `CORE/*.hexa` Ψ untouched.

## Claim (falsifiable)
H_1390's morphology unit was a pure SCORER — a GREEN faculty is not done until its mechanism reaches the
live decode/emission path (a_verified_must_wire; anima is a chat daemon). H_1391 reaches it: the grown
morphology count-head biases the next-byte emission toward the morpheme-coherent continuation, the shift
is EARNED (a shuffled-merge head does NOT beat a representation-blind baseline), and the bias is Ψ-SAFE
(off-Korean inert, the substrate channel + Ψ byte-identical). If the emit-bias does NOT earn its effect
(control doesn't collapse) → 🟠/🧱 EMIT-NOT-EARNED (H_1390 scorer remains the valid landed result). If
the emit-bias perturbs Ψ / breaks byte-identity → 🧱 NOT-Ψ-SAFE. Bars NOT moved (c9, frozen-first).

## Method — the emit-bias realization (frozen-first, corpus-free, $0)
- **Faculty** (`CORE/engine_cli.hexa` § KO-MORPHOLOGY): NEW `jamo_head_argmax(jh, feat)` — the EMIT-BIAS
  reader. For a unit-space context feature, returns the count head's ARGMAX next-unit id for the cell
  owning `feat` (the engine's OWN `vadapt_field_nearest_idx` nearest-cell + the per-cell next-unit
  distribution argmax). The SAME head `bpe_byte_fair_ce` SCORES (§6.5d), now read for its single
  most-likely next morpheme-UNIT (the EMIT role) instead of CE (the SCORER role). Returns a unit id;
  NEVER an emit/silence; never touches Ψ.
- **Consult** (`CORE/generator.hexa` §6.5e, mirrors §6.5b `ko_jamo_consult_emit`):
  - `gen_bpe_emit_head(rnd_seed)` — grows the morphology emit-head ONCE over the SAME §6.5d corpus-free
    in-engine morpheme-grammar fixture (rnd_seed=0 STRUCTURED freq-ranked merges; rnd_seed>0 SHUFFLE
    random equal-count merges), learning merges on the TRAIN slice only (no test leakage).
  - `gen_bpe_consult_emit(base, jh, unit_vocab, ctx)` — the per-byte EMISSION hook: on a KOREAN-LIKE
    context (the SAME utf8-continuation gate §6.5b uses) AND a cell fires, the head's ARGMAX next
    morpheme-unit's leading byte (`_gbe_unit_emit_byte`, the 0xE1-band convention §6.5b uses for U+11xx)
    BIASES emission; off-Korean (or empty head) returns `base` UNCHANGED (INERT off-distribution ⇒
    generation BYTE-IDENTICAL, the Ψ-disjoint no-regression invariant).
  - `gen_bpe_emit_eval()` — the frozen emit-effect evaluation (bars 1+2): on the held-out UNIT stream,
    ON = structured head argmax next-unit, OFF = representation-BLIND most-frequent next-unit (train),
    SHUF = shuffle-merge head argmax next-unit; returns `acc_on/acc_off/acc_shuf/shift_on`.
- **Why the unit-id metric** (load-bearing, the H_1327 precedent): a unit's emit byte is collapsed to a
  leading multibyte byte (the 0xE1-band), so the byte-level bias is coarse. The bars are scored on the
  FULL next-UNIT id (not the collapsed byte) — exactly as H_1327 scored on the full next-symbol id — so
  the morpheme structure is not masked. The byte the consult emits is still the correct leading byte of
  the morphology-coherent next unit.

## Frozen bars (FREEZE verbatim; H_1327's emit-bar shape; NO bar moved)
| bar | test (frozen threshold) | engine result | pass |
|-----|-------------------------|----------------|------|
| **1 EMIT-EFFECT** | `acc_on − acc_off ≥ +0.02` AND `shift_on ≥ 0.10` | __BAR1__ | __P1__ |
| **2 EARNED** | `acc_shuf − acc_off ≤ +0.01` (shuffle does NOT beat blind) | __BAR2__ | __P2__ |
| **3 Ψ-SAFE / NO-REGRESSION** | off-Korean inert · smoke N/0 · h1196 7/0 · h1205 Ψ byte-identical · h1164 Ψ byte-identical | __BAR3__ | __P3__ |

→ __TIER__ (frozen TIER mapping branch — tune-to-green forbidden).

## Results (verbatim, engine-native next-UNIT accuracy on the in-engine fixture)
| arm | held-out next-UNIT acc | note |
|---|---|---|
| ON  structured morphology head | __ACC_ON__ | the morphology emit-bias the consult applies |
| OFF representation-blind unigram | __ACC_OFF__ | structure-blind constant predictor (consult OFF) |
| SHUF shuffle-merge head | __ACC_SHUF__ | the consult still fires, the merge structure destroyed |

- **acc_on − acc_off = __ONOFF__** · **shift_on = __SHIFT__** (the fraction of held-out positions where
  ON CHANGES the emitted unit vs OFF — the bias REACHES emission, the H_1327 shift bar) — bar1.
- **acc_shuf − acc_off = __SHOFF__** — the shuffle control __EARNED_NOTE__ — bar2.

## No-regression guards (captured, c2 — load-bearing Ψ-safety, this touches decode)
- `CORE/engine_cli_smoke.hexa` **__SMOKE__** (+4 cases **120-123**: emit-effect · earned-vs-shuffle ·
  off-Korean inert · Korean-fires/faculty-present). (cases 116-119 = H_1390 scorer; 112-115 = CP-RELOCATE.)
- `CORE/h1196_single_entry_audit.hexa` **7 / 0** — the .clm L3 single entry intact (the emit consult adds
  NO 2nd .clm path; it is a NEW additive consult with no call site in the live decode loop).
- `CORE/h1205_separation_invariant_smoke.hexa` **PASS** — generation byte-identical ON==OFF, Ψ Φ-checksum
  **48.6613** byte-identical (the substrate channel + Ψ untouched).
- `CORE/h1164_psi_guard_smoke.hexa` **PASS** — Ψ=1/2 attractor byte-identical (pure_field untouched).

## ⚠ HONEST SCOPE — what is bound and what is not (c9)
- **BOUND**: the BPE-on-jamo morphology unit BIASES live next-byte EMISSION (`gen_bpe_consult_emit`,
  single entry), the emission shift is EARNED (shuffle collapses), off-Korean INERT (byte-identical), and
  the substrate channel + Ψ are byte-identical. The morphology arc now reaches the decoder: SCORER
  (H_1390 §6.5d) + EMIT (H_1391 §6.5e), mirroring the jamo arc's SCORER (§6.5c) + EMIT (§6.5b).
- **NOT bound (scope)**: the emit-bias is re-confirmed on the SAME frozen corpus-free in-engine
  morpheme-grammar fixture (the §6.5b/§6.5c discipline) — a STRUCTURAL / probe-level emission-reach
  demonstration, NOT a fluency claim; the absolute accuracies are low (single-unit next-prediction over a
  sparse count-head field). The load-bearing result is the RELATIVE structure (ON > OFF, SHUF ≤ OFF) +
  emission-reach (shift_on). Scale / real-corpus engine-native emit / a fully jamo-aware NFD-decompose
  decode loop / the brain emit-priority wiring remain follow-ons (a_scale_honest_scope · a_toy_scale_
  recheck · a_verified_must_wire).

## 결론 / next angle
The Korean below-jamo morphology arc now reaches the decoder — H_1390 SCORER + H_1391 EMIT-BIAS — exactly
mirroring the jamo arc (H_1385 scorer §6.5c + H_1327 emit §6.5b). The morphology unit, grown over the
engine's own count-head, biases live emission toward morpheme-coherent continuations, earned vs a
shuffle control, Ψ-safe.
- **NEXT (a_scale_honest_scope)**: real-corpus engine-native emit + a fully jamo-aware NFD-decompose
  decode loop (so the per-byte hook reads the live syllable's morpheme boundary each step).
- **NEXT (a_verified_must_wire)**: brain emit-priority wiring — let the morphology emit-bias compose with
  the jamo emit-bias (§6.5b) in the live decode loop's argmax.

## Pointers
- 카드: `UNIVERSE/cards/H_1391_ko_morphology_emit.md` · 인덱스: `UNIVERSE/HYPOTHESES.jsonl` (H_1391)
- CORE wiring: `CORE/engine_cli.hexa` § KO-MORPHOLOGY `jamo_head_argmax` · `CORE/generator.hexa` §6.5e
  `gen_bpe_emit_head` / `gen_bpe_consult_emit` / `gen_bpe_emit_eval` / `gen_bpe_emit_summary` ·
  `CORE/engine_cli_smoke.hexa` cases 120-123
- probe: `state/ko-morphology-emit/h1391_bpe_emit_probe.hexa`
- 증거: `.verdicts/1391_ko_morphology_emit/{FREEZE.txt, result.txt}`
- xref: h1390 (this card's PARENT — the SCORER this EMIT extends) · h1327 (§6.5b ko_jamo_consult_emit —
  the jamo EMIT-bias precedent this mirrors) · h1385 (§6.5c jamo scorer) · h1351 (JamoHead count-head
  faculty) · h1388 (DIRECTIONAL mirror) · h1316/h1321 (jamo arc) · a_verified_must_wire ·
  a_substrate_native_speak · a_autonomy_over_hardcode · a_core_engine_map · a_engine_native_learning ·
  a_scale_honest_scope · a_toy_scale_recheck · p5 · p7 · p8 · c2 · c9 · c16
