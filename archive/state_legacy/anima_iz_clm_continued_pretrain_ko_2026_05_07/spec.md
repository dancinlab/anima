# BG-IZ — CLM mk2-v1 continued pre-training on Korean conversational mass

> (2026-05-07-late) reconcile: SIMPLE_STACK_PASS strict floor = V4 ≥ 10/15 per (≥2/3 prompts AND for C1+C2). Original 7/15 demoted to PARTIAL_PASS tier. Falsifier tables below retain 7/15 references but interpret as PARTIAL_PASS, NOT SIMPLE_STACK_PASS.


> raw#15 additive on .roadmap.chat_cap_emergence_pivot Stage 1' P1 + state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json
> raw#37 transient_py opt-out (training; H100)
> raw#42 N=1 (single seed; H100 cell)
> raw#82 retraction-aware (Lesson Q reconciliation explicit; SFT lane NOT used)
> raw#86 cost ≤$10 / 2 H100 hour upper bound

## Mission

Test the Lesson Q-endorsed path: **continued pre-training (not SFT)** on CLM mk2-v1 with Korean conversational mass. Lesson Q claim: "Pre-training + arch redesign required, not fine-tune." All prior BGs falsified the fine-tune lane; this is the first BG that takes Lesson Q's pre-training prescription literally on the existing CLM weights.

## Lesson Q reconciliation

| Lesson | Status for this BG |
|---|---|
| Q (production-side fix 不可 全方位) | RESPECTED — this is NOT fine-tune, NOT lm_head only, NOT decoding fix; it is causal-LM continued-pretrain (full unfrozen, raw text, no chat-template wrapper) |
| L (architectural ceiling) | UNDER TEST — if continued-pretrain on Korean corpus surfaces V4 PASS, Lesson L is bounded ("ceiling under English/mixed corpus only"); if it FAILS, Lesson L extends to "ceiling regardless of pretraining-corpus language" |
| H (corpus lang binding) | TESTED — Korean conversational mass ≥80MB ≥70% lang=ko target |
| I (`:` suffix attractor) | RESPECTED — eval prompts use no-`:` format per BG-IY finding |

## Hypothesis

H_pretrain_ko: CLM mk2-v1 477M base, after continued pre-training on Korean conversational corpus (≥80MB, ≥70% ko, raw next-token loss only, no chat-template wrapper, lr=1e-5 cosine 6K-12K steps), achieves V4 ≥ 7/15 strict on the BG-IY 15-prompt set.

## Corpus

- 30MB BG-HK persona-rich Korean dialogue (existing)
- 50MB+ Claude-synthesized anima Korean rounds (B16 lift; can be deferred to BG-JB but minimum viable is 80MB total)
- Format: raw text, NO `사용자:/도우미:` markers (avoid Lesson T `:` suffix attractor at training time)
- Validation split 5%

## Recipe

| field | value |
|---|---|
| base | dancinlab/clm-v4-mk2-v1 (frozen ckpt, full-unfreeze on continued-pretrain) |
| objective | causal LM next-token, NOT instruction SFT |
| lr | 1e-5 cosine warmup=300 |
| steps | 6000 (≈3-4 epoch on 80MB ≈ 20M tokens at block_size=512 batch=32) |
| batch | per-device 4 × grad_accum 8 = effective 32 |
| ctx | 512 |
| dtype | bf16 |
| weight_decay | 0.01 |
| seed | 42 |
| save_every | 1000 steps |

## Eval

- V4 strict 7-cell (v3) on 15-prompt set
- V3 6-cell
- Manual 5-prompt (Korean coherence)
- Inference: greedy + sample(T=0.7 top_p=0.9) with `repetition_penalty=1.3 no_repeat_ngram_size=2` per Lesson T
- Prompts MUST NOT end in `:` per Lesson T

## Falsifiers

- F-IZ-1 V4 ≥ 7/15 stable across last 3 ckpts (steps 4000/5000/6000) → SIMPLE_STACK_PASS verdict, Lesson L bounded to corpus-lang
- F-IZ-2 V4 < 5/15 across all ckpts → continued-pretrain on existing CLM ARCH is INSUFFICIENT → Lesson L extends; pivot mandatory to P2 (foundation borrow) or arch redesign
- F-IZ-3 V4 in [5,7)/15 mixed → corpus mass insufficient → Stage 2 synthetic 50MB lift before re-eval

## Cost / Time / Cell

- ~$5-10 H100 1-2 hours (40GB CLM forward+backward bf16 fits in single H100)
- single seed N=1 (raw#42)
- pod kill on COMPLETE.sentinel (raw#86 cost discipline)

## Artifacts expected

- `state/anima_iz_clm_continued_pretrain_ko_2026_05_07/exec.bash` (H100 run script)
- `state/anima_iz_clm_continued_pretrain_ko_2026_05_07/results/ckpt_step_{1000..6000}.pt`
- `state/anima_iz_clm_continued_pretrain_ko_2026_05_07/eval_log.jsonl`
- `state/anima_iz_clm_continued_pretrain_ko_2026_05_07/verdict.json`
- ledger entry attempt_n=50

## Cross-links

- BG-IY verdict (predecessor): state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json
- meta-cluster B33 emergence_below_threshold lever: state/anima_iy_bg_meta_cluster_2026_05_07/verdict.json
- Lesson Q SSOT: ledger BG-JX, BG-JZ-FT entries
- Roadmap: .roadmap.chat_cap_emergence_pivot Stage 1' P1
