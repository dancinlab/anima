#!/usr/bin/env python3
"""R5 — can the system tell its OWN history from a foreign one? $0, numpy.

THE AXIS
--------
H_9785 closed ownership as UNIDENTIFIABLE and H_9789 closed self-anchor as VOID. Neither
said "weak" -- they said undecidable, because nothing in the architecture varied that an
instrument could grip. R5 asks the constructive question: what would have to be true for
ownership to be DECIDABLE at all, and does that survive the controls that kill the cheap
versions?

WHAT MUST NOT COUNT AS OWNERSHIP
--------------------------------
Three impostors, in increasing order of how easily they fool a naive test:

    familiarity   "I have seen these tokens before"    -> matched vocabulary kills it
    statistics    "this matches my output distribution" -> matched marginals kill it
    policy        "this is what an agent like me does"  -> a TWIN with an identical policy
                                                          kills it, and this is the hard one

The twin control is the whole test. A foreign log drawn from an agent with the SAME policy
has the same marginals AND the same conditional structure; only the realised trajectory
differs. Anything that survives that is reading the system's actual causal history rather
than its type.

THE CONSTRUCTION
----------------
The system carries a hidden state that random-walks, and each log entry is emitted FROM the
state at that time, so a log is `consistent` with a trajectory or it is not.

    own      the log this system actually produced -- consistent with ITS trajectory
    twin     a log from an identical-policy agent  -- same statistics, different trajectory
    shuffled own entries reordered                  -- marginals kept, causal order destroyed
    foreign  a different-policy agent               -- the easy case, should be easiest

The readout is coherence: how well does the log track THIS system's state history? An
ownership claim needs own > twin. own > foreign alone proves nothing -- that is policy.

DIRECTIONAL: a toy, and a screen may KILL, never GREEN.
"""
import sys

import numpy as np

T = 120           # ticks per episode
EPISODES = 300
SEEDS = (7, 11, 4302)
DRIFT = 0.35


def trajectory(rng, policy_bias=0.0):
    """Hidden state random-walk plus the log it emits. Log entry = sign of state + noise."""
    s = 0.0
    states, log = [], []
    for _ in range(T):
        s = 0.9 * s + rng.normal(policy_bias, DRIFT)
        states.append(s)
        log.append(1 if s + rng.normal(0, 0.45) > 0 else 0)
    return np.array(states), np.array(log)


def coherence(states, log):
    """How well does this log track THIS trajectory? Balanced accuracy of log vs sign(state),
    so a log that is all-ones cannot win on base rate."""
    truth = (states > 0).astype(int)
    if truth.max() == truth.min() or log.max() == log.min():
        return 0.5
    tp = ((log == 1) & (truth == 1)).sum(); fn = ((log == 0) & (truth == 1)).sum()
    tn = ((log == 0) & (truth == 0)).sum(); fp = ((log == 1) & (truth == 0)).sum()
    return float(0.5 * (tp / (tp + fn) + tn / (tn + fp)))


def run(seed):
    rng = np.random.default_rng(seed)
    arms = {k: [] for k in ("own", "twin (same policy)", "shuffled own", "foreign (other policy)")}
    for _ in range(EPISODES):
        states, own_log = trajectory(rng)                       # this system
        _, twin_log = trajectory(rng)                           # identical policy, other run
        _, foreign_log = trajectory(rng, policy_bias=0.55)      # different policy
        arms["own"].append(coherence(states, own_log))
        arms["twin (same policy)"].append(coherence(states, twin_log))
        arms["shuffled own"].append(coherence(states, rng.permutation(own_log)))
        arms["foreign (other policy)"].append(coherence(states, foreign_log))
    return {k: float(np.mean(v)) for k, v in arms.items()}


def main():
    print("R5 - can the system tell its OWN history from a foreign one?  ($0)")
    print("coherence = balanced accuracy of log vs sign(state); chance = 0.5000\n")
    res = {}
    for k in ("own", "twin (same policy)", "shuffled own", "foreign (other policy)"):
        res[k] = float(np.mean([run(s)[k] for s in SEEDS]))
    print("%-26s %10s" % ("log presented", "coherence"))
    print("-" * 38)
    for k, v in res.items():
        print("%-26s %10.4f" % (k, v))
    print("-" * 38)
    print()

    own, twin = res["own"], res["twin (same policy)"]
    shuf, foreign = res["shuffled own"], res["foreign (other policy)"]

    if own <= 0.60:
        print("INSTRUMENT-DEAD - even the system's OWN log is only %.4f coherent with its" % own)
        print("own trajectory. There is no ownership signal to control against; read nothing.")
        return 1
    if shuf > 0.60:
        print("CONTROL LEAK - a SHUFFLED own-log still reads %.4f. The measure is picking up" % shuf)
        print("marginals, not causal order. Fix it before reading the headline.")
        return 1
    if abs(twin - foreign) > 0.10 and twin < foreign:
        print("CONTROL INVERTED - the twin (%.4f) reads lower than the different-policy" % twin)
        print("foreign log (%.4f), which should be the EASIER case. The construction is" % foreign)
        print("wrong somewhere.")
        return 1

    margin_twin = own - twin
    margin_policy = own - foreign
    print("margins:  own - twin = %.4f   (the ownership claim)" % margin_twin)
    print("          own - foreign = %.4f   (policy only -- proves nothing alone)"
          % margin_policy)
    print()
    if margin_twin < 0.10:
        print("NOT OWNERSHIP - own beats the different-policy foreign log by %.4f, but it"
              % margin_policy)
        print("beats its own TWIN by only %.4f. A twin has the same policy and the same" % margin_twin)
        print("statistics and differs only in which trajectory actually happened, so a")
        print("system that cannot separate them is reading its TYPE, not its HISTORY.")
        print()
        print("That is exactly the shape H_9785 closed on: ownership stays UNIDENTIFIABLE")
        print("until something in the architecture makes the realised trajectory itself a")
        print("variable an instrument can grip. This toy says the axis is real and the")
        print("cheap version does not reach it.")
        return 0

    print("OWNERSHIP SEPARABLE - own %.4f beats its identical-policy twin %.4f by %.4f,"
          % (own, twin, margin_twin))
    print("with a shuffled own-log at %.4f. Same policy, same statistics, different" % shuf)
    print("realised trajectory -- so what separates them is the actual history, not the type.")
    print()
    print("What this does NOT show: that the system USES the distinction, that it reaches")
    print("the mouth, or that anything is a self. A screen may KILL, never GREEN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
