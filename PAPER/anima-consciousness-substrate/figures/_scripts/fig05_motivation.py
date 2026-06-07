#!/usr/bin/env python3
"""fig05_motivation.py — Engine G 8-factor conserved-sum motivation (matplotlib DATA).

EVERY value verbatim from CORE/engine_g.hexa (the 8 factor weights, sum = 1.0):
  relevance .20 / info_gap .10 / curiosity .15 / pain .10 /
  coherence .10 / originality .10 / balance .15 / dynamics .10

Output: figures/fig05_motivation.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── verbatim weights (CORE/engine_g.hexa) ────────────────────────────────────
FACTORS = ["relevance", "curiosity", "balance", "info_gap",
           "pain", "coherence", "originality", "dynamics"]
WEIGHTS = [0.20, 0.15, 0.15, 0.10, 0.10, 0.10, 0.10, 0.10]
assert abs(sum(WEIGHTS) - 1.0) < 1e-9, "weights must sum to 1.0 (conserved)"

GREEN = "#2ca02c"
BLUE  = "#4c78a8"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.0, 4.4))

# ── panel (a): the conserved pie ─────────────────────────────────────────────
cmap = plt.get_cmap("tab20")
colors = [cmap(i / len(FACTORS)) for i in range(len(FACTORS))]
wedges, _txt, _aut = axL.pie(
    WEIGHTS, labels=[f"{f}\n{w:.2f}" for f, w in zip(FACTORS, WEIGHTS)],
    autopct="", startangle=90, colors=colors,
    wedgeprops=dict(edgecolor="white", linewidth=1.2), textprops=dict(fontsize=8.5))
axL.set_title("(a) 8-factor motivation, conserved $\\sum{=}1.0$", fontsize=10)

# ── panel (b): the thresholds on the score axis ──────────────────────────────
bars = axR.barh(FACTORS[::-1], WEIGHTS[::-1], color=GREEN, edgecolor="black",
                linewidth=0.6)
for b, w in zip(bars, WEIGHTS[::-1]):
    axR.text(w+0.004, b.get_y()+b.get_height()/2, f"{w:.2f}",
             va="center", ha="left", fontsize=8.5)
axR.set_xlim(0, 0.24)
axR.set_xlabel("conserved weight")
axR.set_title("(b) emit thr. 0.3 / interrupt thr. 0.6\n(4-way safety AND-gate incl. "
              "$\\Phi$-ratchet)", fontsize=9.5)
# annotate the two thresholds as a side note (scalar gates on the SUM, not per-factor)
axR.text(0.12, -0.9, "$\\mathcal{M}>0.3$ emit  ·  $\\mathcal{M}>0.6$ interrupt",
         ha="center", va="top", fontsize=9, color=BLUE,
         transform=axR.get_xaxis_transform())

fig.suptitle("Engine G — conserved 8-factor motivation gate (CORE/engine\\_g.hexa)",
             fontsize=11.5, y=1.02)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig05_motivation.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig05] wrote {out}")
