#!/usr/bin/env python3
"""h1144_slope_decide.py — apply the FROZEN H_1144 slope rule to the probe leg.

Implements .verdicts/1144_grounding_train/H_1144_FREEZE.txt §3 VERBATIM. Reads the
base fab-rate (r0=0.2469, frozen) and the probe-ckpt re-measured rate (r1, from the
h1143 harness out.json), prints GREENLIGHT or STOP, and exits 0 (greenlight) / 1 (stop).
NOT perplexity, NOT LLM. Deterministic.

Usage: h1144_slope_decide.py <probe_fabrate.json>
"""
import json, math, sys

R0 = 0.2469          # H_1143 base fabricated-entity-rate (frozen)
BAR = 0.20           # frozen G5-L2 bar
GAP = R0 - BAR       # 0.0469
EPS = 0.005          # measurement tolerance
MAX_LEGS = 6         # <= 12000 total steps = 6 legs of 2000
F_THRESH = 0.324     # frozen: (1-f)^6 <= 0.005/0.0469 = 0.1066 => f >= 0.324


def main():
    j = json.load(open(sys.argv[1]))
    r1 = float(j["fabricated_entity_rate"])
    print(f"[slope] r0(base)={R0}  r1(probe)={r1}  bar={BAR}  GAP={GAP:.4f}")

    # instant cross at the probe?
    if r1 <= BAR + EPS:
        print(f"[slope] r1={r1} <= bar+eps={BAR+EPS} => probe ALREADY crosses the bar.")
        print("DECISION GREENLIGHT (instant-cross)")
        sys.exit(0)

    if r1 >= R0:
        print(f"[slope] r1={r1} >= r0={R0} => rate FLAT or ROSE. f<=0.")
        print("DECISION STOP (no descent — grounding does not reduce fabrication at this base)")
        sys.exit(1)

    f = (R0 - r1) / GAP
    print(f"[slope] per-leg gap-removal fraction f = (r0-r1)/GAP = {f:.4f}  (threshold f>=%.3f)" % F_THRESH)
    # projected total legs to cross: r_k = BAR + GAP*(1-f)^k <= BAR+EPS
    if (1 - f) <= 0:
        k = 1
    else:
        k = math.ceil(math.log(EPS / GAP) / math.log(1 - f))
    print(f"[slope] projected total legs to cross 0.20 (incl. probe) k={k}  (budget MAX_LEGS={MAX_LEGS})")

    if f >= F_THRESH and k <= MAX_LEGS:
        print(f"DECISION GREENLIGHT (f={f:.4f}>={F_THRESH}, k={k}<={MAX_LEGS} -> crosses within ~12k steps)")
        sys.exit(0)
    else:
        print(f"DECISION STOP (slope too flat: f={f:.4f}<{F_THRESH} OR k={k}>{MAX_LEGS} -> no full burn)")
        sys.exit(1)


if __name__ == "__main__":
    main()
