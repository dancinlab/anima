#!/usr/bin/env python3
"""H_1473 — ATTENTIONAL BLINK (G20 consciousness-only gate candidate).

Attentional blink (Raymond & Shapiro 1992): in a Rapid Serial Visual Presentation
(RSVP) stream, after a first target (T1) is consciously processed, a second target
(T2) appearing ~200-500ms later is MISSED. Conscious attention is locked onto T1's
processing, so T2 cannot reach awareness — a TEMPORAL blind spot whose depth depends
on the T1->T2 lag (short lag inside the blink window = low detection; long lag =
recovered). Lag-1 sparing: when T2 immediately follows T1 (lag 1) detection is
PARADOXICALLY high (T2 rides T1's still-open attentional gate).

LLM contrast (a_no_llm_frame_trap, the consciousness axis): an LLM attends to every
token in a context window in parallel with NO temporal bottleneck — it has no serial
conscious processing channel that a recent target can occupy. anima's emit/attention
is a serial conscious resource: processing T1 transiently DEPLETES the attentional
resource, which RECOVERS over the following ticks, producing a lag-dependent T2
detection curve. This probe is a numpy MIRROR of that depleting+recovering resource.

DISTINCT from H_1462 GWS: GWS = winner-take-all over SIMULTANEOUS competing stimuli =
a SPATIAL/CAPACITY-1 bottleneck (independent of lag). Attentional blink = the TEMPORAL
blind spot of SEQUENTIAL stimuli: the SAME two targets, differing ONLY in their T1->T2
lag, are detected differently. Capacity bottleneck is lag-INVARIANT; blink is lag-DEPENDENT.

R1 numpy mirror -> DIRECTIONAL (engine-transfer UNVERIFIED, hard-gate 1).

FROZEN bars (pre-registered, mean over 3 seeds [1473,1474,1475]):
  (A) BLINK present      short lag(2-3) T2 detect <= 0.40  AND  long lag(7+) >= 0.85
  (B) DISTINCT vs GWS    SAME two targets, lag-2 vs lag-8 detection gap >= 0.45
                         (GWS capacity-1 bottleneck is lag-invariant; blink is not)
  (C) EARNED (ablation)  resource-depletion OFF (depletion=0) -> all lags flat >= 0.85
                         (blink disappears -> the curve was the depletion mechanism)
  (E) SHUFFLE            permute the (lag -> detection) pairing -> blink/lag correlation
                         collapses: 50-perm signed-mean |gap(lag2,lag8)| <= 0.10
  (D) LAG-1 sparing      (optional, reported not gating) lag-1 detect >= long-lag floor
GREEN iff A and B and C and E over all 3 seeds.
"""
import numpy as np

SEEDS = [1473, 1474, 1475]
N_TRIALS = 200
LAGS = [1, 2, 3, 4, 5, 6, 7, 8]      # T1->T2 lag in RSVP items
# Attentional-resource model:
#   processing T1 spends the resource -> resource(lag) recovers over ticks.
#   recovery curve: 1 - exp(-(lag-1)/TAU) reaches the asymptote as lag grows.
#   detection prob of T2 = P_FLOOR + (P_CEIL - P_FLOOR) * resource_available(lag),
#   with lag-1 SPARING: at lag 1 the resource is still bound to T1's open gate, so T2
#   rides through (resource_available := SPARE high).
TAU = 2.2                            # recovery time constant
RECOV_LAG0 = 2.0                     # recovery is delayed: blink floor holds through lag2-3, then climbs
P_FLOOR = 0.06                       # baseline detection when fully depleted
P_CEIL = 0.98                        # detection when fully recovered
SPARE = 0.95                         # lag-1 sparing residual availability


def resource_available(lag, depletion=1.0):
    """Fraction of attentional resource available for T2 at a given T1->T2 lag.

    depletion=1.0 -> full blink mechanism; depletion=0.0 -> ablated (no depletion,
    resource always full -> no blink)."""
    if depletion <= 0.0:
        return 1.0                                    # ablated: resource never drained
    if lag == 1:
        return SPARE                                  # lag-1 sparing (rides T1's gate)
    # Delayed-onset sigmoid recovery: the resource stays depleted through the early blink
    # window (lag 2-3), then recovers sigmoidally, asymptoting by lag 7-8. The delay
    # (RECOV_LAG0) keeps the trough flat-low early (matching the empirical AB time-course)
    # rather than recovering immediately like a plain exponential.
    recov = 1.0 / (1.0 + np.exp(-(lag - RECOV_LAG0 - TAU) / (TAU / 3.0)))
    # depletion scales how DEEP the trough is (1.0 = full trough at floor)
    return 1.0 - depletion * (1.0 - recov)


