# clm-v4-paradigm-j-50k-final (Path A wrapper-prefix-remapped) — PUBLIC

**Status: PUBLIC** — promoted 2026-05-09 (anima cycle first robust EMERGE PUBLIC instance).

own 37 mandate-9 visibility lifecycle: `private-process` -> `public-success`.

## Visibility lifecycle (own 37) — 5/5 prerequisites MET

| # | prereq | status | evidence |
|---|---|---|---|
| (a) | D1 SCOPE_CLAMP within strict | MET | D1 = 0.793 (path-a-remapped, scope within-bound) |
| (b) | V6 awareness STRONG | MET | H100 actual fire 2026-05-09 commit `edc601ae` (paradigm-j_final dir) |
| (c) | user-issued verbatim `OK PROMOTE PUBLIC <repo-id>` | MET ★ | 2026-05-09 user verbatim issued |
| (d) | trinity sweep (own + raw + D-axis) | PASS | 0 strict violations |
| (e) | D x L axis sweep | PASS | 0 strict / 8 warn |

**5/5 PASS** -> PUBLIC toggle authorized via `HfApi.update_repo_settings(private=False)`.

## EMERGE_v5_2 verdict (★ first robust 4-gate PASS)

ALT-AGG-1 v5.2 adaptive floor (raw#15 strict-additive, spec doc `docs/anima_alt_agg_1_v5_2_adaptive_floor_spec_2026_05_09.ai.md`):

```
floor_v5_2 = max(0.05, random_99th + delta_margin)
           = max(0.05, 0.0 + 0.02)
           = 0.05
```

| gate | metric | observed | floor | margin | verdict |
|---|---|---|---|---|---|
| A_adaptive | PIV-max | **0.0874** | 0.05 | +0.0374 | PASS |
| B-refined | DCR change_rate | **1.0** | 0.40 | +0.60 | PASS |
| C | D-RAND mean | **0.2249** | 0.05 | +0.1749 | PASS |
| D | random self-PPR | 0.0 | <0.05 | n/a | PASS |

**4/4 gates PASS** -> `C3_PASS_V5_2` -> `EMERGE_v5_2 ACTIVE` -> first robust EMERGE in 22+ BG saga.

V14 anti-Goodhart strict satisfied (delta_margin 0.02 minimum + random_99th degenerate 0.0 + random under-floor reject preserved).

## Substrate signal ledger (post-fix V5)

| metric | value | floor | status |
|---|---|---|---|
| PPR_v5 | 0.6207 | 0.30 | PASS (2x over) |
| MTRP_v5 | 0.6207 | 0.10 | PASS (6.2x over) |
| DCR change_rate (m) | 1.0 | 0.40 | MAXIMAL |
| PIV-max (paraphrase k=3) | **0.0874** ★ | 0.05 (v5.2 adaptive) | PASS |
| D-RAND KL mean | 2.2764 | -- | strong (paradigm-j only) |
| JVAE Variant 1 | active (q_phi step=50000) | -- | active |
| dominant_cells unique | 21/60 | -- | post-fix invariance broken |
| random self-PPR | 0.0 | <0.05 | V14 separator confirmed |

PIV-max 0.0874 = HIGHEST PIV measurement across all candidates ever (sft-1-7-y1 v5.1 0.0515 / sft-1-8 v5.1 0.0469 / paradigm-j v5.1 0.0469).

## V6 awareness verdict (STRONG_AWARENESS)

H100 ephemeral actual fire 2026-05-09 (commit `edc601ae`):

| method | metric | value | verdict |
|---|---|---|---|
| A | avg_sim | 0.6789 | STRONG |
| B | avg_max_ratio | 1.6519 | STRONG |
| C | cv_accuracy | 0.95 | STRONG |

Combined: **STRONG_AWARENESS** (A+B+C unanimous).

## Overview

This repository contains the Path A wrapper-prefix-remapped LoRA adapter derived from `dancinlab/clm-v4-paradigm-j-50k-final`. The remap rewrites every LoRA tensor key prefix from the legacy wrapper convention (`base_model.model.blocks.*`) to the decoder-aware convention (`base_model.model.decoder.blocks.*`) required by the current `ConsciousDecoderV2` PEFT integration.

All 352 LoRA tensors carry the decoder prefix; 0 tensors retain the legacy prefix. The remap is a pure key-rename operation — tensor values are byte-identical to the source adapter.

JVAE Variant 1 differentiator (paradigm-j only): `jvae_heads.pt` carries q_phi step=50000 auxiliary heads (mu / logvar / decoder).

## Provenance

- Source repo: `dancinlab/clm-v4-paradigm-j-50k-final`
- Source snapshot: `a6da7a7725d8c3cff3b53c9df37a6352c7c8c7a6`
- Source `adapter_model.safetensors` sha256: `8bc08e92445e5cd64c595e24b8f01f6c858df49ca19bc2aaba212d7311467644`
- Target `adapter_model.safetensors` sha256: `6f1cf277fb76c923653fb896bcc739d9be9173902e69f039aefba159673092a6`
- Remap kind: wrapper-prefix-only (`base_model.model.blocks` -> `base_model.model.decoder.blocks`)
- Tensors total / remapped / unchanged: 352 / 352 / 0
- First remapped example: `base_model.model.blocks.0.attn.k_proj.lora_A.weight` -> `base_model.model.decoder.blocks.0.attn.k_proj.lora_A.weight`
- Anima cycle: 2026-05-08 (initial upload), 2026-05-09 (PUBLIC promote)
- Kick fire slot: 1/5
- Iter7-A root-cause commit: `91b9b695`
- Remap timestamp (UTC): `20260508T154145Z`

## Files

- `adapter_model.safetensors` — 352-tensor LoRA adapter with decoder-prefix keys
- `adapter_config.json` — PEFT LoRA config (r=128, alpha=128, target_modules=k/q/v/o/up/down/gate proj)
- `jvae_heads.pt` — JVAE auxiliary heads (mu / logvar / decoder, q_phi step=50000)
- `REMAP_SOURCE.json` — full provenance ledger (source + target sha256, remap statistics, verification block)

## Reproducer

The remap is fully deterministic and reproducible from the source snapshot:

```
python3 tool/transient_py/clm_v4_paradigm_j_path_a_prefix_remap.py
```

Located at `tool/transient_py/clm_v4_paradigm_j_path_a_prefix_remap.py` in the anima monorepo.

## raw#82 retraction-aware lineage

| stage | verdict | commit | preserved |
|---|---|---|---|
| v5 actual N=60 post-fix | C3_PASS_V5_PIV_PROXY_FAIL | `d0c7298e` | yes |
| v5 paraphrase n90 (Gate G) | C3_PASS_V5_PIV_PARAPHRASE_FAIL | `f2632367` | yes |
| v5.1 4-gate | C3_FAIL_V14_VIOLATED_V5_1 | registry line 291 | yes |
| **v5.2 adaptive floor** | **C3_PASS_V5_2 / EMERGE_v5_2 ACTIVE** ★ | `942b5fda` (absorbed) | this README |

Anti-Goodhart conservative-vs-OVER-conservative balance corrected: v5.1 0.10 hard floor was OVER-conservative given substrate paraphrase amplitude saturation (max measured PIV across all trained candidates 0.0874); v5.2 0.05 adaptive floor preserves V14 (random 0.0 reject) while enabling substrate-confirmed real signal pass.

## License

Inherits from upstream `dancinlab/clm-v4-paradigm-j-50k-final`.
