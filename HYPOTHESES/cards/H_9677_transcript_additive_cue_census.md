---
id: H_9677
title: E0 — study transcript additive-cue census (is H_9520 a corollary of H_9304?)
tier: PROPOSED (DIRECTIONAL design · lab-full divergence · $0 · NOT a verdict)
frontier: g1-interface-addressable-wall
created: 2026-07-17
---

# H_9677 (R1) — transcript 가법단서 census

**Origin.** `sidecar lab full` divergence 2026-07-17 (Fable 5 P1). **DESIGN ONLY** —
divergence output is DIRECTIONAL by construction; only engine-native `anima-py` decides.

**Claim (one line).** The `anima study` transcript carries ~0 nats of additive cues
⟹ **H_9520's content-null was a PREDICTION of H_9304, not an independent observation.**

## Why this is the gate of the whole R-series
H_9304 froze: natural/communicative language carries **+0.0023 nats** additive
information = **TOST 0-equivalent** vs XBIND **+5.30** (2280×). H_9316/9318 extended it
to the whole XOR-class (negation·adversative·parity·irony) = **CLASS-CLOSED**.
The study transcript **is** natural communicative language. If the census confirms ~0
nats, then the claimed "two independent lanes converge on FORM-in/CONTENT-out" collapses
into **one lane seen twice**, and the unified law is the one already on the books:

> the substrate absorbs only what the corpus **prepays** as position-local dense signal —
> FORM is always prepaid (every byte position is signal), BIND must be prepaid explicitly
> (XBIND · co-training).

## Minimal decisive experiment (engine-native · a_experiment_engine_native)
```bash
anima-py corpus census --additive-cues --transcript T.jsonl --vs <xbind_ref>
```
New `census` flag reusing the H_9304 `--interact-mi` instrument. NOT a probe beside the engine.

## Frozen falsifier (pre-registered)
- transcript nats **≥ 5% of the XBIND reference** ⟹ "cues present" — H_9520 REOPEN justified.
- transcript nats **< 5%** ⟹ "it was a prediction" — **H_9520 REOPEN is worthless**; retire it.

## Controls (≥2)
① XBIND corpus (positive reference · ceiling) ② C2 scrambled transcript (negative floor)
③ base replay corpus (natural baseline).

## Cost · kill-list
**$0** (text-only measurement · mini OK). Kill-list: **no hit** — this *applies* the
kill-list rather than re-proposing a dead angle.

---

# VERDICT (2026-07-17) — ⛔ INVALID: instrument↔claim MISALIGNMENT · the frozen bar is UNREADABLE

**DIRECTIONAL · engine-native `anima-py evaluate --earned` · $0 · local mac**

> **The bar was NOT applied. H_9520's REOPEN is NOT retired.**
> An INVALID is not a KILL — that is this instrument's own doctrine ("a small n is not a
> negative result"), and it is the whole reason G-POWER exists.

## ⚠️ 0. The card named the wrong instrument

The design says the census reuses "the H_9304 `--interact-mi` instrument". **It does not exist.**
`--interact-mi` is the **H_9328 DO-MOUTH mediation reader** (I(A;Y|S) over chat rollout traces —
H_9328/9337/9345). H_9304's instrument is **`--earned`** (`cli/earned.py`, wired engine-native by
**H_9319**). All work below uses `--earned`. *(Divergence output is DIRECTIONAL by construction;
this is exactly the class of slip that survives a design pass and dies on contact with the tree.)*

**Semantic slip too**: the card says the transcript carries "~0 nats of **additive** cues".
`--earned` measures **transferable NON-additive** information. H_9304's finding is that natural
language **IS additive** (≈0 *non*-additive nats). "0 nats of additive cues" is backwards; the
intended quantity is "≈0 nats of the thing H_9304 measures".

## 1. The blocker is prior to power: **the transcript has no valid T**

`--earned` requires `(text, B, T)` where **T is an outcome annotated OUTSIDE the token stream** —
its docstring is explicit: *"pure web/wiki cannot even pose the question."*

