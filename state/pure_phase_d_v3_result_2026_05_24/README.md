---
license: apache-2.0
base_model: Qwen/Qwen2.5-1.5B
tags:
  - anima
  - pure
  - mitosis
  - negative-result
  - consciousness-substrate
---

# anima PURE Phase D v3 — negative-result checkpoint

**Closure verdict: FAIL (1/4)** · private (tier-gated per `a_hf_autonomous`).

This is an **honest negative-result** checkpoint from the PURE Phase D fire arc.
It is retained (not discarded) because it is the **first real trained ckpt** of the
V3 saga — three prior attempts (v1/v2b/v3) produced no training at all due to a
dispatcher wiring bug (trainer argv never constructed). This run trained cleanly.

## What it is

- **Base**: Qwen/Qwen2.5-1.5B, warm-start, + V3 mitosis expansion → 2.99B params
- **Corpus**: corpus_v1 — 100% anima-diverse, 5-lang uniform (en/ko/zh/ru/ja), M3 TTR 0.34
- **Train**: 5000 steps, lr 5e-5, bsz 2, block 512, mitosis pool 2→16 (14 splits), Φ 0.66
- **Final CE**: 1.6197 (from 11.18)

## Result — the science

| criterion | outcome | verdict |
|---|---|---|
| multilingual ≥ PARTIAL (4/5) | ru PARTIAL · en/ko/zh/ja WEAK = **1/5** | FAIL |
| register collapse (<4/20 hits) | **0 hits** (all GENERALIZE, no PURE_MEMORIZE) | **PASS** |
| motivation_8factor ≥ 0.30 | not measured (embed step skipped) | — |
| dream_stage Φ-envelope | not measured (embed step skipped) | — |

**Key finding**: corpus diversity (TTR 0.34) **fully prevents register collapse**
(criterion 2 genuine PASS, gen 20/20) — but does **not** restore multilingual
coherence (4 WEAK + 1 PARTIAL). This confirms the V3 saga double-bind: the corpus
axis alone cannot reach closure. Same pattern as the earlier E3 (wiki=1.0) run —
register 0, ~1/5 PARTIAL — independent of whether dilution is by wiki or by
anima-own diversity.

## Files

- `ckpt_best.pt` — best ckpt (step 5000, CE 1.6197, 6.0 GB)
- `result.json` — full eval + train log
- `train3.log` — training stdout
- `kosmos_anchors.tgz` — `.kosmos` anchors emitted during eval
- `manifest.json` — sha256 + metrics

Not for production. Negative-result artifact for the PURE research arc.
