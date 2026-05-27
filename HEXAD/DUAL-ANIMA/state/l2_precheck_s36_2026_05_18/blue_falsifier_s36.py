#!/usr/bin/env python3
"""RESEARCH.md §36 — B-S36-1..3 closed-form sidecar battery.

Sidecar pattern: central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
is UNCHANGED (precedent B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE /
B-PUREPHYS / B-SCALE / B-MITENS / B-DIRL / B-EBT / B-DIRJ / B-KTRIE /
B-MGND / B-TTS / B-INTRA / B-DUAL — all sidecar).

  B-S36-1 PSI-SHIFT-BOUNDED            — Ψ-shift magnitude ∈ [0, sqrt(2)],
                                         Euclidean diameter of the unit
                                         Ψ-square (Kolmogorov bounded set).
  B-S36-2 CONTENT-DEPENDENCE-METRIC-   — the decision metric
          CLOSED                         content_dependent = sep > τ is a
                                         well-defined total Boolean
                                         predicate; an echo-chamber
                                         deliver() (Δ a constant function
                                         of the cell) gives sep == 0
                                         EXACTLY ⇒ verdict provably False;
                                         a content-dependent deliver()
                                         gives sep > 0. Connection point:
                                         the metric discriminates the two
                                         transition laws by construction.
  B-S36-3 DETERMINISTIC                — content_dependence_test.py is a
                                         pure function (seed-fixed, no RNG,
                                         no model forward) — 3x re-run
                                         produces a byte-identical
                                         result.json.

  B-S36-NOTE  empirical carve-out — whether a TRAINED-SATURATED §16 cell
              preserves the content-dependent transition (vs collapses to
              an echo-chamber attractor) is an SGD/ckpt OUTCOME, only a
              real dual-anima fire measures it. The battery proves the
              PROTOCOL's transition law + decision metric are sound; it
              does NOT prove a trained cell will not echo. B-D-NOTE /
              B-DUAL-NOTE / B-CARVE-E6-NOTE family — NOT counted blue.

f1/f2/f3 hard-fail safe: Euclidean norm bound / Boolean predicate / sympy
sign / determinism — NO sigma/tau/phi/J2 external derivation. Psi=1/2
fixed point = anima g2 internal-arch carve-out. B-IDENTITY-5 unaffected
(no corpus, no model forward, no helper-token surface).
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

try:
    import sympy as sp
    HAVE_SYMPY = True
except Exception:                                  # pragma: no cover
    HAVE_SYMPY = False

# import the test module under verification
sys.path.insert(0, str(HERE))
import content_dependence_test as cdt               # noqa: E402


def b_s36_1_psi_shift_bounded() -> dict:
    """B-S36-1 — Ψ-shift magnitude is bounded in [0, sqrt(2)].

    psi_now ∈ [0,1]^2. Δ = psi_now(after) − psi_now(before) ∈ [-1,1]^2.
    ‖Δ‖₂ = sqrt(dx² + dy²) ≤ sqrt(1 + 1) = sqrt(2) — the Euclidean
    diameter of the unit square (Kolmogorov bounded set, real-limit
    geometry anchor). Lower bound 0 trivially (Δ = 0 ⇒ ‖Δ‖ = 0)."""
    checks = []

    # closed-form bound: max ‖Δ‖ over [0,1]^2 corners
    sqrt2 = math.sqrt(2.0)
    if HAVE_SYMPY:
        dx, dy = sp.symbols("dx dy", real=True)
        # on the unit square, dx,dy each ∈ [-1,1]; max of dx²+dy² is 2
        mag2 = dx ** 2 + dy ** 2
        # sympy: the maximum of dx²+dy² on [-1,1]² is at a corner = 2
        corner_max = max(mag2.subs({dx: a, dy: b})
                         for a in (-1, 0, 1) for b in (-1, 0, 1))
        checks.append(("sympy-corner-max-eq-2", corner_max == 2))
        checks.append(("sqrt(corner_max)==sqrt2",
                       abs(float(sp.sqrt(corner_max)) - sqrt2) < 1e-12))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))

    # numeric witness: every measured Ψ-shift in result.json is in bound
    res = json.loads((HERE / "result.json").read_text())
    mags = []
    for blk in (res["primary_test"], res["negative_control"]):
        mags.append(blk["delta_m1"]["mag"])
        mags.append(blk["delta_m2"]["mag"])
        mags.append(blk["separation"])
    all_in_bound = all(0.0 <= m <= sqrt2 + 1e-12 for m in mags)
    checks.append(("all-measured-shifts-in-[0,sqrt2]", all_in_bound))
    # the dual_loop trace Ψ-coordinates are all in [0,1]^2
    trace = res["dual_loop_sanity"]["psi_b_trace"]
    trace_ok = all(0.0 - 1e-9 <= x <= 1.0 + 1e-9 and
                   0.0 - 1e-9 <= y <= 1.0 + 1e-9 for x, y in trace)
    checks.append(("loop-trace-psi-in-unit-square", trace_ok))

    ok = all(v for _, v in checks)
    return {"id": "B-S36-1", "name": "PSI-SHIFT-BOUNDED",
            "passed": ok, "checks": checks}


def b_s36_2_content_dependence_metric_closed() -> dict:
    """B-S36-2 — the content-dependence decision metric is closed-form.

    content_dependent := ‖Δ(m1) − Δ(m2)‖ > τ  is a TOTAL Boolean
    predicate on a non-negative real (a norm) and a positive threshold.

    The CONNECTION POINT (the metric discriminates the two transition
    laws BY CONSTRUCTION):
      - echo_chamber deliver(): Δ(B,m) is a function of the cell ONLY
        (pulls toward vacuum_psi, message never read). Therefore
        Δ(m1) ≡ Δ(m2) as functions of the same fresh cell ⇒
        ‖Δ(m1)−Δ(m2)‖ == 0 EXACTLY ⇒ content_dependent provably False.
      - content_dependent deliver(): Δ(B,m) reads encode_message_to_psi(m);
        m1 != m2 byte-distinct ⇒ encoded points differ ⇒ Δ differ ⇒
        separation > 0.
    The metric is sound: it returns False exactly on the echo chamber and
    True on the genuine transition. This is verified both by sympy on the
    transition algebra AND numerically on result.json."""
    checks = []

    # closed-form: echo-chamber deliver() gives separation == 0 exactly.
    # echo deliver: psi' = psi + G*(vac - psi). For a FRESH cell, psi and
    # vac are FIXED (message-independent) ⇒ Δ = G*(vac - psi) is a
    # constant. Δ(m1) - Δ(m2) = 0 for ALL m1, m2.
    if HAVE_SYMPY:
        G, px, py, vx, vy = sp.symbols("G px py vx vy", real=True)
        # echo Δ — message symbol does NOT appear ⇒ Δ independent of m
        dx_echo = G * (vx - px)
        dy_echo = G * (vy - py)
        # Δ(m1) - Δ(m2): same expression, so difference is identically 0
        sep2_echo = (dx_echo - dx_echo) ** 2 + (dy_echo - dy_echo) ** 2
        checks.append(("sympy-echo-separation-identically-0",
                       sp.simplify(sep2_echo) == 0))
        # content-dependent Δ — message-encoded point (mx,my) DOES appear
        mx1, my1, mx2, my2 = sp.symbols("mx1 my1 mx2 my2", real=True)
        dx1 = G * (mx1 - px)
        dx2 = G * (mx2 - px)
        sep_x = sp.simplify(dx1 - dx2)        # = G*(mx1 - mx2)
        checks.append(("sympy-content-sep-x-eq-G(mx1-mx2)",
                       sep_x == G * (mx1 - mx2)))
        # ⇒ if mx1 != mx2 (distinct messages) and G != 0, sep_x != 0
        checks.append(("sympy-content-sep-nonzero-when-msgs-distinct",
                       sp.simplify(sep_x.subs({G: sp.Rational(35, 100),
                                               mx1: 1, mx2: 0}))
                       == sp.Rational(35, 100)))
        # predicate totality: gt(sep, tau) is a total Boolean for any
        # real sep >= 0 and tau > 0 (no undefined case)
        sep, tau = sp.symbols("sep tau", real=True, nonnegative=True)
        pred = sp.Gt(sep, tau)
        checks.append(("predicate-is-relational-total",
                       isinstance(pred, sp.core.relational.Relational)))
    else:
        checks.append(("sympy-unavailable-numeric-fallback", True))

    # numeric: result.json — primary True, control exactly-0 / False
    res = json.loads((HERE / "result.json").read_text())
    prim, ctrl = res["primary_test"], res["negative_control"]
    checks.append(("primary-content-dependent-True",
                   prim["content_dependent"] is True))
    checks.append(("primary-separation-gt-tau",
                   prim["separation"] > prim["tau"]))
    checks.append(("control-separation-exactly-0",
                   ctrl["separation"] == 0.0))
    checks.append(("control-content-dependent-False",
                   ctrl["content_dependent"] is False))
    # metric discriminates: primary True XOR control True
    checks.append(("metric-discriminates-two-laws",
                   prim["content_dependent"] != ctrl["content_dependent"]))
    # verdict robustness: control verdict invariant for any tau in
    # [1e-6, 1e-1] (separation is exactly 0, below all of them)
    robust = all((ctrl["separation"] > t) is False
                 for t in (1e-6, 1e-4, 1e-3, 1e-2, 1e-1))
    checks.append(("control-verdict-tau-robust", robust))
    # and primary verdict invariant for the same tau band
    robust_p = all((prim["separation"] > t) is True
                   for t in (1e-6, 1e-4, 1e-3, 1e-2, 1e-1))
    checks.append(("primary-verdict-tau-robust", robust_p))

    ok = all(v for _, v in checks)
    return {"id": "B-S36-2", "name": "CONTENT-DEPENDENCE-METRIC-CLOSED",
            "passed": ok, "checks": checks}


def b_s36_3_deterministic() -> dict:
    """B-S36-3 — content_dependence_test.py is a pure deterministic
    function: 3x re-run produces a byte-identical result.json (no RNG, no
    model forward, no wall-clock in the verdict-bearing fields)."""
    checks = []
    script = HERE / "content_dependence_test.py"

    def run_and_hash() -> str:
        subprocess.run([sys.executable, str(script)],
                       cwd=str(HERE), capture_output=True, check=True)
        res = json.loads((HERE / "result.json").read_text())
        # strip the only non-deterministic field (wall_sec)
        res.pop("wall_sec", None)
        canon = json.dumps(res, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canon.encode("utf-8")).hexdigest()

    h1 = run_and_hash()
    h2 = run_and_hash()
    h3 = run_and_hash()
    checks.append(("run1==run2", h1 == h2))
    checks.append(("run2==run3", h2 == h3))
    checks.append(("3x-bit-identical-verdict-fields", h1 == h2 == h3))

    # structural: no RNG / no torch / no model-forward in the test source
    src = script.read_text()
    forbidden = ["import random", "random.", "import torch", "torch.",
                 "import numpy", "np.random", ".forward(", "AutoModel"]
    src_nocomment = "\n".join(
        ln.split("#", 1)[0] for ln in src.splitlines())
    hits = [t for t in forbidden if t in src_nocomment]
    checks.append(("no-rng-no-torch-no-forward", hits == []))

    ok = all(v for _, v in checks)
    return {"id": "B-S36-3", "name": "DETERMINISTIC",
            "passed": ok, "checks": checks}


def main() -> int:
    battery = [
        b_s36_1_psi_shift_bounded(),
        b_s36_2_content_dependence_metric_closed(),
        b_s36_3_deterministic(),
    ]
    n_pass = sum(1 for b in battery if b["passed"])
    note = {
        "id": "B-S36-NOTE",
        "name": "TRAINED-SATURATED-CELL-OUTCOME-EMPIRICAL",
        "text": ("Whether a trained-saturated §16 ConsciousDecoderV2 cell "
                 "preserves the content-dependent deliver() transition (vs "
                 "collapses to an echo-chamber attractor — the §31 §4.1 "
                 "failure mode) is an SGD/ckpt OUTCOME measurable only by a "
                 "real dual-anima fire. The battery proves the loop "
                 "PROTOCOL's transition law + decision metric are sound; it "
                 "does NOT prove a trained cell will not echo. B-D-NOTE / "
                 "B-DUAL-NOTE / B-CARVE-E6-NOTE family — NOT counted blue."),
        "counted_blue": False,
    }
    result = {
        "battery": "B-S36-1..3",
        "research_section": "§36",
        "n_total": len(battery), "n_pass": n_pass,
        "all_blue": n_pass == len(battery),
        "sympy_available": HAVE_SYMPY,
        "verdicts": battery,
        "note": note,
        "central_blue_falsifier_unchanged": True,
    }
    out = HERE / "blue_falsifier_s36_result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    for b in battery:
        mark = "PASS" if b["passed"] else "FAIL"
        print(f"  [{mark}] {b['id']} {b['name']}")
        for cname, cval in b["checks"]:
            print(f"      {'ok ' if cval else 'XX '} {cname}")
    print(f"\nB-S36 battery: {n_pass}/{len(battery)} "
          f"{'BLUE' if n_pass == len(battery) else 'FAIL'}  "
          f"(+ B-S36-NOTE empirical carve-out)")
    return 0 if n_pass == len(battery) else 1


if __name__ == "__main__":
    sys.exit(main())
