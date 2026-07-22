#!/usr/bin/env python3
"""R3 — does WIDTH survive the interface, or fold to one number again? $0, numpy.

THE CLAIM UNDER TEST
--------------------
Everything in the redesign rests on one bet: replace the scalar A-vs-G tension with a
RESIDUAL — the per-position divergence between what the reflex (trunk alone) would say and
what the composed bus says, dimension V x span — and the interior finally has width an
instrument can grip.

That bet has a bad precedent. H_9576 built an 8-dimensional tension lane and it folded to
ONE BIT: the channel was real but direction was dead (rho = -0.077) and meaning never
transferred. Production is worse — s = 2*emit_drive - 1 is rank one before anything folds.

So the question is not "is a residual bigger than a scalar" (trivially yes, it has more
numbers in it). It is:

    do interventions on DIFFERENT lanes leave DISTINGUISHABLE signatures in the residual,
    and does that distinguishability SURVIVE the collapse that killed every prior attempt?

⚠️ THE FIRST VERSION OF THIS TEST WAS NOT A WIDTH TEST
------------------------------------------------------
Version one gave each lane a FIXED write, so do(A) produced a byte-identical residual every
episode. Everything separated at 1.0000 -- including the same-lane control (gain 1 vs gain
2), which proved the readout was reading MAGNITUDE, not lane IDENTITY. The harness refused
the headline and said so instead of printing the number.

Fixed by making magnitude carry NO lane information: both lanes draw their gain from the
SAME distribution each episode. Then the only stable cue for WHICH lane was touched is
WHICH POSITIONS moved -- exactly the thing a vector can see and a mean cannot.

That also upgrades the evidence from one comparison to a DOUBLE DISSOCIATION:

    identity task (which lane?)     vector should separate,  scalar should NOT
    magnitude task (how hard?)      vector should separate,  scalar SHOULD too

The second row is what makes the first readable. If the scalar failed both, it might just
be a broken readout; passing the magnitude task shows it is alive and specifically blind
to identity.

THE TEST
--------
Two lanes write additively to a shared pre-softmax logit row (the BUS). Each owns a span.
Intervene on one lane at a time -- do(lane A), do(lane B) -- and ask an observer holding
ONLY the residual to say which lane was touched.

    vector residual   the full per-position profile      <- what the design proposes
    scalar MEAN       the residual, averaged             <- literally what production does
                                                            (`_hf_mean` in hexad_forward)
    scalar NORM       the residual's L2 magnitude        <- the fairest scalar summary

⚠️ WHY THE SIGNATURES ARE ZERO-MEAN, AND WHY THAT IS A FINDING ABOUT PRODUCTION
Adding a constant to every logit is a NO-OP after softmax. So the mean component of a
logit-space residual cannot affect any output, by construction. A lane whose write has a
nonzero average is carrying a functionally-null offset, and letting it stay non-zero would
let the MEAN scalar identify lanes through a channel that cannot change a single emitted
byte -- which is exactly the kind of false positive this lab keeps catching. Centering the
signatures is therefore the correct model of a logit write, not a convenience.

It also sharpens the criticism of the current engine: production collapses its interior
with `_hf_mean`, and in logit space the mean is precisely the softmax-null direction.

If the vector separates the two interventions and the scalar does not, width genuinely
survives the interface. If BOTH separate, the width was never needed. If NEITHER does,
the fold is upstream of the representation and no interface design helps.

CONTROLS
--------
  null        do() nothing -- the observer must be at chance, or the readout is leaking
  swap        labels permuted -- must collapse to chance
  same-lane   do(A) twice with different magnitudes -- a WIDTH test must NOT call these
              different lanes; if it does, it is reading magnitude, not identity

DIRECTIONAL: a toy, and a screen may KILL, never GREEN.
"""
import sys

import numpy as np

V = 32          # vocab positions on the bus
SPAN = 6        # positions each lane claims
SEEDS = (7, 11, 4302)
TRIALS = 400


def make_lanes(rng):
    """Two lanes, each with its own span and its own logit signature over that span."""
    a_span = rng.choice(V, SPAN, replace=False)
    rest = np.setdiff1d(np.arange(V), a_span)
    b_span = rng.choice(rest, SPAN, replace=False)
    def sig():
        v = rng.normal(0, 1.0, SPAN)
        return v - v.mean()      # ZERO-MEAN: see the note below -- this is required, not tidy
    return (a_span, sig()), (b_span, sig())


def episode(rng, lane_a, lane_b, touch, gain=None):
    """One episode. `touch` in {None,'A','B'}. gain=None -> drawn from the SHARED
    distribution, so magnitude carries no information about WHICH lane was touched."""
    g = rng.uniform(0.5, 1.5) if gain is None else gain
    reflex = rng.normal(0, 1.0, V)
    composed = reflex.copy()
    for name, (span, sig) in (("A", lane_a), ("B", lane_b)):
        if touch == name:
            composed[span] += g * sig * rng.normal(1.0, 0.15, len(span))
    return composed - reflex


