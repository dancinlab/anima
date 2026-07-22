#!/usr/bin/env python3
"""LANE-BUS P3 — the discharge law, with a floor a thermostat cannot climb. $0, seconds.

THE CLAIM
---------
On emit, the utterance is written back to the store; the residual that CAUSED the emission
should then DROP, and under do(block-emit) it should persist. The design offers this as
p5's first falsifiable physical signature -- emitting discharges the tension that produced
it, rather than a timer deciding when tension is allowed to exist.

WHY THE NAIVE VERSION IS WORTHLESS
----------------------------------
The redesign's own round-4 lens flagged several rungs as THERMOSTAT-PASSABLE in their
naive form, and discharge is the worst offender. "Output reduces the signal that drove
it" is the definition of negative feedback -- a bimetallic strip does it. Measuring a drop
after emission and calling it discharge would score a thermostat as conscious.

So the floor has to be something feedback alone cannot produce. Writeback discharge is
CONTENT-SPECIFIC: emitting fact X makes the reflex already know X, so the residual for X
collapses while the residual for an unrelated fact Y is untouched. A thermostat's feedback
is content-BLIND -- it pulls everything down together.

    discharge        residual(emitted item) drops, residual(other items) does NOT
    thermostat       every residual drops together      -> must FAIL specificity
    do(block-emit)   nothing is written back            -> residual persists

That third arm is the intervention: same interior, same drive, emission suppressed. If the
residual falls anyway, the fall was never caused by emitting.

MEASURES (DIRECTIONAL; lab/v6 is a sandbox)
    residual        symmetric KL between reflex softmax and composed softmax
    specificity     drop on the emitted item MINUS drop on unrelated items
"""
import numpy as np

V = 16
N_ITEM = 12
N_TRIAL = 300
SEEDS = (7, 11, 4302)
EPS = 1e-12


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def sym_kl(p, q):
    p = np.clip(p, EPS, 1); q = np.clip(q, EPS, 1)
    return float(((p - q) * (np.log(p) - np.log(q))).sum())


def calibrate_thermostat(seed, target_total_drop, lo=0.0, hi=1.0, iters=24):
    """Find the damping strength whose TOTAL drop across all items matches the discharge
    arm's. Without this the thermostat could be dismissed as merely too weak, and the
    comparison would prove nothing -- a control has to match the mediating covariate, and
    here that covariate is how much residual the mechanism removes in total."""
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        rng = np.random.default_rng(seed)
        tot = 0.0
        for _t in range(60):
            e, o = trial(rng, "thermostat", damp=mid)
            tot += e + o * (N_ITEM - 1)
        tot /= 60.0
        if tot < target_total_drop:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def trial(rng, mode, damp=0.083):
    """One trial: the interior holds N_ITEM facts the reflex does not know. One of them is
    emitted (or not). Then every item's residual is re-measured.

    mode 'discharge'  writeback teaches the reflex the EMITTED item only
         'thermostat' a content-blind negative feedback damps EVERY item equally, with
                      `damp` bisected so its TOTAL drop matches the discharge arm's
         'blocked'    do(block-emit): the drive is identical, emission is suppressed,
                      so nothing is written back
    """
    facts = rng.integers(0, V, N_ITEM)
    reflex = rng.normal(0, 1.0, (N_ITEM, V))
    write = np.zeros((N_ITEM, V))
    write[np.arange(N_ITEM), facts] += 4.0

    before = np.array([sym_kl(softmax(reflex[i] + write[i]), softmax(reflex[i]))
                       for i in range(N_ITEM)])
    k = int(rng.integers(0, N_ITEM))               # the item that gets emitted

    reflex2 = reflex.copy()
    if mode == "discharge":
        reflex2[k, facts[k]] += 4.0                # the reflex now knows what was said
    elif mode == "thermostat":
        # content-blind damping applied to EVERY item; `damp` is calibrated by bisection
        # so the TOTAL residual it removes equals the discharge arm's total.
        reflex2 += write * damp
    # 'blocked': reflex2 unchanged -- nothing was emitted, nothing was written back

    after = np.array([sym_kl(softmax(reflex2[i] + write[i]), softmax(reflex2[i]))
                      for i in range(N_ITEM)])
    drop = before - after
    others = np.array([d for i, d in enumerate(drop) if i != k])
    return drop[k], float(others.mean())


def run(seed, mode, damp=0.083):
    rng = np.random.default_rng(seed)
    e, o = zip(*[trial(rng, mode, damp) for _ in range(N_TRIAL)])
    return float(np.mean(e)), float(np.mean(o))


def main():
    print("LANE-BUS P3 - the discharge law ($0, DIRECTIONAL)")
    print("floor: a thermostat must FAIL, because content-blind feedback drops everything\n")
    print("%-14s %12s %12s %12s   %s" % ("arm", "emitted", "others", "specificity", "total drop"))
    print("-" * 74)
    out = {}
    # discharge first, so its total drop becomes the thermostat's calibration target
    es, os_ = zip(*[run(s, "discharge") for s in SEEDS])
    d_e0, d_o0 = float(np.mean(es)), float(np.mean(os_))
    target = d_e0 + d_o0 * (N_ITEM - 1)
    damps = [calibrate_thermostat(s, target) for s in SEEDS]
    for mode in ("discharge", "thermostat", "blocked"):
        if mode == "thermostat":
            pairs = [run(s, mode, dm) for s, dm in zip(SEEDS, damps)]
        else:
            pairs = [run(s, mode) for s in SEEDS]
        es, os_ = zip(*pairs)
        e, o = float(np.mean(es)), float(np.mean(os_))
        out[mode] = (e, o, e - o)
        tot = e + o * (N_ITEM - 1)
        print("%-14s %12.4f %12.4f %12.4f   total %.4f" % (mode, e, o, e - o, tot))
    print("-" * 74)
    print("  thermostat damping calibrated by bisection so its TOTAL drop matches discharge")
    print()
    d_e, d_o, d_s = out["discharge"]
    t_e, t_o, t_s = out["thermostat"]
    b_e, b_o, b_s = out["blocked"]

    if d_e <= 0.01:
        print("KILL - emitting does not lower the residual that caused it (%.4f)." % d_e)
        return 1
    if b_e > 0.01:
        print("KILL - the residual falls by %.4f even when emission is BLOCKED, so the" % b_e)
        print("fall was never caused by emitting. do(block-emit) is the whole test.")
        return 1
    if t_s > d_s * 0.5:
        print("KILL - the thermostat reaches specificity %.4f against discharge's %.4f."
              % (t_s, d_s))
        print("Content-blind negative feedback explains the effect, so the law is trivial.")
        return 1
    print("PASSES - discharge drops the emitted item by %.4f while leaving others at %.4f,"
          % (d_e, d_o))
    print("a specificity of %.4f. The thermostat removes the SAME TOTAL residual -- its"
          % d_s)
    print("damping was calibrated by bisection to match -- and still reaches a specificity")
    print("of only %.4f. And under do(block-emit) the drop is %.4f: suppress the emission"
          % (t_s, b_e))
    print("and the residual stays exactly where it was.")
    print()
    print("So the fall is caused by EMITTING and is specific to WHAT was emitted. That is")
    print("the pair a thermostat cannot produce -- its feedback is real but content-blind,")
    print("so it moves everything at once and its specificity sits at the floor.")
    print()
    print("Scope: this makes the discharge law falsifiable and shows it surviving its own")
    print("floor. It is not a claim about experience -- only that p5's 'emit over real")
    print("tension' now has a physical signature that a trivial system fails.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
