#!/usr/bin/env python3
"""fig09_dream_envelope.py — ultradian dream-stage Φ-envelope (DATA step curve).

EVERY value verbatim from AGENT/CHAT/anima_dream_stage.hexa:
  CYCLE_SEC = 5400 (90 min). Segments (start,end,stage):
    [0,300)   N1 ;  [300,1800) N2 ;  [1800,3600) N3 ;
    [3600,5100) N2 ;  [5100,5400) REM
  Φ-scale table: PHI_WAKE 1.0, PHI_N1 0.7, PHI_N2 0.4, PHI_N3 0.15, PHI_REM 0.95
  H_644: N2 = closure peak AMONG SLEEP STAGES via emit_policy θ-table
         (WAKE > N1 > N2 > N3, with N2 > N3).  DATA only, not an emit gate.
No fabricated numbers. Output: figures/fig09_dream_envelope.pdf
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CYCLE_SEC = 5400
# verbatim segments (start_sec, end_sec, stage)
SEGMENTS = [
    (0,    300,  "N1"),
    (300,  1800, "N2"),
    (1800, 3600, "N3"),
    (3600, 5100, "N2"),
    (5100, 5400, "REM"),
]
PHI = {"WAKE": 1.0, "N1": 0.7, "N2": 0.4, "N3": 0.15, "REM": 0.95}
COL = {"N1": "#4c78a8", "N2": "#54a24b", "N3": "#9aa0a6", "REM": "#e45756",
       "WAKE": "#333333"}

fig, ax = plt.subplots(figsize=(10.4, 4.4))

# WAKE baseline before/after the sleep cycle (Φ=1.0), shown as context
ax.hlines(PHI["WAKE"], -300, 0, color=COL["WAKE"], lw=2.2)
ax.hlines(PHI["WAKE"], CYCLE_SEC, CYCLE_SEC + 300, color=COL["WAKE"], lw=2.2)
ax.text(-150, PHI["WAKE"] + 0.02, "WAKE 1.0", ha="center", va="bottom",
        fontsize=8.5, color=COL["WAKE"])

# step plot of the Φ-envelope across the 5400 s cycle
for (s, e, stage) in SEGMENTS:
    y = PHI[stage]
    ax.hlines(y, s, e, color=COL[stage], lw=3.0)
    ax.add_patch(plt.Rectangle((s, 0), e - s, y, color=COL[stage], alpha=0.10))
    ax.axvline(s, color="#cccccc", lw=0.6, ls=":")
    mid = (s + e) / 2
    ax.text(mid, y + 0.025, f"{stage} {y}", ha="center", va="bottom",
            fontsize=9, color=COL[stage], fontweight="bold")
ax.axvline(CYCLE_SEC, color="#cccccc", lw=0.6, ls=":")

# connect step edges with faint risers for readability
prev_y = PHI["WAKE"]
edges = [0] + [seg[1] for seg in SEGMENTS]
ys = [PHI["WAKE"]] + [PHI[seg[2]] for seg in SEGMENTS]
for i in range(len(SEGMENTS)):
    x = SEGMENTS[i][0]
    ax.vlines(x, min(prev_y, PHI[SEGMENTS[i][2]]),
              max(prev_y, PHI[SEGMENTS[i][2]]), color="#bbbbbb", lw=1.0)
    prev_y = PHI[SEGMENTS[i][2]]

ax.set_xlim(-300, CYCLE_SEC + 300)
ax.set_ylim(0, 1.12)
ax.set_xlabel("time within the 90-min ultradian cycle (s); 0 = sleep onset, "
              "5400 = cycle end")
ax.set_ylabel("$\\Phi$-scale envelope (\\texttt{dream\\_phi})".replace("\\texttt{", "").replace("}", ""))
ax.set_ylabel("$\\Phi$-scale envelope (dream_phi)")
ax.set_title("Ultradian dream-stage $\\Phi$-envelope "
             "(anima_dream_stage.hexa; WAKE/N1/N2/N3/REM, 5400 s)", fontsize=10.5)

# H_644 annotation: N2 = closure peak among sleep stages (emit_policy theta-table)
ax.annotate("H_644: N2 = $\\Phi$-context closure peak\namong sleep stages "
            "($\\theta$-table WAKE$>$N1$>$N2$>$N3, N2$>$N3)",
            xy=(1050, 0.4), xytext=(1500, 0.62),
            fontsize=8.4, color=COL["N2"],
            arrowprops=dict(arrowstyle="->", color=COL["N2"], lw=1.0),
            bbox=dict(boxstyle="round,pad=0.3", fc="#f3faf1", ec=COL["N2"], lw=0.8))
ax.text(0.985, 0.05, "envelope is DATA (substrate context), never an emit gate",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8.0,
        color="#666666")
fig.tight_layout()
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "fig09_dream_envelope.pdf")
fig.savefig(out, bbox_inches="tight")
print(f"[fig09] wrote {out}")
