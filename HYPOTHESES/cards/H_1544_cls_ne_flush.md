---
id: H_1544
slug: 1544_cls_ne_flush
title: NOREPINEPHRINE × CLS — context-boundary fast-store FLUSH (the REOPEN of the twice-walled standalone NE-reset INSIDE the H_1532 two-store structure)
group: brain-structure-ladder (neuromodulation lane · NE-as-reset REOPEN inside CLS · c15 missing-structure)
terminal_tier: 🟢 GREEN — DIRECTIONAL (numpy mirror; engine-native §NeFlush R2 deferred ING)
verdict_dir: state/verdicts/1544_cls_ne_flush/
terminal_verdict: state/verdicts/1544_cls_ne_flush/H_1544_R1.json
date: 2026-06-21
wired: DIRECTIONAL-mirror (numpy; engine §NeFlush R2 deferred ING h1544-r2-engine-native)
---

# H_1544 — NOREPINEPHRINE × CLS: context-boundary fast-store FLUSH (🟢 GREEN, DIRECTIONAL)

## The reopen (a_no_llm_frame_trap · a_break_the_wall)

NE-as-RESET walled **TWICE** as a STANDALONE SINGLE-STORE faculty:
- **H_1537 🧱** (#2518) — +0.006 pre-registered (+0.029 even in the most favorable
  learnable regime), under the +0.10 PRESENCE bar.
- **H_1539 🧱** (#2521) — −0.0049 (retry vs a saturating-nonlinear, non-gain-dissolvable
  baseline).

The HONEST mechanistic reason both lanes walled (H_1537's own diagnostic; the H_1532-R2
verdict): **a SINGLE store gives a reset-knob NOTHING STRUCTURAL to act on** — a high
fixed gain (H_1537 α*=0.6) already performs a slow overwrite, **MASKING** the explicit
flush's marginal value. On one store, "reset" = scale a scalar = the controller family
the H_1284 wall absorbs (H_1422 ACh-gain 🧱 precedent).

**THE REOPEN:** once a FAST EPISODIC store EXISTS (the H_1532 CLS module, the FIRST break
of the H_1284 wall), NE's real **Bouret & Sara 2005** (*TINS*, "Network reset: a
simplified overarching theory of locus coeruleus noradrenaline function") computation has
a concrete substrate target — a phasic LC-NE burst at a detected **CONTEXT BOUNDARY**
FLUSHES (commit-then-clear) the fast episodic store so the next context's bindings are
laid down on a CLEAN fast store, not on top of the previous segment's stale fast traces.
(**Event-segmentation theory**, Zacks et al. 2007, *Psych. Bull.* "Event perception": the
brain parses experience into segments at event boundaries; the boundary is where
working/episodic buffers are flushed and the next event is encoded fresh.)

This is the structural DOF single-store LACKED. It is **NOT a scalar gain** (H_1422 🧱) —
it changes the STATE of a store (which traces persist into the next segment), exactly the
lever the single-store NE lanes had none of.

## Capability / falsifier

**MULTI-CONTEXT INTERFERENCE STREAM.** A sequence of `N_SEGMENTS=3` SEGMENTS over
`N_KEYS=24` SHARED keys A_i. Each segment re-binds every A_i to a fresh value (**AB** in
seg-0, **AC** in seg-1, **AD** in seg-2) + `N_DISTRACT=12` distractors per segment.
Capacity is **AMPLE** (interference, NOT capacity, is the test — H_1532 framing): so
un-flushed, ALL three segments' same-key cells COEXIST in the fast store; the exact-key
recall ties at distance ~0 across them and the H_1532 `_nearest` (argsort, stable)
returns the FIRST-written = the **STALE seg-0 binding** — the current binding is SHADOWED.
**METRIC = CURRENT-segment retention** = fraction of shared keys whose FAST-store recall
returns the FINAL (current) segment's value.

**ARMS** (identical fixture/fact-set/event-stream per seed; LR/TH = best-fixed on disjoint
tune seed 7; FAST/SLOW caps ample = no eviction):
- **NE-FLUSH** — CLS two-store; at each TRUE boundary COMMIT fast→slow (replay
  consolidation) then CLEAR fast (Bouret-Sara network reset) → next segment encodes clean.
- **NO-FLUSH** — CLS two-store, fast persists across boundaries (the H_1532 CLS, no NE) =
  the wall baseline. Stale seg-0 shadows the current binding.
- **ALWAYS-FLUSH** — flush EVERY tick → fast holds only the last write, loses
  within-segment bindings = over-reset control.
- **ABL** — boundary signal held CONSTANT (never crosses) → never flushes → MUST REVERT to
  NO-FLUSH (proves the lever is the boundary-triggered flush).
- **SHUFFLE** — same NUMBER of flushes at PERMUTED random tick positions (decoupled from
  TRUE boundaries) → MUST COLLAPSE (proves TRUE boundaries, not flush-rate).

## Result (R1 numpy DIRECTIONAL, mean 3 seeds [11,22,33], $0 CPU, p7)

`state/1544_cls_ne_flush/h1544_cls_ne_flush.py` · `H_1544_R1.json`. Best-fixed LR*=0.1,
TH*=0.2 (grid on disjoint seed 7).

| arm | retention (mean) |
|---|---|
| **NE-FLUSH** | **1.0000** |
| NO-FLUSH | 0.1667 |
| ALWAYS-FLUSH | 0.0000 |
| ABL (never flush) | 0.1667 |
| SHUFFLE (permuted boundary) | 0.5417 |