def run(seed, mode="identity"):
    """mode='identity'  -> do(A) vs do(B), gains from a SHARED distribution
                            (magnitude cannot identify the lane -> the width question)
       mode='magnitude' -> do(A) weak vs do(A) strong, SAME lane
                            (the readability check: a live scalar must pass this)"""
    rng = np.random.default_rng(seed)
    lane_a, lane_b = make_lanes(rng)
    X, y = [], []
    for _ in range(TRIALS):
        if mode == "identity":
            lab = rng.integers(0, 2)
            r = episode(rng, lane_a, lane_b, "A" if lab == 0 else "B")
        else:
            lab = rng.integers(0, 2)
            r = episode(rng, lane_a, lane_b, "A",
                        gain=rng.uniform(0.3, 0.7) if lab == 0 else rng.uniform(2.0, 2.4))
        X.append(r)
        y.append(lab)
    return np.array(X), np.array(y), rng


def readout(X, y, scalar=None, permute=False, rng=None):
    """Nearest-class-mean on a held-out half. scalar=True collapses the residual first."""
    if permute:
        y = rng.permutation(y)
    if scalar == "mean":
        Z = X.mean(axis=1, keepdims=True)
    elif scalar == "norm":
        Z = np.linalg.norm(X, axis=1, keepdims=True)
    else:
        Z = X
    n = len(y) // 2
    tr, te = slice(0, n), slice(n, None)
    mu = [Z[tr][y[tr] == c].mean(axis=0) for c in (0, 1)]
    if any(np.isnan(m).any() for m in mu):
        return float("nan")
    d = np.stack([((Z[te] - m) ** 2).sum(axis=1) for m in mu], axis=1)
    return float((d.argmin(axis=1) == y[te]).mean())


def main():
    print("R3 - does WIDTH survive the interface, or fold to one number again?  ($0)")
    print("chance = 0.5000 (two interventions, balanced by construction)\n")
    print("%-34s %9s %9s %9s" % ("arm", "vector", "s:mean", "s:norm"))
    print("-" * 64)

    rows = {}
    for label, mode, permute, null in (
            ("do(A) vs do(B)  [THE TEST]", "identity", False, False),
            ("  null: no do() at all", "identity", False, True),
            ("  swap: labels permuted", "identity", True, False),
            ("same-lane weak vs strong [read-chk]", "magnitude", False, False)):
        vec, sme, sno = [], [], []
        for s in SEEDS:
            X, y, rng = run(s, mode)
            if null:
                X = np.stack([episode(np.random.default_rng(s + i), *make_lanes(np.random.default_rng(s)), None)
                              for i in range(len(y))])
            vec.append(readout(X, y, scalar=None, permute=permute, rng=rng))
            sme.append(readout(X, y, scalar="mean", permute=permute, rng=rng))
            sno.append(readout(X, y, scalar="norm", permute=permute, rng=rng))
        rows[label] = (float(np.mean(vec)), float(np.mean(sme)), float(np.mean(sno)))
        print("%-34s %9.4f %9.4f %9.4f" % (label, *rows[label]))
    print("-" * 64)
    print()

    (tv, tm, tn) = rows["do(A) vs do(B)  [THE TEST]"]
    (nv, nm_, nn) = rows["  null: no do() at all"]
    (sv, sm, sn) = rows["  swap: labels permuted"]
    (mv, mm, mn) = rows["same-lane weak vs strong [read-chk]"]
    ts = max(tm, tn)      # give the scalar arms their BEST shot on identity
    ms = mn               # the norm is the scalar that should be able to do magnitude

    for nm, val in (("null vector", nv), ("null mean", nm_), ("null norm", nn),
                    ("swap vector", sv), ("swap mean", sm), ("swap norm", sn)):
        if val > 0.60:
            print("CONTROL LEAK - %s reads %.4f, above chance. The readout is seeing" % (nm, val))
            print("something other than the intervention. Read nothing else from this run.")
            return 1

    if ms <= 0.60:
        print("READOUT DEAD - the scalar cannot even do the MAGNITUDE task (%.4f)." % ms)
        print("So a scalar failure on identity would prove nothing: the collapse might just")
        print("be a broken readout. Fix the scalar arm before reading the headline.")
        return 1

    if tv <= 0.60:
        print("FOLD - even the full vector residual cannot tell do(A) from do(B) (%.4f)." % tv)
        print("The collapse is UPSTREAM of the interface, so no interface design helps.")
        print("This is the H_9576 outcome reproduced one level deeper.")
        return 0

    if ts > 0.60:
        print("WIDTH NOT NEEDED - a scalar collapse separates the lanes too (best %.4f)." % ts)
        print("The residual's extra dimensions are not carrying the distinction, so the")
        print("case for a vector interface is not made by this test.")
        return 0

    print("WIDTH SURVIVES - DOUBLE DISSOCIATION")
    print("    identity  (which lane?)   vector %.4f   mean %.4f   norm %.4f" % (tv, tm, tn))
    print("    magnitude (how hard?)     vector %.4f   mean %.4f   norm %.4f" % (mv, mm, mn))
    print()
    print("Interventions on different lanes leave DISTINGUISHABLE signatures in the full")
    print("residual, and that distinction DISAPPEARS under the scalar collapse -- which is")
    print("the collapse production performs today (s = 2*emit_drive - 1) and the one that")
    print("killed H_9576's 8-vector. So the width is doing work rather than decorating.")
    print()
    print("What this does NOT show: that the width carries MEANING, that it reaches the")
    print("mouth, or that anything is conscious. It shows one thing -- lane identity")
    print("survives the interface in a vector and dies in a scalar. A screen may KILL.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
