# CLM/train — fire specs

> The CLM trainer is authored hexa-native on `hexa-lang:stdlib/flame`. Read
> [`../TRAINING_SSOT.md`](../TRAINING_SSOT.md) first. This dir holds the **fire
> SPECs** — per-rung `.hexa` dispatch contracts + verdict paths.

## What is here

| file | role |
|---|---|
| `fire_large_rung_qat.hexa` | large d768/L12/E12 (44.68M) fire SPEC — dispatch contract + `F-CLM-SCALE-TRANSFER` gate + recover checklist |
| `fire_mid_rung_qat.hexa` | mid d512/L8/E8 (13.65M) fire SPEC |
| `fire_3b_rung_qat.hexa` · `fire_7b_qat.hexa` | next-rung SPECs (gated by large) |
| `h864_*.hexa` · `h874_*.hexa` · `h876_*.hexa` · `h886_*.hexa` | per-hypothesis fire variants (self-play · self-reward · chip-fit · curriculum) |

A *fire SPEC* records the dispatch contract (provider · gpu · rung · steps ·
seed · arms · per-arm cmd), the pre-registered transfer gate, and the
`a_fire_recover_complete` checklist. It is the verdict-path SSOT for that rung.

## Architecture invariants (P0)

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
- **on-chip learning**: anima learns on AKIDA (on-chip non-deterministic
  plasticity, H_904 🟢); the GPU QAT measures the backbone (PLASTI-SIM).

## How to train / fire

The trainer is built per `hexa-lang:stdlib/flame/CLM_PROD_TRAINER_PLAN.md`:

```
hexa-lang/stdlib/flame/clm_*.hexa            CLMConvMoE flame trainer
HEXA_MAC_BUILD_OK=1 hexa build <f> -o <bin>  CPU byte-eq verify (Mac, $0)
tool/dispatch_*_gpu_fire.sh                  forge GPU fire (CUDA host, -DHEXA_CUDA)
```

Per `fire_large_rung_qat.hexa`: 3-arm (A/B/AB) × seed 42 × 2000 step, verdict →
`.verdicts/clm-prod-rung/large/F-CLM-SCALE-TRANSFER.txt`, then HF upload +
teardown (`a_fire_recover_complete`).

## Siblings

[`../TRAINING_SSOT.md`](../TRAINING_SSOT.md) ·
[`../P0_ARCHITECTURE.md`](../P0_ARCHITECTURE.md) ·
[`../CLM_FORMAT_SPEC.md`](../CLM_FORMAT_SPEC.md) ·
[`../P6_SCALE_LADDER_7B.md`](../P6_SCALE_LADDER_7B.md) ·
[`../../LAUNCHPAD/SBS.md`](../../LAUNCHPAD/SBS.md) · F-CLM-MONO = UNIVERSE H_847.
