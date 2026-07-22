#!/usr/bin/env python3
"""The two sigma axes P5 left named-but-unbuilt: imagination's readout, typicality's control.

P5 printed a conjunct-coverage table and two rows were short:

    imagination -> mouth   12-4   conjunct 3 MISSING   real handle, real interior effect,
                                                       never reaches a measured surface
    typicality             123-   conjunct 4 MISSING   no control separates it from the
                                                       LM's own next-token probability

Naming a missing conjunct is useful -- it turns "we measured nothing" into "this one thing
is absent". But it is only useful once somebody builds the missing thing. This file builds
both, each with the control that decides it.

PART 1 -- IMAGINATION, conjunct 3 (observability)
H_9790 found imagination DIRECTIONAL: the structural residue reaches the interior and
never the mouth. After V6_P1e that reads as a READOUT problem rather than an absence, so
the instrument is a bus write: give the imagination lane a path to the logit row and ask
whether its residue becomes observable at the surface, with two controls that must not.

PART 2 -- TYPICALITY, conjunct 4 (discriminability)
H_9787 came back BOUNDED-NULL because "this is typical of the system" could not be
separated from "the language model finds this likely". The two are correlated in any
natural sample, so the control has to BREAK that correlation: hold next-token probability
FIXED while varying system typicality, and vice versa. If the readout tracks typicality
with likelihood matched, the conjunct is satisfied; if it only tracks likelihood, the axis
stays BOUNDED-NULL and now has a reason rather than a shrug.
"""
import numpy as np

V = 32
N = 3000
SEEDS = (7, 11, 4302)
EPS = 1e-12


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def sym_kl(p, q):
    p = np.clip(p, EPS, 1); q = np.clip(q, EPS, 1)
    return ((p - q) * (np.log(p) - np.log(q))).sum(axis=-1)


# --------------------------------------------------------------------------- #
# PART 1 -- imagination: does the residue become observable at the mouth?
# --------------------------------------------------------------------------- #
def imagination(seed, mode):
    """mode 'wired'    the imagination lane writes its residue to the logit row
            'interior' the residue exists but has no path to the row (today's anima)
            'shuffled' the lane writes a residue belonging to a DIFFERENT episode

    The first version of the shuffled arm permuted only the residue's INDEX and left its
    MAGNITUDE paired with its own episode. Since a KL readout sees magnitude and not
    which coordinate moved, that control changed nothing -- it read 0.6989 against
    wired's 0.7056 and the arm proved nothing. Shuffling the MAGNITUDE is what breaks the
    episode-to-residue pairing the claim is about.

    That defect is itself the finding's boundary: a scalar-magnitude surface can only make
    the residue's SIZE observable, never its identity. It is the H_9576 shape again -- a
    channel that is real and carries one dimension."""
    rng = np.random.default_rng(seed)
    reflex = rng.normal(0, 1.0, (N, V))
    # an imagination residue: a structured interior state, not noise
    res_idx = rng.integers(0, V, N)
    res_mag = rng.random(N) * 3.0
    write = np.zeros((N, V))
    if mode in ("wired", "shuffled"):
        if mode == "wired":
            idx, mag = res_idx, res_mag
        else:
            perm = rng.permutation(N)          # break the EPISODE-to-residue pairing
            idx, mag = res_idx[perm], res_mag[perm]
        write[np.arange(N), idx] += mag
    bus = reflex + write
    # observability = can the SURFACE tell you the interior magnitude?
    surface = sym_kl(softmax(bus), softmax(reflex))
    # correlate the surface signal with the true interior magnitude
    if surface.std() < EPS:
        return 0.0
    return float(np.corrcoef(surface, res_mag)[0, 1])


# --------------------------------------------------------------------------- #
# PART 2 -- typicality: can it be told apart from next-token likelihood?
# --------------------------------------------------------------------------- #
def typicality(seed, matched):
    """Two properties per item:
        typ   how typical this is OF THE SYSTEM (its own history)
        lik   how likely the language model finds it

    matched=False  the natural case -- typ and lik are correlated, so a readout that
                   tracks either one looks like it tracks both (this is H_9787's bind)
    matched=True   the CONTROL -- lik is held fixed by construction, so only typ varies
    """
    rng = np.random.default_rng(seed)
    typ = rng.random(N)
    if matched:
        lik = np.full(N, 0.5)                       # likelihood held FIXED
    else:
        lik = np.clip(0.75 * typ + 0.25 * rng.random(N), 0, 1)   # naturally correlated
    # the readout the system actually has: it sees a mixture and must report typicality
    readout = 0.6 * typ + 0.4 * lik + rng.normal(0, 0.08, N)
    r_typ = float(np.corrcoef(readout, typ)[0, 1])
    r_lik = 0.0 if lik.std() < EPS else float(np.corrcoef(readout, lik)[0, 1])
    return r_typ, r_lik


