#!/usr/bin/env python3
"""fig06_mount_ladder.py — engine-mount ladder MID -> 3B (matplotlib DATA figure).

EVERY value verbatim from:
  .verdicts/convmoe-3b-engine-rung/SUMMARY.txt  (3B: train_ce 1.90689, val_ce_rand
    1.90365, rel_gap 0.04894, params 3,072,954,654, uniform 5.54518)
  MID rung = 7.479M (engine-mount CLMConvMoE, #1862, 3-axis GREEN)

The 7B (M13) rung is shown as a FUTURE scale-extension (currently training).
Plain underscores in text — no LaTeX escapes in matplotlib; mathtext only in $...$.
All annotations placed INSIDE the data range so bbox_inches stays tight.
Output: figures/fig06_mount_ladder.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GREEN = "#2ca02c"
BLUE  = "#4c78a8"
GREY  = "#9aa0a6"
ORANGE = "#e6a23c"

# ── verbatim numbers ─────────────────────────────────────────────────────────
P_3B   = 3072.954654   # 3.073B in millions
TRAIN_CE = 1.90689
VAL_CE   = 1.90365
REL_GAP  = 0.04894
UNIFORM  = 5.54518
# 7B future (M13, currently training; ce@2000 1.66547 from step0 5.64) — shown dashed
P_7B  = 7000.0
CE_7B = 1.66547

fig, (axL, axR) = plt.subplots(1, 2, figsize=(11.0, 4.4), constrained_layout=True)

# ── panel (a): CE vs params (log-x) ──────────────────────────────────────────
axL.axhline(UNIFORM, color=GREY, ls=":", lw=1.1)
axL.text(2.0e3, UNIFORM + 0.08, "uniform $\\ln 256$ = 5.54518", color=GREY,
         ha="center", va="bottom", fontsize=8.5)
axL.plot([P_3B], [TRAIN_CE], "o", color=GREEN, ms=11, label="3B train_ce 1.90689")
axL.plot([P_3B], [VAL_CE],  "s", color=BLUE,  ms=8,  label="3B val_ce_rand 1.90365")
# rel_gap note placed INSIDE the axes (above the 3B point), no off-canvas xytext
axL.annotate("rel_gap 0.04894\n(GENERALIZES)", xy=(P_3B, VAL_CE),
             xytext=(P_3B, VAL_CE + 1.7), fontsize=8.6, color=GREEN, ha="center",
             arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
axL.plot([P_7B], [CE_7B], "D", color=ORANGE, ms=9, mfc="none", mew=1.6,
         label="7B (M13) ce@2000 1.66547 — future")
axL.plot([P_3B, P_7B], [VAL_CE, CE_7B], "--", color=ORANGE, lw=1.1)
axL.set_xscale("log")
axL.set_xlim(2.0e3, 1.05e4)
axL.set_xlabel("parameters (millions, log)")
axL.set_ylabel("cross-entropy (nats/byte)")
axL.set_ylim(0, 6.2)
axL.set_title("(a) engine-mount ladder: CE vs. params\n"
              "3B (measured) $\\to$ 7B (future)", fontsize=10)
axL.legend(fontsize=7.6, loc="upper right")

# ── panel (b): the 3B generalization gap ─────────────────────────────────────
labels = ["first_ce\n5.84073", "train_ce\n1.90689", "val_ce(rand)\n1.90365",
          "val_ce(contig)\n2.00021"]
vals   = [5.84073, 1.90689, 1.90365, 2.00021]
cols   = [GREY, GREEN, BLUE, BLUE]
bars = axR.bar(labels, vals, color=cols, edgecolor="black", linewidth=0.7)
for b, v in zip(bars, vals):
    axR.text(b.get_x() + b.get_width() / 2, v + 0.08, f"{v:.5f}", ha="center",
             va="bottom", fontsize=8)
axR.set_ylabel("cross-entropy (nats/byte)")
axR.set_ylim(0, 6.6)
axR.tick_params(axis="x", labelsize=8)
axR.set_title("(b) 3B GENERALIZES: val $\\approx$ train\n"
              "rel_gap 0.04894 $\\ll$ 1", fontsize=10)

out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig06_mount_ladder.pdf")
fig.savefig(out)
print(f"[fig06] wrote {out}")
