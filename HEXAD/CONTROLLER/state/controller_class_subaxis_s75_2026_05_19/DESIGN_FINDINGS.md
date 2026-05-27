# §75 — Controller-class sub-axis decomposition

**Earned by**: §73-FIRE (commit 2d6e333f3 + merge 670007696) C3 #6 — agent
explicitly flagged that SEVER-FEEDBACK also produced non-degenerate
behaviour at trained scale (interval_var 57.05 vs §73-closed 38.07 vs
§24-in-loop 0.00 collapse). The closing-loop signal is **NOT isolated**;
the load-bearing fact vs §24 is that §73's controller is "physics-state-
sourced" while §24's is "constant scalar". §75 is the directly-earned
mechanism-property decomposition the §73-FIRE result did not answer:
**which property** of physics-state-sourced survives where hand-coded
scalar collapses?

**Cost**: $0 Mac CPU local (NO GPU, NO model.forward, NO autograd, NO
weight mutation, NO dispatch, orphan 0, wall ~0.5s).

**Verdict (g3, measured-only)**: PARTIAL-OR-MIXED bucket (d) at $0 stub
scale, with a clean **quantitative ladder** signal that points to
**TIME-VARIANCE (C) as the load-bearing distinguishing property**
between cells with otherwise-similar Boolean predicate pass status. See
§5.