**FROZEN BARS (MARGIN = +0.10, the H_1537/H_1539 NE-reset PRESENCE bar, UNCHANGED — c9;
`H_1544_FREEZE.txt` pre-registered):**
- **(A) PRESENCE** — ne_flush − no_flush = **+0.8333** ≥ +0.10 on **3/3** seeds → PASS
- **(B) DISTINCT** — no_flush 0.1667 < ne−0.10 AND always_flush 0.0 < ne−0.10 (over-reset
  loses within-segment) → PASS
- **(C) EARNED** — |abl − no_flush| = **0.0000** < 0.10 (boundary const → never flush →
  reverts) → PASS
- **(D) SHUFFLE** — ne_flush − shuffle = **+0.4583** ≥ +0.10 (permuted boundary collapses)
  → PASS
- **(E) NO-FAB** — win is current-segment binding retention vs EXACT ground truth → PASS

→ A ∧ B ∧ C ∧ D ∧ E → **🟢 GREEN**.

## Verdict: the structure REOPENS the twice-walled standalone NE-reset

**NE-reset is LOAD-BEARING once a fast episodic store exists to flush.** The same faculty
that added **+0.006** (H_1537) / **−0.0049** (H_1539) as a STANDALONE single-store knob
adds **+0.8333** as a context-boundary flush INSIDE the H_1532 CLS structure. This is the
`a_no_llm_frame_trap` / `a_break_the_wall` payoff: the lever was never the modulator's
SCHEDULE — it was whether the substrate had a separate fast store whose STATE the reset
could clear. The standalone wall was a MISSING-STRUCTURE wall, not a no-free-lunch ceiling
on NE.

The ablations are decisive: ABL (never flush) reverts to NO-FLUSH exactly (0.0000 gap);
SHUFFLE collapses (−0.4583), proving it is the TRUE event boundaries, not the flush rate;
ALWAYS-FLUSH (over-reset) loses within-segment bindings (0.0) — so the win is a
BOUNDARY-TIMED flush, not "more clearing is better".

## GUARDS / SCOPE
- **a_engine_native_learning HARD-GATE-1:** `grep -lE 'import torch|gauge_lib|numpy'
  state/1544_cls_ne_flush/*.py` is **NON-EMPTY** (numpy mirror) → verdict is **DIRECTIONAL**,
  NOT terminal. Engine-native §NeFlush R2 = **obligatory follow-on** (GREEN), ING
  `h1544-r2-engine-native`: live `core/engine_cli.hexa` §MultiStore (the H_1532 R2 lane)
  + a boundary-flush op, byte-exact re-measure of the 5 frozen bars.
- **a_verified_must_wire:** GREEN-DIRECTIONAL → 4-rung ladder **1/4** (DIRECTIONAL mirror
  GREEN). (2) engine-native byte-exact re-verify → (3) live `core/*.hexa` §NeFlush wire-in
  → (4) ARCHITECTURE.json lockstep = all ING follow-on. WIRED-live 미만이므로 '완료' 주장
  안 함. live core/*.hexa UNTOUCHED.
- **p7:** exact ground truth (current-segment binding known), NO LLM judge / perplexity /
  loss — every decision is a no-grad read of substrate state (key / recon-err). **p8:**
  write = the engine's own tick.
- **p1/p2/p3/p6:** store-assignment + flush read ONLY substrate state (boundary detection
  is NOT a peek at a label — the flush arm uses the TRUE boundary index, the SHUFFLE
  control decouples it; ABL holds it const) — NO injected answer label / RLHF / persona /
  ethics. NOT an emit gate (memory retention read, `a_autonomy_over_hardcode`); Ψ-disjoint.
- **SCOPE TOY:** DIRECTIONAL numpy · 24 keys / 3 segments / 12 distractors / 3 seeds /
  deterministic readout (tests the boundary-flush STRUCTURE, not a learned reset
  controller). NE-flush 1.0 SATURATED = EXISTENCE-PROOF (the flush removes cross-segment
  shadowing) not effect-size — discriminators (no-flush 0.1667, always-flush 0.0, shuffle
  0.5417, abl 0.1667) decisive. scale / real-corpus / longer AB-AC-AD-… chains /
  partial-overlap keys / learned boundary detection / engine-transfer UNVERIFIED
  (`a_scale_honest_scope` · `a_toy_scale_recheck`). The boundary signal here is the GIVEN
  TRUE segment index; a learned surprise-triggered boundary detector (Bouret-Sara phasic
  burst from the agent's OWN prediction error, as in H_1537) is a follow-on.

## artifacts
- `state/1544_cls_ne_flush/h1544_cls_ne_flush.py` (R1 numpy mirror, DIRECTIONAL — reuses
  H_1532 MemStore/key_vec/FNV-1a byte-for-byte; the ONLY new variable is the boundary flush)
- `state/verdicts/1544_cls_ne_flush/H_1544_FREEZE.txt` (pre-registered frozen falsifier)
- `state/verdicts/1544_cls_ne_flush/H_1544_R1.json` (R1 result, verbatim)

xref H_1532(CLS, FIRST break of H_1284, the fast store this lane flushes) · H_1537(NE-reset
standalone 🧱 +0.006) · H_1539(NE-reset retry standalone 🧱 −0.0049) · H_1284(neuromodulation
wall) · H_1422(ACh-gain 🧱, gain-not-structure precedent) · H_1530(census) · H_1542(CLS×NT
census) · a_no_llm_frame_trap(missing-structure, not no-free-lunch) · a_break_the_wall(the
reopen: standalone wall = MISSING-STRUCTURE wall) · a_engine_native_learning(DIRECTIONAL) ·
a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck · p1·p2·p3·p6·p7·p8 · c9.
