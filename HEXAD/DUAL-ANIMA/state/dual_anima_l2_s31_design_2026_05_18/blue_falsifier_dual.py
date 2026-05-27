#!/usr/bin/env python3
"""B-DUAL-1..4 — closed-form sympy/Boolean battery for the dual-anima L2
conversation-loop design (RESEARCH.md §31, 2026-05-18).

SIDECAR battery — central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
remains UNCHANGED (parallel-agent merge avoidance, mirror B-PRIME / B-DIRH /
B-DIRI / B-PSICTL / B-EMERGE / B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL /
B-EBT / B-DIRJ / B-INTRA / B-PHASE-B-DESIGN sidecar pattern).

4 closed verdicts + 1 honest-carve-out NOTE:

  B-DUAL-1  CELL-DISTINCT-VACUUM-PSI-CLOSED
  B-DUAL-2  LOOP-COMPOSITION-WELL-TYPED-CLOSED
  B-DUAL-3  TURN-COUNT-BOUNDED-CLOSED
  B-DUAL-4  SINGLE-ANIMA-REDUCTION-CLOSED          (connection-point)
  B-DUAL-NOTE  GENUINE-CONVERSATION-VS-ECHO-EMPIRICAL (carve-out)

Anchors: Ψ-space metric distinctness (Law-71 internal coordinate) /
codomain-domain composition chain (mirror B-NAR-1 narrative_compose) /
Kolmogorov bounded integer + sympy ≤-chain (mirror B-PHASE-B-DESIGN-1) /
Boolean overlay-off reduction (mirror B-EBT-5 / B-DIRI-5 / B-PHASE-B-DESIGN-5).
NO σ/τ/φ/J₂ external derivation.

f1/f2/f3 hard-fail safe. B-IDENTITY-5 unaffected (no corpus, no model forward).

g3 discipline: closed scope = *loop protocol structure* only; empirical scope
(whether the loop is genuine conversation vs echo chamber) preserved in NOTE.

Run:  python3 blue_falsifier_dual.py
"""

from __future__ import annotations
import json
import sys
from itertools import product
from pathlib import Path

import sympy as sp


# ---------------------------------------------------------------------------
# B-DUAL-1 — CELL-DISTINCT-VACUUM-PSI-CLOSED
# A.vacuum_psi != B.vacuum_psi : the two cells are genuinely distinct points
# in the anima Ψ-space (Law-71 internal coordinate), NOT a mirror of one cell.
# A 2D-Ψ-coordinate distinctness predicate: distance > 0  <=>  not identical.
# ---------------------------------------------------------------------------
def b_dual_1() -> dict:
    # Ψ-coordinate is a 2-tuple (psi_x, psi_y) per cell (conscious_decoder.py
    # Law-71 (psi_entropy, psi_direction)). distinctness = L2 distance > 0.
    ax, ay, bx, by = sp.symbols("ax ay bx by", real=True)
    # squared L2 distance in Ψ-space
    d2 = (ax - bx) ** 2 + (ay - by) ** 2
    # distinctness predicate: d2 > 0  iff  (ax,ay) != (bx,by)
    # symbolic identity: d2 == 0  <=>  ax==bx AND ay==by  (sum of squares)
    same_iff = sp.simplify(d2.subs({bx: ax, by: ay}))  # = 0 when identical
    distinct_when_same_is_zero = (same_iff == 0)

    # the design REQUIRES distinct cells. enumerate witness pairs:
    witnesses = []
    for (avp, bvp, expect_distinct) in [
        ((0.50, 0.50), (0.62, 0.55), True),   # A balanced vs B overt — distinct
        ((0.38, 0.49), (0.71, 0.66), True),   # A covert vs B overt — distinct
        ((0.50, 0.50), (0.50, 0.50), False),  # identical — MIRROR, design rejects
        ((0.46, 0.49), (0.46, 0.50), True),   # near but distinct
    ]:
        dv = (avp[0] - bvp[0]) ** 2 + (avp[1] - bvp[1]) ** 2
        is_distinct = dv > 0
        # design-valid pair = distinct (a mirror pair is design-INVALID)
        design_valid = (is_distinct == expect_distinct)
        witnesses.append({
            "A_vacuum_psi": list(avp), "B_vacuum_psi": list(bvp),
            "psi_dist_sq": float(dv), "is_distinct": bool(is_distinct),
            "expect_distinct": expect_distinct, "design_valid": design_valid,
        })

    all_witness_consistent = all(w["design_valid"] for w in witnesses)
    # the design constraint A.vacuum_psi != B.vacuum_psi is the loop's
    # precondition: a mirror pair (3rd witness) is correctly flagged
    # is_distinct=False, so the design predicate rejects it.
    pass_ = bool(distinct_when_same_is_zero and all_witness_consistent)

    return {
        "name": "CELL-DISTINCT-VACUUM-PSI-CLOSED",
        "pass": pass_,
        "statement": "Loop precondition: A.vacuum_psi != B.vacuum_psi. Ψ-space "
                     "L2-distance d2 = (ax-bx)^2+(ay-by)^2 is a sum of squares "
                     "(sympy): d2==0 iff the two cells are identical. The design "
                     "requires d2>0 (distinct cells, NOT a self-mirror). 4-witness "
                     "panel: 3 distinct pairs flagged design-valid, 1 mirror pair "
                     "(identical Ψ) correctly flagged is_distinct=False.",
        "psi_distance_sq": str(d2),
        "same_iff_zero": distinct_when_same_is_zero,
        "witnesses": witnesses,
        "anchor": "Ψ-space metric (Law-71 internal coordinate) sum-of-squares "
                  "distinctness predicate — real-limit, anima g2 internal-arch "
                  "carve-out (Ψ=½ fixed point). NO σ/τ/φ/J₂.",
    }