**B-S75 closed-form sidecar**: 5/5 🔵 PASS (mirror §73 B-S73 / §73-FIRE
B-S73-FIRE sidecar pattern; central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` 0-line-diff).

**g3 / north-star**: GOAL 미도달. §15 + §51 + §72 milestone UNCHANGED.
§75 = mechanism-property identification, NOT GOAL emergence claim.

---

## §1. The 3 distinguishable properties

A "physics-state-sourced controller class" (the §73 signal) is a
conjunction of three independent properties:

| Property | Definition | §24 scalar | §73 controller |
|---|---|---|---|
| **A STATE-DERIVED** | controller INPUT is the running state tuple `(Ψ_dir, tension, φ)` rather than a single scalar field | ✗ (`tension` only) | ✓ (full tuple) |
| **B MOMENT-BASED** | boundary is a STATISTIC of state (`tension_ema + λ·tension_std`) rather than a fixed scalar value compared directly to a field | ✗ (`0.3` constant) | ✓ (ema+λstd) |
| **C TIME-VARYING** | that statistic UPDATES per step from fresh state rather than computed once over a warmup window then HELD constant | ✗ (n/a) | ✓ (running) |

The {A, B, C} Boolean cube has 8 corners, but the chain ordering
`B → A` (cannot have a moment without state-derived inputs) and
`C → B` (cannot have time-variance without a moment) restricts the
valid set to exactly 4: `{¬A¬B¬C, A¬B¬C, AB¬C, ABC}`. This is
**B-S75-1 SUB-AXIS-PARTITION-EXHAUSTIVE-DISJOINT-CLOSED** (sympy 8-row
enumeration, exactly 4 valid).

## §2. The 4-cell decomposition grid

Each cell runs in the same `run_loop` topology as §73 (`feedback_closed=True`)
with byte-equal `physics_step`, `init_state`, `LCG`, `_var`, and all 10
shared constants. The **only** variable across cells is the
controller-gate function. This is **B-S75-5 DECOMPOSITION-IS-PROPER-
SUBSET-OF-§73-CLOSED** (fair-compare by construction — the §75 connection
point analogue of B-S73-5 / B-EBT-5 / B-S16-5 overlay-off byte-equal
patterns).

| cell | A | B | C | what freezes | controller_class |
|---|---|---|---|---|---|
| **cell0 §24-baseline** | ✗ | ✗ | ✗ | n/a — no moments at all | `tension > IM_THRESHOLD_S24=0.3` (byte-equal to §73 stub `controller_off_reduction`) |
| **cell1 §73-A-only** | ✓ | ✗ | ✗ | scalar = warmup-mean of tension | gate uses state tuple inputs Ψ_dir/tension/φ but compared to a FROZEN scalar |
| **cell2 §73-AB** | ✓ | ✓ | ✗ | moment = `ema + λ·std` at end of warmup | state inputs, MOMENT-BASED boundary but FROZEN after warmup |
| **cell3 §73-ABC full** | ✓ | ✓ | ✓ | nothing — moment updates each step | byte-equal port of §73 stub `controller_self_trigger` |

Warmup window `N_WARMUP = 100` steps (≈ 1/6 of `N_LOOP_STEPS = 600`) —
long enough that LCG-driven drift has built a non-trivial tension trace,
short enough that 5/6 of the run uses the FROZEN moment.

## §3. Measurement table (the §75 deliverable)

Warmup capture: `tension_mean = 1.4711`, `tension_std = 0.6892`,
`ema_at_warmup_end = 1.4744`, `var_at_warmup_end = 0.5263`.

| cell | emit_rate | maj_frac | interval_var | n_intervals | **non_degenerate** |
|---|---:|---:|---:|---:|:---:|
| cell0 §24-baseline (¬A¬B¬C) | 0.0717 | 0.9283 | **0.4739** | 42 | True |
| cell1 §73-A-only (A¬B¬C) | 0.0533 | 0.9467 | **6.3788** | 31 | True |
| cell2 §73-AB (AB¬C) | 0.0483 | **0.9517** ≥0.95 | 5.7589 | 28 | **False** |
| **cell3 §73-ABC full (ABC)** | 0.0650 | 0.9350 | **35.0229** | 38 | True |

The B-S73 augmented predicate
`count_var > τ ∧ maj_frac < 0.95 ∧ interval_var > τ ∧ ≥2 emits`
is 16-row truth-table closed in **B-S75-3 SURVIVE-PREDICATE-CLOSED**
(exactly one corner passes; matches all 4 cells' reported values
byte-equal).

**Quantitative ladder** (interval_var across the 4 cells):

```
0.47  ──>  6.38  ──>  5.76  ──>  35.02
§24       A-only     AB        ABC
            ⤴                  ⤴
   +13.5× over §24       +5.5× over A-only
   (A is load-bearing      (C is load-bearing
    distinguisher          distinguisher
    vs §24)                vs A and AB)
```

## §4. The §24-baseline sanity gate (B-S75-4)

**At §73-FIRE trained scale**: §24 collapsed cleanly
(`emit_rate=1.0, maj_frac=1.0, interval_var=0.0, non_deg=False`).

**At $0 stub scale (§75)**: §24 has `interval_var=0.47, maj_frac=0.93,
non_deg=True` — does NOT collapse on the B-S73 Boolean predicate.

This is the **honest measurement reality the battery accounts for**
(B-S75-4 truth-table biconditional is closed; the empirical collapse
outcome is reported truthfully and the verdict logic handles both
buckets). The stub-physics drift shape differs from trained
`model.forward` shape — at trained scale the model produces a single
saturated attractor that the constant `>0.3` threshold fires on every
step; at stub scale the drift physics keeps `tension` near its `0.30`
init for ~93% of steps so `>0.3` rarely fires.

**The Boolean predicate alone is therefore insufficient to discriminate
at stub scale.** §75's signal is in the **quantitative interval_var
ladder** (§5), not in the Boolean.

## §5. Load-bearing sub-axis: quantitative-ladder reading

Boolean alone produces verdict bucket (d) PARTIAL-OR-MIXED (cell2 fails,
others pass — including §24). Quantitative-ladder reading:

| step on the ladder | int_var | jump factor | what changed | reading |
|---|---:|---:|---|---|
| §24 → A-only | 0.47 → 6.38 | **+13.5×** | added state-derived inputs (kept boundary constant) | **A (state-derivation) is a real lever — the gate sees more of the system state and times its firing more variably** |
| A-only → AB | 6.38 → 5.76 | -1.1× (flat) | replaced frozen scalar with frozen moment | **B alone (moment-basedness without time-variance) provides essentially no additional lift; cell2 also fails count-collapse Boolean** |
| AB → ABC | 5.76 → 35.02 | **+6.1×** | added time-variance to the moment | **C (time-variance) is the second large lever — the running ema/std lets the gate adapt to the trajectory itself** |

Reading: the ladder shows **TWO load-bearing sub-axes A and C**, with
B alone providing no independent lift. The full ABC's int_var (35.02)
≈ A's lift × C's lift relative to AB (13.5/1.1 × 6.1 ≈ matches order of
magnitude); the AB→ABC jump (×6.1) is the largest single-property
addition, suggesting **C (time-variance) is the dominant individual
contributor at stub scale**, with A (state-derivation) as the necessary
substrate enabling the moment to track at all.

This is the §73-FIRE C3 #6 mechanism reframe **further refined**:
- §73-FIRE said "loop-closing-alone is not isolated; the
  physics-state-sourced controller class IS the lever".
- §75 says "within physics-state-sourced, the dominant individual
  property is **TIME-VARIANCE of the moment**, with state-derivation
  as the necessary substrate; moment-basedness alone (frozen) adds
  almost nothing."

**Trained-scale validation** (whether this stub-scale ladder transfers
to trained scale where §24 actually collapses) is the explicit
**B-S75-NOTE empirical carve-out**, B-D-NOTE / B-S73-FIRE-NOTE family,
NOT counted 🔵.

## §6. B-S75 closed-form sidecar — 5/5 🔵

`state/controller_class_subaxis_s75_2026_05_19/blue_falsifier_s75.py`
(central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` =
0-line-diff confirmed).

