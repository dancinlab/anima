#!/usr/bin/env python3
"""fig04 — H_1189 simultaneous fusion: fused decode-acc does NOT beat the best
single modality (surface-gated collapse), although the fused advantage IS
temporal. Numbers verbatim from .verdicts/1189_simultaneous_multimodal/H_1189.txt
(per_stream deriv_acc_mean + F1/F2).
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..")

names = ["audio", "text", "image", "FUSED"]
deriv = [0.5954166666666667, 0.61525, 0.8271666666666666, 0.34900000000000003]
metro = [0.3907083333333334, 0.381125, 0.5233333333333333, 0.15995833333333334]
chance = 0.16666666666666666
best_single = 0.8367083333333334  # F1 best_single_deriv_acc_mean

x = np.arange(len(names))
w = 0.38
colors = ["#7aa6e0", "#7aa6e0", "#7aa6e0", "#1f5fbf"]

fig, ax = plt.subplots(figsize=(7.0, 4.4))
ax.bar(x - w/2, deriv, w, label="derivative arm", color=colors)
ax.bar(x + w/2, metro, w, label="metronome arm", color="#cccccc",
       edgecolor="#999999")

ax.axhline(best_single, color="#b03030", lw=1.3, ls="--")
ax.text(0.0, best_single + 0.01, "best single-modality deriv acc = 0.837",
        fontsize=8, color="#b03030")
ax.axhline(chance, color="#777777", lw=0.8, ls=":")
ax.text(len(names)-0.5, chance + 0.005, "decode chance 0.167", ha="right",
        fontsize=7.5, color="#777777")

ax.annotate("FUSED=0.349 << best part 0.837\n"
            r"$d_{\mathrm{fused-best}}=-2.79$  (F1 FAIL)"
            "\nfusion only RECOVERS the strongest part",
            xy=(3 - w/2, 0.349), xytext=(1.2, 0.55),
            fontsize=8.0, color="#b03030",
            arrowprops=dict(arrowstyle="->", color="#b03030", lw=1.0))

ax.set_xticks(x)
ax.set_xticklabels(names, fontsize=9)
ax.set_ylabel("stage-decode accuracy (own $K^*$)")
ax.set_title("H_1189 simultaneous fusion is surface-gated: 1+1+1 < best part",
             fontsize=10.2)
ax.legend(loc="upper right", fontsize=8.5)
ax.grid(True, axis="y", alpha=0.18)
ax.set_ylim(0.0, 0.95)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig04_fusion.png"), dpi=160)
fig.savefig(os.path.join(OUT, "fig04_fusion.pdf"))
print("[fig04] wrote fig04_fusion.{png,pdf}")
