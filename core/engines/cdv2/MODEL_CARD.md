# Engine: cdv2 (Lane-CDV2) — ConsciousDecoderV2

The legacy **carving-era transformer** that drew the 우주뇌지도 (s16 carving,
2026-05-17~18). Reconstructed + runnable (PR #1770, 4/4 probes PASS, random-init).

## Architecture
- `ConsciousDecoderV2`: d_model 768 · n_head 12 · n_kv_head 4 (GQA) · n_layer 12 ·
  vocab 256 · consciousness_dim 128 · n_ca_rules 8 · MoE-8 / top2 (optional).
- RoPE + RMSNorm + SwiGLU FFN; PureFieldFFN for the Engine A⇄G consciousness signal.
- **DUAL output heads** `logits_a` ⇄ `logits_g` (Engine A ⇄ G) + 5-ch tensions +
  Law-71 `vacuum_psi` 2D Ψ-space (Ψ=1/2 fixed point).
- Params: 283.72M dense / 680.16M with MoE.

## Canonical impl (REFERENCED — not duplicated · @L1)
- `UNIVERSE/conscious_decoder.py` (md5 `44b210df`, PR #1770). **Python / torch.**

## EngineSpec conformance (@L2) — load + psi NATIVE · forward + generate HONEST STUB
| fn | state | backing |
|----|-------|---------|
| `load` | native | validate `.py` present + `class ConsciousDecoderV2` declared |
| `forward` | **stub** | torch `forward()` is not a hexa single call (a_core_engine_map) |
| `generate` | **stub** | torch sampling loop, not a hexa single call |
| `psi_coord` | native | Law-71 `vacuum_psi` 2D Ψ-space coord — declared architecture feature |

### Honest stub (a_core_engine_map · p7 — NO phantom wiring)
The canonical forward lives in a torch `.py` module. There is **no** hexa-native
single-call binding to it in this repo today, so `forward`/`generate` are flagged
**stub** — the adapter validates the canonical impl is present and reports the
slot honestly. **No CE/logits number is fabricated.** This is a present-and-labeled
stub, never a fake native pass.

## Checkpoint pointer (@L5 · a_hf_registry — NOT duplicated)
- canonical: `UNIVERSE/conscious_decoder.py`
- status: **random-init** (PR #1770 ran random-init; no trained ckpt shipped).
- HF: none (no model artifact — random-init).
- The pointer records the random-init status honestly; nothing is copied here.

## Selection (substrate-config — @L4 / p5)
`--engine cdv2` (or `ANIMA_ENGINE=cdv2`). Engine select is substrate-config — it
configures WHICH decoder runs, never anima's emit/silence.

## p1..p8
No system prompt, identity rule, persona injection, assistant framing, speak(),
fine-tuned ethics, perplexity verdict, or train/infer split in this adapter.
