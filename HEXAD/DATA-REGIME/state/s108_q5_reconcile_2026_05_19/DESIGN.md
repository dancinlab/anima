# §108-Q5-reconcile — A3-axis predicate conflation fix · design-tier $0

> **status**: RESEARCH §108-Q5-reconcile · DESIGN-TIER · $0 · NO GPU · NO runpod · NO fire · NO dispatch · NO model.forward · analytic resolution only
> **date**: 2026-05-19
> **scope**: §108's Q5 dispatch tree (`state/param_axis_fire_prep_s108_2026_05_19/DESIGN.md §5`) has a Sub-case A whose **trigger** is `A3-axis verdict == False` but whose **rationale** is "physics frozen". §107-RETRY measured these to be DISTINCT: `PHYSICS_RESPONSIVE=True` (Ψ alive, std ≈ 0.0166) yet A3 PASS=False (fails ONLY on the `psi_spread < 0.20` sub-clause). The trigger and rationale diverge. §108-Q5-reconcile = fix this in closed form by splitting the A3-axis predicate into its two distinct sub-clauses, then analytically resolve which §108 Q5 outcome §107-RETRY now maps to under the corrected predicate.
> **NOT a new fire**: §107-RETRY already measured everything (`state/dataregime_threshold_fire_s107_2026_05_19/result.json`). §108-Q5-reconcile is pure analytic resolution. Never re-fire a settled measurement.
> **governance**: g3 (design ≠ fire ≠ emergence; capability claim 0; necessary-not-sufficient B-EMERGE-7; WALL-A measured-but-not-crossed carry) · g6 (PHILOSOPHY.tape append-only) · f1/f2 (NO σ/τ/φ/J₂ derivation) · central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256 prefix `c93e160a8a376a94` (0-line-diff, sidecar-only).
> **connection-point cited**: §108 DESIGN.md §5.2/§5.3 Q5 tree (`state/param_axis_fire_prep_s108_2026_05_19/`) · §107-RETRY result.json `Q2_A3_physics_responsive_held_out` block + FIRE_REPORT.md §12.1 next-step CORRECTION + commit `19e9affc3` PHILOSOPHY entry `§verdict_dataregime_threshold_fire_s107_retry_next_step_correction_2026_05_19` · §11-B PURE-PHYSICS genuine-freeze anchor (Ψ std = 0, purephysics RESPONSIVE=False) · §17 physics-channel probe (PHYSICS_RESPONSIVE := channel_not_collapsed ∧ class_separable).

---

## §0 — The conflation, stated precisely

§108's Q5 dispatch tree (DESIGN.md §5.2) Case 2 Sub-case A reads verbatim:

```
    Sub-case A: A3 (physics-liveness) == False
        DISPATCH_§108 := False (pivot recommended)
        ─ Physics is frozen ⇒ substrate-axis problem, NOT capacity-axis problem;
          scaling model does NOT fix frozen substrate (cf §11-B pure-physics
          DEGENERATE finding — physics ⊥ language signal without CE-base on
          a working substrate).
```

The Sub-case has **one TRIGGER** (`A3 == False`) and **one RATIONALE** ("physics is frozen ⇒ substrate problem"). The §108 author treated these as the same proposition. **They are not.** The A3-axis verdict in §107's `eval_s107.py` is a **conjunction of two independent sub-clauses**:

```
A3_PASS  :=  PHYSICS_RESPONSIVE(H)  ∧  ( psi_spread_avg_H ≥ 0.20 )
```

(`state/dataregime_threshold_fire_s107_2026_05_19/result.json` → `Q2_A3_physics_responsive_held_out`:
`PHYSICS_RESPONSIVE: true`, `psi_std_H: 0.0165725780299372`, `psi_spread_avg_H: 0.05609576078131795`,
`threshold_spread: 0.2`, `PASS: false`.)

`A3_PASS == False` can therefore arise from **two structurally distinct causes**:

