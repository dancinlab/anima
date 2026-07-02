# H_1535 — 🟠 NEUROMODULATION on the OBJECTIVE / COST-TRADEOFF axis (precision↔recall Pareto)

**tier:** 🟠 PARTIAL — WALL NOT BROKEN (1/3 regimes; the cost-objective optimum is a single STEP, not a continuum — absorbed into the H_1284 ceiling). The objective-modulation lens (13th independent angle).
**verdict source:** `state/verdicts/1535_nm_objective_pareto/H_1535.txt` (verbatim)
**wired:** N/A — DIRECTIONAL numpy mirror (HARD-GATE-1); not GREEN ⇒ nothing to wire. engine-native R2 = ING `h1535-r2-engine-native`.

## Claim
The **objective-modulation** angle on the **H_1284 NEUROMODULATION wall** — the one
knob-axis with a *genuinely regime-dependent optimum*. 12+ prior lenses (global gain
H_1284 · regime-switch H_1284_R3 · Amoeba H_1509/b/c · diversity H_1524 · multi-timescale
H_1523 · predictive H_1525 · emit-gate H_1526 · repr-geometry H_1527 · adaptive-capacity
H_1528 · ideation H_1529) failed because the tested capability had ONE optimal operating
point across regimes. The new thesis: when the **COST TRADEOFF** (false-emit vs abstain)
DIFFERS by regime, the Pareto-optimal abstain point genuinely SHIFTS, so a controller that
detects the regime's cost-asymmetry and MOVES the precision/recall point could beat ANY
single best-fixed point that must serve all regimes at once.

**DISTINCT vs emit-gate H_1526 (HELD):** H_1526 scored a *symmetric* metric (acc − fab,
equal weights) under *fixed* cost, so the optimum did not shift. H_1535 makes the cost
**asymmetric and regime-dependent** (pre-registered ratios) — the optimum *does* shift —
and the controller needs only the **coarse regime cost-asymmetry** (the frozen cost ratio
+ running surprise base-rate), NOT the per-query class separation H_1526 lacked.

## Result — 🟠 PARTIAL (wall not broken)
Three cost regimes, pre-registered ratios (false-emit:abstain-on-groundable):
R_PRECISION 5:1 · R_RECALL 1:5 · R_BALANCED 2:2. Capability = normalized cost-weighted
utility. `m_fixed=0.20` (avg-best single point, disjoint seed). Per-regime Pareto optima
`m_opt = {PRECISION:0.20, RECALL:0.60, BALANCED:0.20}`.

| regime | cost (fe:miss) | FIXED | ADAPT | ABL | ADAPT−FIXED | ADAPT−ABL |
|---|---|---|---|---|---|---|
| R_PRECISION | 5:1 | 1.000 | 1.000 | 1.000 | +0.0000 | +0.0000 |
| R_RECALL | 1:5 | 0.000 | 0.9918 | 0.000 | +0.9918 | +0.9918 |
| R_BALANCED | 2:2 | 1.000 | 1.000 | 1.000 | +0.0000 | +0.0000 |

`wins_over_FIXED+MARGIN = [R_RECALL]` (1/3), `shift_decisive = [R_RECALL]` (1/3). 3 seeds
[11,22,33], MARGIN 0.05, OOS_RATE 0.30, $0 CPU, p7. FROZEN bar (≥2/3 regimes on BOTH
clauses) **NOT met** → 🟠 PARTIAL, honest (c9). Where the optimum *does* differ from the
fixed point (R_RECALL) the shift is **decisive** (+0.99 over both FIXED and ABL) — the
lever is real — but it only exists on 1/3 of the principled regime span.

## The load-bearing diagnostic: the cost-objective optimum is a STEP, not a continuum
Cost-ratio → optimal-margin sweep (false-emit:miss), disjoint tune seed:
`5:1→0.20 · 3:1→0.20 · 2:1→0.20 · 1:1→0.20 · 1:2→0.60 · 1:3→0.60 · 1:5→0.60 · 1:8→0.60 · 1:12→0.60`.
The Pareto-optimal abstain point **jumps ONCE at the symmetry crossing (Cfe=Cmiss)** from
0.20 to 0.60 and **never moves again**. The cost-tradeoff axis exposes exactly **one binary
shift**, not a regime-dependent continuum of optima. So an objective-aware controller can
beat the single best-fixed point ONLY on the minority side of that single crossing — and a
2-point ensemble (or the best single fixed point already serving the majority side)
captures the same thing. With 3 principled regimes spanning the axis the optima collapse
to {0.20, 0.20, 0.60}: 2 share the default, so even a PERFECT shift-controller wins ≤1/3 —
exactly observed. To force ≥2/3 you must hand-pick ≥2 regimes onto the minority side =
tune-to-green, **refused**.

