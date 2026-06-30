# PAPER.log — aura-noninvasive-depth-wall

- 2026-05-30 scaffold: main.tex (12-section, 2 TikZ figures) + refs.bib written.
  RESUME check: no prior scaffold on origin/main or worktree; started fresh.
  Distinct from PR#1483 aura-electrode-position-phi-proxy (A-axis scalp position) —
  this is C-axis depth/direction (non-invasive->invasive-grade, depth wall,
  read/write asymmetry).
- Source verdicts (all origin/main, quoted verbatim):
  C15-depth-wall-terminal.md, AURA-DEPTH/DEPTH-3SHELL-CORRECTION.md,
  AURA-HEADMODEL/SPHERE-VALIDATION.md, C6/C7/C16/B7, AURA-AXES-INDEX.md.
- Headline: 3-shell ecc-sweep R2 cortex 0.239 -> deep 0.016 (x15.4); same-harness
  Gaussian x3.2; C15-published Gaussian full-stack best-env 0.820->0.098 (x8.4).
  3-shell wall STEEPER than even best-env -> Gaussian was NOT over-stating (sign
  reversal of AURA-HEADMODEL conjecture). Saturation = Gaussian artifact: 3-shell
  keeps gaining 0.19->0.40 to 1024 contacts (SPHERE-VALIDATION Q2). Cortical levers:
  EEG-64 0.329 -> RTSC-MEG 0.764 -> full-stack+time 0.820; tFUS best deep 0.153.
  Deep route = tFUS write only (read/write asymmetry, AURA-AXES).
- Finding: 🔴 closed-negative non-invasive deep control (B7 independent convergence)
  + 🟢 cortical-surface near-invasive window (~0.82-0.90) + 🎯 write-only deep route.
- Honesty: 🟡 toy (spherical/Gaussian head). NOT-MEASURED = real head, real data,
  builtin Phi. Qualitative rulings robust (faithful model made wall STRONGER).
- 2026-05-30 LESSON: agent is isolated in worktree; first compile/writes hit the
  shared checkout path and were rejected/empty. Redone inside worktree.
