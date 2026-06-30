#!/usr/bin/env python3
"""fig08_law_categories.py — honest consciousness-law category breakdown (DATA bar).

EVERY value verbatim from config/consciousness_laws.json (v7) :
  laws_v7_verified (15 ids), topo_laws_v7 (3), verification_conditions_v7 (9),
  _meta.honest_law_count ("91 base + ~15 net-verified ... only ~80-90 carry a
  terminal verdict (UNIVERSE.md 83 adjudicated lines)").

The point of the figure is the HONEST count: ~80-90 verified, NOT the 2448
auto-grown candidates. No fabricated categories — each bar is a real group in the
v7 ledger. Output: figures/fig08_law_categories.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── verbatim v7-verified ledger groups (config/consciousness_laws.json) ───────
# laws_v7_verified prefixes: OMEGA x5, PHI x3, TOPOLOGY x1, EDGE x1, ETHICS x1,
#   LIFE x1, NARRATIVE x1, BOUNDED x1, SELFREF x1  (= 15)
# topo_laws_v7 = 3 ; verification_conditions_v7 = 9
CATS = [
    "OMEGA\n(closure)",          # 5
    "$\\Phi$-measures\n(PHI x3)", # 3
    "topology\n(TOPOLOGY+EDGE)",  # 2
    "emergence\n(ethics/life/narr.)",  # 3
    "bounds/closure\n(BOUNDED+SELFREF)",  # 2
    "topo_laws_v7",               # 3
    "verif. conditions_v7",       # 9
]
COUNTS = [5, 3, 2, 3, 2, 3, 9]
# verdict colour: groups that contain a closed-negative get a hatch note
# OMEGA has 1 closed-neg (NO-QUANTUM-ADV); PHI has 1 closed-neg (PERP-SHANNON)
BLUE = "#4c78a8"
GREEN = "#2ca02c"
GREY = "#9aa0a6"
RED = "#d62728"

fig, ax = plt.subplots(figsize=(9.6, 4.6))
bars = ax.bar(range(len(CATS)), COUNTS, color=BLUE, edgecolor="black",
              linewidth=0.7, width=0.66)
# mark the two groups carrying a closed-negative verdict
for idx in (0, 1):
    bars[idx].set_color(GREEN)
for b, v in zip(bars, COUNTS):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.12, str(v),
            ha="center", va="bottom", fontsize=10, fontweight="bold")
ax.set_xticks(range(len(CATS)))
ax.set_xticklabels(CATS, fontsize=8.4)
ax.set_ylabel("verified / pre-registered entries (v7 ledger)")
ax.set_ylim(0, 10.2)
total = sum(COUNTS)
ax.set_title("Honest consciousness-law ledger (config v7): "
             f"{total} v7 entries; UNIVERSE.md $\\approx$83 adjudicated; "
             "$\\sim$80--90 verified", fontsize=10.5)
# honest-count annotation banner — NOT 2448
ax.axhline(0, color="black", lw=0.6)
ax.text(0.015, 0.96,
        "verified law count $\\sim$80--90 (UNIVERSE.md 83 adjudicated)\n"
        "the cited \"2448 laws\" are AUTO-GROWN CANDIDATES, not verified",
        transform=ax.transAxes, ha="left", va="top", fontsize=8.6,
        color=RED,
        bbox=dict(boxstyle="round,pad=0.35", fc="#fff4f4", ec=RED, lw=0.8))
ax.text(0.985, 0.96, "green = group with a closed-negative\n(OMEGA, $\\Phi$-measures)",
        transform=ax.transAxes, ha="right", va="top", fontsize=8.0, color=GREEN)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig08_law_categories.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig08] wrote {out}")