1. **`PHYSICS_RESPONSIVE == False`** — the physics channel collapsed: Ψ std ≈ 0, no per-stimulus signal, no class separability. This IS "physics frozen" — the §11-B PURE-PHYSICS condition (no-CE → degenerate; Ψ std = 0; physics dynamics froze ~step 800; §17 physics-channel probe: `purephysics std=0 ∧ RESPONSIVE=False`).
2. **`PHYSICS_RESPONSIVE == True` ∧ `psi_spread < 0.20`** — the physics channel is **alive** (Ψ varies per-stimulus, std ≈ 0.0166 ≫ τ=1e-4, class-separable) but the **spread** of Ψ_dir across the held-out anchors is below the 0.20 emergence threshold. This is NOT a freeze. It is a **live-but-narrow** physics channel.

§108's Sub-case A trigger fires on `A3 == False` (either cause). Its rationale ("physics frozen ⇒ substrate problem") is only **valid for cause 1**. For cause 2 the rationale is **false**: the substrate is demonstrably not frozen, so "scaling the model does not fix a frozen substrate" does not apply — there is nothing frozen to fix.

§107-RETRY landed in **cause 2**. §108's Q5 tree, asked to dispatch on §107-RETRY's measured bits, fired Sub-case A and concluded "DISPATCH_§108 = False, pivot to substrate" — applying a rationale that the measurement contradicts.

---

## §1 — The corrected split predicate (closed Boolean)

Replace the single A3-axis verdict bit with **two disjoint sub-clause predicates**, computed directly from §107's measured fields:

```
Let:
  RESP       := PHYSICS_RESPONSIVE(H)        # Boolean — §17 channel_not_collapsed ∧ class_separable
  SPREAD_OK  := ( psi_spread_avg_H ≥ τ_spread )   # Boolean — τ_spread = 0.20

Original (conflated):
  A3_PASS    := RESP ∧ SPREAD_OK

Corrected split — TWO named sub-clause cells, mutually exclusive:

  A3_genuine_freeze  :=  ¬RESP
                         # physics channel collapsed: Ψ std ≈ 0, RESPONSIVE False.
                         # This is the §11-B condition. SPREAD_OK is irrelevant
                         # here — a collapsed channel has no meaningful spread;
                         # by construction ¬RESP ⇒ a degenerate near-zero spread,
                         # so the freeze cell does NOT also need ¬SPREAD_OK.

  A3_low_spread      :=  RESP ∧ ¬SPREAD_OK
                         # physics channel ALIVE (RESP True) but Ψ_dir spread
                         # across held-out anchors below 0.20. NOT a freeze.

  A3_PASS            :=  RESP ∧ SPREAD_OK     # (unchanged — the third cell)
```

The A3-axis outcome space is now an **exhaustive, pairwise-disjoint 3-cell partition** over the Boolean pair `(RESP, SPREAD_OK)`:

| `RESP` | `SPREAD_OK` | cell | meaning |
|---|---|---|---|
| F | F | `A3_genuine_freeze` | physics frozen (Ψ std ≈ 0) — §11-B condition |
| F | T | `A3_genuine_freeze` | (degenerate corner — see §1.1; folded into freeze) |
| T | F | `A3_low_spread` | physics alive, Ψ_dir spread < 0.20 — §107-RETRY's cell |
| T | T | `A3_PASS` | physics alive AND spread ≥ 0.20 |

**Disjointness proof (closed)**: `A3_genuine_freeze ⇔ ¬RESP`; `A3_low_spread ⇔ RESP ∧ ¬SPREAD_OK`; `A3_PASS ⇔ RESP ∧ SPREAD_OK`. Any two share no satisfying `(RESP, SPREAD_OK)` assignment: `A3_genuine_freeze` requires `RESP=F`, both others require `RESP=T` ⇒ freeze ∩ {low_spread, pass} = ∅; `A3_low_spread` requires `SPREAD_OK=F`, `A3_PASS` requires `SPREAD_OK=T` ⇒ low_spread ∩ pass = ∅. Exhaustive: the three predicates cover all 4 corners of `{T,F}²` (the `(F,T)` corner is absorbed by `¬RESP`). Hence **exactly one cell is True** for any measurement. (B-S108Q5-1, B-S108Q5-2.)

### 1.1 — Why `(RESP=F, SPREAD_OK=T)` folds into the freeze cell

