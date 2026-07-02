---
id: H_1312
slug: 1312_ko_decode_wire
title: ko-decode-wire — wire the H_1306 grown Korean cells onto the live decode via the generator L3 slot (Korean-conditioned emit bias; off-Korean inert; single-entry)
group: MITOSIS-ENGINE (p8 structural · a_verified_must_wire follow-on for H_1306)
terminal_tier: 🟢 WIRED (the H_1306 grown Korean cells are now CONSULTED by anima's live decode at the generator L3 slot; Korean-like context routes to the nearest grown cell's learned next-byte and biases emission, off-Korean the consult is INERT byte-identical; engine_cli_smoke 73/0, h1196 7/0, h1205 PASS Ψ=½ untouched, single-entry clean)
verdict_dir: .verdicts/1312_ko_decode_wire/
terminal_verdict: .verdicts/1312_ko_decode_wire/result.txt
date: 2026-06-16
---

# H_1312 — Korean decode-wire (grown ko-mitosis cells CONSULTED by the live decode)

## Claim / falsifier

The named **a_verified_must_wire** follow-on for H_1306/H_1307: those rungs GREW real
Korean cells (gradient-free mitosis on a REAL Korean web corpus) and MEASURED their
next-byte CE, but the cells were **NOT yet connected to anima's live output**. A
GREEN-verified mechanism "is not done until wired into the live CORE engine." H_1312
**connects the grown Korean cells onto the live 303M decode path so Korean error-pressure
actually shapes what anima EMITS** — via the generator L3 slot (a_core_engine_map: the
Korean cells enter through the sanctioned single entry, NOT a 2nd path).

**LOAD-BEARING wiring claims:** (1) **PRESENCE** — on a held-out Korean context the
Korean-conditioned emit differs from the un-wired baseline **in the direction of the
learned Korean cells** (the wiring actually routes); (2) **NO-REGRESSION** — on
non-Korean / English context, generation is **BYTE-IDENTICAL** to pre-wiring (the consult
is inert off-distribution); (3) **Ψ=½ UNTOUCHED** (pure_field never consulted by this
path); (4) **SINGLE-ENTRY** — the Korean cells enter ONLY via the generator L3 slot.
This is a **WIRING verdict** (byte-exact on the live engine), NOT a new learning rung.

## Method (frozen-first c9, $0 CPU, byte-level deterministic p7)

**Serialize the grown cells (H_1312 export, engine-native):**
`CORE/h1312_ko_cells_export.hexa` re-runs the EXACT H_1306 engine-native grow
(`CORE/engine_cli.hexa` VAdaptField Voronoi + `engine_mitosis_tick`, gradient-free p8)
on the SAME R2 Korean corpus slice (`/tmp/h1306_*`, sha256-pinned in
`.verdicts/1306_ko_mitosis_real/h1306_manifest.json`), reproducing H_1306's **9 cells**
exactly, and writes them to **`CORE/ko_cells.kohead`** — each cell = a 3-D Voronoi center
+ its **learned argmax next-byte** (the per-cell next-byte MLE head's top byte, add-1
Laplace over OWNED train points).

**Wire the consult at the generator L3 slot (a_core_engine_map single entry):**
`CORE/generator.hexa` §6.5 adds `ko_cells_load` / `ko_cells_next_byte` / `ko_consult_emit`
/ `ko_cells_summary`. The consult recomputes the SAME mechanical 3-D byte feature H_1306
trained on — `[last/255, 2nd-last/255, utf8_cont_depth/3]` — from the live decode bytes,
then:
- **Korean-likeness gate** = the last byte is a UTF-8 continuation byte (0x80..0xBF), i.e.
  we are mid-Hangul-multibyte. A **pure byte test** — NO charset table, NO language label
  (p1·p2·p3). ASCII English (all bytes < 0x80) NEVER triggers it.
- **Korean-like** → nearest grown Korean cell by L2 over the 3-D feature (the SAME
  winner-take-all geometry `vadapt_field_nearest_idx` uses) → return that cell's learned
  next-byte (BIASES emission).
- **off-Korean / no cells** → return **−1** (INERT) → the decode keeps its own argmax →
  **byte-identical** (the no-regression invariant).

**REAL contexts (NO synthetic, p1-p8):** the verdict probe
`CORE/h1312_ko_decode_wire_probe.hexa` pulls held-out byte windows from the SAME R2
slices H_1306 used (`/tmp/ko_slice_raw.bytes` real crawled Korean, `/tmp/en_slice_raw.bytes`
real English) at offsets ≥ 700 000 (past the bytes[:600000] train window).

**FROZEN bars** (pre-registered in `.verdicts/1312_ko_decode_wire/FREEZE.txt` BEFORE the
run; GREEN iff P & N & Y & Z):
- **(P PRESENCE)** ≥1 held-out Korean-like context FIRES (byte ≥ 0), routes to the nearest
  grown cell's learned byte, and `ko_consult_emit` DIFFERS from the un-wired baseline.