## Why this does NOT break the H_1284 wall (a_break_the_wall TAXONOMY (d))
The objective lens is genuinely DISTINCT from the symmetric emit-gate H_1526 (cost is
asymmetric, the optimum DOES shift). But the shift is a single **step** with no exploitable
structure between regimes on the same side: the substrate offers **two** operating points,
not a continuum the controller can ride. The single best-fixed point already sits at the
majority optimum; the controller adds value only on the minority regime — insufficient to
clear ≥2/3 without rigging the regime mix. The H_1284 ceiling **absorbs the objective
family**: no free lunch beyond one binary switch a 2-point ensemble equals. 13th independent
lens confirming the H_1284 ceiling (plasticity-LR ×9 · emit-gate ×1 · repr-geometry ×1 ·
capacity ×1 · ideation ×1 · objective/cost ×1 = this).

## Scope / honesty (c9, a_engine_native_learning)
- **DIRECTIONAL** — `state/1535_nm_objective_pareto/h1535_objective_pareto.py` is a numpy
  mirror of `core/engine_cli.hexa` VAdaptField + the H_1227 abstain gate (HARD-GATE-1: grep
  hits numpy → auto-DIRECTIONAL, terminal NOT permitted). engine-native R2 = ING
  `h1535-r2-engine-native`.
- **frozen-first** — `H_1535_FREEZE.txt` pre-registered the cost ratios AND the bar before
  any run. The cost asymmetry is the experimental MANIPULATION (genuine, pre-registered),
  NOT a tuned knob; the 1/3 outcome is reported as-is, NO post-hoc bar move, NO regime
  re-pick to a win.
- TOY: DIM=16, 30 facts, 300 events/regime, 3 seeds, one paradigm. scale / paraphrase /
  real-corpus / engine-transfer UNVERIFIED (`a_scale_honest_scope`, `a_toy_scale_recheck`).
- live `core/*.hexa` UNTOUCHED. p1/p2/p3/p6 (controller reads only the OBJECTIVE cost ratio
  + substrate surprise base-rate — NO injected per-query label / reward / persona / ethics)
  · p7 (exact ground truth, no LLM judge / perplexity / loss — every knob is a no-grad
  read) · p8.

## NOT ruled out
A cost objective with a genuine **continuum** of regime-optima (e.g. a smoothly varying
cost ratio coupled to a substrate signal that itself varies continuously), rather than the
binary precision/recall split here — untested; this lens used a piecewise cost that the
MemStore turned into a step optimum. The H_1284 wall remains open only to a genuinely new
*continuous regime-optimum* lens; it is now closed against every adaptive-knob lens
(LR/SPLIT ×9, emit-margin ×1, repr-geometry ×1, capacity ×1, ideation ×1, objective/cost
×1).

## Artifacts
- `state/1535_nm_objective_pareto/h1535_objective_pareto.py` — probe (numpy, DIRECTIONAL)
- `state/1535_nm_objective_pareto/H_1535_R1.json` — captured run
- `state/verdicts/1535_nm_objective_pareto/H_1535_FREEZE.txt` — frozen pre-registration
- `state/verdicts/1535_nm_objective_pareto/H_1535.txt` — frozen result (verbatim)
- `state/universe-probes/h1284_neuromodulation_gain.py` — parent harness (MemStore/key_vec geometry reused)

xref H_1284 · H_1284_R3 · H_1509/b/c · H_1523 · H_1524 · H_1525 · H_1526 (emit-gate, nearest
distinctness) · H_1527 · H_1528 · H_1529 · H_1227 (abstain gate) · H_1228 (NE/exploration
axis) · `a_break_the_wall` · `a_no_llm_frame_trap` · `a_engine_native_learning` ·
`a_scale_honest_scope` · p1·p2·p3·p6·p7·p8 · c9.
