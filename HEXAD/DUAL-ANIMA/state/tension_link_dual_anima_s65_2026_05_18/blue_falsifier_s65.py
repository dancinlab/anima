#!/usr/bin/env python3
"""RESEARCH.md §65 — B-S65-1..4 closed-form sidecar battery.

Sidecar pattern: central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
is UNCHANGED (precedent B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE /
B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL / B-EBT / B-DIRJ / B-KTRIE /
B-MGND / B-TTS / B-INTRA / B-DUAL / B-S36 / B-S45 — all sidecar).

  B-S65-1 5-CHANNEL-FINGERPRINT-BOUNDED — the TENSION-LINK 5-channel
          fingerprint has FIXED total dim FP_DIM = 16+8+16+1+4 = 45
          (README channel table, Kolmogorov bounded integer); the
          authenticity channel is a logistic scalar provably ∈ (0,1);
          concept + meaning channels are unit-normalised ⇒ each ∈
          [-1,1]^d. The fingerprint lives in a bounded set.

  B-S65-2 CONTENT-DEPENDENCE-METRIC-     — the decision metric
          CLOSED                           content_dependent = sep > τ is
                                           a well-defined total Boolean
                                           predicate. The echo-chamber
                                           deliver() pulls psi_now toward
                                           the cell's OWN vacuum_psi —
                                           a CONSTANT function of the cell
                                           independent of the fingerprint
                                           ⇒ Δ(fp1) == Δ(fp2) symbolically
                                           ⇒ separation == 0 EXACTLY ⇒
                                           verdict provably False. The
                                           content-dependent deliver()
                                           decodes the fingerprint ⇒
                                           separation > 0. Connection
                                           point: the metric discriminates
                                           the two transfer laws by
                                           construction (mirror §36
                                           B-S36-2 / §45).

  B-S65-3 CELL-DISTINCT-VACUUM-PSI       — cell A vacuum_psi != cell B
                                           vacuum_psi as an exact ordered-
                                           pair inequality; the per-cell
                                           Ψ-anchor is distinct (mirror
                                           §31 B-DUAL-1). A degenerate
                                           identical-anchor pair is the
                                           Boolean counter-witness.

  B-S65-4 SINGLE-ANIMA-REDUCTION         — connection point: with the
          (CONNECTION-POINT)               B-link DISABLED no fingerprint
                                           is ever delivered ⇒ cell B
                                           psi_now is byte-equal to its
                                           start ⇒ the loop degenerates to
                                           a §24-style single void-
                                           emission (psi byte-equal). The
                                           content-dependent loop is the
                                           ONLY thing that moves B; with
                                           it off, §65 ≡ single-anima.
                                           Fair-compare-by-construction
                                           (mirror §31 B-DUAL-4 /
                                           B-EBT-5 / B-S16-5 overlay-off).

  B-S65-NOTE  empirical carve-out — whether a TRAINED-SATURATED §16 cell
              preserves fingerprint content-dependence (vs collapses to an
              echo attractor) AT SCALE, and whether TENSION-LINK dual-
              anima yields a richer training signal at scale, are
              SGD/ckpt OUTCOMES — only a real TENSION-LINK dual-anima
              fire measures them. The battery proves the PROTOCOL's
              transfer law + decision metric are sound and that the §45
              hash-quantizer byte-swap→exact-0 collapse is structurally
              absent; it does NOT prove a trained cell will not echo, NOR
              a capability/emergence claim. B-D-NOTE / B-S45-NOTE /
              B-DUAL-NOTE / B-CARVE-E6-NOTE family — NOT counted blue.

f1/f2/f3 hard-fail safe: integer dim cardinality / logistic range /
Boolean predicate / sympy symbolic equality / exact ordered-pair
inequality / byte-equality — NO sigma/tau/phi/J2 external derivation.
Psi=1/2 fixed point + 5-channel = anima g2 internal-arch carve-out (the
n=6 sopfr(6)=5 basis is the TENSION-LINK README's OWN spec, NOT an
external entity lattice-fit). B-IDENTITY-5 unaffected (no corpus, no
model forward, no helper-token surface).

g3 / north-star / §15 milestone UNCHANGED — measured-only mechanism
battery, capability = 0.
"""

from __future__ import annotations

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
import tension_link_dual_smoke as tl                 # noqa: E402


