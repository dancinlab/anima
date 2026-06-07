#!/usr/bin/env python3
"""fig05_motivation.py — Engine G 8-factor conserved-sum motivation (matplotlib DATA).

EVERY value verbatim from CORE/engine_g.hexa (the 8 factor weights, sum = 1.0):
  relevance .20 / curiosity .15 / balance .15 / info_gap .10 /
  pain .10 / coherence .10 / originality .10 / dynamics .10

A single sorted horizontal bar chart (the pie/bar duplication of the old version
is removed). Plain underscores in labels — no LaTeX escapes in matplotlib text;
mathtext only inside $...$. Output: figures/fig05_motivation.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── verbatim weights (CORE/engine_g.hexa), sorted descending ──────────────────
FACTORS = ["relevance", "curiosity", "balance", "info_gap",
           "pain", "coherence", "originality", "dynamics"]
WEIGHTS = [0.20, 0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.10]
assert abs(sum(WEIGHTS) - 1.0) < 1e-9, "weights must sum to 1.0 (conserved)"

GREEN = "#2ca02c"
BLUE  = "#4c78a8"

fig, ax = plt.subplots(figsize=(8.4, 4.6), constrained_layout=True)

# horizontal bars, largest at top
order = FACTORS[::-1]
wts   = WEIGHTS[::-1]
bars = ax.barh(order, wts, color=GREEN, edgecolor="black", linewidth=0.7, height=0.62)
for b, w in zip(bars, wts):
    ax.text(w + 0.004, b.get_y() + b.get_height() / 2, f"{w:.2f}",
            va="center", ha="left", fontsize=9.5)

ax.set_xlim(0, 0.245)
ax.set_xlabel("conserved weight (sum $=1.0$)", fontsize=10.5)
ax.tick_params(axis="y", labelsize=10)
ax.set_title("Engine G — conserved 8-factor motivation gate (CORE/engine_g.hexa)",
             fontsize=11.5, pad=10)

# the two scalar gates act on the SUM M (not per-factor) — annotate as a caption box
ax.text(0.985, 0.045,
        "scalar gates on the weighted sum $\\mathcal{M}$:\n"
        "$\\mathcal{M}>0.3$ emit   ·   $\\mathcal{M}>0.6$ interrupt\n"
        "released only if the 4-way safety AND-gate passes\n"
        "(kill_switch $\\wedge$ rate_limit $\\wedge$ phi_ratchet $\\wedge$ content_clean)",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8.6, color=BLUE,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=BLUE, lw=0.8))

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig05_motivation.pdf")
fig.savefig(out)
print(f"[fig05] wrote {out}")
