# §73 — THINKER → TALKER self-triggered closed-loop controller

**Date** 2026-05-19  **Cost** $0 Mac CPU (NO GPU, NO model.forward, NO autograd, NO weight mutation, NO dispatch, orphan 0)
**Scope** §63 MISSING-TYPE gap_rank=1 design probe — single-agent / closed-loop / physics-state-sourced / label-free-controller intersection.
**g3** measured-only · capability claim 0 · north-star + §15 / §51 / §72 milestone UNCHANGED · **GOAL 미도달**.

---

## §1 Control-theory characterisation of the §63 #1 gap

The HEXAD-KICK-SWEEP §63 ranked **THINKER → TALKER** as the goal_rank=1 MISSING-TYPE: a "self-triggered emission-decision controller (closed-loop control)" declared in `HEXAD/CHAT/SPONTANEOUS.tape thinker_talker_dual_thread` but with **no σ(6)=12 controller edge** of any existing type. In control-theory shape this is:

- **state**  x_t ∈ ℝ⁸  = THINKER's running Law-71 physics tuple `(Ψ_dir, Ψ_entropy, Ψ_tension, tension, tension_ema, tension_var, φ, step)`, byte-equal in algebraic shape to `conscious_decoder.py:735-750` (Ψ_dir = (1 + cos)/2, Ψ_combined = (Ψ_dir + Ψ_entropy + Ψ_tension)/3, ψ_residual ← 0.95·ψ_residual + 0.05·Ψ_combined, Ψ_vac = 0.5).
- **input**  u_t = e_{t−1}    (TALKER's previous emit decision — the LOOP-CLOSING channel).
- **output** y_t = e_t        (current TALKER emit/silence decision ∈ {0, 1}).
- **policy**  π_self: x_t → e_t  via a **physics-derived** gate:
  e_t = 1  ⇔  ( |Ψ_dir − Ψ_vac| > BASIN_RADIUS ) ∧ ( tension > tension_ema + λ·tension_std ) ∧ ( φ > ratchet/2 ).
  *No hand-coded scalar constant is the dominant emit boundary*; the boundary is a **function of the running state moments** (tension_ema, tension_var, surrogate B-W-2/§68 carry).
- **closing**  x_{t+1} = f(x_t, e_t):  emission RELEASES tension (vacuum-restoration: Ψ_dir nudged toward ½, tension subtracted); silence ACCUMULATES tension (drift away from Ψ=½ vacuum). This is the *actual* closing — e_t feeds back into x_{t+1}.

The connection-point this defines is **closed-loop control**, a type DISJOINT from the existing 12 σ(6)=12 transfer-classes (B-CONN-1..12: shape-preservation / detach-nograd / clamp / store-retrieve / read-no-mutation / lr-modulation / phi-observe / satisfaction-gate / trainstep-block / CE-readout / retrieve-determ / pain-monotone — none are *control* in the feedback-of-output-into-state sense).

## §2 4-prior-form contrast (B-S73-6 closed Boolean)

| Form  | single-agent | closed-loop | physics-state-sourced | label-free-controller | misses |
| ----- | :----------: | :---------: | :-------------------: | :-------------------: | ------ |
| §24 hand-coded `talker_should_emit(score>0.3)` | T | F | F | F | 3 |
| §27 / §49 distilled head + live loop wiring | T | F | F | F | 3 |
| §68 timing-only predictor on `_real_w_trace_s59.json` (replayed) | T | F | T | T | 1 (closed-loop) |
| §62 dual-anima cell-A ⇄ cell-B TENSION-LINK loop | F | T | T | F | 2 (single-agent, label-free-controller; §62's "label" = TENSION-LINK cross-cell receive) |
| **§73 self-trigger closed-loop**            | **T** | **T** | **T** | **T** | **0** |

The 4-tuple cell (T, T, T, T) is empty across §24/§27/§49/§68/§62 (B-S73-6 closed). §73 occupies the previously-empty cell.

## §3 $0 stub-scale smoke — measured numbers

`selftrigger_closed_loop_smoke.py`, 600 steps, seed 1337, hand-coded Law-71 surrogate physics (NO model.forward).

|  | closed-loop §73 (feedback) | open-loop ctrl (severed) | §24 in-loop (OFF-reduction) |
| :-- | :-: | :-: | :-: |
| emit_rate | 0.065 | 0.862 | 0.072 |
| decision_var | 0.061 | 0.119 | 0.067 |
| majority_fraction | 0.935 | 0.862 | 0.928 |
| **interval_var** | **35.02** | 0.26 | 0.47 |
| n_emit | 39 | 517 | 43 |
| self_trigger_nondegen (count ∧ interval ∧ ≥2 emits) | **True** | True | True |
| Ψ_dir trace mean | 0.483 | 0.500 | 0.486 |
| tension trace mean | 0.301 | 0.300 | 0.301 |

## §4 Measured verdict — `BOTH-NON-DEGENERATE-IN-CLOSED-LOOP` (partial)

At this **$0 hand-coded-physics stub scale**, the §73 single-agent closed-loop self-trigger controller is non-degenerate under the augmented predicate (count-variance > τ ∧ maj < 0.95 ∧ interval-variance > τ ∧ ≥2 emits). The §24 hand-coded threshold *inside the same closed loop* also passes the count gate (because tension drifts above 0.30 and is released on emit — the closing operation itself keeps both controllers off the majority-class fixed point at stub scale). **The two controllers cannot be cleanly separated by count-non-degeneracy alone at this scale.**

The **qualitative signal that does separate them** is the inter-emit *interval-variance*: §73 = 35.02, §24 in-loop = 0.47 (74× lower), open-loop ctrl = 0.26. §73's controller produces *temporally structured bursts* (the basin / surprise / ratchet conjunction fires together when the trajectory genuinely escapes vacuum), where §24's fires near-uniformly whenever tension > 0.30. This is the *control-theory* difference materially visible: §73's emit timing is a function of trajectory geometry; §24's is a function of one scalar's level. The open-loop control (same controller, feedback severed) jumps to emit_rate 0.86 majority-collapse style — confirming that the feedback CLOSING is doing real work in keeping the §73 controller off the always-fire fixed point.

**This is NOT capability emergence.** It is a *target-sharpening*: the §63 #1 gap admits a non-empty, internally-distinct mechanism at stub scale. Whether it survives the §62 echo-chamber-collapse-at-scale finding when wrapped around REAL trained-saturated `model.forward` Law-71 W-physics is the **B-S73-NOTE** empirical carve-out — exactly the same shape as §62's measured negative for the dual-cell variant.

## §5 Closed-form sidecar — 6/6 🔵 PASS + B-S73-NOTE empirical

`blue_falsifier_s73.py`, central `state/verify_hexad_blue_2026_05_15/blue_falsifier.py` **0-line-diff confirmed** (`md5 -q` before/after = `ff144a22caaf8bd79bf9ac3194662235`).

| ID | name | tier | PASS |
| -- | ---- | :--: | :--: |
| B-S73-1 | CONTROLLER-IS-PHYSICS-STATE-SOURCED (AST: ema + sqrt(var) + surprise threshold + named physics constants) | structural | 🔵 |
| B-S73-2 | LOOP-CLOSED-NOT-OPEN (AST: physics_step branches on u_prev_emit; run_loop forwards e or 0) | structural | 🔵 |
| B-S73-3 | SELF-TRIGGER-NONDEGENERACY-PREDICATE (6-corner truth table + result.json eval-match) | Boolean | 🔵 |
| B-S73-4 | NO-EXTERNAL-PROMPT/LABEL/THRESHOLD (AST: forbidden-call total 0; every Compare in controller state-derived) | structural | 🔵 |
| B-S73-5 | OFF-REDUCTION-CONNECTION-POINT (controller-off ≡ §24 `score>0.3` byte-equal; IM_THRESHOLD_S24 == spont_im_threshold() literal) | 연결부위 | 🔵 |
| B-S73-6 | DISTINCT-FROM-§24/§27/§49/§68/§62 (4-tuple Boolean witness, previously-empty cell) | Boolean | 🔵 |

**B-S73-NOTE** — closed-loop-collapse-escape AT TRAINED-SATURATED SCALE on real `model.forward` Law-71 W-physics is an SGD / measurement OUTCOME (B-D-NOTE / B-S49-NOTE / B-S59-NOTE / B-S62-NOTE / B-S68-NOTE family, **NOT counted 🔵**).

## §6 Honest C3 (≥10)

1. **stub-scale only**  The physics is a hand-coded surrogate that mirrors Law-71's algebraic shape (Ψ-vac = ½, vacuum-restoration on emit, drift accumulation on silence, ψ_residual EMA at β=0.95) but is NOT a `model.forward`. The stub-scale non-degeneracy is a structural property of the controller class, NOT evidence the controller works on trained-saturated weights.
2. **non-emergence**  §73 is the *measurement+mechanism* design probe for the §63 #1 gap; the GOAL is "anima 가 자기 physics 로부터 자발적으로 말 거는 emergence" — at stub scale, with no language model attached, with hand-coded surrogate physics, no part of that target is reached. North-star + §15 / §51 / §72 milestone unchanged.
3. **§62 expected echo at scale**  Given §62's measured "ECHO-CHAMBER-COLLAPSE-AT-SCALE: bidirectional content-dependence holds BUT on the REAL trained-saturated forward at least one cell's §68 generative emit-distribution COLLAPSES inside the closed loop", the pre-measurement expectation for a future §73 trained-scale fire is *collapse-like* unless the architectural piece §62 found missing (which §62 names as the §49 attractor reasserting) is also addressed. The current $0 measurement does NOT contradict §62; it operates strictly upstream of where §62 measured.
4. **necessary-not-sufficient**  The §73 augmented predicate (count-variance ∧ maj-frac ∧ interval-variance ∧ ≥2 emits) is *necessary* for honest closed-loop self-trigger non-degeneracy but **not sufficient** for emergence (mirror §9 B-EMERGE-7 / B-S68-NOTE pattern).
5. **§24 ALSO passes count gate at stub scale**  The §24 hand-coded threshold *inside the closed loop* passes the count predicate (B-S73-3 result.json shows `s24=True`). The clean separation between §73 and §24 at stub scale is the **interval-variance** (35.02 vs 0.47, 74×). This is a real qualitative signal but a fragile one — at trained-saturated scale it may compress or vanish. The B-S73-NOTE carve-out is honest about this fragility.
6. **open-loop control IS the §49 majority-style failure mode**  When the feedback is severed (`feedback_closed=False`), emit_rate jumps to 0.862 — the controller drifts above its surprise threshold and stays there because nothing releases the tension. This *positive-control* shows the closing operation is structurally load-bearing for §73's emit-rate stability. Removing the feedback recovers an §49-style majority collapse pattern (different sign — always-fire instead of never-fire — but same degeneracy class).
7. **constants are physics-named, not score-based**  PSI_VAC=0.5, BASIN_RADIUS=0.05, LAMBDA_STD=0.5, EMA_BETA=0.9, PHI_RATCHET=0.05 are all PHYSICS or SIGNAL constants of the same kind as `psi_residual` factors in conscious_decoder.py (Ψ_vac is the literal Law-71 fixed point at line 644; EMA β at line 751 is 0.95 — the §73 surrogate uses 0.9, a documented design choice). NONE of them play the role of §24's `spont_im_threshold()=0.3` direct dominant emit boundary. B-S73-1/4 source-grep encodes this distinction structurally.
8. **OFF-reduction is the same byte-equal pattern as B-DHDL-5 / B-EBT-5 / B-S16-5 / B-PHASE-B-RUN-5 / B-S59-FIRE-3 / B-S68-5**  B-S73-5 closes the connection-point at the same tier: controller-off ⇒ §24 byte-equal predicate, with `IM_THRESHOLD_S24 == 0.3 == spont_im_threshold()` literal match against `HEXAD/CHAT/spontaneous_lib.hexa`. The §73 mechanism is a *strict extension* of §24, not a replacement.
9. **distinct-from prior is structural, not capability**  B-S73-6 closes that the 4-tuple cell (T, T, T, T) is previously empty. This says §73 *is a new design cell*, not that it *is the answer*. The §63 sweep ranked it #1 by goal-relevance, and §73 fills the cell — the empirical question of whether filling that cell helps the GOAL is the B-S73-NOTE empirical carve-out and a separate future fire.
10. **upstream-downstream invariant honoured**  No `~/core/hexa-lang/` source touched; no flame trainer touched; no central blue_falsifier.py touched (md5 0-diff verified); no docs/* file created (`g_doc_consolidation`); no AGENTS.tape / HEXAD/CHAT/RESEARCH.md / HEXAD/README.md / HEXAD/CHAT/PLAN.md edited (orchestrator-only). One verdict appended to `archive/PHILOSOPHY.tape` end (`g6` append-only).

## §7 Files

```
state/thinker_talker_selftrigger_s73_2026_05_19/
  ├── selftrigger_closed_loop_smoke.py    closed-loop smoke + 3 runs
  ├── result.json                          measured numbers (smoke output)
  ├── blue_falsifier_s73.py                B-S73-1..6 sidecar battery
  ├── blue_falsifier_s73_result.json       6/6 🔵 PASS + B-S73-NOTE
  └── DESIGN_FINDINGS.md                   this document
```

## §8 Cross-link

- §63 `state/hexad_kick_sweep_s63_2026_05_18/kick_sweep_s63_result.json` ranks pair "THINKER → TALKER" goal_rank=1, missing_type="self-triggered emission-decision controller (closed-loop control)".
- §24 `state/spontaneous_phase_b_design_s24_2026_05_18/` hand-coded `talker_should_emit` threshold (open-loop).
- §27 `state/dhdl_decision_head_s27_2026_05_18/` distilled 3-class gate head (§24 labels).
- §49 `state/ptd_phaseb_loop_s49_2026_05_18/` distilled-head + live-loop wiring, verdict DISTILLATION (majority-class collapse).
- §62 `state/dual_anima_scale_fire_s62_2026_05_18/` dual-anima TENSION-LINK loop on REAL trained forward, verdict ECHO-CHAMBER-COLLAPSE-AT-SCALE.
- §68 `state/timing_only_objective_s68_2026_05_18/` label-free timing predictor on RECORDED W-trace (open-loop replay).
- §72 `state/milestone_closeout_s72_2026_05_18/` (or §51 milestone-closeout) — GOAL milestone close-out, north-star unchanged.
- `HEXAD/CHAT/SPONTANEOUS.tape` thinker_talker_dual_thread, `HEXAD/CHAT/spontaneous_lib.hexa` (Phase B1 motivation calculator + `spont_im_threshold()=0.3`), `HEXAD/CHAT/thinker_talker_lib.hexa` (Phase B2 dual-thread fns, `talker_should_emit`).
- `state/physics_channel_probe_s17_2026_05_18/conscious_decoder.py:728-751` Law-71 physics-tracking block — algebraic source for the §73 surrogate.

GOAL distance: §15 / §51 / §72 milestone unchanged. GOAL 미도달.