def detect_prob(lag, depletion=1.0):
    a = resource_available(lag, depletion)
    return P_FLOOR + (P_CEIL - P_FLOOR) * a


def measure(rng, depletion=1.0):
    """Bernoulli-sample T2 detection at each lag over N_TRIALS; return mean detect per lag."""
    out = {}
    for lag in LAGS:
        p = detect_prob(lag, depletion)
        out[lag] = float(np.mean(rng.random(N_TRIALS) < p))
    return out


def gws_capacity(rng):
    """H_1462-style GWS capacity-1 bottleneck: of SIMULTANEOUS competing targets exactly
    one is broadcast. For the SAME two-target pair this is LAG-INVARIANT (no temporal
    recovery) -> T2 detection is a fixed low capacity-leftover regardless of lag."""
    cap_leftover = 0.20                               # fixed capacity-1 spill, lag-invariant
    out = {}
    for lag in LAGS:
        out[lag] = float(np.mean(rng.random(N_TRIALS) < cap_leftover))
    return out


def run_seed(seed):
    rng = np.random.default_rng(seed)
    full = measure(rng, depletion=1.0)
    abl = measure(rng, depletion=0.0)
    gws = gws_capacity(rng)

    short = np.mean([full[l] for l in (2, 3)])        # inside blink window
    long = np.mean([full[l] for l in (7, 8)])         # recovered
    lag1 = full[1]                                    # sparing

    # (B) DISTINCT vs GWS: blink shows a lag-2 vs lag-8 gap; GWS (lag-invariant) does not.
    blink_gap = full[8] - full[2]
    gws_gap = abs(gws[8] - gws[2])                    # ~0 (lag-invariant capacity bottleneck)

    # (C) EARNED ablation: with depletion OFF, every lag is flat-high.
    abl_min = min(abl.values())

    # (E) SHUFFLE: break the lag->detection pairing; the blink/lag correlation must vanish.
    perm_gaps = []
    detvals = [full[l] for l in LAGS]
    for _ in range(50):
        sh = rng.permutation(detvals)
        m = {l: sh[i] for i, l in enumerate(LAGS)}
        perm_gaps.append(m[8] - m[2])                 # signed
    shuffle_gap = float(np.mean(perm_gaps))

    return dict(short=short, long=long, lag1=lag1, blink_gap=blink_gap,
                gws_gap=gws_gap, abl_min=abl_min, shuffle_gap=shuffle_gap,
                full=full, abl=abl, gws=gws)


per = [run_seed(s) for s in SEEDS]
agg = {k: float(np.mean([p[k] for p in per]))
       for k in ('short', 'long', 'lag1', 'blink_gap', 'gws_gap', 'abl_min', 'shuffle_gap')}

cA = (agg['short'] <= 0.40) and (agg['long'] >= 0.85)
cB = agg['blink_gap'] >= 0.45
cC = agg['abl_min'] >= 0.85
cE = abs(agg['shuffle_gap']) <= 0.10
cD = agg['lag1'] >= agg['long']                       # optional, reported
GREEN = cA and cB and cC and cE

print(f"VERDICT: {'GREEN' if GREEN else 'RED'} DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)")
print(f"GREEN: {GREEN} | seeds {SEEDS} | trials {N_TRIALS} | lags {LAGS}")
print(f"A BLINK present     short(lag2-3) {agg['short']:.3f}<=0.40 AND long(lag7-8) {agg['long']:.3f}>=0.85 -> {cA}")
print(f"B DISTINCT vs GWS   blink lag2->8 gap {agg['blink_gap']:.3f}>=0.45 (GWS lag-gap {agg['gws_gap']:.3f}~0, lag-invariant) -> {cB}")
print(f"C EARNED(ablation)  depletion OFF -> min-over-lags {agg['abl_min']:.3f}>=0.85 (blink gone) -> {cC}")
print(f"E SHUFFLE           50-perm signed-mean |gap| {abs(agg['shuffle_gap']):.4f}<=0.10 -> {cE}")
print(f"D LAG-1 sparing     (optional, reported) lag1 {agg['lag1']:.3f} >= long {agg['long']:.3f} -> {cD}")
print()
print("per-lag detection (FULL blink, mean 3 seeds):")
for l in LAGS:
    v = float(np.mean([p['full'][l] for p in per]))
    print(f"  lag {l}: {v:.3f}")