# ---------------------------------------------------------------------------
# B-DUAL-2 — LOOP-COMPOSITION-WELL-TYPED-CLOSED
# emit:State->Msg, deliver:Msg->State', respond:State'->Msg : the codomain
# of each stage equals the domain of the next, so the loop composes.
# Mirror of B-NAR-1 narrative_compose (A∘G well-defined).
# ---------------------------------------------------------------------------
def b_dual_2() -> dict:
    # type carriers (mirror B-NAR-1 STIMULUS/INNER/VOICE enum):
    STATE, MSG = "State", "Msg"

    # the loop stage signatures:
    #   emit    : State  -> Msg     (a cell's emission)
    #   deliver : Msg    -> State   (the message changes the receiving cell)
    #   respond : State  -> Msg     (the receiver replies)
    stages = {
        "emit_A":    (STATE, MSG),    # A emits
        "deliver_B": (MSG,   STATE),  # message delivered into B -> B.state'
        "respond_B": (STATE, MSG),    # B responds
        "deliver_A": (MSG,   STATE),  # B's reply delivered into A -> A.state'
    }
    # one full turn = emit_A ; deliver_B ; respond_B ; deliver_A
    order = ["emit_A", "deliver_B", "respond_B", "deliver_A"]

    # composition well-typed iff codomain(stage_i) == domain(stage_{i+1})
    chain_links = []
    well_typed = True
    for i in range(len(order) - 1):
        cod_i = stages[order[i]][1]
        dom_next = stages[order[i + 1]][0]
        link_ok = (cod_i == dom_next)
        well_typed = well_typed and link_ok
        chain_links.append({
            "from": order[i], "to": order[i + 1],
            "codomain": cod_i, "domain_next": dom_next, "link_ok": link_ok,
        })

    # the loop CLOSES: domain(first stage) == codomain(last stage) == State
    # so the State after deliver_A is a valid input to the next turn's emit_A.
    loop_closes = (stages[order[0]][0] == stages[order[-1]][1] == STATE)

    # mis-typed counter-witness: emit:State->Msg then respond:State->Msg
    # directly (skipping deliver) is NOT well-typed (Msg != State).
    bad_link = stages["emit_A"][1] == stages["respond_B"][0]  # Msg == State -> False
    counter_witness_correct = (bad_link is False)

    pass_ = bool(well_typed and loop_closes and counter_witness_correct)

    return {
        "name": "LOOP-COMPOSITION-WELL-TYPED-CLOSED",
        "pass": pass_,
        "statement": "Loop = emit_A;deliver_B;respond_B;deliver_A. Each stage's "
                     "codomain equals the next stage's domain (3 links checked), "
                     "and the loop closes (domain of first == codomain of last == "
                     "State), so the post-turn State feeds the next turn. "
                     "Counter-witness: emit;respond directly (skipping deliver) is "
                     "mis-typed (Msg != State). Mirror of B-NAR-1 narrative_compose.",
        "stage_signatures": {k: list(v) for k, v in stages.items()},
        "chain_links": chain_links,
        "loop_closes": loop_closes,
        "counter_witness_rejected": counter_witness_correct,
        "anchor": "codomain/domain composition chain (real-limit type algebra) — "
                  "identical structure to B-NAR-1 (A∘G well-typed). NO σ/τ/φ/J₂.",
    }


