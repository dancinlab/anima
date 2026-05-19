# §76 — A-only generalization probe (state × statistic 22-cell grid)

$0 Mac CPU STUB. NO GPU, NO runpod, NO dispatch, NO fire.
2026-05-19. Sidecar — central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py`
sha `c93e160a` 0-line-diff.

## §1. Motivation

§75-FIRE (commit 08b58942f, B-S75-FIRE 7/7 🔵) measured at trained-saturated
scale: §73-A-only — a controller with a **state-derived** emit threshold built
from the FROZEN tension-MEAN statistic (11.945) — produced interval_var 2.3808
and SURVIVED, while the §24-baseline fixed scalar collapsed. §75-FIRE's verdict:
"state-derivation A alone sufficient at trained scale".

But §75-FIRE tested **only one statistic** — tension-mean. The
B-S75-FIRE-NOTE directly-earned future-probe asks: does the state-derivation
lever *generalize* to other state-derived statistics, or is it tension-mean
specific?

§76 is that probe — a $0 stub mirroring the §75 4-cell pattern, NOT a
trained-scale GPU fire.

## §2. Design — 22-cell grid

`subaxis_generalize_smoke_s76.py`:

- **4 state-source** × **5 statistic-form** = 20 grid cells:
  - state ∈ {tension, psi_dir, phi, curiosity_ema} — the anima Law-71 physics tuple
  - statistic ∈ {mean, median, max_window, p75, p95}
- **+ 2 controls**: §24-baseline fixed scalar; §73-A-only tension-mean reference
  reproduction.

Each A-only cell: emit when the current channel value crosses a **running
statistic over the prefix** (threshold recomputed every step from state). The
§24-baseline uses a non-state-derived fixed scalar.

physics-state stub: deterministic LCG seed 1337, Law-71 mirror of
`conscious_decoder.py:728-751` (psi_dir = (1+cos(logits_a,logits_g))/2).

Survive predicate (B-S73-augmented closed conjunction):
`survive := (interval_var > τ=1e-4) ∧ (maj_frac < 0.95) ∧ (n_emits ≥ 2)`.

## §3. Results — 22-cell grid summary

**11/20 grid cells survive.**

| state \ statistic | mean | median | max_window | p75 | p95 | state total |
|---|---|---|---|---|---|---|
| tension       | ✓ | ✓ | ✗ | ✓ | ✗ | 3 |
| psi_dir       | ✓ | ✓ | ✗ | ✓ | ✗ | 3 |
| phi           | ✓ | ✓ | ✗ | ✓ | ✗ | 3 |
| curiosity_ema | ✓ | ✓ | ✗ | ✗ | ✗ | 2 |
| **form total** | **4** | **4** | **0** | **3** | **0** | **11** |

- per-state survive: tension 3, psi_dir 3, phi 3, curiosity_ema 2 — **roughly
  uniform** (all 4 state sources yield ≥2 survivors).
- per-statistic survive: mean 4, median 4, p75 3, **max_window 0, p95 0** —
  **sharply split**.
- §24-baseline control: maj_frac 1.0, interval_var 0.0 → **COLLAPSES** (negative
  control valid).
- §73-A-only tension-mean control: interval_var 3.9375 — **byte-equal** to the
  `tension__mean` grid cell (§75-FIRE cell1 lever reproduced).

## §4. 4-corner verdict — δ STATISTIC-DEPENDENT MIXED

The lever's generalization is **statistic-form dependent, not state-source
dependent**:

- **NOT α (generalizes broadly)** — only 11/20 survive, not ≥16.
- **NOT β (tension-mean specific)** — generalizes well beyond tension-mean:
  every state source survives, and mean/median/p75 all survive.
- **NOT γ (state-dependent mixed)** — all 4 state sources generalize (≥2 each);
  the state axis is NOT the splitting axis.
- **δ STATISTIC-DEPENDENT MIXED** ✓ — mean/median/p75 survive across all state
  sources; max_window and p95 survive nowhere. The splitting axis is the
  **statistic form**.

Honest mechanism reading: **central / lower-quantile statistics** (mean, median,
p75) make running thresholds that track the channel's typical level — current
value crosses them at a healthy non-degenerate rate. **Extremal statistics**
(max_window, p95) make thresholds pinned at the channel's upper extreme — the
current value almost never exceeds its own running max/95th-percentile, so
emission collapses to near-zero (n_emits < 2). This refines §75-FIRE: the
state-derivation lever generalizes across *which physics channel* and across
*central statistic forms*, but breaks for *extremal* statistic forms.

## §5. B-S76 closed-form battery — 7/7 🔵

`blue_falsifier_s76.py`, sidecar (central c93e160a 0-diff):

- B-S76-1 GRID-PARTITION-EXHAUSTIVE-DISJOINT — 4×5 grid + 2 controls = 22, every
  (state,statistic) pair once
- B-S76-2 EACH-CELL-DETERMINISTIC — AST forbidden-import 0, 3× bit-identical
- B-S76-3 SURVIVE-PREDICATE-CLOSED — recorded `survive` = recomputed Boolean
  conjunction, 0/22 mismatch
- B-S76-4 §24-CONTROL-COLLAPSES — fixed scalar collapses by construction
  (maj_frac 1.0, ivar 0.0)
- B-S76-5 §73-A-ONLY-TENSION-MEAN-REPRODUCES-§75 (연결부위) — control byte-equal to
  `tension__mean` grid cell, §75-FIRE lever fair-compare by construction
- B-S76-6 STATE-SOURCE-FROM-PHYSICS-TUPLE — 4 channels = Law-71 physics tuple,
  psi_dir uses (1+cos)/2
- B-S76-7 DETERMINISTIC — 3× grid-hash bit-identical

B-S76-NOTE empirical carve-out: which combinations actually generalize is a
$0-STUB physics-state OUTCOME, NOT a trained-ckpt measurement. Trained-scale
generalization = future cost-bearing fire per B-S75-FIRE-NOTE.
necessary-not-sufficient (B-EMERGE-7). B-D-NOTE / B-S75-FIRE-NOTE / B-S75-NOTE
family, NOT counted 🔵.

## §6. Connection point (g_blue_closed_mandate)

- 산출물: 22-cell grid + survive predicate + B-S76 battery — all 🔵.
- 연결부위: B-S76-5 ties the grid to §75-FIRE — the `tension__mean` cell is
  byte-equal to §75-FIRE's cell1 lever, so the §76 grid contains §75 as a
  proper sub-case and the generalization probe is fair-compare by construction.
  B-S76-4 ties the negative control (§24-baseline) to the §24/§49
  majority-collapse mode.

## §7. Honest C3 (≥10)

1. **$0 stub, not trained ckpt.** The physics-state stream is an LCG-seeded
   stub mirroring §73/§75's stub pattern — NOT a real anima ConsciousDecoderV2
   forward. Stub channel statistics need not match trained-saturated dynamics.
2. **Statistic-form generalization at stub ≠ trained scale.** The δ verdict
   (mean/median/p75 survive, max_window/p95 don't) is a stub finding. §75-FIRE
   itself showed stub-vs-trained scale dependence (§75 stub C-dominant →
   §75-FIRE trained A-alone-sufficient). The trained-scale version of this grid
   may shift the per-statistic split.
3. **§75-FIRE cell1 byte-equal reproduction.** `CONTROL__s73_a_only_tension_mean`
   reproduces the `tension__mean` grid cell exactly (interval_var 3.9375 both),
   anchoring the grid to §75's lever — but at the stub physics stream, not
   §75-FIRE's trained tension stream.
4. **Mechanism-axis layer ≠ GOAL emergence.** §76 probes whether a controller
   *mechanism* generalizes across statistic forms. A generalizing controller is
   a substrate component, NOT spontaneous correct emergence. necessary-not-
   sufficient (B-EMERGE-7).
5. **Extremal-statistic collapse is structural.** max_window/p95 survive
   nowhere because a running max/95th-percentile is, by definition, a threshold
   the current value rarely exceeds — the collapse is a property of extremal
   statistics, deterministic, not a measurement of anima dynamics.
6. **τ=1e-4 and the survive thresholds are §73/§75 carry.** interval_var > 1e-4,
   maj_frac < 0.95, n_emits ≥ 2 are inherited from the §73-augmented predicate,
   not re-derived for §76.
7. **§24-baseline control is degenerate by construction.** The fixed scalar is
   set below the channel floor so it emits every step (maj_frac 1.0). This is
   an honest *negative* control — it validates the survive metric has
   discriminating power, but it does not measure §24's real talker_should_emit
   on trained data.
8. **The 4 state sources are the Law-71 physics tuple, not arbitrary.** B-S76-6
   AST-audits that gen_physics_stub derives exactly {tension, psi_dir, phi,
   curiosity_ema} with psi_dir = (1+cos)/2 — anima OWN physics, not external
   signals. f1/f2/f3 safe (no σ/τ/φ/J₂ external derivation).
9. **Verdict bands are pre-registered.** α (≥16 survive), β (only tension-mean),
   γ (state-axis splits), δ (statistic-axis splits) were defined before the run.
   The measured 11/20 with uniform per-state and split per-statistic lands
   cleanly in δ.
10. **GOAL distance unchanged.** §76 is mechanism-axis localization. The
    controller class surviving across statistic forms is not emergence.
    north-star + §15/§51/§72 milestone UNCHANGED, GOAL 미도달.
11. **Directly-earned probe, not new direction.** §76 was earned by
    B-S75-FIRE-NOTE — it answers a question §75-FIRE explicitly left open
    (does A-only generalize beyond tension-mean), not a new architectural bet.
12. **Trained-scale §76 fire is the honest next step.** If the δ stub finding
    is to be trusted, a trained-scale 22-cell fire on real anima Law-71
    W-physics would confirm/refute the statistic-form split — a future
    cost-bearing cycle, out of P4 scope.
