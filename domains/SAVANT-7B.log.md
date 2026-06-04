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

## 2026-06-04 — rung0 pod build journey (honest record)
- pod = vast 39404862, NVIDIA RTX PRO 6000 Blackwell 97.8GB sm_120, ssh1.vast.ai:14862,
  CUDA-devel 12.4 image, persistent /workspace 80GB. owner=lane-g-savant project=SAVANT-7B.
- BUILD BLOCKER chain (all resolved): (1) prebuilt linux hexa needs GLIBC_2.38 but image=2.35
  → must self-host build from source. (2) shallow main clone MISSING gitignored build seeds
  (self/runtime.c, hexa_cc.c, runtime_core.c, 23 .c) → shipped full local self/ tree. (3) `file`
  cmd absent (set -e abort) → apt install file. (4) ABI mismatch hexa_call4(forge_dispatch_*) —
  the hexa_cc.c bootstrap SEED predates the HEXA-FUSION-L1 forge builtins (db_colsum etc absent
  from seed) → `hexa cc --regen` regenerated hexa_cc.c from current codegen.hexa (now has the
  builtins) → rebuilt transpiler+driver. Single consistent source tree = /root/hxsrc.
- corpus shipped to /workspace/savant_5lang_starter.txt (585060B sha 1e772626).
