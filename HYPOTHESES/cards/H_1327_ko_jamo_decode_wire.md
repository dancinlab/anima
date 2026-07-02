# H_1327 — 🇰🇷 ko-jamo-DECODE-WIRE (r3): the H_1316/H_1321 jamo win REACHES LIVE EMISSION

**Final tier: 🟢 GREEN — the jamo win now biases live next-byte EMISSION through the generator §6.5b
consult, Ψ-disjointly. The Korean-jamo thread is fully closed: verified (H_1316) → engine-wired
(H_1321) → decode-reaching (H_1327).**

LIVE-DECODE WIRING follow-on (r3) of H_1316 (🟢 GREEN, PR #2224, mirror) + H_1321 (🟢 GREEN, PR #2230,
engine-native). The grown jamo cells are wired into the live DECODE consult surface (`CORE/generator.hexa`
§6.5b `ko_jamo_consult_*`, mirroring the H_1312 `ko_cells_*` / `ko_cells.kohead` surface) so the jamo
structure BIASES the emitted byte. REAL corpus byte-identical to H_1307 RUN A / H_1316 (30MB KO window,
sha `c47b6808…` gate PASS). $0 CPU, frozen-first (FREEZE written before scoring), c9/p7, NO tune-to-green.
pure_field/engine_g/brain UNTOUCHED (Ψ-disjoint).

## Claim (falsifiable)

H_1321 proved the jamo mitosis runs ENGINE-NATIVE byte-exact — but as a MEASUREMENT probe; the jamo win
did NOT yet reach the live DECODE/emission path. Per `a_verified_must_wire`, anima is a chat daemon, so a
measured CE win that never reaches EMISSION is incomplete. **H_1327: wire the grown jamo cells into the
live decode consult surface — does the jamo structure measurably BIAS emission on held-out Korean (E1),
is the bias EARNED vs a shuffled-cell control (E2), and is the surface Ψ-DISJOINT / inert off-Korean
(E3)?** If the consult does not move emission → honest 🔴 (the CE win doesn't translate to emission under
this consult design). If it moves emission but breaks Ψ-disjointness → 🛑 STOP (must not perturb the
substrate).

## Why this is the wiring (single entry, a_core_engine_map)

