#!/usr/bin/env python3
"""fig01 — H_1183 bimodal derivative-tick advantage curve over cell-capacity.

Real numbers, verbatim from .verdicts/1183_bimodal_capacity/H_1183.txt (d_curve)
and overlaid with the H_1178 audio inverted-U (.verdicts/1178_critical_capacity_tick).
Emits both PNG (matplotlib) and PDF (for \\includegraphics in main.tex).
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(__file__), "..")

# H_1183 (N=10, fine cap ladder) d(DERIVATIVE,METRONOME) stage-decode
K_1183 = [3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96]
d_1183 = [0.0, 1.2370554294843201, -0.23568929196680896, 0.008885942480709811,
          0.05055696961828667, -0.0646162025571694, -0.01555466072039176,
          0.14701828332012376, 1.1717472995162717, 0.8927161687413202,
          0.7502514936826506, 0.7573218441474898, 1.2899876477218697,
          0.826141009030421, 0.4347733539399861, 0.4833495950519602,
          0.038473553712068814, -0.7562461988890004]

# H_1178 (N=6 audio) single asymmetric inverted-U
K_1178 = [6, 8, 12, 16, 24, 32, 48, 64, 96]
d_1178 = [-0.15095982722698645, 0.47868225359000044, 0.5607824180925532,
          0.7407368030547042, 0.8096704517285566, 1.1521333863107566,
          0.6687312535800919, 0.0627478385071793, -0.05976602516932061]

fig, ax = plt.subplots(figsize=(7.2, 4.4))

ax.plot(K_1178, d_1178, "o-", color="#888888", lw=1.6, ms=5,
        label="H_1178 audio (N=6): single inverted-U, K*=32")
ax.plot(K_1183, d_1183, "s-", color="#1f5fbf", lw=2.0, ms=5,
        label="H_1183 (N=10, fine ladder): BIMODAL")

# annotate the two H_1183 peaks
ax.annotate("scarcity peak\nK=4  d=+1.24", xy=(4, 1.237), xytext=(7, 1.55),
            fontsize=8.5, color="#b03030",
            arrowprops=dict(arrowstyle="->", color="#b03030", lw=1.0))
ax.annotate("coverage peak\nK=40  d=+1.29", xy=(40, 1.290), xytext=(48, 1.55),
            fontsize=8.5, color="#207020",
            arrowprops=dict(arrowstyle="->", color="#207020", lw=1.0))
ax.annotate("valley\nK=5  d=-0.24", xy=(5, -0.236), xytext=(10, -0.62),
            fontsize=8.5, color="#555555",
            arrowprops=dict(arrowstyle="->", color="#555555", lw=1.0))

ax.axhline(0.0, color="k", lw=0.7, ls=":")
ax.axhline(0.5, color="#999999", lw=0.7, ls="--")
ax.text(96, 0.53, "d=0.5 advantage bar", ha="right", va="bottom", fontsize=7.5,
        color="#777777")

ax.set_xscale("log")
ax.set_xticks([4, 6, 8, 12, 20, 32, 48, 64, 96])
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_xlabel("cell-capacity $K$ (max cells, log scale)")
ax.set_ylabel(r"$d$(derivative, metronome)  stage-decode (Cohen's $d$, paired)")
ax.set_title("Event-tick advantage is BIMODAL over cell-capacity", fontsize=11)
ax.legend(loc="lower center", fontsize=8.0, framealpha=0.9)
ax.grid(True, which="both", alpha=0.18)
ax.set_ylim(-0.95, 1.8)

fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig01_bimodal.png"), dpi=160)
fig.savefig(os.path.join(OUT, "fig01_bimodal.pdf"))
print("[fig01] wrote fig01_bimodal.{png,pdf}")