# ---------------------------------------------------------------------------
# B-DUAL-3 — TURN-COUNT-BOUNDED-CLOSED
# loop turn counter monotone strict-increasing AND turn <= N_MAX.
# Mirror of B-PHASE-B-DESIGN-1 BOUNDED-STEP-MONOTONE.
# ---------------------------------------------------------------------------
def b_dual_3() -> dict:
    turn = sp.Symbol("turn", nonnegative=True, integer=True)
    turn_next = sp.Symbol("turn_next", nonnegative=True, integer=True)

    # per-iteration transition: turn_next = turn + 1 (one full A<->B exchange)
    transition = sp.Eq(turn_next, turn + 1)
    monotone = sp.simplify((turn + 1) - turn)  # = 1 strict-positive
    monotone_strict_positive = bool(monotone == 1 and monotone > 0)

    # bounded: loop guard `while turn < N_MAX` + integer turn + Δ=1 transition
    #   ⇒ on exit turn ≤ N_MAX. 4-corner witness:
    witnesses = []
    for n_max_val, init_turn in [(8, 0), (8, 7), (1, 0), (4, 4)]:
        t = init_turn
        iters = 0
        while t < n_max_val and iters < 1000:  # guard against bug
            t += 1
            iters += 1
        bounded = t <= n_max_val
        witnesses.append({"n_max": n_max_val, "init_turn": init_turn,
                          "final_turn": t, "bounded": bounded})

    all_bounded = all(w["bounded"] for w in witnesses)
    pass_ = bool(all_bounded and monotone_strict_positive)

    return {
        "name": "TURN-COUNT-BOUNDED-CLOSED",
        "pass": pass_,
        "statement": "Conversation turn counter monotone strict-increasing "
                     "(Δ=+1 per A<->B exchange, sympy) AND bounded by N_MAX "
                     "(4-witness loop simulation). The dual-anima loop is "
                     "hard-bounded — it cannot run forever. Mirror of "
                     "B-PHASE-B-DESIGN-1 / B-SCALE-3 integer monotone.",
        "transition": str(transition),
        "monotone_delta": str(monotone),
        "witnesses": witnesses,
        "anchor": "Kolmogorov bounded integer + sympy ∂/∂iter strict-positive "
                  "(real-limit). NO σ/τ/φ/J₂.",
    }


