# SAVANT-7B rung0 — pipeline-validation forge CLM (Lane-G / GPU) — VERDICT

substrate = GPU (Lane G) · forge flame · `a_lane_akida_gpu_split` (NEVER merged with Lane A).
campaign = SAVANT-7B (domains/SAVANT-7B.md), rung0 of the 7B 5-lang descent ladder.
scope (a_scale_honest_scope) = **PIPELINE VALIDATION** — small d768 forge CLM on the 5-lang
starter. NOT a 7B, NOT a competent LM. Validates forge train+ckpt+recover on real GPU.
date = 2026-06-04 · est cost ~$2-3 (a_fire_autonomous, no cost gate).

## pod + build (3-GATE / GPU-required, a_train_flame_forge)
- pod = vast 39410751, **NVIDIA B200 183 GB**, ssh5.vast.ai:10750, CUDA-devel 12.4, persistent
  /workspace. (First pod 39404862 RTX-PRO-6000 was EVICTED mid-fire — re-fired here, a_wall_first.)
- build = self-host hexa from source (prebuilt needs GLIBC_2.38 > image 2.35). 5 blockers solved
  (see SAVANT-7B.log.md): GLIBC, gitignored seeds, `file` util, stale hexa_cc.c seed (→ hexa cc
  --regen), forge dispatch impls unintegrated (→ forge_extra.c inject). clm_prod CLM_BUILD_RC=0.
- trainer = `hexa-lang/stdlib/flame/clm_prod.hexa` (CLMConvMoE + int4-QAT), run via `hexa run`.

## rung0 fire (g63 VERBATIM)

CONFIG rung0_d768 : d=768 T=256 E=2 nsamp=96 epochs=8, corpus savant_5lang_starter.txt
(585060 B, 10069 lines, sha256 1e77262690725b731f4c22823612110d67f2ddf825cadea8bf9c5bc724119eae)

```
<FILL: FIRE_RC / wall / UTIL / DEVMEM / epoch-1 mean CE / epoch-8 mean CE / F-CLM-PROD-DESCENT / ckpt sha256>
```

## descent verdict
<FILL: PASS (CE descends) or FAIL (honest) — verbatim>

## util (NOT a campaign gate — host-bound CLOSED, recorded only)
<FILL: UTIL line>

## artifact
<FILL: ckpt path + sha256 + HF repo>

## 7B ETA (see domains/SAVANT-7B.md §4) — interpreter 7B INFEASIBLE (~5yr), device-resident
BF16-TC on 3× H100 ~1 day / ~$150-250 (a_wall_first). The 7B is gated on the device-resident step
path, not GPU spend.
