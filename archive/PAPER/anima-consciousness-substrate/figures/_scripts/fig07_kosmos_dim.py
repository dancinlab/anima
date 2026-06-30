#!/usr/bin/env python3
"""fig07_kosmos_dim.py — KOSMOS coordinate dimension ladder D*=6 (matplotlib DATA).

EVERY value verbatim from .verdicts/kosmos-dim-ladder/SUMMARY.txt
  (per-rung dAcc + verdict; capacity knee D*=6; no-collapse contrast 3.09->1.94).

Output: figures/fig07_kosmos_dim.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── verbatim per-rung dAcc (kosmos-dim-ladder/SUMMARY.txt) ────────────────────
D       = [3, 4, 5, 6, 7, 8]
AXIS    = ["t time", "e emotion", "tau tier", "m modality", "s scale", "kap lane"]
DACC    = [0.003333, 0.008333, 0.011111, 0.045556, 0.018889, 0.001111]
BAND    = [0.001361, 0.006804, 0.009061, 0.012862, 0.016906, 0.005500]
HOLDS   = [True, True, True, True, False, False]   # D=7,8 SATURATED

GREEN = "#2ca02c"
GREY  = "#9aa0a6"

fig, ax = plt.subplots(figsize=(9.0, 4.6))

cols = [GREEN if h else GREY for h in HOLDS]
x = range(len(D))
bars = ax.bar(x, DACC, yerr=BAND, color=cols, edgecolor="black", linewidth=0.7,
              width=0.62, capsize=4, error_kw=dict(lw=1.0))
for xi, v, h in zip(x, DACC, HOLDS):
    tag = "HOLDS" if h else "SATURATED"
    ax.text(xi, v+BAND[list(x).index(xi)]+0.0015, f"{v:+.4f}\n{tag}",
            ha="center", va="bottom", fontsize=8,
            color=(GREEN if h else GREY))

# capacity knee marker between D=6 and D=7
ax.axvline(3.5, color="black", ls="--", lw=1.3)
ax.text(3.5, 0.060, "capacity knee  $D^\\ast=6$", ha="center", va="bottom",
        fontsize=10, fontweight="bold")

ax.set_xticks(list(x))
ax.set_xticklabels([f"D={d}\n{a}" for d, a in zip(D, AXIS)], fontsize=8.5)
ax.set_ylabel("joint info added ($d$Acc, kNN LOO)")
ax.set_ylim(-0.004, 0.068)
ax.axhline(0, color="black", lw=0.6)
ax.set_title("KOSMOS coordinate dimension ladder — capacity $D^\\ast=6$\n"
             "(2D + 4 independent axes HOLD; scale/lane SATURATE; "
             "no-collapse 3.09$\\to$1.94$>$1)", fontsize=10.5)

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig07_kosmos_dim.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig07] wrote {out}")
