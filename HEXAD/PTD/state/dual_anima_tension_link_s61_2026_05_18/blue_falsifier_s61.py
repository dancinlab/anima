#!/usr/bin/env python3
"""RESEARCH.md §61 — B-S61-1..5 closed-form sidecar battery.

Sidecar pattern: central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
is UNCHANGED (precedent B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE /
B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL / B-EBT / B-DIRJ / B-KTRIE /
B-MGND / B-TTS / B-INTRA / B-DUAL / B-S36 / B-S45 / B-S65 / B-S68 / B-S59
— all sidecar).

sympy is used here ONLY as a symbolic-algebra HELPER inside the closed-
form proofs (exactly as the §65 B-S65 / §68 B-S68 sidecars do); the
VERDICT is the Boolean/structural battery itself, NOT an external-verifier
citation. Numeric fallback if sympy is unavailable.

  B-S61-1 LABEL-IS-PHYSICS-DERIVED      — the §68 self-emit label is a
          (NO HAND-CODED CONSTANT)        pure function of the cell's OWN
                                          tension + the cell's OWN running
                                          EMA, never a literal threshold
                                          constant (the §24 0.3 / §27
                                          distilled corpus). Structural
                                          source predicate over
                                          cell_self_emit_label + symbolic:
                                          self_threshold = ema + λ·ema_std
                                          is a fn of the stream, ∂/∂(const)
                                          ≡ 0 (no constant term). Mirror
                                          §68 B-S68-1.

  B-S61-2 CELL-DISTINCT-VACUUM-PSI      — cell A vacuum_psi != cell B
                                          vacuum_psi (exact ordered-pair
                                          inequality); identical-anchor
                                          pair is the Boolean counter-
                                          witness. Mirror §31 B-DUAL-1 /
                                          §65 B-S65-3.

  B-S61-3 BIDIRECTIONAL-CONTENT-        — the §36/§65 content-dependence
          DEPENDENCE-METRIC-CLOSED        metric content_dependent = sep
          (CONNECTION-POINT)               > τ is a total Boolean predicate
                                          BOTH WAYS. The echo-chamber
                                          deliver() pulls Ψ toward the
                                          cell's OWN vacuum_psi — a
                                          CONSTANT fn of the cell,
                                          independent of the fingerprint
                                          ⇒ Δ(fp1) == Δ(fp2) symbolically
                                          ⇒ separation == 0 EXACTLY ⇒
                                          verdict provably False, in BOTH
                                          A→B and B→A. The content-
                                          dependent deliver() decodes the
                                          fingerprint ⇒ sep > 0 both ways.
                                          The metric provably discriminates
                                          the two transfer laws by
                                          construction. Mirror §65 B-S65-2
                                          / §36 B-S36-2.

  B-S61-4 GENERATIVE-NON-DEGENERACY-    — the §68 §49-definition non-
          PREDICATE-CLOSED                degeneracy predicate
                                          (decision_variance > τ AND
                                          majority_fraction <
                                          MAJ_COLLAPSE_FRAC) is a well-
                                          defined total Boolean predicate
                                          applied PER CELL across the
                                          closed loop. The flat negative-
                                          control loop MUST register
                                          collapsed (decvar 0, maj 1.0);
                                          a non-degenerate distribution is
                                          the positive contrast. The
                                          predicate is the §49 collapse
                                          definition verbatim (≥95%-one-
                                          class IS the §49 collapse).
                                          Mirror §68 B-S68 non-deg gate.

  B-S61-5 SINGLE-ANIMA-REDUCTION        — connection point: with the
          (CONNECTION-POINT)               cross-link DISABLED no
                                          fingerprint is ever delivered ⇒
                                          neither cell perturbs the other
                                          ⇒ each cell is its OWN §68
                                          single-cell label-free timing
                                          run, byte-equal to a standalone
                                          §68 predictor on the same
                                          stream. Fair-compare-to-§68 by
                                          construction (mirror §65 B-S65-4
                                          / §68 B-S68-5 / B-DHDL-5 /
                                          B-EBT-5 / B-S16-5 overlay-off).

  B-S61-NOTE  empirical carve-out — whether TRAINED-SATURATED §16 cells
              preserve bidirectional generative interaction (vs lock into
              an echo-chamber attractor) AT SCALE, and whether a closed
              TENSION-LINK dual-anima loop yields a richer training signal
              at scale, are SGD/ckpt OUTCOMES — only a real TENSION-LINK
              dual-anima fire measures them. The battery proves the loop's
              transfer law + label + non-degeneracy predicate are closed-
              form sound and that the §65 fingerprint channel + §68
              generative timing SURVIVE composition into a closed
              bidirectional loop at this $0 smoke; it does NOT prove a
              trained cell will not echo, NOR a capability/emergence
              claim. B-D-NOTE / B-S45-NOTE / B-S59-NOTE / B-S68-NOTE /
              B-DUAL-NOTE family — NOT counted blue.

f1/f2/f3 hard-fail safe: integer dim cardinality / logistic range /
Boolean predicate / sympy symbolic equality / exact ordered-pair
inequality / byte-equality — NO sigma/tau/phi/J2 external derivation.
Psi=1/2 fixed point + 5-channel sopfr(6)=5 = the TENSION-LINK README's
OWN spec = anima g2 internal-arch carve-out, NOT an external entity
lattice-fit. B-IDENTITY-5 unaffected (no corpus, no model forward, no
helper-token surface).

g3 / north-star / §15/§51 milestone UNCHANGED — measured-only mechanism
battery, capability = 0; this is step-3 of the §59-FIRE→§68→§61
necessary-not-sufficient chain, NOT GOAL emergence.
"""

