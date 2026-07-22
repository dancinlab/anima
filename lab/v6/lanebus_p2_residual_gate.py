#!/usr/bin/env python3
"""LANE-BUS P2 — does a residual gate beat the clock? $0, numpy, seconds.

WHAT P2 DECIDES
---------------
Production's emit gate is a clock. H_9401-9403 measured it: the score gate never binds
because the 30s rate limit opens first, so `emit <=> clock` and "whether to speak" has no
free variable left to measure. That is why H_9786 came back UNIDENTIFIABLE -- not because
the interior is empty, but because nothing about the decision could vary with content.

The redesign replaces the scalar drive with a RESIDUAL: the per-position divergence
between what the trunk alone would say (the reflex) and what the composed bus says. Emit
fires when the interior adds information over the reflex, above a noise floor measured on
a shuffled-store control and FROZEN before the main arm is read.

P2 asks whether that actually restores the free variable:

    content-dependence   does emitting track whether the store had anything to say?
    clock-independence   is emitting predictable from the tick index alone? (must be ~0)
    thermostat floor     a timer gate must FAIL content-dependence, by construction

DISCIPLINE, IN ORDER (this is the part that makes the number readable)
    1. run the SHUFFLED-STORE arm
    2. take its residual distribution and set the threshold at its 95th percentile
    3. FREEZE it -- print it before the main arm runs
    4. only then read the main arm

Setting the floor after seeing the main arm would be tune-to-green, and this repo has a
standing rule against re-freezing a gate that has already been read.

MEASURES (DIRECTIONAL; lab/v6 is a sandbox)
    residual   symmetric KL between reflex softmax and composed softmax at the answer slot
    I(content;emit)  mutual information, in bits, between "the store had a relevant fact"
                     and "the gate fired"
    I(tick;emit)     the same against the tick index -- the clock's share
"""
import numpy as np

V = 16
N_TICK = 600
SEEDS = (7, 11, 4302)
P_CONTENT = 0.35           # fraction of ticks where the store actually holds something
EPS = 1e-12


def softmax(z):
    z = z - z.max(axis=-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=-1, keepdims=True)


def sym_kl(p, q):
    p = np.clip(p, EPS, 1); q = np.clip(q, EPS, 1)
    return ((p - q) * (np.log(p) - np.log(q))).sum(axis=-1)


def mutual_info(x, y):
    """MI in bits between two binary vectors."""
    n = len(x)
    h = 0.0
    for a in (0, 1):
        for b in (0, 1):
            nab = float(((x == a) & (y == b)).sum())
            if nab == 0:
                continue
            na = float((x == a).sum()); nb = float((y == b).sum())
            h += (nab / n) * np.log2((nab * n) / (na * nb))
    return max(h, 0.0)


def episode(seed, shuffled=False):
    """Each tick: the trunk emits a reflex row; on `content` ticks the store holds a fact
    and the lane writes it onto the bus. shuffled=True severs the fact from the tick, so
    the lane still writes with the same statistics but about the wrong thing."""
    rng = np.random.default_rng(seed)
    reflex = rng.normal(0, 1.0, (N_TICK, V))
    content = (rng.random(N_TICK) < P_CONTENT)
    facts = rng.integers(0, V, N_TICK)
    write = np.zeros((N_TICK, V))
    idx = np.where(content)[0]
    if shuffled:
        # same number of writes, same magnitudes -- but placed on ticks chosen independently
        idx = rng.permutation(N_TICK)[:len(idx)]
    write[idx, facts[idx]] += 4.0
    composed = reflex + write
    resid = sym_kl(softmax(composed), softmax(reflex))
    return content.astype(int), resid


def run(seed):
    # --- 1. noise floor from the SHUFFLED arm, frozen before the main arm is touched ----
    _, resid_shuf = episode(seed, shuffled=True)
    floor = float(np.percentile(resid_shuf, 95))

    # --- 2. main arm -------------------------------------------------------------------
    content, resid = episode(seed, shuffled=False)
    emit_resid = (resid > floor).astype(int)

    # --- 3. the two floors that must FAIL ---------------------------------------------
    tick = np.arange(N_TICK)
    emit_clock = (tick % 3 == 0).astype(int)                 # thermostat: a timer
    rate = emit_resid.mean()
    emit_rand = (np.random.default_rng(seed + 1).random(N_TICK) < rate).astype(int)

    return dict(
        floor=floor,
        rate=float(rate),
        mi_resid=mutual_info(content, emit_resid),
        mi_clock=mutual_info(content, emit_clock),
        mi_rand=mutual_info(content, emit_rand),
        tick_leak=mutual_info((tick % 3 == 0).astype(int), emit_resid),
        shuf_rate=float((resid_shuf > floor).mean()),
    )


def main():
    print("LANE-BUS P2 - residual gate vs the clock ($0, DIRECTIONAL)\n")
    rs = [run(s) for s in SEEDS]
    k = lambda n: float(np.mean([r[n] for r in rs]))
    print("noise floor from the SHUFFLED-store arm, frozen before the main arm:")
    print("  floor = %.4f (95th pct of shuffled residual) · shuffled fires %.3f of ticks"
          % (k("floor"), k("shuf_rate")))
    print()
    print("%-34s %9s" % ("gate", "I(content;emit) bits"))
    print("-" * 58)
    print("%-34s %9.4f   <- THE MEASUREMENT" % ("residual gate", k("mi_resid")))
    print("%-34s %9.4f   thermostat floor, must fail" % ("clock (every 3rd tick)", k("mi_clock")))
    print("%-34s %9.4f   rate-matched noise, must fail" % ("random, rate-matched", k("mi_rand")))
    print("-" * 58)
    print("  residual gate fires on %.3f of ticks (content ticks are %.2f)"
          % (k("rate"), P_CONTENT))
    print("  I(tick;emit) for the residual gate = %.4f bits  <- the clock's share" % k("tick_leak"))
    print()
    if k("mi_resid") < 0.05:
        print("KILL - the residual gate carries %.4f bits about content. Whether to speak" % k("mi_resid"))
        print("is still not a function of what there is to say.")
        return 1
    if k("mi_clock") > 0.05 or k("mi_rand") > 0.05:
        print("CONTROL-LEAK - a timer (%.4f) or rate-matched noise (%.4f) also tracks"
              % (k("mi_clock"), k("mi_rand")))
        print("content, so the task is leaking and the main number is unreadable.")
        return 1
    if k("tick_leak") > 0.05:
        print("CLOCK-BOUND - the residual gate is %.4f bits predictable from the tick index"
              % k("tick_leak"))
        print("alone, so it has not escaped the clock.")
        return 1
    print("PASSES - the residual gate carries %.4f bits about content while a timer carries"
          % k("mi_resid"))
    print("%.4f and rate-matched noise carries %.4f. Its dependence on the tick index is"
          % (k("mi_clock"), k("mi_rand")))
    print("%.4f bits, so it is reading the interior rather than the schedule." % k("tick_leak"))
    print()
    print("What this restores is the FREE VARIABLE that H_9786 found missing: whether to")
    print("speak now varies with what there is to say, which is the precondition for the")
    print("question being identifiable at all. It is not a claim that the decision is")
    print("well-made, only that it is no longer a clock reading itself.")
    print()
    print("Floor discipline: the threshold came from the shuffled-store arm and was frozen")
    print("before the main arm was read, so it cannot have been tuned to this result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
