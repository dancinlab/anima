---
id: H_1437
slug: 1437_form_supervised
title: G6 IDEATION ★ FALS-depth wall — TRAINING side r3 — H_1314 negatable-form scaffold supervision → free gen (303M full-weight)
group: gate-dig (G6 IDEATION ★) — FALS-depth wall, TRAINING-side test #3 (internalize the H_1314 form)
terminal_tier: 🧱 WALL=CAPACITY (form internalized into free gen but cross-shuffle does NOT collapse; most extreme distinctness collapse)
wired: N/A (did not cross — a_verified_must_wire GREEN-only)
verdict_dir: .verdicts/1437_form_supervised/
terminal_verdict: .verdicts/1437_form_supervised/result.txt
date: 2026-06-17
---

# H_1437 — G6 IDEATION ★ FALS-depth: form-supervised internalization (TRAINING side)

## Why

H_1314 supplied the negatable-form scaffold EXTERNALLY (the model never owned it). H_1437 tests whether
SUPERVISING the model on the scaffold→completed-claim FORMAT makes the form NATIVE, evaluated on FREE
generation (no scaffold at eval). If form-supervision transfers to unprompted negatable claims AND the
cross-shuffle control collapses → the bind is earned and internalized → learn-gap. Else → capacity.

## Method (frozen-first, c9/p7)

- base = h1129c_chat.pt (PRESERVED, new ckpt). full-weight AdamW lr=3e-5, 400 steps, vast A100 pod 41270711.
- supervision targets = templated negatable-form lines ("a testable claim: if {s} changes, then the {m} of {s2} is {c} measured.") over training-only subjects DISJOINT from eval. EVAL is FREE (gauge IDEATION_SEEDS + held-out seeds; NO scaffold given).
- FROZEN 5-bar + shuffle-corpus control + detector/decode = IDENTICAL to H_1435 (state/1437_form_supervised/g6_common.py). seeds [7,4302,4303].

## Result (mean 3 seeds — captured pod output)

| arm | FALS_in | DIST_in | FALS_shuf | FALS_ho |
|---|---|---|---|---|
| BASE | 0.0 | 3.0 | 0.0 | 0.0 |
| TRAINED | **5.0** | **1.3333** | **5.0** | **5.0** |
| SHUFFLE-CORPUS (ctrl) | 0.0 | — | — | 0.0 |

- B1 FALS≥1 = 5.0 **PASS** · B2 DIST≥5 = 1.3333 **FAIL (most extreme collapse of the three)** · **B3 cross-shuffle 5.0 < 5.0 → FAIL (NO COLLAPSE)** · B4 held-out 5.0 **PASS** · B5 vs-base **PASS** · CTRL inert **PASS**.

## Verdict 🧱 WALL=CAPACITY (c9)

Form-supervision DOES internalize the negatable form into free generation (base 0.0 → trained 5.0,
held-out 5.0, control 0.0 — real and generalizing). But it produces the SAME memorized templated SHELL
every time: DIST collapses to 1.33 (the model emits essentially ONE form filled with interchangeable
tokens), and cross-shuffle does NOT collapse (swapping the measurable leaves FALS=5.0). Internalizing the
FORM produces form-without-content — the most direct demonstration that the 303M wall is semantic-binding
capacity, not a missing form or a learn-gap for the form. Confirms the capacity thesis from a 3rd
training-side angle. base ckpt NOT overwritten. trained ckpt = path-only (c5).

wired: N/A.
