# CLM/train — fire specs + dispatch (hexa-native flame+forge)

> ⚠ **Canonical trainer is hexa-native, in `hexa-lang:stdlib/flame`.** Read
> [`../TRAINING_SSOT.md`](../TRAINING_SSOT.md) FIRST. This dir holds the **fire
> SPECs** (`.hexa` dispatch contracts) — not the trainer itself.
> The old torch `train_clm.py` is **archived** at
> `archive/CLM_torch_legacy_2026_06_01/` (`@D a_train_flame_forge`: no torch
> production trainer · `@D a_akida_native_train`: no GPU/CPU backprop production).

## What is here

| file | role |
|---|---|
| `fire_large_rung_qat.hexa` | large d768/L12/E12 (44.68M) fire SPEC — dispatch contract + `F-CLM-SCALE-TRANSFER` gate + recover checklist |
| `fire_mid_rung_qat.hexa` | mid d512/L8/E8 (13.65M) fire SPEC (landed rung) |
| `fire_3b_rung_qat.hexa` · `fire_7b_qat.hexa` | next-rung SPECs (gated by large) |
| `h864_*.hexa` · `h874_*.hexa` · `h886_*.hexa` | per-hypothesis fire variants (self-play · self-reward · curriculum) |
| `train_clm.hexa` | ⚠ legacy driver — it shells the **archived** `train_clm.py`; superseded by the flame trainer (see SSOT) |
| `run.sh` · `job.hexa` | legacy dispatch glue for the archived `.py` payload |

A *fire SPEC* records the dispatch contract (provider · gpu · rung · steps ·
seed · arms · per-arm cmd), the pre-registered transfer gate, and the
`a_fire_recover_complete` checklist. It is the verdict-path SSOT for that rung.

## Architecture invariants (unchanged — P0)

- **byte-vocab V=256**, no tokenizer (P0 Q3). Corpus = `.kosmos` byte stream
  (`../corpus/clm_p1.corpus.kosmos`).
- **QAT toward AKIDA envelope** (P0 §9): weights int4-sym `[-7,+7]`
  per-output-channel STE (chip rejects −8); acts `step = 2^(input_bits−act_bits)`,
  `act_bits ∈ {1,2,4}`; router/readout convs are LOGITS → act-quant excluded.
  backward = STE (fp32 master, quantized forward). Inference = AKIDA-int4-only.
- **3-arm router** (P0 §3): A = entropy-reg (content axis) · B = topK+load-bal
  (routing axis) · AB = dual-axis.
- **scale-ladder** (P6 §1): tiny d64/L2/E4 · small d256/L4/E8 ·
  mid d512/L8/E8 = 13.65M · **large d768/L12/E12 = 44.68M** · 3B · 7B.
- **honest boundary**: QAT uses GPU backprop (pretrain); on-chip contextual
  adaptation is PLASTICITY edge-learn (orthogonal). Inference byte-identical.

## How to train / fire (canonical path)

```
author/build/run the flame trainer in hexa-lang (NOT here, NOT .py):
  hexa-lang/stdlib/flame/clm_*.hexa            CLMConvMoE flame port
  HEXA_MAC_BUILD_OK=1 hexa build <f> -o <bin>  CPU byte-eq verify (Mac, $0)
  tool/dispatch_*_gpu_fire.sh                  forge GPU fire (CUDA host, -DHEXA_CUDA)
```

Per `fire_large_rung_qat.hexa`: 3-arm (A/B/AB) × seed 42 × 2000 step,
verdict → `.verdicts/clm-prod-rung/large/F-CLM-SCALE-TRANSFER.txt`, then HF
upload + teardown (`a_fire_recover_complete`).

**Open gap (see SSOT §honest status):** the hexa-native trainers are currently
GRAD-EXACT smokes / GPU-wall measures — a production trainer (corpus loop +
2000-step + QAT envelope + checkpoint) must be built on flame before the real
large fire. Do **not** resurrect `train_clm.py` to shortcut this.

## Siblings

[`../TRAINING_SSOT.md`](../TRAINING_SSOT.md) (start here) ·
[`../P0_ARCHITECTURE.md`](../P0_ARCHITECTURE.md) ·
[`../CLM_FORMAT_SPEC.md`](../CLM_FORMAT_SPEC.md) ·
[`../P6_SCALE_LADDER_7B.md`](../P6_SCALE_LADDER_7B.md) ·
[`../../LAUNCHPAD/SBS.md`](../../LAUNCHPAD/SBS.md) · F-CLM-MONO = UNIVERSE H_847.
