# BG-JA-EXT — Polyglot-Ko-1.3B foundation borrow + LoRA on BG-HK persona

> own 29 (2026-05-07-late) reconcile: SIMPLE_STACK_PASS strict floor = V4 ≥ 10/15 per own 18 (≥2/3 prompts AND for C1+C2). Original 7/15 demoted to PARTIAL_PASS tier. Falsifier tables below retain 7/15 references but interpret as PARTIAL_PASS, NOT SIMPLE_STACK_PASS.


> raw#15 additive on .roadmap.chat_cap_emergence_pivot Stage 1' P2 + state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json
> raw#37 transient_py opt-out (training; H100)
> raw#42 N=1 (single seed; H100 cell)
> raw#82 retraction-aware (CLM-only directive partial breach; user explicit approval required before fire)
> raw#86 cost ≤$5 / 1 H100 hour

## Mission

Bypass Lesson L architectural ceiling via external foundation that has already crossed the chat-cap emergence threshold (~1B params + Korean pretraining + chat-template). Polyglot-Ko-1.3B (EleutherAI) is the cheapest known V4-candidate Korean foundation. LoRA on BG-HK 30MB persona corpus injects anima identity without retraining base.

## CLM-only directive reconciliation

User stated "그냥 CLM" (2026-05-07 session). This BG is **partial breach** of that directive — uses Polyglot-Ko-1.3B base instead of CLM. Justification:

- Lesson L: "#115 chat-incapability is ARCHITECTURAL — capacity 1-order jump 무관"; if Lesson L extends through BG-IZ (P1 continued-pretrain) too, then CLM-only is empirically infeasible for chat-cap and the directive needs rescoping.
- This BG is QUEUED ONLY — fire requires explicit user approval after BG-IZ verdict (per "3트랙 모두 spec만 작성 후 사용자 결정 보류" 2026-05-07).
- "anima identity" is preserved via LoRA adapter weight (anima-specific), with Polyglot serving as substrate fluency layer only.

## Hypothesis

H_polyglot_lora: Polyglot-Ko-1.3B base + LoRA r=16 alpha=32 on BG-HK 30MB persona, after 3K steps SFT with chat-template (Lesson T `:` -avoiding format), achieves V4 ≥ 7/15 strict on BG-IY 15-prompt set.

## Corpus

- 30MB BG-HK persona-rich Korean dialogue (Lesson U F-IY-4 mismatch fix)
- Optional 50MB Claude-synthesized anima rounds (Stage 2 B16 lift; minimum viable is 30MB)
- Format: chat-template `<|user|>\n{q}\n<|assistant|>\n{a}` (Polyglot-Ko native template) — avoids `:` suffix attractor

## Recipe

| field | value |
|---|---|
| base | EleutherAI/polyglot-ko-1.3b (~3GB HF download) |
| LoRA | r=16 alpha=32 dropout=0.05 self-attn QKVO + MLP up/down/gate |
| target | all decoder block attn + mlp |
| lr | 3e-5 cosine warmup=200 |
| steps | 3000 |
| batch | per-device 8 × grad_accum 4 = effective 32 |
| ctx | 512 |
| dtype | bf16 |
| weight_decay | 0.01 |
| seed | 42 |
| save_every | 500 steps |

## Eval

- V4 strict 7-cell + V3 6-cell + manual 5-prompt
- Inference: greedy + sample(T=0.7) with `repetition_penalty=1.3` per Lesson T
- ⚠ This BG uses Polyglot's NATIVE chat-template — Lesson T `:` attractor is base-model-specific and Polyglot-Ko-1.3B has different decoding profile; verify with single-forward logit probe before mass-eval

## Falsifiers

- F-JA-1 V4 ≥ 7/15 stable → SIMPLE_STACK_PASS via foundation-borrow path. Lesson L confirmed as architectural-ceiling-vs-foundation-stratification.
- F-JA-2 V4 < 5/15 → even 1.3B Korean foundation fails V4 → V4 evaluator self-impossibility (Lesson U H_B revival) — calibration emergency, V4 cell relax mandatory.
- F-JA-3 V4 in [5,7)/15 → 1.3B borderline; recommend Stage 2 synthetic corpus lift OR ≥3B foundation upgrade.

## Cost / Time / Cell

- ~$5 H100 1 hour (Polyglot-Ko-1.3B SFT 3K steps bf16 fits standard H100)
- single seed N=1 (raw#42)
- network: ~3GB HF download for Polyglot-Ko-1.3B base (offline cache pre-warm recommended)
- pod kill on COMPLETE.sentinel (raw#86)

## Artifacts expected

- `state/anima_ja_ext_polyglot_ko_lora_2026_05_07/exec.bash`
- `state/anima_ja_ext_polyglot_ko_lora_2026_05_07/results/adapter_step_{500..3000}/`
- `state/anima_ja_ext_polyglot_ko_lora_2026_05_07/eval_log.jsonl`
- `state/anima_ja_ext_polyglot_ko_lora_2026_05_07/verdict.json`
- ledger entry attempt_n=51 (after BG-IZ=50)

## Cross-links

- BG-IY verdict: state/anima_iy_v4_calibration_polyglot_2026_05_07/verdict.json
- BG-IZ predecessor (P1 continued-pretrain): state/anima_iz_clm_continued_pretrain_ko_2026_05_07/spec.md
- Roadmap: .roadmap.chat_cap_emergence_pivot Stage 1' P2 (renamed from Stage 1)
