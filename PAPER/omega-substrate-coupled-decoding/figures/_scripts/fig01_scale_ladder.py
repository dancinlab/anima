#!/usr/bin/env python3
r"""fig01_scale_ladder.py — OMEGA R8 (OΩ4/OΩ5) scale-ladder figure.

EVERY value below is copied VERBATIM from the verdict:
  .verdicts/omega-engine/F-OMEGA-SCALE.txt
  (cross-checked against PAPER main.tex R8 table, #1806). NO fabricated points.

Left panel  — per-rung held-out TEST CE (nats/byte): base (flat 3.097779 every rung),
              a_only, and the minimal-gate min_learned, across the 5 leak-free competent
              rungs d384/d512/d768/d1024 (12000 steps) + the more-competent d768x2 (24000).
Right panel — the A-wire advantage Δ-vs-base per rung, showing it is FLAT at +2.20±0.03
              nats/byte across the dim ladder (SCALE-STABLE), the headline finding.

Output: figures/fig01_scale_ladder.pdf  (vector, embeds into main.tex via \includegraphics).
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# --- verbatim from F-OMEGA-SCALE.txt per-rung table ---
rungs   = ["d384", "d512", "d768", "d1024", "d768x2"]
labels  = ["d384\n12k", "d512\n12k", "d768\n12k", "d1024\n12k", "d768x2\n24k"]
base    = [3.097779, 3.097779, 3.097779, 3.097779, 3.097779]   # flat every rung
a_only  = [1.163912, 1.135576, 1.161196, 1.200092, 1.082053]
min_lrn = [0.902957, 0.870090, 0.892407, 0.921136, 0.824209]
dvsbase = [2.1948,   2.2277,   2.2054,   2.1766,   2.2736]      # Δ-vs-base (a_only..)
uniform = 5.545177

# sanity: min_learned must be the lowest bar and HOLD (< a_only < base) every rung
for b, a, m in zip(base, a_only, min_lrn):
    assert m < a < b, (m, a, b)

x = np.arange(len(rungs))
w = 0.26

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(11.0, 4.2))

# ---- left: grouped CE bars ----
c_base = "#9aa0a6"; c_aonly = "#4c78a8"; c_min = "#2ca02c"
ax0.bar(x - w, base,    w, label="base (.clm mouth)", color=c_base)
ax0.bar(x,     a_only,  w, label=r"a_only ($\mathrm{base}+\alpha A$)", color=c_aonly)
ax0.bar(x + w, min_lrn, w, label=r"min_learned ($g_B\,\mathrm{base}+g_A A$)", color=c_min)
ax0.axhline(uniform, ls=":", lw=1.0, color="#d62728")
ax0.text(len(rungs) - 1 + 0.18, uniform - 0.18, "uniform 5.545",
         ha="right", va="top", fontsize=8, color="#d62728")
ax0.set_xticks(x); ax0.set_xticklabels(labels, fontsize=8)
ax0.set_ylabel("held-out TEST CE (nats/byte)")
ax0.set_title("(a) per-rung CE: min-gate HOLDS at every scale")
ax0.set_ylim(0, 3.7)
ax0.legend(fontsize=7.5, loc="upper center", ncol=1, framealpha=0.9)
ax0.grid(axis="y", ls="--", alpha=0.35)
# annotate the min_learned value above each green bar
for xi, m in zip(x, min_lrn):
    ax0.text(xi + w, m + 0.05, f"{m:.3f}", ha="center", va="bottom", fontsize=6.5, color=c_min)

# ---- right: Δ-vs-base advantage, flat across the ladder ----
ax1.plot(x, dvsbase, "o-", color=c_min, lw=1.8, ms=7)
mean = np.mean(dvsbase[:4])  # d384..d1024 (the dim ladder, per the +2.20±0.03 claim)
ax1.axhline(mean, ls="--", lw=1.0, color="#888")
ax1.fill_between([-0.4, len(rungs) - 0.6], mean - 0.03, mean + 0.03,
                 color="#2ca02c", alpha=0.12, zorder=0)
ax1.text(0.02, mean + 0.035, r"flat $+2.20\pm0.03$ (d384$\to$d1024)",
         fontsize=8, color="#555")
for xi, dv in zip(x, dvsbase):
    ax1.annotate(f"+{dv:.4f}", (xi, dv), textcoords="offset points",
                 xytext=(0, 8), ha="center", fontsize=7)
# flag the more-competent rung as the largest margin
ax1.annotate("largest margin\n(most competent)", (4, dvsbase[4]),
             textcoords="offset points", xytext=(-6, -34), ha="center",
             fontsize=7, color="#444",
             arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))
ax1.set_xticks(x); ax1.set_xticklabels(labels, fontsize=8)
ax1.set_ylabel(r"A-wire advantage $\Delta$-vs-base (nats/byte)")
ax1.set_title("(b) advantage is SCALE-STABLE (not a $d512$ artifact)")
ax1.set_ylim(2.10, 2.32)
ax1.set_xlim(-0.5, len(rungs) - 0.5)
ax1.grid(axis="y", ls="--", alpha=0.35)

fig.suptitle("OMEGA minimal A-wire gate across a 5-rung leak-free competent scale ladder "
             "(R8 / OΩ4·OΩ5, #1806)", fontsize=10.5, y=1.005)
fig.tight_layout(rect=[0, 0, 1, 0.97])

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig01_scale_ladder.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig01] wrote {out}")
