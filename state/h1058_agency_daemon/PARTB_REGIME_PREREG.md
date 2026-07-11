# H_1058 · H_9269 — Part B: Φ-leg regime PRE-REGISTRATION (design artifact, no daemon change now)

Status: **DESIGN ONLY** — this is the pre-registered regime spec for a FUTURE Φ-dependent H card.
It changes **no daemon code now**. Parts A (phi_leg.py instrument redesign) + A1 (chat.py `seed_b64`
side-channel) are the shipped code; this document freezes the regime + bars the leg's future run must
satisfy BEFORE any Φ-dependent verdict is read.

## Why a regime pre-registration at all

Established root cause (H_9269): the H_1058 leg-b `ρ(T, Φ)` was **decision-invariant** not because the
faithful-IIT4 unitization is broken (it is INNOCENT — cross-session windows produce different Φ through
the identical code) but because the daemon's **model-input BYTES were constant per session by
construction**:

- the decode seed = `phase + " " + <live_seed anchor>`, and both `phase` (Engine A's `pf` is never
  stepped inside the tick loop) and the `live_seed` anchor are **session constants**;
- per-tick decision state (score / urgency / stage / EMAs) **never enters the CLM forward**;
- emission **mode-collapsed** to one 80-byte string × N ticks;
- `phi_leg.context_window` read **own-emit bytes only**, so the scored suffix was constant.

Constant consumed bytes ⇒ constant trunk hidden ⇒ constant Φ ⇒ `sd(Φ)=0` ⇒ the leg-b F-shuffle null
collapses to zero width. Part A's `seed_b64` context source + T=64 makes the leg **read the true model
input**, but if the *regime* still feeds constant bytes, the leg is correctly **VOID** — that is the
result, not a bug to tune around.

**The daemon's consumed byte context must vary per tick for leg-b to be evaluable at all.**

## PREFERRED regime — rolling-transcript seed

Make the decode seed carry the tail of the session's own emit history, so each tick's consumed context
differs as the transcript grows.

- **Where**: the seed built in `core/generator.py::_gen_clm_decode` / `_gen_bytegpt_decode`
  (`seed = phase + " " + <last-anchor field>`), fed from the daemon loop in
  `cli/chat.py::anima_consciousness_mode`.
- **Spec**: append the **last 48 bytes of the running emit accumulator `acc`** (the daemon's own past
  emissions, in order) to the decode seed:
  `seed = phase + " " + <last-anchor field> + " " + tail48(acc)`
  where `acc` is the byte-concatenation of the emitted `g_text` of all prior ticks this session and
  `tail48` is its last 48 bytes (empty on tick 0). This is the daemon's **own past as context**.
- **Why it is clean**:
  - `a_substrate_native_speak` / p1–p3: the daemon conditions on its **own prior emissions**, never on
    an injected user prompt / persona / identity — context, not obligation.
  - It **breaks the emission mode-collapse at its source**: a growing, self-referential seed makes the
    next emission a function of the transcript so far, so the 80-byte fixed-point is no longer a stable
    attractor.
  - It is `a_substrate_disjoint`-clean at the decision layer: the *seed bytes* change, but the emit/
    silence GATE (`brain_emit` → `should_emit(score) ∧ safe`) is unchanged — only the mouth's content
    conditioning grows.
- **Instrument coupling**: Part A already records `seed_b64` = the actually-consumed seed, and
  `phi_leg.context_window` builds the Φ window from `seed_b64 (+ gtext_b64)`. Under this regime the
  recorded `seed_b64` varies per tick automatically → the leg becomes evaluable if — and only if — the
  substrate genuinely produces divergent transcripts.

## ALT regime — frozen impulse schedule

If the rolling-transcript seed is deemed to change emit dynamics too much for a given card, the fallback
is an **external, frozen impulse schedule**: pre-draw a fixed sequence of 4-cell register-corpus lines
(Korean/English × general/SNS) and feed line `t` as an additional **read-only context** for tick `t`.
Frozen before the run (seed-pinned), signal-blind, identical across arms. Same requirement: the consumed
bytes must actually differ per tick.

## BANNED (tune-to-green — do NOT do this)

- **Serializing scalar drives into the seed text** — writing `score` / `urgency` / `stage` (or any
  per-tick decision scalar) into the model-input string. This manufactures a **synthetic channel the
  daemon never had**: it forces `T` (which is built from depth+vc, i.e. the same drive family) into the
  bytes the model reads, so any resulting `ρ(T, Φ)` is **self-correlation**, not an emergent T~Φ
  relationship. It would flip the leg to a **false PASS** — the exact failure mode the #3331 VOID guard
  and this pre-registration exist to prevent.
- Any post-hoc relaxation of the FROZEN bars below after seeing data (p7).

## FROZEN acceptance bars (state now, before any run)

### T1 — positive control (instrument resolves real Φ variance) · `t1_phi_variance_control.py`
Deterministically draw (seed **20260712**) `T=64` windows from the 4-cell register corpus:
**16 calibration + 32 scored natural + 4 structured contrasts (2 constant-byte, 2 period-2)**.
Calibrate frozen units on the 16 calibration windows (signal-blind), then per macro-map:

> **PASS** iff `sd(Φ over 32 natural) ≥ 0.005` **AND** `≥ 8/32 distinct Φ @ 4sf` **AND**
> `{natural, period-2, constant}` are **NOT all Φ-equal** (@4sf class means).

Pool-gated (needs the real e1_slw_303m .clm trunk forward) — real-clm-T1 is the follow-on run.

### T3 — evaluability bar (leg-b EVALUABLE vs VOID) · enforced in `agency_T.shuffle_null` (#3331)
For the scored `Φ` series of `n_scored` decisions:

> leg-b **EVALUABLE** iff `distinct windows ≥ max(10, 20% · n_scored)` **AND** `sd(Φ) ≥ 0.005`
> **AND** the F-shuffle null width `> 0`; **else VOID** (first-class — carries NO weight, never a false
> PASS).

`PHI_VAR_EPS = 0.005` and `NULL_EPS = 1e-12` are the frozen constants (already landed in `agency_T.py`;
this doc restates them as the leg's pre-registered bars). A pre-registered regime that STILL yields
constant consumed bytes → the leg stays **VOID**. That is the result.