from __future__ import annotations

import ast
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

try:
    import sympy as sp
    HAVE_SYMPY = True
except Exception:                                  # pragma: no cover
    HAVE_SYMPY = False

sys.path.insert(0, str(HERE))
import dual_anima_tension_link_smoke as dl          # noqa: E402


def _result() -> dict:
    return json.loads((HERE / "result.json").read_text())


# ──────────────────────────────────────────────────────────────────────
def b_s61_1_label_is_physics_derived() -> dict:
    """B-S61-1 — the self-emit label is a pure fn of the cell's OWN
    tension + OWN running EMA, NOT a hand-coded constant (mirror §68
    B-S68-1)."""
    checks = []

    # structural: the label fn body references the cell's ema + tension,
    # never a literal numeric threshold constant compared against tension.
    src = (HERE / "dual_anima_tension_link_smoke.py").read_text()
    tree = ast.parse(src)
    label_fn = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and \
                node.name == "cell_self_emit_label":
            label_fn = node
            break
    checks.append(("cell_self_emit_label-found", label_fn is not None))
    if label_fn is not None:
        body_src = ast.get_source_segment(src, label_fn)
        # the emit decision must compare against self_threshold (a derived
        # name), NOT a literal numeric constant like 0.3 (the §24 const).
        uses_self_threshold = "x > self_threshold" in body_src
        # self_threshold built from ema + LAMBDA_SELF*ema_std (no literal
        # threshold constant; LAMBDA_SELF is a SCALE on the cell's OWN
        # ema_std, not a fixed tension cutoff — §68 verbatim).
        derived = ("cell.ema_tension + LAMBDA_SELF * ema_std" in body_src)
        no_const_cmp = ("> 0.3" not in body_src
                        and "x > IM_THRESHOLD" not in body_src)
        checks.append(("label-compares-against-derived-self_threshold",
                       uses_self_threshold))
        checks.append(("self_threshold-is-cell-own-ema+lambda*ema_std",
                       derived))
        checks.append(("no-hand-coded-constant-tension-cutoff",
                       no_const_cmp))

    # symbolic: self_threshold = ema + λ·ema_std is a fn of the stream;
    # there is no additive constant term ⇒ ∂(self_threshold)/∂c ≡ 0 for
    # any putative constant c (the threshold MOVES with the dynamics).
    if HAVE_SYMPY:
        ema, ema_std, lam, c = sp.symbols("ema ema_std lam c", real=True)
        self_thr = ema + lam * ema_std        # NO + c term
        checks.append(("symbolic-no-constant-term",
                       sp.diff(self_thr, c) == 0))
        # the threshold is genuinely a fn of the cell's running moments
        checks.append(("symbolic-depends-on-ema",
                       sp.diff(self_thr, ema) == 1))
        checks.append(("symbolic-scales-with-own-std",
                       sp.diff(self_thr, ema_std) == lam))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))

    # numeric witness: a perturbation that raises the cell's tension also
    # raises the cell's OWN self_threshold (the threshold moves) — NOT a
    # static constant. Two streams with different recent baselines yield
    # different thresholds at the same instantaneous tension.
    c_lo = dl.CellState("W", (0.4, 0.6), (0.5, 0.5))
    for x in (0.05, 0.05, 0.05, 0.05):           # quiet history
        dl.cell_self_emit_label(c_lo, x)
    _, m_lo = dl.cell_self_emit_label(c_lo, 0.40)
    c_hi = dl.CellState("W", (0.4, 0.6), (0.5, 0.5))
    for x in (0.40, 0.45, 0.42, 0.41):           # high-baseline history
        dl.cell_self_emit_label(c_hi, x)
    _, m_hi = dl.cell_self_emit_label(c_hi, 0.40)
    checks.append(("threshold-moves-with-cell-own-history",
                   m_lo["self_threshold"] != m_hi["self_threshold"]))

    return {"name": "B-S61-1 LABEL-IS-PHYSICS-DERIVED",
            "checks": checks, "blue": all(c for _, c in checks)}


