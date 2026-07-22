#!/usr/bin/env python3
"""phi-unfold pedestal — the ZERO-TRUTH arm for any integration claim. $0, numpy-free.

WHY A PEDESTAL IS NOT OPTIONAL
------------------------------
This repo has already lost a lane to a broken estimator rather than a real wall (the
thalamus content-relay lane), and the standing rule is that a Phi/MI verdict needs an arm
whose TRUE value is zero. Without it you cannot tell "the system integrates" from "the
estimator returns a positive number on anything".

IIT hands us that arm for free, as a theorem rather than a convention:

    a strictly feedforward system has Phi = 0, exactly.

So take the recurrent core, UNFOLD it in time into its feedforward twin -- same units,
same update rule, same input-output behaviour over the horizon, but every cycle replaced
by a chain of copies -- and measure again. The twin MUST read ~0. If it does not, the
estimator is broken and no positive reading from it means anything.

  core (cyclic)         Phi > 0 expected
  unfolded twin         Phi == 0 REQUIRED   <- if this fails, stop; the number is noise

WHAT THIS FILE MEASURES, HONESTLY
---------------------------------
NOT faithful IIT-4. The faithful big_phi lives in `stdlib/` and is the only thing allowed
to cement a number (`a_phi_iit4_tool`). This is a transparent, small, standard
effective-information-over-the-MIP measure:

    EI(S)   = H over the distribution of next states induced by a UNIFORM intervention
              on current states (deterministic system, so the conditional term is 0)
    Phi     = min over bipartitions of I(Y_A ; Y_B), the mutual information between the
              two parts' NEXT states under that same uniform intervention

Phi is then non-negative by construction and exactly zero iff the mechanism FACTORISES
across some cut -- which is what a feedforward system does and a cycle does not. The
VALUE is DIRECTIONAL and means nothing on its own. What is load-bearing is the CONTROL
STRUCTURE: whatever measure you plug in, the unfolded twin has to collapse, and this file
is the harness that checks it. (It already earned that keep: the first version of this
measure could go NEGATIVE, and the pedestal is what exposed it -- see phi_mip.)
"""
import itertools
import math
import sys

EPS = 1e-9


def tpm(n, step):
    """Deterministic transition map over all 2^n states. step(state_tuple) -> tuple."""
    states = list(itertools.product((0, 1), repeat=n))
    return {s: tuple(step(s)) for s in states}


def _entropy(counts, total):
    h = 0.0
    for c in counts.values():
        if c:
            p = c / total
            h -= p * math.log2(p)
    return h


def ei(n, t, units=None):
    """Effective information over `units`: H of the next-state distribution induced by a
    UNIFORM intervention on current states. Deterministic system, so the conditional term
    is zero and EI is just that entropy."""
    units = tuple(range(n)) if units is None else tuple(units)
    if not units:
        return 0.0
    counts = {}
    for s in t:
        key = tuple(t[s][i] for i in units)
        counts[key] = counts.get(key, 0) + 1
    return _entropy(counts, len(t))


def phi_mip(n, t):
    """Phi = min over bipartitions of I(Y_A ; Y_B) under uniform intervention.

    FIRST VERSION WAS WRONG and the pedestal caught it. It computed
    EI(whole) - (EI(A|cut) + EI(B|cut)) with the cut side RANDOMISED, and randomising
    injects entropy that the parts then count as their own -- so the parts could exceed
    the whole and Phi came out NEGATIVE (-1.0000 on ring(5)). A quantity that can go
    negative is not an integration measure.

    The mutual-information form is non-negative by construction and is exactly zero iff
    the two parts' outputs are independent -- i.e. iff the mechanism FACTORISES across
    the cut, which is what a feedforward system does and a cycle does not.
    """
    allu = list(range(n))
    best = None
    for r in range(1, n // 2 + 1):
        for A in itertools.combinations(allu, r):
            B = tuple(u for u in allu if u not in A)
            if not B:
                continue
            mi = ei(n, t, A) + ei(n, t, B) - ei(n, t, A + B)
            if best is None or mi < best:
                best = mi
    return ei(n, t), (best if best is not None else 0.0)


# --------------------------------------------------------------------------- #
# systems
# --------------------------------------------------------------------------- #
def ring(n):
    """Recurrent core: a ring where each unit XORs itself with its neighbour."""
    def step(s):
        return [s[i] ^ s[(i + 1) % n] for i in range(n)]
    return n, tpm(n, step)


def unfolded_ring(n):
    """The feedforward TWIN of ring(n), unfolded one step.

    Same units, same update rule, but the ring is CUT: unit 0 no longer reads unit n-1,
    it reads a constant. Every cycle is gone, so the graph is a chain -- and by the
    feedforward theorem the true Phi is 0.
    """
    def step(s):
        out = [s[i] ^ s[(i + 1) % n] for i in range(n)]
        out[0] = s[0]          # the cut: unit 0 stops closing the loop
        return out
    return n, tpm(n, step)


def chain(n):
    """A pure feedforward shift register: strictly no cycles at all."""
    def step(s):
        return [0] + [s[i] for i in range(n - 1)]
    return n, tpm(n, step)


def main():
    print("phi-unfold pedestal - the zero-truth arm ($0)")
    print("measure: EI over the MIP. DIRECTIONAL - not faithful IIT-4 (that lives in stdlib).")
    print("the VALUE means nothing alone; the CONTROL STRUCTURE is the point.\n")
    print("%-26s %8s %8s   %s" % ("system", "EI", "Phi", "reading"))
    print("-" * 74)
    rows = []
    for name, mk in (("ring(5) - recurrent core", lambda: ring(5)),
                     ("unfolded twin (cut ring)", lambda: unfolded_ring(5)),
                     ("chain(5) - pure feedforward", lambda: chain(5))):
        n, t = mk()
        e, p = phi_mip(n, t)
        rows.append((name, p))
        tag = "integrated" if p > EPS else "ZERO (as the theorem requires)"
        print("%-26s %8.4f %8.4f   %s" % (name, e, p, tag))
    print("-" * 74)
    core = dict(rows)["ring(5) - recurrent core"]
    twin = dict(rows)["unfolded twin (cut ring)"]
    ff = dict(rows)["chain(5) - pure feedforward"]
    print()
    if core <= EPS:
        print("INSTRUMENT-DEAD - the recurrent core itself reads 0. The measure cannot see")
        print("integration where the structure guarantees it, so read nothing from it.")
        return 1
    if twin > EPS or ff > EPS:
        print("PEDESTAL FAILED - a feedforward system read Phi > 0 (twin %.4f, chain %.4f)."
              % (twin, ff))
        print("The theorem says both are exactly 0, so the estimator is inflating.")
        print("Every positive reading from this measure is now UNREADABLE.")
        return 1
    print("PEDESTAL HOLDS - core %.4f > 0 while both feedforward systems read exactly 0."
          % core)
    print("The measure separates a cycle from its own unfolded twin, which is the one")
    print("thing an integration estimator has to do before any positive number is worth")
    print("reading. This licenses nothing else: a pedestal is a precondition, not a result.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