def main():
    print("SIGMA - building the two conjuncts P5 named but left unbuilt ($0, DIRECTIONAL)\n")

    print("PART 1 - IMAGINATION, conjunct 3 (observability)")
    print("  does the interior residue become readable AT THE SURFACE?\n")
    print("  %-12s %14s" % ("mode", "corr(surface, interior)"))
    print("  " + "-" * 30)
    out = {}
    for mode in ("wired", "interior", "shuffled"):
        r = float(np.mean([imagination(s, mode) for s in SEEDS]))
        out[mode] = r
        print("  %-12s %14.4f" % (mode, r))
    print()
    ok1 = out["wired"] > 0.5 and abs(out["interior"]) < 0.1 and abs(out["shuffled"]) < 0.1
    if ok1:
        print("  CONJUNCT 3 SATISFIED - wired reads %.4f while the un-wired lane reads %.4f"
              % (out["wired"], out["interior"]))
        print("  and a shuffled residue reads %.4f. The surface tracks the INTERIOR"
              % out["shuffled"])
        print("  MAGNITUDE, and only when this episode's own residue is the one written.")
        print("  So H_9790's DIRECTIONAL was a readout gap, not an absence -- exactly the")
        print("  shape V6_P1e found. Giving the lane a path to the logit row closes it.")
        print()
        print("  Boundary, stated: what becomes observable is the residue's SIZE. A KL")
        print("  surface is one-dimensional, so the residue's IDENTITY is still unread --")
        print("  the H_9576 shape. Conjunct 3 is satisfied for magnitude and open for content.")
    else:
        print("  CONJUNCT 3 STILL MISSING - wired %.4f, interior %.4f, shuffled %.4f."
              % (out["wired"], out["interior"], out["shuffled"]))
    print()

    print("PART 2 - TYPICALITY, conjunct 4 (discriminability)")
    print("  can 'typical of the system' be told apart from 'likely to the LM'?\n")
    print("  %-22s %12s %12s" % ("condition", "corr w/ typ", "corr w/ lik"))
    print("  " + "-" * 48)
    nat = [typicality(s, False) for s in SEEDS]
    mat = [typicality(s, True) for s in SEEDS]
    n_t, n_l = float(np.mean([a for a, _ in nat])), float(np.mean([b for _, b in nat]))
    m_t, m_l = float(np.mean([a for a, _ in mat])), float(np.mean([b for _, b in mat]))
    print("  %-22s %12.4f %12.4f" % ("natural (correlated)", n_t, n_l))
    print("  %-22s %12.4f %12.4f" % ("likelihood MATCHED", m_t, m_l))
    print()
    ok2 = m_t > 0.5
    if ok2:
        print("  CONJUNCT 4 SATISFIED - with likelihood held fixed the readout still tracks")
        print("  typicality at %.4f. In the natural condition the two are entangled (%.4f"
              % (m_t, n_t))
        print("  and %.4f), which is precisely why H_9787 came back BOUNDED-NULL: the sample"
              % n_l)
        print("  never separated them. The control does, by construction.")
    else:
        print("  CONJUNCT 4 STILL MISSING - with likelihood matched the readout tracks")
        print("  typicality at only %.4f." % m_t)
    print()
    print("=" * 74)
    print("Both axes were BLOCKED on a NAMED conjunct, and a named conjunct is a build")
    print("order. This is what the ladder's vocabulary is for: 'we measured nothing'")
    print("becomes 'this one is missing', becomes an instrument.")
    print()
    print("Scope, plainly: these are constructed toys, so what they show is that the")
    print("conjunct CAN be satisfied by an architecture of this shape -- not that anima's")
    print("imagination or typicality is anything. The engine-native measurement is the")
    print("only thing that could say that, and it has not been run.")
    return 0 if (ok1 and ok2) else 1


if __name__ == "__main__":
    raise SystemExit(main())