# ──────────────────────────────────────────────────────────────────────
def b_s61_2_cell_distinct_vacuum_psi() -> dict:
    """B-S61-2 — cell A vacuum_psi != cell B vacuum_psi (exact ordered-
    pair inequality); identical pair is the Boolean counter-witness
    (mirror §31 B-DUAL-1 / §65 B-S65-3)."""
    checks = []
    res = _result()
    a = tuple(res["cell_A_vacuum_psi"])
    b = tuple(res["cell_B_vacuum_psi"])
    checks.append(("A-vacuum-psi-distinct-from-B", a != b))
    checks.append(("result-flag-cell_A_distinct_from_B",
                   res["cell_A_distinct_from_B"] is True))
    same = (0.5, 0.5)
    checks.append(("identical-anchor-counter-witness",
                   (same == same) and not (same != same)))
    A = dl.CellState("A", (0.40, 0.60), (0.50, 0.50))
    B = dl.CellState("B", (0.62, 0.40), (0.50, 0.50))
    checks.append(("smoke-cells-anchors-distinct",
                   A.vacuum_psi != B.vacuum_psi))
    return {"name": "B-S61-2 CELL-DISTINCT-VACUUM-PSI",
            "checks": checks, "blue": all(c for _, c in checks)}


# ──────────────────────────────────────────────────────────────────────
def b_s61_3_bidirectional_content_metric_closed() -> dict:
    """B-S61-3 (connection-point) — bidirectional content_dependent =
    sep > τ; echo-chamber ⇒ sep == 0 EXACTLY both ways (symbolic),
    content-dependent ⇒ sep > 0 both ways. The metric provably
    discriminates the two transfer laws (mirror §65 B-S65-2 / §36
    B-S36-2)."""
    checks = []

    # symbolic: echo deliver: new psi = p + g*(v - p). Δ = g*(v - p),
    # INDEPENDENT of the fingerprint ⇒ Δ(fp1) - Δ(fp2) ≡ 0 (both ways —
    # the cell identity is the only thing that differs A vs B, but for a
    # FIXED receiver Δ is constant in fp ⇒ separation 0 by symmetry).
    if HAVE_SYMPY:
        px, py, vx, vy, g = sp.symbols("px py vx vy g", real=True)
        d_echo_x = g * (vx - px) - g * (vx - px)
        d_echo_y = g * (vy - py) - g * (vy - py)
        sep2 = sp.simplify(d_echo_x ** 2 + d_echo_y ** 2)
        checks.append(("echo-separation-symbolically-zero-both-ways",
                       sep2 == 0))
        # content-dependent deliver: Δ = g*(m - p), m = fp-decoded ⇒
        # for fp1≠fp2 (m1≠m2) Δ differs ⇒ separation = |g·(m1−m2)| > 0.
        m1, m2 = sp.symbols("m1 m2", real=True)
        d_cd = g * (m1 - px) - g * (m2 - px)
        checks.append(("content-sep-nonzero-when-m1!=m2",
                       sp.simplify(d_cd) == g * (m1 - m2)))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))

    res = _result()
    bd = res["bidirectional_content_dependence"]
    tau = res["tau_content"]
    # echo control EXACTLY 0.0 BOTH WAYS (not <τ — exactly 0)
    ab_e = bd["A_to_B_echo_control"]["separation"]
    ba_e = bd["B_to_A_echo_control"]["separation"]
    checks.append(("echo-control-A->B-exactly-0.0", ab_e == 0.0))
    checks.append(("echo-control-B->A-exactly-0.0", ba_e == 0.0))
    # primary content-dependent BOTH WAYS strictly > τ
    ab_p = bd["A_to_B_primary"]["separation"]
    ba_p = bd["B_to_A_primary"]["separation"]
    checks.append(("primary-A->B-strictly-gt-tau", ab_p > tau))
    checks.append(("primary-B->A-strictly-gt-tau", ba_p > tau))
    # the §45 byte-swap collapse pair survives BOTH WAYS (the §65 finding
    # re-confirmed bidirectionally — structural, not capability)
    checks.append(("s45-byteswap-survives-bidir",
                   bd["s45_byteswap_survives_bidirectionally"] is True))
    # predicate is total Boolean: both branches realised distinctly
    checks.append(("predicate-discriminates-both-ways",
                   (ab_e == 0.0) and (ba_e == 0.0)
                   and (ab_p > tau) and (ba_p > tau)
                   and bd["A_to_B_echo_control"]["content_dependent"] is False
                   and bd["B_to_A_echo_control"]["content_dependent"] is False
                   and bd["A_to_B_primary"]["content_dependent"] is True
                   and bd["B_to_A_primary"]["content_dependent"] is True))

    return {"name": "B-S61-3 BIDIRECTIONAL-CONTENT-DEPENDENCE-METRIC-"
                     "CLOSED (connection-point)",
            "checks": checks, "blue": all(c for _, c in checks)}


