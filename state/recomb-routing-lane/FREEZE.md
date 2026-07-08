# FREEZE — H_9235 H2-lite (γ binding-lane · earned×trained cell) · frozen BEFORE any hidden dump

**date** 2026-07-09 · **owner spend-go**: "둘다 go" (H1+H2 authorized; fork B GPU gated on lite verdict per Fable) ·
**design** Fable (`state/g1_c2_grounded/../fable_h2_gamma_design.md` reasoning · scratchpad) · **implements** card H_9235.

## The unmeasured cell (why this is discovery, not H_1840-confirmation)
```
             atom source          bind operator            result
 H_9234       handed (clean)   ×  trained (interaction)  → 1.000 PASS (proven)
 #3135        blind (learned)  ×  fixed (VSA)            → FAIL
 H_1840       blind (learned)  ×  trained-via-CE         → FAIL (signal never reaches bind)
 H2-lite  ►   earned (real 303M hiddens) × trained-via-composition-signal → THE UNTESTED CELL
```
H2-lite's training signal = the systematic zero-unary-MI XOR table on SEEN pairs only (NOT corpus CE) — the bind
path's ONLY loss, so gradient provably reaches it (dodges H_1840's learning-signal trap). Atoms are earned from real
303M hiddens (blind, per evaluate-py-3), NOT handed. Only the supervision target is synthetic (dodges the handed trap).

## Frozen inputs (sha before dump)
- **ckpt**: `~/anima-weights/e1_slw_303m/e1_slw_303m.final.clm` (293,119,146 B · canonical E1-SLW 303M).
- **concepts.json** sha `20f32916d8c0` — 32 concepts (5 ρ·weave-gate + 27 nouns), 5-bit codes by seeded-perm(7),
  zero-unary-MI verified (every bit marginal 0.5). 16 content-matched paraphrases each (prompt ENDS with concept →
  T=24 last-position penultimate = the atom).
- **unary_prompts.json** sha `5d56e00147b3` — 512 items (32×16), split 8 train / 8 test paraphrases.
- **pair_prompts.json** sha `8f1e354242fe` — 992 items (842 train, 150 held-out; held split mirrors operator_test.py H_9234 verbatim).

## Frozen bars (pre-registered · no tune-to-green · card H_9235 table)
| gate | bar |
|---|---|
| H1 unary probe | held-out-paraphrase concept-id acc ≥0.80 clean / <0.55 blind (expected-pass · NOT a γ greenlight) |
| RUNG-a operator (real atoms) | ≥0.85 PASS · 0.60–0.85 partial · ≤0.60 FAIL · ≥2/3 seeds |
| additive control | ≤0.60 must FAIL (H_9234 gate replication) |
| fixed-VSA control | ≤0.60 must FAIL (#3135 replication · trained adapter load-bearing) |
| handed positive control | ≥0.85 must PASS (harness learnability · evaluate-py-3) |
| shuffle | ≈0.5±0.1 (bind-destruction) |

**CRACK(rung-a)** = real-atom operator ≥0.85 ∧ additive FAIL ∧ fixed-VSA FAIL ∧ handed PASS ∧ shuffle chance
→ rung b (superposed-real, per-position pair hiddens) → fork A wiring → engine-native system-G1 = the G1 crack.
**modal (Fable ~85%)** = real-atom operator ≤0.60 while handed PASS ⇒ blind real hiddens not operator-grade
(#3135 recurses), wall localizes to atom-cleanness → fork B (trunk curriculum, GPU) the only remaining lever.

## verdict-integrity guard (convergence clm-decode-py-2)
A low H1 unary probe (<0.55) is INVALID-SUSPECT, not a blind result, UNTIL the dump's poscontrol distinguishability
(cos of two distinct-concept hiddens < 0.999) rules out hexa/py conditioning-collapse skew. Re-dump if suspect.

## Scope (honest)
Engine-native py 2-production hidden dump = engine-native MECHANISM measurement of the frozen trunk representation
(atom cleanness / slot recovery / operator on real hiddens) — TERMINAL-eligible as a REPRESENTATION verdict, NEVER as
a G1 verdict (only fork A's wired system-G1 on frozen bars is that). A rung-a PASS = "supervised-earnable cleanness",
not self-organized/emergent atoms.
