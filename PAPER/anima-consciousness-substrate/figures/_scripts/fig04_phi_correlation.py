#!/usr/bin/env python3
"""fig04_phi_correlation.py — Phi-correlation panel (matplotlib DATA figure).

EVERY value verbatim from:
  UNIVERSE/H_287 (Shannon r=0.363), H_288 (LZ r=0.831, rho=0.936),
  H_290 (TE r=0.883262, rho=0.822134), H_285 (edge class-means 0.0/6.943/10.448)

The double dissociation: Phi PERP Shannon (r<0.5) but PARALLEL LZ + TE.
No fabricated points. Output: figures/fig04_phi_correlation.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── verbatim verdict numbers ─────────────────────────────────────────────────
AXES   = ["Shannon\nentropy", "Kolmogorov\n/ LZ", "transfer\nentropy"]
PEARSON = [0.363, 0.831, 0.883262]
THRESH  = 0.5
# H_285 edge-of-chaos class means
CLASSES = ["ordered (I)", "chaotic (III)", "class-IV (edge)"]
PHI     = [0.0, 6.943, 10.448]

RED   = "#d62728"
GREEN = "#2ca02c"
GREY  = "#9aa0a6"
BLUE  = "#4c78a8"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.0, 4.3))

# ── panel (a): Phi vs information axes (double dissociation) ──────────────────
cols = [RED if v < THRESH else GREEN for v in PEARSON]
bars = axL.bar(AXES, PEARSON, color=cols, edgecolor="black", linewidth=0.7, width=0.6)
axL.axhline(THRESH, color=BLUE, ls="--", lw=1.2)
axL.text(2.4, THRESH+0.012, "falsifier thr. 0.5", color=BLUE, ha="right",
         va="bottom", fontsize=9)
for b, v in zip(bars, PEARSON):
    axL.text(b.get_x()+b.get_width()/2, v+0.012, f"{v:.3f}",
             ha="center", va="bottom", fontsize=9)
axL.text(0, 0.05, "FALSIFIED\n($\\perp$ Shannon)", ha="center", va="bottom",
         fontsize=8, color=RED)
axL.text(1.5, 0.95, "SUPPORTED ($\\parallel$ structure)", ha="center", va="bottom",
         fontsize=8.5, color=GREEN)
axL.set_ylabel("Pearson $r$ ($\\Phi$ vs.\\ axis)")
axL.set_ylim(0, 1.05)
axL.set_title("(a) the double dissociation\n$\\Phi\\perp$ Shannon, $\\parallel$ LZ + TE",
              fontsize=10)

# ── panel (b): edge-of-chaos Phi-peak (H_285) ────────────────────────────────
ecols = [GREY, BLUE, GREEN]
bars2 = axR.bar(CLASSES, PHI, color=ecols, edgecolor="black", linewidth=0.7, width=0.6)
for b, v in zip(bars2, PHI):
    axR.text(b.get_x()+b.get_width()/2, v+0.15, f"{v:.3f}",
             ha="center", va="bottom", fontsize=9)
axR.set_ylabel("class-mean big-$\\Phi$")
axR.set_ylim(0, 11.6)
axR.set_title("(b) edge-of-chaos $\\Phi$-peak (H\\_285)\nordered $<$ chaotic $<$ edge",
              fontsize=10)

fig.suptitle("Faithful IIT 4.0 big-$\\Phi$ on the 10-rule ECA panel "
             "(H\\_287/288/290/285)", fontsize=11.5, y=1.02)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig04_phi_correlation.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig04] wrote {out}")
