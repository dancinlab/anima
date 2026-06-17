---
id: H_1435
slug: 1435_continued_pretrain
title: G6 IDEATION ★ FALS-depth wall — TRAINING side r1 — continued-pretrain on falsifiable-claim corpus (303M full-weight)
group: gate-dig (G6 IDEATION ★) — FALS-depth wall, TRAINING-side test #1 (capacity vs learn-gap separation)
terminal_tier: 🧱 WALL=CAPACITY (form installed 0→5, held-out holds, control inert, but cross-shuffle does NOT collapse)
wired: N/A (did not cross — a_verified_must_wire GREEN-only)
verdict_dir: .verdicts/1435_continued_pretrain/
terminal_verdict: .verdicts/1435_continued_pretrain/result.txt
date: 2026-06-17
---

# H_1435 — G6 IDEATION ★ FALS-depth: continued-pretrain (TRAINING side)

## Why (the question this isolates — a_break_the_wall, c16)

Five prior digs (H_1305/1309/1314/1431/1432/1434) found the G6 FALS-depth floor unmovable at 303M
from the ELICITATION side (composition-route, form-scaffold, external bind, negation-slot, two-pass).
All concluded 🧱 CAPACITY. But every one held the WEIGHTS fixed. The open question they all named:
**is the wall a CAPACITY ceiling, or just a TRAINING-DISTRIBUTION gap?** The base chat corpus rarely
contains falsifiable-claim FORM, so a frozen mouth might simply never have learned to bind
comparator×measurable into a negatable claim. H_1435 tests this directly: **full-weight continued-
pretrain on a corpus DENSE in falsifiable claims**, then re-measure the FROZEN 5-bar. If training
crosses (incl. the decisive cross-shuffle COLLAPSE) → wall was a LEARN-GAP. If it does not → CAPACITY.

## Method (frozen-first, c9/p7)

- base = `state/chat_303m/h1129c_chat.pt` (303,097,856 params; d=1024 L=24 H=16 block=512). PRESERVED — wrote a NEW ckpt.
- training corpus = structurally-generated falsifiable claims over subjects DISJOINT from the gauge CONCEPT keywords / eval seeds / held-out seeds (anti-tune-to-green: the model cannot memorize an eval string).
- full-weight AdamW lr=3e-5, 400 steps, on a rented vast A100-SXM4-80GB pod (41270711), torch 2.5.1+cu121.
- FROZEN 5-bar declared BEFORE training (state/1435_continued_pretrain/g6_common.py docstring): B1 FALS_in≥1 · B2 DIST_in≥5 · **B3 CROSS-SHUFFLE COLLAPSE** (re-weld each idea's clause with a RANDOM measurable from a DIFFERENT idea; FALS_shuf<FALS_in) · B4 HELD-OUT FALS_ho≥1 · B5 vs-base FALS_in≥base+1.
- CONTROL (tune-to-green killer): a sibling trained on the SAME bytes TOKEN-SHUFFLED (structure destroyed) must be INERT.
- detector = h1305 `_is_falsifiable` imported VERBATIM (COMPARATOR/MEASURABLE frozen sets); decode = gauge_lib._decode top-k=40 temp=0.7 max_new=110 (live G6 path); seeds [7,4302,4303].

## Result (mean 3 seeds — captured pod output, NOT self-judged)

| arm | FALS_in | DIST_in | FALS_shuf | FALS_ho |
|---|---|---|---|---|
| BASE | 0.0 | 3.0 | 0.0 | 0.0 |
| TRAINED | **5.0** | **5.0** | **5.0** | **5.0** |
| SHUFFLE-CORPUS (ctrl) | 0.0 | — | — | 0.0 |

- B1 FALS≥1 = 5.0 **PASS** · B2 DIST≥5 = 5.0 **PASS** · **B3 cross-shuffle FALS_shuf 5.0 < FALS_in 5.0 → FAIL (NO COLLAPSE)** · B4 held-out 5.0 **PASS** · B5 vs-base 5.0≥0+1 **PASS** · CTRL shuffle-corpus inert (lift_real 5.0 − lift_shuf 0.0 ≥ 1) **PASS**.

## Verdict 🧱 WALL=CAPACITY (c9)

Continued-pretrain DOES install the falsifiable FORM (base 0.0 → trained 5.0), it GENERALIZES off the
training distribution (held-out 5.0), and the lift is REAL learning not an artifact (the shuffle-corpus
control reads 0.0 — destroying structure kills the lift). So the **learn-distribution-gap is real for the
FORM**: training the form moves B1/B2/B4/B5. BUT the decisive **cross-shuffle does NOT collapse** —
swapping the measurable leg between ideas leaves FALS=5.0 unchanged → the legs are SEMANTICALLY
INTERCHANGEABLE shells, exactly the H_1434 failure mode. The purely-structural H_1305 detector cannot
distinguish an earned idea-specific binding from any-comparator+any-measurable+content, and 303M
produces the form WITHOUT idea-specific semantics. Training fixes the form-gap but NOT the
semantic-binding capacity. Loosening the detector to demand semantic earning = tune-to-green (forbidden).
This is the FIRST training-side confirmation of the capacity thesis (prior 5 digs were elicitation-side).
base ckpt NOT overwritten. trained ckpt = path-only (c5, pod destroyed; reproducible from scripts).

wired: N/A.