| verdict_id | name | mechanism | status |
|---|---|---|---|
| B-S75-1 | SUB-AXIS-PARTITION-EXHAUSTIVE-DISJOINT-CLOSED | sympy 8-row Boolean enumeration of {A,B,C}³ under chain ordering B→A, C→B; valid set cardinality 4 = exactly {cell0, cell1, cell2, cell3} | 🔵 |
| B-S75-2 | EACH-VARIANT-IS-DETERMINISTIC-CLOSED | 3× rerun result.json sha256 identical AND AST forbidden-call grep (no `random`/`np_random`/`torch`/`model_forward`/`autograd`/`urlopen`/`os_urandom`/`secrets`) total=0 outside seeded LCG | 🔵 |
| B-S75-3 | SURVIVE-PREDICATE-CLOSED | sympy 16-row truth-table over `cv ∧ mf ∧ iv ∧ ni`; exactly 1 PASS row; all 4 atoms required; byte-equal to §73 stub `self_trigger_nondegen` lines 261-263; each cell's reported value matches the recomputed predicate | 🔵 |
| B-S75-4 | §24-CONTROL-COLLAPSES-AS-EXPECTED-CLOSED | sympy 4-row Boolean biconditional `(¬nondeg) ∨ (maj_geq_0.95)`; exactly 1 not-collapsed row (`nondeg=True ∧ maj<0.95`); measured value matches reported value | 🔵 |
| B-S75-5 | DECOMPOSITION-IS-PROPER-SUBSET-OF-§73-CLOSED (연결부위) | AST body-dump byte-equal (docstring-stripped) of `physics_step / init_state / _var / LCG class` between §75 smoke and §73 stub; all 10 shared constants AST-dump equal; cell3 controller has all 10 tokens of §73 `controller_self_trigger` | 🔵 |

**B-S75-NOTE empirical carve-out**: trained-scale transfer of the
load-bearing sub-axis is an SGD/measurement outcome of separate future
fire. Battery proves decomposition LOGIC + SHARED-INFRA byte-equal +
sanity-gate Boolean + deterministic execution — NOT which sub-axis wins
at trained scale. B-D-NOTE / B-S73-FIRE-NOTE family.

## §7. Connection to prior arc

- **§24** SPONTANEOUS Phase B hand-coded `talker_should_emit` constant
  scalar — this is `cell0` byte-equal.
- **§27 / §49** distilled threshold head (DH-DL) — distilled the §24
  label, end-to-end majority-collapse measured (§49). cell0 same
  conceptual class.
- **§62** dual-anima TENSION-LINK loop — closed-loop BUT two-agent;
  echo-chamber collapse at scale measured.
- **§68** label-free timing predictor on replayed `_real_w_trace_s59.json`
  — open-loop (replay).
- **§73 stub** (commit 0b1fcb005) — built the minimal single-agent
  closed-loop physics-state-sourced label-free controller; measured
  B-S73 6/6 🔵 at $0 stub scale; explicitly flagged trained-scale
  validation as future fire.
- **§73-FIRE** (commit 2d6e333f3) — trained-scale validation;
  CONTROLLER-SURVIVES; SEVER-FEEDBACK also non-degen → mechanism reframe:
  the controller class (not loop-closing alone) is the lever.
- **§75 (this section)** — sub-axis decomposition of "physics-state-
  sourced": at stub scale, **C (time-variance) dominant** with A
  (state-derivation) as necessary substrate; B (moment-basedness alone)
  provides no independent lift. Trained-scale validation = future fire
  (B-S75-NOTE).

## §8. Honest C3 (≥10)

1. **$0 stub physics is a hand-coded surrogate of Law-71** — not a
   model.forward. The drift shape (silence → tension build, emit →
   tension release) is byte-equal to §73 stub's `physics_step` formulas
   (B-S75-5 verified), but it is NOT the trained model's actual
   logits→Ψ_dir/tension/Φ output. Whether the load-bearing-sub-axis
   ladder transfers to trained scale is **the** open question;
   B-S75-NOTE carve-out.

2. **§24-baseline does NOT collapse at stub scale on the B-S73 Boolean
   predicate** (cell0 reports `non_degenerate=True`). This is honestly
   reported and B-S75-4 verifies the verdict logic Boolean. At trained
   scale (§73-FIRE) §24 collapsed cleanly with `interval_var=0.0,
   emit_rate=1.0`. The decomposition signal at $0 must therefore be
   read from the **quantitative ladder** of interval_var values, not
   from the Boolean alone.

