# CLM TRAINING — SSOT (START HERE before any train/fire)

> The CLM trainer is authored hexa-native on `hexa-lang:stdlib/flame` and runs on
> the forge GPU substrate. This file is the navigation source: where the trainer
> is, which stack to use, how to fire. Binding: `@D a_train_flame_forge` ·
> `@D a_akida_native_train`.
>
> **Whole-picture map** (training · on-chip learning · road to 7B):
> [`ANIMA_TRAINING_AND_7B_MAP.md`](./ANIMA_TRAINING_AND_7B_MAP.md).

## 🔒 measure ⊥ deploy (P6 §0 · @L2 · H_679/H_904)

anima learns **on the chip** — AKIDA on-chip non-deterministic plasticity is the
identity (the sole HW↔SW difference, live on AKD1000 at H_904 🟢). The chip runs
the int4 backbone byte-identical and opens learning there.

The GPU flame+forge QAT is the **PLASTI-SIM**: it measures whether the int4
backbone allows production quality across the scale ladder. It produces the
backbone the chip transplants; learning lives on the chip.

```
deploy / LEARN track (HW = AKIDA)        measure track (GPU)
─────────────────────────────────       ─────────────────────────────
on-chip non-deterministic plasticity     flame+forge QAT backbone scale-measure
= anima's learning = the identity        = PLASTI-SIM instrument
same input → different trace (alive)     deterministic backbone envelope check
```

The R4 large 44.68M H100 fire is a measurement rung. See
`CLM/P6_SCALE_LADDER_7B.md` §0 ("GPU = 계측기 · 학습자 = 온칩 비경첩 가소성") ·
`UNIVERSE/H_904` (on-chip plasticity 🟢).

## flame vs forge — usage criteria

| layer | what it is | you use it for | lives in |
|---|---|---|---|
| **flame** | hexa-native NN + autograd stdlib (tensors · `ag_tape` autograd · `nn_lib` ops · `decoder_lib` · `train_lib` · `opt_*`) | **author** the trainer/model in `.hexa` | `hexa-lang:stdlib/flame/*.hexa` |
| **forge** | GPU execution substrate — device-resident farr + cuBLAS Dgemm + `.cu` kernels + BF16-TC, reached via `forge_dispatch_*` / `farr_*_gpu` builtins under `#ifdef HEXA_CUDA` | **run** the flame trainer fast on GPU | `hexa-lang` runtime + `stdlib/flame/flame_forge_dispatch_test.hexa` |

Rule of thumb:
- **author** anything trainable in `.hexa` using flame ops.
- **build CPU** (Mac, byte-eq verification): `HEXA_MAC_BUILD_OK=1 hexa build <f> -o <bin>`.
- **build/run GPU** (production rungs): CUDA host, `-DHEXA_CUDA`, via a dispatch
  script — forge engaged. Production rungs require GPU; verify `nvidia-smi` busy
  (`@D a_train_flame_forge`).

`flame : forge :: torch : ATen` — flame is the authoring layer, forge is the GPU
substrate it dispatches to.

## Canonical file locations

```
hexa-lang/stdlib/flame/                      ← the trainer lives HERE
├─ tensor_lib · nn_lib · ag_tape             stdlib primitives + autograd tape
├─ decoder_lib · decoder_block_lib · train_lib   transformer decoder + train loop
├─ clm_{model,train,step,qat,gen,large}.hexa CLMConvMoE flame op chain
├─ flame_d768_12L_corpus_test.hexa           decoder large (d768/12L) hand-fused GPU wall
├─ flame_d768_12L_agtape_fire.hexa           decoder large generic ag_tape GPU wall
├─ CLM_PROD_TRAINER_PLAN.md                  production trainer build plan (PR1–4)
└─ flame_forge_dispatch_test.hexa            forge GPU dispatch smoke
hexa-lang/tool/dispatch_*_gpu_fire.sh        GPU fire scripts (provision→build→run→teardown)
hexa-lang/stdlib/flame/PHASE4D_DISPATCH_CLI_GUIDE.md   runpod/vast auth + cost reference

anima/CLM/
├─ train/fire_{large,mid,3b,7b}_rung_qat.hexa   FIRE SPECs (dispatch contract + verdict path)
├─ corpus/clm_p1.corpus.kosmos                  corpus data (byte-vocab V=256)
├─ P0_ARCHITECTURE.md · CLM_FORMAT_SPEC.md       arch + .clm int4 format
└─ P6_SCALE_LADDER_7B.md                         rung ladder SSOT (mid→large→3B→7B)
```

## stdlib setup (hexa-lang)

- imports: `use "stdlib/flame/<lib>"` at the top of the trainer `.hexa`.
- build: `hexa build stdlib/flame/<trainer>.hexa -o build/<bin>` (Mac: prefix
  `HEXA_MAC_BUILD_OK=1`; CPU byte-eq path).
- GPU: compile with `-DHEXA_CUDA` on a CUDA host (the dispatch scripts do
  provision + build + supervise + teardown).
- verify (g5): `hexa verify` / the harness's own falsifier stdout is the verdict.

## Production trainer

Built per `hexa-lang:stdlib/flame/CLM_PROD_TRAINER_PLAN.md` — 4 stacked PRs:
compose loop (CPU) → `.clm` checkpoint → conv-MoE forge GPU dispatch → large
44.68M H100 fire. It composes `clm_gen` (model + autograd) · `quant_lib`/`clm_qat`
(int4 QAT) · `optim_lib` (AdamW) · the byte-vocab corpus loader, with a `.clm`
checkpoint export. Falsifier gates: `F-CLM-PROD-DESCENT` · `F-CLM-CKPT-ROUNDTRIP`
· `F-CLM-PROD-GPU-EQ` · `F-CLM-SCALE-TRANSFER` (P6 §2).

## Flow context

`LAUNCHPAD/SBS.md` rung ladder: R0–R3 landed at mid (13.65M) → **R4 launch gate =
P6 backbone production-scale** (mid 13.65M ✅ → large 44.68M → 3B → 7B), each
gated by `F-CLM-SCALE-TRANSFER`. The large fire is a runpod/forge GPU fire of the
hexa-native trainer.

## Siblings

`CLM/train/README.md` · `CLM/P6_SCALE_LADDER_7B.md` · `CLM/P4_PRODUCTION_ROADMAP.md`
· `LAUNCHPAD/SBS.md` · `project.tape @D a_train_flame_forge`.
