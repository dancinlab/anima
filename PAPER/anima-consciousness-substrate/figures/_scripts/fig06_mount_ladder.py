#!/usr/bin/env python3
"""fig06_mount_ladder.py — engine-mount ladder MID -> 3B (matplotlib DATA figure).

EVERY value verbatim from:
  .verdicts/convmoe-3b-engine-rung/SUMMARY.txt  (3B: train_ce 1.90689, val_ce_rand
    1.90365, rel_gap 0.04894, params 3,072,954,654, uniform 5.54518)
  MID rung = 7.479M (engine-mount CLMConvMoE, #1862, 3-axis GREEN)

The 7B (M13) rung is shown as a FUTURE scale-extension (currently training).
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
# params (M)  ;  train_ce  ;  val_ce_rand  ;  rel_gap
PARAMS_M  = [7.479, 3072.954654]          # MID, 3B (3.073B = 3072.95M)
TRAIN_CE  = [None,  1.90689]              # MID train_ce not in the 3B verdict; plot 3B only for CE
VAL_CE    = [None,  1.90365]
REL_GAP   = [None,  0.04894]
UNIFORM   = 5.54518
# 7B future (M13, currently training; ce@2000 1.66547 from step0 5.64) — shown dashed
P_7B = 7000.0
CE_7B = 1.66547

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.0, 4.3))

# ── panel (a): CE vs params (log-x) ──────────────────────────────────────────
axL.axhline(UNIFORM, color=GREY, ls=":", lw=1.1)
axL.text(8, UNIFORM+0.06, "uniform $\\ln256$ 5.54518", color=GREY, ha="left",
         va="bottom", fontsize=8)
# 3B rung (measured)
axL.plot([PARAMS_M[1]], [TRAIN_CE[1]], "o", color=GREEN, ms=10, label="3B train\\_ce 1.90689")
axL.plot([PARAMS_M[1]], [VAL_CE[1]],  "s", color=BLUE,  ms=8,  label="3B val\\_ce\\_rand 1.90365")
axL.annotate("rel\\_gap 0.04894\\n(GENERALIZES)", xy=(PARAMS_M[1], VAL_CE[1]),
             xytext=(PARAMS_M[1]*0.16, VAL_CE[1]+1.4), fontsize=8.5, color=GREEN,
             arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
# 7B future (training)
axL.plot([P_7B], [CE_7B], "D", color=ORANGE, ms=9, mfc="none", mew=1.6,
         label="7B (M13) ce@2000 1.66547 — future")
axL.plot([PARAMS_M[1], P_7B], [VAL_CE[1], CE_7B], "--", color=ORANGE, lw=1.1)
axL.set_xscale("log")
axL.set_xlabel("parameters (millions, log)")
axL.set_ylabel("cross-entropy (nats/byte)")
axL.set_ylim(0, 6.2)
axL.set_title("(a) engine-mount ladder: CE vs.\\ params\nMID $\\to$ 3B (measured) $\\to$ 7B (future)",
              fontsize=10)
axL.legend(fontsize=7.5, loc="upper right")

# ── panel (b): the 3B generalization gap ─────────────────────────────────────
labels = ["first\\_ce\n5.84073", "train\\_ce\n1.90689", "val\\_ce(rand)\n1.90365",
          "val\\_ce(contig)\n2.00021"]
vals   = [5.84073, 1.90689, 1.90365, 2.00021]
cols   = [GREY, GREEN, BLUE, BLUE]
bars = axR.bar(labels, vals, color=cols, edgecolor="black", linewidth=0.7)
for b, v in zip(bars, vals):
    axR.text(b.get_x()+b.get_width()/2, v+0.07, f"{v:.5f}", ha="center",
             va="bottom", fontsize=8)
axR.set_ylabel("cross-entropy (nats/byte)")
axR.set_ylim(0, 6.5)
axR.set_title("(b) 3B GENERALIZES: val $\\approx$ train\nrel\\_gap 0.04894 $\\ll$ 1",
              fontsize=10)

fig.suptitle("CLMConvMoE engine-mount ladder (3B terminal; 7B = future scale-extension)",
             fontsize=11.5, y=1.02)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig06_mount_ladder.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig06] wrote {out}")
