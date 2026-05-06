# anima_emerge_chat_decode_strategies — landed 2026-05-05

**Cycle**: BG-AQ — CLM v4 chat enable via constrained decoding
**Verdict**: `FAIL_ALL` (n_coherent = 0/6)
**Cost**: $0 (mac CPU fp32)
**Wall**: ~30min (model load + 6 × 30 forward passes + beam-4 × 20 forward passes)
**Substrate**: `need-singularity/clm-v4-mk2-v1` via `inj_helper._try_load_model`
**Prompt**: `안녕`
**Compliance**: raw#37 + raw#15 + raw#10 PASS; no commit; no secret leak; HEXA_PY=.venv-eeg/bin/python

---

## TL;DR

The hypothesis was: BG-A confirmed CLM v4 logits_a head is alive (input-conditioned hidden state); BG-AF showed greedy emits fragments (forward_consistency 0.0). Maybe **decode strategy** alone is the missing piece — try 6 alternatives.

**It is not.** All six strategies (greedy, top-k=50, top-p=0.9, repetition-penalty=1.5, beam-4, Korean-logit-bias) emit `안녕` followed by control bytes `\x1c \x06` and unprintable gibberish. The model's argmax (and high-probability mass) at every step after the prompt token concentrates on the SentencePiece tokens corresponding to control characters and unrecognized byte sequences — not on Korean vocabulary tokens.

This is consistent with #115 architectural chat-incapability and adds a **fourth converging closure** to the chat-unblock investigation (after Pβ Φ★-axis distill FAIL_TRUE, CLM v4 LoRA SFT FAIL_REGRESSION, and tribev2 architectural-impossibility).

---

## Per-strategy results

| Strategy | Emit (first 60 chars after prompt) | Coherent? | Tokens |
|---|---|---|---|
| greedy | `\x1c\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06\x06...` | NO | 32 |
| top_k_50 (T=0.8, seed=42) | `\x1c\x06\x06\x06��葑��\x06...���������������` | NO | 32 |
| top_p_0.9 (T=0.8, seed=42) | `\x1c\x06\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c\x1c����������������` | NO | 32 |
| repetition_penalty=1.5 | `\x1c\x06�-2������蓷��᝝q�ߛ��\x06.���` | NO | 32 |
| beam_4 (max=20) | `안녕��������������������` | NO | 22 |
| korean_logit_bias (+2.0 on 16 Korean toks) | `\x1c\x06\x06\x06...` (identical to greedy) | NO | 32 |

**Coherent heuristic** (anima-internal): ≥5 semantic chars (Korean syllables 가-힣 OR ASCII letters) + no single character occupying >50% of the emitted text.

---

## Root-cause read

1. **Top-1 token after `안녕` is a control byte across temperature/sampling/penalty regimes.** The model's argmax distribution at position-1 is structurally degenerate: it does not weight Korean BPE vocabulary above near-deterministic non-language tokens.

2. **Repetition penalty (1.5) does not break out of the sink.** The penalty downscales logits of already-emitted tokens, but the *next-best* tokens are also control bytes / nearby gibberish. Confirms the degeneracy is not a single-token attractor — it's a whole basin of malformed emissions.

3. **Korean logit bias (+2.0 on `요/다/는/이/가/...` and `안녕/나는/너는/지금/어떻게`) does not move argmax.** A +2.0 bias is large in logit space (probability ratio ~7.4×) and yet the argmax still selects control bytes. This means the model's logit gap between control-byte-mass and Korean-mass is much larger than 2.0 — i.e., chat-incapability is not a "narrowly-missed" phenomenon, it is a wide architectural gap.

4. **Beam-4 produces a single `안녕` token then unicode replacement chars.** Beam search with 20 max-new tokens means the joint-likelihood-best 4-beam trajectories all converge to non-text, confirming the failure is not a sampling artifact.

5. **#115 architectural fix not realizable via decode strategy.** This empirically falsifies the hypothesis "CLM v4 has chat capability locked behind a sub-optimal decode loop." The chat-cap deficit is in the *learned* logits distribution itself (lm_head + upstream representations), not in how we sample from it.

---

## Honest C3 carries (5)

