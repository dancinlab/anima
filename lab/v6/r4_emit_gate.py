#!/usr/bin/env python3
"""R4 — is whether-to-speak a FREE VARIABLE, or is it just the clock? $0, numpy.

WHAT R4 ASKS
------------
H_9401-9403 closed the emit-drive lane at the regime level: the G-readout margin crack is
real (0.62) but it is swallowed, and emit <=> clock. With emit determined by a schedule,
"whether to speak" has no free variable, so H_9786 came back UNIDENTIFIABLE -- not weak,
UNDECIDABLE. That is conjunct 1 (independence) failing, and no amount of measurement fixes
a variable that does not vary.

The redesign's answer is an information-gain gate: emit iff the interior adds information
over the reflex, above a noise floor measured on shuffled-store controls and frozen before
use. This file asks whether that actually buys a free variable, or whether the gate just
tracks the clock through a different name.

THE TEST
--------
Simulate ticks. Each tick has (a) a clock phase and (b) an interior residual whose
information gain over the reflex varies with CONTENT, independently of the clock. Then ask
three questions of each gate:

    1 does it fire?                       -- alive at all
    2 is it predictable from the CLOCK?   -- if yes, it is a schedule wearing a costume
    3 is it predictable from CONTENT?     -- the thing that would make it a free variable

    clock gate      fires on schedule                   the current production behaviour
    infogain gate   fires on interior information gain  the proposal

A gate is a FREE VARIABLE only if content predicts it well ABOVE what the clock predicts.
Reporting both is the point: a gate that is content-driven AND clock-correlated (because
content happens to arrive on a rhythm) is not a win, and this separates them.

CONTROLS
--------
  shuffle-store   the interior is replaced by a marginal-matched shuffle -- the infogain
                  gate must fall back to chance, or it is firing on magnitude not content
  always/never    degenerate gates -- the readout must call them unpredictable-by-content,
                  or the metric rewards constants
  clock-jitter    the clock is randomised while content is held -- a genuine content gate
                  must be UNMOVED; a disguised schedule follows the jitter

DIRECTIONAL: a toy, and a screen may KILL, never GREEN.
"""
import sys

import numpy as np

TICKS = 4000
SEEDS = (7, 11, 4302)
PERIOD = 7          # the production clock: a fixed rate limit
FLOOR_Q = 0.70      # infogain fires above this quantile of the shuffled-store floor


def world(rng, jitter=False):
    """Ticks with a clock phase and a content-driven information gain.

    `gain` is what the interior adds over the reflex. It is driven by CONTENT (a latent
    that arrives irregularly), NOT by the clock -- so a gate that tracks the clock and a
    gate that tracks content are genuinely different objects here.
    """
    phase = rng.integers(0, PERIOD, TICKS) if jitter else np.arange(TICKS) % PERIOD
    content = (rng.random(TICKS) < 0.18).astype(float)          # irregular arrivals
    gain = np.abs(rng.normal(0, 0.3, TICKS)) + 1.6 * content    # content lifts the gain
    return phase, content, gain


def floor_from_shuffle(rng, gain):
    """The noise floor, measured on a marginal-matched shuffle and FROZEN before use."""
    return float(np.quantile(rng.permutation(gain), FLOOR_Q))


def gates(phase, gain, floor):
    return {
        "clock (production)": (phase == 0).astype(int),
        "infogain (proposed)": (gain > floor).astype(int),
        "always (degenerate)": np.ones_like(phase),
        "never  (degenerate)": np.zeros_like(phase),
    }


def predictability(fire, cue):
    """How well does `cue` predict firing? Balanced accuracy, so a constant gate scores
    0.5 rather than being rewarded for matching the base rate."""
    fire = np.asarray(fire)
    if fire.max() == fire.min():
        return 0.5                       # constant gate: nothing to predict
    best = 0.5
    for t in np.unique(cue):
        pred = (cue == t).astype(int)
        for p in (pred, 1 - pred):
            tp = ((p == 1) & (fire == 1)).sum(); fn = ((p == 0) & (fire == 1)).sum()
            tn = ((p == 0) & (fire == 0)).sum(); fp = ((p == 1) & (fire == 0)).sum()
            if (tp + fn) and (tn + fp):
                bal = 0.5 * (tp / (tp + fn) + tn / (tn + fp))
                best = max(best, bal)
    return float(best)


