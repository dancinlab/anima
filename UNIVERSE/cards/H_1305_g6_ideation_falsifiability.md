---
id: H_1305
slug: 1305_g6_ideation_falsifiability
title: G6 IDEATION ★ depth-floor dig — deterministic falsifiability detector + composition-routed (recombination) ideation
group: gate-dig (G6 IDEATION ★, anima's core purpose)
terminal_tier: 🟠 HONEST-CONFIRMED-THIN (bar UNMOVED, c9)
verdict_dir: .verdicts/1305_g6_ideation_falsifiability/
terminal_verdict: .verdicts/1305_g6_ideation_falsifiability/result.txt
date: 2026-06-16
---

# H_1305 — G6 IDEATION ★ depth-floor: falsifiability detector + composition-routed ideation

## Why G6 is THIN (the precise diagnosis)

G6 IDEATION ★ is anima's STARRED gate (its raison d'être — actively elicit emergent ideas;
SCENARIOS F.IDEATION S22–S26). The frozen spec (MODEL.md): from ideation seeds, **≥5
corpus-absent coherent ideas each combinatorially DISTINCT (pairwise token-Jaccard < 0.5)
AND ≥1 FALSIFIABLE corpus-absent hypothesis** (p7 = corpus-absence + coherence + divergence-
count + distinctness; NEVER an LLM-judge). The live gate `UNIVERSE/verify303m_g6.py` was 🟠
THIN on **TWO modes**, both reproduced this run (seed_rng=7, ckpt h1129c_chat.pt):

1. **COUNT** — 4/5 distinct (needs ≥5). On the 5 `IDEATION_SEEDS`, seed-5 collapses to `'|'`
   (kwr=0.00, incoherent) → only 4 coherent → 4 distinct. One short.