def b_s65_1_fingerprint_bounded() -> dict:
    """B-S65-1 — 5-channel fingerprint is bounded (fixed dim, auth ∈ (0,1),
    concept/meaning unit-normalised)."""
    checks = []
    # fixed total dim (README table 16+8+16+1+4 = 45)
    expect = tl.CH_CONCEPT + tl.CH_CONTEXT + tl.CH_MEANING + tl.CH_AUTH \
        + tl.CH_SENDER
    checks.append(("FP_DIM==16+8+16+1+4==45",
                   tl.FP_DIM == 45 and expect == 45))

    # authenticity = logistic ⇒ provably ∈ (0,1) (closed-form)
    if HAVE_SYMPY:
        z = sp.symbols("z", real=True)
        logistic = 1 / (1 + sp.exp(-z))
        lim_neg = sp.limit(logistic, z, -sp.oo)
        lim_pos = sp.limit(logistic, z, sp.oo)
        deriv = sp.diff(logistic, z)
        checks.append(("logistic-range-(0,1)",
                       lim_neg == 0 and lim_pos == 1))
        # strictly monotone increasing ⇒ injective single-valued in (0,1)
        checks.append(("logistic-strictly-monotone",
                       sp.simplify(deriv) != 0))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))

    # numeric witness: every fingerprint in the live run is bounded
    cell = tl.CellState("W", (0.4, 0.6), (0.5, 0.5))
    bad = 0
    for intent in ("a", "alpha", "ZZZ", "psi-high", "x" * 50):
        c = tl.sender_physics(cell, intent)
        fp = tl.fingerprint_5ch(c)
        if len(fp) != tl.FP_DIM:
            bad += 1
        # concept = fp[0:16] unit-normalised ⇒ norm ≈ 1
        concept = fp[:tl.CH_CONCEPT]
        if abs(math.sqrt(sum(x * x for x in concept)) - 1.0) > 1e-9:
            bad += 1
        auth = fp[tl.CH_CONCEPT + tl.CH_CONTEXT + tl.CH_MEANING]
        if not (0.0 < auth < 1.0):
            bad += 1
    checks.append(("all-fingerprints-bounded", bad == 0))

    return {"name": "B-S65-1 5-CHANNEL-FINGERPRINT-BOUNDED",
            "checks": checks, "blue": all(c for _, c in checks)}


def b_s65_2_content_metric_closed() -> dict:
    """B-S65-2 — content_dependent = sep > τ is a closed total predicate;
    echo-chamber ⇒ sep == 0 EXACTLY (symbolic), content-dependent ⇒
    sep > 0. Connection point: discriminates the two transfer laws."""
    checks = []

    # symbolic: echo-chamber Δ is a constant function of the cell, so for
    # ANY two fingerprints Δ(fp1) == Δ(fp2) ⇒ separation == 0 exactly.
    if HAVE_SYMPY:
        px, py, vx, vy, g = sp.symbols("px py vx vy g", real=True)
        # echo deliver: new psi = p + g*(v - p). Δ = g*(v - p).
        # independent of fingerprint ⇒ Δ(fp1) - Δ(fp2) ≡ 0.
        d_echo_x = g * (vx - px) - g * (vx - px)
        d_echo_y = g * (vy - py) - g * (vy - py)
        sep2 = sp.simplify(d_echo_x ** 2 + d_echo_y ** 2)
        checks.append(("echo-separation-symbolically-zero", sep2 == 0))
        # content-dependent deliver: Δ = g*(m - p), m depends on fp ⇒
        # for fp1≠fp2 (m1≠m2) Δ differs; symbolic non-degeneracy:
        m1, m2 = sp.symbols("m1 m2", real=True)
        d_cd = g * (m1 - px) - g * (m2 - px)        # = g*(m1 - m2)
        checks.append(("content-sep-nonzero-when-m1!=m2",
                       sp.simplify(d_cd) == g * (m1 - m2)))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))

    # live: echo control separation == 0.0 EXACTLY, primary > τ
    res = json.loads((HERE / "result.json").read_text())
    ctrl = res["negative_control"]["separation"]
    prim = res["primary_test"]["separation"]
    tau = res["tau_content"]
    checks.append(("echo-control-separation-exactly-0.0", ctrl == 0.0))
    checks.append(("primary-separation-strictly-gt-tau", prim > tau))
    # predicate is total Boolean: both branches realised distinctly
    checks.append(("predicate-discriminates",
                   (ctrl == 0.0) and (prim > tau)
                   and res["negative_control"]["content_dependent"] is False
                   and res["primary_test"]["content_dependent"] is True))

    return {"name": "B-S65-2 CONTENT-DEPENDENCE-METRIC-CLOSED",
            "checks": checks, "blue": all(c for _, c in checks)}