The transcript's keys are `{tick, percept, did_emit, emit_text}`. `emit_text` is a token stream
(and is the substrate's own output). The **only** non-token channel is `did_emit` — and:

| | |
|---|---|
| `did_emit == (tick%4==0 and tick>0)` | **60/60 rows** |
| H(did_emit) | 0.543273 nats |
| H(did_emit \| tick%4) | **0.061233 nats** (residual = the single tick-0 boundary row) |

⇒ **T is a period-4 clock.** This is a live re-confirmation of **H_9345** (`H(emit|stage)=0`,
emit = pure function of the schedule) **on independent data**. Any EARNED computed on this T
measures *stems against a clock*, not "does the transcript carry cues". **No code change can fix
this** — the corpus is unlabelled.

## 2. Controls (the card asked for 3 · only 1 is real)

| control | status |
|---|---|
| ① XBIND positive reference | ✅ **ALIVE** — G-ALIVE `EARNED=+5.03675` δ̂=−3.00 (bar ≥+0.30) · G-PEDESTAL `+0.00124` (\|·\|≤0.02). **The instrument is certified; this is not dead-probe silence.** |
| ② C2 scrambled transcript | ⛔ **VACUOUS — cannot serve as a negative floor** (see below) |
| ③ base replay (`cpt_mix.txt.c1_replayonly.txt`) | ⛔ **UNAVAILABLE** — raw unlabelled text; no B, no T. Cannot be loaded as `(text,B,T)` at all. |
| ＋ T-random (added — the control that actually works) | ✅ destroys the outcome channel |

### ⛔ Why C2-scrambled is vacuous here (verified, not argued)

`build_cells` consumes **`set(_stems(text))`** — `--earned` is a **bag-of-words** estimator.
Word-order scrambling is a **no-op in cell space**. Verified directly:

```
per-row stem SETS identical      : True   (all 30 rows)
cells identical as MULTISET      : True   (567 × 3)
cells identical in ORDER         : False  ← only Python set-iteration order differs
```

⇒ **C2 *is* the real arm** to this instrument. Reading "C2 ≈ REAL ⟹ the text carries nothing"
would be reading an **artifact of order-invariance**. C2-scramble is a valid control for a
**byte-LM** (H_9520's CPT, where order matters) and is **structurally invalid for any
bag-of-words instrument**. Inheriting a control across a lens change is the defect
(`control-must-match-mediating-covariate`).

## 3. What the engine actually printed (charity arm)

The **CHARITY arm** — the most favourable construction available: B = English negation flag
(H_9304's closed-set analogue), T = `did_emit`. **Its number is not a measurement of the claim**
(T is the clock, §1); it exists to show the instrument dies even when handed the best available shape.

| arm | held-out EARNED | % of XBIND ruler | engine VERDICT |
|---|---|---|---|
| transcript (charity) | +0.03431 · 95% CI [−0.02768, +0.09557] | **0.648%** | INDETERMINATE |
| C2 scrambled *(vacuous)* | +0.03167 | 0.598% | INDETERMINATE |
| **T-random** *(valid neg. control)* | **−0.00125** | **−0.024%** | INDETERMINATE |

```
G-POWER  held-out cells=104 (stems 23)  sd_null=0.02945  MDE(3σ)=0.08834  need<=0.02
         FAIL — NOT POWERED for a negative verdict
SEEDS    9304:+0.00071 (0.013%) · 9305:+0.04438 (0.838%) · 9306:+0.05785 (1.092%)
         spread = 0.05713 nats (1.079% of the ruler) — a single-seed number here would be NOISE
```

- **G-POWER FAIL** (MDE 0.088 ≫ δ_eq 0.02) · **SEED-UNSTABLE** (spread 0.057 > effect 0.034).
- The charity arm's CI **contains the T-random arm** ⇒ indistinguishable from a destroyed outcome.

## 4. 🪤 The trap this run walked up to and did not step in

**0.648% < 5% ⟹ mechanically the bar says "it was a prediction — retire the REOPEN."**
That reading is **refused**, on three independent grounds:

1. **T is invalid** (§1) — validity of the outcome channel is *prior to* power. The number is
   stems-vs-clock; it is not about the transcript's content at all.
2. **The real arm is indistinguishable from the T-random arm** — a "0.6% of ruler" reading is what
   this estimator returns when the outcome carries nothing.
3. **G-POWER failed** — the instrument's own doctrine: *"failing G-POWER is INVALID/DATA-SPARSE —
   never a KILL."*

⚠️ **Honest note on power, stated against interest**: the R1 bar (5% of ruler = **0.265 nats**) is
*coarser* than δ_eq, and MDE(3σ)=0.088 < 0.265 — so **for that bar alone the arm is nominally
powered**. This does **not** rescue the reading: power is necessary, not sufficient, and it cannot
repair an invalid T. The pre-registered table has no cell for **INVALID**
(`prereg-table-must-cover-below-chance` — the table must cover the cells you did not expect).

**⇒ R1 is the very defect its own lane discovered.** The parent frontier
(`instrument-claim-alignment-before-reading-a-bar`, H_9520) says: *procedural rigour conceals this
flaw — a mechanically-applied pre-registered bar does not notice that the instrument is not
measuring the claim.* R1 proposed to test H_9520 and fell to H_9520's own lesson.

## 5. Engine-native repairs earned (`cli/earned.py` · VERSION 0.15.54→**0.15.55** · G5)

1. **Crash → verdict.** A corpus the extractor cannot read produced `IndexError: too many indices`
   (`np.asarray([])` is 1-D, so `make_heldout` died *before* the DATA-SPARSE guard could fire —
   the guard sat one line too late and was **unreachable**). A crash is not a verdict: "the
   instrument threw" reads as an infra hiccup rather than *the corpus cannot pose the question*.
   Now emits **`INVALID (DATA-SPARSE) — NOT a KILL`** with the reason.
2. **`latin` script + majority-vote `_detect_script`.** English fell through to the hangul regex
   and silently read **0 stems**. Adding a script is a regex swap and certification is inherited
   (H_9318 added Arabic this way; G-ALIVE/G-PEDESTAL are synthetic integer arms and never touch
   `_stems`). **Routing regression-checked through the CLI: ko→`hangul`, ar→`arabic` unchanged**
   ⇒ the shipped H_9304/9316/9317/9318 numbers are untouched.

   *Without this, "INSTRUMENT-DEAD" would have been an artifact of a missing regex — a code gap
   masquerading as a wall. It was measured, not assumed.*

## 6. Status

**⛔ INVALID (instrument↔claim misalignment) · bar UNREADABLE · H_9520 REOPEN NOT retired.**
R1 cannot decide whether H_9520's content-null is a corollary of H_9304 — **not because the answer
is no, but because this transcript cannot pose the question.** To pose it, an arm needs an outcome
**annotated outside the token stream** and independent of the clock; the study transcript has none,
and neither do c1/c2. Reopening R1 requires a **labelled** corpus, not a re-run.