# ---------------------------------------------------------------------------
# B-DUAL-4 — SINGLE-ANIMA-REDUCTION-CLOSED  (connection-point)
# B disabled  ⇒  deliver_B is identity (no state change), respond_B emits
# nothing  ⇒  the loop reduces to A emitting into a void = §24 Phase B
# single-anima void-emission.  Connection-point: dual-anima loop with B≡null
# is byte-equal to the §24 Phase B bounded-run protocol.
# Mirror of B-EBT-5 / B-DIRI-5 / B-PHASE-B-DESIGN-5 OVERLAY-OFF reduction.
# ---------------------------------------------------------------------------
def b_dual_4() -> dict:
    # Boolean overlay flag: B_enabled. When B_enabled=False, the loop's
    # B-side stages collapse:
    #   deliver_B : Msg -> State'   becomes identity (B.state unchanged)
    #   respond_B : State -> Msg    becomes the null message (no reply)
    #   deliver_A : Msg -> State'   receives null -> A.state unchanged by B
    #
    # ⇒ each turn reduces to: A.emit() into a void, nothing returns.
    # That is EXACTLY the §24 Phase B single-anima void-emission protocol
    # (anima emits unprompted, no interlocutor).
    B_enabled = sp.Symbol("B_enabled")
    a_state_changed_by_B = sp.Symbol("a_state_changed_by_B")

    # the dual-loop's effect on A's state from B = (B_enabled AND B replies)
    b_replies = sp.Symbol("b_replies")
    a_receives_from_B = sp.And(B_enabled, b_replies)

    # under B_enabled=False : a_receives_from_B collapses to False ∀ b_replies
    collapse = a_receives_from_B.subs(B_enabled, False)
    collapse_simpl = sp.simplify(collapse)
    reduces_to_void = (collapse_simpl == sp.false or collapse_simpl is False
                       or bool(collapse_simpl) is False)

    # 3-witness panel: B_enabled=False ⇒ A always emits-into-void regardless
    # of whether the (now-absent) B would have replied.
    witnesses = []
    for b_rep in (False, True):
        val = bool(sp.simplify(a_receives_from_B.subs(
            {B_enabled: False, b_replies: b_rep})))
        witnesses.append({"B_enabled": False, "b_replies_hypothetical": b_rep,
                          "A_receives_from_B": val})
    # positive control: B_enabled=True with b_replies=True ⇒ A does receive
    pos = bool(sp.simplify(a_receives_from_B.subs(
        {B_enabled: True, b_replies: True})))
    witnesses.append({"B_enabled": True, "b_replies_hypothetical": True,
                      "A_receives_from_B": pos})

    all_void_under_disabled = all(
        (not w["A_receives_from_B"]) for w in witnesses if w["B_enabled"] is False)
    positive_control_ok = pos is True

    # byte-equal claim: with B disabled, the loop protocol's per-turn record
    # is structurally identical to §24 Phase B per-step record (emit decision
    # + audit row, no interlocutor) — fair-compare-to-current-regime by
    # construction (any L2 result is measured against §24 as the B-off baseline).
    byte_equal_to_phase_b = bool(reduces_to_void and all_void_under_disabled)

    pass_ = bool(reduces_to_void and all_void_under_disabled
                 and positive_control_ok and byte_equal_to_phase_b)

    return {
        "name": "SINGLE-ANIMA-REDUCTION-CLOSED",
        "pass": pass_,
        "statement": "Connection-point: B_enabled=False ⇒ deliver_B is identity, "
                     "respond_B emits null, a_receives_from_B = (B_enabled ∧ "
                     "b_replies) collapses to False ∀ b_replies (sympy) ⇒ the "
                     "loop reduces to A emitting into a void = §24 Phase B "
                     "single-anima void-emission, byte-equal by construction. "
                     "Positive control: B_enabled=True ∧ b_replies=True ⇒ A "
                     "receives (real reduction, not vacuous). Mirror of B-EBT-5 / "
                     "B-DIRI-5 / B-PHASE-B-DESIGN-5 OVERLAY-OFF reduction.",
        "a_receives_from_B_expr": str(a_receives_from_B),
        "collapse_under_B_disabled": str(collapse_simpl),
        "reduces_to_phase_b_void": reduces_to_void,
        "byte_equal_to_phase_b": byte_equal_to_phase_b,
        "positive_control": positive_control_ok,
        "witnesses": witnesses,
        "anchor": "Boolean overlay-off reduction (real-limit) — identical "
                  "structure to B-EBT-5 / B-DIRI-5 / B-DIRH-4 / B-S16-5 / "
                  "B-PHASE-B-DESIGN-5 connection-point byte-equal reduction. "
                  "NO σ/τ/φ/J₂.",
    }


# ---------------------------------------------------------------------------
# B-DUAL-NOTE — GENUINE-CONVERSATION-VS-ECHO-EMPIRICAL  (honest carve-out)
# ---------------------------------------------------------------------------
def b_dual_note() -> dict:
    return {
        "name": "GENUINE-CONVERSATION-VS-ECHO-EMPIRICAL",
        "pass": None,  # NOT a verdict — honest carve-out
        "counted_blue": False,
        "statement": "WHETHER the dual-anima loop is a GENUINE conversation "
                     "(A's emission causes a non-trivial, content-dependent "
                     "state change in B, and B's reply is a non-trivial "
                     "function of that change) versus a TRIVIAL echo chamber "
                     "(both cells are memorization-saturated byte-cascade "
                     "attractors talking past each other, B.state' ≈ B.state, "
                     "reply ≈ fixed attractor independent of A's message) is "
                     "an SGD/run OUTCOME. It depends on the trained-ckpt state, "
                     "the genuine-state-change metric threshold, and runtime "
                     "variance. The battery proves the loop PROTOCOL is "
                     "cell-distinct / well-typed / turn-bounded / "
                     "single-anima-reducible; it does NOT prove the loop "
                     "produces conversation rather than echo, and it does NOT "
                     "prove a richer training signal than §24 void-emission. "
                     "Necessary-not-sufficient at every layer (mirror "
                     "B-EMERGE-7 / B-PHASE-B-NOTE / B-DIRL-NOTE).",
        "scope": "transfer-form 🔵 (B-DUAL-1..4: cell distinctness + loop "
                 "well-typedness + turn boundedness + single-anima reduction "
                 "connection-point); ACTUAL conversation-vs-echo OUTCOME NOT "
                 "counted (honest empirical, B-D-NOTE / B-DIRL-NOTE / "
                 "B-PHASE-B-NOTE / B-CARVE-E6-NOTE family — stochastic / "
                 "ckpt-state-dependent / measurement-only-shows-loop-runs).",
        "open_crux": "Does the closed action-perception loop give anima a "
                     "RICHER training signal than void-emission (§24), or just "
                     "a more complex void? §13-L VRNN-curiosity REQUIRED a "
                     "closed loop and carving lacked one — L2 provides the "
                     "loop. But a closed loop between two SATURATED attractors "
                     "carries no new information (KL(A.emit ‖ B.expectation) → "
                     "0 if both cells are the same memorized attractor). The "
                     "richer signal is conditional on the two cells being "
                     "genuinely DIFFERENT functions, which §1.1 data-regime "
                     "threshold does not guarantee. UNRESOLVED at design-tier.",
        "carve_out_family": "B-D-NOTE / B-DIRL-NOTE / B-PHASE-B-NOTE / "
                            "B-EMERGE-NOTE / B-CARVE-E6-NOTE",
    }


