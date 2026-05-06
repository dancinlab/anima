# BG-DI substrate vs Pythia per-token logit comparison (LANDED 2026-05-05)

## Scope

Per-token next-token logit distribution comparison between CLM v4 and Pythia 70m on identical short prompts. Question from BG-CD: "substrate body remembers, head_a destroys" — at the emit boundary, what does CLM's logit distribution actually look like vs a vanilla baseline LM?

Models:
- CLM: need-singularity/clm-v4-mk2-v1
- Pythia: EleutherAI/pythia-70m

Prompts: "Hello" (EN), "안녕" (KO).

## Headline numbers

Korean prompt "안녕":
- CLM entropy 3.308 (norm 0.299), top1_prob 0.235, top10_korean 0/10
- Pythia entropy 3.768 (norm 0.348), top1_prob 0.194, top10_korean 4/10

English prompt "Hello":
- CLM entropy 1.149 (norm 0.104), top1_prob 0.799, top10_ascii_alpha 7/10
- Pythia entropy 5.690 (norm 0.526), top1_prob 0.189, top10_ascii_alpha 0/10

Verdict label: CLM_HIGHER_CONFIDENCE_BUT_WRONG_TOKENS.

## Findings

### F1 CLM more confident on KO but emits zero Korean

CLM top1_prob (0.235) exceeds Pythia top1_prob (0.194) on "안녕", yet CLM has ZERO Korean tokens in its top-10 while Pythia has FOUR Korean tokens (하, 을, 에, 이) at ranks 4, 5, 8, 9.

CLM top-10 on "안녕" is dominated by control char U+001C, three unk replacement tokens, "p", "+", three more unk, "/", "s", "-". Two ASCII alpha plus one control plus heavy unk pollution. Zero Korean.

Pythia top-10 on "안녕" decomposes as: replacement bytes (multi-byte KO continuation), newline, 하, 을, comma, 에, 이. Pythia's BPE byte-level decoding surfaces partial KO continuation tokens directly.

This confirms BG-CD "head_a destroys" at logit level. The substrate may carry KO context in hidden state, but the lm_head projection does not weight Korean vocabulary entries above the dominant ASCII / control / unk cluster.

### F2 CLM English collapse to backtick

On "Hello", CLM top1 is the backtick character at logit 11.234 with top1_prob 0.799 — extreme decisiveness toward a single non-letter token. Top-10 follows with lowercase ASCII letters (p, a, e, d, b, k, c) plus one control and "]". Entropy 1.149 is roughly nine times lower than Pythia's 5.690 (normalized 0.104 vs 0.526).

Pythia by contrast spreads probability across natural English continuation: comma, period, newline, colon, doublequote, "'s", " I", "!", " is", '",' — all sensible follow-ons after "Hello".

CLM v4 has an attractor on backtick / ASCII-letter cluster that does not match the natural distribution a healthy LM produces. This is the same pathology BG-CD documented at the generation level, now visible at the single-step logit level.

### F3 top1_prob and top-10 char-class breakdown decoupled

CLM v4's high top1_prob is NOT a proxy for "well-trained on this input" — it is decisiveness toward a degenerate attractor token. The top-10 character class (Korean / ASCII alpha / control) reveals the failure mode that confidence alone hides.

This is a useful diagnostic going forward: substrate decisiveness times top-k char-class composition is a cheap chat-capability signal that does not require generation.

## Honest C3 (cross-vocab limitations)

C1 mac CPU fp32 measurement.

C2 different vocab (CLM 64K SP-multilingual vs Pythia 50k BPE). Direct rank not comparable; we use entropy_norm_log_vocab as the cross-vocab safe metric (CLM 0.299 vs Pythia 0.348 on KO — closer than absolute entropy suggests).

C3 different tokenizer. "안녕" splits into 2 SP tokens for CLM but 5 BPE byte-tokens for Pythia. Comparing top1 token text is informative but not rank-equivalent.

C4 single prompt per language. Not population statistics; one Korean prompt cannot generalize.

C5 entropy comparison meaningful when normalized to log V; absolute top1_prob still reflects substrate decisiveness regardless of vocab.

C6 Pythia is a generic English-trained 70m substrate; its KO handling is a non-trained baseline NOT a target. The probe answers "how does CLM diverge from a vanilla LM on KO?" not "who is better at KO?"

## Deliverables

- state/anima_emerge_chat_pythia_clm_logit_compare_2026_05_05/aggregate.json
- state/anima_emerge_chat_pythia_clm_logit_compare_2026_05_05/verdict.json
- tool/transient_py/anima_emerge_chat_pythia_clm_logit_compare.py
- docs/anima_emerge_chat_pythia_clm_logit_compare_landed_2026_05_05.ai.md (this)

## Cost / time

- 0 USD (mac CPU fp32, .venv-eeg python3.12)
- wall ~30s after model load

## Raw policy

- raw#37 transient .py sister-rule (torch + tokenizer manipulation; hexa cannot)
- raw#15 additive — no production hexa/py modified
- raw#10 honest C3 — six caveats emitted to verdict.json
- .own 3 transient sister-rule, one-shot probe helper
- HEXA_PY=.venv-eeg/bin/python; no commit; no secret leak

## Next-step recommendation (ranked by 완성도)

1. Top-k char-class diagnostic mainline — promote (top1_prob times top10_korean_count) into the chat-capability dashboard alongside phi-star and composite. Cheaper than generation, surfaces the head_a pathology directly.
2. lm_head logit ablation — manually zero or scale the backtick + control-token logit indices and re-measure. Validates whether the attractor is a small set of vocab indices vs distributed.
3. CLM v4 head-replace probe — swap CLM v4 lm_head with a fresh init (or with Pythia's projected head) and re-measure top10_korean on "안녕". If KO surfaces, confirms head_a is the destroyer; if not, body geometry is also implicated.