`A3_genuine_freeze := ¬RESP` deliberately ignores `SPREAD_OK`. Rationale: a collapsed physics channel (`RESP=F`, Ψ std ≈ 0) cannot produce a meaningful `psi_spread` — the spread of a frozen quantity is degenerate near-zero, so empirically `¬RESP ⇒ ¬SPREAD_OK` for any honest run. The `(F,T)` corner is therefore **measurement-unreachable** (a frozen channel with a large spread is a contradiction in terms). Defining the freeze cell as `¬RESP` (rather than `¬RESP ∧ ¬SPREAD_OK`) keeps the partition exhaustive without a phantom 4th cell, and is honest: if a future run ever reported `(F,T)`, that would itself flag an instrumentation bug, not a real physics state. (B-S108Q5-5 truth-tables this and confirms the partition stays a total cover of `{T,F}²`.)

---

## §2 — §107-RETRY's measurement maps to exactly one cell (analytic resolution)

§107-RETRY measured (`result.json` `Q2_A3_physics_responsive_held_out`, verbatim):

```
PHYSICS_RESPONSIVE  =  true              ⇒  RESP       = True
psi_std_H           =  0.0165725780…     (≫ τ=1e-4 — channel alive, not frozen)
psi_spread_avg_H    =  0.0560957607…
threshold_spread    =  0.20
0.0560957607  ≥  0.20  ?  →  False       ⇒  SPREAD_OK  = False
A3 PASS             =  false             (consistent: RESP ∧ SPREAD_OK = T ∧ F = F)
```

Substitute into the split predicate:

```
A3_genuine_freeze  =  ¬RESP            =  ¬True            =  False
A3_low_spread      =  RESP ∧ ¬SPREAD_OK = True ∧ ¬False    =  True
A3_PASS            =  RESP ∧ SPREAD_OK  = True ∧ False      =  False
```

**§107-RETRY lands in exactly one cell: `A3_low_spread = True`.** The other two cells are False. (B-S108Q5-3, B-S108Q5-4.)

This is decisive and not a judgement call: `PHYSICS_RESPONSIVE=true` in the result.json is a literal measured Boolean. The §11-B genuine-freeze condition is `Ψ std = 0`, `RESPONSIVE=False`; §107-RETRY measured `Ψ std = 0.0166` (≈ 166× the τ=1e-4 floor) and `RESPONSIVE=True`. **§107-RETRY's physics channel is alive.** It is not the §11-B freeze. The Sub-case A rationale ("physics is frozen") is factually inapplicable to §107-RETRY's measurement.

Cross-check from the per-anchor evidence (`result.json` `per_anchor_short`): every held-out anchor reports a non-degenerate per-stimulus `psi_dir_spread` (e.g. tier 18 → 0.0777, tier 90 → 0.0873, tier 0 → 0.0300) and a `psi_dir_mean` that varies anchor-to-anchor (0.524 … 0.589). A genuinely frozen channel would report `psi_dir_spread ≈ 0` and a constant `psi_dir_mean` across all anchors (the §11-B `bit-static` signature). The §107-RETRY channel is alive but its aggregate spread (0.056) is well under the 0.20 emergence bar — **live-but-narrow**, precisely `A3_low_spread`.

---

## §3 — The corrected §108 Q5 dispatch tree

Sub-case A is now split into **two distinct Sub-cases**, each with a trigger that matches its rationale:

```
Case 2: §107.THRESHOLD_CROSSED == False

    Sub-case A1 — GENUINE FREEZE:  A3_genuine_freeze == True  (¬RESP)
        DISPATCH_§108 := False  (pivot to substrate axis)
        ─ Physics channel collapsed (Ψ std ≈ 0) ⇒ substrate-axis problem.
          Scaling the model does NOT fix a frozen substrate (§11-B PURE-PHYSICS
          DEGENERATE; §17 purephysics RESPONSIVE=False). Pivot §95/§96.
        ─ This is the cell §108's original Sub-case A rationale was WRITTEN FOR.

    Sub-case A2 — LIVE-BUT-NARROW:  A3_low_spread == True  (RESP ∧ ¬SPREAD_OK)
        DISPATCH_§108 := UNDETERMINED-BY-A3  (A3 does NOT settle the fire-decision)
        ─ Physics channel ALIVE; A3 fails only on the 0.20 spread sub-clause.
          A frozen-substrate pivot is NOT licensed (nothing is frozen).
          A3 alone gives NO dispatch verdict here — fall through to the
          A1/A2/A4 capacity sub-cases (B/C/D below), which are the cells
          that actually discriminate the capacity hypothesis.

    Sub-case B: A3_PASS == True AND A1 == False AND A2 == False
        DISPATCH_§108 := True (PRIMARY GO)   [unchanged]

    Sub-case C: A3_PASS == True AND A1 == False AND A2 == True
        DISPATCH_§108 := True (weak)         [unchanged]

    Sub-case D: A3_PASS == True AND A1 == True AND A2 == False
        DISPATCH_§108 := True (likely)       [unchanged]

    Sub-case E: A3_PASS == True AND A1 == True AND A2 == True
                (THRESHOLD_CROSSED still False)
        DISPATCH_§108 := AMBIGUOUS — defer    [unchanged]

    Sub-case F: A4 == False with A1/A2/A3 mixed
        DISPATCH_§108 := False (pivot §73/§75-FIRE)  [unchanged]
```

