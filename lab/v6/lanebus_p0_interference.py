#!/usr/bin/env python3
"""LANE-BUS P0 — the bus-interference screen. $0, numpy, seconds. ABORT-ALL gate.

WHAT P0 DECIDES
---------------
The redesign puts every lane's output on ONE shared surface: the pre-softmax logit row.
Lanes write ADDITIVELY, and the design's claim about collisions is specific:

    overlapping claims are visible as measurable DISAGREEMENT, not silent corruption.

That claim is the load-bearing one, because if two lanes can quietly corrupt each other at
a contested position, then every downstream phase (P1 arity, P2 residual gate, P3
discharge) is built on a surface whose readings cannot be trusted. So P0 runs first and
carries ABORT-ALL authority.

Three things get measured, in this order:

    1. each lane ALONE            positive control -- if a lane cannot hit its own target
                                  by itself, nothing else here is readable
    2. both lanes on the bus      at UNCONTESTED positions (they claim different spans)
                                  and at CONTESTED ones (both claim the same position)
    3. detectability at contested positions -- can an observer tell, from the bus alone,
       that a collision happened? This is the actual claim under test.

    silent corruption  = wrong answer AND the bus looks normal   -> KILL, abort the plan
    visible disagreement = wrong answer BUT the bus says so      -> survivable, measurable

WHY "VISIBLE" IS ENOUGH
-----------------------
It is not a claim that collisions are harmless. It is the weaker, checkable claim that
they are INSTRUMENTED: a contested position announces itself, so a later phase can gate on
it, route around it, or report it as INVALID instead of quietly scoring it as a result.
This repo has lost campaigns to numbers that were wrong without saying so.

MEASURES (all DIRECTIONAL -- lab/v6 is a sandbox; only anima-py cements)
    accuracy      argmax of the composed logit row == the lane's target
    margin        top1 - top2 of the composed row (how decided the bus is)
    contenders    how many coordinates sit within 1.0 of the row's max -- readable from
                  the BUS ALONE, with no access to the lanes or the targets
"""
import numpy as np

V = 16                 # vocabulary
N_POS = 12             # positions per sequence
N_SEQ = 400
SEEDS = (7, 11, 4302)
EPS = 1e-9


