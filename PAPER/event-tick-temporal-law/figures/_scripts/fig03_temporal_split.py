#!/usr/bin/env python3
"""fig03 — H_1184 temporal split of the two bimodal peaks (audio, N=10).

At the scarcity peak K=4 the time-shuffle HELPS (drop<0 -> non-temporal,
variance-spread artifact); at the coverage peak K=40 the shuffle KILLS the
advantage (drop>0 -> temporal). Numbers verbatim from
.verdicts/1184_temporal_grounding/H_1184.txt.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..")

# per_peak from H_1184
peaks  = ["K=4\n(scarcity peak)", "K=40\n(coverage peak)"]
d_real = np.array([1.2370554294843201, 1.2899876477218697])
d_shuf = np.array([2.6661032238934257, 0.21736921029971432])
drop   = d_real - d_shuf  # [-1.429, +1.073]

x = np.arange(2)
w = 0.34

fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.bar(x - w/2, d_real, w, label=r"$d_{\mathrm{real}}$ (real time-order)",
       color="#1f5fbf")
ax.bar(x + w/2, d_shuf, w, label=r"$d_{\mathrm{shuf}}$ (time-shuffled)",
       color="#c0c0c0", edgecolor="#909090")

ax.annotate("shuffle HELPS\ndrop=-1.43\n-> NON-temporal\n(variance-spread)",
            xy=(0 + w/2, 2.666), xytext=(0.28, 2.05),
            fontsize=8.2, color="#b03030", ha="left",
            arrowprops=dict(arrowstyle="->", color="#b03030", lw=1.0))
ax.annotate("shuffle KILLS\ndrop=+1.07\n-> TEMPORAL\n(coverage reads time)",
            xy=(1 - w/2, 1.290), xytext=(0.95, 1.9),
            fontsize=8.2, color="#207020", ha="left",
            arrowprops=dict(arrowstyle="->", color="#207020", lw=1.0))

ax.axhline(0.0, color="k", lw=0.8)
ax.set_xticks(x)
ax.set_xticklabels(peaks, fontsize=9)
ax.set_ylabel(r"Cohen's $d$(derivative, metronome) stage-decode")
ax.set_title("H_1184 temporal split: the two peaks differ in kind (audio, N=10)",
             fontsize=10.5)
ax.legend(loc="upper center", fontsize=8.5)
ax.grid(True, axis="y", alpha=0.18)
ax.set_ylim(-0.2, 3.0)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig03_temporal_split.png"), dpi=160)
fig.savefig(os.path.join(OUT, "fig03_temporal_split.pdf"))
print("[fig03] wrote fig03_temporal_split.{png,pdf}")
