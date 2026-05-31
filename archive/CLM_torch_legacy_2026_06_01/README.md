# CLM torch/.py legacy — archived 2026-06-01

Tombstone for the **PyTorch / Python** CLM tooling, moved here from `CLM/**`
by `git mv` (history preserved). Nothing was deleted; this is a relocation.

## Why archived

`@D a_train_flame_forge` (project.tape, binding) mandates that **production
training is hexa-native flame + forge GPU, authored in `.hexa`** — and
explicitly forbids shipping a torch/CPU `train_clm.py` as the production
trainer. `@D a_akida_native_train` (CLAUDE.md) likewise forbids GPU/CPU
backprop training as the production path. These `.py` files were the prior
torch trainer + model + distill/measure tooling; they are superseded by the
hexa-native flame trainer and are kept here only as reference.

## Where the canonical (live) trainer lives now

The SSOT pointer is `CLM/TRAINING_SSOT.md` (anima). In short:

```
[ anima CLM/ ]  ── spec/driver/corpus (.hexa + .kosmos) ──▶ [ hexa-lang stdlib/flame ]
                                                              the actual hexa-native trainer
```

| role | canonical location |
|---|---|
| flame trainer (CLMConvMoE port) | `hexa-lang:stdlib/flame/clm_{model,train,step,qat,gen,large}.hexa` |
| flame decoder large (d768/12L) | `hexa-lang:stdlib/flame/flame_d768_12L_{corpus_test,agtape_fire}.hexa` |
| forge GPU dispatch | `hexa-lang:stdlib/flame/flame_forge_dispatch_test.hexa` · `tool/dispatch_*_gpu_fire.sh` |
| fire spec (rung dispatch contract) | `anima:CLM/train/fire_large_rung_qat.hexa` |

## Honest status of the hexa-native trainer (2026-06-01)

The hexa-native CLM trainers are **validated SMOKES / wall-measures**, not yet
a production corpus trainer:

| artifact | what it is | NOT yet |
|---|---|---|
| `clm_large.hexa` | 44.68M GRAD-EXACT + 4-step synthetic-token descent smoke | corpus loader · 2000-step · QAT envelope · checkpoint |
| `flame_d768_12L_agtape_fire.hexa` | generic ag_tape GPU wall measurement (3-step) | full convergence run |

→ The torch `train_clm.py` archived here is the only artifact that was a
*complete* corpus/QAT/checkpoint trainer. Building the hexa-native production
trainer (corpus + 2000-step + QAT + checkpoint + forge-GPU) is the open gap
before the real R4 large-rung fire. Until that lands, treat the files here as
the **reference production trainer** — do not assume the hexa smoke replaces
their full functionality yet.

## Restore

`git mv archive/CLM_torch_legacy_2026_06_01/<path> CLM/<path>` (history intact).
