#!/usr/bin/env python3
# fig01_example.py — minimal working matplotlib bar chart shipped with the template
# so `/paper new` produces a paper that actually compiles with one real figure
# inlined, not just a placeholder include. Replace DATA with your own; rerun via
# `make figures` from the paper root, or `python3 figures/_scripts/fig01_example.py`.
import matplotlib.pyplot as plt

# Replace these three rows with your headline data. Order matters for the bar
# x-axis. Keep units explicit in the y-axis label and the figure caption.
DATA = [
    ("baseline",      0.42),
    ("method A",      0.71),
    ("this work",     0.96),
]

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size":   10,
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(5.5, 3.2))
labels  = [d[0] for d in DATA]
heights = [d[1] for d in DATA]
colors  = ["#C62828", "#FB8C00", "#388E3C"][:len(DATA)]

ax.bar(labels, heights, color=colors, edgecolor="black", linewidth=0.6, width=0.55)
for i, h in enumerate(heights):
    ax.text(i, h + 0.02, f"{h:.2f}", ha="center", va="bottom",
            fontsize=10, fontweight="bold")

ax.set_ylabel("metric (units)", fontsize=11)
ax.set_ylim(0, max(heights) * 1.25)
ax.grid(axis="y", linestyle=":", alpha=0.4)
ax.set_title("Example headline figure (replace with your result)",
             fontsize=11, pad=8)

plt.tight_layout()

# Output to figures/fig01_example.pdf (one level up from _scripts/).
out_pdf = __file__.rsplit("/", 2)[0] + "/fig01_example.pdf"
plt.savefig(out_pdf, format="pdf", bbox_inches="tight")
print(f"[fig01_example] wrote {out_pdf}")
