# H_1526 — 🧱 NEUROMODULATION on the EMIT/SALIENCE gate (abstain_margin), CALIBRATION capability

**tier:** 🧱 WALL HOLDS (CLOSED-NEGATIVE, no free lunch — the 10th independent lens, the emit-gate knob too)
**verdict source:** `state/verdicts/1526_neuromod_emitgate/H_1526.txt` (verbatim)
**wired:** N/A — DIRECTIONAL numpy mirror (HARD-GATE-1); WALL-HOLDS ⇒ nothing to wire.

## Claim
The LAST live angle on the **H_1284 NEUROMODULATION wall**. All 9 prior lenses
(global gain H_1284 · regime-switch H_1284_R3 · Amoeba allosteric-buffer H_1509/b/c ·
diversity H_1524 · multi-timescale H_1523 · predictive H_1525) modulated the
**plasticity-LR / SPLIT_THRESH** knobs and were INERT — because RECALL is decided by
cell **KEY-GEOMETRY**, not the LR schedule (geometry-not-protocol bottleneck). The ONE
knob that is NOT geometry-bound = the **abstain_margin** (the emit/abstain gate, H_1227
no-fabrication threshold). The abstain DECISION is THRESHOLD-bound, and the OPTIMAL
threshold SHIFTS with regime. A-priori thesis: a neuromodulator that ADAPTS the abstain
margin by substrate confidence/surprise could beat a single best-fixed margin ACROSS
regimes where the fixed one cannot — measured on a **CALIBRATION** capability (emit the
right answer when groundable, abstain when ungroundable), NOT recall-accuracy. Stream
has BOTH groundable + ungroundable ("ghost") queries in EVERY regime (OOS_RATE=0.30) so
the abstain gate is the load-bearing decision.

## Result — 🧱 WALL HOLDS
Adaptive abstain margin **NEVER** beats best-fixed (0/3 regimes) and the substrate
gating is **INERT**: collapsing the per-event adaptive margin schedule to its own MEAN
(ABLATE) reproduces ADAPT's calibration essentially exactly (ADAPT−ABLATE ≈ 0 on every
regime). `m_star = 0.55` (grid-tuned, disjoint seed 7).

| regime | A (best-fixed) | ADAPT | ABLATE | ADAPT−A | ADAPT−ABLATE | A_fab | ADAPT_fab |
|---|---|---|---|---|---|---|---|
| R1_STABLE | 0.7211 | 0.7189 | 0.7211 | −0.0022 | −0.0022 | 0.2422 | 0.2733 |
| R2_DRIFT  | 0.7144 | 0.7144 | 0.7156 | −0.0000 | −0.0011 | 0.2167 | 0.2656 |
| R3_NOISE  | 0.7211 | 0.7167 | 0.7211 | −0.0044 | −0.0044 | 0.2133 | 0.2778 |

`wins_over_A+MARGIN = []` (0/3), `ablate_decisive = []` (0/3). 3 seeds [11,22,33],
MARGIN 0.05, OOS_RATE 0.30, $0 CPU, p7. FROZEN bar (≥2/3 regimes ADAPT beats best-fixed
by ≥0.05 AND ablation decisive on ≥2) **NOT met on either clause** → WALL HOLDS, honest
(c9).

## Why the emit gate is INERT too (the load-bearing diagnostic)
The adaptive margin **does move** (mean 0.60–0.65 per regime, with per-event variation
around `m_star=0.55`) — this is not a frozen knob. Yet calibration is unchanged because
the substrate surprise signal **û (EMA of recon-err) cannot separate a noisy-groundable
query from an ungroundable ghost**: their recon-errors overlap, so raising the margin
under high û trades fewer fabrications for more misses (and vice-versa) at the **same
total calibration**. ADAPT in fact slightly RAISES fab on every regime (its mean margin
> m_star ⇒ emits more on OOS) — the H_1284 family's exact no-free-lunch mode. The
geometry-not-protocol bottleneck **reappears on the emit gate**: because the two query
classes are not threshold-separable by any substrate confidence signal available, no
adaptive margin policy beats the single best-fixed threshold — and collapsing the policy
to its mean (ABLATE) loses nothing, confirming the gating itself contributes zero.

## Verdict frozen
🧱 **WALL HOLDS** on the emit/salience knob too. The emit-gate angle does **NOT** escape
the geometry bottleneck — the abstain threshold is THRESHOLD-bound but the *signal* that
would gate it (recon-err / surprise) does not separate the groundable-noisy from the
ungroundable, so it offers no exploitable adaptive structure over a single best-fixed
margin. 10th independent lens CONFIRMING the H_1284 ceiling; the wall now holds against
both the plasticity-LR family (9 lenses) and the emit-gate family (this lens).
`a_break_the_wall` TAXONOMY: (d) genuine no-free-lunch ceiling, NOT (a) metric-artifact
/ (b) confound / (c) infra.

## Scope / honesty (c9, a_engine_native_learning)
- **DIRECTIONAL** — `state/1526_neuromod_emitgate/h1526_emitgate.py` is a numpy mirror of
  `core/engine_cli.hexa` VAdaptField + the H_1227 abstain gate (HARD-GATE-1: grep hits
  numpy → auto-DIRECTIONAL, terminal NOT permitted). WALL-HOLDS ⇒ nothing verified to
  wire; engine-native R2 (live `core/*.hexa` abstain gate) is a confirming follow-on ONLY
  (binding re-test is GREEN-only) — ING `h1526-r2-engine-native`.
- TOY: DIM=16, 30 facts, 300 events/regime, 3 seeds, one paradigm. scale / paraphrase /
  real-corpus / engine-transfer UNVERIFIED (`a_scale_honest_scope`, `a_toy_scale_recheck`).
- live `core/*.hexa` UNTOUCHED. frozen-first, NO tune-to-green; the bar was pre-registered
  in `H_1526_FREEZE.txt` before any run and is reported as-is.
- p1/p2/p3/p6 (the gate reads only substrate recon-err/surprise — NO injected label /
  reward / persona / ethics) · p7 (exact ground truth, no LLM judge / perplexity / loss —
  the margin is a no-grad read-out) · p8.

## NOT ruled out
Calibration on a **richer substrate confidence signal** (a margin gated on the
nearest-vs-second-nearest *gap* rather than absolute recon-err, which might separate the
two query classes) — untested here; this lens used the recon-err surprise channel that
the H_1284 FREEZE cites (H_1228 NE/exploration axis). The H_1284 wall remains open to a
genuinely new *separability* lens, but is now closed against every adaptive-knob lens
(LR/SPLIT × 9, emit-margin × 1).

## Artifacts
- `state/1526_neuromod_emitgate/h1526_emitgate.py` — probe (numpy, DIRECTIONAL)
- `state/1526_neuromod_emitgate/H_1526_R1.json` — captured run
- `state/verdicts/1526_neuromod_emitgate/H_1526_FREEZE.txt` — frozen pre-registration
- `state/verdicts/1526_neuromod_emitgate/H_1526.txt` — frozen result (verbatim)
- `state/universe-probes/h1284_neuromodulation_gain.py` — parent harness (MemStore/key_vec geometry reused)

xref H_1284 · H_1284_R3 · H_1509/b/c · H_1523 · H_1524 · H_1525 · H_1227 (abstain gate) ·
H_1228 (NE/exploration axis) · `a_break_the_wall` · `a_no_llm_frame_trap` ·
`a_engine_native_learning` · p1·p2·p3·p6·p7·p8 · c9.