def run(seed, jitter=False, shuffle_store=False):
    rng = np.random.default_rng(seed)
    phase, content, gain = world(rng, jitter=jitter)
    floor = floor_from_shuffle(np.random.default_rng(seed + 1), gain)
    if shuffle_store:
        gain = rng.permutation(gain)     # marginal-matched, content link destroyed
    out = {}
    for name, fire in gates(phase, gain, floor).items():
        out[name] = (float(np.mean(fire)),
                     predictability(fire, phase),
                     predictability(fire, content.astype(int)))
    return out


def main():
    print("R4 - is whether-to-speak a free variable, or the clock in a costume?  ($0)")
    print("balanced accuracy, so a constant gate scores 0.5000 rather than winning\n")
    print("%-22s %8s %10s %10s" % ("gate", "rate", "by CLOCK", "by CONTENT"))
    print("-" * 54)
    agg = {}
    for name in ("clock (production)", "infogain (proposed)",
                 "always (degenerate)", "never  (degenerate)"):
        r = np.mean([[*run(s)[name]] for s in SEEDS], axis=0)
        agg[name] = r
        print("%-22s %8.4f %10.4f %10.4f" % (name, r[0], r[1], r[2]))
    print("-" * 54)

    sh = np.mean([[*run(s, shuffle_store=True)["infogain (proposed)"]] for s in SEEDS], axis=0)
    ji = np.mean([[*run(s, jitter=True)["infogain (proposed)"]] for s in SEEDS], axis=0)
    print("%-22s %8.4f %10.4f %10.4f" % ("  infogain +shuf-store", sh[0], sh[1], sh[2]))
    print("%-22s %8.4f %10.4f %10.4f" % ("  infogain +clock-jitter", ji[0], ji[1], ji[2]))
    print()

    ck, ig = agg["clock (production)"], agg["infogain (proposed)"]
    al, nv = agg["always (degenerate)"], agg["never  (degenerate)"]

    if al[2] > 0.60 or nv[2] > 0.60:
        print("METRIC BROKEN - a degenerate gate scores %.4f / %.4f by content." % (al[2], nv[2]))
        print("The readout rewards constants; fix it before reading anything else.")
        return 1
    if sh[2] > 0.60:
        print("CONTROL LEAK - with the store SHUFFLED the infogain gate is still %.4f" % sh[2])
        print("predictable by content. It is firing on magnitude, not on content.")
        return 1
    if abs(ji[2] - ig[2]) > 0.10:
        print("CLOCK-COUPLED - jittering the clock moved content-predictability by %.4f."
              % abs(ji[2] - ig[2]))
        print("A genuine content gate must be unmoved by the clock; this one follows it.")
        return 1
    if ig[2] <= 0.60:
        print("NO FREE VARIABLE - the infogain gate is only %.4f predictable by content."
              % ig[2])
        print("It does not track the interior, so R4 stays BLOCKED and the redesign's")
        print("emit story is not made by this test.")
        return 0
    if ig[2] - ig[1] < 0.15:
        print("COSTUME - content %.4f is not clearly above clock %.4f. The gate may be a"
              % (ig[2], ig[1]))
        print("schedule under another name; widen the margin before claiming a free variable.")
        return 0

    print("FREE VARIABLE - the infogain gate is %.4f predictable by CONTENT and only" % ig[2])
    print("%.4f by the CLOCK, while production's clock gate is the exact mirror:" % ig[1])
    print("%.4f by clock, %.4f by content." % (ck[1], ck[2]))
    print()
    print("So whether-to-speak stops being determined by the schedule and starts varying")
    print("with the interior -- which is conjunct 1 (independence) supplied, the conjunct")
    print("H_9786 failed on. Controls hold: shuffling the store drops content-")
    print("predictability to %.4f, and jittering the clock leaves it at %.4f (unmoved)."
          % (sh[2], ji[2]))
    print()
    print("What this does NOT show: that the gate speaks at the RIGHT times, that the")
    print("information gain means anything, or that the interior it reads is rich. It")
    print("shows that emit has a free variable at all. A screen may KILL, never GREEN.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