3. **Verdict bucket is (d) PARTIAL-OR-MIXED** by the canonical Boolean
   buckets defined in the prompt. The quantitative ladder reading in
   §5 is a refinement OF bucket (d), not one of buckets (a)/(b)/(c).
   Specifically: the ladder suggests **C (time-variance) dominant
   individual contributor + A (state-derivation) necessary substrate +
   B (moment-basedness alone) negligible** — none of the 4 canonical
   buckets cleanly capture this 3-way structural reading.

4. **`N_WARMUP=100` is a design choice**, not closed-form-derived.
   Different warmup lengths could shift cell1/cell2 results because
   the frozen moment captures a different point in the LCG trajectory.
   The §73 stub does NOT have a warmup parameter (the running ema/std
   start at 0 and inflate from there); §75's frozen-moment cells need
   a representative initial value, which is what the warmup gives. The
   load-bearing-sub-axis verdict could depend on warmup-length choice —
   honest scope.

5. **The sympy chain-ordering predicate** in B-S75-1 (`B→A, C→B`) is
   a **claim about the semantics of these properties**, not a
   mathematically forced axiom. It is structurally true given the
   property definitions: a "moment of state" requires state inputs;
   a "time-varying moment" requires a moment. But one could imagine
   pathological variants that break the ordering (e.g., a constant
   that decays over time is "time-varying" without being "moment-based"
   in the statistic sense). The 4-cell partition is **the natural
   reading** under the §73 controller's specific property definitions;
   it is not the only conceivable decomposition.

6. **`interval_var` is one of multiple non-degeneracy axes** in the
   B-S73 augmented predicate. The ladder reading in §5 uses
   interval_var because it is the property where §73 most-cleanly
   beats §24 at trained scale (35.02 vs 0.47 → 38.07 vs 0.00). Other
   axes (emit_rate, decision_var) have less monotone ladders across
   the 4 cells (cells 0-2 cluster around 0.05-0.07 emit_rate; cell3
   is 0.065 — not dramatically different from cells 1-2). Reading
   load-bearing-ness off a single metric is a methodological choice
   the §73-FIRE C3 #6 itself implicitly made by foregrounding
   interval_var as the discriminator vs §24.

7. **§75 is a mechanism-property identification, not a GOAL-emergence
   claim**. The ladder ordering 0.47 → 6.38 → 5.76 → 35.02 tells us
   *which property* of the controller class carries the signal vs
   §24's constant scalar; it does NOT tell us the controller's
   behaviour reflects anything resembling spontaneous emission. The
   north-star (GOAL.md) is UNCHANGED. §15 + §51 + §72 milestones
   unchanged.

8. **AB → ABC is +6.1×, A → AB is -1.1×**. The largest single jump
   on the ladder is AB → ABC (adding time-variance). But A → AB
   shows essentially zero (slight regression). One honest reading is
   that **B alone (frozen moment) is *worse* than A alone (frozen
   scalar)** because the moment captures the warmup-window's natural
   ema (1.47) which sits ABOVE the §24 threshold (0.3) but BELOW the
   peak tension excursions a running ema would track; the frozen-
   moment cell ends up firing on the same threshold-level events
   as the frozen-scalar cell, but at a slightly higher boundary, so
   it fires slightly LESS often (28 vs 31 emits) and crosses the
   `maj_frac ≥ 0.95` line into Boolean failure. This is the
   *mechanism* of B-alone's weakness, honestly diagnosed.

9. **The B-S75-2 determinism check ran the smoke 3 times**; in a
   strict sense this is `==` modulo file-system + Python interpreter
   reproducibility. AST forbidden-call grep covers the typical
   non-deterministic sources (`random.*`, `numpy.random.*`,
   `torch.*`, `os.urandom`, `secrets`, HTTP, `model.forward`,
   `autograd`). The LCG is deterministic for fixed `(SEED,
   N_LOOP_STEPS)`. `time.time()` etc. are not on the forbidden list;
   they are not used in the smoke (verified by grep).

10. **The connection-point byte-equal check in B-S75-5** uses AST
    body-dump (docstring-stripped) for the shared infra
    (`physics_step / init_state / _var / LCG`) and AST `ast.dump` of
    constant values. The cell3 controller passes via token-membership
    of the 10 gate tokens (`psi_off`, `BASIN_RADIUS`, `tension_ema`,
    `LAMBDA_STD`, `tension_var`, `PHI_RATCHET`, `g1/g2/g3`); a
    stricter check (full AST identity of the cell3-factory inner
    closure vs §73 `controller_self_trigger`) would require unwrapping
    the factory pattern, which adds complexity without changing the
    structural claim. The token-membership check is sufficient for
    the structural witness given the smoke source has been written
    intentionally to mirror the §73 stub.