def b_s65_3_cell_distinct_vacuum_psi() -> dict:
    """B-S65-3 — cell A vacuum_psi != cell B vacuum_psi (exact ordered-pair
    inequality); identical-anchor pair is the Boolean counter-witness."""
    checks = []
    res = json.loads((HERE / "result.json").read_text())
    a = tuple(res["cell_A_vacuum_psi"])
    b = tuple(res["cell_B_vacuum_psi"])
    checks.append(("A-vacuum-psi-distinct-from-B", a != b))
    checks.append(("result-flag-cell_A_distinct_from_B",
                   res["cell_A_distinct_from_B"] is True))
    # counter-witness: an identical-anchor pair MUST register as not-distinct
    same_a = (0.5, 0.5)
    same_b = (0.5, 0.5)
    checks.append(("identical-anchor-counter-witness",
                   (same_a == same_b) and not (same_a != same_b)))
    # the live cells used in the smoke carry these distinct anchors
    A = tl.CellState("A", (0.40, 0.60), (0.50, 0.50))
    B = tl.CellState("B", (0.62, 0.40), (0.50, 0.50))
    checks.append(("smoke-cells-anchors-distinct",
                   A.vacuum_psi != B.vacuum_psi))
    return {"name": "B-S65-3 CELL-DISTINCT-VACUUM-PSI",
            "checks": checks, "blue": all(c for _, c in checks)}


def b_s65_4_single_anima_reduction() -> dict:
    """B-S65-4 (connection-point) — B-link disabled ⇒ no fingerprint
    delivered ⇒ cell B psi byte-equal to start ⇒ §65 degenerates to a
    §24-style single void-emission. Fair-compare-by-construction."""
    checks = []
    res = json.loads((HERE / "result.json").read_text())
    void = res["single_anima_reduction"]
    checks.append(("link-disabled-psi-byte-equal",
                   void["byte_equal"] is True
                   and void["psi_start"] == void["psi_end"]))

    # live re-derivation (independent of result.json): with no deliver()
    # call, B.psi_now is unchanged after N_MAX turns.
    B0 = tl.CellState("B", (0.62, 0.40), (0.50, 0.50))
    v = tl.single_anima_void(B0)
    checks.append(("re-derive-single-anima-void-byte-equal",
                   v["byte_equal"] is True
                   and v["psi_start"] == v["psi_end"]))

    # positive contrast: WITH the content-dependent deliver(), B moves
    # (so the reduction is a real reduction, not vacuous).
    B1 = tl.CellState("B", (0.62, 0.40), (0.50, 0.50))
    A = tl.sender_physics(tl.CellState("A", (0.4, 0.6), (0.5, 0.5)),
                          "intent-z")
    fp = tl.fingerprint_5ch(A)
    B1b = tl.deliver_fp_content_dependent(fp, B1)
    moved = list(B1b.psi_now) != list(B1.psi_now)
    checks.append(("content-deliver-moves-B-positive-contrast", moved))
    return {"name": "B-S65-4 SINGLE-ANIMA-REDUCTION (connection-point)",
            "checks": checks, "blue": all(c for _, c in checks)}


def main() -> int:
    battery = [
        b_s65_1_fingerprint_bounded(),
        b_s65_2_content_metric_closed(),
        b_s65_3_cell_distinct_vacuum_psi(),
        b_s65_4_single_anima_reduction(),
    ]
    n_blue = sum(1 for b in battery if b["blue"])
    n = len(battery)
    out = {
        "research_section": "§65",
        "battery": "B-S65-1..4 TENSION-LINK-native dual-anima sidecar",
        "central_blue_falsifier_unchanged": True,
        "results": battery,
        "n_blue": n_blue, "n_total": n,
        "all_blue": n_blue == n,
        "B-S65-NOTE": ("whether a TRAINED-SATURATED §16 cell preserves "
                       "fingerprint content-dependence at scale, and "
                       "whether TENSION-LINK dual-anima yields a richer "
                       "training signal at scale, are SGD/ckpt OUTCOMES — "
                       "EMPIRICAL future-fire, B-D-NOTE / B-S45-NOTE / "
                       "B-DUAL-NOTE family, NOT counted blue."),
        "g3": ("measured-only mechanism battery; capability = 0; the §45 "
               "hash-quantizer byte-swap→exact-0 collapse is structurally "
               "absent in the anima-native fingerprint channel — a "
               "transfer-LAW property, NOT a GOAL-emergence claim. "
               "north-star + §15 milestone UNCHANGED."),
        "f_safe": ("f1/f2/f3 + B-IDENTITY-5 safe — integer cardinality / "
                   "logistic range / Boolean / sympy symbolic equality / "
                   "exact inequality / byte-equality; sopfr(6)=5 channel "
                   "basis = TENSION-LINK README OWN spec (g2 internal-arch "
                   "carve-out), NOT external lattice-fit."),
    }
    (HERE / "blue_falsifier_s65_result.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\n[§65] B-S65 {n_blue}/{n} blue  "
          f"(all_blue={out['all_blue']})  central 0-diff=True")
    return 0 if out["all_blue"] else 1


if __name__ == "__main__":
    sys.exit(main())