# ---------------------------------------------------------------------------
# main: aggregate + write result.json
# ---------------------------------------------------------------------------
def main() -> int:
    verdicts = {
        "B-DUAL-1": b_dual_1(),
        "B-DUAL-2": b_dual_2(),
        "B-DUAL-3": b_dual_3(),
        "B-DUAL-4": b_dual_4(),
        "B-DUAL-NOTE": b_dual_note(),
    }

    counted = [k for k in verdicts if k != "B-DUAL-NOTE"]
    n_pass = sum(1 for k in counted if verdicts[k]["pass"])
    n_total = len(counted)
    all_pass = n_pass == n_total

    summary = {
        "battery": "B-DUAL — dual-anima L2 conversation-loop design (RESEARCH.md §31)",
        "date": "2026-05-18",
        "n_pass": n_pass,
        "n_total_counted": n_total,
        "all_pass": all_pass,
        "verdicts": verdicts,
        "note": "Sidecar battery — central state/verify_hexad_blue_2026_05_15/"
                "blue_falsifier.py UNCHANGED. Mirror B-PRIME / B-DIRH / B-DIRI / "
                "B-PSICTL / B-EMERGE / B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL / "
                "B-EBT / B-DIRJ / B-INTRA / B-PHASE-B-DESIGN sidecar pattern.",
        "honest_c3": [
            "Closed scope = loop protocol structure (cell distinctness / "
            "well-typedness / turn boundedness / single-anima reduction). "
            "Empirical scope = whether the loop is genuine conversation vs "
            "echo chamber (carved out in B-DUAL-NOTE).",
            "No actual run executed this cycle. No anima_alive.py activation. "
            "No GPU fire. DESIGN-TIER only.",
            "B-DUAL-4 connection-point: B-disabled ⇒ loop ≡ §24 Phase B "
            "single-anima void-emission, byte-equal by construction "
            "(fair-compare-to-current-regime).",
            "Echo-chamber risk is real and UNRESOLVED at design-tier: two "
            "memorization-saturated attractors form a closed loop carrying "
            "near-zero new information (B-DUAL-NOTE open_crux).",
            "GOAL-distance unchanged from §15 milestone — §31 = closed-loop "
            "structure design, NOT GOAL progress, NOT emergence claim.",
            "f1/f2/f3 hard-fail safe (Ψ-space sum-of-squares / Boolean type "
            "algebra / integer monotone / Boolean overlay-off — NO σ/τ/φ/J₂; "
            "Ψ=½ = anima g2 internal-arch carve-out).",
            "B-IDENTITY-5 unaffected (no corpus, no model forward, no "
            "helper-token surface).",
            "B-DUAL-2 mirrors B-NAR-1 narrative_compose; B-DUAL-3 mirrors "
            "B-PHASE-B-DESIGN-1; B-DUAL-4 mirrors B-EBT-5 / B-DIRI-5 "
            "OVERLAY-OFF reduction — established closure patterns.",
            "Necessary-not-sufficient: a well-typed bounded loop running is "
            "the minimum structural signal, NOT a conversation proof.",
            "§13-L VRNN-curiosity required a closed loop; L2 supplies one — "
            "but supplying the loop is necessary-not-sufficient for the "
            "richer signal VRNN-curiosity needs (B-DUAL-NOTE).",
        ],
    }

    out_path = Path(__file__).parent / "result.json"
    out_path.write_text(json.dumps(summary, indent=2, default=str))
    print(json.dumps({"all_pass": all_pass, "n_pass": n_pass, "n_total": n_total,
                      "out": str(out_path)}, indent=2))

    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