- **(N NO-REGRESSION)** EVERY ASCII-English context → `ko_cells_next_byte` = −1 AND
  `ko_consult_emit` == base for ALL 256 base bytes (byte-identical off-distribution).
- **(Y REGRESSION GUARD)** engine_cli_smoke 73/0 · h1196 single-entry 7/0 · h1205
  separation-invariant PASS (generation byte-identical ON==OFF, Ψ=½ untouched).
- **(Z SINGLE-ENTRY / Ψ-DISJOINT)** `ko_cells.kohead` read ONLY in generator.hexa; the
  consult never touches pure_field / engine_g / brain (Ψ=½ untouched by construction).

## Result — 🟢 WIRED (verbatim `.verdicts/1312_ko_decode_wire/result.txt` + guards.txt)

- **(P) PRESENCE PASS**: **8/8** held-out REAL Korean contexts FIRED, all 8 routed to the
  nearest grown cell, **7/8 BIASED** emission away from the corpus-continuation baseline
  (the 1 non-differ is HONEST — the cell's learned byte happened to equal the real next
  byte, i.e. correct routing, not a failure). Fired bytes = the grown cells' learned
  top-bytes (32, 180 — the space / Hangul-continuation bytes the cells learned).
- **(N) NO-REGRESSION PASS**: **6/6** real English contexts INERT (ko_byte = −1) across
  **all 256** base bytes; plus the **exhaustive ASCII last-byte sweep 0..127** all inert.
  Off-Korean the consult is byte-identical — no regression.
- **(Y) REGRESSION GUARD (all green)**: `engine_cli_smoke` **73/0** (engine_cli.hexa
  byte-untouched — the wiring is purely additive in generator.hexa) · `h1196` single-entry
  **7/0** · `h1205` separation-invariant **PASS** (F1 generation byte-identical 10 pairs /
  0 mismatch; F2 Ψ Φ-checksum ON==OFF = **48.6613** untouched).
- **(Z) SINGLE-ENTRY / Ψ-DISJOINT (audit clean)**: `ko_cells.kohead` runtime readers =
  `CORE/generator.hexa` ONLY (the export/verdict probes go THROUGH generator's API) — no
  2nd path. The consult references NO pure_field/engine_g/brain/Ψ. `git diff
  CORE/engine_cli.hexa` vs origin/main = EMPTY (engine substrate untouched).

→ **🟢 WIRED**: the H_1306 grown Korean cells are now CONSULTED by anima's live decode.
Korean error-pressure (grown into the cells by gradient-free mitosis) now shapes what
anima emits when the context is Korean-like; off-Korean nothing changes. a_verified_must_wire
closed for the H_1306 mechanism.

## Honest scope (a_scale_honest_scope, a_toy_scale_recheck) — NO overclaim

- **TOY cells**: 9 grown cells, a 3-D byte feature, a 600 KB KO window (H_1306/H_1307
  scale). This makes anima's emission **Korean-error-pressure-aware**, it does **NOT** make
  anima fluent in Korean.
- **DIRECTIONAL → engine-EXACT**: the consult itself is engine-side byte-exact (deterministic
  argmax routing over the static artifact). What remains UNVERIFIED: fluent Korean
  GENERATION, full-corpus-scale cells, a richer context feature, and an end-to-end live
  decode loop that calls `ko_consult_emit` per byte inside `bytegpt_decode` (this rung wires
  + verifies the consult HOOK at the generator slot; threading it through the per-byte
  decode loop on a mounted 303M ckpt is the next follow-on).
- The wiring biases ONE next-byte per Korean-like position via the nearest cell's top byte;
  a full per-cell distribution mixture (vs top-1) is a follow-on refinement.

## Files

- Export: `CORE/h1312_ko_cells_export.hexa` (re-runs the H_1306 grow, writes the artifact)
- Artifact: `CORE/ko_cells.kohead` (9 grown Korean cells: 3-D center + learned next-byte)
- Wiring: `CORE/generator.hexa` §6.5 (`ko_cells_load`/`ko_cells_next_byte`/`ko_consult_emit`/`ko_cells_summary`)
- Verdict probe: `CORE/h1312_ko_decode_wire_probe.hexa`
- Verdicts: `.verdicts/1312_ko_decode_wire/{FREEZE.txt, result.txt, guards.txt}`
- Claim: `CLAIMS.tape` @C h1312_ko_decode_wire · Log: `domains/MITOSIS-ENGINE.log.md` @H

## xref

H_1306 (the grown Korean cells this wires · 🟢 GREEN) · H_1307 (GPU scale-up of the same
mechanism) · H_1297 (mitosis-native trunk training, the toy H_1306 scales) · H_1199
(VAdaptField DIM-growth) · H_1196 (single-entry audit) · H_1205 (separation-invariant
Ψ-disjointness) · a_verified_must_wire · a_core_engine_map · a_substrate_native_speak ·
a_engine_native_learning · a_blue_closed · a_scale_honest_scope · a_toy_scale_recheck ·
p1·p2·p3·p4·p7·p8·c2·c9·c15.