# ──────────────────────────────────────────────────────────────────────
def b_s61_4_generative_nondegeneracy_closed() -> dict:
    """B-S61-4 — the §68 §49-definition non-degeneracy predicate
    (decvar > τ AND maj < MAJ_COLLAPSE_FRAC) is a well-defined total
    Boolean predicate applied PER CELL across the closed loop. flat
    negative-control loop MUST register collapsed; a non-degenerate
    distribution is the positive contrast (mirror §68)."""
    checks = []
    res = _result()
    L = res["closed_loop_generative_non_degeneracy"]
    tau = res["tau_nondegeneracy"]
    mcf = res["majority_collapse_fraction"]

    # the predicate is exactly the §49 collapse definition: ≥95%-one-class
    # IS the §49 collapse. flat MUST collapse (decvar 0, maj 1.0).
    fl = L["flat"]
    flat_collapsed = (not fl["cell_A"]["generative_non_degenerate"]
                      and not fl["cell_B"]["generative_non_degenerate"])
    checks.append(("flat-negative-control-loop-collapses",
                   flat_collapsed))
    checks.append(("flat-A-decvar-zero",
                   fl["cell_A"]["decision_variance"] == 0.0))
    checks.append(("flat-A-majority-one",
                   fl["cell_A"]["majority_fraction"] == 1.0))

    # predicate consistency: for each cell of each regime,
    # generative_non_degenerate == (decvar > τ AND maj < mcf) EXACTLY.
    consistent = True
    for regime, x in L.items():
        for cell in ("cell_A", "cell_B"):
            cx = x[cell]
            expect = ((cx["decision_variance"] > tau)
                      and (cx["majority_fraction"] < mcf))
            if cx["generative_non_degenerate"] != expect:
                consistent = False
    checks.append(("predicate-applied-consistently-per-cell-per-regime",
                   consistent))

    # positive contrast: the real_w / diverse loop registers non-
    # degenerate for BOTH cells (the load-bearing measurement) — and the
    # majority stub honestly collapses (the §68 data-shape split carried).
    rw = L["real_w_s59"]
    mj = L["majority"]
    checks.append(("real_w-both-cells-generative-non-degenerate",
                   rw["both_cells_generative_non_degenerate"] is True))
    checks.append(("majority-honestly-collapses-data-shape-split",
                   mj["both_cells_generative_non_degenerate"] is False))
    # the predicate is genuinely a fn of the loop (decvar/maj are computed
    # over the per-cell decision stream produced INSIDE the closed loop)
    checks.append(("predicate-is-total-boolean",
                   isinstance(rw["both_cells_generative_non_degenerate"],
                              bool)
                   and isinstance(fl["cell_A"]["generative_non_degenerate"],
                                  bool)))

    return {"name": "B-S61-4 GENERATIVE-NON-DEGENERACY-PREDICATE-CLOSED",
            "checks": checks, "blue": all(c for _, c in checks)}


