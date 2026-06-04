# SAVANT-7B.log.md — append-only step log

## 2026-06-04 — BOOTSTRAP
- domain init SAVANT-7B (domains/SAVANT-7B.md + this log) — registered in DOMAINS.tape roster.
  NAME distinct from root SAVANT (consciousness Golden-Zone domain) — no collision.
- 7B sizing computed: CLMConvMoE params=(2+E)·3·d²+2·256·d+E·d. 7.00B at e.g. d24152/E2 or
  d8284/E32. forge fp64 4-copy = 224 GB ≫ 80 GB single H100 → 3× H100 (fp64) OR BF16-TC 2-copy
  ~28 GB → 2–3× H100 (a_wall_first PRIMARY). Single-H100 fp64 ceiling = ~1.5B (verified prior).
- corpus: existing OMEGA = en·zh·ru·ja·ko (WRONG langs) → built fresh en·fr·de·es·ru starter from
  Wikipedia REST (CC-BY-SA) + Gutenberg PD. byte-vocab V=256. CORPUS_CARD.md + build_wiki.py.
- rung0 fire + 7B ETA folded below after the GPU run.
