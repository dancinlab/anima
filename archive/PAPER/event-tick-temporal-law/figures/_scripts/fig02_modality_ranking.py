#!/usr/bin/env python3
"""fig02 — per-modality temporal ranking: d_real (at own cap K*) and the
time-shuffle drop = d_real - d_shuf. Temporal iff drop >= 0.5.

Numbers verbatim from:
  audio/text/video : .verdicts/1186_temporal_grounding_modalities/H_1186.txt
  numeric/image    : .verdicts/1188_numeric_image_modalities/H_1188.txt
  text(saccadic)   : .verdicts/1187_learned_surprise_reader/H_1187.txt
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..")

# (label, K*, d_real, d_shuf, temporal?)
rows = [
    ("numeric\n(AR1)",        16,  3.1683267640483117, -0.18493105571386906, True),
    ("audio\n(drift-tone)",   32,  1.1521333863107566,  0.2688310922289032,  True),
    ("text-saccadic\n(learned)", 24, 1.0154873423557071, 0.5031433779228894,  True),
    ("video\n(motion+cut)",   64,  0.4914664732419215, -0.6186769056595218,  False),
    ("text-byte\n(raw d/dt)",  4,  0.4988385350726899,  0.9052798625772911,  False),
    ("image\n(static)",        4,  0.0,                 1.3752636619073235,  False),
]

labels  = [r[0] for r in rows]
d_real  = np.array([r[2] for r in rows])
d_shuf  = np.array([r[3] for r in rows])
drop    = d_real - d_shuf
temporal = [r[4] for r in rows]

x = np.arange(len(rows))
w = 0.38

fig, ax = plt.subplots(figsize=(8.4, 4.6))
b1 = ax.bar(x - w/2, d_real, w, label=r"$d_{\mathrm{real}}$ (real time-order)",
            color="#1f5fbf")
b2 = ax.bar(x + w/2, d_shuf, w, label=r"$d_{\mathrm{shuf}}$ (time-shuffled)",
            color="#c0c0c0", edgecolor="#909090")

# drop annotations + temporal verdict.
# A modality is TEMPORAL iff BOTH gates pass: d_real>=0.5 (real advantage)
# AND drop>=0.5 (advantage destroyed by time-shuffle). video has drop>=0.5 but
# d_real=0.49<0.5 (advantage-bar miss) -> non-temporal; the note records why.
why = {
    "video\n(motion+cut)": "d_real<0.5",
    "text-byte\n(raw d/dt)": "drop<0.5",
    "image\n(static)": "drop<0",
}
for i in range(len(rows)):
    col = "#207020" if temporal[i] else "#b03030"
    tag = "TEMPORAL" if temporal[i] else "non-temporal"
    sub = "" if temporal[i] else f"\n({why.get(labels[i], '')})"
    ax.text(x[i], max(d_real[i], d_shuf[i]) + 0.12,
            f"drop={drop[i]:+.2f}\n{tag}{sub}", ha="center", va="bottom",
            fontsize=7.4, color=col, fontweight="bold")

ax.axhline(0.0, color="k", lw=0.8)
ax.axhline(0.5, color="#999999", lw=0.7, ls="--")
ax.text(len(rows)-0.5, 0.55, "d=0.5 bar", ha="right", fontsize=7.5, color="#777777")

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=8.2)
ax.set_ylabel(r"Cohen's $d$(derivative/surprise tick, metronome)")
ax.set_title("Per-modality temporal ranking: a modality reads time iff "
             "drop $=d_{\\mathrm{real}}-d_{\\mathrm{shuf}}\\geq 0.5$",
             fontsize=10.5)
ax.legend(loc="upper right", fontsize=8.5)
ax.grid(True, axis="y", alpha=0.18)
ax.set_ylim(-1.0, 4.0)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig02_modality_ranking.png"), dpi=160)
fig.savefig(os.path.join(OUT, "fig02_modality_ranking.pdf"))
print("[fig02] wrote fig02_modality_ranking.{png,pdf}")
