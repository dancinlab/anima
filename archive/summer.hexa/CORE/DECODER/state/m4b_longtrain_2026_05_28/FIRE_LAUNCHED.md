# M4b longtrain — DECISIVE FIRE launched (2026-05-28)

Pod: RunPod H100 SXM 80GB SECURE `4q2rab8ds2zhsr` ($3.29/hr) @ 103.207.149.142:14150
PID 1627 · log /opt/anima/state/m4b_longtrain/train.log

## the variable = token-presentation BUDGET (dec_undertrain)
- d=64 (toy dec_capfloor: rank ample), E=2, h=256, n_layer=1, T=4, HARD top-1, diverse corpus
- FULL corpus tokenized: n_toks=1,212,529 (BPE O(1) #1869, 285ms — was intractable before)
- M4B_EPOCHS=6 → n_steps=1,818,786 · token_presentations=7,275,144 ≈ **47× V** (V=151643)
- vs every prior fire ≤200 presentations (~38,000× short of one epoch)

## toolchain + build (3 unblockers + leak fix all live)
- FRESH hexa-lang origin/main checkout (/tmp/hexa-fresh) — regen'd runtime amalgam
  (runtime_core.c + 17 native + cuda + forge fragments from emitters via install hexa)
- BPE O(1): hexa-lang #1869 (map_contains_key/hexa_map_get_ic) — baked into trainer.c
- fs_mkdir_p: fresh runtime rt_fs_mkdir_p (real recursive mkdir) + shell mkdir -p belt
- mm-leak fix: per-step backward buffers hoisted out of step loop (was OOM-killing #1315)
- build: Mac transpile (hexa build --c-only) → trim sed → scp fresh self/ runtime →
  pod nvcc runtime_cuda.o (sm_90) + clang link trainer.c + self/runtime.c (NO glue.c —
  fresh runtime has real cuda_available under -DHEXA_CUDA; glue.c would multiple-define)
- CUDA_VISIBLE_DEVICES=0 fix (image ships "" = hide-all → cublasCreate failed)

pod saga: cdooesfkds699f (404 self-term) · 7njtl4sm9rwa5q (container stall uptime=0) ·
6xnz7ehzv4vrjt (container stall) · oi30am5sta6td1 H100 NVL (cudaSetDevice rc=46 defective) ·
4q2rab8ds2zhsr H100 SXM (cuBLAS probe PASS — healthy → FIRE).