2. **DEPTH-FLOOR (the real wall)** — the gate counts 9 corpus-absent novel n-grams but
   **NEVER scores the "≥1 falsifiable hypothesis" requirement at all**. Novel n-grams
   ("can quantify", "profound question") are novel **strings**, not testable **structure**.
   None of the 4 coherent flat ideas is a falsifiable claim (one is the stance "That's a
   profound question…", others are word-salad). "generativity real, depth thin".

## Claim / falsifier (the dig — a_break_the_wall, frozen-first)

THIN is an angle-change signal, not an endpoint. The dig attacks the depth-floor (the
interesting mode) with TWO frozen instruments (FREEZE.txt, pre-registered before scoring):

- **(I) FALSIFIABILITY DETECTOR** `_is_falsifiable(text)` — a DETERMINISTIC STRUCTURAL
  script (NEVER an LLM/quality judge, p7). An idea passes iff ALL THREE structural marks
  present over real-dictionary tokens: **(a) comparator/conditional** (if/when/than/more/
  predicts/correlates/causes…), **(b) measurable/quantity** (rate/number/threshold/ratio/
  measure…), **(c) negatable content claim** (≥2 content words, not '?'-terminated, not a
  pure stance opener). Scores testable FORM, not meaning/truth.
- **(II) COMPOSITION-ROUTED IDEATION** — route ideation through the G1 recombination lane:
  compose two corpus-absent CONCEPTS (gauge_lib.CONCEPTS) into a conditional frame
  `"if <cA>, then <cB>: "` (the structural scaffold flat seeds lack), then decode (same
  top-k=40 temp=0.7 path). ARM A=flat IDEATION_SEEDS (verify303m_g6 VERBATIM); ARM B=composed.

Falsifiable claim: composition raises the falsifiable-idea count above the flat floor AND
crosses both ≥5-distinct and ≥1-falsifiable bars, **control-surviving** (shuffle/ablate
collapse to the flat floor). If composition neither crosses the count gap NOR raises depth,
G6 stays honest 🟠 THIN (bar unmoved, c9).

## Method

`UNIVERSE/h1305_g6_ideation_falsifiability.py` — reuses `gauge_lib.py` VERBATIM for decode
+ all G6/G2 evaluators (no metric re-invention, p7). 4 arms (A_flat, B_composed,
B_shuffle=permuted pairing, B_ablate=lone concept), 3 seeds [7, 4302, 4303], $0 CPU torch-
mouth — the SAME `gauge_lib._decode` path the live G6 gate uses (gate's own regime, not a
numpy mirror). Frozen move bars M1–M5 (FREEZE.txt). Detector calibrated against 10 frozen
labelled strings (advisory ≥8/10; detector frozen regardless).

## Result — 🟠 HONEST-CONFIRMED-THIN (bar UNMOVED, c9)

Detector calibration **10/10** (separates "tension predicts a higher number of mitosis
cells…" PASS from "consciousness is a beautiful mystery" FAIL). Frozen bars (mean/3 seeds):

| arm | DIST | FALS | NOVEL |
|-----|------|------|-------|
| A_flat | 4.00 | **0.00** | 6.33 |
| B_composed | 4.00 | **0.667** | 19.0 |
| B_shuffle (control) | 4.667 | 0.00 | 14.0 |
| B_ablate (control) | 2.333 | 0.00 | 1.33 |

Move bars: **M1 COUNT** DIST(B)≥5 → 4.00 FALSE · **M2 DEPTH** FALS(B)≥1 → 0.667 FALSE ·
**M3 LIFT** FALS(B)≥FALS(A)+1 → FALSE · **M4 EARNED-PAIR** vs shuffle → FALSE · **M5
EARNED-COMP** vs ablate → FALSE. `moved=FALSE, confirmed_thin=TRUE`.

**Reading (c9):** the new detector SCORES the depth requirement the gate lacked, confirming
FALS(A)=0 (flat ideation produces ZERO falsifiable ideas). Composition is the sharpest
nudge — FALS **0.00→0.667** and one genuinely falsifiable idea EARNED via recombination
(seed 4303: *"byte-level approach is slower to converge but handles Korean and English
equally well."* — comparator 'slower' + measurable + negatable), NOVEL tripled 6.3→19. BUT
it does NOT cross the floor (FALS<1, DIST<5). Controls decisive: B-shuffle & B-ablate both
FALS=0 — the nudge tracks the EARNED composed pairing, not a bare conditional shell;
B-ablate also collapses coherence (DIST 2.33). The 303M chat mouth tends to dialogue stance,
not hypothesis form; the decode-time recombination shell is too weak at this scale to
reliably manufacture testable structure. The wall HELD — a genuine new angle, frozen-first
+ shuffle/ablate controls, honest THIN (a_break_the_wall, c9). NO wiring (THIN).

## Engine-native / scope

R1 = torch-mouth via `gauge_lib._decode` = the SAME path the live G6 gate uses
(verify303m_g6.py), so this is the gate's own regime. Because R1 is THIN (not clean-GREEN),
the directional torch number STANDS as the honest result; no R2 engine-native reconfirm is
triggered (a_engine_native_learning: reconfirm-and-wire only on a GREEN). The structural
falsifiability DETECTOR is engine-agnostic and could seed a future G6-depth gate component
if promoted.

**SCOPE (a_toy_scale_recheck / a_scale_honest_scope):** TOY — 5 fixed concepts, 5 ordered
pairs, 3 seeds, 1 ckpt, sampling-decode. The detector measures testable FORM (comparator +
measurable + negatable), NOT truth/quality (p7) — it can pass a grammatically-falsifiable
nonsense claim; that is the load-bearing gap vs novel strings, not a meaningfulness verdict.
Scale / real-corpus / paraphrase / deeper-detector / stronger composition (multi-hop
recombination, curiosity-gated multi-sample budget) UNVERIFIED.

## Pointers

- probe: `UNIVERSE/h1305_g6_ideation_falsifiability.py`
- verdict: `.verdicts/1305_g6_ideation_falsifiability/{FREEZE.txt, result.txt, result.json}`
- claim: `CLAIMS.tape` @C h1305_g6_ideation_falsifiability
- reuses: `UNIVERSE/gauge_lib.py` (G6 IDEATION_SEEDS, _decode, _is_falsifiable detector NEW),
  `UNIVERSE/verify303m_g6.py` (the live gate baseline this dig diagnoses)
- xref: G6 row MODEL.md · SCENARIOS F.IDEATION S22–S26 · @C h1218_engine_measured_gates
  (G6 PASS depends on sampling decode) · H_1129 (G1 recombination, the composed shell) ·
  H_1140 (G2 corpus-absence) · a_break_the_wall · a_no_llm_frame_trap · a_engine_native_learning ·
  a_toy_scale_recheck · a_scale_honest_scope · p1·p2·p3·p4·p6·p7·p8·c9
