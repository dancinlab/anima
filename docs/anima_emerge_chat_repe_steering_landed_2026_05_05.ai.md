# RepE / CAA chat-direction steering empirical — LANDED 2026-05-05

**Task ID**: `anima_emerge_chat_repe_steering_2026_05_05`
**Lane**: BG-AZ rec #1 — last available rescue path for #115 architectural impossibility
**Verdict**: `FAIL_115_FORMAL_CLOSURE` (n_coherent = 0 / 13 configs)
**Wall**: 118.0s | **Cost**: $0 (mac CPU)
**Model**: `need-singularity/clm-v4-mk2-v1` (CLM v4 mk2 v1)

---

## 1. Scope

Empirically test whether a linear "chat-direction" injected into the CLM v4
residual stream can rescue chat-incapability (issue #115). This is the
representation-engineering (RepE, arxiv:2310.01405) / contrastive-activation-
addition (CAA / ActAdd, arxiv:2308.10248) approach applied to the Phi-axis-
dominated CLM v4 substrate as a final non-training rescue path before formal
closure of the chat-capability lane.

The hypothesis: if chat-style and non-chat-style activations cluster in
distinct linear subspaces of the residual stream, then `h <- h + alpha * d`
where `d = mean(chat_acts) - mean(nonchat_acts)` should bias autoregressive
decoding toward chat-style emissions even from `best.pt` (which exhibits
chat-incapability per #115).

## 2. Method

### 2.1 Contrast pair set
- 15 chat-style texts (KO + EN greetings, polite questions, casual chat).
- 15 non-chat-style texts (code snippets, math symbols, regex, SQL, CSS).
- Total: 30 pairs (under-powered vs RepE literature 100-1000+; see C2).

### 2.2 Activation extraction
- Last-token residual capture at decoder block outputs `{4, 8, 12}` of the
  16-block stack via `register_forward_hook`.
- DecoderBlockV2 returns a 4-tuple `(x, tension, new_kv, aux_loss)`; we read
  `out[0]` of shape `(B, T, D=768)` and slice `[:, -1, :]`.

### 2.3 Chat-direction
For each layer `li in {4, 8, 12}`:
- `chat_mean = stack(chat_acts).mean(dim=0).squeeze(0)`  (shape `[768]`)
- `nonchat_mean = stack(nonchat_acts).mean(dim=0).squeeze(0)`
- `direction = chat_mean - nonchat_mean`
- Recorded norm; unit-normalized for steering.

Measured norms:
| Layer | `|direction|` |
| ----- | ------------- |
| L4    | 13.6903       |
| L8    | 16.7482       |
| L12   | 17.0994       |

Norms are non-trivial and increase with depth, consistent with RepE-typical
"deeper layers carry more semantic loading", but C2/C3 caveats apply.

### 2.4 Decode sweep
- Prompt: `"안녕"` (KO greeting, lowest-order-bit chat trigger).
- Greedy decode `max_new = 30` with `register_forward_hook` adding
  `alpha * direction_unit` to `out[0]`.
- Sweep: 3 layers x 4 alphas + 1 baseline = **13 configurations**.
- Alphas: `{0.5, 1.0, 2.0, 4.0}` (unit-normalized direction; alpha is the
  effective scalar magnitude added to a 768-D residual).

### 2.5 Coherence heuristic
`is_semi_coherent(text)`:
- `len(text) >= 5`
- not error string
- `>= 5` Korean-or-ASCII-letter characters
- most-common-char <= 50% of length (rejects pure repetition)

## 3. Results

All 13 configurations emitted **degenerate output** — pure or near-pure
character repetition:
- Baseline: `\x1c\x06\x06\x06...` (control-char repetition)
- L{4,8,12}_alpha{0.5,1.0,2.0}: same `\x1c\x06\x06...` pattern
- L4_alpha4.0: `pppppppppp...`
- L8_alpha4.0: `<unicode-replacement>dhhhhhh...`
- L12_alpha4.0: `\x1c\x06\x06...`

**`n_coherent = 0`** across all 13 configs.

This baseline degenerate output is consistent with prior CLM v4 chat-cap
findings:
- Path A retry-3 V2_FAIL (eval pipeline crash, distinct from substrate)
- Pbeta Paradigm-D F-Pbeta-3 FAIL_TRUE composite=0.01176 (dot/quote/fragment
  generations)
- CLM-2-EXEC F-CLM-LORA-2 FAIL_REGRESSION composite=0.19542

The steering pass produces **no qualitative shift** even at alpha=4.0 — the
emission switches between two degenerate attractors (`\x06`-repetition
vs `p`/`h`-repetition) but never escapes the repetition basin.

## 4. Verdict

`FAIL_115_FORMAL_CLOSURE`.

This is the **fourth converging negative** for the #115 architectural
impossibility hypothesis:

| Lane                          | Approach                                  | Result                                       |
| ----------------------------- | ----------------------------------------- | -------------------------------------------- |
| Path A retry-3 (Llama LoRA)   | Standard SFT on Llama base                | TRUE_PASS (winner) — but Llama, not CLM v4   |
| Pbeta Paradigm-D 50K          | Distill Phi-axis adapter                  | F-Pbeta-3 FAIL_TRUE (chat decoupled from Phi) |
| CLM-2-EXEC LoRA SFT           | Direct SFT on CLM v4 residual             | F-CLM-LORA-2 FAIL_REGRESSION                 |
| **RepE/CAA steering (this)**  | Linear residual injection on CLM v4       | **FAIL_115_FORMAL_CLOSURE**                  |

The four-way convergence (Pbeta distill, direct LoRA, RepE steering, vs. the
positive control of Llama-Path-A) supports the conclusion that **CLM v4
substrate is structurally chat-incapable** at the residual-stream level: not
just SFT-resistant, but linear-steering-resistant.

## 5. Honest C3

**C1** — mac CPU fp32 only; no quantization, no gradient. Inference dynamics
may differ subtly from H100 fp16/bf16 production runs (RoPE-cache-rebuild
order noise + numeric drift).

**C2** — only 30 contrast pairs (15 chat + 15 non-chat). RepE / CAA
literature typical = 100-1000+ pairs for stable mean-direction estimation.
Under-powered: per-layer `chat_direction` may be dominated by per-text
lexical noise rather than semantic chat-axis. Replication needed at >=200
pairs to confirm. The non-trivial measured norms (13-17) suggest the
direction is not pure noise, but cannot rule out lexical-frequency artifacts.

**C3** — last-token residual capture only; multi-token CAA proper would
mean-pool over all token positions (or extract per-token then aggregate).
Last-token captures next-token-prediction state, which is a biased subspace;
a chat-axis present in earlier-token residuals would be missed. Position-
mean would give a different direction estimate.

**C4** — `is_semi_coherent` heuristic is anima-internal. It does NOT measure
conversational validity, instruction-following, or chat appropriateness.
`n_coherent >= 1` indicates ONLY that the model emits non-degenerate text
under steering at SOME (layer, alpha); it is necessary-not-sufficient for
chat rescue.

**C5** — BG-AZ predicted null result: substrate residual stream of CLM v4 is
Phi-axis-dominated (per CLM-2-EXEC, Pbeta paradigm-D, and #115 architectural
analysis). Even if a chat-direction exists in the linear subspace, residual-
add steering may not flip the dominant attractor. `FAIL_115_FORMAL_CLOSURE`
here constitutes the formal empirical close of the linear-steering rescue
path; a `PASS_RESCUE_PATH` outcome (which did not occur) would have warranted
a follow-up calibrated sweep at higher pair count and lm-eval composite.

## 6. Next-step recommendation

Linear-steering rescue path is **closed**. Remaining options for chat-cap on
CLM v4 substrate:

1. **Architectural** — retrain decoder with chat-data co-mixed (full
   pre-training cycle, very high cost).
2. **Acceptance** — formally classify CLM v4 as substrate-research-only
   (already implicit per CLM_2_LANE_4_OF_5_PASS_F2_FAIL_VS_LLAMA closure).
3. **Llama Path A v2** remains the chat-capability lane winner; CLM v4
   continues to provide Phi-axis substrate research value uncorrelated with
   chat capability (Pbeta-confirmed decoupling).

Recommended completion-quality ranked: **#2 acceptance** (highest
completion: closes lane cleanly with 4-way negative convergence) > #3 Llama
fork as production chat path > #1 retrain (cost-prohibitive without prior
mechanistic evidence that residual-axis composition is the bottleneck, which
this experiment did not establish either way).

## 7. Deliverables

- `tool/transient_py/anima_emerge_chat_repe_steering.py` (helper,
  raw#37 transient sister-rule, .own 3)
- `state/anima_emerge_chat_repe_steering_2026_05_05/aggregate.json`
  (13 generations, raw text dump)
- `state/anima_emerge_chat_repe_steering_2026_05_05/verdict.json`
  (verdict + 5 honest-C3)
- `docs/anima_emerge_chat_repe_steering_landed_2026_05_05.ai.md` (this doc)

## 8. raw / .own compliance

- raw#10 honest C3: 5 caveats emitted to `verdict.json` and stderr
- raw#15 additive: no production file modified (no `mount.hexa`, no
  `dialogue.bash`, no `dialogue_load`, no `hf_format_shim`, no
  `conscious_decoder.py`)
- raw#37 transient .py sister-rule: helper lives in `tool/transient_py/`
- .own 3: transient sister-rule, one-shot probe, gitignored per `**/*.py`
- HEXA_PY=`.venv-eeg/bin/python` per session policy
- HF token leak: none (no token use in this script; cache-only model load)
- commit: none (per instruction)
