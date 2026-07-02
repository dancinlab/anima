---
id: H_1431
slug: 1431_bind_compose
title: G6 IDEATION ★ FALS-depth wall — BIND-compose (external deterministic comparator×measurable bind)
group: gate-dig (G6 IDEATION ★, anima's core purpose) — FALS-depth wall, 3rd angle
terminal_tier: 🧱 BIND-CAPACITY-BOUND — ENGINE-NATIVE CONFIRMED (R3 live CORE/bytegpt_decode; was torch DIRECTIONAL, c9)
wired: engine-native (decode via live CORE/bytegpt_decode .hexa; N/A wire-in — 🧱 did not cross, a_verified_must_wire GREEN-only)
verdict_dir: state/verdicts/1431_bind_compose/
terminal_verdict: state/verdicts/1431_bind_compose/H_1431_engine_native_result.txt
date: 2026-06-19 (R3 engine-native; R1/R2 torch 2026-06-17)
---

# H_1431 — G6 IDEATION ★ FALS-depth: BIND-compose lane

## Why (the precise diagnosis this attacks — a_break_the_wall, c16)

G6 IDEATION ★ is anima's STARRED gate. The FALS-depth floor (≥1 falsifiable corpus-absent
hypothesis) has held across three prior digs:
- **H_1305** — composition-route (recombination shell) nudged FALS 0.00→0.667, sub-threshold.
- **H_1309** — curiosity multi-sample BUDGET plateaus at 0.667 → CAPACITY-bound, not budget.
- **H_1314** — hypothesis-FORM scaffold fixes DIST/NOVEL but FALS stays 0; named the EXACT
  bottleneck: *"the mouth produces a COMPARATIVE shape OR a MEASURABLE shape but cannot BIND
  them into one negatable declarative claim — the capacity-limited step."*

**New angle (NOT a re-run of 1305/1309/1314):** if each leg is in-capacity and only the BIND
fails, pull the BIND OUT of the mouth's internal generation into an EXTERNAL DETERMINISTIC
compose lane — the same move H_1414 (mem×ToM arbiter) and H_1397 (ko emit-compose) made for
other faculties. The mouth supplies a RELATION fragment (primed for a comparator) + a MEASURE
fragment (primed for a measurable); the lane deterministically WELDS the mouth's OWN comparator
+ measurable + content into one negatable claim the FROZEN H_1305 detector scores. The lane
authors ZERO detector tokens (NO-FAB).

## Method (FREEZE.txt, frozen-first, c9/p7)

- detector = H_1305 `_is_falsifiable` imported VERBATIM (not redefined); calibration 10/10.
- decode = gauge_lib._decode top-k=40 temp=0.7 max_new=110 (the live G6 path); 303M
  `h1129c_chat.pt`; corpus `data/corpus.txt`; seeds [7,4302,4303]; 5 subjects (H_1314 nouns).
- relation seed = `"a relationship about {subj}: it tends to be "` ·
  measure seed = `"something we could observe about {subj}: the "`.
- weld schema (pure function words only) = `"the {meas} of {cA} is {comp} with {cB}"` where
  `{comp},{meas},{cA},{cB}` are MOUTH-EMITTED. Bind FAILS (claim="") if the mouth supplied no
  comparator OR no measurable (NO-FAB).
- ARMS: COMPOSE (earned per-idea bind) · SHUFFLE_BIND (measurable routed from a DIFFERENT idea
  via derangement) · ABLATE (compose OFF = single flat decode = the H_1314 plateau).
- R1 = slot-strict extraction (comparator from relation frag, measurable from measure frag).
  R2 = union extraction (each leg from the union of an idea's two native fragments; bars
  UNCHANGED) — corrects the R1 observation that the mouth crosses the primed slots. **R1 and
  R2 returned byte-identical bar numbers** (the slot-crossing was not the bottleneck).
- Compute: summer pool (CUDA), per protocol (303M decode is heavy; c17/mini forbidden).

## FROZEN 5-bar (declared BEFORE the run) + result (mean 3 seeds)