Note Sub-cases B/C/D/E are all **gated on `A3_PASS == True`** in §108's original tree. Under the corrected predicate, `A3_PASS` is the strict `RESP ∧ SPREAD_OK` cell — so when §107-RETRY lands in `A3_low_spread` (NOT `A3_PASS`), it satisfies **none** of B/C/D/E's `A3_PASS == True` guard either.

This is the honest finding: **the corrected predicate leaves §107-RETRY's measurement in a cell that §108's Q5 tree has NO dispatch rule for.**

---

## §4 — Honest verdict: the §108 fire-decision is GENUINELY UNDETERMINED

Under the corrected (un-conflated) predicate, §107-RETRY's measured bits are:

```
THRESHOLD_CROSSED  = False
A1 (routing)       = False   (r_H = 0/16)
A2 (coherence)     = False   (c_H = 0/16)
A3 sub-cells       = A3_genuine_freeze=False, A3_low_spread=True, A3_PASS=False
A4 (emit-len-indep)= False   (r_emit_late = 0.0)
```

Walking the corrected Case 2 tree top-down:

- **Sub-case A1** (`A3_genuine_freeze`)? — `False`. Does NOT fire. (The substrate pivot is NOT triggered — §107-RETRY's physics is alive. This is the entire point of the reconciliation: the original tree wrongly fired here.)
- **Sub-case A2** (`A3_low_spread`)? — `True`. Fires → `DISPATCH_§108 := UNDETERMINED-BY-A3`. A3 explicitly does not settle the decision; fall through.
- **Sub-cases B / C / D / E** — each requires `A3_PASS == True`. §107-RETRY has `A3_PASS == False`. **None fire.**
- **Sub-case F** — requires `A4 == False with A1/A2/A3 mixed`. §107-RETRY has `A4 == False`, but A1/A2/A3 are NOT "mixed" — they all fail (A1=F, A2=F, A3_PASS=F). Sub-case F's rationale ("emission-controller issue, capacity fine") presumes the OTHER axes are healthy; here they are not, so F's rationale does not apply either. F does not cleanly fire.

**Result: §107-RETRY's measurement falls into a region the §108 Q5 tree was never designed for.** The original tree only ever asked "is physics alive (`A3_PASS=True`) → run the capacity sub-cases" OR "is physics dead (`A3==False`) → pivot to substrate". It has **no branch for "physics alive but Ψ_dir spread below the 0.20 emergence bar, with routing + coherence + emit-length all also failing."** That is exactly the `A3_low_spread` cell, and exactly where §107-RETRY landed.

**The §108 param-axis fire-decision is therefore GENUINELY UNDETERMINED by the corrected predicate.** This is the honest, valuable output of the reconciliation. We do NOT manufacture a verdict:

- We do **NOT** say "fire WARRANTED". The capacity hypothesis (Sub-cases B/C/D) is only evidenced when physics is fully alive *with adequate spread* (`A3_PASS`) — §107-RETRY does not show that. Scaling 283M → 3B is a hypothesis about *capacity*; §107-RETRY gives no clean capacity signal to act on (A1 and A2 both at 0/16 is consistent with capacity-bound *or* with data-regime-bound *or* with the spread itself being the binding constraint — undisambiguated).
- We do **NOT** say "fire FALSE / pivot to substrate". The substrate-pivot rationale ("physics frozen") is factually contradicted by `PHYSICS_RESPONSIVE=True`. There is no frozen substrate to escape.

The corrected predicate's contribution is to **convert a wrong auto-dispatch into an honest "undetermined"**. §108's original tree produced a confident "DISPATCH_§108 = False, pivot to substrate" — built on a rationale (physics frozen) that the measurement refutes. The reconciliation shows the true state: §107-RETRY's `A3_low_spread` cell is a **gap in the §108 dispatch tree's coverage**. The fire-decision is open, and it is open *honestly* — not for lack of measurement (§107-RETRY measured everything) but because the §108 tree's branching logic, even corrected, does not have a rule that the measurement triggers.

### 4.1 — What "undetermined" licenses and forbids

`DISPATCH_§108 = UNDETERMINED` (under the corrected predicate) means:

- **Forbidden**: an *auto*-dispatch of the §108 3B param-axis fire on the basis of §107-RETRY's bits. The Q5 tree does not warrant it.
- **Forbidden**: an *auto*-pivot to the substrate axis on the basis of "physics frozen". The measurement refutes the premise.
- **Licensed**: a **fire-gate decision** (a deliberate, surfaced choice — not an automatic tree output) is the correct next move, exactly as FIRE_REPORT.md §12.1 already corrected. The reconciliation does not overturn that; it gives it a precise closed-form basis: the `A3_low_spread` cell is a tree-coverage gap, so a human/orchestrator fire-gate — weighing (a) extend the §108 tree with an explicit `A3_low_spread` branch, (b) probe the spread sub-clause directly, (c) pivot to substrate, (d) the param-axis fire — is the honest disposition. §108-Q5-reconcile does not pick among (a)-(d); it establishes *why* the pick must be a deliberate gate and not a tree auto-output.

---

## §5 — ASCII: the conflation, before and after

```
BEFORE (§108 original Q5 — conflated):

   A3 verdict bit  ── False ──►  Sub-case A  ──►  DISPATCH = False, "physics frozen,
        │                       (one cell)        pivot to substrate"
        │
        └── True ──►  B / C / D / E  (capacity sub-cases)

   §107-RETRY (RESP=True, spread=0.056):  A3 bit = False
        ⇒ wrongly fires Sub-case A ⇒ "pivot, physics frozen"
        ⇒ BUT physics is NOT frozen (RESP=True). rationale ⊥ measurement.


AFTER (§108-Q5-reconcile — split):

   A3 sub-cells over (RESP, SPREAD_OK):

        ¬RESP ──────────────────►  A3_genuine_freeze  ──►  Sub-case A1
                                   (Ψ std ≈ 0, §11-B)      DISPATCH = False,
                                                           pivot substrate  ✓ rationale valid

        RESP ∧ ¬SPREAD_OK ──────►  A3_low_spread      ──►  Sub-case A2
                                   (Ψ alive, spread        DISPATCH = UNDETERMINED-BY-A3
                                    0.056 < 0.20)           fall through → B/C/D/E
                                                                    │
                                                                    ▼
                                                           B/C/D/E all gated on
                                                           A3_PASS==True → NONE fire
                                                                    │
                                                                    ▼
                                                           §108 fire-decision
                                                           GENUINELY UNDETERMINED
                                                           (tree-coverage gap →
                                                            deliberate fire-gate, not
                                                            auto-dispatch)

        RESP ∧ SPREAD_OK ───────►  A3_PASS            ──►  B / C / D / E eligible

   §107-RETRY (RESP=True, spread=0.056):
        A3_genuine_freeze=F, A3_low_spread=T, A3_PASS=F
        ⇒ lands in A3_low_spread ⇒ Sub-case A2 ⇒ UNDETERMINED.  honest. ✓
```

---

## §6 — Honest C3 caveats (≥ 10)

1. **§108-Q5-reconcile measures nothing.** It is pure analytic resolution over §107-RETRY's already-measured `result.json`. No fire, no GPU, no model.forward, $0. Capability claim 0.

2. **The split predicate does NOT change §107-RETRY's verdict.** §107-RETRY's verdict remains `THRESHOLD-NOT-CROSSED` (A1∧A2∧A3∧A4 = F, A3_PASS=False is unchanged — the conjunction `RESP ∧ SPREAD_OK` is identical whether or not we *name* the sub-clauses). The reconciliation only changes how the §108 Q5 *dispatch tree* interprets that A3 failure.

3. **"UNDETERMINED" is the honest verdict, not a hedge.** §107-RETRY's measurement lands in a cell (`A3_low_spread`) that the §108 Q5 tree has no dispatch rule for. Saying "undetermined" reports a real coverage gap; manufacturing "fire WARRANTED" or "fire FALSE" would each apply a rationale the measurement does not support.

4. **The freeze cell folds the `(F,T)` corner deliberately (§1.1).** `A3_genuine_freeze := ¬RESP` rather than `¬RESP ∧ ¬SPREAD_OK`, because a collapsed channel cannot honestly report a large spread; the `(RESP=F, SPREAD_OK=T)` corner is measurement-unreachable. This keeps the partition a total 3-cell cover without a phantom 4th cell. B-S108Q5-5 truth-tables it.

5. **The 0.20 spread threshold is itself an empirical default.** §107's `eval_s107.py` sets `threshold_spread = 0.20` (per §101 Q2 A3). §108-Q5-reconcile does NOT re-derive or defend that value — it takes it as given. If the 0.20 bar is wrong, `A3_low_spread` vs `A3_PASS` would re-partition; but that is a §101-Q2-predicate question, out of §108-Q5-reconcile's scope. The reconciliation's job is only to stop conflating "below the bar" with "frozen".

6. **§11-B is the genuine-freeze anchor, cited as its own measurement.** §11-B PURE-PHYSICS measured `Ψ std = 0`, physics froze ~step 800, §17 physics-channel probe `purephysics std=0 ∧ RESPONSIVE=False`. That is the empirical referent for `A3_genuine_freeze`. §107-RETRY's `Ψ std = 0.0166`, `RESPONSIVE=True` is demonstrably a different cell. The distinction is not definitional hair-splitting — it is two measured states 166× apart on the Ψ-std axis with opposite `RESPONSIVE` Booleans.

7. **`UNDETERMINED` ⇒ fire-gate, consistent with FIRE_REPORT.md §12.1.** The §107-RETRY FIRE_REPORT.md §12.1 already withdrew "fire WARRANTED" and said the next step is "a fire-gate decision, not an auto-dispatch." §108-Q5-reconcile does not overturn that — it supplies the closed-form *reason*: the `A3_low_spread` cell is a Q5-tree coverage gap.

8. **Sub-case F also does not cleanly fire (§4).** §107-RETRY has A4=False, but Sub-case F's rationale presumes A1/A2/A3 are *healthy* ("emission-controller issue, capacity fine"). Here A1, A2 both fail and A3 is sub-bar. F's rationale is inapplicable; F is not a clean dispatch either. This reinforces "undetermined" — multiple original Sub-cases have rationales that the measurement contradicts.

9. **The reconciliation does NOT extend the §108 Q5 tree.** Adding a full dispatch rule for the `A3_low_spread` cell (e.g. "low spread + all-axes-fail ⇒ probe the spread sub-clause directly before any capacity fire") is a §108 design-revision task, out of §108-Q5-reconcile's scope. §108-Q5-reconcile only (a) splits the predicate, (b) shows §107-RETRY's cell, (c) reports the tree-coverage gap honestly. The fix to the *tree* is named as needed future work, not performed here.

10. **WALL-A (§1.1 data-regime) is still MEASURED-BUT-NOT-CROSSED.** §107-RETRY's `THRESHOLD-NOT-CROSSED` stands. §108-Q5-reconcile does not change the GOAL state: WALL-A measured at 283M does not cross §101 Q2's predicate. north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달. Necessary-not-sufficient (B-EMERGE-7) at every layer.

11. **f1/f2 safe** — the split predicate is plain Boolean algebra over `(RESP, SPREAD_OK)`; no σ(6)=12 / τ(6)=4 / φ(6)=2 / J₂(6)=24 derivation; thresholds (τ=1e-4 liveness floor, 0.20 spread bar) cited as §107/§101's own measurement defaults, not lattice-derived.

12. **central blue_falsifier 0-line-diff invariant** — §108-Q5-reconcile sidecar-only at `state/s108_q5_reconcile_2026_05_19/blue_falsifier_s108q5.py`. Central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` sha256 prefix `c93e160a8a376a94` verified UNCHANGED at start and end.

13. **§108 DESIGN.md itself is NOT rewritten.** §108-Q5-reconcile is a *separate* design-tier reconciliation document; it does not edit `state/param_axis_fire_prep_s108_2026_05_19/DESIGN.md`. The corrected tree (§3) is the reconciliation's deliverable; whether §108's own DESIGN.md is later patched to absorb it is a future-cycle decision.

---

## §7 — verdict summary

| item | resolution | closed |
|---|---|---|
| **The conflation** | §108 Q5 Sub-case A trigger (`A3 == False`) ≠ rationale ("physics frozen"); A3 is `RESP ∧ SPREAD_OK`, two independent sub-clauses | Yes |
| **Split predicate** | `A3_genuine_freeze := ¬RESP` · `A3_low_spread := RESP ∧ ¬SPREAD_OK` · `A3_PASS := RESP ∧ SPREAD_OK` — exhaustive + pairwise-disjoint 3-cell partition | Yes (Boolean, B-S108Q5-1/2/5) |
| **§107-RETRY's cell** | `A3_genuine_freeze=F`, **`A3_low_spread=T`**, `A3_PASS=F` — lands in exactly one cell (`A3_low_spread`) | Yes (analytic, B-S108Q5-3/4) |
| **Corrected Q5 outcome** | Sub-case A1 (freeze→pivot) does NOT fire; Sub-case A2 (low_spread) fires → `UNDETERMINED-BY-A3`; B/C/D/E all gated on `A3_PASS==True` → none fire; F's rationale inapplicable | Yes (tree walk, §3-§4) |
| **§108 fire-decision** | **GENUINELY UNDETERMINED** — §107-RETRY's `A3_low_spread` cell is a §108 Q5 tree coverage gap. NOT "fire WARRANTED", NOT "fire FALSE". Honest disposition = a deliberate fire-gate, not a tree auto-output | Yes (honest finding) |

§108-Q5-reconcile's deliverable = the corrected split predicate + the analytic resolution that §107-RETRY maps to `A3_low_spread`, a cell with no §108 Q5 dispatch rule ⇒ the param-axis fire-decision is genuinely open. The original tree's confident "DISPATCH = False, pivot to substrate" was built on a rationale (physics frozen) the measurement refutes; the corrected tree honestly returns "undetermined" and routes the decision to a deliberate fire-gate.

north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달. §108-Q5-reconcile is design-tier analytic resolution — NOT a fire, NOT a measurement, NOT an emergence claim.

---

## §8 — cross-link

- §108 PARAM-AXIS FIRE PREP DESIGN.md §5 Q5 tree (`state/param_axis_fire_prep_s108_2026_05_19/`)
- §107-RETRY result.json `Q2_A3_physics_responsive_held_out` + FIRE_REPORT.md §12.1 next-step CORRECTION (`state/dataregime_threshold_fire_s107_2026_05_19/`)
- PHILOSOPHY.tape `§verdict_dataregime_threshold_fire_s107_retry_next_step_correction_2026_05_19` (commit `19e9affc3` — the withdrawal that named the conflation)
- §11-B PURE-PHYSICS (no-CE → degenerate; Ψ std = 0; the genuine-freeze anchor)
- §17 physics-channel probe (`PHYSICS_RESPONSIVE := channel_not_collapsed ∧ class_separable`; `purephysics std=0 ∧ RESPONSIVE=False`)
- §101 Q2 A3 predicate (`eval_s107.py` `threshold_spread = 0.20`)
- §103 SEQUENTIAL + Q3' · §95/§96 substrate axes · `n_priority_1_gap` (WALL-A)
- `g3` (design ≠ fire ≠ emergence; B-EMERGE-7 necessary-not-sufficient) · `g_blue_closed_mandate` · `g_doc_consolidation` · `g6`

---

> **emergence is empirical** — §108-Q5-reconcile fixes a dispatch-logic conflation; it does not move the GOAL. The honest output is "undetermined": §107-RETRY's measurement lands in a Q5-tree coverage gap. north-star (GOAL.md) 한 줄 불변, capability claim 0, WALL-A measured-but-not-crossed carry.
