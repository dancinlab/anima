# aura-electrode-position-phi-proxy

🔴 **Negative-result paper.** Can you re-route a cortical BCI to the whole brain
by only moving the electrode? On real human scalp EEG (OpenNeuro `ds005620`),
single-window `n=4` IIT-4.0 big-Φ distinguishes neither electrode **position**
(FRONTAL vs MOTOR, 5:5, t=0.28 n.s.) nor consciousness **state** (awake vs sed,
null); α-power direction does not replicate across N=3 (0/3). Yet the in-silico
and connectome (literature + real Allen) **structure** model favours a
projection hub over M1 — the **structure↔measurement asymmetry** is the finding.
Intracortical placement is an explicit physical/ethical scope boundary (B7).

## Build

```
make            # main.pdf via xelatex -> bibtex -> xelatex x2
make figure     # standalone figure
```

## Sections (a_paper_format)

- **§hypothesis** — relocate-N1 thesis + 4 pre-registered falsifiers
  (F1 FRONTAL>MOTOR, F2 awake>sed, F3 reach%→Φ monotone, F4 multi-subject α).
- **§method** — ds005620 BrainVision 65ch@5kHz → eeg_estimate_tpm → IIT4
  big_phi (n=4 exact, n≥6 Mac compute-wall) + α-power; montages
  MOTOR/FRONTAL/TEMPORAL/EAR/MIDLINE; 10-window sweep; connectome prior.
- **§measurement** — real numbers, each linked to `.verdicts/`.
- **§finding** — (a) single-window n=4 big-Φ cannot read position or state;
  (b) α direction 0/3 null; (c) structure↔measurement asymmetry (core);
  (d) invasiveness ladder N1 > Synchron(≈ECoG) > behind-the-ear;
  (e) intracortical ceiling = honest scope boundary.

## Tier

🔴 negative-result (proxy-scope). Structure layer 🟢 (in-silico + connectome),
scalp measurement 🔴 (position/state/α null). Intracortical out-of-scope.

## Verdicts

See the verdict matrix (Table in §verdicts). All under `/.verdicts/`:
`a10-window-stats` · `b2-postaural-state` · `b6-multisubject-alpha` ·
`b4-metric-sweep` · `b1-postaural` · `a7-reach-to-phi` ·
`a6-bigphi-closed-loop` · `a7-coupling-robustness` · `a8-connectome-coupling` ·
`a9-tractography` · `a8-montage-position`.