| arm | DIST | FALS |
|---|---|---|
| COMPOSE | 0.3333 | **0.3333** |
| SHUFFLE_BIND | 0.0 | 0.0 |
| ABLATE | 4.6667 | 0.0 |

- **(1) FALS≥1 cross** : 0.3333 → **FAIL**
- **(2) count≥5 distinct** : 0.3333 → **FAIL**
- **(3) shuffle-bind COLLAPSE** : 0.3333 ≥ 0.0+1 → FAIL (vacuous — compose never reached ≥1)
- **(4) ablate-compose INERT** : 0.3333 ≥ 0.0+1 → FAIL (compose adds +0.333 over ablate, < +1)
- **(5) NO-FAB audit CLEAN** : **PASS** — and with teeth: the audit CAUGHT a draft weld token
  `"when"` (a frozen COMPARATOR) and **ABORTED** the first run; re-froze the weld to pure
  function words → CLEAN (p7 working as designed).

crossed_floor=FALSE · controls_survive=FALSE · GREEN=FALSE.

## Decisive bottleneck diagnostic (`bottleneck_diag.txt`)

Across 15 COMPOSE ideas (5 subjects × 3 seeds), how often the 303M mouth emitted the EXACT
frozen detector tokens needed to weld:

| leg | hit rate |
|---|---|
| emitted a frozen COMPARATOR token | **3/15 (20%)** |
| emitted a frozen MEASURABLE token | **4/15 (27%)** |
| emitted BOTH (the weld precondition) | **0/15 (0%)** |

## Verdict — 🧱 BIND-CAPACITY-BOUND (c9, honest)

The BIND-compose lane does NOT cross the FALS floor. The external deterministic weld is sound
and Ψ-disjoint, the NO-FAB audit is CLEAN, and the lane DID manufacture a NON-ZERO FALS
(0.333 > ablate 0.0 — one falsifiable claim across 15 ideas via a cross-idea union under a
specific permutation), so the literal frozen WALL flag is False (FALS_compose > FALS_ablate)
and the bars score 🟠 PARTIAL. **But the bottleneck diagnostic shows the SUBSTANCE is a capacity
wall:** the mouth emits each leg only weakly (comparator 20%, measurable 27%) and emits BOTH
exact frozen tokens for the SAME idea in **0/15** cases — the bind has nothing to weld.

Handing the BIND to an external lane does NOT rescue G6 FALS-depth, confirming the
H_1314/H_1309 capacity thesis from a **THIRD independent angle** (external-bind, after
composition-route H_1305 and form-scaffold H_1314). The 303M mouth produces comparator-SEMANTICS
("tends to be", "correlate", "between") and measurable-SEMANTICS ("number", "measure", "value")
but rarely the EXACT frozen lexical tokens, and **never both at once** — and the detector cannot
be loosened (that is tune-to-green / moving the frozen bar, forbidden, c9/p7). The earlier
diagnosis was incomplete: it is not merely that the mouth "can't bind" two in-capacity legs — at
303M the legs are only weakly in-capacity at the LEXICAL level and are mutually exclusive within
an idea, so even a perfect external binder is starved of material.

## What this grounds — H_1433 (7B falsifier)

This is the result that grounds the **H_1433 7B falsifier**: the pre-registered prediction is
that a 7B mouth emits both exact frozen tokens densely enough (each leg reliably in-capacity at
the lexical level, with co-occurrence > 0) that the SAME external BIND-compose lane welds a
falsifiable claim and crosses FALS≥1. The BIND becomes externally fixable only once each leg is
reliably lexically in-capacity — a scale prediction, falsifiable by re-running this exact lane
(detector + weld + 5-bar, all frozen) on a 7B ckpt. NO wiring (did not cross).

## Scope (honest, a_scale_honest_scope / a_toy_scale_recheck)

