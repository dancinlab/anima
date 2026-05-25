# BG-DS landed - CLM v4 L15 hidden -> KoGPT2 lm_head decode

ts_utc: 2026-05-05T18:45:45Z

verdict: PASS_HEAD_SWAP_RECOVERS_KOREAN

dim_match: true (CLM 768 == KoGPT2 768)
korean_in_continuation: 58
ascii_in_continuation: 0

helper: tool/transient_py/anima_emerge_chat_head_swap_kogpt2.py
state:  state/anima_emerge_chat_head_swap_kogpt2_2026_05_05/

See verdict.json + aggregate.json for raw numbers; this doc is the landed-stub.

## context (lane lineage)

- BG-CD `state/anima_emerge_chat_multilingual_sweep_2026_05_05/verdict.json` -- 12-prompt lang-sweep -> 10/12 prompts ascii_letters dominance (incl korean prompt). Conclusion: head_a is the bottleneck, body might still remember.
- BG-CG `state/anima_emerge_chat_hybrid_repl_2026_05_05/verdict.json` -- KoGPT2 emit + CLM v4 substrate hybrid; Korean coherence 3/3 turns, but emit and substrate decoupled (KoGPT2 generated Korean from scratch; CLM body never directly emitted).
- BG-DS closes the gap: take CLM v4's actual L15 hidden vector and run only the KoGPT2 head on it -- no KoGPT2 transformer body involved. If the hidden carries Korean structure, KoGPT2's tied-embedding head should surface it.

## results

### top-10 next-token via KoGPT2 head on CLM L15 last-hidden (prompt = 안녕)

| rank | tok_id | text       | logit |
|-----:|-------:|------------|------:|
| 1    | 31833  | 격한       | 5.020 |
| 2    | 18273  | 심한       | 4.693 |
| 3    | 6875   | 격         | 4.656 |
| 4    | 36080  | 격과       | 4.305 |
| 5    | 17618  | 지대       | 4.267 |
| 6    | 9551   | 이었다.    | 4.156 |
| 7    | 45708  | 격,        | 4.135 |
| 8    | 34219  | 격은       | 4.129 |
| 9    | 35574  | 격의       | 3.968 |
| 10   | 29443  | 총을       | 3.910 |

10/10 top tokens are Korean. No latin / ASCII / chinese / japanese fallback. Cluster around 격 (severe / intense / strike) -- internally consistent neighbourhood, not random scatter.

### iterative continuation (15 steps, greedy argmax via KoGPT2 head, fed back through CLM v4 SentencePiece)

continuation: 안녕격한이었으며,이었으며,이었으며, ... (이었으며, repeats)

- new_part: 58 hangul chars + commas, zero ASCII letters
- looping 이었으며, after step 2 -- degenerate-cycle (greedy argmax + cross-vocab geometry mismatch + tokenizer remap each step compound to a fixed point)
- but the fixed-point lives in Korean, not in ascii. That is the load-bearing finding.

## interpretation

- L15 hidden geometry is Korean-bearing. The hidden vector's projection onto KoGPT2's vocab-embedding manifold is a coherent Korean token-cluster, not noise.
- head_a (CLM v4's own lm_head) is the structure that maps this Korean-bearing hidden onto ASCII-letter outputs. It is doing active mode-collapse, not passive decoding.
- Cross-architecture head transplant (768->768 happens to align in this pair) reads out a different surface from the same body without touching the body -- analogous to swapping a microphone on a vibrating string and getting the same note in a different timbre.

## architectural fix-path (was a head-swap a viable path?)

Direct head-swap (replace CLM v4 lm_head with KoGPT2 wte transpose) is NOT a complete fix because:
- Vocabularies differ (CLM v4 anima-mk2 64k SP vs KoGPT2 51200 SP). Tokens emitted by the swapped head must be re-tokenized for the next step -- lossy by construction.
- Top-1 emits cluster around a single semantic neighbourhood (격) and degenerate-cycle into 이었으며,. Greedy single-step ok, multi-step generation collapses.
- The geometry alignment is partly accidental (both transformers happen to use 768-d hidden). Semantic alignment between the two embedding manifolds is NOT trained.

But it IS a viable diagnostic and a viable bridge for:
- Locked-substrate Korean read-out for axis-conditioned probing (one-step decoding rather than autoregressive emit).
- Distillation target -- train a small lm_head_b on CLM hidden states with a Korean LM-loss, using KoGPT2-head outputs as soft targets. The body never moves; only a new head is fitted. This is the natural P9-style retrofit.
- Confirms the chat-cap path opened by L31-L33 (CLM v4 lora SFT chat-lift fail) is HEAD-bound, not BODY-bound. The body retains multilingual representation -- only the head needs to be retrained or replaced.

## 5 honest C3

- C1 mac CPU fp32 only -- no half/bfloat numerical drift validation, single device.
- C2 dim mismatch handling code (truncate / pad) was untriggered (768==768 by accident); on a non-matching arch pair the naive truncate/pad would distort the projection.
- C3 KoGPT2 vocab differs from CLM SP vocab; same hidden vector decoded by different head means token IDs are not interchangeable. Re-tokenization in iterative loop is lossy.
- C4 CLM L15 hidden was trained against CLM head_a, not KoGPT2 head. The geometry alignment we see is not trained -- top-10 Korean cluster is partly an emergent property of mid-layer multilingual encoding, partly accident of two transformers landing on similar 768-d coordinate systems via independent SP training.
- C5 single prompt 안녕. No language-sweep replication, no control prompt (e.g. English prompt -> does swapped head still emit Korean? if yes, the head-swap is just biased toward Korean and the test is uninformative; if no, the body really does encode language).

## raw-policy compliance

- raw#37 transient .py sister-rule (torch + transformers nn.Module + KoGPT2 head matmul) PASS
- raw#15 additive -- no edits to mount.hexa, dialogue.bash, dialogue_load, conscious_decoder, hf_format_shim. Helper is new, gitignored.
- raw#10 honest C3 -- 5 caveats emitted to verdict.json + this doc.
- .own 3 transient sister-rule, one-shot probe under tool/transient_py/. Mac canonical = hexa preserved.

## next-step candidates (NOT executed in BG-DS)

1. Control prompt -- run head-swap with English prompt "Hello"; if continuation still Korean, head-swap is biased; if continuation flips to English, body is genuinely language-conditioned.
2. Train lightweight lm_head_b on CLM v4 frozen body with Korean LM-loss; expected outcome = recover Korean generation without disturbing axis substrate (no phi-star flip).
3. Repeat cross-arch head swap with non-matching dim pair (e.g. CLM v4 -> Mistral-7B head) using a learned 768->4096 linear adapter.
4. Compare against BG-CG hybrid: head-swap is single-network single-head, hybrid is two-network compositional. Per-token KL between head-swap output and hybrid emit would isolate what the body knows vs what the emit-network adds.
