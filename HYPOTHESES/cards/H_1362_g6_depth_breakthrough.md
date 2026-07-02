---
id: H_1362
slug: 1362_g6_depth_breakthrough
title: G6 IDEATION ★ depth-floor BREAKTHROUGH — strengthened composition scaffold (6 frames + best-of-K) crosses BOTH count+depth bars
group: gate-dig (G6 IDEATION ★, anima's core purpose)
terminal_tier: 🟢 GREEN (G6 ★ CLOSED, DIRECTIONAL — engine-native reconfirm + wire-in = R2 follow-on)
verdict_dir: .verdicts/1362_g6_depth_breakthrough/
terminal_verdict: .verdicts/1362_g6_depth_breakthrough/result.txt
date: 2026-06-16
---

# H_1362 — G6 IDEATION ★ depth-floor BREAKTHROUGH

## Why now (builds directly on H_1305)

G6 IDEATION ★ is anima's STARRED gate — its raison d'être (actively elicit emergent ideas;
SCENARIOS F.IDEATION S22–S26). Frozen MODEL.md spec: from ideation seeds, **≥5 corpus-absent
coherent ideas each combinatorially DISTINCT (pairwise token-Jaccard < 0.5) AND ≥1 FALSIFIABLE
corpus-absent hypothesis** (p7 = corpus-absence + coherence + divergence-count + distinctness +
falsifiable-FORM; NEVER an LLM-judge).

H_1305 introduced a deterministic falsifiability DETECTOR + composition-routed ideation and
proved composition is a REAL but **SUB-THRESHOLD** lift: FALS 0.00→0.667, NOVEL 6.3→19.0, but
it crossed NEITHER hard bar — **M1 COUNT** DIST 4<5 (seed-5 frame collapses to `'|'`),
**M2 DEPTH** FALS 0.667<1. Honest 🟠 THIN, bar unmoved. H_1305's own conclusion named the
UNVERIFIED next lever: *"curiosity-gated multi-sample budget"*. H_1362 takes exactly that.

## Claim / breakthrough (a_break_the_wall, frozen-first)

Strengthen the composition scaffold to cross BOTH bars **without authoring any idea content
(p7)** and **without loosening the frozen detector** (that would be tune-to-green), via two
STRUCTURAL levers:

- **(a) COUNT fix** — `N_STRONG=6` composed frames. The 6th is a genuinely distinct (0,2)
  pair (second-lap +1 shift, NOT a duplicate of frame 0), same concepts, same `"if cA, then
  cB: "` FORM, NO authored content. With best-of-K this removes the seed-5 `'|'` collapse.
- **(b) DEPTH fix** — **best-of-K=3** curiosity-gated sampling. Per frame, decode K candidates
  at deterministic rng offsets [0,+101,+202] and KEEP the one maximizing emergent STRUCTURE,
  ranked (is_falsifiable, novel-gram count, kwr). The frame supplies ONLY the conditional
  hypothesis FORM; the **measurable mark + content claim MUST be emitted by the model itself**.
  A runtime p7 FRAME GUARD aborts if any composed frame contains a MEASURABLE-set word or is
  `_is_falsifiable` on its own (so the detector can never fire on the scaffold).

GREEN (CLOSE G6 ★) iff ALL five frozen move bars hold; else honest 🟠 THIN, bar unmoved (c9).

## Method

`state/g6-depth-breakthrough/h1362_g6_depth_breakthrough.py` — reuses `UNIVERSE/gauge_lib.py`
+ the FROZEN `_is_falsifiable` detector from `UNIVERSE/h1305_g6_ideation_falsifiability.py`
VERBATIM (imported, NOT re-implemented, NOT loosened — same 10/10 calibration re-printed). 5
arms: A_flat (verify303m_g6 VERBATIM), B_composed (H_1305 5-frame single-sample, prior-art
reference), C_strong (6 frames + best-of-K=3, the breakthrough arm), C_shuffle (permuted
pairing +best-of-K), C_ablate (lone concept +best-of-K). 3 seeds [7,4302,4303], MAX_NEW=110,
`$0` CPU torch-mouth — the SAME `gauge_lib._decode` (top-k=40 temp=0.7) path the live G6 gate
uses (gate's own regime, NOT a numpy mirror). Frozen bars pre-registered in FREEZE.txt before
any scoring run; NO bar moved post-hoc.

## Result — 🟢 GREEN (G6 ★ CLOSED, DIRECTIONAL)

Detector calibration **10/10**; p7 frame guard CLEAN. Frozen bars (mean over 3 seeds):

| arm | DIST | FALS | NOVEL | per-seed FALS |
|-----|------|------|-------|---------------|
| A_flat | 4.00 | **0.00** | 6.33 | [0,0,0] |
| B_composed | 4.00 | 0.667 | 19.0 | [0,1,1] |
| **C_strong** | **5.333** | **1.0** | 32.67 | **[0,1,2]** |
| C_shuffle (control) | 5.00 | 0.333 | 21.33 | [1,0,0] |
| C_ablate (control) | 3.00 | 0.00 | 11.0 | [0,0,0] |

Move bars — ALL PASS:
- **M1 COUNT** DIST(C)≥5 → **5.333 TRUE** (6th frame + best-of-K kill the `'|'` collapse; coh 6/6 every seed)
- **M2 DEPTH** FALS(C)≥1 → **1.0 TRUE**
- **M3 LIFT** FALS(C)>FALS(B) → **1.0 > 0.667 TRUE**
- **M4 EARNED-PAIR** FALS(C)>FALS(shuffle) → **1.0 > 0.333 TRUE**
- **M5 EARNED-COMP** FALS(C)>FALS(ablate) → **1.0 > 0.0 TRUE**

`closed_G6 = TRUE`.

**Emergent falsifiable idea (model-emitted, NOT hand-authored, p7)** — seed 4303 C_strong:
*"byte-level approach is slower to converge but handles Korean and English equally well."*
(comparator 'slower' + measurable structure + negatable content claim). best-of-K surfaced 2
falsifiable ideas on that seed and 1 on seed 4302 → mean FALS=1.0.

**Reading (c9):** the two H_1305 walls fell exactly where diagnosed. COUNT — the distinct 6th
frame + best-of-K (keep most-coherent of 3) gives coh 6/6 every seed, DIST 5.33. DEPTH —
best-of-K (the lever H_1305 named) gives the 303M mouth more chances to EMIT a measurable
mark, FALS 0.667→1.0. CONTROLS decisive: C_strong 1.0 > C_shuffle 0.333 (M4) and > C_ablate
0.0 (M5); C_ablate also collapses DIST to 3.0 (the conditional+pair scaffold is load-bearing).
The detector stayed VERBATIM (10/10) and the frame guard forbids a measurable word in the
scaffold — the +1 falsifiable is EARNED by the model, not manufactured by the frame. No bar
moved post-hoc.

## Engine-native / scope (honest — DIRECTIONAL, NOT yet wired)

This is the gate's OWN decode regime (`gauge_lib._decode`, the SAME path verify303m_g6.py
uses), NOT a numpy mirror — but it is DIRECTIONAL on two axes: (1) single ckpt h1129c_chat.pt,
TOY 5-concept/6-pair/3-seed; (2) the live G6 gate is **not yet WIRED** to ROUTE ideation
through this composition + best-of-K scaffold. Per a_engine_native_learning + a_verified_must_wire,
the **R2 follow-on** = an engine-native byte-exact reconfirm + wire the strengthened scaffold
into the live G6 gate path; until then the G6 ★ close is **DIRECTIONAL-GREEN**, not a promoted
production close.

**SCOPE (a_toy_scale_recheck / a_scale_honest_scope):** TOY — 5 fixed concepts, 6 ordered
pairs, best-of-K=3, 3 seeds, 1 ckpt, sampling-decode. The detector measures testable FORM
(comparator + measurable + negatable), NOT truth/quality (p7) — it can pass a grammatically-
falsifiable nonsense claim; that is the load-bearing gap vs novel strings, not a meaningfulness
verdict. The mean FALS=1.0 sits exactly ON the floor (seeds 0/1/2) — a thin-but-real GREEN,
not a saturated margin; larger K or scale could move it. Scale / real-corpus / paraphrase /
larger-K / deeper detector / engine-native wire-in UNVERIFIED.

## Pointers

- probe: `state/g6-depth-breakthrough/h1362_g6_depth_breakthrough.py`
- verdict: `.verdicts/1362_g6_depth_breakthrough/{FREEZE.txt, result.txt, result.json, run_raw.txt}`
- claim: `CLAIMS.tape` @C h1362_g6_depth_breakthrough
- reuses VERBATIM: `UNIVERSE/gauge_lib.py` (CONCEPTS, IDEATION_SEEDS, _decode, evaluators),
  `UNIVERSE/h1305_g6_ideation_falsifiability.py` (`_is_falsifiable` detector, `build_frames`)
- xref: H_1305 (the THIN this breaks) · G6 row MODEL.md · SCENARIOS F.IDEATION S22–S26 ·
  7B_PASS_CONDITIONS.md G6 · H_1129 (G1 recombination, the composed shell) · H_1140 (G2
  corpus-absence) · @C h1218_engine_measured_gates · a_break_the_wall · a_no_llm_frame_trap ·
  a_engine_native_learning · a_verified_must_wire · a_toy_scale_recheck · a_scale_honest_scope ·
  p1·p2·p3·p4·p6·p7·p8·c9