def make_task(rng, contested_frac=0.0):
    """Each position carries a cue: 'a' (lane A owns it), 'b' (lane B owns it), or 'ab'
    (BOTH claim it -- the contested case). Targets differ per lane, so a collision has a
    right answer for each lane and they cannot both win."""
    cues, tgt_a, tgt_b = [], [], []
    for _ in range(N_SEQ):
        c, ta, tb = [], [], []
        for _p in range(N_POS):
            r = rng.random()
            if r < contested_frac:
                c.append("ab")
            elif r < contested_frac + (1 - contested_frac) / 2:
                c.append("a")
            else:
                c.append("b")
            ta.append(rng.integers(0, V // 2))          # lane A targets the low half
            tb.append(rng.integers(V // 2, V))          # lane B targets the high half
        cues.append(c); tgt_a.append(ta); tgt_b.append(tb)
    return cues, np.array(tgt_a), np.array(tgt_b)


def lane_write(cues, targets, owner, gate_mode, rng):
    """A lane's additive contribution to the bus.

    An ORACLE lane: it knows its own target, because P0 is not testing whether a lane can
    learn -- that is P1. P0 tests what happens on the SURFACE when two competent lanes
    meet. Giving both lanes oracle competence is the strongest possible setting for the
    bus, so a failure here is a property of the bus itself.

    gate_mode 'naive'      -> write at every position, claimed or not
              'negotiated' -> write only where this lane owns the cue; at a contested
                              position both still write (that IS the contest)
    """
    W = np.zeros((N_SEQ, N_POS, V))
    for i, seq in enumerate(cues):
        for p, c in enumerate(seq):
            mine = (owner in c)
            if gate_mode == "naive" or mine:
                W[i, p, targets[i, p]] += 3.0
    return W


def run(seed, contested_frac, gate_mode):
    rng = np.random.default_rng(seed)
    cues, ta, tb = make_task(rng, contested_frac)
    reflex = rng.normal(0, 0.5, (N_SEQ, N_POS, V))       # the trunk's own logit row
    WA = lane_write(cues, ta, "a", gate_mode, rng)
    WB = lane_write(cues, tb, "b", gate_mode, rng)

    def score(bus, targets, mask):
        if mask.sum() == 0:
            return float("nan"), float("nan")
        pred = bus.argmax(axis=2)
        acc = float((pred[mask] == targets[mask]).mean())
        srt = np.sort(bus, axis=2)
        margin = float((srt[..., -1] - srt[..., -2])[mask].mean())
        return acc, margin

    owns_a = np.array([[("a" in c) for c in s] for s in cues])
    owns_b = np.array([[("b" in c) for c in s] for s in cues])
    contested = np.array([[(c == "ab") for c in s] for s in cues])
    clean_a = owns_a & ~contested
    clean_b = owns_b & ~contested

    solo_a = score(reflex + WA, ta, clean_a)[0]
    solo_b = score(reflex + WB, tb, clean_b)[0]
    bus = reflex + WA + WB
    both_a = score(bus, ta, clean_a)[0]
    both_b = score(bus, tb, clean_b)[0]

    # contested positions: neither lane can be "right"; the question is whether the bus SAYS so
    if contested.sum():
        c_acc_a = score(bus, ta, contested)[0]
        c_margin = score(bus, ta, contested)[1]
        clean_margin = score(bus, ta, clean_a)[1]
        # A detector must read the BUS ALONE -- no lane access, no targets. Count how many
        # coordinates sit within 1.0 of the row max: one lane boosting one coordinate
        # leaves a single contender; two lanes boosting different coordinates leave two.
        #
        # (The first version of this file used |writeA - writeB| and reported it as if it
        #  discriminated. It does not -- it reads 3.0000 on contested AND uncontested
        #  positions, because at an uncontested slot one lane writes 3 and the other 0.
        #  It also peeked at the lanes, which a bus-alone detector may not do. The printed
        #  conclusion asserted a rise that the numbers flatly contradicted; the fix is this
        #  metric, and the lesson is that a detector has to be checked on the arm where it
        #  is supposed to stay FLAT, not only where it is supposed to move.)
        near = (bus.max(axis=2, keepdims=True) - bus) < 1.0
        cont_n = near.sum(axis=2).astype(float)
        dis_contested = float(cont_n[contested].mean())
        dis_clean = float(cont_n[clean_a].mean())
    else:
        c_acc_a = c_margin = clean_margin = dis_contested = dis_clean = float("nan")
    return dict(solo_a=solo_a, solo_b=solo_b, both_a=both_a, both_b=both_b,
                c_acc=c_acc_a, c_margin=c_margin, clean_margin=clean_margin,
                dis_contested=dis_contested, dis_clean=dis_clean)


def mean(rs, k):
    return float(np.nanmean([r[k] for r in rs]))


def main():
    print("LANE-BUS P0 - bus-interference screen ($0, DIRECTIONAL, ABORT-ALL gate)\n")

    print("STEP 1 - positive control: can each lane hit its own target alone?")
    rs = [run(s, 0.0, "negotiated") for s in SEEDS]
    sa, sb = mean(rs, "solo_a"), mean(rs, "solo_b")
    print("  lane A alone %.4f   lane B alone %.4f" % (sa, sb))
    if sa < 0.99 or sb < 0.99:
        print("  INSTRUMENT-DEAD - a lane cannot hit its own target by itself.")
        print("  Nothing below is readable (positive-control-before-reading-a-negative).")
        return 1
    print("  OK\n")

    print("STEP 2 - both lanes on one bus, at UNCONTESTED positions")
    for mode in ("naive", "negotiated"):
        rs = [run(s, 0.0, mode) for s in SEEDS]
        print("  %-11s  A %.4f -> %.4f    B %.4f -> %.4f"
              % (mode, mean(rs, "solo_a"), mean(rs, "both_a"),
                 mean(rs, "solo_b"), mean(rs, "both_b")))
    print()

    print("STEP 3 - CONTESTED positions (both lanes claim the same slot)")
    rs = [run(s, 0.30, "negotiated") for s in SEEDS]
    c_acc = mean(rs, "c_acc")
    c_m, cl_m = mean(rs, "c_margin"), mean(rs, "clean_margin")
    d_c, d_cl = mean(rs, "dis_contested"), mean(rs, "dis_clean")
    print("  accuracy at contested (lane A's target)   %.4f" % c_acc)
    print("  bus margin   contested %.4f   uncontested %.4f" % (c_m, cl_m))
    print("  contenders   contested %.4f   uncontested %.4f  (bus-alone detector)" % (d_c, d_cl))
    print()

    # the actual claim: is a collision DETECTABLE from the bus, without knowing targets?
    margin_moves = (cl_m - c_m) > 0.5
    contenders_move = (d_c - d_cl) > 0.5
    detectable = margin_moves or contenders_move
    naive = [run(s, 0.0, "naive") for s in SEEDS]
    naive_hurts = (mean(naive, "solo_a") - mean(naive, "both_a")) > 0.01

    print("=" * 74)
    if not detectable:
        print("KILL - collisions are SILENT. The bus at a contested position looks like the")
        print("bus at an uncontested one (contenders %.4f vs %.4f, margin %.4f vs %.4f),"
              % (d_c, d_cl, c_m, cl_m))
        print("so a later phase would score a corrupted position as a clean result.")
        print("ABORT-ALL: P1-P3 are built on this surface and cannot be trusted.")
        return 1
    print("SURVIVES - collisions are VISIBLE, not silent.")
    if contenders_move:
        print("  contenders rise %.4f -> %.4f" % (d_cl, d_c))
    if margin_moves:
        print("  margin falls %.4f -> %.4f" % (cl_m, c_m))
    print("  at contested slots, so the position announces itself on the bus WITHOUT")
    print("  anyone seeing the lanes or the targets. A later phase can gate on it, route")
    print("  around it, or report INVALID -- instead of quietly scoring it.")
    if naive_hurts:
        print("  Note: the naive mode (write everywhere, no ownership) DOES degrade the")
        print("  other lane, so position negotiation is load-bearing, not decoration.")
    print()
    print("This is not a GREEN for the bus. P0 only had authority to KILL, and it did not")
    print("fire. Whether a lane can LEARN its write is P1, and this file gave both lanes")
    print("oracle competence precisely so that P0 tests the surface and nothing else.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
