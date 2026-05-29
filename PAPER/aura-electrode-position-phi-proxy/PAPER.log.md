# PAPER.log — aura-electrode-position-phi-proxy

- 2026-05-30 scaffold: created PAPER/aura-electrode-position-phi-proxy/
  (main.tex, references.bib, Makefile, README, figures/, companion/).
  Registered in root PAPER.tape.
- 2026-05-30 sections filled (a_paper_format): §hypothesis (relocate-N1 thesis +
  4 pre-registered falsifiers F1-F4 + F5 equivalence probe), §method
  (ds005620 BrainVision 65ch@5kHz pipeline, n=4 exact, n>=6 compute-wall,
  5 montages, 10-window sweep, in-silico + literature + real-Allen connectome
  priors), §measurement (all numbers verbatim from .verdicts/), §finding
  (5 closed-negatives + structure<->measurement asymmetry + invasiveness ladder
  + intracortical ceiling). Every claim linked to its .verdicts/ pointer
  (a_paper_sections); verdict matrix table added.
- 2026-05-30 figure: fig01 two-panel TikZ/pgfplots — (A) invasiveness x reach
  3-position ladder (N1 > Synchron approx ECoG > behind-the-ear),
  (B) window-fragility FRONTAL-MOTOR per-window bar (5:5 split). Body shared
  by main.tex (\input) and standalone wrapper. (Self-contained vector figure;
  no fal.ai call needed — TikZ is the reproducible/auditable choice for a
  data plot of the verdict numbers.)
- 2026-05-30 compile: see PR/build notes for page count + engine.