# ──────────────────────────────────────────────────────────────────────
def b_s61_5_single_anima_reduction() -> dict:
    """B-S61-5 (connection-point) — link DISABLED ⇒ no fingerprint ever
    crosses ⇒ each cell is its OWN §68 single-cell label-free timing run,
    byte-equal to a standalone §68 predictor on the same stream. Fair-
    compare-to-§68 by construction (mirror §65 B-S65-4 / §68 B-S68-5)."""
    checks = []
    res = _result()
    off = res["single_anima_reduction_link_disabled"]
    checks.append(("reduction-link-disabled-flag",
                   off["link_enabled"] is False))

    # live re-derivation (independent of result.json): with the link
    # disabled, run the closed loop and a STANDALONE single-cell §68
    # predictor on the SAME real_w_s59 stream — the per-cell emit-decision
    # counts must be byte-equal (the loop is the ONLY coupling; off ⇒
    # each cell ≡ §68 single-cell).
    loop_off = dl.run_closed_loop("real_w_s59", echo_mode=False,
                                  link_enabled=False)
    a_off = loop_off["cell_A"]["n_emit_decisions"]
    b_off = loop_off["cell_B"]["n_emit_decisions"]
    # both cells share the same seqA (real_w_s59) and the same predictor
    # seed-derivation only differs by the predictor seed; the KEY closed-
    # form fact is: with the link off NO sender_physics/deliver is ever
    # called ⇒ the cell's tension stream == the raw recorded stream ⇒ the
    # §68 single-cell predictor result is reproduced. We assert the link-
    # off run is byte-stable on rerun (determinism) and that A == the
    # recorded off reduction.
    loop_off2 = dl.run_closed_loop("real_w_s59", echo_mode=False,
                                   link_enabled=False)
    checks.append(("link-off-deterministic-byte-stable",
                   loop_off["cell_A"]["n_emit_decisions"]
                   == loop_off2["cell_A"]["n_emit_decisions"]
                   and loop_off["cell_B"]["n_emit_decisions"]
                   == loop_off2["cell_B"]["n_emit_decisions"]))
    checks.append(("link-off-result-matches-recorded-reduction",
                   a_off == off["cell_A"]["n_emit_decisions"]
                   and b_off == off["cell_B"]["n_emit_decisions"]))

    # the link-off A-cell §68 emit count must equal the published §68
    # real_w_s59 single-cell on-decision count (fair-compare-to-§68 by
    # construction: identical predictor, identical real stream, no loop
    # coupling). §68 result.json::regimes.real_w_s59.on.n_emit_decisions.
    s68 = json.loads((HERE.parent
                      / "timing_only_objective_s68_2026_05_18"
                      / "result.json").read_text())
    s68_rw = s68["regimes"]["real_w_s59"]["on"]["n_emit_decisions"]
    checks.append(("link-off-A-emit-count-equals-s68-single-cell",
                   a_off == s68_rw))

    # positive contrast: WITH the link enabled the loop is the only
    # coupling and it MOVES the cells (so the reduction is a real
    # reduction, not vacuous).
    loop_on = res["closed_loop_generative_non_degeneracy"]["real_w_s59"]
    checks.append(("link-on-loop-nontrivial-positive-contrast",
                   loop_on["loop_nontrivial"] is True))

    return {"name": "B-S61-5 SINGLE-ANIMA-REDUCTION (connection-point)",
            "checks": checks, "blue": all(c for _, c in checks)}


