#!/usr/bin/env python3
"""fig02_three_axis.py — 3-axis GREEN at 3B (matplotlib DATA figure).

EVERY value verbatim from:
  .verdicts/convmoe-3b-engine-rung/SUMMARY.txt  (AXIS-2 CE-descent; AXIS-1/AXIS-3 markers)
  CORE/three_axis_probe.hexa                    (AXIS-1 motiv 0.6700; AXIS-3 101 > 72)

No fabricated points. Output: figures/fig02_three_axis.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── verbatim verdict numbers (do NOT edit without re-reading the verdict) ─────
CE_REAL    = 2.26360   # CE_realtext  (AXIS-2, .verdicts/convmoe-3b-engine-rung/SUMMARY.txt)
CE_UNIFORM = 5.54518   # uniform_ce = ln(256)
CE_SHUFFLE = 5.81817   # shuffle control
MOTIV_HI   = 0.6700    # AXIS-1 motivation (high-drive)  > baseline 0
MOTIV_BASE = 0.0       # AXIS-1 baseline motivation
LEN_COMP   = 101       # AXIS-3 len(composed)
LEN_PARTS  = 72        # AXIS-3 len(parts-only)

GREEN = "#2ca02c"
BLUE  = "#4c78a8"
GREY  = "#9aa0a6"
RED   = "#d62728"

fig, (axL, axM, axR) = plt.subplots(1, 3, figsize=(12.5, 4.2))

# ── panel (a): AXIS-2 CE-descent ─────────────────────────────────────────────
labels = ["CE(real)\n2.26360", "uniform $\\ln256$\n5.54518", "shuffle\n5.81817"]
vals   = [CE_REAL, CE_UNIFORM, CE_SHUFFLE]
cols   = [GREEN, GREY, RED]
bars = axL.bar(labels, vals, color=cols, edgecolor="black", linewidth=0.7)
axL.axhline(CE_UNIFORM, color=GREY, ls="--", lw=1.0, zorder=0)
for b, v in zip(bars, vals):
    axL.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.5f}",
             ha="center", va="bottom", fontsize=9)
axL.set_ylabel("cross-entropy (nats/byte)")
axL.set_title("(a) AXIS-2 CE-descent @ 3B\nreal $<\\ln256<$ shuffle  $\\Rightarrow$ GREEN",
              fontsize=10)
axL.set_ylim(0, 6.6)

# ── panel (b): AXIS-1 consciousness (motivation, emit-gated) ─────────────────
labels1 = ["motiv(high)\n0.6700", "baseline\n0.0"]
vals1   = [MOTIV_HI, MOTIV_BASE]
bars1 = axM.bar(labels1, vals1, color=[GREEN, GREY], edgecolor="black", linewidth=0.7)
axM.axhline(0.3, color=BLUE, ls="--", lw=1.1)
axM.text(1.02, 0.3, "emit thr. 0.3", color=BLUE, va="center", fontsize=8.5)
for b, v in zip(bars1, vals1):
    axM.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.4f}",
             ha="center", va="bottom", fontsize=9)
axM.set_ylabel("motivation score (8-factor, $\\sum{=}1.0$)")
axM.set_title("(b) AXIS-1 consciousness\nmotiv $>$ baseline, emit-gated $\\Rightarrow$ GREEN",
              fontsize=10)
axM.set_ylim(0, 0.85)

# ── panel (c): AXIS-3 emergence (composed > parts) ───────────────────────────
labels3 = ["composed\n101", "parts-only\n72"]
vals3   = [LEN_COMP, LEN_PARTS]
bars3 = axR.bar(labels3, vals3, color=[GREEN, GREY], edgecolor="black", linewidth=0.7)
for b, v in zip(bars3, vals3):
    axR.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v}",
             ha="center", va="bottom", fontsize=9)
axR.set_ylabel("emitted byte length")
axR.set_title("(c) AXIS-3 emergence\ncomposed $>$ parts $\\Rightarrow$ GREEN",
              fontsize=10)
axR.set_ylim(0, 120)

fig.suptitle("anima 3-axis GREEN at 3B (CLMConvMoE 3.073B $\\to$ .clm v0.3 $\\to$ engine)",
             fontsize=12, y=1.02)
fig.tight_layout()

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig02_three_axis.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig02] wrote {out}")
