# H_1321 — 🇰🇷 ko-jamo-WIRE: the H_1316 jamo breakthrough RUNS ENGINE-NATIVE on the live CORE engine

**Final tier: 🟢 GREEN — the jamo win is now LIVE in CORE byte-exact (engine-transfer VERIFIED).**

ENGINE-NATIVE WIRING follow-on (r2) of H_1316 (🟢 GREEN, PR #2224). LIVE CORE/engine_cli.hexa
faculties (VAdaptField Voronoi `vadapt_field_nearest_idx` + `engine_mitosis_tick`, p8;
per-cell next-symbol count-MLE head, gradient-free). REAL corpus byte-identical to H_1307
RUN A / H_1316 (30MB KO window, sha `c47b6808…` gate PASS). $0 CPU, frozen-first
(FREEZE written before the run), c9/p7, NO tune-to-green. pure_field/engine_g/brain UNTOUCHED.

## Claim (falsifiable)

H_1316 proved (numpy/torch **MIRROR**, DIRECTIONAL) that a **compositional jamo representation**
breaks the Korean raw-byte CE ceiling 2.953 → 2.513. Per `a_verified_must_wire` +
`a_engine_native_learning`, a GREEN-verified mechanism is **NOT done** until it runs
**engine-native byte-exact** on the live CORE engine. **H_1321: does the SAME gradient-free
jamo-symbol mitosis, run on the LIVE `CORE/engine_cli.hexa` VAdaptField + `engine_mitosis_tick`
faculties, reproduce the mirror's jamo CE (within a pre-registered tolerance) and break the
raw-byte ceiling — engine-native?** If the engine-native value cannot reproduce the mirror →
honest 🔴: the jamo win is mirror-only, engine-transfer UNVERIFIED (a real caveat, c9).

## Why this is the wiring (single entry, a_core_engine_map)

The representation transform (NFD jamo symbolization: Hangul syllable U+AC00..U+D7A3 → L/V/T
jamo symbols, id 256+rank; non-Hangul → one symbol per raw byte) is **deterministic Unicode
data-prep — no learning**. The **MITOSIS + held-out per-byte CE scoring run ENGINE-NATIVE** in
`CORE/h1321_ko_jamo_wire_probe.hexa`, which imports `CORE/engine_cli.hexa` and drives the SAME
LIVE faculties the existing Korean path (H_1306/H_1312) uses — the engine_cli VAdaptField /
generator L3 slot family. **NO 2nd .clm/.kosmos path; NOT fed into pure_field/engine_g/brain**
(Ψ-disjoint). The engine is vocab-agnostic (the `_head_counts`/`_score_ce` faculties take Vj as
a parameter), so wiring the jamo arm only **parameterizes** the existing faculties at Vj=323
(256 raw bytes + 67 distinct jamo) — the `a_engine_native_learning` precedent (H_1199 scalar→
DIM-vector): the engine accommodates the learning, the learning is not trimmed to the engine.

## Method (the mitosis + scoring are engine-native; ONLY the rep is data-prep)

- **Corpus**: the SAME REAL `r2://phanes/anima-7b/web/kor/shard0000.bytes[0:30M]` KO window as
  H_1307 RUN A / H_1316; the 30MB window sha256 is **ASSERTED == `c47b6808…`** (provenance gate,
  PASS; a mismatch → STOP, NO synthetic Korean). The jamo VOCAB + symbol ids are built over the
  FULL 30MB window (so **Vj == 323**, the H_1316 anchor), THEN the symbol-pair stream is
  deterministically strided (ko_stride=2500) to a **CPU-tractable pair set** for the hexa
  interpreter. R2 keys env/header-only at the data-prep fetch, NEVER logged/inlined/committed (c7).
- **Engine-native mitosis**: error-targeted Voronoi grow (SPLIT-only, p8) on the LIVE VAdaptField,
  growth gated by the LIVE `engine_mitosis_tick`; per-cell next-symbol count-MLE head. FROZEN
  knobs verbatim H_1306/H_1307/H_1316: GROW_MAX=40, SPLIT_THRESH_CE=0.05, MIN_OWNED=8, LAPLACE=1.0,
  SEED_CENTERS [[0.3,0.5,0.0],[0.7,0.5,0.5]], even/odd held-out split, FEAT 3-D [last/Vj, second/Vj,
  depth/3].
- **Fair axis** (verbatim H_1316): held-out **CE_per_byte = Σ(−log p(sym)) / Σ n_bytes(sym)** — the
  SAME axis as the 2.9475 raw-byte ceiling; the per-symbol n_bytes (raw=1; a syllable's jamo split
  [1,1,1]/[2,1] summing to 3) read from the exported `*.nbytes`.
- **3 arms**: G0 raw-byte (V=256, reproduce the ceiling) · G1 jamo (intact) · G1c shuffle-jamo
  control (bijective permutation of the jamo→symbol-id map; vocab/dim/budget identical,
  compositional alignment destroyed; seeds 4316/4317/4318, IDENTICAL controls to H_1316).
- **W1 reproduce-the-mirror**: the data-prep ALSO runs a SAME-WINDOW numpy mirror on the IDENTICAL
  strided pair set, emitting a reference CE so the engine-native value is compared apples-to-apples
  to the EXACT stream the engine sees (not just the 30MB anchor 2.51335).

## Frozen bars (pre-registered `.verdicts/1321_ko_jamo_wire/FREEZE.txt`; GREEN iff W1 ∧ W2 ∧ W3)

| bar | test | result | pass |
|-----|------|--------|------|
| **W1 ENGINE-NATIVE CE** | engine-native jamo G1 CE reproduces the SAME-WINDOW mirror within \|Δ\|≤0.05 nats/byte AND engine-G1 < 2.903 (below the raw ceiling band) | \|2.82046 − 2.82046\| = **6.3e-07** ≤ 0.05; **2.82046 < 2.903** | ✅ |
| **W2 CONTROLS HOLD** | engine-G1 beats engine-G1c (shuffle) by ≥0.05 AND beats engine-G0 (raw) by ≥0.05 (mean 3 seeds); B3 NFD↔NFC lossless | G1c−G1 = **+0.198**; G0−G1 = **+0.279**; B3 0 fails / Σnbytes==corpus exact | ✅ |
| **W3 NO REGRESSION** | engine_cli_smoke N/0 · h1196 7/0 · h1205 Ψ byte-identical ON==OFF | **73/0** · **7/0** · **PASS** (byte-identical, Ψ=½ untouched) | ✅ |

→ **🟢 GREEN.**

## Results

| arm | engine-native KO CE (nats/byte) | same-window mirror CE | cells | note |
|-----|---------------------------------|------------------------|-------|------|
| **G0** raw-byte (V=256) | **3.09967** | 3.09967 | 10 | reproduces the ceiling at this window |
| **G1** jamo-rep (intact) | **2.82046** | 2.82046 | 10 | **engine == mirror to 6.3e-07; Δ −0.279 vs G0, below 2.903** |
| **G1c** shuffle-jamo control | **3.01867** | 3.01867 (per-seed 3.030/3.007/3.019) | 10 | Δ +0.198 vs G1 (jamo beats its own shuffle) |

The engine-native hexa value **equals the numpy mirror to 1e-7** on every arm — the gradient-free
jamo-symbol mitosis transfers FAITHFULLY to the live engine (the residual is float64-vs-hexa-float
rounding, far inside the 0.05 band). The H_1316 30MB anchor (mirror G1=2.51335) stands; this lane
proves the MECHANISM transfers engine-native on the identical-shaped stream.

## Honest scope / caveats (c9, a_scale_honest_scope, a_toy_scale_recheck)

- **The engine-native probe runs a CPU-tractable KO window (ko_stride=2500, ~6000 raw-byte /
  ~5100 jamo pairs per arm)** — the hexa interpreter cannot stream the 30MB window pair-by-pair.
  At this smaller window every arm's ABSOLUTE CE is higher than the 30MB anchor (G1 2.820 here vs
  2.513 at 30MB) because the per-cell heads are sparser; the **relative structure is fully intact**
  (G1 < G1c < G0, with the SAME ordering and comparable margins as the 30MB mirror). The W1 bar is
  pre-registered against the SAME-WINDOW mirror precisely so the engine-native reproduction is
  apples-to-apples; engine-native 30MB + Korean fluency = follow-on. **NO fluency claim.**