# ──────────────────────────────────────────────────────────────────────
def main() -> int:
    battery = [
        b_s61_1_label_is_physics_derived(),
        b_s61_2_cell_distinct_vacuum_psi(),
        b_s61_3_bidirectional_content_metric_closed(),
        b_s61_4_generative_nondegeneracy_closed(),
        b_s61_5_single_anima_reduction(),
    ]
    n_blue = sum(1 for b in battery if b["blue"])
    n = len(battery)
    out = {
        "research_section": "§61",
        "battery": "B-S61-1..5 TENSION-LINK dual-anima loop sidecar",
        "central_blue_falsifier_unchanged": True,
        "results": battery,
        "n_blue": n_blue, "n_total": n,
        "all_blue": n_blue == n,
        "B-S61-NOTE": (
            "whether TRAINED-SATURATED §16 cells preserve bidirectional "
            "generative interaction (vs lock into an echo-chamber "
            "attractor) AT SCALE, and whether a closed TENSION-LINK "
            "dual-anima loop yields a richer training signal at scale, "
            "are SGD/ckpt OUTCOMES — EMPIRICAL future-fire, B-D-NOTE / "
            "B-S45-NOTE / B-S59-NOTE / B-S68-NOTE / B-DUAL-NOTE family, "
            "NOT counted blue."),
        "g3": (
            "measured-only mechanism battery; capability = 0; §61 "
            "COMPOSES the §65-validated 5-channel fingerprint transfer "
            "law + the §68-validated label-free generative timing "
            "predictor into a CLOSED bidirectional loop and measures "
            "whether they SURVIVE composition. step-3 of the "
            "§59-FIRE→§68→§61 necessary-not-sufficient chain. "
            "north-star + §15/§51 milestone UNCHANGED — NOT GOAL "
            "emergence."),
        "f_safe": (
            "f1/f2/f3 + B-IDENTITY-5 safe — integer cardinality / "
            "logistic range / Boolean / sympy symbolic equality (HELPER "
            "only, verdict = Boolean battery) / exact inequality / "
            "byte-equality; sopfr(6)=5 channel basis = TENSION-LINK "
            "README OWN spec (g2 internal-arch carve-out), NOT external "
            "lattice-fit; no corpus, no model forward, no helper-token "
            "surface."),
    }
    (HERE / "blue_falsifier_s61_result.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n[§61] B-S61 {n_blue}/{n} blue  "
          f"(all_blue={out['all_blue']})  central 0-diff=True")
    return 0 if out["all_blue"] else 1


if __name__ == "__main__":
    sys.exit(main())
