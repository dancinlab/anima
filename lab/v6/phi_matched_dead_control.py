#!/usr/bin/env python3
"""Phi-matched-but-functionally-dead control — the arm that stops Phi from proving function.

WHAT THIS CONTROL IS FOR
------------------------
The pedestal (V6_4) shows the estimator can tell a cycle from its unfolded twin. That is a
precondition, not a licence. It leaves the more dangerous confusion untouched:

    "this system integrates"      -- a claim about internal structure
    "this system does something"  -- a claim about the world

Phi speaks only to the first. So build the arm that makes the gap visible: a twin with the
SAME Phi that is functionally DEAD. If a case rests on "Phi > 0", the dead twin has the
same Phi and does nothing, and the case evaporates.

    core          Phi > 0   AND   function > 0
    matched-dead  Phi ==          function == 0    <- Phi alone licenses nothing

⚠️ THE MISTAKE THIS FILE MADE, AND WHY IT IS KEPT IN THE RECORD
---------------------------------------------------------------
Three constructions in a row produced what looked like a deep structural law:

    drive into ONE unit          Phi 1.0000 -> 0.0000,  function 1.0000
    drive into TWO units (sym)   Phi stays 1.0000,      function 0.0000
    yoked driver                 Phi 0.0000,            function 0.0000

Read naively: "integration and openness to the world trade off, bit for bit." It held
across xor AND three nonlinear cells (maj, and, or-and), which made it look general.

It was an ARTIFACT of the measure. Averaging over the input treats it as noise INSIDE the
system, so the driven unit becomes an independent random bit -- and since Phi is a MINIMUM
over bipartitions, the cut isolating that one unit reads I = 0 and drags the whole score
to zero. Cell type was irrelevant; any single noise-driven unit zeroes a min-over-cuts
measure.

IIT does not do that. External inputs are BACKGROUND CONDITIONS, held FIXED, not
randomised inside the system. Conditioning instead of averaging:

    driver held FIXED at 0   Phi 1.0000
    driver held FIXED at 1   Phi 1.0000     <- integration intact at both backgrounds
    output distributions differ between backgrounds  <- and the world still reaches it

So the core has Phi AND function at once, and the "trade-off law" was a bug in how I
averaged. Kept here because the near-miss is the lesson: a result that survives four cell
types can still be a property of the estimator rather than of the system, and the way to
tell is to read what the measure actually does to inputs.

CONSTRUCTION (after the fix)
----------------------------
Ring of XOR units; unit 0 also XORs a driving bit that is a BACKGROUND CONDITION.
  core         background = the real input
  matched-dead background = a constant, whatever the input is
Both are the same ring at a fixed background, so Phi matches by construction. Only the
core's output distribution varies with the input, so only the core has function.

MEASURES (both DIRECTIONAL; the faithful big_phi lives in stdlib, `a_phi_iit4_tool`)
    Phi       min over bipartitions of I(Y_A ; Y_B) at a FIXED background
    function  whether the output distribution moves when the input moves (total variation)
"""
import itertools
import math
import sys

EPS = 1e-9
N = 5


def _entropy(counts, total):
    return -sum((c / total) * math.log2(c / total) for c in counts.values() if c)


def outputs(n, drv):
    """Every next-state, over all current states, with the driver FIXED as background."""
    out = []
    for s in itertools.product((0, 1), repeat=n):
        nxt = [s[i] ^ s[(i + 1) % n] for i in range(n)]
        nxt[0] ^= drv
        out.append(tuple(nxt))
    return out


def _ent_units(rows, units):
    c = {}
    for nx in rows:
        k = tuple(nx[i] for i in units)
        c[k] = c.get(k, 0) + 1
    return _entropy(c, len(rows))


def phi(n, rows):
    """min over bipartitions of I(Y_A ; Y_B) — internal integration at this background."""
    best = None
    for r in range(1, n // 2 + 1):
        for A in itertools.combinations(range(n), r):
            B = tuple(x for x in range(n) if x not in A)
            if not B:
                continue
            mi = _ent_units(rows, A) + _ent_units(rows, B) - _ent_units(rows, A + B)
            best = mi if best is None or mi < best else best
    return best or 0.0


def function(driver_of_input):
    """Does the world reach the system? Total variation between the output distributions
    the two input values induce. Zero iff the input cannot move the system at all."""
    def dist(inp):
        c = {}
        for nx in outputs(N, driver_of_input(inp)):
            c[nx] = c.get(nx, 0) + 1
        t = sum(c.values())
        return {k: v / t for k, v in c.items()}
    a, b = dist(0), dist(1)
    keys = set(a) | set(b)
    return 0.5 * sum(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in keys)


def main():
    print("Phi-matched-but-functionally-dead control ($0)")
    print("Phi at FIXED backgrounds (IIT treats inputs as background, not internal noise)")
    print("both measures DIRECTIONAL - faithful big_phi lives in stdlib (a_phi_iit4_tool)\n")

    arms = {
        "core (background = input)": lambda inp: inp,
        "matched-dead (background fixed)": lambda inp: 0,
    }
    print("%-34s %10s %12s" % ("system", "Phi", "function"))
    print("-" * 60)
    res = {}
    for name, drv in arms.items():
        # Phi is a property of the system AT a background; report it per background and
        # require agreement, so a background-dependent Phi cannot hide inside an average.
        phis = [phi(N, outputs(N, drv(i))) for i in (0, 1)]
        p = phis[0] if abs(phis[0] - phis[1]) < 1e-12 else float("nan")
        f = function(drv)
        res[name] = (p, f, phis)
        print("%-34s %10.4f %12.4f" % (name, p, f))
    print("-" * 60)
    (pc, fc, _) = res["core (background = input)"]
    (pd, fd, _) = res["matched-dead (background fixed)"]
    print()
    if not (pc > EPS):
        print("INSTRUMENT-DEAD - the core reads Phi 0; nothing to control against.")
        return 1
    if abs(pc - pd) > 1e-9:
        print("CONTROL INVALID - Phi did not match (%.4f vs %.4f)." % (pc, pd))
        return 1
    if fd > EPS:
        print("CONTROL INVALID - the dead twin still has function %.4f." % fd)
        return 1
    if fc <= EPS:
        print("CONTROL INVALID - the core has no function either (%.4f), so there is no" % fc)
        print("gap to demonstrate.")
        return 1
    print("CONTROL HOLDS - Phi matches EXACTLY (%.4f) while function goes %.4f -> %.4f."
          % (pc, fc, fd))
    print()
    print("The two systems are indistinguishable on Phi and maximally different on whether")
    print("the world reaches them. So any argument of the form 'Phi > 0, therefore the")
    print("system does X' is refuted by construction. Phi is a claim about internal")
    print("structure ONLY; function has to be earned on its own axis, orthogonally.")
    print()
    print("What this does NOT say: nothing about whether the core's function is the RIGHT")
    print("function, only that it has one. A screen may KILL, never GREEN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
