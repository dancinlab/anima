# d768 DEPLOY-THEN-FIRE recovery — verdict (2026-06-02)

Pod: vast `38991004` (NVIDIA H100 80GB HBM3, driver 595.71.05) · project=anima · purpose=d768-recovery

## DEPLOY-GATE (PHASE ②) — PASS
- origin/main carries BOTH fixes:
  - #2472 `fix(forge): route FP64 conv GEMM dispatch to cuBLAS` (commit 32228c31b)
  - #2478 `fix(cloud): idempotent cloud rent per (project,purpose)` (commit 7f905bc50)
- `~/.hx/src` synced to origin/main HEAD (`efdba81`); `hexa cloud rent --selftest` → all 7 PASS
  (`rent_selftest PASS — idempotent-rent dedup verified`).
- Pod-side build: stale pre-baked hexa was glibc-2.38-broken + missing all gitignored seed `.c`.
  Repaired by: patchelf hexa.real/hexat/hexa_module_loader → staged glibc-2.39 loader;
  shipped the 44 seed `.c` from the mac install; compiled runtime.o natively WITH -DHEXA_CUDA.
  #2472 cuBLAS dispatch present in linked runtime.c (line 8644: FP64 MATMUL → hexa_farr_matmul_gpu).

## FIRE (PHASE ①) — d768/12L on c4 5-lang backbone
- corpus: dancinlab/clm-backbone-5lang-sample (clm_backbone_5lang_sample.txt, 67,733,069 bytes, 20000 records)
- config: d=768, E=2, epochs=12, nwin=8, T=24, V=256, K=3 (CLMConvMoE int4-QAT)
- trainer: stdlib/flame/clm_prod.hexa (PR4 — env d/E/epochs/nsamp override + .clm save), `hexa run`

### CE descent (F-CLM-PROD-DESCENT) — PASS (verbatim)
    epoch-1  mean CE = 4.71554
    epoch-12 mean CE = 0.859092
    F-CLM-PROD-DESCENT = 1
    PASS — real-corpus mean CE descends under int4 envelope

### GPU util (F-RFC046 re-check) — RED (verbatim, honest)
    UTIL: n=1617 PEAK=0% MEAN=0.000% pct_gt20=0.0%
    (live nvidia-smi during run: 0% util, 0 MiB GPU mem, 67W idle — trainer ran 100% on ONE CPU core)

RED root cause (structural, NOT fixed by #2472 alone): the `hexa run` user-program build
links only `-lm -lpthread` (os_clang_ldflags, self/main.hexa:1186) — it never compiles the
trainer with -DHEXA_CUDA nor links cuBLAS/cudart + the nvcc runtime_cuda.o. So forge's
FP64-conv→hexa_farr_matmul_gpu (#2472) always takes the CPU fallback. #2472 is necessary but
not sufficient; the host-side `hexa run` link is the bottleneck (consistent with prior F-RFC046
"1-4% util RED"). Closing this needs a `hexa run --cuda` link path (cuBLAS + runtime_cuda.o),
filed for hexa-cloud.

## CKPT (a_fire_recover_complete) — RECOVERED + VERIFIED
- artifact: d768_5lang_c4.clm — 3,651,389 bytes, 6 int4 blocks, "CLM\x01" magic
- sha256: 6975dbb090290ea15e0fb051665d424872f558499f0e63a320582cf403750bd1
- local home: ~/.anima/ckpt/d768_recovery_2026_06_02/d768_5lang_c4.clm (sha re-verified after pull + move)
- ROOT FIX that ends the "lost twice" failure: clm_prod.hexa PR4 now writes CLM_PROD_OUT — prior
  PR1 printed a CE descent with NO saved weights (a lost model). PR4 save-path lives on local
  branch feat/clm-prod-env-corpus (not yet on origin/main); it was overlaid into HEXA_SRC for this fire.

## HF upload (a_hf_autonomous · PRIVATE) — DONE
- repo: dancinlab/anima-clm-d768-util-probe (PRIVATE — intermediate util-probe, not closure-PASS)
- upload commit: 2e9255f4798bf88446d00101183fd50c4a6ee945 (ckpt + README model card + ckpt.sha256)
- collection: added to dancinlab CLM (dancinlab/clm-6a1cf58f621490134dade186 — .clm models, a_hf_collection_split)
- HF.jsonl row: run=anima_clm_d768_recovery_2026_06_02, status=uploaded, private=true

## Teardown (a_fire_recover_complete) — DONE
- hf-recover-guard marker verified (HF repo exists on Hub) → teardown allowed
- pod vast 38991004 destroyed (confirmed) — billing stopped
- also destroyed earlier: vast 38990747 (accidental RTX-6000 probe from a bare `rent vast` with no --query;
  the vast rent path ignores --gpu and selects any GPU — must pass `--query "gpu_name=H100_SXM"`)
- no d768-recovery billing pod remains; no other-project pod touched

## Handoff to hexa-cloud
- a_runpod_inbox: file the `hexa run --cuda` link-path gap (cuBLAS + runtime_cuda.o) so #2472's
  forge GPU dispatch can actually engage; and the stale-pod-image gap (glibc-2.38 binary + missing
  seed .c on a pre-baked pod) that required the patchelf + seed-.c ship workaround.
