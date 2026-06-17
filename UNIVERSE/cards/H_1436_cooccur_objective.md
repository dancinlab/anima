---
id: H_1436
slug: 1436_cooccur_objective
title: G6 IDEATION ★ FALS-depth wall — TRAINING side r2 — comparator∧measurable co-occurrence aux-objective (303M full-weight)
group: gate-dig (G6 IDEATION ★) — FALS-depth wall, TRAINING-side test #2 (variant objective, not just data)
terminal_tier: 🧱 WALL=CAPACITY (form installed but cross-shuffle does NOT collapse; aux saturated, even costs distinctness)
wired: N/A (did not cross — a_verified_must_wire GREEN-only)
verdict_dir: .verdicts/1436_cooccur_objective/
terminal_verdict: .verdicts/1436_cooccur_objective/result.txt
date: 2026-06-17
---

# H_1436 — G6 IDEATION ★ FALS-depth: co-occurrence aux objective (TRAINING side)

## Why

H_1431's bottleneck diagnostic: the 303M mouth emits a comparator OR a measurable but BOTH-in-one
0/15. H_1436 attacks that with a VARIANT OBJECTIVE (not just data, distinguishing it from H_1435):
add an AUXILIARY LOSS that rewards JOINT emission — within a sequence, push predicted prob mass onto
BOTH a comparator lead-byte AND a measurable lead-byte. CE + λ·cooccur_aux, on the same falsifiable-
claim corpus. If shaping the JOINT emission buys earned binding → learn-gap; else → capacity.

## Method (frozen-first, c9/p7)

- base = h1129c_chat.pt (PRESERVED, new ckpt). full-weight AdamW lr=3e-5, λ=0.5, 400 steps, vast A100 pod 41270711.
- aux = −mean over batch of (peak comparator-lead mass) × (peak measurable-lead mass) — shapes joint co-activation; does NOT author detector tokens into targets (anti-tune-to-green; corpus subjects + eval seeds disjoint).
- FROZEN 5-bar + shuffle-corpus control + detector/decode = IDENTICAL to H_1435 (state/1436_cooccur_objective/g6_common.py). seeds [7,4302,4303].

## Result (mean 3 seeds — captured pod output)

| arm | FALS_in | DIST_in | FALS_shuf | FALS_ho |
|---|---|---|---|---|
| BASE | 0.0 | 3.0 | 0.0 | 0.0 |
| TRAINED | **5.0** | 4.3333 | **5.0** | **5.0** |
| SHUFFLE-CORPUS (ctrl) | 0.0 | — | — | 0.0 |

- B1 FALS≥1 = 5.0 **PASS** · B2 DIST≥5 = 4.3333 **FAIL** · **B3 cross-shuffle 5.0 < 5.0 → FAIL (NO COLLAPSE)** · B4 held-out 5.0 **PASS** · B5 vs-base **PASS** · CTRL inert **PASS**.
- **KEY DIAGNOSTIC**: the aux co-occurrence reward SATURATED at −1.0000 from step 0 (captured in train.log) — peak joint mass on comparator+measurable lead-bytes is TRIVIALLY reachable, so the aux supplied ~no extra gradient over plain continued-pretrain. H_1436 effectively reduced to H_1435 plus a distinctness COST (DIST 5.0→4.33).

## Verdict 🧱 WALL=CAPACITY (c9)

The co-activation objective is INFORMATIVE-NULL: it saturates instantly (the model already trivially
co-activates the two lexical CLASSES), so it cannot teach the missing thing (idea-SPECIFIC pairing).
Form installs (0→5), held-out holds, control inert — same as H_1435 — but cross-shuffle still does NOT
collapse and the objective even costs distinctness (B2 fails). Shaping JOINT lexical emission does not
buy earned semantic binding. Confirms the capacity thesis from a 2nd training-side angle (variant objective).
base ckpt NOT overwritten. trained ckpt = path-only (c5).

wired: N/A.