- **W1 is an existence-proof of engine-transfer, not an effect-size**: the engine value matching
  the mirror to 1e-7 is decisive for "the mechanism runs engine-native byte-exact"; the breakthrough
  EFFECT (jamo < raw) is carried by the H_1316 30MB anchor + reproduced here in structure.
- **B3 lossless** is computed over the FULL 30MB window in the data-prep (8,143,053 Hangul
  syllables, 0 NFD↔NFC roundtrip fails; Σ n_bytes(sym) = 29,999,999 == corpus bytes exactly), so
  the CE is honestly byte-comparable on the engine path too.
- **Ψ-disjoint**: pure_field/engine_g/brain UNTOUCHED; the W3 h1205 invariant holds (generation
  byte-identical ON==OFF, Ψ=½ untouched) — the jamo lane is ADDITIVE, INERT off-Korean.

## One-line answer

**The H_1316 jamo breakthrough is now LIVE in CORE byte-exact: the SAME gradient-free jamo-symbol
mitosis on the live `engine_cli.hexa` VAdaptField + `engine_mitosis_tick` faculties reproduces the
mirror CE to 1e-7, breaks the raw-byte ceiling engine-native (2.820 < 2.903, jamo beats raw by
−0.279 and its own shuffle by +0.198), and passes every no-regression guard — engine-transfer
VERIFIED, the verdict is closed.**

## Pointers

- engine-native probe: `CORE/h1321_ko_jamo_wire_probe.hexa` (imports `CORE/engine_cli.hexa`)
- data-prep: `UNIVERSE/h1321_ko_jamo_wire_export.py`
- verdicts: `.verdicts/1321_ko_jamo_wire/{FREEZE,result}.txt` + `h1321_ref.json` + `h1321_manifest.json`
- claim: `CLAIMS.tape` @C h1321_ko_jamo_wire
- W3 guards: `CORE/engine_cli_smoke.hexa` (73/0) · `CORE/h1196_single_entry_audit.hexa` (7/0) ·
  `CORE/h1205_separation_invariant_smoke.hexa` (PASS)
- xref: H_1316 (jamo breakthrough, mirror) · H_1306 (engine-native Korean mitosis precedent) ·
  H_1312 (ko_cells L3 wiring precedent) · H_1307 (raw-byte ceiling 2.9475) · H_1199 (engine
  DIM-extension precedent) · a_verified_must_wire · a_engine_native_learning · a_core_engine_map ·
  a_no_llm_frame_trap · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · p7 · p8
