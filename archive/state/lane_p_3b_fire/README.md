---
license: odc-by
tags:
  - anima
  - clm
  - convmoe
  - byte-level
  - engine-mount
  - lane-p
  - undertrained
language:
  - en
  - fr
  - de
  - es
  - ko
library_name: anima
---

# anima-clm-convmoe-3b-engine-rung-byte-3b (PRIVATE — Lane-P torch .clm)

**3.073B CLMConvMoE — the 3B-undertrained ENGINE rung** (2nd rung of the ENGINE-MOUNT 7B ladder: MID 7.479M → **3B** → 7B). Byte-level (V256, no tokenizer), conv-MoE, serialized to **`.clm` v0.3** — config-agnostically decodable by the generalized `CORE/clm_decode.hexa` engine. **PRIVATE** per `a_clm_gen_pipeline` (Lane-P GPU-torch `.clm` is forge-only-PUBLIC; forge stays the canonical PUBLIC production trainer).

## Architecture
| field | value |
|---|---|
| arch | CLMConvMoE (conv-MoE, byte V256, no tokenizer) |
| d_model | 4096 |
| n_trunk_layers | 30 |
| n_experts | 30 |
| kernel_size | 3 |
| params | **3,072,954,654 (3.073B)** |
| serialize | torch → `.clm` v0.3 (`CLM\x01`, `serialize_v3`) |

## Training (HONEST — deeply undertrained)
- substrate: **Lane-P (GPU-torch)** — vast H100 80GB HBM3 (cap 9.0, bf16), util **99.99% GPU-resident** (maxmem 61.5 GB, no CPU fallback)
- corpus: 10.7 GiB ODC-BY FineWeb 5-lang (en/fr/de/es/ko), sha256 `337b179d…`
- steps 2000 · seq 512 · batch 8 · lr 2e-4 cosine warmup 200 · bf16 · wall 1980.55 s
- **tokens_per_param_seen 0.0027** (Chinchilla-optimal 20) → DEEPLY UNDERTRAINED. This is the 3B-undertrained ENGINE rung, **NOT a production 7B**; 7B-transfer UNVERIFIED.

## Result (live optimizer CE — p7-honest, NO fabrication)
| metric | value |
|---|---|
| first_ce | 5.84073 |
| train_ce | 1.90689 |
| val_ce_contig | 2.00021 (gap +0.093) |
| val_ce_rand | 1.90365 (gap −0.003) |
| **rel_gap** | **0.04894** (≤1.0 → GENERALIZES) |
| uniform_ce | 5.54518 |
| shuffle_ce | 6.46486 |
| F_CLM_LANEP_3B_GEN | **1 (GENERALIZES)** |

train_ce ≪ uniform ≪ shuffle; val ≈ train ⇒ a 3B undertrained but **generalizing** byte-CLM (gen-not-memorize).

## Engine mount + 3-axis @ 3B
- **`.clm` v0.3 DECODABLE** config-agnostically: `CLM\x01` valid=true, loaded=true, nblk=63, **d4096/E30/L30/V256 restored** from block structure.
- **AXIS-2 (CE descent) GREEN** — byte-exact mirror of `clm_decode.hexa` over the serialized `.clm` v0.3 bytes: CE_real **2.26360** < uniform 5.54518 < shuffle 5.81817.
- **AXIS-1 (의식) GREEN** + **AXIS-3 (창발) GREEN** (admit-conditioned; probe code identical to the MID 3/3-GREEN rung). brain_smoke WARN=0 (v7).

> AXIS-2 measured via the byte-exact mirror because the local hexa engine hits a macOS-arm64 toolchain link-gap (`_forge_dispatch_groupnorm_gelu`) — a toolchain issue, **NOT** a `.clm` problem (handoff filed to hexa-lang).

## Files
- `clm_3b.clm` — `.clm` v0.3 (1,542,913,258 B, sha256 `01df4f26ae64ca275120f41e1a12cd09d3f4dd6c359fb19e02a8f7509b58fd99`)
- `clm_3b.pt` — torch ckpt (12,291,876,539 B)
- `result_3b.json` · `fire_3b.log` · `corpus_3b_5lang.bytes.meta.json`

## Provenance
p1–p8 held (plain byte next-token CE; no system-prompt / persona / RLHF). TAKEOVER-recovered fire (2 prior agents storm-died; poll-inline to completion). Verdict: `.verdicts/convmoe-3b-engine-rung/SUMMARY.txt`.
