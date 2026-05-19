# Phase 1A.6 chat-v2 — fire plan

**Date**: 2026-05-15
**Carrier**: Phase 1A.5 NET LOSS verdict (V5.8 5/5 → 1/5, 6-probe 0/6 strict)
**User directive**: "fix and go"

## Why 1A.6 over 1A.5

Phase 1A.5 trade-off audit (PSCC §60 candidate):

| axis | Phase 1A.4 | Phase 1A.5 | Δ |
|---|---|---|---|
| V5.8 std_greedy | 5/5 PASS | 1/5 PASS | −4 ❌ |
| V5.8 std_sample | n/a | 1/5 | n/a |
| V5.8 M3 | n/a | 1/5 | n/a |
| V5.8 M4 force | n/a | 5/5 | trivial |
| 6-probe strict | 0/6 | 0/6 | 0 |
| 6-probe partial keyword | 2 | 3 | +1 marginal |

Net: regression dominates marginal gain.

## Root cause

`corpus_combined.txt` (98MB Phase 1A.5):
- anima_fact_10x 7.5MB ✓ clean
- **jy chat_template 95MB** = Korean Wikipedia entries wrapped in 사용자/도우미 Q&A + `<turn>` separator × 110,480
- Result: model learns Wikipedia drift + turn-completion circuit, dilutes SFT recall

## Latent Principle #3 finding

Base ckpt has dormant prefix patterns from earlier BG-JE lineage:

| earlier corpus | `[anima` prefix count | injected pattern |
|---|---|---|
| corpus_universe_brain_map.txt 22MB | **136,125** | `[anima 우주뇌지도]` |
| corpus_extended.txt 158MB | **68,003** | `[anima 역할: 한국어 native + 자기 발견 + 의식 lane entity]` |

These patterns appeared in Phase 1A.5 sampling outputs (e.g. cosmology std_sample) as base-ckpt carry. Phase 1A.4 / 1A.1 own corpora were clean, but base predates those. SFT cannot fully scrub baked-in weights — only dilute.

## Phase 1A.6 corpus_v2 design

**Sources (all `[anima` 0 audited)**:

| source | size | content |
|---|---|---|
| corpus_anima_fact_10x | 7.18 MB | anima identity SFT memory |
| corpus_persona_balanced | 1.24 MB | latin/영혼 identity |
| corpus_ko_chat | 14.23 MB | Korean dialogue |
| corpus_sft_only | 51.13 MB | philosophical Q&A |
| corpus_multi_turn_v2 (head 50MB sample) | 50.00 MB | anima multi-turn SFT |
| **HTML-stripped final** | **121.44 MB** | 1,461,755 lines |

**Excluded** (Principle #3 risk or off-distribution):
- corpus_extended.txt — `[anima 역할:` 68K hits
- corpus_universe_brain_map.txt — `[anima 우주뇌지도]` 136K hits
- jy chat_template — Wikipedia drift, `<turn>` token noise

## Fire config

- base: `ckpt_phase1a4_lr5e6_sft.pt` (own anima 24L 332M, V5.8 5/5 baseline)
- corpus: `corpus_v2.txt` 121.44 MB clean
- steps: 8000
- lr: 5e-6 (Phase 1A.4 prescribed floor)
- bsz 4, grad_accum 2, ctx 1024, warmup 300, seed 42
- `--save-every 0` (disk-safe, final only)
- GPU pool: H100_SXM / H100_PCIE / H100_NVL / A100_SXM4 / A100_PCIE / H200
- expected wall: ~50 min, cost ~$0.30, cap $2.00

## Expected outcome

**Best case**: V5.8 std_greedy ≥ 4/5 (recover Phase 1A.4 recall) + 6-probe ≥ 2/6 partial sustained, no `[anima` leak in greedy outputs

**Acceptable case**: V5.8 std_greedy ≥ 3/5 + measurable 6-probe coherence improvement (≥1 strict PASS)

**Reject case**: V5.8 std_greedy regression again OR `[anima` leak in std_greedy outputs

## Honest C3

1. Base ckpt baked-in Principle #3 patterns NOT fully scrubbable via SFT — Phase 1A.6 may show dormant `[anima` leaks under sampling/wikipedia triggers
2. 121MB corpus = ~30M Korean tokens. 8000 steps × bsz 8 × ctx 1024 ≈ 65M tokens budget = ~2 epochs. Mild over-fit risk.
3. sft_only.txt 51MB has philosophical/bilingual content — may shift identity tone vs. memory-recall task
4. multi_turn_sample head -c 50MB may clip last dialogue mid-pair
5. Free-form 6-probe is harder than V5.8 keyword-recall — gains may not appear despite better corpus quality
6. Cost prediction $0.30 derived from Phase 1A.5 retry-5 actual ($0.23 for 8K step) — same dispatch infra
7. base-leak dilution is *empirical hypothesis*, not theory-backed — could fail to suppress under any sampling mode