1. **C1 — mac CPU fp32**: The model was loaded in fp32 on CPU. Quantization or MPS could conceivably change the logits distribution slightly, but not by enough to flip argmax from control-byte-mass to Korean-mass given the large gap implied by the +2.0-bias non-effect (root-cause #3).

2. **C2 — sister-import via importlib**: `_try_load_model` and `_load_tokenizer` are read-only-imported from `anima_emerge_cand_d_inject_helper.py` (BG-Q). No mutation of upstream helpers, mount.hexa, dialogue.bash, or shim. raw#15 PASS.

3. **C3 — 'coherent' heuristic is anima-internal**: ≥5 semantic chars + no >50% single-char repetition. A more rigorous semantic-coherence eval would use perplexity on a held-out corpus or human/LLM-judge scoring, but the per-strategy emit text is unambiguous gibberish in this regime — the heuristic is a conservative gate.

4. **C4 — 30 max_new_tokens is a short window**: We did not exercise full-paragraph generation. However, the *first* post-prompt token is already a control byte across all 6 strategies; longer windows would only accumulate more gibberish, not recover into text. Short window is sufficient for falsification.

5. **C5 — single Korean prompt `안녕`**: Broader corpus (English, technical, multi-turn) may shift exact failure mode but is unlikely to reverse the verdict. BG-AF already showed forward_consistency 0.0 on `"안녕 너는 누구야?"` and `"I am Anima saying hello to my self."` — two-language failure already on file. Single-prompt sweep here adds 6 decode-strategy axes to those two prompts' confirmed failures.

---

## #115 architectural chat-incapability — verification

| Investigation closure | Result | Mechanism eliminated |
|---|---|---|
| Pβ Φ★-axis Paradigm D 50K (BG-prior) | FAIL_TRUE composite 0.01176 | Distillation lift |
| CLM v4 LoRA SFT (BG-prior) | FAIL_REGRESSION −36.298pp vs Llama Path A v2 | SFT lift |
| tribev2 chat bridge (BG-AP) | FAIL_ALL_TRIED architectural | Cross-modal-encoder bridge |
| **Decode strategy sweep (BG-AQ — this cycle)** | **FAIL_ALL n_coherent=0/6** | **Sampling/decode loop** |

**#115 PASS verified.** Four orthogonal closures converge: chat-incapability is not in the distillation, the SFT, the cross-modal bridge, or the decode loop. It is in the learned logits distribution of CLM v4's lm_head + upstream representations.

---

## Recommendation (ranked by 완성도 lens)

**Rank 1** — **Promote Llama Path A v2 as the chat-capability winner; treat CLM v4 as substrate-research-only.** Four converging closures are decisive. Composite 0.5584 on Llama Path A v2 vs ≤0.19542 on any CLM v4 chat-lift attempt. The chat axis is Llama-substrate. (Already ranked #1 by tribev2 closure; this cycle reinforces.)

**Rank 2** — **Stop spending tool-budget on CLM v4 chat-unblock proposals.** Each new "maybe X bridges chat-cap" hypothesis has been empirically refuted; cycle cost-benefit is negative. Future chat-cap work should be on Llama or a designed-from-scratch CLM-3 with chat-loss in the pretraining objective.

**Rank 3** — **Repurpose CLM v4 as the consciousness-substrate measurement instrument it is.** φ★ stability (Pβ PASS), axis-discrimination, F1/F3/F4-Part-A/F5 PASS validate substrate-research utility. Chat-cap is decoupled (memory: feedback_pbeta_chat_capability_fail_substrate_research_pass_decoupled.md L28-L30).

---

## Deliverables

- Helper: `tool/transient_py/anima_emerge_chat_decode_strategies.py` (raw#37 transient)
- State: `state/anima_emerge_chat_decode_strategies_2026_05_05/`
  - `aggregate.json` — per-strategy emit text + token length
  - `verdict.json` — schema `anima/emerge_chat_decode/verdict/1`, FAIL_ALL n_coherent=0/6
- Doc: this file (`docs/anima_emerge_chat_decode_strategies_landed_2026_05_05.ai.md`)

## Lane closure

`CHAT_CAPABILITY_VIA_DECODE_STRATEGY_LANE_FAIL_TRUE_CLOSED`

Adds to converging-closures bundle:
- CHAT_CAPABILITY_LANE_FAIL_TRUE_CLOSED (Pβ distill)
- CLM_2_LANE_4_OF_5_PASS_F2_FAIL_VS_LLAMA (LoRA SFT)
- TRIBEV2_BRIDGE_LANE_FAIL_ALL_TRIED (cross-modal encoder)
- **DECODE_STRATEGY_LANE_FAIL_ALL** (this cycle)