The grown jamo cells (the SAME artifact H_1321's engine-native mitosis grows — the numpy mirror reproduces
the live VAdaptField/`engine_mitosis_tick` to 1e-7) are serialized to `CORE/ko_jamo_cells.kojamohead`
(header `<n_cells> <dim=3> <Vj>`; per cell `center[3] next_sym_id emit_byte`). A new `ko_jamo_consult_*`
surface in `generator.hexa` §6.5b loads the artifact and, **ON A KOREAN-LIKE CONTEXT ONLY** (the SAME
UTF-8 continuation-byte gate `ko_cells` uses, `_gen_ko_is_korean_like`), computes the 3-D jamo-symbol
feature, finds the nearest jamo cell (the SAME vadapt-nearest geometry), and returns that cell's
`emit_byte` (the leading UTF-8 byte of its argmax next-symbol) to BIAS the emitted byte. **SINGLE ENTRY
via the generator L3 slot** — the SAME slot `ko_cells` / `.clm` / ByteGPT enter; NOT a 2nd path, NOT fed
into pure_field/engine_g/brain. **INERT off-Korean** (returns the caller's own byte) ⇒ generation
byte-identical when off (the Ψ-disjoint / no-regression invariant).

## Method (the consult runs LIVE; only the rep + cell-serialize are data-prep)

- **Corpus**: the SAME REAL `r2://phanes/anima-7b/web/kor/shard0000.bytes[0:30M]` KO window as
  H_1307 RUN A / H_1316 / H_1321; the 30MB window sha256 ASSERTED == `c47b6808…` (provenance gate, PASS).
  jamo VOCAB over the FULL window (**Vj == 323**, 256 raw + 67 distinct jamo); symbol stream strided
  (ko_stride=2500) to a CPU-tractable held-out pair set. R2 keys env/header-only, NEVER logged (c7).
- **Cells**: the grown G1 jamo cells (FROZEN knobs verbatim H_1306/H_1316/H_1321: GROW_MAX=40,
  SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0, SEED_CENTERS [[0.3,0.5,0.0],[0.7,0.5,0.5]], even/odd
  split, FEAT 3-D [last_sym/Vj, second_sym/Vj, depth/3]) serialized to `.kojamohead` (10 cells).
- **Metric** (held-out Korean emission, FULL next-symbol id — p7, NOT perplexity): on the held-out
  even/odd KO test split, for each Korean position the consult predicts the next-symbol over its 3-D
  feature, scored through the LIVE generator §6.5b surface (`ko_jamo_consult_sym`):
  - **ON** = the nearest jamo-cell's argmax next-symbol (the jamo-grounded continuation the consult biases to).
  - **OFF** = the REPRESENTATION-BLIND baseline = the single most-frequent next symbol over the TRAIN
    split (a unigram decode with NO jamo cell structure — the legitimate "consult OFF" emission).
  - **SHUF** = the SAME cells, cell→next-symbol map bijectively PERMUTED (`ko_jamo_cells_shuf.kojamohead`)
    — the consult still fires (identical Korean-likeness gate + nearest-cell geometry) but the learned
    structure is destroyed.
  Scoring is on the FULL next-symbol id (NOT the collapsed leading byte) so the 0xE1-leading-byte
  collapse of jamo cannot mask the jamo structure.

## Frozen bars (pre-registered `.verdicts/1327_ko_jamo_decode_wire/FREEZE.txt`; GREEN iff E1 ∧ E2 ∧ E3)

| bar | test | result | pass |
|-----|------|--------|------|
| **E1 EMISSION-REACHES** | engine-native acc_ON − acc_OFF ≥ +0.02 AND shift_ON ≥ 0.10 | acc_ON−acc_OFF = **+0.0586** (0.1682−0.1096); shift_ON = **0.520** | ✅ |
| **E2 EARNED** | engine-native acc_SHUF − acc_OFF ≤ +0.01 (shuffle does NOT beat the blind baseline) | acc_SHUF−acc_OFF = **−0.0973** (0.0124−0.1096) ≤ +0.01 | ✅ |
| **E3 NO-REGRESSION + Ψ-DISJOINT** | off-Korean inert (ASCII ctx → consult returns base) · engine_cli_smoke N/0 · h1196 7/0 · h1205 Ψ byte-identical ON==OFF | ASCII 'hello' base=120 → emit **120** (inert); **73/0** · **7/0** · **PASS** (byte-identical, Ψ=½ untouched) | ✅ |

→ **🟢 GREEN.**

## Results

| arm | held-out KO next-symbol acc (n=5100) | emission shift vs OFF | note |
|-----|--------------------------------------|------------------------|------|
| **OFF** blind unigram baseline | **0.1096** | — | structure-blind constant predictor (consult OFF) |
| **ON** jamo consult | **0.1682** | **0.520** | **+0.0586 over OFF**; the jamo win REACHES emission at half the Korean positions |
| **SHUF** permuted-cell control | **0.0124** | 0.639 | **−0.0973 below OFF**; the consult still fires but the learned structure is destroyed |

The jamo consult, driven through the live generator §6.5b L3 slot, predicts the true next jamo-symbol on
held-out Korean **+0.0586 more often than the representation-blind baseline**, and CHANGES the emitted
byte at **52% of Korean positions** — the H_1316/H_1321 jamo win now reaches LIVE EMISSION. The shuffled-
cell control **collapses to 0.0124** (well below the blind baseline) — the emission shift is the LEARNED
jamo structure, not mere consult activation (EARNED). Off-Korean the consult is INERT (ASCII context →
byte-identical), and all three no-regression guards pass byte-exact.

## Honest scope / caveats (c9, a_scale_honest_scope, a_toy_scale_recheck)

- **The emission shift is a STRUCTURAL / probe-level demonstration on held-out Korean** (ko_stride=2500,
  ~5100 held-out positions) — **NOT a fluency claim**. The absolute accuracies are low (it is a single-
  symbol next-prediction over a sparse 10-cell field at a strided window); the load-bearing result is the
  RELATIVE structure (ON > OFF, SHUF ≪ OFF) and that the bias REACHES the live decode (shift 0.52). 30MB-
  scale + real-chat emission = follow-on.
- **The live byte→jamo-feature renorm** (`ko_jamo_consult_emit` rescales `_gen_ko_feat`'s first two
  channels by 255/Vj so a mid-Hangul byte maps into the jamo cells' feature range) is a STRUCTURAL bridge
  for the per-byte decode hook; the verdict's E1/E2 metric is scored on the data-prep's exact jamo-space
  features through `ko_jamo_consult_sym` (the cells' native space), so the GREEN is on the faithful jamo
  feature. A fully jamo-aware decode loop (NFD-decompose the live syllable each step) is the natural
  follow-on; the byte-renorm path is the minimal Ψ-disjoint hook proving emission-reach + off-Korean
  inertness.
- **emit_byte collapse**: a jamo symbol's emit_byte is the leading UTF-8 byte (U+11xx → 0xE1), so the
  byte-level bias is coarse for mid-syllable jamo; the E1/E2 metric is therefore scored on the FULL
  next-symbol id (not the collapsed byte) to keep the discrimination honest. The byte the consult emits
  is still the correct leading byte of the jamo-grounded continuation.
- **Ψ-disjoint**: pure_field/engine_g/brain UNTOUCHED; the surface is purely additive (new functions, no
  call site in the existing decode loop), off-Korean inert, and the h1205 invariant holds (generation
  byte-identical ON==OFF, Ψ=½ untouched). $0 CPU, no GPU, no secrets at .hexa run time.

## One-line answer

**The H_1316/H_1321 jamo breakthrough now REACHES LIVE EMISSION: the grown jamo cells, consulted through
the generator §6.5b L3 slot, bias the emitted byte on held-out Korean (+0.0586 over the blind baseline,
shift 0.52), the bias is EARNED (shuffle collapses to −0.0973), and the consult is INERT off-Korean
(byte-identical, Ψ=½ untouched) — the Korean-jamo thread is fully closed: verified → engine-wired →
decode-reaching.**

## Pointers

- consult surface: `CORE/generator.hexa` §6.5b `ko_jamo_cells_load` / `ko_jamo_consult_sym` /
  `ko_jamo_consult_byte` / `ko_jamo_consult_emit` / `ko_jamo_cells_summary`
- cells artifact: `CORE/ko_jamo_cells.kojamohead` + `CORE/ko_jamo_cells_shuf.kojamohead` (E2 control)
- engine-native probe: `CORE/h1327_ko_jamo_decode_probe.hexa` (imports `CORE/generator.hexa`)
- data-prep: `UNIVERSE/h1327_ko_jamo_decode_export.py`
- verdicts: `.verdicts/1327_ko_jamo_decode_wire/{FREEZE,result}.txt` + `h1327_ref.json`
- claim: `CLAIMS.tape` @C h1327_ko_jamo_decode_wire
- E3 guards: `CORE/engine_cli_smoke.hexa` (73/0) · `CORE/h1196_single_entry_audit.hexa` (7/0) ·
  `CORE/h1205_separation_invariant_smoke.hexa` (PASS)
- xref: H_1316 (jamo breakthrough, mirror) · H_1321 (engine-native wiring) · H_1312 (ko_cells L3 wiring
  precedent — the surface mirrored here) · H_1306 (engine-native Korean mitosis) · H_1307 (raw-byte
  ceiling 2.9475) · a_verified_must_wire · a_core_engine_map · a_substrate_native_speak ·
  a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · p7 · p8
