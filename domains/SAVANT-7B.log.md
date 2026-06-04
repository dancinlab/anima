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

## 2026-06-04 — rung0 build blocker #5 (forge dispatch impls) RESOLVED
- After the regen fixed the transpiler ABI, clm_prod LINK-failed: undefined `hexa_forge_dispatch_*`
  for db_colsum/int4_quant/int4_quant_bwd/residual_add/gelu/groupnorm/adamw_keepmv. These 7
  HEXA-FUSION-L1 forge dispatch wrappers are DECLARED in runtime.h but their C bodies are NOT
  integrated into runtime.c at the local commit (they live as a DRAFT `drafts/lever_a_fragment.c`).
  ROOT: local hexa-lang commit predates the forge-dispatch integration the prior fires used.
- FIX: extracted the 7 missing fn pairs (14 fns: hexa_ wrapper + builtin) from lever_a_fragment.c
  into self/forge/forge_extra.c, #included after forge_tier_v1.c in runtime.c (im2col/col2im/adamw
  already present → only the 7 net-new added, no redefinition). runtime.c compiles clean (rc=0).
  rebuilt hexa driver → clm_prod build.

## 2026-06-04 — rung0 fire LAUNCHED then pod EVICTED (honest)
- clm_prod built CLEAN (CLM_RC=0, errors=0) after the 5-blocker fix chain. rung0_d768 fire LAUNCHED
  (d768 E2 8ep on the 585KB 5-lang starter, detached nohup on /workspace).
- ~3min into the fire, pod 39404862 SSH went refused, then the instance DISAPPEARED from vast
  (provider eviction of the interruptible instance — #2671 orphan/eviction scenario). /workspace
  ephemeral data LOST (no harvest possible from a vanished instance). registry pod forgotten
  (status=closed). myself.pods re-checked: 39404862 absent (gone, not leaked).
- a_wall_first re-fire: the COMPLETE working build recipe is now captured in a one-shot
  (savant_oneshot.sh — all 5 blockers pre-solved: file/clang apt, full self/ src, forge_extra.c
  inject, hexa cc --regen, then build+fire). Re-rented fresh H100 39410751, re-firing.

## 2026-06-04 — rung0 re-fire: 2nd pod ALSO evicted → shrink config for fast completion
- B200 pod 39410751: build PASSED (all RC=0, clm_prod CLEAN), rung0 fire ran ~3-5min at 100% CPU
  (host-bound interpreter, T=256 d768 epoch-1 not yet done) then the instance was EVICTED again
  (vast interruptible reclaim — 2nd eviction in a row, both within ~5-15min). registry forgotten.
- DIAGNOSIS: the host-bound interpreter d768/T256 fire (~30min) is LONGER than the vast
  interruptible eviction window (~5-15min) → the fire never reaches epoch CE before reclaim.
- FIX (a_wall_first practical): shrink to T=64 E2 6ep nsamp=64 (~16x lighter forward/backward →
  ~2-4min) so descent completes INSIDE the eviction window. Validates the pipeline + descent the
  same way at lower per-step cost. Re-rented fresh H100 (pod #3).
