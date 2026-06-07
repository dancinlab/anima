#!/usr/bin/env python3
"""fig10_edge_of_chaos.py — the edge-of-chaos Phi-peak (H_285) as a standalone
matplotlib DATA figure.

EVERY value verbatim from:
  UNIVERSE/H_285_edge_of_chaos_big_phi.md (= Appendix A, eq:edge):
    Wolfram class-mean big-Phi:  ordered (I) 0.0 < chaotic (III) 6.943
                                 < class-IV / edge 10.448   (5/5 falsifiers PASS)
  M6 per-rule anchors (Appendix A, app:phi-edge):
    rule-204 Phi = 0.0 (ordered, state 1010),  rule-110 Phi ~= 7.5475 (class-IV)
  Honest scope (Appendix A): the CHAOTIC (class III) class is BIMODAL —
    rule-30 high vs rule-90 XOR Phi = 0 — so "edge > chaotic" is a class-AGGREGATE
    statement, not per-rule. We annotate that bimodality rather than smooth it.

Falsifier (frozen, H_285): F285.1 Phi(IV) > Phi(I) AND F285.2 Phi(IV) > Phi(III).
Integration peaks at the boundary between order and chaos: emergence lives at the edge.

No fabricated points. Output: figures/fig10_edge_of_chaos.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── verbatim verdict numbers (H_285 / Appendix A eq:edge) ────────────────────
CLASSES = ["ordered (I)", "chaotic (III)", "class-IV (edge)"]
PHI     = [0.0, 6.943, 10.448]            # Wolfram class-mean big-Phi (verbatim)
# M6 per-rule anchors (verbatim, Appendix A app:phi-edge)
RULE110 = 7.5475                          # rule-110 (class-IV) Phi anchor
RULE204 = 0.0                             # rule-204 (ordered) Phi at state 1010

GREY  = "#9aa0a6"   # ordered
BLUE  = "#4c78a8"   # chaotic
GREEN = "#2ca02c"   # class-IV / edge (the peak)
RED   = "#d62728"

fig, ax = plt.subplots(figsize=(7.4, 4.8))

cols = [GREY, BLUE, GREEN]
bars = ax.bar(CLASSES, PHI, color=cols, edgecolor="black", linewidth=0.8, width=0.62)

# highlight the class-IV / edge peak (thicker green edge)
bars[2].set_edgecolor(GREEN)
bars[2].set_linewidth(2.4)

for b, v in zip(bars, PHI):
    ax.text(b.get_x() + b.get_width()/2, v + 0.18, f"{v:.3f}",
            ha="center", va="bottom", fontsize=11, fontweight="bold")

# falsifier annotations: F285.1 (IV > I) and F285.2 (IV > III)
ax.annotate("", xy=(2, 10.448), xytext=(0, 0.0),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.3,
                            connectionstyle="arc3,rad=-0.18"))
ax.text(0.62, 9.55, "F285.1: $\\Phi$(IV) $>$ $\\Phi$(I)", color=GREEN, fontsize=8.5)
ax.annotate("", xy=(2, 10.448), xytext=(1, 6.943),
            arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.3,
                            connectionstyle="arc3,rad=-0.12"))
ax.text(1.06, 9.05, "F285.2: $\\Phi$(IV) $>$ $\\Phi$(III)", color=GREEN, fontsize=8.5)

# honest scope: the CHAOTIC (III) class is bimodal (rule-30 high vs rule-90 XOR = 0)
ax.errorbar(1, 6.943, yerr=[[6.943], [0.6075]], fmt="none", ecolor=RED,
            elinewidth=1.4, capsize=5, capthick=1.4, zorder=5)
ax.text(1.0, 0.45, "class III is BIMODAL\n(rule-30 high; rule-90 XOR $\\Phi$=0)",
        ha="center", va="bottom", fontsize=7.6, color=RED)

# M6 per-rule anchor markers
ax.plot([2], [RULE110], marker="D", color=RED, markersize=6, zorder=6)
ax.text(2.34, RULE110, "rule-110\n$\\Phi$=7.5475", color=RED, fontsize=7.4,
        va="center", ha="left")

ax.set_ylabel("class-mean big-$\\Phi$ (faithful IIT 4.0)", fontsize=11)
ax.set_ylim(0, 12.2)
ax.set_title("Edge-of-chaos $\\Phi$-peak (H\\_285): emergence lives at the edge\n"
             "ordered $0.0$ $<$ chaotic $6.943$ $<$ class-IV/edge $10.448$  "
             "(5/5 falsifiers PASS)", fontsize=10.5)
ax.grid(axis="y", ls=":", lw=0.5, alpha=0.5)

fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig10_edge_of_chaos.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig10] wrote {out}")
