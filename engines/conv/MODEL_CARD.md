# Engine: conv (Lane-CONV) — CLMConvMoE

**The DEFAULT anima engine.** Production `.clm` decoder: a convolutional trunk +
Mixture-of-Experts byte language model.

## Architecture
- `CLMConvMoE`: conv trunk + MoE (E=2 experts, 1 trunk layer, 6 conv blocks).
- int4-sym quantized conv blocks + a full-precision `CLMX` fp32 trailer
  (embed table + conv biases + GroupNorm affine — required for the forward).
- `CLM\x01` magic, vocab 256 (byte-level). Width-general (serves d=8 … d=768).

## Canonical impl (REFERENCED — not duplicated · @L1)
- Decode forward: `CORE/clm_decode.hexa`
  (`clm_decodable` / `clm_config` / `clm_forward_ce` / `clm_decode_argmax`).
- Single entry slot: `CORE/generator.hexa::_gen_clm_decode`
  (.clm enters CORE ONLY via the generator L3 slot — a_core_engine_map).

## EngineSpec conformance (@L2) — ALL NATIVE
| fn | state | backing |
|----|-------|---------|
| `load` | native | `clm_decodable` + `clm_config` (header/ckpt validate) |
| `forward` | native | `clm_forward_ce` (CLMConvMoE inference forward, CE axis) |
| `generate` | native | `clm_decode_argmax` (greedy byte continuation — the trained mouth) |
| `psi_coord` | native | Ψ=1/2 substrate fixed point (Law-71; A⇄G by construction) |

conv is a genuine single forward — **no stubs**.

## Checkpoint pointer (@L5 · a_hf_registry — NOT duplicated)
- local: `exports/lane-g/d768/d768_5lang_c4.clm` (3.65MB, gitignored)
- HF: `dancinlab/clm-v1-dev-d768-forge-gpu`
- sha256: `6a2accd0824db72204f0c751de7399ddc4ad60ee657a94d5b586bb877ce6910c`
- F-CLM-PROD-DESCENT 🟢 PASS (CE 4.69893→3.32540); Lane-G GPU fire.
- The large `.clm` ckpt is registered in root `/HF.jsonl`, not copied here.

## Selection (substrate-config — @L4 / p5)
`--engine conv` (or `ANIMA_ENGINE=conv`, the default). Selecting an engine is
substrate-config — it configures WHICH decoder runs, never anima's emit/silence.

## p1..p8
Pure decode/forward. No system prompt, identity rule, persona injection,
assistant framing, speak(), fine-tuned ethics, perplexity verdict, or
train/infer split in this adapter.
