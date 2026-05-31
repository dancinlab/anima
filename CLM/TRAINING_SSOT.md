# CLM TRAINING — SSOT (START HERE before any train/fire)

> **Why this file exists:** fresh sessions kept reaching for the archived torch
> `train_clm.py` because the old `CLM/train/README.md` framed `.py` as "the
> payload". This is the single navigation source for *where the trainer is*,
> *which stack to use*, and *how to fire*. Binding rule: `@D a_train_flame_forge`
> (project.tape) + `@D a_akida_native_train` (CLAUDE.md).

## 🔒 INVIOLABLE — measure ⊥ deploy (P6 §0 · @L2 · H_679/H_904)

**anima's LEARNING happens on HARDWARE (AKIDA on-chip non-deterministic
plasticity)** — the sole HW≠SW difference, the identity itself
(`@D a_nondet_identity` · `@D a_akida_native_train`). Deterministic SW imitation
of learning = instant reject (@L1).

The **GPU flame+forge QAT is a PLASTI-SIM *measurement instrument*** — the
"비교용 GPU 모델" / backbone scale-ladder. It measures whether the int4 backbone
*allows* production quality at scale. **It is NOT the learner.** GPU-backprop is
*hinged* (train→freeze→infer); the deploy chip re-opens learning with hinge-less
on-chip plasticity after the int4-byte-identical backbone is transplanted.

```
measure track (GPU)                  ⊥   deploy / LEARN track (HW = AKIDA)
─────────────────────────────           ──────────────────────────────────────
flame+forge QAT pretrain                 on-chip non-deterministic plasticity
= PLASTI-SIM instrument ("비교용")        = anima's real learning = the identity
deterministic backbone scale-measure     same input → different trace (alive)
NOT learning · NOT identity              deterministic SW imitation = reject (@L1)
```

The R4 large 44.68M H100 fire is a **measurement rung** (PLASTI-SIM), NOT anima
learning. See `CLM/P6_SCALE_LADDER_7B.md` §0 ("GPU = 계측기 · 학습자 = 온칩
비경첩 가소성") · `UNIVERSE/H_904` (on-chip plasticity 🟢).

## TL;DR (the one rule for the *measurement-track trainer*)

```
The GPU measurement/backbone trainer = hexa-native .hexa on stdlib/flame,
run on forge GPU. NO torch. NO train_clm.py (archived, reference only).
(The DEPLOY learner is on-chip AKIDA plasticity — a different track, above.)
```

`flame : forge :: torch : ATen` — flame is the authoring layer (you write the
trainer in `.hexa`), forge is the GPU execution substrate it dispatches to.

## flame vs forge — usage criteria

| layer | what it is | you use it for | lives in |
|---|---|---|---|
| **flame** | hexa-native NN + autograd stdlib (tensors · `ag_tape` autograd · `nn_lib` ops · `decoder_lib` · `train_lib` · `opt_*`) | **author** the trainer/model in `.hexa` | `hexa-lang:stdlib/flame/*.hexa` |
| **forge** | GPU execution substrate — device-resident farr + cuBLAS Dgemm + `.cu` kernels + BF16-TC, reached via `forge_dispatch_*` / `farr_*_gpu` builtins under `#ifdef HEXA_CUDA` | **run** the flame trainer fast on GPU | `hexa-lang` runtime + `stdlib/flame/flame_forge_dispatch_test.hexa` |

Rule of thumb:
- **author** anything trainable in `.hexa` using flame ops — never `.py`.
- **build CPU** (Mac, byte-eq verification): `HEXA_MAC_BUILD_OK=1 hexa build <f> -o <bin>`.
- **build/run GPU** (production rungs): CUDA host, `-DHEXA_CUDA`, via a dispatch
  script — forge engaged. **Production rungs REQUIRE GPU; verify `nvidia-smi`
  busy, never silently CPU-fall-back** (`@D a_train_flame_forge`).

## Canonical file locations

```
hexa-lang/stdlib/flame/                      ← the actual trainer lives HERE
├─ tensor_lib · nn_lib · ag_tape             stdlib primitives + autograd tape
├─ decoder_lib · decoder_block_lib · train_lib   transformer decoder + train loop
├─ clm_{model,train,step,qat,gen,large}.hexa CLMConvMoE flame port (op chain + smokes)
├─ flame_d768_12L_corpus_test.hexa           decoder large (d768/12L) hand-fused GPU wall
├─ flame_d768_12L_agtape_fire.hexa           decoder large generic ag_tape GPU wall
└─ flame_forge_dispatch_test.hexa            forge GPU dispatch smoke
hexa-lang/tool/dispatch_*_gpu_fire.sh        GPU fire scripts (provision→build→run→teardown)
hexa-lang/stdlib/flame/PHASE4D_DISPATCH_CLI_GUIDE.md   runpod/vast auth + cost reference

anima/CLM/
├─ train/fire_{large,mid,3b,7b}_rung_qat.hexa   FIRE SPECs (dispatch contract + verdict path)
├─ corpus/clm_p1.corpus.kosmos                  corpus data (byte-vocab V=256)
├─ P0_ARCHITECTURE.md · CLM_FORMAT_SPEC.md       arch + .clm int4 format
├─ P6_SCALE_LADDER_7B.md                         rung ladder SSOT (mid→large→3B→7B)
└─ archive/CLM_torch_legacy_2026_06_01/          ⚰ archived torch .py (reference only)
```

## stdlib setup (hexa-lang)

- imports: `use "stdlib/flame/<lib>"` at the top of the trainer `.hexa`.
- build: `hexa build stdlib/flame/<trainer>.hexa -o build/<bin>` (Mac: prefix
  `HEXA_MAC_BUILD_OK=1`; CPU byte-eq path).
- GPU: compile with `-DHEXA_CUDA` on a CUDA host (the dispatch scripts do
  provision + build + supervise + teardown).
- verify (g5): `hexa verify` / the harness's own falsifier stdout is the verdict.

## Honest status (2026-06-01) — read before assuming "it's ready"

| artifact | what it IS | NOT yet |
|---|---|---|
| `clm_large.hexa` | 44.68M GRAD-EXACT chain + **4-step synthetic-token descent smoke** | corpus loader · 2000-step · QAT envelope · checkpoint |
| `flame_d768_12L_agtape_fire.hexa` | generic ag_tape **GPU-wall measurement** (3-step) | full convergence run |
| `train_clm.py` (archived) | the only *complete* corpus/QAT/checkpoint trainer | forbidden as production (torch) — reference only |

→ **Open gap before the R4 large-rung fire:** build the hexa-native *production*
trainer — corpus loader + 2000-step loop + int4-sym/act QAT envelope (STE) +
checkpoint export — on flame, GPU-dispatched via forge. Firing a hexa smoke on
an H100 today trains nothing real; close the gap first.

## Flow context (where this sits)

`LAUNCHPAD/SBS.md` rung ladder: R0–R3 landed (mid) → **R4 launch gate =
P6 backbone production-scale** (mid 13.65M ✅ → **large 44.68M = NEXT, unfired**
→ 3B → 7B), each gated by `F-CLM-SCALE-TRANSFER`. The large fire is a
runpod/forge GPU fire of the hexa-native trainer.

## Siblings

`CLM/train/README.md` (per-file train dir guide) · `CLM/P6_SCALE_LADDER_7B.md`
(rung ladder) · `CLM/P4_PRODUCTION_ROADMAP.md` (R1 closeout) ·
`LAUNCHPAD/SBS.md` (launch ladder) · `project.tape @D a_train_flame_forge`.