**R3 ENGINE-NATIVE re-measure (2026-06-19, vast 41469555 2267G-CPU, rent — a_engine_native_learning HARD-GATE SATISFIED):**
The FALS 5-bar was RE-MEASURED with decode run on the **live CORE byte-mouth** —
`state/1431_bind_compose/engine_decode_batch_cli.hexa` → `CORE/bytegpt_decode.hexa::bytegpt_decode_batch_to_file`
(full-load `bg_load`, 303M `chat_full.bin`, hexa v0.241 glibc-2.34), NOT the torch mouth. 30 fragments
(5 subj × 3 seed × 2 kind) decoded byte-LM native, scored by the SAME frozen H_1305 `_is_falsifiable` (VERBATIM).
The R2 BLOCKER (forward-parity argmax 227-vs-32) did NOT recur on the v0.241 full-load decode path — the engine
generated coherent English ("universalized with the new data…") and the lane welded+scored it.
**ENGINE-NATIVE 5-bar (30/30, missing=0, mean 3 seeds):**

| arm | FALS (engine-native) | (torch DIRECTIONAL) |
|---|---|---|
| COMPOSE | **0.0** | 0.3333 |
| SHUFFLE_BIND | 0.6667 | 0.0 |
| ABLATE | 0.0 | 0.0 |

Engine-native decode is NOT byte-exact vs the torch golden (engine COMPOSE 0.0 vs torch 0.333 — different build +
sampling realization) but the **verdict is IDENTICAL at the level that matters: FALS_compose < 1, and COMPOSE
(0.0) ≤ SHUFFLE (0.667) and == ABLATE (0.0)** — on the live CORE mouth the external bind crosses neither the
falsifiability floor nor its own controls (if anything weaker than the torch mirror: compose == ablate == 0). The
🧱 BIND-CAPACITY-BOUND verdict is therefore **CONFIRMED ENGINE-NATIVE** (no longer DIRECTIONAL). decode=ENGINE-NATIVE
(.hexa live CORE), score=frozen H_1305 detector (torch-loaded but decode-independent, p7 VERBATIM). Evidence:
`state/verdicts/1431_bind_compose/H_1431_engine_native_result.txt` ·
`state/1431_bind_compose/{engine_decode_batch_cli.hexa, h1431_score_native.py, batch_out_full30.tsv}`.

DIRECTIONAL R1 torch-mouth mirror on summer CUDA (engine-native byte-exact reconfirm = follow-on
only on a future GREEN; a_engine_native_learning); toy 303M; 5 subjects; 3 seeds; deterministic
structural detector (form not quality, p7). The lane tests an external deterministic bind, not a
learned binder. NO tune-to-green (the weld was re-frozen, not loosened, after the audit caught a
leak). Device-invariance: gauge_lib._decode samples via a CPU Generator over CPU-copied probs, so
the emitted bytes are device-independent given the seed (CUDA only accelerated the forward,
a_wall_first). 7B re-test = the live falsifier (H_1433).

## Pointers

- probe: `state/1431_bind_compose/h1431_bind_compose.py` · diagnostic:
  `state/1431_bind_compose/h1431_bottleneck_diag.py`
- verdict: `.verdicts/1431_bind_compose/{FREEZE.txt, result.txt, result.json, bottleneck_diag.txt,
  result_R1.{json,txt}, result_R2.{json,txt}}`
- reuses: `state/universe-probes/h1305_g6_ideation_falsifiability.py` (frozen detector, VERBATIM),
  `tool/gauge_lib.py` (decode/evaluators), `state/universe-probes/h1129_*` (ByteGPT arch).
- xref: H_1305 (composition-route, frozen detector source) · H_1309 (curiosity-budget, capacity
  thesis) · H_1314 (form-scaffold, the BIND diagnosis this attacks) · H_1397 (ko emit-compose
  pattern) · H_1414 (mem×ToM external arbiter pattern) · H_1433 (7B falsifier this grounds) ·
  a_break_the_wall · a_no_llm_frame_trap · a_substrate_native_speak · a_engine_native_learning ·
  a_verified_must_wire · a_toy_scale_recheck · a_scale_honest_scope · a7b_pass ·
  p1·p2·p3·p4·p6·p7·p8 · c9 · c16.
