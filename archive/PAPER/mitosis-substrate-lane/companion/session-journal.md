# session-journal — mitosis-substrate-lane

## 2026-06-15 — scaffold + draft v1

- Based worktree on origin/main (tip `de306d3af`, the H_1210 merge).
- Assembled the verdict matrix from the 9 merged MITOSIS-ENGINE verdicts
  (H_1202–H_1210) + 2 framing closed-negatives (H_1200/H_1201) + the clm_v2
  addendum. All numbers copied verbatim from `.verdicts/<slug>/<id>.txt` (p7,
  no LLM self-judge, no paraphrase).
- `/paper` plugin binary is NOT installed in this environment; scaffolded the
  directory + roster row by hand following the existing `PAPER/savant-iit4-bridge`
  convention (PAPER.tape row · PAPER.md · PAPER.log.md · main.tex · Makefile ·
  references.bib · figures/ · companion/). This is the same artifact the tool
  produces.
- Figures: fig01 stream-determinant (TikZ), fig02 separation ratios (pgfplots) —
  both native + reproducible via `make figures`. fig03 generated via fal.ai
  `fast-sdxl` (queue API, request 019eca73-...; downloaded 1024x576 PNG) as the
  illustrative concept image; prompt preserved in `figures/_prompts/`.
- Compile: `make` → xelatex x3 + bibtex → main.pdf, 14 pages, 0 undefined
  references / 0 undefined citations / 0 bibtex warnings.
- Gate check: all 9 section claims terminal (5🟢 + 2🔴 closed-neg; H_1203/H_1204
  partials are 🟢-parent sub-results). g51 satisfied (≥10 pages, ≥1 figure).
- Honest scope stated in §Limitations: toy DIM=8, single corpus, 3–5 seeds,
  gradient-free, $0 CPU; toy→prod transfer unverified; no frozen bar moved.
