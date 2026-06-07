#!/usr/bin/env python3
"""fig03_omega_ladder.py — OMEGA 5-rung minimal-gate scale ladder (matplotlib DATA).

EVERY value verbatim from:
  .verdicts/omega-engine/F-OMEGA-SCALE.txt  (per-rung min_learned, base, Delta-vs-base)
  .verdicts/omega-engine/F-OH1-MINGATE.txt  (uniform floor)

No fabricated points. Output: figures/fig03_omega_ladder.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── verbatim verdict numbers (F-OMEGA-SCALE.txt) ─────────────────────────────
RUNGS   = ["d384", "d512", "d768", "d1024", "d768x2"]
PARAMS  = [48_240_448, 85_816_384, 189_279_808, 334_686_272, 189_279_808]
MINLRN  = [0.902957, 0.870090, 0.892407, 0.921136, 0.824209]
DELTA   = [2.1948, 2.2277, 2.2054, 2.1766, 2.2736]   # Delta-vs-base
BASE    = 3.097779
UNIFORM = 5.545177

GREEN = "#2ca02c"
BLUE  = "#4c78a8"
GREY  = "#9aa0a6"

fig, (axL, axR) = plt.subplots(1, 2, figsize=(12.0, 4.3))

x = range(len(RUNGS))

# ── panel (a): min_learned CE per rung vs base / uniform ──────────────────────
axL.axhline(UNIFORM, color=GREY, ls=":", lw=1.1)
axL.text(len(RUNGS)-1, UNIFORM+0.06, "uniform $\\ln256$ 5.545177", color=GREY,
         ha="right", va="bottom", fontsize=8)
axL.axhline(BASE, color=BLUE, ls="--", lw=1.1)
axL.text(0, BASE+0.06, "base 3.097779", color=BLUE, ha="left", va="bottom", fontsize=8)
axL.plot(x, MINLRN, "o-", color=GREEN, lw=1.8, ms=7, label="min\\_learned (gB·base+gA·A)")
for xi, v in zip(x, MINLRN):
    axL.text(xi, v-0.18, f"{v:.4f}", ha="center", va="top", fontsize=8, color=GREEN)
axL.set_xticks(list(x)); axL.set_xticklabels(RUNGS)
axL.set_ylabel("held-out test CE (nats/byte)")
axL.set_ylim(0, 6.1)
axL.set_title("(a) minimal-gate HOLDS at every rung\nmin\\_learned $\\ll$ base $<$ uniform",
              fontsize=10)
axL.legend(fontsize=8, loc="center right")

# ── panel (b): Delta-vs-base flat at +2.20 +/- 0.03 ──────────────────────────
bars = axR.bar(x, DELTA, color=GREEN, edgecolor="black", linewidth=0.7, width=0.6)
axR.axhline(2.20, color=BLUE, ls="--", lw=1.2)
axR.text(len(RUNGS)-1, 2.20+0.012, "mean $+2.20\\pm0.03$", color=BLUE,
         ha="right", va="bottom", fontsize=9)
for b, v in zip(bars, DELTA):
    axR.text(b.get_x()+b.get_width()/2, v+0.004, f"+{v:.4f}",
             ha="center", va="bottom", fontsize=8)
axR.set_xticks(list(x)); axR.set_xticklabels(RUNGS)
axR.set_ylabel("A-wire advantage $\\Delta$ vs.\\ base (nats/byte)")
axR.set_ylim(2.10, 2.32)
axR.set_title("(b) advantage is SCALE-STABLE\n$48$M$\\to$$335$M params, $\\Delta$ flat",
              fontsize=10)

fig.suptitle("OMEGA minimal-gate 5-rung scale ladder (leak-free, causal\\_ca=True; "
             "self-test 0.000 every rung)", fontsize=11.5, y=1.02)
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig03_omega_ladder.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig03] wrote {out}")
