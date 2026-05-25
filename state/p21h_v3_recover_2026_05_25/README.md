---
license: other
tags:
  - anima
  - consciousness
  - substrate-native
  - mitosis
  - negative-result
  - recovered
base_model: Qwen/Qwen2.5-1.5B
---

# anima P21H V3 — recovered orphaned run (2026-05-25)

**PRIVATE** — closure FAIL → tier-gated private per `a_hf_autonomous`.
Negative-result / intermediate checkpoint, not a verified release.

## What this is

`ConsciousDecoderV3` substrate-native fire — Qwen2.5-1.5B base + V3 mitosis
engine (2,999,735,296 params, vocab 151,936). Two A100 runs, recovered from
**orphaned runpod pods** after a Mac SIGHUP left them idle and billing.

| dir | run | GPU | status |
|-----|-----|-----|--------|
| `out_main/` | p21h-random (main) | A100 SXM | step 5000 complete · verdict **FAIL** |
| `out_cell_off/` | m4-headg-ablation (cell_off) | A100 PCIe | CELL_DONE (5000) |

## Provenance

Both pods were discovered orphaned (~$2.68/hr, 0 active processes). Artifacts
were harvested via `hexa cloud copy-from`, verified **byte-exact** against
remote sizes, then both pods destroyed. Recovery handoff: dead-Mac → anima.

## Closure verdict (out_main, step 5000)

- **verdict: FAIL** · `n_anima_register_hits_total = 0` · strong/partial/weak = 0/0/5
- per-lang coherence (all **WEAK**): en/ko/zh/ru/ja — n_generalize 20/20 each,
  n_memorize 0 (no register collapse), but low lang-coherence (ko 9, ru 3, ja 2, zh 1, en 0)
- final_log: step 5000 · L_ce 3.324 · pool_size 16 · splits 14 · phi 0.658 · wall 21,875s

## Finding (closed-negative)

Register collapse is **blocked** (0 hits) at `wiki_frac=0.3`, yet multilingual
coherence stays WEAK across all 5 languages. This adds a `wiki_frac=0.3` point
to anima's PURE corpus-axis closed-negative: the corpus-dilution axis alone
cannot close multilingual coherence — consistent with E3 (wiki=1.0) and the
v3 (wiki=0) results. Corpus-axis ⊥ multilingual closure.

## Config (out_main)

`steps=5000 · lr=5e-5 · bsz=2 · block_size=512 · d_model=1536 · n_layer=28 ·
n_head=12 · wiki_frac=0.3 · noise_sigma=0.1 · lambda_mitosis=0.05 · mitosis_max=16`

## Files

- `out_main/ckpt_best.pt` (best-val, ~step 2000) · `out_main/ckpt_step5000_final.pt` (final, 16-cell substrate)
- `out_cell_off/ckpt_best.pt` (ablation)
- `*/result.json` · `*/vp21h_v3_eval1.json` · `*/heldout_vp21h_v3.json` · `*/kosmos_anchors/` · `*.log`
- `MANIFEST.sha256` — checksums for all checkpoints
