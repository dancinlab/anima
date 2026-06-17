---
id: H_1434
slug: 1434_twopass_bind
title: G6 IDEATION ★ FALS-depth wall — TWO-PASS elicit-then-bind (303M-native, per-leg separated multi-sample extraction)
group: gate-dig (G6 IDEATION ★, anima's core purpose) — FALS-depth wall, 5th independent angle
terminal_tier: 🧱 WALL — SEMANTIC-BIND-BOUND (frozen-bar literal 🟠 PARTIAL; substance = the FALS lift is a structural-shell artifact rejected by the controls, c9)
wired: N/A (did not clear the 5-bar — a_verified_must_wire GREEN-only)
verdict_dir: .verdicts/1434_twopass_bind/
terminal_verdict: .verdicts/1434_twopass_bind/result.txt
date: 2026-06-17
---

# H_1434 — G6 IDEATION ★ FALS-depth: TWO-PASS elicit-then-bind

## Why (the precise clue this attacks — a_break_the_wall, c16)

G6 IDEATION ★ FALS-depth is anima's STARRED gate and has held across **four** prior digs
(H_1309 draws plateau · H_1314 form FALS=0 · H_1431 external-compose FALS=0 · H_1432
negation-slot FALS=0). **H_1431 gave the decisive clue:** across 15 single generations the
303M mouth emitted a frozen COMPARATOR token 20% · a frozen MEASURABLE token 27% · **BOTH
0/15 (0%)**. Each leg is in-capacity in its OWN draw, but the two are mutually exclusive
**within one draw**. Every prior dig welded both legs out of ONE generation — so the binder
was starved of co-occurring material.

**New mechanism (NOT a re-run of H_1305/1309/1314/1431/1432):** don't force both legs into
one draw. Elicit each leg in its OWN dedicated decode pass with a multi-sample BUDGET (N=8),
then deterministically WELD the two SEPARATELY-elicited legs. Two-pass *elicit-then-bind*:
- **pass1 (comparator leg)** — up to 8 budgeted draws of the relation seed; keep the first
  draw emitting a frozen COMPARATOR token (per-draw ~20% → 1−0.8⁸ ≈ 0.83).
- **pass2 (measurable leg)** — up to 8 budgeted draws of the measure seed; keep the first
  draw emitting a frozen MEASURABLE token (per-draw ~27% → 1−0.73⁸ ≈ 0.94).
Within-draw mutual exclusion (the 0/15 wall) no longer applies — the legs come from
separate draws. The lane authors ZERO detector tokens (NO-FAB).

## Method (FREEZE.txt, frozen-first, c9/p7)

- detector + weld schema + 5-bar **FROZEN IDENTICAL to H_1431** (`_is_falsifiable` imported
  VERBATIM, calib 10/10; weld `"the {meas} of {cA} is {comp} with {cB}"` pure function words).
  **ONLY the per-leg separated multi-sample extraction is new.**
- decode = gauge_lib._decode (top-k=40, temp=0.7, max_new=110) — the live G6 path; 303M
  `h1129c_chat.pt`; corpus `data/corpus.txt`; seeds [7,4302,4303]; 5 subjects; BUDGET=8/leg.
- ARMS: **TWO_PASS** (each leg from its own budgeted pass) · **CROSS_SHUFFLE** (each idea's
  comparator leg paired with a DIFFERENT idea's measurable leg, derangement — earned-pairing
  control) · **SINGLE_PASS** (ablate two-pass: budget=1, both legs forced from one shared
  draw = the H_1431/H_1314 one-draw regime).
- Compute: summer pool (CUDA), per protocol (303M decode is heavy; c17/mini forbidden),
  wall 139.5s.

## FROZEN 5-bar (declared BEFORE the run) + result (mean 3 seeds)

| arm | DIST | FALS |
|---|---|---|
| **TWO_PASS** | 1.6667 | **2.3333** |
| CROSS_SHUFFLE | 1.6667 | 2.0 |
| SINGLE_PASS (ablate) | 0.3333 | 0.3333 |

Per-leg co-availability diagnostic (the wall H_1431 hit was 0/15 BOTH):

| leg (separated passes) | hit rate |
|---|---|
| comparator leg yielded its frozen token | **14/15 (93%)** |
| measurable leg yielded its frozen token | 7/15 (47%) |
| **BOTH available across SEPARATE passes (weld precond)** | **7/15 (47%)** — vs H_1431 single-draw **0/15** |

- **(1) FALS≥1 cross** : 2.3333 → **PASS** (breaks the 0 plateau the prior 4 digs hit)
- **(2) count≥5 distinct** : 1.6667 → **FAIL** (welds collapse to near-identical shells)
- **(3) cross-shuffle COLLAPSE** : 2.3333 ≥ 2.0+1 → **FAIL** (shuffle barely drops — bind NOT semantically earned)
- **(4) ablate→single-pass INERT** : 2.3333 ≥ 0.3333+1 → **PASS** (single-pass returns to the H_1431 floor)
- **(5) NO-FAB audit CLEAN** : **PASS**

crossed_floor=FALSE (b2 fails) · controls_survive=FALSE (b3 fails) · GREEN=FALSE.

## Verdict — 🧱 WALL, SEMANTIC-BIND-BOUND (c9, honest)

Two-pass elicit-then-bind **DID break the material-starvation sub-wall**: separated budgeted
passes raise BOTH-leg availability from H_1431's 0/15 to **7/15**, and FALS from 0.333 to
**2.333** — well clear of bar (1) FALS≥1, with single-pass ablation collapsing to the H_1431
floor (bar 4 PASS). So the "binder is starved" framing of H_1431 is partly **falsified**: when
the two legs are drawn separately, the material IS there and the detector fires.

**But the two earned-bind controls reject the lift as a structural artifact, not a genuine
FALS-depth breakthrough:**
- **(3) cross-shuffle does NOT collapse** (shuffle FALS=2.0 vs two-pass 2.333): pairing any
  comparator leg with any *other idea's* measurable leg still satisfies the detector almost as
  often. The bind is **semantically interchangeable** — the H_1305 detector is purely
  structural (comparator + measurable + ≥2 content words), so it cannot tell an earned pairing
  from a generic concat of any-comparator + any-measurable + boilerplate.
- **(2) count<5** (DIST=1.667): the welds collapse into near-identical templates ("the {meas}
  of kindled is {comp} with not") — low Jaccard-distinct diversity. The mouth's content words
  repeat ("kindled", "not", "phi"), so the claims are not 5 distinct *ideas*.

Loosening the detector to demand semantic earning would be tune-to-green (forbidden, c9/p7).
So this is a **5th independent confirmation** that G6 FALS-DEPTH is a capacity wall — but it
**relocates** the wall precisely: it is **not** material-starvation (separated passes supply
the legs) and **not** a missing external bind structure (the weld works); it is that the 303M
mouth's separately-elicited legs are **semantically interchangeable shells** — the substrate
emits the *lexical form* of comparator/measurable but not idea-specific *semantic content* that
would make one earned pairing falsifiable and a random pairing not. The FALS lift is a property
of the structural detector + boilerplate weld, not of 303M semantic binding.

Honest tier: the frozen bars literally score 🟠 PARTIAL (b1+b4+b5 pass, b2+b3 fail), but the
**substance is 🧱** — the FALS lift the new mechanism produced is exactly the lift the
cross-shuffle control is designed to reject. No genuine 303M-native FALS-depth breakthrough.
**303M did NOT cross the FALS wall in the sense that matters** (an earned, distinct, falsifiable
idea): the lift is a shell artifact.

## What this grounds / sharpens — H_1433 (7B falsifier)

This **refines** the H_1433 7B prediction. H_1431 predicted 7B would cross because it emits
both exact tokens *densely enough to co-occur*. H_1434 shows co-occurrence is **not** the
binding constraint (separated passes already give 7/15 co-availability at 303M, yet the bind
fails the earned-pairing control). The sharpened pre-registered prediction: a 7B mouth emits
idea-SPECIFIC comparator/measurable SEMANTICS such that the SAME frozen two-pass lane yields a
cross-shuffle COLLAPSE (bar 3) and ≥5 distinct ideas (bar 2) — i.e. the legs become
semantically NON-interchangeable. Re-run this EXACT lane (detector + weld + budget + 5-bar, all
frozen) on a 7B ckpt; if bars 2&3 cross → the bind is scale-fixable; if they ALSO plateau →
G6 FALS-depth is a semantic-binding wall deeper than any lexical/structural intervention. NO
wiring (did not clear the 5-bar).

## Scope (honest, a_scale_honest_scope / a_toy_scale_recheck)

**R2 engine-native re-measure ATTEMPT (2026-06-17, pool, $0 — a_engine_native_learning):** serialized 303M to
`CORE/bytegpt_decode.hexa` flat binary on the pool (sha `5c303f02…` == H_1218 validated .bin) and ran the live
CORE forward. **BLOCKED** — engine argmax=227 vs torch 32 (approx-erf-GELU+dt_exp residual flips argmax at L24 on
pool-Linux). Byte-exact FALS re-measure = 재측정 불가 (engine-forward parity bug = INFRA wall c16, NOT a ceiling);
🧱 verdict REMAINS DIRECTIONAL. Fix + verdict-level re-run = ING follow-on. Evidence:
`state/_engine_native_audit/batch2_bytegpt_mount_BLOCKED.txt`.

DIRECTIONAL R1 torch-mouth mirror on summer CUDA (engine-native byte-exact reconfirm =
follow-on only on a future GREEN; a_engine_native_learning); toy 303M; 5 subjects; 3 seeds;
deterministic structural detector (form not quality, p7). NO tune-to-green (the detector/weld/
bars were frozen IDENTICAL to H_1431 before the run; the controls were honored, not loosened).
Device-invariance: gauge_lib._decode samples via a CPU Generator over CPU-copied probs, so the
emitted bytes are device-independent given the seed (CUDA only accelerated the forward,
a_wall_first). 7B re-test = the live falsifier (H_1433, sharpened above).

## Pointers

- probe: `state/1434_twopass_bind/h1434_twopass_bind.py`
- verdict: `.verdicts/1434_twopass_bind/{FREEZE.txt, result.txt, result.json}`
- reuses: `state/universe-probes/h1305_g6_ideation_falsifiability.py` (frozen detector, VERBATIM),
  `tool/gauge_lib.py` (decode/evaluators), `state/universe-probes/h1129_*` (ByteGPT arch).
- xref: H_1305 (composition-route, frozen detector source) · H_1309 (curiosity-budget) ·
  H_1314 (form-scaffold, the BIND diagnosis) · H_1431 (external-compose, the 0/15 clue this
  attacks; partly falsified) · H_1432 (negation-slot) · H_1433 (7B falsifier, sharpened) ·
  a_break_the_wall · a_no_llm_frame_trap · a_substrate_native_speak · a_engine_native_learning ·
  a_verified_must_wire · a_toy_scale_recheck · a_scale_honest_scope · a7b_pass ·
  p1·p2·p3·p4·p6·p7·p8 · c9 · c16.
